<div align="center">

# 🌿 Moss Inference — Work Sample

**Muhammad Faizan** · Full-Stack & Agentic AI Engineer

[![GitHub](https://img.shields.io/badge/GitHub-MuhammadFaizan--prog-181717?logo=github)](https://github.com/MuhammadFaizan-prog)
[![Portfolio](https://img.shields.io/badge/Portfolio-faizi--dev.vercel.app-000?logo=vercel)](https://faizi-dev.vercel.app/)
[![Email](https://img.shields.io/badge/Email-muhammadfaizanali18%40gmail.com-EA4335?logo=gmail&logoColor=white)](mailto:muhammadfaizanali18@gmail.com)

*Work sample submission for Moss · Tested live on 25 November 2026*

---

</div>

## 📋 What's Inside

| File | Purpose |
|:-----|:--------|
| [`ONE_PAGER.md`](./ONE_PAGER.md) | **The submission** — 1-page memo with real measurements, honest opinions, and suggested improvements |
| [`scripts/probe.py`](./scripts/probe.py) | The test harness — five sequential probes against the live API |
| [`scripts/evidence.py`](./scripts/evidence.py) | Helpers: credential redaction, SSE parsing, timing |
| [`logs/`](./logs/) | Raw JSONL evidence from every live probe (secrets auto-redacted) |
| [`evidence/`](./evidence/) | Portal UI observations captured via browser |
| [`tests/`](./tests/) | Offline unit tests — no network, no credentials needed |
| [`.env.example`](./.env.example) | Credential template |

---

## 📊 Results at a Glance

> All five probes ran live against `https://inference.moss.dev/v1` on 25 Nov 2026.

<div align="center">

| Probe | Result | Key Metric |
|:------|:------:|:-----------|
| `invalid-inference` — bad model name | ✅ `HTTP 400` | `model_not_found` in 835 ms |
| `inference` — `moss/fastlane-1`, sync | ✅ `HTTP 200` | **1,096 ms** end-to-end · 136 tokens |
| `stream` — `moss/fastlane-1`, SSE | ✅ `HTTP 200` | **TTFT 723 ms** 🚀 |
| `invalid-task` — unsupported environment | ✅ `HTTP 400` | Clear error message in 1,130 ms |
| `task` — browser → `example.com` | ✅ `completed` | **~20 s** · $0.0053 total |

</div>

### Task Evidence

```
Task ID  :  task_7c6c74abf1ef49f5a483d3192f1af1fe
Created  :  2026-11-25T18:46:51Z
Finished :  2026-11-25T18:47:11Z  (~20 seconds)
Steps    :  3  |  Model calls: 4
Tokens   :  17,232 input  (9,342 cached)  ·  725 output
Cost     :  $0.005 model  +  $0.0003 browser  =  $0.0053 total
Result   :  {"title":"Example Domain","paragraph":"This domain is for use in..."}
Verified :  output_schema · passed: true
```

### Inference Request IDs

```
sync   →  req 6aecbdb5817a405fa3760b89cc1bdfe7
stream →  req f054e3f0e7604d4dada9a0007b5a1104
```

---

## 🔍 Key Findings (from [`ONE_PAGER.md`](./ONE_PAGER.md))

### Portal 🌐
- ✅ **Configure screen is excellent** — project ID + key creation + quickstarts in one place; zero-doc onboarding
- ⚠️ **Key exposure in shareable snippet** — newly created key embeds in copy-paste env snippet; should be masked behind a "reveal" button
- ⚠️ **"Session minutes" label** on the Usage page doesn't match how inference is actually billed

### Inference API ⚡
- ✅ **723 ms TTFT** on `moss/fastlane-1` streaming — fast enough to cut dead-air in voice agents
- ✅ **Drop-in OpenAI replacement** — same SSE wire format, same `response.output_text.delta` events; LiveKit / Pipecat adapters work with one base URL change
- ✅ **Clean error contract** — `model_not_found` with exact fix suggestion at <900 ms
- 💡 **Missing:** `GET /v1/responses/{id}` — no way to recover a generation if the SSE client drops

### Tasks API 🤖
- ✅ **Fast and reliable** — example.com task queued, ran, and completed with verified JSON output in ~20 s
- ✅ **Schema-validated output** — `verification.passed: true` enables safe downstream consumption without extra parsing
- ⚠️ **`max_cost_usd` only caps model spend** — browser time and traffic are billed on top; rename to `max_model_cost_usd` or add a tooltip
- 💡 **Missing:** `GET /v1/tasks` list endpoint — no programmatic way to query or resume prior runs

---

## 🚀 Run It Yourself

**Requirements:** Python 3.11+, standard library only. No extra dependencies for the probes.

```bash
# 1. Clone the repo
git clone https://github.com/MuhammadFaizan-prog/moss-inference-eval
cd moss-inference-eval

# 2. Set up credentials (never commit .env)
cp .env.example .env
# Edit .env → add MOSS_PROJECT_ID and MOSS_PROJECT_KEY
```

```bash
# 3. Run offline tests first (zero cost, no network)
python -m unittest discover -s tests -v
```

```bash
# 4. Run live probes (check your credit balance in the portal first)
python -m scripts.probe invalid-inference --balance-checked  # free  — error contract
python -m scripts.probe inference        --balance-checked  # ~$0.001 — sync latency
python -m scripts.probe stream           --balance-checked  # ~$0.001 — TTFT
python -m scripts.probe invalid-task     --balance-checked  # free  — task validation
python -m scripts.probe task             --balance-checked  # ~$0.007 — full browser task
```

Each command writes a timestamped JSONL file to `logs/`. **Credentials are never written to logs** — the harness redacts known key patterns before saving.

---

## ⚠️ Safety Notes

> [!WARNING]
> `max_cost_usd` on Tasks caps **model spend only**. Browser time and traffic are billed on top of this limit — a task navigating a heavy page can exceed your expected cap. This is documented in the Moss docs but not surfaced at task-creation time.

> [!CAUTION]
> Never commit `.env`. It is in `.gitignore`. Review `logs/` manually before sharing — the redaction covers known key patterns but is not exhaustive.

---

## 🏗️ How the Harness Works

```
scripts/probe.py
│
├── read_env()          → loads .env, never reads env vars with secrets from shell
├── call()              → urllib only, no SDK, no redirects followed
│   ├── clean_headers() → drops all headers except a safe allowlist
│   └── log()           → redact() every value before writing to JSONL
│
├── case: invalid-inference  → POST /responses with bad model → expect 400
├── case: inference          → POST /responses, sync          → expect 200
├── case: stream             → POST /responses, SSE           → measure TTFT
├── case: invalid-task       → POST /tasks with bad env type  → expect 400
└── case: task               → POST /tasks → poll → GET files → expect completed
```

---

## 📚 References

- [Moss Inference Quickstart](https://docs.moss.dev/docs/inference/quickstart)
- [Moss Tasks API](https://docs.moss.dev/docs/inference/tasks)
- [API Reference — Tasks](https://docs.moss.dev/docs/api-reference/v1/inference/tasks)
- [Pricing](https://docs.moss.dev/docs/inference/pricing)
- [Streaming](https://docs.moss.dev/docs/inference/streaming)

---

<div align="center">

Made with curiosity · [One-pager →](./ONE_PAGER.md)

</div>
