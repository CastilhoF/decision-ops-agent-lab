from fastapi.testclient import TestClient

from decision_ops.api.app import app

client = TestClient(app)


def test_search_endpoint_returns_sources() -> None:
    response = client.post(
        "/v1/rag/search",
        json={"query": "What conditions require human approval?"},
    )

    assert response.status_code == 200
    assert response.json()[0]["source"] == "data/knowledge/approval-policy.md"


def test_capacity_endpoint_calculates_risk() -> None:
    response = client.post("/v1/tools/capacity-risk", json={"period": "2026-W24"})

    assert response.status_code == 200
    assert response.json()["risk_level"] == "high"


def test_capacity_endpoint_reports_missing_evidence_without_guessing() -> None:
    response = client.post("/v1/tools/capacity-risk", json={"period": "2026-W27"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["evidence_status"] == "insufficient"
    assert payload["risk_level"] == "unknown"
    assert payload["missing_inputs"] == ["planned coverage", "required lead-role status"]


def test_capacity_endpoint_revises_analysis_when_missing_evidence_arrives() -> None:
    response = client.post(
        "/v1/tools/capacity-risk",
        json={
            "period": "2026-W27",
            "evidence": {"planned_coverage": 11, "required_lead_present": True},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["evidence_status"] == "sufficient"
    assert payload["analysis_status"] == "revised"
    assert payload["risk_level"] == "low"
    assert payload["missing_inputs"] == []


def test_agent_endpoint_requires_explicit_key() -> None:
    response = client.post(
        "/v1/agent/recommendations",
        json={"question": "Which risk should a planner review first?"},
    )

    assert response.status_code == 503
