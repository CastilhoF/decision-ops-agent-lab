from __future__ import annotations

from decision_ops.domain.models import CapacityRisk

SYNTHETIC_PERIODS = {
    "2026-W24": {"required": 12, "planned": 10, "missing_lead": True},
    "2026-W25": {"required": 10, "planned": 9, "missing_lead": False},
    "2026-W26": {"required": 9, "planned": 9, "missing_lead": False},
}


def get_capacity_risk(period: str) -> CapacityRisk:
    """Calculate a read-only capacity-risk summary for synthetic planning data."""

    try:
        data = SYNTHETIC_PERIODS[period]
    except KeyError as error:
        supported = ", ".join(sorted(SYNTHETIC_PERIODS))
        raise ValueError(f"Unknown period '{period}'. Supported periods: {supported}.") from error

    uncovered = max(data["required"] - data["planned"], 0)
    if uncovered >= 2 or data["missing_lead"]:
        level = "high"
    elif uncovered == 1:
        level = "medium"
    else:
        level = "low"

    return CapacityRisk(
        period=period,
        required_positions=data["required"],
        planned_coverage=data["planned"],
        uncovered_positions=uncovered,
        risk_level=level,
        requires_human_review=level in {"medium", "high"},
        rationale=(
            "Synthetic capacity calculation. A human must review any medium or high risk before a "
            "plan changes."
        ),
    )
