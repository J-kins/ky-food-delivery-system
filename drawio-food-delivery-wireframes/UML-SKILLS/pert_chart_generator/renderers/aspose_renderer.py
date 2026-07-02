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

class AsposePertRenderer:
    """Wraps Aspose.Diagram logic with a dry-run stub for testing without a license."""
    def __init__(self, config):
        self.config = config
        self.diagram = Diagram()
        self.shape_id_counter = 0

    def add_pert_node(self, node_id: str, text: str, x: float, y: float, w: float, h: float, is_critical: bool) -> int:
        self.shape_id_counter += 1
        sid = self.shape_id_counter
        
        border_color = "#E53935" if is_critical else "#000000"
        
        if not _ASPOSE_AVAILABLE:
            log.debug(f"[dry-run] PERT Node '{node_id}' | Pos: ({x:.2f}, {y:.2f}) | Border: {border_color} | Critical: {is_critical}\nText:\n{text}")
        return sid
        
    def add_directed_edge(self, from_id: int, to_id: int, is_critical: bool) -> int:
        self.shape_id_counter += 1
        sid = self.shape_id_counter
        
        color = "#E53935" if is_critical else "#666666"
        thickness = "3pt" if is_critical else "1pt"
        
        if not _ASPOSE_AVAILABLE:
            log.debug(f"[dry-run] Directed Edge {from_id} -> {to_id} | Color: {color} | Thickness: {thickness}")
        return sid

    def save(self, output_path: str):
        if not _ASPOSE_AVAILABLE:
            log.debug(f"[dry-run] Saved chart to {output_path}")
        else:
            self.diagram.save(output_path, SaveFileFormat.VSDX)
