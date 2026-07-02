class PertError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")

class CyclicDependencyError(PertError):
    def __init__(self):
        super().__init__("Pert-001", "A cyclic dependency was detected in the project network. PERT charts must be Directed Acyclic Graphs (DAGs).")

class MissingDependencyError(PertError):
    def __init__(self, item_id: str):
        super().__init__("Pert-002", f"Dependency references a missing task ID: {item_id}")

class InvalidInputError(PertError):
    def __init__(self, message: str):
        super().__init__("Pert-003", message)
