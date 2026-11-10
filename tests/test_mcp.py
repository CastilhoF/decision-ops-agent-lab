import pytest
from mcp import Client

from decision_ops.mcp.server import server


@pytest.mark.asyncio
async def test_mcp_server_exposes_and_runs_read_only_tool() -> None:
    async with Client(server, raise_exceptions=True) as client:
        tools = await client.list_tools()

        assert {tool.name for tool in tools.tools} == {
            "get_capacity_risk",
            "search_operational_knowledge",
        }

        result = await client.call_tool("get_capacity_risk", {"period": "2026-W24"})

    assert result.structured_content["risk_level"] == "high"


@pytest.mark.asyncio
async def test_mcp_reports_insufficient_evidence_without_calculating_risk() -> None:
    async with Client(server, raise_exceptions=True) as client:
        result = await client.call_tool("get_capacity_risk", {"period": "2026-W27"})

    assert result.structured_content["evidence_status"] == "insufficient"
    assert result.structured_content["risk_level"] == "unknown"
    assert result.structured_content["missing_inputs"] == [
        "planned coverage",
        "required lead-role status",
    ]


@pytest.mark.asyncio
async def test_mcp_revises_analysis_after_receiving_all_missing_inputs() -> None:
    async with Client(server, raise_exceptions=True) as client:
        result = await client.call_tool(
            "get_capacity_risk",
            {
                "period": "2026-W27",
                "planned_coverage": 11,
                "required_lead_present": True,
            },
        )

    assert result.structured_content["evidence_status"] == "sufficient"
    assert result.structured_content["analysis_status"] == "revised"
    assert result.structured_content["risk_level"] == "low"
