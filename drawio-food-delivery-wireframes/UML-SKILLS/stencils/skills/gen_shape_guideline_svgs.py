#!/usr/bin/env python3
"""Shape & Diagram Design Guideline — Generic Walkthrough (4 pages)

Palette extracted from the reference brand image. Generic primitives only —
no named diagram shapes (no UML boxes, flowchart symbols, etc). This is the
foundation layer; individual per-shape guidelines get built on top of it.
"""
import os

OUT = "/mnt/user-data/outputs/shape-guideline-svgs"
os.makedirs(OUT, exist_ok=True)

W, H = 1280, 720
FF   = "'Helvetica Neue', Helvetica, Arial, sans-serif"
LM   = 72
RM   = W - 72

# ── Palette — extracted from the reference image ───────────────────────
L_CANVAS = "#FFFFFF"
L_FILL   = "#E5E5E5"
L_STROKE = "#1A1A1A"
L_MUTED  = "#8A8A85"
D_CANVAS = "#0D0D0D"
D_FILL   = "#1E1E1E"
D_STROKE = "#F2F2F2"
D_MUTED  = "#8A8A85"

DK = L_STROKE   # page-chrome ink (the doc uses its own system for its own chrome)
MD = L_MUTED
LT = L_FILL

# ── Base helpers ─────────────────────────────────────────────────────
def SVG(body):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
        + body
        + '</svg>\n'
    )

def BG(c=L_CANVAS):
    return f'  <rect id="bg" width="{W}" height="{H}" fill="{c}"/>\n'

def T(tid, x, y, txt, sz=11, wt="400", col=DK, anc="start", ls=0):
    ls_a = f' letter-spacing="{ls}"' if ls else ""
    return (f'  <text id="{tid}" x="{x}" y="{y}" font-family="{FF}" font-size="{sz}" '
            f'font-weight="{wt}" fill="{col}" text-anchor="{anc}"{ls_a}>{txt}</text>\n')

def R(rid, x, y, w, h, col=L_CANVAS, rx=0, sc=None, sw=1):
    st = f' stroke="{sc}" stroke-width="{sw}"' if sc else ""
    return f'  <rect id="{rid}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" rx="{rx}"{st}/>\n'

def L(lid, x1, y1, x2, y2, col=LT, sw=1):
    return f'  <line id="{lid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}"/>\n'

def ARROW(aid, x, y, direction="right", size=9, col=DK, hollow=False):
    if direction == "right":
        pts = f"{x},{y} {x-size},{y-size*0.6} {x-size},{y+size*0.6}"
    else:
        pts = f"{x},{y} {x+size},{y-size*0.6} {x+size},{y+size*0.6}"
    if hollow:
        return f'  <polygon id="{aid}" points="{pts}" fill="none" stroke="{col}" stroke-width="1.2"/>\n'
    return f'  <polygon id="{aid}" points="{pts}" fill="{col}"/>\n'

def OPEN_ARROW(aid, x, y, direction="right", size=8, col=DK, sw=1.5):
    if direction == "right":
        d = f"M {x-size},{y-size*0.6} L {x},{y} L {x-size},{y+size*0.6}"
    else:
        d = f"M {x+size},{y-size*0.6} L {x},{y} L {x+size},{y+size*0.6}"
    return f'  <path id="{aid}" d="{d}" stroke="{col}" fill="none" stroke-width="{sw}"/>\n'

def DIAMOND(did, x, y, size=8, filled=True, col=DK):
    pts = f"{x-size},{y} {x},{y-size*0.65} {x+size},{y} {x},{y+size*0.65}"
    if filled:
        return f'  <polygon id="{did}" points="{pts}" fill="{col}"/>\n'
    return f'  <polygon id="{did}" points="{pts}" fill="none" stroke="{col}" stroke-width="1.2"/>\n'

def TRI_HOLLOW(tid, x, y, size=10, col=DK):
    pts = f"{x},{y-size*0.6} {x+size},{y} {x},{y+size*0.6}"
    return f'  <polygon id="{tid}" points="{pts}" fill="none" stroke="{col}" stroke-width="1.3"/>\n'

def HDR(n, sec="SHAPE &amp; DIAGRAM DESIGN GUIDELINE"):
    return (
        f'  <g id="header">\n'
        f'    <text x="{LM}" y="36" font-family="{FF}" font-size="8" fill="{MD}" letter-spacing="2.5">{sec}</text>\n'
        f'    <text x="{RM}" y="36" font-family="{FF}" font-size="8" fill="{MD}" text-anchor="end">{str(n).zfill(2)}</text>\n'
        f'    <line x1="{LM}" y1="48" x2="{RM}" y2="48" stroke="{LT}" stroke-width="1"/>\n'
        f'  </g>\n'
    )

def FTR():
    return (
        f'  <g id="footer">\n'
        f'    <line x1="{LM}" y1="{H-44}" x2="{RM}" y2="{H-44}" stroke="{LT}" stroke-width="1"/>\n'
        f'    <text x="{LM}" y="{H-26}" font-family="{FF}" font-size="8" fill="{MD}" letter-spacing="1.5">SHAPE &amp; DIAGRAM LIBRARY</text>\n'
        f'    <text x="{RM}" y="{H-26}" font-family="{FF}" font-size="8" fill="{MD}" text-anchor="end" letter-spacing="1">GENERAL GUIDELINE — WALKTHROUGH</text>\n'
        f'  </g>\n'
    )

def INNER(n, sec_lbl, title, body, subtitle=""):
    sub = T("subtitle", LM, 130, subtitle, 11, "400", MD) if subtitle else ""
    return SVG(
        BG()
        + R("accent-bar", 0, 0, 6, H, DK)
        + HDR(n, sec_lbl)
        + T("pg-title", LM, 108, title, 24, "700", DK, ls=-0.5)
        + sub
        + L("title-accent", LM, 142, LM + 52, 142, DK, 2)
        + body
        + FTR()
    )

# ════════════════════════════════════════════════════════════════════
# PAGE 1 — COLOR SYSTEM
# ════════════════════════════════════════════════════════════════════
def page_color_system():
    body = T("desc", LM, 168,
             "Four tokens per mode — canvas, shape fill, stroke/text, and one shared muted tone.",
             11, "400", MD)

    body += T("row-light", LM, 192, "LIGHT MODE", 8, "700", DK, ls=2)
    light_sw = [
        (L_CANVAS, "CANVAS", "Page / artboard background", "#FFFFFF", True),
        (L_FILL,   "FILL",   "Shape body fill",             "#E5E5E5", False),
        (L_STROKE, "STROKE / TEXT", "Outlines &amp; primary text", "#1A1A1A", False),
        (L_MUTED,  "MUTED",  "Captions &amp; secondary text", "#8A8A85", False),
    ]
    sw_w = 250
    for i, (col, role, desc, hexv, needs_border) in enumerate(light_sw):
        bx = LM + i * (sw_w + 30)
        sc = LT if needs_border else None
        body += (
            R(f"ls{i}", bx, 204, sw_w, 128, col, 4, sc, 1)
            + T(f"lr{i}", bx, 350, role, 8, "700", MD, ls=1.5)
            + T(f"ld{i}", bx, 366, desc, 10, "400", DK)
            + T(f"lh{i}", bx, 381, hexv, 9, "400", MD)
        )

    body += T("row-dark", LM, 412, "DARK MODE", 8, "700", DK, ls=2)
    dark_sw = [
        (D_CANVAS, "CANVAS", "Page / artboard background", "#0D0D0D"),
        (D_FILL,   "FILL",   "Shape body fill",             "#1E1E1E"),
        (D_STROKE, "STROKE / TEXT", "Outlines &amp; primary text", "#F2F2F2"),
        (D_MUTED,  "MUTED",  "Captions &amp; secondary text", "#8A8A85"),
    ]
    for i, (col, role, desc, hexv) in enumerate(dark_sw):
        bx = LM + i * (sw_w + 30)
        body += (
            R(f"ds{i}", bx, 426, sw_w, 128, col, 4, None, 1)
            + T(f"dr{i}", bx, 572, role, 8, "700", MD, ls=1.5)
            + T(f"dd{i}", bx, 588, desc, 10, "400", DK)
            + T(f"dh{i}", bx, 603, hexv, 9, "400", MD)
        )

    body += T("note", LM, 636,
              "Muted keeps the identical hex in both modes — the one constant that ties light and dark together.",
              9, "400", MD)

    return INNER(1, "01  FOUNDATIONS", "Color System", body,
                 "The complete palette for every shape you draw. Never introduce a color outside this set.")

# ════════════════════════════════════════════════════════════════════
# PAGE 2 — LINE & CONNECTOR LANGUAGE
# ════════════════════════════════════════════════════════════════════
def page_line_connector():
    body = T("desc", LM, 168,
             "Weight and end-style are semantic, never decorative. Shown in the light-mode stroke token; "
             "invert to dark-mode stroke on dark canvas.",
             11, "400", MD)

    body += T("sec-a", LM, 200, "STROKE WEIGHT", 8, "700", DK, ls=2)
    weights = [
        (1.5,  "Shape outline", "Every shape boundary"),
        (2.0,  "Connector / flow line", "Default line between shapes"),
        (2.75, "Emphasis line", "Critical path, active state — weight signals it, not color"),
    ]
    wy = 224
    for i, (w, name, use) in enumerate(weights):
        ly = wy + i * 40
        body += (
            L(f"wl{i}", LM, ly, LM + 140, ly, DK, w)
            + T(f"wn{i}", LM + 168, ly + 4, f"{name} — {w}px", 11, "600", DK)
            + T(f"wu{i}", LM + 168, ly + 20, use, 9, "400", MD)
        )

    body += (
        T("sec-b", LM, 372, "CONNECTOR MEANING", 8, "700", DK, ls=2)
        + L("sec-b-r", LM, 384, RM, 384, LT, 1)
    )

    connectors = [
        ("solid-filled",  "Flow / synchronous message"),
        ("solid-open",    "Async message / directed association"),
        ("dashed-open",   "Dependency"),
        ("dashed-tri",    "Realization / interface implementation"),
        ("solid-tri",     "Generalization / inheritance"),
        ("hollow-diamond","Aggregation"),
        ("filled-diamond","Composition"),
    ]

    def draw_connector(cid, x, y, kind):
        x1, x2 = x, x + 110
        out = ""
        if kind == "solid-filled":
            out += L(f"{cid}l", x1, y, x2 - 10, y, DK, 2)
            out += ARROW(f"{cid}a", x2, y, "right", 9, DK, hollow=False)
        elif kind == "solid-open":
            out += L(f"{cid}l", x1, y, x2 - 8, y, DK, 2)
            out += OPEN_ARROW(f"{cid}a", x2, y, "right", 8, DK)
        elif kind == "dashed-open":
            out += (f'  <line id="{cid}l" x1="{x1}" y1="{y}" x2="{x2-8}" y2="{y}" '
                     f'stroke="{DK}" stroke-width="2" stroke-dasharray="5,4"/>\n')
            out += OPEN_ARROW(f"{cid}a", x2, y, "right", 8, DK)
        elif kind == "dashed-tri":
            out += (f'  <line id="{cid}l" x1="{x1}" y1="{y}" x2="{x2-14}" y2="{y}" '
                     f'stroke="{DK}" stroke-width="2" stroke-dasharray="5,4"/>\n')
            out += TRI_HOLLOW(f"{cid}a", x2, y, 12, DK)
        elif kind == "solid-tri":
            out += L(f"{cid}l", x1, y, x2 - 14, y, DK, 2)
            out += TRI_HOLLOW(f"{cid}a", x2, y, 12, DK)
        elif kind == "hollow-diamond":
            out += L(f"{cid}l", x1, y, x2 - 14, y, DK, 2)
            out += DIAMOND(f"{cid}a", x2 - 8, y, 9, filled=False, col=DK)
        elif kind == "filled-diamond":
            out += L(f"{cid}l", x1, y, x2 - 14, y, DK, 2)
            out += DIAMOND(f"{cid}a", x2 - 8, y, 9, filled=True, col=DK)
        return out

    col_x = [LM, LM + 570]
    for i, (kind, meaning) in enumerate(connectors):
        col = i // 4
        row = i % 4
        x = col_x[col]
        y = 424 + row * 56
        body += draw_connector(f"c{i}", x, y, kind)
        body += T(f"cm{i}", x + 150, y + 4, meaning, 10, "400", DK)

    return INNER(2, "01  FOUNDATIONS", "Line &amp; Connector Language", body,
                 "Reach for the meaning first, then draw the line that says it.")

# ════════════════════════════════════════════════════════════════════
# PAGE 3 — SHAPE, CORNER & CURVE LANGUAGE
# ════════════════════════════════════════════════════════════════════
def page_shape_corner_curve():
    body = T("desc", LM, 168,
             "Radius is decided by geometry, not preference. Curves appear only where the shape is inherently curved.",
             11, "400", MD)

    body += T("sec-a", LM, 200, "CORNER RADIUS", 8, "700", DK, ls=2)
    corners = [
        (0,  "Sharp — 0px",   "Diamonds, triangles — never round"),
        (8,  "8px radius",    "Process, task &amp; module shapes"),
        (6,  "6px radius",    "UML class, ER entity, records"),
        (40, "Fully rounded", "Terminator — inherent, not chosen"),
    ]
    cw = 236
    for i, (rx, name, use) in enumerate(corners):
        bx = LM + i * (cw + 20)
        body += (
            R(f"cr{i}", bx, 224, cw, 80, L_FILL, rx, DK, 1.5)
            + T(f"crn{i}", bx, 322, name, 10, "600", DK)
            + T(f"cru{i}", bx, 338, use, 8, "400", MD)
        )

    body += (
        T("sec-b", LM, 388, "CURVES &amp; ARCS", 8, "700", DK, ls=2)
        + L("sec-b-r", LM, 400, LM + 640, 400, LT, 1)
    )

    body += (
        f'  <path id="arc1" d="M {LM},460 A 70,45 0 0,1 {LM+140},460" stroke="{DK}" fill="none" stroke-width="1.5"/>\n'
        + T("arc-lbl", LM, 540, "Arc", 10, "600", DK)
        + T("arc-use", LM, 556, "Cylinder caps, pie segments", 8, "400", MD)
    )

    cx0 = LM + 220
    body += (
        f'  <path id="curve1" d="M {cx0},440 Q {cx0+70},510 {cx0+140},440" stroke="{DK}" fill="none" stroke-width="1.5"/>\n'
        + T("curve-lbl", cx0, 540, "Curve", 10, "600", DK)
        + T("curve-use", cx0, 556, "Smart-routed connector paths", 8, "400", MD)
    )

    ex = LM + 460
    body += (
        f'  <ellipse id="ell1" cx="{ex+70}" cy="470" rx="70" ry="35" fill="{L_FILL}" stroke="{DK}" stroke-width="1.5"/>\n'
        + T("ell-lbl", ex, 540, "Ellipse", 10, "600", DK)
        + T("ell-use", ex, 556, "Data store cap, oval terminator", 8, "400", MD)
    )

    ax = LM + 720
    body += (
        T("sec-c", ax, 388, "SHAPE ANATOMY", 8, "700", DK, ls=2)
        + L("sec-c-r", ax, 400, RM, 400, LT, 1)
        + R("anat", ax, 424, 180, 100, L_FILL, 8, DK, 1.5)
        + T("anat-lbl", ax, 546, "Fill + 1.5px stroke,", 9, "400", MD)
        + T("anat-lbl2", ax, 560, "always together", 9, "400", MD)
    )

    return INNER(3, "01  FOUNDATIONS", "Shape, Corner &amp; Curve Language", body,
                 "The same primitives, drawn consistently, are what let hundreds of SVGs read as one library.")

# ════════════════════════════════════════════════════════════════════
# PAGE 4 — TYPOGRAPHY SCALE
# ════════════════════════════════════════════════════════════════════
def page_typography():
    body = T("desc", LM, 168,
             "One sans-serif family throughout. Size, weight, and color are the only variables.",
             11, "400", MD)

    ts_items = [
        ("Panel Heading — 18px / 600 / stroke", "Shape &amp; Diagram Style", 18, "600", DK),
        ("Shape Label — 12px / 400\u2013500 / stroke", "Process Step", 12, "500", DK),
        ("Small / Tight Label — 10px / 600 / stroke", "Valid?", 10, "600", DK),
        ("Micro / Attribute — 8px / 400 / stroke", "+ field: Type", 8, "400", DK),
        ("Caption Label — 10.5px / 400 / muted, +0.3 tracking", "Decision", 10.5, "400", MD),
        ("Panel Subheading — 11px / 400 / muted", "Same rules, tokens swap by mode", 11, "400", MD),
    ]
    y = 200
    for i, (lbl, sample, sz, wt, col) in enumerate(ts_items):
        body += (
            T(f"tl{i}", LM, y, lbl, 8, "400", MD)
            + T(f"ts{i}", LM, y + sz + 10, sample, sz, wt, col)
            + L(f"tr{i}", LM, y + sz + 26, LM + 620, y + sz + 26, LT, 1)
        )
        y += sz + 26 + 24

    rx = LM + 700
    body += (
        T("cmp-hdr", rx, 200, "SAME SCALE, TOKENS SWAP", 8, "700", DK, ls=1.5)
        + R("cmp-l", rx, 220, 200, 110, L_CANVAS, 6, LT, 1)
        + T("cmp-lt", rx + 20, 282, "Aa Decision", 16, "600", L_STROKE)
        + T("cmp-ll", rx + 20, 316, "Light", 8, "400", MD)
        + R("cmp-d", rx, 350, 200, 110, D_CANVAS, 6, None, 1)
        + T("cmp-dt", rx + 20, 412, "Aa Decision", 16, "600", D_STROKE)
        + T("cmp-dl", rx + 20, 446, "Dark", 8, "400", MD)
    )

    return INNER(4, "01  FOUNDATIONS", "Typography Scale", body,
                 "Every text element in the library maps to exactly one of these six roles.")

# ════════════════════════════════════════════════════════════════════
# Write all files
# ════════════════════════════════════════════════════════════════════
pages = {
    "01-color-system": page_color_system(),
    "02-line-connector-language": page_line_connector(),
    "03-shape-corner-curve-language": page_shape_corner_curve(),
    "04-typography-scale": page_typography(),
}

for name, content in sorted(pages.items()):
    path = os.path.join(OUT, f"{name}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ok  {path}")

print(f"\nGenerated {len(pages)} SVG pages -> {OUT}/")
