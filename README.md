# Moss Inference evaluation — work in progress

**Not a submission.** As of 25 November 2026 no live inference or Tasks API calls have been run by this harness. The portal did not respond to the browser, and the project key and current credit balance were unavailable. Do not infer product results from this scaffolding.

## Purpose

Reproduce a small set of sequential, synthetic probes for Moss Inference and Tasks, capturing HTTP status, allowed diagnostic headers, response, elapsed time and task polling states. `stream` measures client-side first text delta, first complete sentence and end-of-stream separately; neither is end-to-end voice latency. This is not yet a RAG benchmark. Full raw API responses may contain sensitive information: review every log manually before sharing.

## Safety first

- First inspect the portal for the remaining included balance, pending usage and auto-reload. Do not run these if spending could exceed included credits.
- Tasks' `max_cost_usd` is **not a total cap**: it covers model calls only, in-flight calls can overshoot, and browser time/traffic are billed separately, even for failures and cancellations. Traffic costs may appear later. The script cannot enforce a credit-only budget. Run one task at a time, monitor it and stop if unsure.
- The code sends credentials only to `https://inference.moss.dev`; redirects are not followed. Logs do not record the authorization header and known key values are redacted. This does not guarantee all sensitive content is removed. Audit outputs before committing or publishing.
- A timed-out creation or poll has an unknown outcome; inspect the portal before retrying. Never start another task blindly. The script records the task ID on confirmed creation and exits if polling fails.

## Run

Requires Python 3.11+; standard library only. Run from this directory. Set project ID and key in the shell securely; do not place the key in source or command history. Never commit `.env` files. Set the variables only for the process/session and do not paste them in chat.

```powershell
python -m unittest discover -s tests -v
# After confirming the balance and auto-reload status:
python -m scripts.probe invalid-inference --balance-checked
python -m scripts.probe inference --balance-checked
python -m scripts.probe stream --balance-checked
python -m scripts.probe invalid-task --balance-checked
# Only if the balance and pending costs leave adequate headroom:
python -m scripts.probe task --balance-checked
```

Each command creates a timestamped JSONL file under `logs/`. The live cases are not unit tests and may cost credits. See `PLAN.md` for the remaining coverage and completion criteria. Evidence should distinguish documentation from measured results; add request IDs, task IDs, timestamp, actual costs, sample size and environment. Do not claim sub-200ms, schema failures, or retrieval results until measured.

## Sources

- https://docs.moss.dev/docs/inference/quickstart
- https://docs.moss.dev/docs/inference/tasks
- https://docs.moss.dev/docs/api-reference/v1/inference/tasks
- https://docs.moss.dev/docs/inference/pricing
- https://docs.moss.dev/docs/inference/streaming
