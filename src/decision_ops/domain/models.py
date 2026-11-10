from __future__ import annotations

from typing import Literal

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
    required_positions: int | None = None
    planned_coverage: int | None = None
    uncovered_positions: int | None = None
    risk_level: Literal["low", "medium", "high", "unknown"]
    requires_human_review: bool
    rationale: str
    evidence_status: Literal["sufficient", "insufficient"] = "sufficient"
    missing_inputs: list[str] = Field(default_factory=list)
    analysis_status: Literal["initial", "revised"] = "initial"
    applied_inputs: list[str] = Field(default_factory=list)
    next_action: str


class CapacityEvidence(BaseModel):
    """Supplemental, caller-provided facts for one read-only calculation."""

    planned_coverage: int = Field(ge=0)
    required_lead_present: bool


class CapacityRiskRequest(BaseModel):
    period: str = Field(pattern=r"^\d{4}-W\d{2}$")
    evidence: CapacityEvidence | None = None


class AgentQuestion(BaseModel):
    question: str = Field(min_length=8, max_length=1_000)


class AgentRecommendation(BaseModel):
    answer: str
    approval_required: bool = True
    disclaimer: str = "Read-only recommendation; no operational plan was changed."
