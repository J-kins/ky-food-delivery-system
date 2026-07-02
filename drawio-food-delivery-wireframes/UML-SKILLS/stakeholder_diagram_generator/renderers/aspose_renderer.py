import logging

log = logging.getLogger(__name__)

try:
    from aspose.diagram import Diagram, SaveFileFormat
    _ASPOSE_AVAILABLE = True
except ImportError:
    _ASPOSE_AVAILABLE = False
    log.warning("aspose.diagram not installed — rendering will be skipped.")

    class Diagram:
        def save(self, *args, **kwargs):
            pass

    class SaveFileFormat:
        VSDX = "vsdx"

class BaseAsposeBuilder:
    def __init__(self, config):
        self.config = config
        self.diagram = Diagram()
        
    def save(self, output_path: str):
        if not _ASPOSE_AVAILABLE:
            log.debug(f"[dry-run] Would save {output_path}")
        else:
            self.diagram.save(output_path, SaveFileFormat.VSDX)
