class ProblemTreeError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")


class InvalidInputError(ProblemTreeError):
    def __init__(self, message: str):
        super().__init__("PT-001", message)


class MissingCoreProblemError(ProblemTreeError):
    def __init__(self):
        super().__init__("PT-002", "A core_problem (trunk) must be defined.")


class TooManyNodesError(ProblemTreeError):
    def __init__(self, tier: str, limit: int, actual: int):
        super().__init__("PT-003", f"Too many nodes in '{tier}' tier: {actual} provided, max is {limit}.")
