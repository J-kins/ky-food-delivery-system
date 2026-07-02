"""SVG parsing utilities for stencil conversion."""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from svg.path import parse_path

from .utils import parse_length, polygon_points, rounded_rect_points

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
NS = {"svg": SVG_NS}


@dataclass
class Style:
    fill: Optional[str] = None
    stroke: Optional[str] = None
    stroke_width: Optional[float] = None
    stroke_dasharray: Optional[str] = None
    font_family: Optional[str] = None
    font_size: Optional[float] = None
    text_anchor: Optional[str] = None


@dataclass
class MarkerDef:
    id: str
    path_d: str
    ref_x: float
    ref_y: float
    width: float
    height: float
    fill: Optional[str] = None
    stroke: Optional[str] = None


@dataclass
class SvgElement:
    kind: str
    style: Style
    points: List[tuple[float, float]] = field(default_factory=list)
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    cx: float = 0.0
    cy: float = 0.0
    rx: float = 0.0
    ry: float = 0.0
    r: float = 0.0
    x1: float = 0.0
    y1: float = 0.0
    x2: float = 0.0
    y2: float = 0.0
    path_d: str = ""
    text: str = ""
    closed: bool = False
    marker_end: Optional[str] = None
    marker_start: Optional[str] = None


@dataclass
class ParsedSvg:
    path: Path
    viewbox: tuple[float, float, float, float]
    default_style: Style
    elements: List[SvgElement]
    markers: Dict[str, MarkerDef]

    @property
    def width(self) -> float:
        return self.viewbox[2]

    @property
    def height(self) -> float:
        return self.viewbox[3]


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _parse_style(node: ET.Element, inherited: Style) -> Style:
    fill = node.get("fill", inherited.fill)
    stroke = node.get("stroke", inherited.stroke)
    stroke_width = node.get("stroke-width")
    return Style(
        fill=fill,
        stroke=stroke,
        stroke_width=parse_length(stroke_width, inherited.stroke_width or 1.0),
        stroke_dasharray=node.get("stroke-dasharray", inherited.stroke_dasharray),
        font_family=node.get("font-family", inherited.font_family),
        font_size=parse_length(node.get("font-size"), inherited.font_size or 12.0),
        text_anchor=node.get("text-anchor", inherited.text_anchor),
    )


def _collect_defs_nodes(root: ET.Element) -> set[int]:
    skipped: set[int] = set()
    for node in root.iter():
        if _local_name(node.tag) == "defs":
            for child in node.iter():
                skipped.add(id(child))
    return skipped


def _parse_markers(root: ET.Element) -> Dict[str, MarkerDef]:
    markers: Dict[str, MarkerDef] = {}
    for node in root.iter():
        if _local_name(node.tag) != "marker":
            continue
        marker_id = node.get("id")
        if not marker_id:
            continue
        path_node = None
        for child in node:
            if _local_name(child.tag) == "path":
                path_node = child
                break
        if path_node is None:
            continue
        markers[marker_id] = MarkerDef(
            id=marker_id,
            path_d=path_node.get("d", ""),
            ref_x=parse_length(node.get("refX"), 0.0),
            ref_y=parse_length(node.get("refY"), 0.0),
            width=parse_length(node.get("markerWidth"), 8.0),
            height=parse_length(node.get("markerHeight"), 8.0),
            fill=path_node.get("fill"),
            stroke=path_node.get("stroke"),
        )
    return markers


def _path_points(path_d: str, samples: int = 24) -> tuple[List[tuple[float, float]], bool]:
    if not path_d or not path_d.strip():
        return [], False
    try:
        parsed = parse_path(path_d)
    except Exception:
        return [], False
    if not parsed:
        return [], False
    try:
        length = parsed.length()
    except Exception:
        return [], False
    if length <= 0:
        return [], str(path_d).strip().upper().endswith("Z")
    count = max(int(length / 2) + 2, samples)
    points: List[tuple[float, float]] = []
    for i in range(count + 1):
        pos = min((i / count) * length, max(length - 1e-9, 0))
        try:
            point = parsed.point(pos)
        except (IndexError, ValueError):
            break
        points.append((point.real, point.imag))
    closed = str(path_d).strip().upper().endswith("Z")
    if closed and points and points[0] != points[-1]:
        points.append(points[0])
    return points, closed


def _rounded_rect_d(x: float, y: float, w: float, h: float, rx: float, ry: float) -> str:
    ry = ry or rx
    rx = min(rx, w / 2.0)
    ry = min(ry, h / 2.0)
    if rx <= 0:
        return f"M{x},{y} H{x + w} V{y + h} H{x} Z"
    return (
        f"M{x + rx},{y} H{x + w - rx} Q{x + w},{y} {x + w},{y + ry} "
        f"V{y + h - ry} Q{x + w},{y + h} {x + w - rx},{y + h} "
        f"H{x + rx} Q{x},{y + h} {x},{y + h - ry} "
        f"V{y + ry} Q{x},{y} {x + rx},{y} Z"
    )


def _parse_element(node: ET.Element, inherited: Style) -> Optional[SvgElement]:
    tag = _local_name(node.tag)
    style = _parse_style(node, inherited)

    if tag == "defs":
        return None

    if tag == "rect":
        x = parse_length(node.get("x"))
        y = parse_length(node.get("y"))
        w = parse_length(node.get("width"))
        h = parse_length(node.get("height"))
        rx = parse_length(node.get("rx"))
        ry = parse_length(node.get("ry"), rx)
        if rx > 0 or ry > 0:
            points = rounded_rect_points(x, y, w, h, rx, ry)
            return SvgElement(kind="polyline", style=style, points=points, closed=True)
        return SvgElement(kind="rect", style=style, x=x, y=y, width=w, height=h)

    if tag == "circle":
        return SvgElement(
            kind="circle",
            style=style,
            cx=parse_length(node.get("cx")),
            cy=parse_length(node.get("cy")),
            r=parse_length(node.get("r")),
        )

    if tag == "ellipse":
        return SvgElement(
            kind="ellipse",
            style=style,
            cx=parse_length(node.get("cx")),
            cy=parse_length(node.get("cy")),
            rx=parse_length(node.get("rx")),
            ry=parse_length(node.get("ry")),
        )

    if tag == "line":
        marker_end = node.get("marker-end")
        marker_start = node.get("marker-start")
        if marker_end:
            marker_end = re.sub(r"^url\(#(.+)\)$", r"\1", marker_end)
        if marker_start:
            marker_start = re.sub(r"^url\(#(.+)\)$", r"\1", marker_start)
        return SvgElement(
            kind="line",
            style=style,
            x1=parse_length(node.get("x1")),
            y1=parse_length(node.get("y1")),
            x2=parse_length(node.get("x2")),
            y2=parse_length(node.get("y2")),
            marker_end=marker_end,
            marker_start=marker_start,
        )

    if tag in {"polygon", "polyline"}:
        points = polygon_points(node.get("points", ""))
        return SvgElement(kind="polyline", style=style, points=points, closed=tag == "polygon")

    if tag == "path":
        path_d = node.get("d", "")
        points, closed = _path_points(path_d)
        return SvgElement(kind="polyline", style=style, points=points, path_d=path_d, closed=closed)

    if tag == "text":
        return SvgElement(
            kind="text",
            style=style,
            x=parse_length(node.get("x")),
            y=parse_length(node.get("y")),
            text="".join(node.itertext()).strip(),
        )

    return None


def parse_svg_file(path: Path) -> ParsedSvg:
    tree = ET.parse(path)
    root = tree.getroot()

    viewbox_raw = root.get("viewBox")
    if viewbox_raw:
        parts = [float(v) for v in viewbox_raw.split()]
        viewbox = (parts[0], parts[1], parts[2], parts[3])
    else:
        width = parse_length(root.get("width"), 80.0)
        height = parse_length(root.get("height"), 80.0)
        viewbox = (0.0, 0.0, width, height)

    default_style = Style(
        fill=root.get("fill"),
        stroke=root.get("stroke"),
        stroke_width=parse_length(root.get("stroke-width"), 1.5),
        stroke_dasharray=root.get("stroke-dasharray"),
        font_family=root.get("font-family"),
        font_size=parse_length(root.get("font-size"), 12.0),
        text_anchor=root.get("text-anchor"),
    )

    markers = _parse_markers(root)
    skipped_nodes = _collect_defs_nodes(root)
    elements: List[SvgElement] = []
    for node in root.iter():
        if node is root or id(node) in skipped_nodes:
            continue
        element = _parse_element(node, default_style)
        if element is not None:
            elements.append(element)

    return ParsedSvg(
        path=path,
        viewbox=viewbox,
        default_style=default_style,
        elements=elements,
        markers=markers,
    )
