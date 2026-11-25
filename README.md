# Moss Inference evaluation

**Status: review draft, not a finished submission.** This private repository contains live **portal UI** observations from 25 November 2026, a reproducible direct-API harness and offline tests. No direct Inference or Tasks API request has been executed with this harness; UI outcomes are not raw HTTP transcripts. A terminal task failure and empty retrieval result remain untested. The one-page work sample is [WORKING_DRAFT.md](WORKING_DRAFT.md) and needs the candidate's personal review and wording.

## What was observed

- A built-in 55-document SaaS FAQ index returned a password-reset answer matching the example shown in the sample picker. Without the index, the same question produced a missing-information answer. One sample each; not a benchmark.
- Two Playground requests had different timing numbers in Playground and Logs & Traces for the same request IDs. The clocks' boundaries are unknown.
- Two portal Tasks completed: example.com yielded a schema-matching result; the unreachable-site task reported the access error and succeeded at its fallback goal. Neither establishes terminal job failure.
- Empty goals and malformed JSON were blocked; an array-root schema enabled Run but was rejected on submission.
- The task screens displayed $0.053 and $0.051 with $0.05 limits; documented model-call-only limits, in-flight calls and extra browser/traffic charges mean this alone is not proof of a billing bug. See [evidence](evidence/) for exact inputs and qualifications.

## Reproduce safely

Requires Python 3.11+, standard library. First verify included credit, auto-reload, pending costs and absence of out-of-pocket exposure. Tasks' model-call limit is **not an all-in cap**: browser/traffic, failed work and in-flight calls can add costs; billing can lag. Never use an exposed credential. Provide a new, safely stored authorized key in an ignored local .env based on .env.example. Do not put keys in code, logs, history or GitHub. Redirects are disabled and log redaction is best-effort; manually review every output before sharing.

Run from the repo directory:

    python -m unittest discover -s tests -v
    python -m scripts.probe invalid-inference --balance-checked
    python -m scripts.probe inference --balance-checked
    python -m scripts.probe stream --balance-checked
    python -m scripts.probe invalid-task --balance-checked
    python -m scripts.probe task --balance-checked

The task command is billable and must be run singly with adequate headroom. A timed-out submission has an unknown outcome; inspect it before retrying. Inspect the logged terminal status and verification even if the command exits zero; terminal failed/cancelled states are not currently classified as a failing exit by the harness. Logs are ignored by default. Offline tests were run previously (11 passing); they do not validate the remote service.

## Sources

- https://docs.moss.dev/docs/inference/quickstart
- https://docs.moss.dev/docs/inference/tasks
- https://docs.moss.dev/docs/api-reference/v1/inference/tasks
- https://docs.moss.dev/docs/inference/pricing
- https://docs.moss.dev/docs/inference/streaming
