"""Render layout dicts from layouts.py to PNG using Pillow (no Graphviz required)."""
from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    raise ImportError("Pillow is required: pip install pillow") from exc

PAGE_WIDTH_IN = 26.0
PAGE_HEIGHT_IN = 14.0
DEFAULT_DPI = 120


def _hex_to_rgb(color: str, default: Tuple[int, int, int] = (0, 0, 0)) -> Tuple[int, int, int]:
    if not isinstance(color, str) or not color.startswith("#"):
        return default
    color = color.lstrip("#")
    if len(color) == 8:
        color = color[:6]
    if len(color) != 6:
        return default
    try:
        return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return default


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap_text(text: str, max_chars: int = 28) -> List[str]:
    lines: List[str] = []
    for paragraph in (text or "").split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=max_chars) or [""])
    return lines[:6]


def render_layout_to_png(
    layout: Dict[str, Any],
    output_path: str,
    dpi: int = DEFAULT_DPI,
) -> str:
    width_px = int(PAGE_WIDTH_IN * dpi)
    height_px = int(PAGE_HEIGHT_IN * dpi)
    scale = dpi

    img = Image.new("RGB", (width_px, height_px), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    title = layout.get("title", "")
    if title:
        font_title = _load_font(18, bold=True)
        draw.text((20, 12), title, fill="#1a237e", font=font_title)

    shape_ids: Dict[str, Tuple[int, int, int, int]] = {}

    for node in layout.get("nodes", []):
        x_in, y_in = node.get("x", 0), node.get("y", 0)
        w_in, h_in = node.get("w", 2), node.get("h", 1)
        x0 = int((x_in - w_in / 2) * scale)
        y0 = int((y_in - h_in / 2) * scale)
        x1 = int((x_in + w_in / 2) * scale)
        y1 = int((y_in + h_in / 2) * scale)

        fill = _hex_to_rgb(node.get("fill", "#FFFFFF"), (255, 255, 255))
        border = _hex_to_rgb(node.get("border", "#AAAAAA"), (170, 170, 170))
        text_color = _hex_to_rgb(node.get("text_color", "#000000"))

        draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=fill, outline=border, width=2)
        shape_ids[node["id"]] = (x0, y0, x1, y1)

        label = str(node.get("text", ""))
        if label.strip():
            font = _load_font(11)
            lines = _wrap_text(label, max_chars=max(12, int(w_in * 4)))
            ty = y0 + 6
            for line in lines:
                draw.text((x0 + 6, ty), line, fill=text_color, font=font)
                ty += 14

    for edge in layout.get("edges", []):
        src = shape_ids.get(edge.get("from"))
        dst = shape_ids.get(edge.get("to"))
        if not src or not dst:
            continue
        sx = (src[0] + src[2]) // 2
        sy = (src[1] + src[3]) // 2
        dx = (dst[0] + dst[2]) // 2
        dy = (dst[1] + dst[3]) // 2
        color = _hex_to_rgb(edge.get("color", "#666666"))
        draw.line([(sx, sy), (dx, dy)], fill=color, width=2)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, format="PNG")
    return output_path
