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


def test_agent_endpoint_requires_explicit_key() -> None:
    response = client.post(
        "/v1/agent/recommendations",
        json={"question": "Which risk should a planner review first?"},
    )

    assert response.status_code == 503
