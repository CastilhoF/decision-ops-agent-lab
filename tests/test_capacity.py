import pytest

from decision_ops.domain.models import CapacityEvidence
from decision_ops.services.capacity import get_capacity_risk


def test_high_risk_requires_human_review() -> None:
    risk = get_capacity_risk("2026-W24")

    assert risk.risk_level == "high"
    assert risk.requires_human_review is True
    assert risk.uncovered_positions == 2


def test_low_risk_does_not_require_human_review() -> None:
    risk = get_capacity_risk("2026-W26")

    assert risk.risk_level == "low"
    assert risk.requires_human_review is False


def test_missing_operational_data_returns_safe_non_recommendation() -> None:
    risk = get_capacity_risk("2026-W27")

    assert risk.evidence_status == "insufficient"
    assert risk.risk_level == "unknown"
    assert risk.uncovered_positions is None
    assert risk.missing_inputs == ["planned coverage", "required lead-role status"]
    assert "No risk level" in risk.rationale
    assert "Provide planned coverage" in risk.next_action


def test_complete_evidence_revises_previously_incomplete_analysis() -> None:
    first_result = get_capacity_risk("2026-W27")
    revised_result = get_capacity_risk(
        "2026-W27",
        CapacityEvidence(planned_coverage=11, required_lead_present=True),
    )

    assert first_result.evidence_status == "insufficient"
    assert revised_result.evidence_status == "sufficient"
    assert revised_result.analysis_status == "revised"
    assert revised_result.risk_level == "low"
    assert revised_result.missing_inputs == []
    assert revised_result.applied_inputs == [
        "planned coverage",
        "required lead-role status",
    ]
    assert "Provide planned coverage" not in revised_result.next_action
    assert get_capacity_risk("2026-W27").evidence_status == "insufficient"


def test_unknown_period_has_explanatory_error() -> None:
    with pytest.raises(ValueError, match="Supported periods"):
        get_capacity_risk("2026-W99")
