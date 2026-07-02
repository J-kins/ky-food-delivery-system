class MilestoneError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")

class InvalidDateError(MilestoneError):
    def __init__(self, message: str):
        super().__init__("Milestone-001", message)

class OutOfBoundsError(MilestoneError):
    def __init__(self, item_type: str, item_id: str, date_val: str, bounds: str):
        super().__init__("Milestone-002", f"{item_type} '{item_id}' date '{date_val}' is outside project bounds {bounds}")

class InvalidInputError(MilestoneError):
    def __init__(self, message: str):
        super().__init__("Milestone-003", message)
