#!/usr/bin/env python3
"""
Generate and download SVG stencil shapes.

- Generates consistent primitives for delivery=generate
- Downloads delivery=download shapes when download_url is set
- Builds consolidated shapes/sprite.svg
- Writes shapes/manifest.json with status per shape

Usage:
  python scripts/generate_shapes.py
  python scripts/generate_shapes.py --only basic-geometric
  python scripts/generate_shapes.py --download-only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shape_catalog import CATEGORIES, STYLE, Shape  # noqa: E402

SHAPES_DIR = ROOT / "shapes"
SPRITE_PATH = SHAPES_DIR / "sprite.svg"
MANIFEST_PATH = SHAPES_DIR / "manifest.json"

# PrimeReact Lara tokens — single source: shape_catalog.STYLE / STYLE_GUIDE.md
STROKE = STYLE["stroke"]
SW = STYLE["stroke_width"]
SW_CONN = STYLE["stroke_width_connector"]
FILL = STYLE["fill"]
MARKER_FILL = STYLE["marker_fill"]
TEXT = STYLE["surface_700"]
TEXT_MUTED = STYLE["text_muted"]
FONT = STYLE["font_family"]
RADIUS = STYLE["border_radius"]
RADIUS_SM = STYLE["border_radius_sm"]
FS_LABEL = STYLE["font_size_label"]
FS_STEREOTYPE = STYLE["font_size_stereotype"]
FS_CAPTION = STYLE["font_size_caption"]


def _svg_open(viewbox: str, extra: str = "", *, stroke_width: Optional[float] = None) -> str:
    sw = stroke_width if stroke_width is not None else SW
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" '
        f'fill="none" stroke="{STROKE}" stroke-width="{sw}" '
        f'stroke-linecap="round" stroke-linejoin="round"{extra}>\n'
    )


def _svg_open_connector(viewbox: str = "0 0 120 24") -> str:
    return _svg_open(viewbox, stroke_width=SW_CONN)


def _svg_close() -> str:
    return "</svg>\n"


def _rect(x: float, y: float, w: float, h: float, rx: float = 0, fill: str = FILL) -> str:
    return f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>\n'


def _circle(cx: float, cy: float, r: float, fill: str = FILL) -> str:
    return f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>\n'


def _ellipse(cx: float, cy: float, rx: float, ry: float, fill: str = FILL) -> str:
    return f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"/>\n'


def _line(x1: float, y1: float, x2: float, y2: float, dash: Optional[str] = None) -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{d}/>\n'


def _polygon(points: str, fill: str = FILL) -> str:
    return f'  <polygon points="{points}" fill="{fill}"/>\n'


def _text(
    x: float,
    y: float,
    content: str,
    size: Optional[float] = None,
    anchor: str = "middle",
    italic: bool = False,
    muted: bool = False,
) -> str:
    style = "font-style:italic;" if italic else ""
    color = TEXT_MUTED if muted else TEXT
    fs = size if size is not None else FS_LABEL
    esc = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'  <text x="{x}" y="{y}" font-family="{FONT}" font-size="{fs}" '
        f'text-anchor="{anchor}" fill="{color}" stroke="none" style="{style}">{esc}</text>\n'
    )


def _labeled_box(
    stereotype: Optional[str],
    title: str,
    *,
    italic_title: bool = False,
    compartments: int = 1,
) -> str:
    parts = [_svg_open("0 0 120 80")]
    parts.append(_rect(8, 8, 104, 64, rx=0))
    y = 28
    if stereotype:
        parts.append(_text(60, 22, f"<<{stereotype}>>", size=FS_STEREOTYPE, muted=True))
        y = 36
    parts.append(_text(60, y, title, size=FS_LABEL, italic=italic_title))
    if compartments >= 2:
        parts.append(_line(8, 40, 112, 40))
        parts.append(_text(60, 54, "attributes", size=FS_STEREOTYPE, muted=True))
    if compartments >= 3:
        parts.append(_line(8, 58, 112, 58))
        parts.append(_text(60, 72, "methods", size=FS_STEREOTYPE, muted=True))
    parts.append(_svg_close())
    return "".join(parts)


# --- generators keyed by generator id ---
Generators = Dict[str, Callable[[], str]]


def _gen_rectangle() -> str:
    return _svg_open("0 0 80 80") + _rect(10, 16, 60, 48) + _svg_close()


def _gen_rounded_rectangle() -> str:
    return _svg_open("0 0 80 80") + _rect(10, 16, 60, 48, rx=RADIUS) + _svg_close()


def _gen_square() -> str:
    return _svg_open("0 0 80 80") + _rect(16, 16, 48, 48) + _svg_close()


def _gen_circle() -> str:
    return _svg_open("0 0 80 80") + _circle(40, 40, 24) + _svg_close()


def _gen_ellipse() -> str:
    return _svg_open("0 0 80 80") + _ellipse(40, 40, 32, 20) + _svg_close()


def _gen_diamond() -> str:
    return _svg_open("0 0 80 80") + _polygon("40,12 68,40 40,68 12,40") + _svg_close()


def _gen_triangle() -> str:
    return _svg_open("0 0 80 80") + _polygon("40,14 66,66 14,66") + _svg_close()


def _gen_hexagon() -> str:
    return _svg_open("0 0 80 80") + _polygon("40,10 64,24 64,56 40,70 16,56 16,24") + _svg_close()


def _gen_pentagon() -> str:
    return _svg_open("0 0 80 80") + _polygon("40,10 68,32 58,68 22,68 12,32") + _svg_close()


def _gen_cylinder() -> str:
    parts = [_svg_open("0 0 80 80")]
    parts.append(_ellipse(40, 22, 28, 8, fill=FILL))
    parts.append(_line(12, 22, 12, 58))
    parts.append(_line(68, 22, 68, 58))
    parts.append(_ellipse(40, 58, 28, 8, fill=FILL))
    parts.append(_ellipse(40, 22, 28, 8, fill="none"))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_folder() -> str:
    parts = [_svg_open("0 0 80 80")]
    parts.append(_polygon("12,28 32,28 38,20 68,20 68,68 12,68", fill=FILL))
    parts.append(_line(12, 28, 32, 28))
    parts.append(_line(32, 28, 38, 20))
    parts.append(_line(38, 20, 68, 20))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_line_solid() -> str:
    return _svg_open_connector() + _line(4, 12, 116, 12) + _svg_close()


def _gen_line_dashed() -> str:
    return _svg_open_connector() + _line(4, 12, 116, 12, dash="6 4") + _svg_close()


def _gen_line_dotted() -> str:
    return _svg_open_connector() + _line(4, 12, 116, 12, dash="2 3") + _svg_close()


def _gen_arrow_solid() -> str:
    parts = [_svg_open_connector()]
    parts.append(
        '  <defs><marker id="af" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 Z" fill="{MARKER_FILL}"/></marker></defs>\n'
    )
    parts.append('  <line x1="4" y1="12" x2="110" y2="12" marker-end="url(#af)"/>\n')
    parts.append(_svg_close())
    return "".join(parts)


def _gen_arrow_open() -> str:
    parts = [_svg_open_connector()]
    parts.append(
        '  <defs><marker id="ao" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10" fill="none" stroke="{STROKE}" stroke-width="{SW_CONN}"/></marker></defs>\n'
    )
    parts.append('  <line x1="4" y1="12" x2="108" y2="12" marker-end="url(#ao)"/>\n')
    parts.append(_svg_close())
    return "".join(parts)


def _gen_arrow_dashed() -> str:
    parts = [_svg_open_connector()]
    parts.append(
        '  <defs><marker id="ad" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 Z" fill="{MARKER_FILL}"/></marker></defs>\n'
    )
    parts.append('  <line x1="4" y1="12" x2="110" y2="12" stroke-dasharray="6 4" marker-end="url(#ad)"/>\n')
    parts.append(_svg_close())
    return "".join(parts)


def _gen_arrow_double() -> str:
    parts = [_svg_open_connector()]
    parts.append(
        '  <defs>'
        f'<marker id="al" markerWidth="8" markerHeight="8" refX="1" refY="4" orient="auto">'
        f'<path d="M8,0 L0,4 L8,8 Z" fill="{MARKER_FILL}"/></marker>'
        f'<marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 Z" fill="{MARKER_FILL}"/></marker></defs>\n'
    )
    parts.append('  <line x1="10" y1="12" x2="110" y2="12" marker-start="url(#al)" marker-end="url(#ar)"/>\n')
    parts.append(_svg_close())
    return "".join(parts)


def _gen_inheritance() -> str:
    parts = [_svg_open_connector()]
    parts.append(
        '  <defs><marker id="inh" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">'
        f'<path d="M0,0 L12,6 L0,12 Z" fill="{FILL}" stroke="{STROKE}" stroke-width="{SW_CONN}"/></marker></defs>\n'
    )
    parts.append('  <line x1="4" y1="12" x2="106" y2="12" marker-end="url(#inh)"/>\n')
    parts.append(_svg_close())
    return "".join(parts)


def _gen_realization() -> str:
    parts = [_svg_open_connector()]
    parts.append(
        '  <defs><marker id="real" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">'
        f'<path d="M0,0 L12,6 L0,12 Z" fill="{FILL}" stroke="{STROKE}" stroke-width="{SW_CONN}"/></marker></defs>\n'
    )
    parts.append('  <line x1="4" y1="12" x2="106" y2="12" stroke-dasharray="6 4" marker-end="url(#real)"/>\n')
    parts.append(_svg_close())
    return "".join(parts)


def _gen_aggregation() -> str:
    parts = [_svg_open_connector()]
    parts.append(_polygon("4,12 14,6 24,12 14,18", fill=FILL))
    parts.append(_line(24, 12, 116, 12))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_composition() -> str:
    parts = [_svg_open_connector()]
    parts.append(_polygon("4,12 14,6 24,12 14,18", fill=MARKER_FILL))
    parts.append(_line(24, 12, 116, 12))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_dependency() -> str:
    return _gen_arrow_dashed()


def _gen_class_box() -> str:
    return _labeled_box(None, "ClassName", compartments=3)


def _gen_abstract_class() -> str:
    return _labeled_box(None, "AbstractClass", italic_title=True, compartments=3)


def _gen_interface_box() -> str:
    return _labeled_box("interface", "InterfaceName", compartments=2)


def _gen_enumeration() -> str:
    return _labeled_box("enumeration", "EnumName", compartments=2)


def _gen_actor() -> str:
    parts = [_svg_open("0 0 80 80")]
    parts.append(_circle(40, 16, 10))
    parts.append(_line(40, 26, 40, 50))
    parts.append(_line(40, 34, 24, 44))
    parts.append(_line(40, 34, 56, 44))
    parts.append(_line(40, 50, 28, 68))
    parts.append(_line(40, 50, 52, 68))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_use_case() -> str:
    parts = [_svg_open("0 0 120 60")]
    parts.append(_ellipse(60, 30, 52, 22))
    parts.append(_text(60, 34, "Use Case"))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_system_boundary() -> str:
    parts = [_svg_open("0 0 120 80")]
    parts.append(_rect(8, 8, 104, 64, rx=0, fill="none"))
    parts.append(_text(60, 22, "System Name", size=FS_CAPTION, muted=True))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_lifeline() -> str:
    parts = [_svg_open("0 0 80 120")]
    parts.append(_rect(16, 8, 48, 24, rx=RADIUS_SM))
    parts.append(_text(40, 24, "Object", size=FS_CAPTION))
    parts.append(_line(40, 32, 40, 112, dash="4 4"))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_actor_lifeline() -> str:
    parts = [_svg_open("0 0 80 120")]
    parts.append(_circle(40, 14, 8))
    parts.append(_line(40, 22, 40, 38))
    parts.append(_line(40, 38, 40, 112, dash="4 4"))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_activation_bar() -> str:
    parts = [_svg_open("0 0 40 80")]
    parts.append(_rect(14, 16, 12, 48, fill=FILL))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_self_message() -> str:
    parts = [_svg_open("0 0 80 60")]
    parts.append(
        '  <defs><marker id="sm" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 Z" fill="{MARKER_FILL}"/></marker></defs>\n'
    )
    parts.append('  <polyline points="16,48 16,16 64,16 64,32" fill="none" marker-end="url(#sm)"/>\n')
    parts.append(_svg_close())
    return "".join(parts)


def _gen_combined_fragment(label: str) -> str:
    parts = [_svg_open("0 0 120 80")]
    parts.append(_rect(8, 8, 104, 64, fill="none"))
    parts.append(_rect(8, 8, 104, 18, fill=FILL))
    parts.append(_text(60, 20, label, size=FS_CAPTION))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_initial_node() -> str:
    return _svg_open("0 0 80 80") + _circle(40, 40, 10, fill=MARKER_FILL) + _svg_close()


def _gen_final_node() -> str:
    parts = [_svg_open("0 0 80 80")]
    parts.append(_circle(40, 40, 14, fill="none"))
    parts.append(_circle(40, 40, 10, fill=MARKER_FILL))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_flow_final_node() -> str:
    parts = [_svg_open("0 0 80 80")]
    parts.append(_circle(40, 40, 14, fill="none"))
    parts.append(_line(32, 32, 48, 48))
    parts.append(_line(48, 32, 32, 48))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_fork_bar() -> str:
    parts = [_svg_open("0 0 80 24", stroke_width=SW_CONN)]
    parts.append(f'  <rect x="8" y="10" width="64" height="4" fill="{MARKER_FILL}" stroke="none"/>\n')
    parts.append(_svg_close())
    return "".join(parts)


def _gen_join_bar() -> str:
    return _gen_fork_bar()


def _gen_swimlane() -> str:
    parts = [_svg_open("0 0 120 80")]
    parts.append(_line(40, 8, 40, 72))
    parts.append(_rect(8, 8, 32, 64, fill="none"))
    parts.append(_text(24, 24, "Lane", size=FS_CAPTION))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_component() -> str:
    parts = [_svg_open("0 0 120 60")]
    parts.append(_rect(16, 12, 88, 36, rx=0))
    parts.append(_rect(8, 20, 12, 20, fill=FILL))
    parts.append(_text(60, 34, "Component", size=FS_CAPTION))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_node() -> str:
    parts = [_svg_open("0 0 120 70")]
    parts.append(_polygon("16,20 104,20 104,58 16,58", fill=FILL))
    parts.append(_polygon("16,20 24,12 112,12 104,20", fill=FILL))
    parts.append(_line(16, 20, 24, 12))
    parts.append(_line(104, 20, 112, 12))
    parts.append(_line(24, 12, 112, 12))
    parts.append(_text(60, 42, "Node", size=FS_CAPTION))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_lollipop() -> str:
    parts = [_svg_open("0 0 80 40")]
    parts.append(_line(8, 20, 56, 20))
    parts.append(_circle(64, 20, 8, fill="none"))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_socket() -> str:
    parts = [_svg_open("0 0 80 40")]
    parts.append(_line(24, 20, 72, 20))
    parts.append('  <path d="M8,12 A16,16 0 0 1 8,28" fill="none"/>\n')
    parts.append(_svg_close())
    return "".join(parts)


def _gen_table() -> str:
    parts = [_svg_open("0 0 120 80")]
    parts.append(_rect(8, 8, 104, 64))
    parts.append(_line(8, 24, 112, 24))
    parts.append(_line(8, 40, 112, 40))
    parts.append(_line(48, 24, 48, 72))
    parts.append(_text(28, 19, "Table", size=FS_STEREOTYPE, muted=True))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_stereotype_box(st: str, title: str) -> str:
    return _labeled_box(st, title, compartments=1)


def _gen_internet_cloud() -> str:
    parts = [_svg_open("0 0 120 60")]
    parts.append(
        '  <path d="M30,42 C18,42 14,32 22,26 C20,14 36,10 44,18 C52,8 68,10 72,22 '
        'C84,20 92,30 88,40 C96,44 92,52 82,52 L38,52 C32,52 28,48 30,42 Z" fill="none"/>\n'
    )
    parts.append(_text(60, 38, "Internet", size=FS_CAPTION))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_arch_box(st: str, title: str) -> str:
    return _labeled_box(st, title, compartments=1)


def _gen_zigzag() -> str:
    parts = [_svg_open_connector()]
    parts.append('  <polyline points="4,12 20,4 36,20 52,4 68,20 84,4 100,20 116,12" fill="none"/>\n')
    parts.append(_svg_close())
    return "".join(parts)


def _gen_diamond_filled_marker() -> str:
    return _svg_open("0 0 80 80") + _polygon("40,20 60,40 40,60 20,40", fill=MARKER_FILL) + _svg_close()


def _gen_expansion_region() -> str:
    parts = [_svg_open("0 0 120 80")]
    parts.append('  <rect x="8" y="8" width="104" height="64" fill="none" stroke-dasharray="6 4"/>\n')
    parts.append(_svg_close())
    return "".join(parts)


def _gen_predefined_process() -> str:
    parts = [_svg_open("0 0 80 80")]
    parts.append(_rect(12, 18, 56, 44))
    parts.append(_rect(14, 20, 52, 40, fill="none"))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_destroy_message() -> str:
    parts = [_svg_open_connector("0 0 120 40")]
    parts.append(
        '  <defs><marker id="dm" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 Z" fill="{MARKER_FILL}"/></marker></defs>\n'
    )
    parts.append('  <line x1="4" y1="20" x2="90" y2="20" marker-end="url(#dm)"/>\n')
    parts.append(_line(98, 12, 110, 28))
    parts.append(_line(110, 12, 98, 28))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_create_message() -> str:
    return _gen_arrow_dashed()


def _gen_include() -> str:
    return _gen_arrow_dashed()


def _gen_extend() -> str:
    return _gen_arrow_dashed()


def _gen_interaction_occurrence() -> str:
    parts = [_svg_open("0 0 80 40")]
    parts.append(_rect(8, 8, 64, 24, rx=RADIUS_SM, fill="none"))
    parts.append(_text(40, 24, "ref", size=FS_CAPTION))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_continuation() -> str:
    parts = [_svg_open("0 0 80 32")]
    parts.append(_rect(8, 8, 64, 16, rx=RADIUS_SM, fill=FILL))
    parts.append(_text(40, 20, "cont.", size=FS_STEREOTYPE, muted=True))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_deep_history() -> str:
    parts = [_svg_open("0 0 80 80")]
    parts.append(_circle(40, 40, 16, fill=FILL))
    parts.append(_text(40, 44, "H*", size=FS_CAPTION))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_shallow_history() -> str:
    parts = [_svg_open("0 0 80 80")]
    parts.append(_circle(40, 40, 16, fill=FILL))
    parts.append(_text(40, 44, "H", size=FS_CAPTION))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_composite_state() -> str:
    parts = [_svg_open("0 0 120 80")]
    parts.append(_rect(8, 8, 104, 64, rx=RADIUS))
    parts.append(_rect(20, 28, 80, 36, rx=RADIUS_SM, fill="none"))
    parts.append(_text(60, 22, "Composite", size=FS_CAPTION))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_submachine_state() -> str:
    parts = [_svg_open("0 0 120 60")]
    parts.append(_rect(8, 8, 104, 44, rx=RADIUS))
    parts.append(_text(60, 28, "State", size=FS_LABEL))
    parts.append(_text(60, 44, "ref", size=FS_STEREOTYPE, muted=True))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_port() -> str:
    return _svg_open("0 0 80 80") + _rect(34, 34, 12, 12) + _svg_close()


def _gen_component_lollipop() -> str:
    parts = [_svg_open("0 0 120 60")]
    parts.append(_rect(8, 12, 72, 36))
    parts.append(_line(80, 30, 100, 30))
    parts.append(_circle(108, 30, 8, fill="none"))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_component_socket() -> str:
    parts = [_svg_open("0 0 120 60")]
    parts.append(_rect(40, 12, 72, 36))
    parts.append(_line(32, 30, 40, 30))
    parts.append('  <path d="M12,18 A20,20 0 0 1 12,42" fill="none"/>\n')
    parts.append(_svg_close())
    return "".join(parts)


def _gen_data_store() -> str:
    parts = [_svg_open("0 0 120 60")]
    parts.append(_rect(16, 12, 88, 36))
    parts.append(_line(8, 12, 8, 48))
    parts.append(_line(8, 48, 104, 48))
    parts.append(_text(60, 34, "Data Store", size=FS_STEREOTYPE, muted=True))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_activity() -> str:
    return _labeled_box("activity", "Activity", compartments=1)


def _gen_legend() -> str:
    parts = [_svg_open("0 0 120 80")]
    parts.append(_rect(8, 8, 104, 64, rx=RADIUS_SM))
    parts.append(_text(60, 22, "Legend", size=FS_CAPTION))
    parts.append(_circle(24, 40, 6, fill=MARKER_FILL))
    parts.append(_text(40, 44, "symbol", size=FS_STEREOTYPE, anchor="start", muted=True))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_title_block() -> str:
    parts = [_svg_open("0 0 120 80")]
    parts.append(_rect(8, 8, 104, 64))
    parts.append(_text(60, 28, "Project", size=FS_CAPTION))
    parts.append(_text(60, 44, "Version 1.0", size=FS_STEREOTYPE, muted=True))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_phase() -> str:
    parts = [_svg_open("0 0 120 50")]
    parts.append(_rect(8, 8, 104, 34, rx=RADIUS_SM))
    parts.append(_text(60, 30, "Phase 1", size=FS_CAPTION))
    parts.append(_svg_close())
    return "".join(parts)


def _gen_tag() -> str:
    return _labeled_box("tag", "Tag", compartments=1)


def _gen_cloud_region() -> str:
    return _labeled_box(None, "us-east-1", compartments=1)


def _gen_cloud_az() -> str:
    return _labeled_box(None, "AZ-A", compartments=1)


def _gen_cloud_generic() -> str:
    return _gen_internet_cloud()


GENERATORS: Dict[str, Callable[[], str]] = {
    "rectangle": _gen_rectangle,
    "rounded-rectangle": _gen_rounded_rectangle,
    "square": _gen_square,
    "circle": _gen_circle,
    "ellipse": _gen_ellipse,
    "diamond": _gen_diamond,
    "triangle": _gen_triangle,
    "hexagon": _gen_hexagon,
    "pentagon": _gen_pentagon,
    "cylinder": _gen_cylinder,
    "folder": _gen_folder,
    "line-solid": _gen_line_solid,
    "line-dashed": _gen_line_dashed,
    "line-dotted": _gen_line_dotted,
    "arrow-solid": _gen_arrow_solid,
    "arrow-open": _gen_arrow_open,
    "arrow-dashed": _gen_arrow_dashed,
    "arrow-double": _gen_arrow_double,
    "inheritance": _gen_inheritance,
    "realization": _gen_realization,
    "aggregation": _gen_aggregation,
    "composition": _gen_composition,
    "dependency": _gen_dependency,
    "class-box": _gen_class_box,
    "abstract-class": _gen_abstract_class,
    "interface-box": _gen_interface_box,
    "enumeration": _gen_enumeration,
    "actor": _gen_actor,
    "use-case": _gen_use_case,
    "system-boundary": _gen_system_boundary,
    "lifeline": _gen_lifeline,
    "actor-lifeline": _gen_actor_lifeline,
    "activation-bar": _gen_activation_bar,
    "self-message": _gen_self_message,
    "combined-fragment": lambda: _gen_combined_fragment("fragment"),
    "alt-fragment": lambda: _gen_combined_fragment("alt"),
    "loop-fragment": lambda: _gen_combined_fragment("loop"),
    "opt-fragment": lambda: _gen_combined_fragment("opt"),
    "par-fragment": lambda: _gen_combined_fragment("par"),
    "initial-node": _gen_initial_node,
    "final-node": _gen_final_node,
    "flow-final-node": _gen_flow_final_node,
    "fork-bar": _gen_fork_bar,
    "join-bar": _gen_join_bar,
    "swimlane": _gen_swimlane,
    "component": _gen_component,
    "node": _gen_node,
    "lollipop": _gen_lollipop,
    "socket": _gen_socket,
    "table": _gen_table,
    "internet-cloud": _gen_internet_cloud,
    "zigzag": _gen_zigzag,
    "diamond-filled-marker": _gen_diamond_filled_marker,
    "expansion-region": _gen_expansion_region,
    "predefined-process": _gen_predefined_process,
    "destroy-message": _gen_destroy_message,
    "create-message": _gen_create_message,
    "include": _gen_include,
    "extend": _gen_extend,
    "interaction-occurrence": _gen_interaction_occurrence,
    "continuation": _gen_continuation,
    "deep-history": _gen_deep_history,
    "shallow-history": _gen_shallow_history,
    "composite-state": _gen_composite_state,
    "submachine-state": _gen_submachine_state,
    "port": _gen_port,
    "component-lollipop": _gen_component_lollipop,
    "component-socket": _gen_component_socket,
    "data-store": _gen_data_store,
    "activity": _gen_activity,
    "legend": _gen_legend,
    "title-block": _gen_title_block,
    "phase": _gen_phase,
    "tag": _gen_tag,
    "cloud-region": _gen_cloud_region,
    "cloud-az": _gen_cloud_az,
    "cloud-generic": _gen_cloud_generic,
    "association": _gen_line_solid,
    "device": lambda: _gen_stereotype_box("device", "Server"),
    "execution-environment": lambda: _gen_stereotype_box("EE", "JVM"),
    "artifact": lambda: _gen_stereotype_box("artifact", "Artifact"),
    "package-stereotype": lambda: _gen_stereotype_box("stereotype", "Package"),
    "model": lambda: _gen_stereotype_box("model", "Model"),
    "subsystem": lambda: _gen_stereotype_box("subsystem", "Subsystem"),
    "profile": lambda: _gen_stereotype_box("profile", "Profile"),
    "microservice": lambda: _gen_stereotype_box("ms", "Service"),
    "api-gateway": lambda: _gen_stereotype_box("gateway", "API"),
    "cache": lambda: _gen_arch_box("cache", "Cache"),
    "message-queue": lambda: _gen_stereotype_box("queue", "Queue"),
    "load-balancer": lambda: _gen_stereotype_box("lb", "LB"),
    "firewall": lambda: _gen_stereotype_box("fw", "FW"),
    "storage": lambda: _gen_stereotype_box("storage", "Storage"),
    "container-box": lambda: _gen_stereotype_box("container", "App"),
    "pod": lambda: _gen_stereotype_box("pod", "Pod"),
    "k8s-service": lambda: _gen_stereotype_box("service", "Service"),
    "ingress": lambda: _gen_stereotype_box("ingress", "Ingress"),
    "configmap": lambda: _gen_stereotype_box("config", "Config"),
    "secret": lambda: _gen_stereotype_box("secret", "Secret"),
    "persistent-volume": lambda: _gen_stereotype_box("pv", "Volume"),
    "namespace": lambda: _gen_stereotype_box("ns", "Namespace"),
    "consumer": lambda: _gen_stereotype_box("consumer", "Consumer"),
    "producer": lambda: _gen_stereotype_box("producer", "Producer"),
    "broker": lambda: _gen_stereotype_box("broker", "Broker"),
    "topic": lambda: _gen_stereotype_box("topic", "Topic"),
    "view-db": lambda: _gen_stereotype_box("view", "View"),
    "stored-procedure": lambda: _gen_stereotype_box("sp", "SP"),
    "index-db": lambda: _gen_stereotype_box("index", "Index"),
    "server": _gen_node,
    "switch": lambda: _gen_stereotype_box("switch", "Switch"),
    "router": lambda: _gen_stereotype_box("router", "Router"),
    "vpn": lambda: _gen_stereotype_box("vpn", "VPN"),
    "dmz": lambda: _gen_stereotype_box("dmz", "DMZ"),
    "subnet": lambda: _gen_stereotype_box("subnet", "10.0.0.0/24"),
    "display": lambda: _gen_stereotype_box("display", "Display"),
    "aws-ec2": lambda: _gen_arch_box("AWS", "EC2"),
    "aws-s3": lambda: _gen_arch_box("AWS", "S3"),
    "aws-rds": lambda: _gen_arch_box("AWS", "RDS"),
    "aws-lambda": lambda: _gen_arch_box("AWS", "Lambda"),
    "aws-api-gateway": lambda: _gen_arch_box("AWS", "API GW"),
    "aws-vpc": lambda: _gen_arch_box("AWS", "VPC"),
}


def _extract_viewbox(svg: str) -> str:
    m = re.search(r'viewBox="([^"]+)"', svg)
    return m.group(1) if m else "0 0 80 80"


def _inner_svg(svg: str) -> str:
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
    m = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else svg


def download_svg(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "UML-SKILLS-stencil-fetcher/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def process_shape(shape: Shape, category_id: str, download_only: bool) -> Tuple[str, Optional[str]]:
    out_dir = SHAPES_DIR / category_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{shape.id}.svg"

    if shape.delivery == "annotation":
        return "skipped", None

    if shape.delivery == "manual":
        return "manual", None

    if shape.delivery == "download":
        if not shape.download_url:
            return "manual", None
        if download_only or shape.delivery == "download":
            try:
                content = download_svg(shape.download_url)
                if "<svg" not in content.lower():
                    return "download-failed", None
                out_path.write_text(content, encoding="utf-8")
                return "downloaded", str(out_path.relative_to(ROOT))
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                print(f"  download failed {shape.id}: {e}")
                return "download-failed", None
        return "manual", None

    if shape.delivery == "generate":
        gen_key = shape.generator or shape.id
        fn = GENERATORS.get(gen_key)
        if not fn:
            return "no-generator", None
        svg = fn()
        out_path.write_text(svg, encoding="utf-8")
        return "generated", str(out_path.relative_to(ROOT))

    return "unknown", None


def build_sprite(entries: List[dict]) -> None:
    symbols: List[str] = []
    for e in entries:
        if not e.get("path"):
            continue
        path = ROOT / e["path"]
        if not path.exists():
            continue
        svg = path.read_text(encoding="utf-8")
        vb = _extract_viewbox(svg)
        inner = _inner_svg(svg)
        symbols.append(f'  <symbol id="{e["id"]}" viewBox="{vb}">\n{inner}\n  </symbol>\n')

    sprite = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n'
        + "".join(symbols)
        + "</svg>\n"
    )
    SPRITE_PATH.write_text(sprite, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate/download UML stencil SVGs")
    parser.add_argument("--only", help="Limit to category id prefix")
    parser.add_argument("--download-only", action="store_true")
    args = parser.parse_args()

    manifest: List[dict] = []
    counts: Dict[str, int] = {}

    for cat in CATEGORIES:
        if args.only and cat.id != args.only:
            continue
        print(f"Category: {cat.id}")
        for shape in cat.shapes:
            status, path = process_shape(shape, cat.id, args.download_only)
            counts[status] = counts.get(status, 0) + 1
            manifest.append({
                "id": shape.id,
                "name": shape.name,
                "category": cat.id,
                "delivery": shape.delivery,
                "status": status,
                "path": path,
            })
            if path:
                print(f"  {status}: {path}")

    build_sprite(manifest)
    MANIFEST_PATH.write_text(json.dumps({"shapes": manifest, "counts": counts}, indent=2), encoding="utf-8")

    print("\nSummary:")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    print(f"Sprite: {SPRITE_PATH}")
    print(f"Manifest: {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
