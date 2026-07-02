"""Render layout dicts to PNG for reliable Word document embedding."""
from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

# Layout functions use a ~24×14 inch reference canvas.
REF_W = 26.0
REF_H = 15.0
DEFAULT_DPI = 120


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    c = (hex_color or "#FFFFFF").lstrip("#")
    if len(c) == 6:
        return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return 255, 255, 255


def _wrap_text(text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
    lines: List[str] = []
    for paragraph in str(text or "").split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        wrapped = textwrap.wrap(paragraph, width=40)
        lines.extend(wrapped or [""])
    # Trim to fit height — crude width check
    out: List[str] = []
    for line in lines:
        if font.getlength(line) <= max_width:
            out.append(line)
        else:
            out.extend(textwrap.wrap(line, width=max(10, len(line) // 2)) or [line[:40]])
    return out[:8]


def layout_to_png(layout: dict, output_path: Path, dpi: int = DEFAULT_DPI) -> str:
    """Render a {nodes, edges, title} layout dict to a PNG file."""
    scale = dpi
    img_w = int(REF_W * scale)
    img_h = int(REF_H * scale)
    img = Image.new("RGB", (img_w, img_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    title_font = _load_font(max(14, dpi // 8), bold=True)
    body_font = _load_font(max(10, dpi // 12))
    small_font = _load_font(max(9, dpi // 14))

    title = layout.get("title", "")
    if title:
        draw.text((int(0.4 * scale), int(0.25 * scale)), title, fill=(26, 35, 126), font=title_font)

    centers: Dict[str, Tuple[float, float]] = {}
    bounds: Dict[str, Tuple[float, float, float, float]] = {}

    for node in layout.get("nodes", []):
        cx = node.get("x", 0) * scale
        cy = node.get("y", 0) * scale
        w = max(node.get("w", 1) * scale, 8)
        h = max(node.get("h", 0.5) * scale, 8)
        x0, y0 = cx - w / 2, cy - h / 2
        fill = _hex_to_rgb(node.get("fill", "#FFFFFF"))
        border = _hex_to_rgb(node.get("border", "#AAAAAA"))
        text_color = _hex_to_rgb(node.get("text_color", "#000000"))

        draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=6, fill=fill, outline=border, width=2)
        centers[node["id"]] = (cx, cy)
        bounds[node["id"]] = (x0, y0, x0 + w, y0 + h)

        label = str(node.get("text", ""))
        if label.strip():
            font = body_font if h > 30 else small_font
            lines = _wrap_text(label, font, int(w - 12))
            line_h = max(11, dpi // 11)
            total_h = len(lines) * line_h
            ty = cy - total_h / 2
            for i, line in enumerate(lines):
                draw.text((x0 + 6, ty + i * line_h), line, fill=text_color, font=font)

    for edge in layout.get("edges", []):
        src = bounds.get(edge.get("from", ""))
        dst = bounds.get(edge.get("to", ""))
        if not src or not dst:
            continue
        x1, y1 = src[2], (src[1] + src[3]) / 2
        x2, y2 = dst[0], (dst[1] + dst[3]) / 2
        color = _hex_to_rgb(edge.get("color", "#666666"))
        mid_x = (x1 + x2) / 2
        draw.line([(x1, y1), (mid_x, y1), (mid_x, y2), (x2, y2)], fill=color, width=2)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), format="PNG", optimize=True)
    return str(output_path)
