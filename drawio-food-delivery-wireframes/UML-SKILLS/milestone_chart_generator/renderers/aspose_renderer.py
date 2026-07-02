"""Aspose.Diagram helpers for milestone chart rendering."""
from __future__ import annotations

import logging
import os

log = logging.getLogger(__name__)

_ASPOSE_AVAILABLE = False
_Diagram = None
_SaveFileFormat = None
_SHAPE_ID = 0


def _ensure_jvm() -> bool:
    global _ASPOSE_AVAILABLE, _Diagram, _SaveFileFormat
    if _ASPOSE_AVAILABLE:
        return True
    try:
        import jpype
        if not jpype.isJVMStarted():
            jpype.startJVM(convertStrings=False)
        import asposediagram.api as api
        _Diagram = api.Diagram
        _SaveFileFormat = api.SaveFileFormat
        _ASPOSE_AVAILABLE = True
        return True
    except Exception as exc:
        log.warning("Aspose.Diagram unavailable (%s) — Visio output will fail.", exc)
        return False


def reset_counter() -> None:
    global _SHAPE_ID
    _SHAPE_ID = 0


def new_diagram():
    if not _ensure_jvm():
        raise RuntimeError(
            "Aspose.Diagram is not available. Install: pip install aspose-diagram JPype1 "
            "and ensure Java JRE 11+ is installed."
        )
    return _Diagram()


def add_rectangle(
    page,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str = "",
    fill_color: str = "#FFFFFF",
    border_color: str = "#CCCCCC",
    border_width: float = 1.0,
    font_size: float = 9.0,
    font_bold: bool = False,
    no_fill: bool = False,
    no_border: bool = False,
) -> int:
    global _SHAPE_ID
    _SHAPE_ID += 1
    sid = _SHAPE_ID
    try:
        shape = page.addText(x - w / 2, y - h / 2, w, h, text or " ")
        if no_fill:
            if shape.getFill() is not None:
                shape.getFill().getFillPattern().setValue(0)
        elif shape.getFill() is not None:
            shape.getFill().getFillForegnd().setValue(fill_color)
            shape.getFill().getFillBkgnd().setValue(fill_color)
        if shape.getLine() is not None:
            if no_border:
                shape.getLine().getLinePattern().setValue(0)
            else:
                shape.getLine().getLineColor().setValue(border_color)
                shape.getLine().getLineWeight().setValue(border_width / 72.0)
        return int(shape.getID())
    except Exception as exc:
        log.debug("  [shape %03d] addText failed: %s", sid, exc)
        return sid


def draw_line(page, x1: float, y1: float, x2: float, y2: float) -> None:
    try:
        page.drawLine(float(x1), float(y1), float(x2), float(y2))
    except Exception as exc:
        log.debug("drawLine failed: %s", exc)


def save_diagram(diagram, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    if not _ASPOSE_AVAILABLE:
        raise RuntimeError("Aspose.Diagram JVM is not running.")
    diagram.save(output_path, _SaveFileFormat.VSDX)
    log.info("Milestone chart saved to %s (%d bytes)", output_path, os.path.getsize(output_path))
