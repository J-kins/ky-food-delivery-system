class GanttError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")

class InvalidDateError(GanttError):
    def __init__(self, message: str):
        super().__init__("Gantt-001", message)

class MissingDependencyError(GanttError):
    def __init__(self, dep_id: str):
        super().__init__("Gantt-002", f"Dependency points to missing task/milestone ID: {dep_id}")

class InvalidCompletionError(GanttError):
    def __init__(self):
        super().__init__("Gantt-003", "Completion percentage must be between 0 and 100")

class InvalidInputError(GanttError):
    def __init__(self, message: str):
        super().__init__("Gantt-004", message)
