from __future__ import annotations

from decision_ops.domain.models import CapacityEvidence, CapacityRisk

SYNTHETIC_PERIODS = {
    "2026-W24": {"required": 12, "planned": 10, "missing_lead": True},
    "2026-W25": {"required": 10, "planned": 9, "missing_lead": False},
    "2026-W26": {"required": 9, "planned": 9, "missing_lead": False},
    # The capacity playbook is available for this period, but the coverage feed has not arrived.
    "2026-W27": {"required": 11},
}


def get_capacity_risk(period: str, evidence: CapacityEvidence | None = None) -> CapacityRisk:
    """Calculate a read-only risk using base facts plus an optional evidence supplement."""

    try:
        data = SYNTHETIC_PERIODS[period]
    except KeyError as error:
        supported = ", ".join(sorted(SYNTHETIC_PERIODS))
        raise ValueError(f"Unknown period '{period}'. Supported periods: {supported}.") from error

    data = data.copy()
    applied_inputs: list[str] = []
    if evidence:
        data["planned"] = evidence.planned_coverage
        data["missing_lead"] = not evidence.required_lead_present
        applied_inputs = ["planned coverage", "required lead-role status"]

    missing_inputs = [field for field in ("planned", "missing_lead") if field not in data]
    if missing_inputs:
        readable_inputs = {
            "planned": "planned coverage",
            "missing_lead": "required lead-role status",
        }
        return CapacityRisk(
            period=period,
            required_positions=data.get("required"),
            risk_level="unknown",
            requires_human_review=True,
            evidence_status="insufficient",
            missing_inputs=[readable_inputs[field] for field in missing_inputs],
            rationale=(
                "The capacity-risk playbook was found, but the available operational data is "
                "not sufficient to apply it safely. No risk level or staffing recommendation "
                "was produced."
            ),
            next_action=(
                "Provide planned coverage and required lead-role status for this period, then "
                "recalculate the read-only risk summary."
            ),
        )

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
        analysis_status="revised" if evidence else "initial",
        applied_inputs=applied_inputs,
        next_action=(
            "Review the result with a human planner before changing an operational plan."
            if level in {"medium", "high"}
            else "No operational change is proposed by this read-only tool."
        ),
    )
