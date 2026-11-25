import unittest
from scripts.evidence import redact, first_sentence_ms, parse_sse

class EvidenceTests(unittest.TestCase):
    def test_redacts_secrets_at_any_depth(self):
        value = {'Authorization': 'Bearer secret', 'nested': [{'message': 'oops secret'}], 'id': 'task_123'}
        self.assertEqual(redact(value, ['secret']), {'Authorization': '[redacted]', 'nested': [{'message': 'oops [redacted]'}], 'id': 'task_123'})

    def test_sse_text_delta_and_terminal(self):
        event = parse_sse('data: {"type":"response.output_text.delta","delta":"Hello."}')
        self.assertEqual(event['delta'], 'Hello.')
        self.assertIsNone(parse_sse('event: ignored'))

    def test_sentence_time_is_not_first_token_time(self):
        self.assertIsNone(first_sentence_ms('Hello there'))
        self.assertEqual(first_sentence_ms('Hello there.', 231.5), 231.5)

if __name__ == '__main__':
    unittest.main()
