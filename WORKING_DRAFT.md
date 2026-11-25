# Moss Inference — working notes

**Incomplete draft for Faizan’s review. Not ready to send.** Sri asked for firsthand results and the candidate’s own words. The live API and Tasks checks have not run, so this is not a completed work sample.

## Portal

The Configure screen brings the project ID, key creation and Python, TypeScript and cURL instructions together. That makes the path to a first request easy to find. It also displays a newly created key in the setup snippet; I would mask it by default and make copying an explicit action, while keeping the one-time-save warning visible. The Developer plan screen says $10 once at signup, but the current balance and auto-reload status were not verified.

## Inference API

The documentation describes OpenAI-compatible Responses, streaming and retrieval through indexes. I would add a small voice example that records time to first text and first complete sentence, alongside retrieval time and request ID; these are separate from microphone-to-speaker latency. I have not run the API, checked compatibility, measured speed or tested grounding, so I cannot yet give a firsthand verdict.

## Tasks API

The docs describe async jobs, status polling, cancellation, files and schema verification. A completed job can still have a failed schema verification, and the stated cost limit covers model calls rather than the entire job. I would make verification and estimated all-in cost conspicuous before users consume an answer or start a run. These are documentation-based product suggestions, not observed failures. No Tasks have been submitted and there are no task IDs, results or costs to report.

## Remaining before submission

Run the portal, Inference and Tasks checks using a replacement key and confirmed included credits; add redacted evidence and measured results; update these notes in Faizan’s own words. The repository is private and Sri cannot access it unless its visibility or access is changed after review.

Work in progress: https://github.com/MuhammadFaizan-prog/moss-inference-eval
