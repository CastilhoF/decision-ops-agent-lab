# MCP in this project

Model Context Protocol (MCP) is a standard way for an LLM host to discover and call capabilities. It separates an application that exposes context from the application that runs the model.

| Term | Here |
| --- | --- |
| Host | An IDE, desktop application, or agent runtime the user talks to. |
| Client | The MCP-speaking component inside that host. |
| Server | `src/decision_ops/mcp/server.py`, which exposes tools and resources. |
| Tool | A model-controlled capability, such as `get_capacity_risk`. |
| Resource | Application-controlled context, such as the approval policy. |

The MCP server does not call an LLM. That boundary is deliberate: the server exposes trusted capabilities, while the host decides whether and when to make them available to a model.

The official MCP Python SDK derives tool schema from function names, docstrings, and type hints. This is why the tool functions are small, typed, and side-effect-free.
