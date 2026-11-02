# MCP: publish capabilities, not prompts

MCP is an interoperability protocol. It gives an LLM host a uniform way to discover typed tools, resources, and prompts from another application.

This lab publishes a search tool, a calculation tool, and one policy resource. The implementation has no LLM dependency. That is intentional: an MCP server should be safe and useful regardless of which host or model connects to it.

The important design method is least privilege. A tool should accept the smallest input, return the smallest useful output, and expose no state-changing action until it has an authorization and approval design.

Run `mcp run src/decision_ops/mcp/server.py` to start the server through stdio. The tool schema comes from Python signatures and docstrings, so type hints become a user-facing contract.
