#!/usr/bin/env python3
"""shape_kit — shared helpers for the Shape & Diagram SVG library.

Every category script imports this. Palette, page chrome, and low-level
drawing primitives live here once, so category scripts only contain their
own shape logic and grid layout.
"""
import math

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

DK = L_STROKE
MD = L_MUTED
LT = L_FILL

# ── Core wrappers ───────────────────────────────────────────────────
def SVG(body):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
        + body + '</svg>\n'
    )

def BG(c=L_CANVAS):
    return f'  <rect id="bg" width="{W}" height="{H}" fill="{c}"/>\n'

def T(tid, x, y, txt, sz=11, wt="400", col=DK, anc="start", ls=0):
    ls_a = f' letter-spacing="{ls}"' if ls else ""
    return (f'  <text id="{tid}" x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{sz}" '
            f'font-weight="{wt}" fill="{col}" text-anchor="{anc}"{ls_a}>{txt}</text>\n')

# ── Primitive drawing helpers — fc = fill, col = stroke, everywhere ────
def R(rid, x, y, w, h, fc=L_CANVAS, rx=0, col=None, sw=1):
    st = f' stroke="{col}" stroke-width="{sw}"' if col else ""
    return f'  <rect id="{rid}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fc}" rx="{rx}"{st}/>\n'

def L(lid, x1, y1, x2, y2, col=LT, sw=1, dash=None, cap="butt"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    c = f' stroke-linecap="{cap}"' if cap != "butt" else ""
    return f'  <line id="{lid}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}"{d}{c}/>\n'

def C(cid, cx, cy, r, fc=L_FILL, col=DK, sw=1.5):
    return f'  <circle id="{cid}" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fc}" stroke="{col}" stroke-width="{sw}"/>\n'

def E(eid, cx, cy, rx, ry, fc=L_FILL, col=DK, sw=1.5):
    return f'  <ellipse id="{eid}" cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fc}" stroke="{col}" stroke-width="{sw}"/>\n'

def POLY(pid, pts, fc=L_FILL, col=DK, sw=1.5):
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'  <polygon id="{pid}" points="{pts_str}" fill="{fc}" stroke="{col}" stroke-width="{sw}"/>\n'

def PATH(pid, d, fc="none", col=DK, sw=1.5):
    return f'  <path id="{pid}" d="{d}" fill="{fc}" stroke="{col}" stroke-width="{sw}"/>\n'

def ARROW(aid, x, y, direction="right", size=9, col=DK, hollow=False):
    if direction == "right":
        pts = [(x, y), (x - size, y - size * 0.6), (x - size, y + size * 0.6)]
    else:
        pts = [(x, y), (x + size, y - size * 0.6), (x + size, y + size * 0.6)]
    if hollow:
        return POLY(aid, pts, "none", col, 1.2)
    return POLY(aid, pts, col, col, 0)

def OPEN_ARROW(aid, x, y, direction="right", size=8, col=DK, sw=1.5):
    if direction == "right":
        d = f"M {x-size:.1f},{y-size*0.6:.1f} L {x:.1f},{y:.1f} L {x-size:.1f},{y+size*0.6:.1f}"
    else:
        d = f"M {x+size:.1f},{y-size*0.6:.1f} L {x:.1f},{y:.1f} L {x+size:.1f},{y+size*0.6:.1f}"
    return PATH(aid, d, "none", col, sw)

def DIAMOND(did, x, y, size=8, filled=True, col=DK):
    pts = [(x - size, y), (x, y - size * 0.65), (x + size, y), (x, y + size * 0.65)]
    if filled:
        return POLY(did, pts, col, col, 0)
    return POLY(did, pts, "none", col, 1.2)

def TRI_HOLLOW(tid, x, y, size=10, col=DK):
    pts = [(x, y - size * 0.6), (x + size, y), (x, y + size * 0.6)]
    return POLY(tid, pts, "none", col, 1.3)

# ── Reusable components: <defs>/<symbol> + <use> ───────────────────────
# Use these instead of calling a drawing helper repeatedly when the same
# shape appears 3+ times in one diagram (Gantt task bars, repeated flowchart
# nodes, legend swatches, etc). Define once, <use> everywhere. See
# references/reusable-components.md in the svg-diagram-system skill for the
# full methodology (mode-swapping via CSS custom properties, ID namespacing,
# embedded-defs-vs-sprite-sheet tradeoffs).
def DEFS(*symbols):
    return "  <defs>\n" + "".join(symbols) + "  </defs>\n"

def SYMBOL(sid, viewbox, inner_svg):
    return f'    <symbol id="{sid}" viewBox="{viewbox}">\n{inner_svg}    </symbol>\n'

def USE(sid, x, y, w=None, h=None, cls=None, extra=""):
    dims = f' width="{w}" height="{h}"' if w is not None else ""
    klass = f' class="{cls}"' if cls else ""
    return f'  <use href="#{sid}" x="{x:.1f}" y="{y:.1f}"{dims}{klass}{extra}/>\n'

def reg_poly_pts(cx, cy, r, sides, rotation=-90):
    pts = []
    for i in range(sides):
        ang = math.radians(rotation + i * 360 / sides)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts

def star_pts(cx, cy, r_outer, r_inner, points=5, rotation=-90):
    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        ang = math.radians(rotation + i * 360 / (points * 2))
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts

# ── Page chrome (mode-aware: a dark-mode page is a real dark page) ────
def INNER(n, title, body, subtitle="", mode="light", cat_label="SHAPE &amp; DIAGRAM LIBRARY"):
    if mode == "light":
        bg, ink, muted = L_CANVAS, L_STROKE, L_MUTED
    else:
        bg, ink, muted = D_CANVAS, D_STROKE, D_MUTED

    hdr = (
        f'  <g id="header">\n'
        f'    <text x="{LM}" y="36" font-family="{FF}" font-size="8" fill="{muted}" letter-spacing="2.5">{cat_label}</text>\n'
        f'    <text x="{RM}" y="36" font-family="{FF}" font-size="8" fill="{muted}" text-anchor="end">{str(n).zfill(2)}</text>\n'
        f'    <line x1="{LM}" y1="48" x2="{RM}" y2="48" stroke="{muted}" stroke-width="0.5" opacity="0.4"/>\n'
        f'  </g>\n'
    )
    ftr = (
        f'  <g id="footer">\n'
        f'    <line x1="{LM}" y1="{H-44}" x2="{RM}" y2="{H-44}" stroke="{muted}" stroke-width="0.5" opacity="0.4"/>\n'
        f'    <text x="{LM}" y="{H-26}" font-family="{FF}" font-size="8" fill="{muted}" letter-spacing="1.5">{cat_label}</text>\n'
        f'    <text x="{RM}" y="{H-26}" font-family="{FF}" font-size="8" fill="{muted}" text-anchor="end" letter-spacing="1">{mode.upper()} MODE</text>\n'
        f'  </g>\n'
    )
    sub = T("subtitle", LM, 130, subtitle, 11, "400", muted) if subtitle else ""
    return SVG(
        BG(bg)
        + R("accent-bar", 0, 0, 6, H, ink, 0, None, 0)
        + hdr
        + T("pg-title", LM, 108, title, 24, "700", ink, ls=-0.5)
        + sub
        + L("title-accent", LM, 142, LM + 52, 142, ink, 2)
        + body
        + ftr
    )
