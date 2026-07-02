class BudgetError(Exception):
    """Base exception for budget breakdown errors."""
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")

class InvalidInputError(BudgetError):
    def __init__(self, message: str):
        super().__init__("BG-001", message)

class CategoryMismatchError(BudgetError):
    def __init__(self, category: str):
        super().__init__("BG-002", f"Line item references undefined category: '{category}'")

class InvalidFormulaError(BudgetError):
    def __init__(self, item: str):
        super().__init__("BG-003", f"Line item total does not equal qty * unit_cost: '{item}'")
