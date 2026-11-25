"""Hermetic exercise of CLI behavior; this does not call Moss."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from scripts import probe

class FakeResponse(io.BytesIO):
    def __init__(self, body, status=200):
        super().__init__(body)
        self.status = status
        self.headers = {'Content-Type': 'application/json', 'X-Moss-Request-Id': 'req_synthetic'}

class ProbeOfflineTests(unittest.TestCase):
    def run_cli(self, case, response):
        old = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                opener = mock.Mock()
                opener.open.return_value = response
                with mock.patch.dict(os.environ, {'MOSS_PROJECT_ID':'unit-project', 'MOSS_PROJECT_KEY':'unit-secret'}), \
                     mock.patch.object(probe.urllib.request, 'build_opener', return_value=opener), \
                     mock.patch('sys.argv', ['probe', case, '--balance-checked']), \
                     contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    status = probe.main()
                logs = list(Path('logs').glob('*.jsonl'))
                self.assertEqual(len(logs), 1)
                content = logs[0].read_text(encoding='utf-8')
                self.assertNotIn('unit-secret', content)
                self.assertIn('req_synthetic', content)
                return status, [json.loads(line) for line in content.splitlines()]
            finally:
                os.chdir(old)

    def test_inference_logs_sanitized_result(self):
        status, records = self.run_cli('inference', FakeResponse(b'{"output_text":"unit-secret"}'))
        self.assertEqual(status, 0)
        self.assertEqual(records[-1]['body']['output_text'], '[redacted]')

    def test_incomplete_stream_is_reported_as_failure(self):
        body = b'data: {"type":"response.output_text.delta","delta":"Hello."}\n\n'
        status, records = self.run_cli('stream', FakeResponse(body))
        self.assertEqual(status, 1)
        self.assertIsNone(records[-1]['terminal'])
        self.assertIsNotNone(records[-1]['ttft_ms'])

if __name__ == '__main__':
    unittest.main()
