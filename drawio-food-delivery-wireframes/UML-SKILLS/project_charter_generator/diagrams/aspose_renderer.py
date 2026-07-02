"""
diagrams/aspose_renderer.py — Aspose.Diagram Visio deck builder (JVM-backed).
"""
from __future__ import annotations

import copy
import logging
import os
from typing import Dict, Optional, Tuple

log = logging.getLogger(__name__)

_DRY_RUN_COUNTER = 0
_ASPOSE_AVAILABLE = False
_Diagram = None
_SaveFileFormat = None
_Page = None

# Layouts are authored for a 24×14 reference canvas; scale to A2 landscape.
_LAYOUT_REF_W = 24.0
_LAYOUT_REF_H = 14.0
_PAGE_W, _PAGE_H = 59.4, 42.0
_LAYOUT_SCALE = min((_PAGE_W - 1.0) / _LAYOUT_REF_W, (_PAGE_H - 3.0) / _LAYOUT_REF_H)


def _ensure_jvm() -> bool:
    global _ASPOSE_AVAILABLE, _Diagram, _SaveFileFormat, _Page
    if _ASPOSE_AVAILABLE:
        return True
    try:
        import jpype
        if not jpype.isJVMStarted():
            jpype.startJVM(convertStrings=False)
        import asposediagram.api as api
        _Diagram = api.Diagram
        _SaveFileFormat = api.SaveFileFormat
        _Page = api.Page
        _ASPOSE_AVAILABLE = True
        return True
    except Exception as exc:
        log.warning("Aspose.Diagram unavailable (%s) — Visio output will be dry-run.", exc)
        return False


def _next_id() -> int:
    global _DRY_RUN_COUNTER
    _DRY_RUN_COUNTER += 1
    return _DRY_RUN_COUNTER


def reset_counter() -> None:
    global _DRY_RUN_COUNTER
    _DRY_RUN_COUNTER = 0


def new_diagram():
    if not _ensure_jvm():
        raise RuntimeError(
            "Aspose.Diagram is not available. Install: pip install aspose-diagram JPype1 "
            "and ensure Java JRE 11+ is installed."
        )
    return _Diagram()


def _setup_page(page, page_w: float, page_h: float) -> None:
    props = page.getPageSheet().getPageProps()
    props.getPageWidth().setValue(page_w)
    props.getPageHeight().setValue(page_h)


def add_rectangle(
    page,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str = "",
    fill_color: str = "#FFFFFF",
    text_color: str = "#000000",
    border_color: str = "#AAAAAA",
    border_width: float = 1.5,
    font_size: float = 10.0,
    font_bold: bool = False,
    no_fill: bool = False,
    no_border: bool = False,
) -> int:
    sid = _next_id()
    if not _ASPOSE_AVAILABLE:
        log.debug(
            "  [shape %03d] rect(%r) pos=(%.1f,%.1f) fill=%s",
            sid, (text or "")[:35], x, y, fill_color,
        )
        return sid
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
    if not _ASPOSE_AVAILABLE:
        return
    try:
        page.drawLine(float(x1), float(y1), float(x2), float(y2))
    except Exception as exc:
        log.debug("drawLine failed: %s", exc)


def draw_orthogonal_connector(
    page,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str = "#666666",
) -> None:
    """Route dependency-style elbow connector between two points."""
    mid_x = (x1 + x2) / 2
    draw_line(page, x1, y1, mid_x, y1)
    draw_line(page, mid_x, y1, mid_x, y2)
    draw_line(page, mid_x, y2, x2, y2)


def add_connector(
    page,
    from_id: int,
    to_id: int,
    color: str = "#666666",
    label: str = "",
    from_xy: tuple = None,
    to_xy: tuple = None,
    orthogonal: bool = True,
) -> int:
    sid = _next_id()
    if not _ASPOSE_AVAILABLE:
        log.debug("  [conn  %03d] %s → %s", sid, from_id, to_id)
        return sid
    if from_xy and to_xy:
        x1, y1 = float(from_xy[0]), float(from_xy[1])
        x2, y2 = float(to_xy[0]), float(to_xy[1])
        if orthogonal:
            draw_orthogonal_connector(page, x1, y1, x2, y2, color)
        else:
            draw_line(page, x1, y1, x2, y2)
    return sid


def save_diagram(diagram, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    if not _ASPOSE_AVAILABLE:
        raise RuntimeError(
            "Aspose.Diagram is not available. Install: pip install aspose-diagram JPype1 "
            "and ensure Java JRE 11+ is installed."
        )
    diagram.save(output_path, _SaveFileFormat.VSDX)
    log.info("  Saved Visio: %s (%d bytes)", output_path, os.path.getsize(output_path))


def verify_vsdx_readable(output_path: str) -> None:
    """Reload a .vsdx with Aspose to confirm it opens without corruption."""
    if not _ensure_jvm():
        raise RuntimeError("Cannot verify Visio — Aspose JVM unavailable.")
    diagram = _Diagram(str(output_path))
    count = diagram.getPages().getCount()
    if count < 1:
        raise RuntimeError(f"Visio file has no pages: {output_path}")
    log.debug("Verified Visio readable: %s (%d pages)", output_path, count)


def _scale_layout(layout: dict, offset_x: float, offset_y: float) -> dict:
    """Scale reference layout coordinates to A2 canvas with margin offset."""
    scaled = copy.deepcopy(layout)
    sx = _LAYOUT_SCALE
    sy = _LAYOUT_SCALE
    for node in scaled.get("nodes", []):
        node["x"] = offset_x + node.get("x", 0) * sx
        node["y"] = offset_y + node.get("y", 0) * sy
        node["w"] = max(0.15, node.get("w", 1) * sx)
        node["h"] = max(0.12, node.get("h", 0.5) * sy)
    return scaled


def _draw_page_chrome(page, title: str, subtitle: str = "") -> None:
    """Professional title bar at top of each analytical diagram page."""
    header_text = title.upper()
    if subtitle:
        header_text += f"\n{subtitle}"
    add_rectangle(
        page,
        _PAGE_W / 2,
        _PAGE_H - 0.55,
        _PAGE_W - 1.0,
        0.9,
        text=header_text,
        fill_color="#1a237e",
        text_color="#FFFFFF",
        border_color="#1a237e",
        font_size=11.0,
        font_bold=True,
        no_border=True,
    )
    add_rectangle(
        page,
        _PAGE_W / 2,
        0.45,
        _PAGE_W - 1.0,
        0.55,
        text="CONFIDENTIAL — Internal Use Only",
        fill_color="#ECEFF1",
        text_color="#546E7A",
        border_color="#90A4AE",
        font_size=7.5,
    )


def _render_layout_page(page, layout: dict, page_title: str = "") -> None:
    """Render nodes and edges with scaled coordinates on A2 page."""
    _setup_page(page, _PAGE_W, _PAGE_H)
    offset_x = 0.5
    offset_y = 1.2
    scaled = _scale_layout(layout, offset_x, offset_y)
    project = layout.get("_project_name", "")
    _draw_page_chrome(page, page_title or layout.get("title", "Diagram"), project)

    shape_map: dict = {}
    positions: dict = {}
    node_bounds: Dict[str, Tuple[float, float, float, float]] = {}

    for node in scaled.get("nodes", []):
        x, y = node.get("x", 0), node.get("y", 0)
        w, h = node.get("w", 2), node.get("h", 1)
        positions[node["id"]] = (x, y)
        node_bounds[node["id"]] = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
        tier = node.get("tier", "")
        font_size = 8.0 if tier in ("cell", "axis_label", "risk", "stakeholder") else 9.0
        font_bold = tier in ("trunk", "system", "quadrant", "member") and node.get("y", 0) > 6
        sid = add_rectangle(
            page,
            x=x, y=y,
            w=w, h=h,
            text=str(node.get("text", "")),
            fill_color=node.get("fill", "#FFFFFF"),
            text_color=node.get("text_color", "#000000"),
            border_color=node.get("border", "#AAAAAA"),
            font_size=font_size,
            font_bold=font_bold,
        )
        shape_map[node["id"]] = sid

    for edge in scaled.get("edges", []):
        src_id = edge.get("from")
        dst_id = edge.get("to")
        src_xy = positions.get(src_id)
        dst_xy = positions.get(dst_id)
        if not src_xy or not dst_xy:
            continue
        x1, y1, x2, y2 = src_xy[0], src_xy[1], dst_xy[0], dst_xy[1]
        sb = node_bounds.get(src_id)
        db = node_bounds.get(dst_id)
        if sb and db:
            x1 = sb[2]
            y1 = (sb[1] + sb[3]) / 2
            x2 = db[0]
            y2 = (db[1] + db[3]) / 2
        add_connector(
            page, 0, 0,
            color=edge.get("color", "#666666"),
            from_xy=(x1, y1), to_xy=(x2, y2),
            orthogonal=True,
        )


def build_visio_deck(payload: dict, diagram_paths: dict, output_path: str) -> str:
    """Build multi-page editable Visio deck via Aspose.Diagram."""
    from config.settings import apply_aspose_diagram_license
    from diagrams.layouts import (
        layout_milestone_timeline,
        layout_org_chart,
        layout_problem_tree,
        layout_risk_matrix,
        layout_scope_boundary,
        layout_stakeholder_matrix,
        layout_system_context,
    )

    reset_counter()
    apply_aspose_diagram_license()
    _ensure_jvm()

    project_name = payload.get("project", {}).get("name", "")
    pages = [
        ("Problem Tree", layout_problem_tree(payload)),
        ("Stakeholder Matrix", layout_stakeholder_matrix(payload)),
        ("Scope Boundary", layout_scope_boundary(payload)),
        ("Org Chart", layout_org_chart(payload)),
        ("Milestone Timeline", layout_milestone_timeline(payload)),
        ("Risk Matrix", layout_risk_matrix(payload)),
        ("System Context", layout_system_context(payload)),
    ]

    if _ASPOSE_AVAILABLE:
        diagram = _Diagram()
        for idx, (name, layout) in enumerate(pages):
            layout["_project_name"] = project_name
            if idx == 0:
                page = diagram.getPages().get(0)
            else:
                new_page = _Page()
                diagram.getPages().add(new_page)
                page = diagram.getPages().get(diagram.getPages().getCount() - 1)
            page.setName(name[:31])
            _render_layout_page(page, layout, page_title=name)
            log.info("Visio page rendered: %s (%d nodes)", name, len(layout.get("nodes", [])))
        save_diagram(diagram, output_path)
        verify_vsdx_readable(output_path)
    else:
        raise RuntimeError(
            "Aspose.Diagram JVM failed to start. Check Java installation and aspose-diagram package."
        )

    return output_path
