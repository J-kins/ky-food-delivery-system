from typing import Dict, Any
from pydantic import ValidationError
from core.models import KanbanSpec
from core.errors import InvalidInputError, InvalidAssignmentError, WIPLimitExceededError

def validate_kanban(spec_dict: Dict[str, Any]) -> KanbanSpec:
    try:
        spec = KanbanSpec(**spec_dict)
    except ValidationError as e:
        raise InvalidInputError(f"Schema validation failed:\n{e}")

    kb = spec.kanban_chart
    
    col_ids = {c.id for c in kb.columns}
    swim_ids = {s.id for s in kb.swimlanes}
    
    # Calculate items per column to check WIP
    col_counts = {c.id: 0 for c in kb.columns}

    for item in kb.work_items:
        if item.status not in col_ids:
            raise InvalidAssignmentError(item.id, "status", item.status)
        if item.swimlane_id not in swim_ids:
            raise InvalidAssignmentError(item.id, "swimlane_id", item.swimlane_id)
            
        col_counts[item.status] += 1

    # Check WIP Limits
    for col in kb.columns:
        if col.wip_limit is not None and col_counts[col.id] > col.wip_limit:
            raise WIPLimitExceededError(col.id, col.wip_limit, col_counts[col.id])

    return spec
