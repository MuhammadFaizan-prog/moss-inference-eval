import unittest
from scripts.probe import task_payload, clean_headers, valid_task_id

class ProbeTests(unittest.TestCase):
    def test_task_is_short_and_model_cap_is_explicit(self):
        body = task_payload()
        self.assertEqual(body['environment']['start_url'], 'https://example.com')
        self.assertEqual(body['limits']['max_runtime_seconds'], 60)
        self.assertEqual(body['limits']['max_cost_usd'], 0.05)

    def test_task_ids_must_not_contain_path_characters(self):
        self.assertTrue(valid_task_id('task_' + 'a' * 32))
        self.assertFalse(valid_task_id('task_../../elsewhere'))

    def test_only_diagnostic_headers_survive(self):
        headers = {'Authorization': 'secret', 'X-Moss-Request-Id': 'req_1', 'Content-Type': 'application/json'}
        self.assertEqual(clean_headers(headers), {'x-moss-request-id': 'req_1', 'content-type': 'application/json'})

if __name__ == '__main__':
    unittest.main()
