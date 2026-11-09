from __future__ import annotations

from pathlib import Path

from mcp.server import MCPServer

from decision_ops.rag.retriever import LexicalRetriever
from decision_ops.services.capacity import get_capacity_risk as calculate_capacity_risk
from decision_ops.settings import get_settings

server = MCPServer("Decision Ops Knowledge")


def _retriever() -> LexicalRetriever:
    return LexicalRetriever(Path(get_settings().knowledge_directory))


@server.tool()
def search_operational_knowledge(query: str, limit: int = 3) -> list[dict[str, str | float]]:
    """Retrieve source-backed synthetic operating guidance for a question."""

    return [chunk.model_dump() for chunk in _retriever().search(query, limit)]


@server.tool()
def get_capacity_risk(period: str) -> dict[str, object]:
    """Calculate a read-only risk, or report missing evidence without guessing."""

    return calculate_capacity_risk(period).model_dump()


@server.resource("policy://approval")
def approval_policy() -> str:
    """Return the policy requiring human review before operational changes."""

    policy_path = Path(get_settings().knowledge_directory) / "approval-policy.md"
    return policy_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    server.run()
