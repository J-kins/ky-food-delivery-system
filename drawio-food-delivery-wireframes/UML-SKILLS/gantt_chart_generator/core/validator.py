from typing import Dict, Any
from dateutil import parser
from pydantic import ValidationError
from core.models import GanttSpec
from core.errors import InvalidInputError, InvalidDateError, MissingDependencyError, InvalidCompletionError

def validate_gantt(spec_dict: Dict[str, Any]) -> GanttSpec:
    try:
        spec = GanttSpec(**spec_dict)
    except ValidationError as e:
        raise InvalidInputError(f"Schema validation failed:\n{e}")

    gantt = spec.gantt_chart
    
    # 1. Project dates check
    try:
        p_start = parser.parse(gantt.start_date)
        p_end = parser.parse(gantt.end_date)
    except Exception as e:
        raise InvalidDateError("Invalid project start_date or end_date format.")
        
    if p_start >= p_end:
        raise InvalidDateError("Project start_date must be strictly before end_date.")

    all_ids = set()
    
    # Check phases and tasks
    for p in gantt.phases:
        for t in p.tasks:
            all_ids.add(t.id)
            if not (0 <= t.completion <= 100):
                raise InvalidCompletionError()
            try:
                t_s = parser.parse(t.start)
                t_e = parser.parse(t.end)
                if t_s > t_e:
                    raise InvalidDateError(f"Task {t.id} start date is after end date.")
                if t_s < p_start or t_e > p_end:
                    # Optional: Could warn or raise. We'll let it pass but maybe it overflows.
                    pass
            except Exception:
                raise InvalidDateError(f"Invalid date format in task {t.id}.")

    # Add milestones
    for m in gantt.milestones:
        all_ids.add(m.id)
        try:
            parser.parse(m.date)
        except Exception:
            raise InvalidDateError(f"Invalid date format in milestone {m.id}.")

    # Validate dependencies
    for p in gantt.phases:
        for t in p.tasks:
            for dep in t.dependencies:
                if dep not in all_ids:
                    raise MissingDependencyError(dep)
                    
    for m in gantt.milestones:
        for dep in m.dependencies:
            if dep not in all_ids:
                raise MissingDependencyError(dep)

    return spec
