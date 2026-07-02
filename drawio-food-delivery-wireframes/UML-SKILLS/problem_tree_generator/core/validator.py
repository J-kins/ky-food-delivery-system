from typing import Dict, Any
from pydantic import ValidationError
from core.models import ProblemTreeSpec
from core.errors import InvalidInputError, MissingCoreProblemError, TooManyNodesError

# Tier limits as defined in the SKILL.md spec
TIER_LIMITS = {
    "roots": 5,
    "branches": 4,
    "leaf": 3,
}


def validate_schema(spec_dict: Dict[str, Any]) -> ProblemTreeSpec:
    try:
        spec = ProblemTreeSpec(**spec_dict)
    except ValidationError as e:
        raise InvalidInputError(f"Schema validation failed:\n{e}")

    pt = spec.problem_tree

    if not pt.core_problem or not pt.core_problem.statement:
        raise MissingCoreProblemError()

    for tier, limit in TIER_LIMITS.items():
        nodes = getattr(pt, tier, [])
        if len(nodes) > limit:
            raise TooManyNodesError(tier, limit, len(nodes))

    return spec
