class WBSError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")


class InvalidInputError(WBSError):
    def __init__(self, message: str):
        super().__init__("WB-001", message)


class NoProjectRootError(WBSError):
    def __init__(self):
        super().__init__("WB-002", "No level_0 defined in wbs.levels")


class EmptyProjectNameError(WBSError):
    def __init__(self):
        super().__init__("WB-003", "Project name is empty")


class TooManyLevelsError(WBSError):
    def __init__(self, node_id: str, depth: int):
        super().__init__("WB-004", f"Node '{node_id}' exceeds maximum depth (level {depth} > 3)")


class InvalidLevelIdError(WBSError):
    def __init__(self, node_id: str, parent_id: str):
        super().__init__("WB-005", f"ID '{node_id}' does not match parent prefix '{parent_id}'")


class MissingDescriptionError(WBSError):
    def __init__(self, node_id: str):
        super().__init__("WB-006", f"Node '{node_id}' is missing a description")


class LayoutError(WBSError):
    def __init__(self, message: str):
        super().__init__("WB-009", message)
