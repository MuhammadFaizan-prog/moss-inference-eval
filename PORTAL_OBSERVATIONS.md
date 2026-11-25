# Portal observations — 25 November 2026

These observations are limited to screens actually viewed during this evaluation. They are not a complete portal audit.

- Configure grouped the project ID, project-key creation and Python, TypeScript and cURL quickstarts into a three-step onboarding flow. I could locate the path to a first request without hunting through the docs.
- After a project key was created, the Configure screen displayed it in the environment-variable snippet and showed a one-time-save warning. Improvement to consider: hide the value by default, make the one-time reveal/copy explicit, and ensure copied snippets can be safely shared without revealing a credential. Displaying the key once is part of normal onboarding; this is a product improvement, not evidence of a server-side vulnerability.
- The Plans screen showed the Developer Free plan and listed $10 once at signup. It also said that the workspace pauses when credits run out. The actual account credit balance, pending charges, and auto-reload setting were not verified; do not assume the remaining balance from the plan table.
- A later attempt to open API keys and billing in fresh tabs timed out. Browser responsiveness was intermittent; this alone is not evidence of a Moss product defect because the local browser/extension could also be responsible.

No Inference API or Tasks API calls were executed for this take-home as of this note. No latency, error, task ID, verification, cost, or completion figures are claimed. The key exposed in an earlier browser tool result must be treated as compromised. It was not added to the repository; no revocation has been confirmed.
