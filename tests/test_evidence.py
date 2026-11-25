import unittest
import tempfile
from pathlib import Path
from scripts.evidence import redact, first_sentence_ms, parse_sse, read_env

class EvidenceTests(unittest.TestCase):
    def test_redacts_secrets_at_any_depth(self):
        value = {'Authorization': 'Bearer secret', 'nested': [{'message': 'oops secret'}], 'id': 'task_123'}
        self.assertEqual(redact(value, ['secret']), {'Authorization': '[redacted]', 'nested': [{'message': 'oops [redacted]'}], 'id': 'task_123'})

    def test_env_reads_only_expected_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / '.env'
            p.write_text('MOSS_PROJECT_ID=project\nMOSS_PROJECT_KEY=secret\nOTHER=ignored\n', encoding='utf-8')
            self.assertEqual(read_env(p), {'MOSS_PROJECT_ID': 'project', 'MOSS_PROJECT_KEY': 'secret'})

    def test_sse_text_delta_and_terminal(self):
        event = parse_sse('data: {"type":"response.output_text.delta","delta":"Hello."}')
        self.assertEqual(event['delta'], 'Hello.')
        self.assertIsNone(parse_sse('event: ignored'))

    def test_sentence_time_is_not_first_token_time(self):
        self.assertIsNone(first_sentence_ms('Hello there'))
        self.assertEqual(first_sentence_ms('Hello there.', 231.5), 231.5)

if __name__ == '__main__':
    unittest.main()
