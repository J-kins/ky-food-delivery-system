from typing import Dict, Any
from core.models import StakeholderSpec

def validate_and_enrich(spec_dict: Dict[str, Any]) -> StakeholderSpec:
    """Validates the raw dictionary and auto-classifies engagement strategies."""
    spec = StakeholderSpec(**spec_dict)
    
    if spec.stakeholder_register:
        for s in spec.stakeholder_register.stakeholders:
            if s.engagement_strategy == "auto" or not s.engagement_strategy:
                # Auto classification based on Power/Interest
                if s.power == "High" and s.interest == "High":
                    s.engagement_strategy = "Manage Closely"
                elif s.power == "High" and s.interest in ["Medium", "Low"]:
                    s.engagement_strategy = "Keep Satisfied"
                elif s.power in ["Medium", "Low"] and s.interest == "High":
                    s.engagement_strategy = "Keep Informed"
                else:
                    s.engagement_strategy = "Monitor"
                    
    return spec
