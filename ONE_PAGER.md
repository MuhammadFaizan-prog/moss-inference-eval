# Moss Inference — Work Sample  
**Muhammad Faizan · muhammadfaizanali18@gmail.com**  
*Tested: 25 November 2026 · Repo: https://github.com/MuhammadFaizan-prog/moss-inference-eval*

---

**Portal.** The Configure screen puts the project ID, key-creation link, and Python/TypeScript/cURL quickstarts on a single page. I went from signup to a working first request without reading the docs. That flow is well thought out.

One thing to tighten: when the portal displays a newly created key, it embeds the value inside a copy-paste environment-variable snippet. That snippet is designed to be shared. A new user is likely to paste it into Slack or a README before they think to redact it. The fix is small — mask the value behind a "reveal" button, keep the snippet with a placeholder — but it matters once keys are production-scoped.

The Usage page labels bandwidth as "Session minutes," which doesn't match what developers expect; inference isn't billed per session minute. Even if that's a backend label, it caused a moment of confusion on the billing page. The Tasks page correctly showed my task (`task_7c6c74abf1ef49f5a483d3192f1af1fe`) with model, status, and cost columns right after it completed. The "New task" button in the portal was a nice surprise — a no-code task runner that lets you iterate without touching the API.

---

**Inference API.** I ran `moss/fastlane-1` synchronously and streaming against `POST /v1/responses`. Synchronous: **1,096 ms** end-to-end, 136 tokens (request ID `6aecbdb5817a405fa3760b89cc1bdfe7`). Streaming: **TTFT 723 ms** to first token and first complete sentence at 724 ms (request ID `f054e3f0e7604d4dada9a0007b5a1104`).

That 723 ms TTFT matters for voice. It's fast enough to cut the dead-air feeling between a user finishing a sentence and an agent starting its reply — which is exactly the problem I described in my cold email. I wanted to verify it held in practice, not just on the marketing page; it does.

The OpenAI wire format (`/v1/responses`, SSE with `response.output_text.delta`) means voice stacks like LiveKit Agents and Pipecat can point their existing OpenAI adapter at Moss with a one-line base URL change. That's a real integration accelerator.

Error handling is clean: sending an unknown model name returned HTTP 400 with `code: model_not_found` and a message that told me exactly what to send instead. The `x-moss-request-id` header is on every response, which is what you need when you're chasing a one-in-a-thousand failure across logs.

One gap I'd fill: a `GET /v1/responses/{id}` endpoint. If a client loses the SSE connection mid-stream, there's no way to recover the generation without re-running the whole request.

---

**Tasks API.** I submitted a browser task — read the title and first paragraph of `example.com`, validate the output against a JSON schema — and tracked it from `queued → running → completed` by polling `GET /v1/tasks/{id}`.

**Task `task_7c6c74abf1ef49f5a483d3192f1af1fe`:** created 18:46:51 UTC, finished 18:47:11 UTC — **~20 seconds** wall time. Result: `{"title": "Example Domain", "paragraph": "This domain is for use in..."}`. Schema verification passed. Usage: 3 steps, 4 model calls, 17,232 input tokens (9,342 cached), 725 output tokens. Cost: **\$0.0053** total (\$0.005 model + \$0.0003 browser).

One edge case to flag: `max_cost_usd` caps model spend only, not browser time or traffic. The usage object shows this clearly — total = model + browser + traffic, but the limit only guards the model column. A tooltip on the field, or renaming it `max_model_cost_usd`, removes that ambiguity before it becomes a support ticket.

The missing piece: no `GET /v1/tasks` list endpoint. Agents that want to audit or resume prior runs have no programmatic path; the portal table helps humans but not code. A list endpoint with status filters would round out the CRUD surface.

---

*Scripts, raw JSONL logs, and an offline test suite are in the repo. Everything that hits the API lives in `scripts/probe.py`; logs are saved to `logs/` with secrets redacted automatically.*
