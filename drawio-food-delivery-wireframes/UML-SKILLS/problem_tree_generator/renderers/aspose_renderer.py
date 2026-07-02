import logging
from typing import Optional

log = logging.getLogger(__name__)

_DRY_RUN_COUNTER = 0


def _next_id() -> int:
    global _DRY_RUN_COUNTER
    _DRY_RUN_COUNTER += 1
    return _DRY_RUN_COUNTER


try:
    from aspose.diagram import Diagram, SaveFileFormat
    _ASPOSE_AVAILABLE = True
except ImportError:
    _ASPOSE_AVAILABLE = False
    log.warning("aspose.diagram not installed — rendering will be skipped.")

    class DummyProps:
        def __init__(self):
            self.page_width = type("W", (), {"value": 0})()
            self.page_height = type("H", (), {"value": 0})()

    class DummySheet:
        def __init__(self):
            self.page_props = DummyProps()

    class DummyPage:
        def __init__(self):
            self.page_sheet = DummySheet()

    class Diagram:
        def __init__(self, *args, **kwargs):
            self.pages = type("Pages", (), {"get": lambda self, idx: DummyPage()})()

        def save(self, *args, **kwargs):
            pass

    class SaveFileFormat:
        VSDX = "vsdx"


def add_rectangle(
    page,
    x: float, y: float,
    w: float, h: float,
    text: str = "",
    fill_color: str = "#FFFFFF",
    text_color: str = "#000000",
    border_color: str = "#000000",
    border_width: float = 1.5,
    font_family: str = "Arial",
    font_size: float = 10.0,
    font_bold: bool = False,
    shadow: bool = False,
) -> Optional[int]:
    sid = _next_id()
    if not _ASPOSE_AVAILABLE:
        log.debug(
            f"[dry-run] rect[{sid}] text={text!r:30s} "
            f"pos=({x:.2f},{y:.2f}) size={w:.2f}×{h:.2f} "
            f"fill={fill_color}"
        )
        return sid

    shape = page.add_shape(x, y, w, h, "Rectangle")
    shape.text.value = text
    shape.fill.fill_foregnd.value = fill_color
    shape.fill.fill_bkgnd.value = fill_color
    shape.line.line_weight.value = border_width / 72.0
    shape.line.line_color.value = border_color
    if shape.chars.count > 0:
        ch = shape.chars[0]
        ch.font.value = font_family
        ch.size.value = font_size / 72.0
        ch.bold.value = 1 if font_bold else 0
        ch.color.value = text_color
    if shadow:
        shape.fill.shadow_foregnd.value = "#CCCCCC"
    return shape.id


def add_connector(
    page,
    from_shape_id: int,
    to_shape_id: int,
    line_color: str = "#666666",
    line_width: float = 1.0,
    dashed: bool = False,
    label: str = "",
    font_size: float = 8.0,
    font_family: str = "Arial",
) -> Optional[int]:
    sid = _next_id()
    if not _ASPOSE_AVAILABLE:
        log.debug(
            f"[dry-run] connector[{sid}] {from_shape_id} → {to_shape_id} "
            f"label={label!r} color={line_color}"
        )
        return sid

    connector = page.add_shape(0, 0, "Dynamic connector")
    connector.text.value = label
    page.connect_shapes_via_connector(
        from_shape_id, "Port", to_shape_id, "Port", connector.id
    )
    connector.line.line_weight.value = line_width / 72.0
    connector.line.line_color.value = line_color
    connector.line.line_pattern.value = 2 if dashed else 1
    connector.line.end_arrow.value = 4  # filled triangle
    if connector.chars.count > 0:
        ch = connector.chars[0]
        ch.font.value = font_family
        ch.size.value = font_size / 72.0
        ch.color.value = line_color
    return connector.id
