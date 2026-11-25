"""Small, sequential Moss probes. Running live modes may spend credits."""
import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request
from scripts.evidence import redact, parse_sse, first_sentence_ms

BASE = 'https://inference.moss.dev/v1'
ALLOWED_HEADERS = {'content-type', 'x-moss-request-id', 'x-moss-retrieve-ms', 'idempotent-replayed', 'retry-after'}
TERMINAL = {'completed', 'failed', 'cancelled'}

def clean_headers(headers):
    return {k.lower(): v for k, v in headers.items() if k.lower() in ALLOWED_HEADERS}

def valid_task_id(value):
    return isinstance(value, str) and re.fullmatch(r'task_[0-9a-f]{32}', value) is not None

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def task_payload():
    return {'goal': 'Read the page and report its title and the first paragraph. Do not visit any other site.',
            'environment': {'type': 'browser', 'start_url': 'https://example.com'},
            'model': 'moss-fast', 'limits': {'max_runtime_seconds': 60, 'max_cost_usd': 0.05},
            'output_schema': {'type': 'object', 'properties': {'title': {'type': 'string'}, 'paragraph': {'type': 'string'}}, 'required': ['title', 'paragraph']}}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('case', choices=['inference', 'invalid-inference', 'stream', 'invalid-task', 'task'])
    p.add_argument('--balance-checked', action='store_true', help='Confirm included credit balance and auto-reload were checked manually; not a spending cap')
    args = p.parse_args()
    if not args.balance_checked:
        p.error('Check remaining included credits and auto-reload first, then pass --balance-checked')
    project, key = os.getenv('MOSS_PROJECT_ID'), os.getenv('MOSS_PROJECT_KEY')
    if not project or not key:
        p.error('Set MOSS_PROJECT_ID and MOSS_PROJECT_KEY in your environment; never commit them')
    secrets = [key, project + ':' + key]
    out = Path('logs'); out.mkdir(exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    path = out / f'{stamp}-{args.case}.jsonl'
    def log(value):
        with path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(redact(value, secrets), ensure_ascii=False) + '\n')
    def call(method, endpoint, body=None, streaming=False):
        start = time.perf_counter()
        headers = {'Authorization': f'Bearer {project}:{key}', 'Content-Type': 'application/json'}
        req = urllib.request.Request(BASE + endpoint, data=json.dumps(body).encode() if body is not None else None, headers=headers, method=method)
        try:
            response = urllib.request.build_opener(NoRedirect()).open(req, timeout=30)
        except urllib.error.HTTPError as err:
            response = err
        with response:
            h = clean_headers(response.headers)
            if streaming and response.status == 200:
                text = ''; first = sentence = None; terminal = None
                for raw in response:
                    if len(raw) > 1048576:
                        raise ValueError('SSE frame exceeds one MiB')
                    event = parse_sse(raw.decode('utf-8').rstrip('\r\n'))
                    if not event: continue
                    elapsed = round((time.perf_counter() - start)*1000, 2)
                    if event.get('type') == 'response.output_text.delta':
                        text += event.get('delta', '')
                        if first is None and text: first = elapsed
                        if sentence is None: sentence = first_sentence_ms(text, elapsed)
                    if event.get('type') in ('response.completed', 'response.failed', 'response.incomplete'):
                        terminal = event
                record = {'status': response.status, 'headers': h, 'ttft_ms': first, 'first_sentence_ms': sentence, 'elapsed_ms': round((time.perf_counter()-start)*1000, 2), 'text': text, 'terminal': terminal}
            else:
                raw = response.read(1048577)
                if len(raw) > 1048576: raise ValueError('response exceeds one MiB')
                try: data = json.loads(raw)
                except (ValueError, UnicodeDecodeError): data = {'non_json_response': True}
                record = {'status': response.status, 'headers': h, 'elapsed_ms': round((time.perf_counter()-start)*1000, 2), 'body': data}
            log({'case': args.case, 'endpoint': endpoint, 'method': method, **record})
            return record
    try:
        if args.case in ('inference', 'invalid-inference', 'stream'):
            body = {'model': 'invalid-model-for-contract-test' if args.case == 'invalid-inference' else 'moss/fastlane-1', 'input': 'Answer in one sentence: what is a prefix cache?', 'stream': args.case == 'stream'}
            log({'case': args.case, 'request_body': body})
            call('POST', '/responses', body, args.case == 'stream')
        elif args.case == 'invalid-task':
            body = {'goal': 'Read example.com', 'environment': {'type': 'unsupported'}}
            log({'case': args.case, 'request_body': body})
            call('POST', '/tasks', body)
        else:
            body = task_payload(); log({'case': args.case, 'request_body': body})
            created = call('POST', '/tasks', body)
            task = created.get('body', {}); task_id = task.get('id')
            if created['status'] != 202 or not valid_task_id(task_id):
                print('Task was not confirmed created; inspect the evidence before retrying.', file=sys.stderr); return 1
            deadline = time.monotonic() + 100
            while task.get('status') not in TERMINAL and time.monotonic() < deadline:
                time.sleep(3)
                got = call('GET', '/tasks/' + task_id)
                if got['status'] != 200:
                    print('Polling failed; inspect task before retrying.', file=sys.stderr); return 1
                task = got['body']
            if task.get('status') not in TERMINAL:
                print('Task still nonterminal; inspect/cancel it in the portal. Do not create a replacement blindly.', file=sys.stderr); return 1
            call('GET', '/tasks/' + task_id + '/files')
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        log({'case': args.case, 'client_error': str(exc)})
        print('Request failed or timed out; inspect task state before any retry.', file=sys.stderr); return 1
    print('Evidence saved to', path)
    return 0

if __name__ == '__main__':
    sys.exit(main())
