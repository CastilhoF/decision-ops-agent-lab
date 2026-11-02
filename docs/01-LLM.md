# LLM: the reasoning layer, not the source of truth

An LLM receives instructions and context, then predicts a useful next output. It does not automatically know your current operational facts, and it is not a reliable calculator or authorization system.

In this project, the LLM has three responsibilities:

1. understand the user's question;
2. choose from explicit read-only tools; and
3. write a recommendation that identifies supporting evidence and uncertainty.

It does **not** calculate capacity, retrieve arbitrary private data, or modify a plan. Those operations stay in normal Python functions where inputs, outputs, and tests are deterministic.

The agent is intentionally optional. Run the RAG and tool endpoints first, then add `OPENAI_API_KEY` when you can inspect exactly what the model receives.
