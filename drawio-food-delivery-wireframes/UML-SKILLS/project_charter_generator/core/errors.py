"""core/errors.py — PC-001 to PC-010 error codes."""


class CharterError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")


class InvalidInputError(CharterError):
    def __init__(self, detail: str = ""):
        super().__init__("PC-001", f"Invalid input JSON schema. {detail}".strip())


class MissingFieldError(CharterError):
    def __init__(self, field: str):
        super().__init__("PC-002", f"Missing required field: '{field}'")


class InvalidFieldValueError(CharterError):
    def __init__(self, field: str, value: str, hint: str = ""):
        super().__init__("PC-003", f"Invalid value for '{field}': {value}. {hint}".strip())


class GraphvizNotInstalledError(CharterError):
    def __init__(self):
        super().__init__("PC-004", "Graphviz not installed. Ensure 'dot' is in PATH.")


class JavaNotInstalledError(CharterError):
    def __init__(self):
        super().__init__("PC-005", "Java runtime not found. Install JRE 8+ and set JAVA_HOME.")


class LicenseMissingError(CharterError):
    def __init__(self):
        super().__init__("PC-006", "Aspose license missing. Set ASPOSE_DIAGRAM_LICENSE_PATH in .env")


class WordGenerationError(CharterError):
    def __init__(self, detail: str = ""):
        super().__init__("PC-007", f"Word document generation failed. {detail}".strip())


class DiagramTimeoutError(CharterError):
    def __init__(self):
        super().__init__("PC-008", "Diagram rendering timed out. Increase subprocess timeout.")


class DiskSpaceError(CharterError):
    def __init__(self):
        super().__init__("PC-009", "Insufficient disk space.")


class PermissionError_(CharterError):
    def __init__(self, path: str = ""):
        super().__init__("PC-010", f"Permission denied. Check directory permissions. Path: {path}")
