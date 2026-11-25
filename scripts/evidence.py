"""Small helpers for redacted, timestamped evidence."""
import json
import re

SENSITIVE_KEYS = {'authorization', 'api_key', 'project_key', 'x-moss-provider-key'}

def read_env(path):
    if not path.is_file():
        return {}
    values = {}
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        name, sep, value = line.partition('=')
        if sep and name.strip() in {'MOSS_PROJECT_ID', 'MOSS_PROJECT_KEY'}:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('\"', "'"):
                value = value[1:-1]
            values[name.strip()] = value
    return values

def redact(value, secrets):
    if isinstance(value, dict):
        return {key: '[redacted]' if key.lower() in SENSITIVE_KEYS else redact(val, secrets) for key, val in value.items()}
    if isinstance(value, list):
        return [redact(item, secrets) for item in value]
    if isinstance(value, str):
        for secret in secrets:
            if secret:
                value = value.replace(secret, '[redacted]')
    return value

def parse_sse(line):
    if not line.startswith('data:'):
        return None
    data = line[5:].strip()
    return json.loads(data) if data and data != '[DONE]' else None

def first_sentence_ms(text, elapsed_ms=None):
    return elapsed_ms if re.search(r'[.!?](?:\s|$)', text) else None
