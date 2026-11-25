# Moss Inference take-home — execution plan

Status: **Not ready to submit.** The email asks for firsthand results and the candidate’s own words. Documentation is not evidence of product behavior.

## Ground rules

- Work in the existing AI Agent project, using only the included credit balance. Confirm the available balance and whether auto-reload is enabled before billable calls. Do not add payment methods or credits.
- Do not publish the repository or send the email until Faizan reviews the work and authorizes those actions. A private repository is not accessible to Sri unless access is granted or its visibility is changed.
- Never include project keys, Authorization headers, personal data, or private page content in logs. Use synthetic inputs, restrict destinations to public examples, and review all evidence before sharing.
- Preserve the difference between documented behavior and observations. Report samples, exact prompts, timing method, task IDs, errors and costs, including failures and missing data.

## 1. Inspect and record the portal

Record screen, action, observed result, and a concrete improvement. Check Configure/key creation and the first-request copy; Playground and model/index selection; Indexes and Tasks empty and populated states; Logs & Traces request IDs and timing; Usage and billing balance. Do not change billing or unrelated settings. The supplied prior transcript reported a Session minutes label, but it has not been independently verified in this run. The documentation says inference itself is not billed by session minutes; validate both screens before treating this as a defect.

## 2. Test inference

Start with a single non-streaming Responses request and an invalid model; record HTTP status, request ID, text, usage and wall time. Stream a few repeated short support questions and record first text delta, first sentence and full-response elapsed times separately. These are client-observed, ungrounded timings, not an end-to-end voice or RAG benchmark. If budget and index creation permit, add a small synthetic knowledge index and compare the same prompts with and without retrieval, reporting exact sample sizes, retrieval headers and grounding quality. Do not promise a sub-200 ms result or compare providers without measurements.

## 3. Test Tasks safely

Use a public benign page such as example.com. First test invalid input; then submit a single simple extraction task with a short runtime and small model-call limit. Poll until terminal, record transitions, verification, error, step counts, task ID, files and itemized usage. Test a job failure only when sufficient remaining credit is verified; try a non-resolving public hostname or tight runtime, and report the actual result. A task’s `max_cost_usd` limits model calls only; in-flight calls can overshoot, and browser time and traffic are additional. It is **not** a hard all-in spending cap. Traffic charges can appear hours later. Recheck balance and pending costs before further jobs; stop well before included credit is exhausted.

## 4. Assemble submission

Aggregate only actually run cases; explain environment and limitations. Include reproducible scripts, sanitized evidence, local checks and a short README. Review logs for secrets and identifying data before committing. Draft a one-page memo addressing all three areas with prioritized day-one improvements, then render and check one page. The draft is for Faizan to inspect and rewrite in his own words, as Sri requested. Prepare a Gmail reply to Sri with Ashvath copied and the reviewed document and repository link; do not send.

## Blockers and current evidence

- Gmail request and sender/CC verified in the original thread.
- Moss API docs and pricing read. Task validation, state and billing are **documented**, not observed in a live test.
- No project key was present in the workspace `.env` or the process environment at the time checked. The portal tab was not responding to browser snapshots; live account state and remaining balance could not be confirmed. No billable API calls were attempted.
- No claims of a finished portal audit, API benchmark, task run, or GitHub publication are justified yet.

## Sources

- https://docs.moss.dev/docs/inference/quickstart
- https://docs.moss.dev/docs/inference/tasks
- https://docs.moss.dev/docs/api-reference/v1/inference/tasks
- https://docs.moss.dev/docs/inference/pricing
- https://docs.moss.dev/docs/inference/streaming
