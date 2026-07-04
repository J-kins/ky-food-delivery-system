#!/usr/bin/env python3
"""Category 01 — Basic & Primitive Shapes.

Generates one clean, transparent SVG per shape per mode (64 files total).
No grid sheet, no combined file — each shape is its own standalone asset,
sized to a consistent 140x100 viewBox so they compose predictably.
"""
import os
import math
from shape_kit import (
    L_FILL, L_STROKE, D_FILL, D_STROKE,
    R, L, C, E, POLY, PATH, ARROW,
    reg_poly_pts, star_pts,
)

OUT = "/mnt/user-data/outputs/shape-library/01-basic-primitive-shapes"
os.makedirs(OUT, exist_ok=True)

VB_W, VB_H = 140, 100
CX, CY = VB_W / 2, VB_H / 2

SHAPES = [
    ("circle-simple",     "Circle, Simple"),
    ("circle-filled",     "Circle, Filled"),
    ("circle-bullseye",   "Circle, Bullseye"),
    ("circle-hollow",     "Circle, Hollow"),
    ("circle-x",          "Circle with X"),
    ("circle-plus",       "Circle with Plus"),
    ("circle-double",     "Double Circle"),
    ("circle-concentric", "Concentric Circles"),
    ("oval",               "Oval / Ellipse"),
    ("rectangle",           "Rectangle"),
    ("rounded-rectangle",   "Rounded Rectangle"),
    ("square",               "Square"),
    ("diamond",              "Diamond / Rhombus"),
    ("triangle-up",          "Triangle, Up"),
    ("triangle-down",        "Triangle, Down"),
    ("triangle-right",       "Right Triangle"),
    ("parallelogram",        "Parallelogram"),
    ("trapezoid",            "Trapezoid"),
    ("pentagon",             "Pentagon (Home-Plate)"),
    ("hexagon",              "Hexagon"),
    ("cylinder",             "Cylinder"),
    ("cloud",                "Cloud"),
    ("cross",                "Cross / Plus"),
    ("x-mark",               "X Mark"),
    ("star",                 "Star"),
    ("arrow-straight",       "Arrow, Straight"),
    ("arrow-curved",         "Arrow, Curved"),
    ("arrow-block",          "Arrow, Block/Thick"),
    ("line-solid",           "Line, Solid"),
    ("line-dashed",          "Line, Dashed"),
    ("line-dotted",          "Line, Dotted"),
    ("bracket",              "Bracket / Brace"),
]

def draw_shape(kind, cx, cy, fc, col):
    p = kind
    if kind == "circle-simple":
        return C(p, cx, cy, 26, fc, col, 1.5)
    if kind == "circle-filled":
        return C(p, cx, cy, 15, col, col, 0)
    if kind == "circle-bullseye":
        return C(p+"-o", cx, cy, 25, fc, col, 1.5) + C(p+"-i", cx, cy, 12, col, col, 0)
    if kind == "circle-hollow":
        return C(p, cx, cy, 24, "none", col, 1.5)
    if kind == "circle-x":
        s = 9
        return (C(p, cx, cy, 25, fc, col, 1.5)
                + L(p+"-1", cx-s, cy-s, cx+s, cy+s, col, 1.5)
                + L(p+"-2", cx-s, cy+s, cx+s, cy-s, col, 1.5))
    if kind == "circle-plus":
        s = 10
        return (C(p, cx, cy, 25, fc, col, 1.5)
                + L(p+"-1", cx-s, cy, cx+s, cy, col, 1.5)
                + L(p+"-2", cx, cy-s, cx, cy+s, col, 1.5))
    if kind == "circle-double":
        return C(p+"-o", cx, cy, 26, "none", col, 1.5) + C(p+"-i", cx, cy, 18, "none", col, 1.5)
    if kind == "circle-concentric":
        return (C(p+"-1", cx, cy, 10, "none", col, 1.2)
                + C(p+"-2", cx, cy, 19, "none", col, 1.2)
                + C(p+"-3", cx, cy, 28, "none", col, 1.2))
    if kind == "oval":
        return E(p, cx, cy, 40, 22, fc, col, 1.5)
    if kind == "rectangle":
        return R(p, cx-44, cy-26, 88, 52, fc, 0, col, 1.5)
    if kind == "rounded-rectangle":
        return R(p, cx-44, cy-26, 88, 52, fc, 10, col, 1.5)
    if kind == "square":
        return R(p, cx-28, cy-28, 56, 56, fc, 0, col, 1.5)
    if kind == "diamond":
        return POLY(p, [(cx, cy-30), (cx+40, cy), (cx, cy+30), (cx-40, cy)], fc, col, 1.5)
    if kind == "triangle-up":
        return POLY(p, [(cx, cy-28), (cx+34, cy+22), (cx-34, cy+22)], fc, col, 1.5)
    if kind == "triangle-down":
        return POLY(p, [(cx, cy+28), (cx+34, cy-22), (cx-34, cy-22)], fc, col, 1.5)
    if kind == "triangle-right":
        return POLY(p, [(cx-32, cy+26), (cx+32, cy+26), (cx-32, cy-26)], fc, col, 1.5)
    if kind == "parallelogram":
        return POLY(p, [(cx-30, cy-24), (cx+44, cy-24), (cx+30, cy+24), (cx-44, cy+24)], fc, col, 1.5)
    if kind == "trapezoid":
        return POLY(p, [(cx-22, cy-24), (cx+22, cy-24), (cx+42, cy+24), (cx-42, cy+24)], fc, col, 1.5)
    if kind == "pentagon":
        return POLY(p, [(cx-42, cy-24), (cx+14, cy-24), (cx+42, cy), (cx+14, cy+24), (cx-42, cy+24)], fc, col, 1.5)
    if kind == "hexagon":
        return POLY(p, reg_poly_pts(cx, cy, 32, 6, rotation=0), fc, col, 1.5)
    if kind == "cylinder":
        bw, bh, cap = 76, 34, 11
        top, bot = cy - bh/2, cy + bh/2
        out  = R(p+"-body", cx-bw/2, top, bw, bh, fc, 0, None, 0)
        out += L(p+"-l", cx-bw/2, top, cx-bw/2, bot, col, 1.3)
        out += L(p+"-r", cx+bw/2, top, cx+bw/2, bot, col, 1.3)
        out += E(p+"-b", cx, bot, bw/2, cap, fc, col, 1.3)
        out += E(p+"-t", cx, top, bw/2, cap, fc, col, 1.3)
        return out
    if kind == "cloud":
        out  = E(p+"-base", cx, cy+8, 42, 15, fc, "none", 0)
        out += C(p+"-c1", cx-24, cy, 15, fc, fc, 0)
        out += C(p+"-c2", cx-3, cy-13, 20, fc, fc, 0)
        out += C(p+"-c3", cx+18, cy-5, 17, fc, fc, 0)
        out += C(p+"-c4", cx+31, cy+3, 12, fc, fc, 0)
        return out
    if kind == "cross":
        a, b = 12, 34
        pts = [(cx-a,cy-b),(cx+a,cy-b),(cx+a,cy-a),(cx+b,cy-a),(cx+b,cy+a),(cx+a,cy+a),
               (cx+a,cy+b),(cx-a,cy+b),(cx-a,cy+a),(cx-b,cy+a),(cx-b,cy-a),(cx-a,cy-a)]
        return POLY(p, pts, fc, col, 1.5)
    if kind == "x-mark":
        s = 26
        return (L(p+"-1", cx-s, cy-s, cx+s, cy+s, col, 2.5)
                + L(p+"-2", cx-s, cy+s, cx+s, cy-s, col, 2.5))
    if kind == "star":
        return POLY(p, star_pts(cx, cy, 30, 13, 5), fc, col, 1.5)
    if kind == "arrow-straight":
        return L(p, cx-40, cy, cx+30, cy, col, 2) + ARROW(p+"-h", cx+42, cy, "right", 9, col)
    if kind == "arrow-curved":
        p0 = (cx-38, cy+16); p1 = (cx-4, cy-32); p2 = (cx+38, cy-2)
        d = f"M {p0[0]:.1f},{p0[1]:.1f} Q {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
        ang = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
        size = 10
        a1 = (p2[0]-size*math.cos(ang-0.45), p2[1]-size*math.sin(ang-0.45))
        a2 = (p2[0]-size*math.cos(ang+0.45), p2[1]-size*math.sin(ang+0.45))
        return PATH(p, d, "none", col, 2) + POLY(p+"-h", [p2, a1, a2], col, col, 0)
    if kind == "arrow-block":
        tail_x, head_x, tip_x = cx-44, cx+6, cx+44
        st, sb, ht, hb = cy-12, cy+12, cy-24, cy+24
        pts = [(tail_x,st),(head_x,st),(head_x,ht),(tip_x,cy),(head_x,hb),(head_x,sb),(tail_x,sb)]
        return POLY(p, pts, fc, col, 1.5)
    if kind == "line-solid":
        return L(p, cx-46, cy, cx+46, cy, col, 2)
    if kind == "line-dashed":
        return L(p, cx-46, cy, cx+46, cy, col, 2, dash="8,5")
    if kind == "line-dotted":
        return L(p, cx-46, cy, cx+46, cy, col, 2.5, dash="0.5,6", cap="round")
    if kind == "bracket":
        d = (f"M {cx+14:.1f},{cy-30:.1f} Q {cx-6:.1f},{cy-30:.1f} {cx-6:.1f},{cy-12:.1f} "
             f"Q {cx-6:.1f},{cy:.1f} {cx-18:.1f},{cy:.1f} Q {cx-6:.1f},{cy:.1f} {cx-6:.1f},{cy+12:.1f} "
             f"Q {cx-6:.1f},{cy+30:.1f} {cx+14:.1f},{cy+30:.1f}")
        return PATH(p, d, "none", col, 1.8)
    return C(p, cx, cy, 20, fc, col, 1.5)

def svg_wrap(body):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}" '
        f'width="{VB_W}" height="{VB_H}">\n{body}</svg>\n'
    )

if __name__ == "__main__":
    count = 0
    for kind, label in SHAPES:
        for mode, fc, col in (("light", L_FILL, L_STROKE), ("dark", D_FILL, D_STROKE)):
            body = draw_shape(kind, CX, CY, fc, col)
            path = os.path.join(OUT, f"shape-{kind}-{mode}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg_wrap(body))
            count += 1
    print(f"Generated {count} files -> {OUT}/")
