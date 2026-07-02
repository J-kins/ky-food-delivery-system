class KanbanError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")

class InvalidAssignmentError(KanbanError):
    def __init__(self, item_id: str, field: str, value: str):
        super().__init__("Kanban-001", f"WorkItem {item_id} assigns to invalid {field}: {value}")

class WIPLimitExceededError(KanbanError):
    def __init__(self, col_id: str, limit: int, actual: int):
        super().__init__("Kanban-002", f"Column '{col_id}' exceeds WIP limit ({actual}/{limit})")

class InvalidInputError(KanbanError):
    def __init__(self, message: str):
        super().__init__("Kanban-003", message)
