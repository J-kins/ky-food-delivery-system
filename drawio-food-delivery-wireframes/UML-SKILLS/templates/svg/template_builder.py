"""SVG layout builders for blank diagram templates (PrimeReact Lara aesthetic)."""
from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Tuple

from template_catalog import STYLE, Template

W, H = 1920, 1080
M = 40
CONTENT_TOP = 118
CONTENT_BOTTOM = 1000
FOOTER_Y = 1048

S = STYLE
FONT = S["font_family"]


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SvgBuilder:
    def __init__(self, template: Template) -> None:
        self.template = template
        self.parts: List[str] = []

    def build(self) -> str:
        from template_layouts import render_layout  # local import avoids cycle

        self._open()
        self._chrome()
        render_layout(self, self.template)
        self._legend()
        self._footer()
        self.parts.append("</svg>\n")
        return "".join(self.parts)

    def _open(self) -> None:
        self.parts.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}" fill="none">\n'
        )
        self.parts.append(f'  <rect width="{W}" height="{H}" fill="{S["surface_0"]}"/>\n')

    def _chrome(self) -> None:
        t = self.template
        self.parts.append(
            f'  <rect x="{M}" y="{M}" width="{W - 2 * M}" height="{H - 2 * M}" '
            f'rx="8" fill="{S["surface_0"]}" stroke="{S["surface_200"]}" stroke-width="2"/>\n'
        )
        # Title bar — PrimeReact primary header
        tb_w, tb_h = 760, 56
        tb_x = (W - tb_w) // 2
        self.parts.append(
            f'  <rect x="{tb_x}" y="52" width="{tb_w}" height="{tb_h}" '
            f'rx="{S["border_radius"]}" fill="{S["primary"]}"/>\n'
        )
        self.parts.append(
            f'  <text x="{W // 2}" y="88" text-anchor="middle" fill="{S["surface_0"]}" '
            f'font-family="{FONT}" font-size="22" font-weight="600">{_esc(t.title)}</text>\n'
        )
        self.parts.append(
            f'  <text x="{W // 2}" y="108" text-anchor="middle" fill="{S["primary_tint"]}" '
            f'font-family="{FONT}" font-size="12">&lt;Project Name&gt; · Template</text>\n'
        )
        # Grid
        self.parts.append(
            '  <defs>\n'
            f'    <pattern id="grid-{t.id}" width="50" height="50" patternUnits="userSpaceOnUse">\n'
            f'      <path d="M 50 0 L 0 0 0 50" fill="none" stroke="{S["surface_200"]}" stroke-width="0.5"/>\n'
            "    </pattern>\n"
            "  </defs>\n"
        )
        self.parts.append(
            f'  <rect x="{M}" y="{CONTENT_TOP}" width="{W - 2 * M}" '
            f'height="{CONTENT_BOTTOM - CONTENT_TOP}" fill="url(#grid-{t.id})"/>\n'
        )
        self.parts.append(
            f'  <rect x="{M}" y="{CONTENT_TOP}" width="{W - 2 * M}" '
            f'height="{CONTENT_BOTTOM - CONTENT_TOP}" fill="{S["surface_50"]}" fill-opacity="0.35"/>\n'
        )

    def _legend(self) -> None:
        lx, ly, lw, lh = W - M - 300, CONTENT_BOTTOM - 150, 280, 130
        self.placeholder(lx, ly, lw, lh, "Legend", muted=True, rx=S["border_radius"])

    def _footer(self) -> None:
        self.parts.append(
            f'  <text x="{M + 12}" y="{FOOTER_Y}" fill="{S["text_muted"]}" '
            f'font-family="{FONT}" font-size="11">Page 1 of 1 · CONFIDENTIAL — Internal Use Only</text>\n'
        )
        self.parts.append(
            f'  <text x="{W - M - 12}" y="{FOOTER_Y}" text-anchor="end" fill="{S["text_muted"]}" '
            f'font-family="{FONT}" font-size="11">&lt;Project Name&gt; · Version 1.0 · '
            f'{_esc(self.template.title)}</text>\n'
        )

  # --- primitives ---------------------------------------------------------

    def placeholder(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        label: str,
        *,
        muted: bool = False,
        rx: float = 6,
        fill: Optional[str] = None,
    ) -> None:
        stroke = S["placeholder_stroke"] if not muted else S["text_muted"]
        fill_attr = f' fill="{fill}"' if fill else ' fill="none"'
        self.parts.append(
            f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"{fill_attr} '
            f'stroke="{stroke}" stroke-width="1.5" stroke-dasharray="8 5"/>\n'
        )
        self.parts.append(
            f'  <text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle" '
            f'fill="{S["text_muted"]}" font-family="{FONT}" font-size="13">{_esc(label)}</text>\n'
        )

    def solid_box(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        label: str,
        *,
        fill: str = None,
        rx: float = 6,
    ) -> None:
        fill = fill or S["surface_0"]
        self.parts.append(
            f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{S["surface_700"]}" stroke-width="1.5"/>\n'
        )
        self.parts.append(
            f'  <text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle" '
            f'fill="{S["surface_700"]}" font-family="{FONT}" font-size="13">{_esc(label)}</text>\n'
        )

    def guide_line(self, x1: float, y1: float, x2: float, y2: float) -> None:
        self.parts.append(
            f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{S["guide_stroke"]}" '
            f'stroke-width="1.5" stroke-dasharray="4 4"/>\n'
        )

    def connector(self, x1: float, y1: float, x2: float, y2: float, label: str = "") -> None:
        self.parts.append(
            f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{S["surface_700"]}" '
            f'stroke-width="1.25" marker-end="url(#arrow)"/>\n'
        )
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 8
            self.parts.append(
                f'  <text x="{mx}" y="{my}" text-anchor="middle" fill="{S["text_muted"]}" '
                f'font-family="{FONT}" font-size="11">{_esc(label)}</text>\n'
            )

    def label(self, x: float, y: float, text: str, *, size: int = 12, anchor: str = "start", muted: bool = False) -> None:
        color = S["text_muted"] if muted else S["surface_700"]
        self.parts.append(
            f'  <text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" '
            f'font-family="{FONT}" font-size="{size}">{_esc(text)}</text>\n'
        )

    def swimlane(self, x: float, y: float, w: float, h: float, title: str) -> None:
        self.parts.append(
            f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{S["surface_0"]}" '
            f'stroke="{S["surface_200"]}" stroke-width="1.5"/>\n'
        )
        self.parts.append(
            f'  <rect x="{x}" y="{y}" width="36" height="{h}" fill="{S["surface_100"]}" '
            f'stroke="{S["surface_200"]}" stroke-width="1.5"/>\n'
        )
        self.parts.append(
            f'  <text x="{x + 18}" y="{y + h / 2}" text-anchor="middle" '
            f'fill="{S["surface_700"]}" font-family="{FONT}" font-size="12" '
            f'transform="rotate(-90 {x + 18} {y + h / 2})">{_esc(title)}</text>\n'
        )

    def layer_band(self, x: float, y: float, w: float, h: float, title: str) -> None:
        self.parts.append(
            f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{S["primary_tint"]}" '
            f'stroke="{S["surface_200"]}" stroke-width="1.5" rx="{S["border_radius"]}"/>\n'
        )
        self.label(x + 16, y + 28, title, size=14)
        inner_y = y + 40
        self.placeholder(x + 20, inner_y, w - 40, h - 52, f"{title} components")

    def class_box(self, x: float, y: float, w: float, h: float, name: str) -> None:
        self.parts.append(
            f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{S["surface_0"]}" '
            f'stroke="{S["surface_700"]}" stroke-width="1.5"/>\n'
        )
        self.parts.append(f'  <line x1="{x}" y1="{y + 36}" x2="{x + w}" y2="{y + 36}" stroke="{S["surface_700"]}" stroke-width="1.5"/>\n')
        self.parts.append(f'  <line x1="{x}" y1="{y + 68}" x2="{x + w}" y2="{y + 68}" stroke="{S["surface_700"]}" stroke-width="1.5"/>\n')
        self.label(x + w / 2, y + 24, name, anchor="middle", size=13)
        self.label(x + w / 2, y + 54, "+ attributes", anchor="middle", muted=True, size=11)
        self.label(x + w / 2, y + 86, "+ operations", anchor="middle", muted=True, size=11)

    def lifeline(self, x: float, top: float, bottom: float, name: str) -> None:
        self.solid_box(x - 50, top, 100, 36, name, rx=S["border_radius"])
        self.parts.append(
            f'  <line x1="{x}" y1="{top + 36}" x2="{x}" y2="{bottom}" stroke="{S["surface_700"]}" '
            f'stroke-width="1.25" stroke-dasharray="6 4"/>\n'
        )

    def activation(self, x: float, y: float, h: float) -> None:
        self.parts.append(
            f'  <rect x="{x - 8}" y="{y}" width="16" height="{h}" fill="{S["primary_tint"]}" '
            f'stroke="{S["primary"]}" stroke-width="1.5"/>\n'
        )

    def use_case_oval(self, cx: float, cy: float, rx: float, ry: float, label: str) -> None:
        self.parts.append(
            f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{S["surface_0"]}" '
            f'stroke="{S["surface_700"]}" stroke-width="1.5"/>\n'
        )
        self.label(cx, cy + 5, label, anchor="middle", size=12)

    def state_rounded(self, x: float, y: float, w: float, h: float, label: str) -> None:
        self.placeholder(x, y, w, h, label, rx=S["border_radius"])

    def matrix(
        self,
        x: float,
        y: float,
        cols: int,
        rows: int,
        cell_w: float,
        cell_h: float,
        *,
        col_labels: Sequence[str] = (),
        row_labels: Sequence[str] = (),
    ) -> None:
        for r in range(rows):
            for c in range(cols):
                self.parts.append(
                    f'  <rect x="{x + c * cell_w}" y="{y + r * cell_h}" width="{cell_w}" height="{cell_h}" '
                    f'fill="{S["surface_0"]}" stroke="{S["surface_200"]}" stroke-width="1"/>\n'
                )
        for i, lbl in enumerate(col_labels):
            self.label(x + i * cell_w + cell_w / 2, y - 12, lbl, anchor="middle", muted=True)
        for i, lbl in enumerate(row_labels):
            self.label(x - 12, y + i * cell_h + cell_h / 2 + 4, lbl, anchor="end", muted=True)

    def add_markers(self) -> None:
        if any("marker-end" in p for p in self.parts):
            return
        self.parts.insert(
            2,
            '  <defs>\n'
            '    <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">\n'
            f'      <path d="M0,0 L8,4 L0,8 Z" fill="{S["surface_700"]}"/>\n'
            "    </marker>\n"
            "  </defs>\n",
        )