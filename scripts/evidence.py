"""Small helpers for redacted, timestamped evidence."""
import json
import re

SENSITIVE_KEYS = {'authorization', 'api_key', 'project_key', 'x-moss-provider-key'}

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
