# Moss Inference — Work Sample

**Muhammad Faizan** · muhammadfaizanali18@gmail.com · [github.com/MuhammadFaizan-prog](https://github.com/MuhammadFaizan-prog)

Submission for the Moss work-sample round. Live tests run on 25 November 2026 against the Moss Inference API. The one-pager with findings is in [`ONE_PAGER.md`](./ONE_PAGER.md).

---

## What's here

| Path | Purpose |
|---|---|
| `ONE_PAGER.md` | The 1-page submission memo with real measurements |
| `scripts/probe.py` | Sequential probes: inference, streaming, tasks, and validation error cases |
| `scripts/evidence.py` | Helpers: credential redaction, SSE parsing, timing |
| `logs/` | Raw JSONL evidence from every live probe (secrets auto-redacted) |
| `evidence/` | Portal UI observations captured via browser (from earlier session) |
| `tests/` | Offline unit tests (no network, no credentials required) |
| `.env.example` | Template — copy to `.env` and add your own key |

## Results summary

| Test | Status | Key number |
|---|---|---|
| `invalid-inference` (bad model name) | ✅ HTTP 400, `model_not_found` | 835 ms |
| `inference` (moss/fastlane-1, sync) | ✅ HTTP 200, 147 tokens | 1,353 ms e2e |
| `stream` (moss/fastlane-1, SSE) | ✅ HTTP 200 | TTFT **1,090 ms** |
| `invalid-task` (unsupported env) | ✅ HTTP 400, helpful message | 1,130 ms |
| `task` (browser → example.com) | ✅ completed in ~20 s | \$0.0066 total |

Task ID verified: `task_00f7d6540bf5401db9a7d505e7c175da`  
Request IDs: inference `29ae8b279b154644bffe2cefc0114ab9`, stream `7b897ebefaf34c81a94d550d8b35134b`

## Run it yourself

Requires Python 3.11+, standard library only.

```powershell
# 1. Clone and enter the repo
git clone https://github.com/MuhammadFaizan-prog/moss-inference-eval
cd moss-inference-eval

# 2. Add credentials (never commit .env)
copy .env.example .env
# Edit .env: set MOSS_PROJECT_ID and MOSS_PROJECT_KEY

# 3. Run offline tests (no network required)
python -m unittest discover -s tests -v

# 4. Check your credit balance in the portal, then run live probes
python -m scripts.probe invalid-inference --balance-checked  # free
python -m scripts.probe inference --balance-checked          # ~$0.001
python -m scripts.probe stream --balance-checked             # ~$0.001
python -m scripts.probe invalid-task --balance-checked       # free
python -m scripts.probe task --balance-checked               # ~$0.007
```

Each command creates a timestamped JSONL file in `logs/`. Credentials are never written to logs.

## Safety notes

- `max_cost_usd` on tasks caps **model spend only** — browser time and traffic are billed on top. See [`ONE_PAGER.md`](./ONE_PAGER.md) for details.
- Never commit `.env`. It is gitignored.
- Review `logs/` manually before sharing — the redaction covers known key patterns but is not exhaustive.

## Sources

- https://docs.moss.dev/docs/inference/quickstart
- https://docs.moss.dev/docs/inference/tasks
- https://docs.moss.dev/docs/api-reference/v1/inference/tasks
- https://docs.moss.dev/docs/inference/pricing
- https://docs.moss.dev/docs/inference/streaming
