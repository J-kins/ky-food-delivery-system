from typing import Dict, Any
from dateutil import parser
from pydantic import ValidationError
from core.models import MilestoneSpec
from core.errors import InvalidInputError, InvalidDateError, OutOfBoundsError

def validate_milestones(spec_dict: Dict[str, Any]) -> MilestoneSpec:
    try:
        spec = MilestoneSpec(**spec_dict)
    except ValidationError as e:
        raise InvalidInputError(f"Schema validation failed:\n{e}")

    mc = spec.milestone_chart
    
    try:
        p_start = parser.parse(mc.start_date)
        p_end = parser.parse(mc.end_date)
    except Exception:
        raise InvalidDateError("Invalid project start_date or end_date format.")
        
    if p_start >= p_end:
        raise InvalidDateError("Project start_date must be strictly before end_date.")

    bounds_str = f"[{mc.start_date} to {mc.end_date}]"

    for p in mc.phases:
        try:
            ph_s = parser.parse(p.start)
            ph_e = parser.parse(p.end)
            if ph_s > ph_e:
                raise InvalidDateError(f"Phase {p.id} start date is after end date.")
            
            # Check bounds
            if ph_s < p_start or ph_e > p_end:
                raise OutOfBoundsError("Phase", p.id, f"{p.start} - {p.end}", bounds_str)
                
        except InvalidDateError:
            raise
        except Exception:
            raise InvalidDateError(f"Invalid date format in phase {p.id}.")

    for m in mc.milestones:
        try:
            m_date = parser.parse(m.date)
            
            if m_date < p_start or m_date > p_end:
                raise OutOfBoundsError("Milestone", m.id, m.date, bounds_str)
                
        except OutOfBoundsError:
            raise
        except Exception:
            raise InvalidDateError(f"Invalid date format in milestone {m.id}.")

    return spec
