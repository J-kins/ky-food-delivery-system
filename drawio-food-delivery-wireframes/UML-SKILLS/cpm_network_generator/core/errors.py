class CpmError(Exception):
    """Base exception for CPM errors."""
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")

class InvalidInputError(CpmError):
    def __init__(self, message: str):
        super().__init__("CPM-001", message)

class NoActivitiesError(CpmError):
    def __init__(self):
        super().__init__("CPM-002", "Empty activities list. Provide at least 2 activities.")

class CycleDetectedError(CpmError):
    def __init__(self):
        super().__init__("CPM-003", "Cycle detected in network diagram. AON cannot have cycles.")

class MissingReferenceError(CpmError):
    def __init__(self, ref_id: str):
        super().__init__("CPM-004", f"Predecessor points to missing id: '{ref_id}'")

class InvalidLagError(CpmError):
    def __init__(self):
        super().__init__("CPM-005", "Lag value must be an integer.")

class InvalidDepTypeError(CpmError):
    def __init__(self, t: str):
        super().__init__("CPM-006", f"Dependency type '{t}' is not FS, SS, FF, or SF.")
