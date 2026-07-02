class DiagramError(Exception):
    """Base class for all Communication Diagram exceptions."""
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")


class InvalidInputError(DiagramError):
    def __init__(self, message: str = "Input JSON missing required fields"):
        super().__init__("CD-001", message)


class NoParticipantsError(DiagramError):
    def __init__(self):
        super().__init__("CD-002", "No participants defined — add at least one participant")


class NoMessagesError(DiagramError):
    def __init__(self):
        super().__init__("CD-003", "No messages defined — add at least one message")


class InvalidParticipantRefError(DiagramError):
    def __init__(self, ref: str, sequence: str = ""):
        super().__init__("CD-004", f"Message {sequence!r} references unknown participant: {ref!r}")


class DuplicateSequenceError(DiagramError):
    def __init__(self, sequence: str):
        super().__init__("CD-005", f"Duplicate sequence number: {sequence!r}")


class InvalidSequenceFormatError(DiagramError):
    def __init__(self, sequence: str):
        super().__init__("CD-006", f"Invalid sequence number format: {sequence!r} — use e.g. 1, 1.1, 2.3.1")


class CircularDependencyError(DiagramError):
    def __init__(self):
        super().__init__("CD-007", "Circular message dependency detected — check message flow")


class JavaNotInstalledError(DiagramError):
    def __init__(self):
        super().__init__("CD-008", "Java runtime not found — install JRE 8+ and set JAVA_HOME")


class LicenseMissingError(DiagramError):
    def __init__(self):
        super().__init__("CD-009", "Aspose license missing — set ASPOSE_DIAGRAM_LICENSE_PATH in .env")


class RenderError(DiagramError):
    def __init__(self, detail: str = ""):
        super().__init__("CD-010", f"Rendering failed — check Aspose.Diagram installation. {detail}".strip())
