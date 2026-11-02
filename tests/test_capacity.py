import pytest

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


def test_unknown_period_has_explanatory_error() -> None:
    with pytest.raises(ValueError, match="Supported periods"):
        get_capacity_risk("2026-W99")
