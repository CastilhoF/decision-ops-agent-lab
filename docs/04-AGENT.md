# Agent orchestration

An agent is a runtime loop around an LLM, instructions, and tools. The loop lets the model decide whether it needs a tool, receive the tool result, and continue with better context.

The orchestration module uses two read-only function tools:

- knowledge retrieval for policy evidence;
- deterministic capacity calculation for synthetic periods.

The agent has no write tool. This is the simplest meaningful guardrail: a capability that does not exist cannot be selected by the model.

The OpenAI Agents SDK records traces by default in its normal server-side path. Inspect traces before optimizing prompts: they reveal whether the model chose the right tool, received useful evidence, and respected the approval boundary.
