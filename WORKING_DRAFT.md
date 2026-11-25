# Moss Inference: work sample

**Review draft — please put this in your own words.** 25 November 2026.

## Portal
The three-step setup and built-in sample index made it easy to get from an empty workspace to a useful FAQ. In Playground, the password-reset answer matched the example fact in Moss's 55-document sample; without the index, the model said the FAQ was missing. That is one question per setup, not a retrieval benchmark. I would show retrieved passages beside the answer and make it clearer which timing each screen measures: for the same request, Playground showed 839 ms to first token and 1,524 ms total, while Logs & Traces showed 78 ms and 595 ms. The measurement boundaries may differ; I cannot call that a bug without them.

## Inference API
The documented Responses interface, streaming and index support look promising for a voice integration. My live observations came from Playground, not direct API calls; I have not established HTTP compatibility or a voice latency distribution. I would ship a small LiveKit or Pipecat example that logs retrieval, first text, first complete sentence and request ID, with clear measurement boundaries and a no-results fallback.

## Tasks API
Through the portal, a one-minute example.com task returned the title and first paragraph, and the portal said it matched the output schema. A second task against a non-resolving address correctly reported that the page could not load; it was marked succeeded because reporting failure was part of the goal, so this is not a terminal job-failure test. Empty goals and malformed schema JSON were blocked; an array-root schema enabled Run but was rejected on submission. I would validate the schema before enabling Run and show the same actionable error in the form.

## Priorities and limits
1. Clarify all-in cost: the two tasks displayed $0.053 and $0.051 against $0.05 limits. The docs say the limit covers model calls, not all browser/traffic costs, and in-flight work can overshoot; the cost breakdown was not visible.
2. Align or explain timing labels, then publish a runnable streaming voice example with no-result handling.
3. Show retrieved sources and make task validation and failure states easier to understand.

These are small UI observations, not a full benchmark. Direct Inference and Tasks API calls and a terminal job failure remain untested. The repository is private and is not yet accessible to reviewers: https://github.com/MuhammadFaizan-prog/moss-inference-eval
