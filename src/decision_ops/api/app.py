from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException

from decision_ops.agent.orchestrator import answer_question
from decision_ops.domain.models import (
    AgentQuestion,
    AgentRecommendation,
    CapacityRisk,
    CapacityRiskRequest,
    KnowledgeChunk,
    SearchRequest,
)
from decision_ops.rag.retriever import LexicalRetriever
from decision_ops.services.capacity import get_capacity_risk
from decision_ops.settings import get_settings

app = FastAPI(
    title="Decision Ops Agent Lab",
    version="0.1.0",
    description="A study API for RAG, deterministic tools, MCP, and LLM orchestration.",
)


def _retriever() -> LexicalRetriever:
    settings = get_settings()
    return LexicalRetriever(Path(settings.knowledge_directory))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "decision-ops-agent-lab"}


@app.post("/v1/rag/search", response_model=list[KnowledgeChunk])
def search_knowledge(request: SearchRequest) -> list[KnowledgeChunk]:
    return _retriever().search(request.query, request.limit)


@app.post("/v1/tools/capacity-risk", response_model=CapacityRisk)
def capacity_risk(request: CapacityRiskRequest) -> CapacityRisk:
    try:
        return get_capacity_risk(request.period)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.post("/v1/agent/recommendations", response_model=AgentRecommendation)
async def agent_recommendation(request: AgentQuestion) -> AgentRecommendation:
    if not get_settings().openai_api_key:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is required for the optional LLM agent endpoint.",
        )
    return await answer_question(request.question)
