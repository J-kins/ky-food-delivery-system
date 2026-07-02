"""
Low-level Aspose.Diagram helpers for Communication Diagram rendering.
Coordinates are in inches (Visio page units).
"""
from __future__ import annotations

import logging
import os
from typing import Optional

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
    text_color: str = "#000000",
    border_color: str = "#000000",
    border_width: float = 1.0,
    corner_radius: float = 0.0,
    font_family: str = "Arial",
    font_size: float = 9.0,
    font_bold: bool = False,
    shadow: bool = False,
    line_pattern: int = 1,
    no_fill: bool = False,
    no_border: bool = False,
) -> Optional[int]:
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
            if no_border or line_pattern == 0:
                shape.getLine().getLinePattern().setValue(0)
            else:
                shape.getLine().getLineColor().setValue(border_color)
                shape.getLine().getLineWeight().setValue(border_width / 72.0)
                if line_pattern == 2:
                    shape.getLine().getLinePattern().setValue(2)
        return int(shape.getID())
    except Exception as exc:
        log.debug("  [shape %03d] addText failed: %s", sid, exc)
        return sid


def draw_line(page, x1: float, y1: float, x2: float, y2: float) -> None:
    try:
        page.drawLine(float(x1), float(y1), float(x2), float(y2))
    except Exception as exc:
        log.debug("drawLine failed: %s", exc)


def add_connector(
    page,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    label: str = "",
    line_color: str = "#1a237e",
    line_width: float = 1.0,
    dashed: bool = False,
    font_size: float = 8.0,
    font_family: str = "Arial",
) -> None:
    draw_line(page, x1, y1, x2, y2)
    if label:
        mx = (x1 + x2) / 2.0
        my = (y1 + y2) / 2.0
        lw = max(len(label) * 0.08, 1.5)
        add_rectangle(
            page,
            mx,
            my + 0.15,
            lw,
            0.45,
            text=label,
            fill_color="#FFFFFF",
            border_color="#FFFFFF",
            font_size=font_size,
            no_border=True,
        )


def add_text_box(
    page,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    text_color: str = "#000000",
    font_family: str = "Arial",
    font_size: float = 8.0,
    font_bold: bool = False,
) -> Optional[int]:
    return add_rectangle(
        page,
        x,
        y,
        w,
        h,
        text=text,
        text_color=text_color,
        font_family=font_family,
        font_size=font_size,
        font_bold=font_bold,
        no_fill=True,
        no_border=True,
    )


def save_diagram(diagram, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    if not _ASPOSE_AVAILABLE:
        raise RuntimeError("Aspose.Diagram JVM is not running.")
    diagram.save(output_path, _SaveFileFormat.VSDX)
    log.info("Communication diagram saved to %s (%d bytes)", output_path, os.path.getsize(output_path))
