# Portal observations — 25 November 2026

These are browser UI observations, not direct HTTP/API tests. See the redacted JSON evidence for inputs, outputs, request IDs and qualifications. Values are as displayed; billing can lag.

- Configure puts project setup and language quickstarts together. A key was displayed in an onboarding snippet; masking by default with explicit reveal/copy would reduce accidental exposure. The key is not in this repo, was not used for tests, and its revocation has not been confirmed.
- A sample SaaS FAQ index reported 55 documents. The indexed password-reset answer matched the example fact; without the index the answer stated the FAQ was unavailable. Individual retrieved passages were not inspected.
- The same two request IDs showed differing first-token and total timings in Playground and Logs & Traces; this requires an explanation of measurement boundaries rather than an assumption of a defect.
- Example.com produced the requested schema-matching task result; the unreachable-site task successfully reported the loading error as instructed. The latter is not a terminal task failure.
- Empty goals and malformed JSON were blocked. A root-array schema enabled Run but was rejected upon submission, with no task ID shown.
- The two task pages displayed $0.053 and $0.051 against $0.05 limits; total cost includes categories not necessarily capped by model-call limit. A task's intermediate elapsed display was higher than its final displayed time; the clocks may measure different intervals.
- Billing displayed a $10 balance, $0.11 of $5 monthly credit used and $4.89 remaining, auto-reload off and no payment methods; values may be rounded or delayed.

No direct API calls were made. Portal responsiveness was intermittent and its cause was not established.
