from __future__ import annotations

from pathlib import Path

from agents import Agent, Runner, function_tool, set_default_openai_key

from decision_ops.domain.models import AgentRecommendation
from decision_ops.rag.retriever import LexicalRetriever
from decision_ops.services.capacity import get_capacity_risk
from decision_ops.settings import get_settings


@function_tool
def search_operational_knowledge(query: str) -> list[dict[str, str | float]]:
    """Retrieve source-backed synthetic operational guidance for a user question."""

    directory = Path(get_settings().knowledge_directory)
    return [chunk.model_dump() for chunk in LexicalRetriever(directory).search(query)]


@function_tool
def calculate_capacity_risk(period: str) -> dict[str, str | int | bool]:
    """Calculate read-only capacity risk for a supported synthetic period, such as 2026-W24."""

    return get_capacity_risk(period).model_dump()


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
high risk. Do not invent facts when a tool has no answer.
""".strip(),
        tools=[search_operational_knowledge, calculate_capacity_risk],
    )


async def answer_question(question: str) -> AgentRecommendation:
    result = await Runner.run(_build_agent(), question)
    return AgentRecommendation(answer=str(result.final_output))
