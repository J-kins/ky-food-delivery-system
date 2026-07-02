"""Compile Graphviz/D2 source to SVG XML for Word embedding."""
from __future__ import annotations

import logging
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Optional, Tuple

from config.settings import get_d2_path, get_dot_path
from core.errors import GraphvizNotInstalledError
from diagrams.description_schema import DiagramDescription
from diagrams.source_builder import description_to_d2, description_to_dot

log = logging.getLogger(__name__)


def compile_description_to_svg(
    desc: DiagramDescription,
    source_dir: Path,
    svg_dir: Path,
) -> Dict[str, str]:
    """
    Compile a diagram description to source + SVG XML files.

    Returns paths: source, svg, svg_xml (same as svg — SVG is XML).
    """
    source_dir.mkdir(parents=True, exist_ok=True)
    svg_dir.mkdir(parents=True, exist_ok=True)
    diagram_id = desc.id

    if desc.format == "d2":
        source_text = description_to_d2(desc)
        source_path = source_dir / f"{diagram_id}.d2"
        svg_path = svg_dir / f"{diagram_id}.svg"
        source_path.write_text(source_text, encoding="utf-8")
        _run_d2(source_path, svg_path)
    else:
        source_text = description_to_dot(desc)
        source_path = source_dir / f"{diagram_id}.dot"
        svg_path = svg_dir / f"{diagram_id}.svg"
        source_path.write_text(source_text, encoding="utf-8")
        _run_graphviz(source_text, svg_path, engine=desc.engine)

    svg_xml = svg_path.read_text(encoding="utf-8")
    _validate_svg(svg_xml)

    return {
        "id": diagram_id,
        "title": desc.title,
        "format": desc.format,
        "source": str(source_path),
        "svg": str(svg_path),
        "svg_xml": svg_xml,
        "caption": desc.caption or desc.title,
    }


def _run_graphviz(dot_source: str, svg_path: Path, engine: str = "dot") -> None:
    dot_bin = get_dot_path()
    if not shutil.which(dot_bin) and dot_bin == "dot":
        raise GraphvizNotInstalledError()

    cmd = [dot_bin if engine == "dot" else engine, "-Tsvg", "-o", str(svg_path)]
    result = subprocess.run(cmd, input=dot_source, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Graphviz failed: {result.stderr.strip()}")
    log.debug("Graphviz compiled → %s", svg_path)


def _run_d2(source_path: Path, svg_path: Path) -> None:
    d2_bin = get_d2_path()
    if not shutil.which(d2_bin):
        raise RuntimeError(
            f"D2 CLI not found at '{d2_bin}'. Install from https://d2lang.com or set D2_PATH."
        )
    result = subprocess.run([d2_bin, str(source_path), str(svg_path)], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"D2 compile failed: {result.stderr.strip()}")
    log.debug("D2 compiled → %s", svg_path)


def _validate_svg(svg_xml: str) -> None:
    try:
        ET.fromstring(svg_xml)
    except ET.ParseError as exc:
        raise RuntimeError(f"Invalid SVG XML produced: {exc}") from exc


def description_to_svg_xml(desc: DiagramDescription, output_path: Path) -> str:
    """Render diagram description to SVG XML without Graphviz/D2 (pure Python)."""
    width, height = 2600, 1400
    n = max(len(desc.nodes), 1)
    cols = min(4, n)
    rows = (n + cols - 1) // cols
    cell_w = width / (cols + 1)
    cell_h = height / (rows + 2)

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="40" y="50" font-family="Arial" font-size="24" font-weight="bold" '
        f'fill="#1a237e">{_esc(desc.title)}</text>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" '
        'orient="auto"><path d="M0,0 L10,3 L0,6 Z" fill="#666"/></marker></defs>',
    ]

    centers: Dict[str, Tuple[float, float]] = {}
    for i, node in enumerate(desc.nodes):
        col, row = i % cols, i // cols
        cx = cell_w * (col + 1)
        cy = cell_h * (row + 1.5)
        box_w = min(cell_w * 0.85, 520)
        box_h = min(cell_h * 0.7, 120)
        x0, y0 = cx - box_w / 2, cy - box_h / 2
        fill = node.fill or "#FFFFFF"
        border = node.border or "#666666"
        parts.append(
            f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{box_w:.1f}" height="{box_h:.1f}" '
            f'rx="8" fill="{fill}" stroke="{border}" stroke-width="2"/>'
        )
        label = _esc(node.label.replace("\\n", " "))
        parts.append(
            f'<text x="{x0 + 10:.1f}" y="{y0 + 28:.1f}" font-family="Arial" font-size="13" '
            f'fill="{node.text_color or "#000"}">{label}</text>'
        )
        centers[node.id] = (cx, cy)

    id_map = {node.id: node.id for node in desc.nodes}
    for edge in desc.edges:
        src = centers.get(edge.from_id)
        dst = centers.get(edge.to_id)
        if src and dst:
            color = edge.color or "#666666"
            parts.append(
                f'<line x1="{src[0]:.1f}" y1="{src[1]:.1f}" x2="{dst[0]:.1f}" y2="{dst[1]:.1f}" '
                f'stroke="{color}" stroke-width="2" marker-end="url(#arrow)"/>'
            )

    parts.append("</svg>")
    svg = "\n".join(parts)
    output_path.write_text(svg, encoding="utf-8")
    _validate_svg(svg)
    return svg


def layout_to_svg_xml(layout: dict, output_path: Path) -> str:
    """Fallback: emit SVG XML directly from layout dict (no Graphviz required)."""
    width = 2600
    height = 1400
    scale = width / 26.0

    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        f'<rect width="100%" height="100%" fill="white"/>',
        f'<text x="20" y="40" font-family="Arial" font-size="22" font-weight="bold" '
        f'fill="#1a237e">{_esc(layout.get("title", ""))}</text>',
    ]

    centers: Dict[str, Tuple[float, float]] = {}
    for node in layout.get("nodes", []):
        x_in, y_in = node.get("x", 0), node.get("y", 0)
        w_in, h_in = node.get("w", 2), node.get("h", 1)
        x0 = (x_in - w_in / 2) * scale
        y0 = (y_in - h_in / 2) * scale
        w = w_in * scale
        h = h_in * scale
        fill = node.get("fill", "#FFFFFF")
        border = node.get("border", "#AAAAAA")
        parts.append(
            f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="8" fill="{fill}" stroke="{border}" stroke-width="2"/>'
        )
        label = _esc(str(node.get("text", "")))
        for i, line in enumerate(label.split("\\n")):
            parts.append(
                f'<text x="{x0 + 8:.1f}" y="{y0 + 22 + i * 16:.1f}" '
                f'font-family="Arial" font-size="12" fill="#000">{line}</text>'
            )
        centers[node["id"]] = (x0 + w / 2, y0 + h / 2)

    for edge in layout.get("edges", []):
        src = centers.get(edge.get("from"))
        dst = centers.get(edge.get("to"))
        if src and dst:
            color = edge.get("color", "#666666")
            parts.append(
                f'<line x1="{src[0]:.1f}" y1="{src[1]:.1f}" x2="{dst[0]:.1f}" y2="{dst[1]:.1f}" '
                f'stroke="{color}" stroke-width="2" marker-end="url(#arrow)"/>'
            )

    parts.append(
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" '
        'orient="auto"><path d="M0,0 L10,3 L0,6 Z" fill="#666"/></marker></defs>'
    )
    parts.append("</svg>")
    svg = "\n".join(parts)
    output_path.write_text(svg, encoding="utf-8")
    return svg


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
