from __future__ import annotations

from pydantic import BaseModel, Field


class KnowledgeChunk(BaseModel):
    source: str
    content: str
    score: float = Field(ge=0)


class SearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=500)
    limit: int = Field(default=3, ge=1, le=10)


class CapacityRisk(BaseModel):
    period: str
    required_positions: int
    planned_coverage: int
    uncovered_positions: int
    risk_level: str
    requires_human_review: bool
    rationale: str


class CapacityRiskRequest(BaseModel):
    period: str = Field(pattern=r"^\d{4}-W\d{2}$")


class AgentQuestion(BaseModel):
    question: str = Field(min_length=8, max_length=1_000)


class AgentRecommendation(BaseModel):
    answer: str
    approval_required: bool = True
    disclaimer: str = "Read-only recommendation; no operational plan was changed."
