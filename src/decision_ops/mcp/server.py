from __future__ import annotations

from pathlib import Path

from mcp.server import MCPServer

from decision_ops.domain.models import CapacityEvidence
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
def get_capacity_risk(
    period: str,
    planned_coverage: int | None = None,
    required_lead_present: bool | None = None,
) -> dict[str, object]:
    """Calculate risk or revise an incomplete result with both requested inputs.

    Supply both planned_coverage and required_lead_present only after the tool reports
    insufficient evidence. The tool recalculates without persisting caller data.
    """

    values = (planned_coverage, required_lead_present)
    has_partial_evidence = any(value is not None for value in values) and not all(
        value is not None for value in values
    )
    if has_partial_evidence:
        raise ValueError(
            "Provide both planned_coverage and required_lead_present when supplementing evidence."
        )
    evidence = (
        CapacityEvidence(
            planned_coverage=planned_coverage,
            required_lead_present=required_lead_present,
        )
        if all(value is not None for value in values)
        else None
    )
    return calculate_capacity_risk(period, evidence).model_dump()


@server.resource("policy://approval")
def approval_policy() -> str:
    """Return the policy requiring human review before operational changes."""

    policy_path = Path(get_settings().knowledge_directory) / "approval-policy.md"
    return policy_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    server.run()
