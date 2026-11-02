# Decision Ops Agent Lab

A study-first portfolio project for building reliable LLM applications with **RAG**, **MCP**, tool calling, guardrails, and human approval.

The project answers synthetic operational questions such as “what is the staffing risk for the next period?” without letting an LLM invent operational facts. Retrieval provides cited evidence, deterministic tools calculate the risk, and the LLM (when configured) explains the result in a structured recommendation.

> All documents, metrics, and identifiers in this repository are fictional.

## What you will learn

| Concept | Where it appears | Key lesson |
| --- | --- | --- |
| LLM | `src/decision_ops/agent/` | The model reasons over a bounded prompt and calls explicitly declared tools. |
| RAG | `src/decision_ops/rag/` | Retrieved source chunks are evidence injected into the model context; they are not model memory. |
| MCP | `src/decision_ops/mcp/` | The same deterministic capabilities are exposed to an MCP host as typed tools. |
| Guardrails | `src/decision_ops/agent/` | The agent may recommend but never performs an operational write. |
| Evaluation | `tests/` and `docs/EVALUATION.md` | Test retrieval, tool outputs, and agent behavior separately. |

## System design

```
                         ┌────────────────────┐
question ───────────────►│ FastAPI API         │
                         └───────┬────────────┘
                                 │
                  ┌──────────────┼──────────────┐
                  ▼              ▼              ▼
          RAG retrieval    deterministic    LLM agent
          (source chunks)  planning tools   (optional)
                  │              │              │
                  └──── evidence + facts ───────┘
                                      │
                                      ▼
                         structured recommendation
                         + sources + approval state

The MCP server exposes the same retrieval and planning capabilities
to external MCP hosts; it never connects directly to an LLM.
```

## Quick start

Requires Python 3.12+.

```bash
git clone https://github.com/CastilhoF/decision-ops-agent-lab.git
cd decision-ops-agent-lab

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
cp .env.example .env
```

Run the API:

```bash
uvicorn decision_ops.api.app:app --reload --port 8030
```

Open [http://localhost:8030/docs](http://localhost:8030/docs).

### Try RAG without an API key

The retrieval and deterministic-tool endpoints run entirely offline:

```bash
curl -X POST http://localhost:8030/v1/rag/search \
  -H 'content-type: application/json' \
  -d '{"query":"What conditions require human approval?"}'
```

```bash
curl -X POST http://localhost:8030/v1/tools/capacity-risk \
  -H 'content-type: application/json' \
  -d '{"period":"2026-W24"}'
```

### Enable the LLM agent

Set `OPENAI_API_KEY` in `.env`. The agent endpoint then combines RAG evidence and function tools into a recommendation:

```bash
curl -X POST http://localhost:8030/v1/agent/recommendations \
  -H 'content-type: application/json' \
  -d '{"question":"Which risk should a planner review first?"}'
```

The key is never committed. Without it, the API returns a clear configuration error instead of simulating a model response.

## Run the MCP server

```bash
mcp run src/decision_ops/mcp/server.py
```

The server exposes:

- `search_operational_knowledge(query, limit)`
- `get_capacity_risk(period)`
- `approval_policy` as a resource

See [docs/MCP.md](docs/MCP.md) for host/client/server terminology and testing instructions.

## Quality checks

```bash
pytest
ruff check src tests
ruff format --check src tests
```

## Learning path

1. Read [docs/01-LLM.md](docs/01-LLM.md).
2. Run the RAG API and inspect its returned chunks and source paths.
3. Run the capacity-risk tool and compare its deterministic output with the policy document.
4. Start the MCP server and inspect its typed tools.
5. Configure the LLM agent only after you understand the inputs it receives.
6. Add adversarial cases from [docs/EVALUATION.md](docs/EVALUATION.md) before broadening its capabilities.
7. Use [docs/REFERENCES.md](docs/REFERENCES.md) alongside the code for the primary specifications.

## Important boundaries

- RAG is retrieval, not training or durable model memory.
- MCP is a protocol for exposing context and tools; it is not an agent framework.
- An LLM is probabilistic. Capacity calculations and write permissions stay in typed, testable code.
- This project returns recommendations only. Any action that could change an operational plan must remain behind explicit human approval.

## License

[MIT](LICENSE)
