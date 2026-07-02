"""Validate raw dict against CharterSpec and business rules."""
from __future__ import annotations

from typing import Any, Dict, Set

from pydantic import ValidationError

from core.errors import (
    InvalidFieldValueError,
    InvalidInputError,
    MissingFieldError,
)
from core.models import CharterSpec


def _strip_runtime_keys(spec_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Remove keys not in CharterSpec before pydantic validation."""
    data = dict(spec_dict)
    data.pop("word_document", None)
    data.pop("visio_deck", None)
    return data


def validate_payload(spec_dict: Dict[str, Any]) -> CharterSpec:
    try:
        spec = CharterSpec(**_strip_runtime_keys(spec_dict))
    except ValidationError as e:
        raise InvalidInputError(str(e))

    if not spec.project.name.strip():
        raise MissingFieldError("project.name")
    if not spec.vision.statement.strip():
        raise MissingFieldError("vision.statement")

    _validate_unique_ids(spec.objectives, "objectives", "id")
    _validate_unique_ids(spec.stakeholders, "stakeholders", "id")
    _validate_unique_ids(spec.risks, "risks", "id")
    _validate_unique_ids(spec.milestones, "milestones", "id")

    for risk in spec.risks:
        if not 1 <= risk.likelihood <= 5:
            raise InvalidFieldValueError("risks.likelihood", str(risk.likelihood), "Must be 1–5")
        if not 1 <= risk.impact <= 5:
            raise InvalidFieldValueError("risks.impact", str(risk.impact), "Must be 1–5")

    if spec.budget and spec.budget.breakdown:
        bd = spec.budget.breakdown
        total_parts = bd.personnel + bd.hardware + bd.software + bd.training + bd.contingency
        if abs(total_parts - spec.budget.total) > 1.0:
            raise InvalidFieldValueError(
                "budget.breakdown",
                str(total_parts),
                f"Must sum to budget.total ({spec.budget.total})",
            )

    team_ids: Set[str] = {m.id for m in spec.team}
    for member in spec.team:
        rt = member.reports_to
        if rt is not None and rt not in team_ids:
            raise InvalidFieldValueError(
                f"team.{member.id}.reports_to",
                rt,
                "Must reference an existing team member id",
            )

    return spec


def _validate_unique_ids(items, section: str, field: str) -> None:
    seen: Set[str] = set()
    for item in items:
        val = getattr(item, field)
        if val in seen:
            raise InvalidFieldValueError(f"{section}.{field}", val, "Must be unique")
        seen.add(val)
