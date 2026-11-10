from __future__ import annotations

from pathlib import Path

from agents import Agent, Runner, function_tool, set_default_openai_key

from decision_ops.domain.models import AgentRecommendation, CapacityEvidence
from decision_ops.rag.retriever import LexicalRetriever
from decision_ops.services.capacity import get_capacity_risk
from decision_ops.settings import get_settings


@function_tool
def search_operational_knowledge(query: str) -> list[dict[str, str | float]]:
    """Retrieve source-backed synthetic operational guidance for a user question."""

    directory = Path(get_settings().knowledge_directory)
    return [chunk.model_dump() for chunk in LexicalRetriever(directory).search(query)]


@function_tool
def calculate_capacity_risk(
    period: str,
    planned_coverage: int | None = None,
    required_lead_present: bool | None = None,
) -> dict[str, object]:
    """Calculate risk or revise it after both requested operational inputs are supplied."""

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
    return get_capacity_risk(period, evidence).model_dump()


def _build_agent() -> Agent:
    settings = get_settings()
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required to run the LLM agent.")

    set_default_openai_key(settings.openai_api_key)
    return Agent(
        name="Decision Operations Analyst",
        model=settings.llm_model,
        instructions="""
You are a read-only decision-support analyst. Use the knowledge-search tool for
policy questions and the capacity tool for period-specific risk. Never claim to
have changed, approved, or published an operational plan. State uncertainty,
identify the source or calculation used, and require human review for medium or
high risk. If a tool returns insufficient evidence, do not infer a risk level or
recommend an operational action: name the missing inputs and the next safe step. If
the user supplies every requested input, call the tool again with those values and
use the revised result instead of asking for the same evidence again. Do not invent
facts when a tool has no answer.
""".strip(),
        tools=[search_operational_knowledge, calculate_capacity_risk],
    )


async def answer_question(question: str) -> AgentRecommendation:
    result = await Runner.run(_build_agent(), question)
    return AgentRecommendation(answer=str(result.final_output))
