from typing import Dict, Any
from pydantic import ValidationError
from core.models import BudgetSpec
from core.errors import InvalidInputError, CategoryMismatchError, InvalidFormulaError

def validate(spec_dict: Dict[str, Any]) -> BudgetSpec:
    """Validates the raw dictionary against schemas and business rules."""
    try:
        spec = BudgetSpec(**spec_dict)
    except ValidationError as e:
        raise InvalidInputError(f"Schema validation failed:\n{e}")

    budget = spec.budget
    category_names = {cat.name for cat in budget.categories}

    for item in budget.line_items:
        if item.category not in category_names:
            raise CategoryMismatchError(item.category)
        
        # Validate simple math
        if round(item.qty * item.unit_cost, 2) != round(item.total, 2):
            raise InvalidFormulaError(item.item)

    return spec
