from typing import Dict, Any
from pydantic import ValidationError
from core.models import CpmSpec, PredecessorObj
from core.errors import InvalidInputError, NoActivitiesError, MissingReferenceError

def validate(spec_dict: Dict[str, Any]) -> CpmSpec:
    """Validates the raw dictionary against schemas and business rules."""
    try:
        spec = CpmSpec(**spec_dict)
    except ValidationError as e:
        raise InvalidInputError(f"Schema validation failed:\n{e}")

    activities = spec.cpm_network.activities
    if len(activities) < 2:
        raise NoActivitiesError()
        
    activity_ids = {act.id for act in activities}

    for act in activities:
        for pred in act.predecessors:
            if isinstance(pred, str):
                pid = pred
            else:
                pid = pred.id
                
            if pid not in activity_ids:
                raise MissingReferenceError(pid)

    return spec
