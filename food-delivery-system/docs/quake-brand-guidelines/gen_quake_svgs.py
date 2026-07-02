#!/usr/bin/env python3
"""Quaké Paraná Brand Guidelines SVG Generator — 11 pages"""
import os

OUT = "/mnt/user-data/outputs/quake-brand-guidelines"
os.makedirs(OUT, exist_ok=True)

W, H   = 1280, 720
FF     = "'Poppins','Helvetica Neue',Helvetica,Arial,sans-serif"
LM, RM = 72, 1208
CW     = RM - LM   # 1136 content width

# ── Brand colours ─────────────────────────────────────────────────────
FG  = "#005638"   # Forest Green
FGD = "#003D28"   # Forest Green Dark
TR  = "#DC4024"   # Tomato Red
SO  = "#F38919"   # Sunset Orange
MY  = "#F0C039"   # Mustard Yellow
KB  = "#E8B57A"   # Kraft Beige
DB  = "#3B2A1A"   # Deep Brown
OW  = "#F7F4EF"   # Off White
WH  = "#FFFFFF"
DK  = "#1A1A1A"
MD  = "#6B6B6B"
LT  = "#E0DBD4"

# ── Core helpers ──────────────────────────────────────────────────────
def SVG(body):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
            + body + '</svg>\n')

def BG(c=OW):  return f'  <rect id="bg" width="{W}" height="{H}" fill="{c}"/>\n'

def R(i, x, y, w, h, c=OW, rx=0, sc=None, sw=1):
    s = f' stroke="{sc}" stroke-width="{sw}"' if sc else ""
    return f'  <rect id="{i}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" rx="{rx}"{s}/>\n'

def L(i, x1, y1, x2, y2, c=LT, sw=0.5):
    return f'  <line id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"/>\n'

def T(i, x, y, t, sz=11, wt="400", c=DK, a="start", ls=0):
    la = f' letter-spacing="{ls}"' if ls else ""
    return (f'  <text id="{i}" x="{x}" y="{y}" font-family="{FF}" '
            f'font-size="{sz}" font-weight="{wt}" fill="{c}" text-anchor="{a}"{la}>{t}</text>\n')

def IMG(i, x, y, w, h, lbl="PHOTO", bg=KB):
    cx, cy = x + w // 2, y + h // 2
    return (f'  <g id="{i}">\n'
            f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}" rx="6"/>\n'
            f'    <line x1="{x+12}" y1="{y+12}" x2="{x+w-12}" y2="{y+h-12}" '
            f'stroke="{WH}" stroke-width="1" opacity="0.3"/>\n'
            f'    <line x1="{x+w-12}" y1="{y+12}" x2="{x+12}" y2="{y+h-12}" '
            f'stroke="{WH}" stroke-width="1" opacity="0.3"/>\n'
            f'    <text x="{cx}" y="{cy+5}" font-family="{FF}" font-size="10" '
            f'fill="{WH}" text-anchor="middle" font-weight="600" opacity="0.85">{lbl}</text>\n'
            f'  </g>\n')

def LB(i, x, y, ws, g=15, bh=8, c=LT):
    o = [f'  <g id="{i}">\n']
    for j, w in enumerate(ws):
        o.append(f'    <rect x="{x}" y="{y+j*g}" width="{w}" height="{bh}" rx="2" fill="{c}"/>\n')
    o.append('  </g>\n')
    return "".join(o)

def CHECK(i, x, y, sz=18, c=FG):
    r = sz // 2
    return (f'  <circle id="{i}-c" cx="{x+r}" cy="{y+r}" r="{r}" fill="{c}"/>\n'
            f'  <text id="{i}-t" x="{x+r}" y="{y+r+5}" font-family="{FF}" '
            f'font-size="{sz-6}" font-weight="700" fill="{WH}" text-anchor="middle">&#10003;</text>\n')

def CROSS(i, x, y, sz=18, c=TR):
    r = sz // 2
    return (f'  <circle id="{i}-c" cx="{x+r}" cy="{y+r}" r="{r}" fill="{c}"/>\n'
            f'  <text id="{i}-t" x="{x+r}" y="{y+r+5}" font-family="{FF}" '
            f'font-size="{sz-4}" font-weight="700" fill="{WH}" text-anchor="middle">&#215;</text>\n')

# ── Pattern strip ─────────────────────────────────────────────────────
PDATA = [
    (FG,MY,"d"),(TR,WH,"x"),(MY,TR,"a"),(FG,SO,"d"),(SO,FG,"x"),(TR,MY,"d"),
    (MY,FG,"a"),(FG,TR,"d"),(SO,WH,"x"),(TR,SO,"a"),(FG,MY,"d"),(MY,TR,"d"),
    (SO,FG,"x"),(TR,WH,"a"),(FG,SO,"d"),(MY,FG,"d"),(TR,MY,"x"),(SO,TR,"a"),
    (FG,MY,"d"),(TR,SO,"d"),(MY,WH,"x"),(SO,FG,"a"),(FG,TR,"d"),(MY,SO,"d"),
    (TR,FG,"x"),(SO,MY,"a"),(FG,WH,"d"),(TR,MY,"d"),(MY,FG,"x"),(SO,TR,"a"),
    (FG,MY,"d"),(TR,SO,"d"),(MY,WH,"x"),(SO,FG,"a"),(FG,TR,"d"),(MY,SO,"d"),
    (TR,FG,"x"),(SO,MY,"a"),(FG,WH,"d"),(TR,MY,"d"),
]

def PSTRIP(pid, x, y, w, h):
    sz    = h
    count = (w // sz) + 1
    o = [f'  <g id="{pid}">\n',
         f'    <rect x="{x}" y="{y}" width="{w}" height="{sz}" fill="{FG}"/>\n']
    for i in range(min(count, len(PDATA))):
        c1, c2, st = PDATA[i]
        ix = x + i * sz
        o.append(f'    <rect x="{ix}" y="{y}" width="{sz}" height="{sz}" fill="{c1}"/>\n')
        if st == "d":
            o.append(f'    <circle cx="{ix+sz//2}" cy="{y+sz//2}" r="{sz//3}" fill="{c2}"/>\n')
        elif st == "x":
            o.append(f'    <line x1="{ix+4}" y1="{y+sz-4}" x2="{ix+sz-4}" y2="{y+4}" '
                     f'stroke="{c2}" stroke-width="{max(3,sz//5)}"/>\n')
        else:
            o.append(f'    <path d="M{ix+sz},{y} A{sz},{sz} 0 0,0 {ix},{y+sz} '
                     f'L{ix+sz},{y+sz} Z" fill="{c2}"/>\n')
    o.append('  </g>\n')
    return "".join(o)

# ── Page chrome ───────────────────────────────────────────────────────
def HDR(n, title):
    nz = f"{str(n).zfill(2)}."
    return (R("top-bar", 0, 0, W, 6, FG)
            + T("s-num",   LM,      48, nz,            11, "800", FG)
            + T("s-title", LM + 42, 48, title.upper(), 11, "800", DK, ls=2)
            + L("s-rule",  LM,      58, RM,            58, LT, 0.75))

def FTR():
    return (PSTRIP("ftr-pat", 0, H - 36, W, 36)
            + T("ftr-l", LM, H - 13,
                "BRAND GUIDELINES  |  VERSION 1.0  |  2024", 8, "600", WH, ls=1)
            + T("ftr-r", RM, H - 13, "QUAKÉ PARANÁ", 8, "700", MY, "end", ls=2))

def INNER(n, title, body):
    return SVG(BG() + HDR(n, title) + body + FTR())

# ════════════════════════════════════════════════════════════════════
# PAGES
# ════════════════════════════════════════════════════════════════════
pages = {}

# ── 01  COVER ─────────────────────────────────────────────────────────
pages["01-cover"] = SVG(
    BG()
    # Left green panel
    + R("gp",    0, 0,      420, H,      FGD)
    + R("gp-dk", 0, H - 94, 420, 58,     FG)
    # Logo & title
    + T("lg1", 48, 126, "Quaké",           54, "800", WH,  ls=-1)
    + T("lg2", 48, 162, "PARANÁ",          19, "700", MY,  ls=6)
    + R("lg-r", 48, 177, 196, 3, MY, 1)
    + T("bg-t", 48, 208, "BRAND GUIDELINES",12, "800", MY,  ls=3)
    + LB("cv-d", 48, 234,
         [308, 328, 288, 328, 308, 288, 328, 304, 284, 308],
         g=17, bh=7, c="rgba(255,255,255,0.2)")
    + PSTRIP("cv-pp", 0, H - 94, 420, 58)
    + T("cv-v", 48, H - 94 - 14, "VERSION 1.0  /  2024",
        8, "600", "rgba(255,255,255,0.38)", ls=2)
    # Centre hero photo
    + IMG("hero", 420, 0, 488, H - 36, "HERO FOOD PHOTO", KB)
    + f'  <rect id="hero-grd" x="420" y="{H-130}" width="488" height="94" '
      f'fill="{FGD}" opacity="0.72"/>\n'
    # Right cream panel
    + R("rp", 908, 0, W - 908, H, OW)
    + T("r-01",  932,  78, "01.",             9, "800", TR)
    + T("r-h1",  932, 104, "BRAND",          20, "800", FG,  ls=0.5)
    + T("r-h2",  932, 128, "ESSENCE",        20, "800", FG,  ls=0.5)
    + L("r-rl",  932, 140, RM - 16, 140, TR, 2)
    + T("r-pl",  932, 168, "Our Purpose",    10, "700", TR)
    + LB("r-pb", 932, 184, [256, 288, 264, 288], g=15, bh=7)
    + T("r-ml",  932, 276, "Our Mission",    10, "700", TR)
    + LB("r-mb", 932, 292, [256, 288, 264, 256], g=15, bh=7)
    + T("r-vl",  932, 368, "Our Values",     10, "700", TR)
    + R("vi0", 932, 385, 44, 44, FG, 22) + T("vt0",  954, 413, "Q", 14, "700", WH, "middle")
    + R("vi1", 985, 385, 44, 44, TR, 22) + T("vt1", 1007, 413, "B", 14, "700", WH, "middle")
    + R("vi2",1038, 385, 44, 44, SO, 22) + T("vt2", 1060, 413, "W", 14, "700", WH, "middle")
    + R("vi3",1091, 385, 44, 44, MY, 22) + T("vt3", 1113, 413, "S", 14, "700", DK, "middle")
    + R("vi4",1144, 385, 44, 44, FG, 22) + T("vt4", 1166, 413, "T", 14, "700", WH, "middle")
    + T("vl0",  954, 443, "Quality",  7, "400", MD, "middle")
    + T("vl1", 1007, 443, "Boldness", 7, "400", MD, "middle")
    + T("vl2", 1060, 443, "Warmth",   7, "400", MD, "middle")
    + T("vl3", 1113, 443, "Speed",    7, "400", MD, "middle")
    + T("vl4", 1166, 443, "Trust",    7, "400", MD, "middle")
    # Footer
    + PSTRIP("cv-ftr", 0, H - 36, W, 36)
    + T("cv-fl", LM, H - 13,
        "BRAND GUIDELINES  |  VERSION 1.0  |  2024", 8, "600", WH, ls=1)
    + T("cv-fr", RM, H - 13, "QUAKÉ PARANÁ", 8, "700", MY, "end", ls=2)
)

# ── 02  BRAND ESSENCE ─────────────────────────────────────────────────
SEC = CW // 5   # 227 per value section
val_body = ""
VALS = [("Quality", FG, WH), ("Boldness", TR, WH),
        ("Warmth",  SO, WH), ("Speed",    MY, DK), ("Trust", FG, WH)]
for vi, (vname, vcol, vtc) in enumerate(VALS):
    vcx  = LM + vi * SEC + SEC // 2
    vbx  = vcx - 52
    val_body += (
        R(f"vb{vi}", vbx, 420, 104, 104, vcol, 52)
        + T(f"vs{vi}", vcx, 480, vname[0], 26, "800", vtc, "middle")
        + T(f"vn{vi}", vcx, 552, vname,    10, "700", DK,  "middle")
    )

pages["02-brand-essence"] = INNER(2, "Brand Essence",
    T("pur-h",    LM,       92,  "Our Purpose",     13, "700", TR)
    + R("pur-r",  LM,      106,  52, 3, TR, 1)
    + T("pur-s1", LM,      130, "To deliver bold, crave-worthy food",       10, "400", MD)
    + T("pur-s2", LM,      148, "experiences that bring people together.",   10, "400", MD)
    + LB("pur-b", LM,      172, [448, 496, 472, 496, 448, 472], g=16, bh=8)
    + T("mis-h",  LM+584,   92,  "Our Mission",     13, "700", TR)
    + R("mis-r",  LM+584,  106,  52, 3, TR, 1)
    + T("mis-s1", LM+584,  130, "To serve high-quality food with speed,",   10, "400", MD)
    + T("mis-s2", LM+584,  148, "warmth and consistency.",                   10, "400", MD)
    + LB("mis-b", LM+584,  172, [448, 496, 472, 496, 448, 472], g=16, bh=8)
    + L("vdiv",   LM,      396, RM, 396, LT, 1)
    + T("val-h",  LM,      414,  "Our Values",      13, "700", TR)
    + val_body
)

# ── 03  LOGO SYSTEM ───────────────────────────────────────────────────
pages["03-logo-system"] = INNER(3, "Logo System",
    # Primary logo (large box)
    T("pl-lbl",  LM,       80,  "PRIMARY LOGO",   8, "700", MD, ls=2)
    + L("pl-r",  LM,       90,  LM+488, 90, LT)
    + R("pl-box",LM,       96,  488, 244, WH, 6, LT)
    + T("pl-mk", LM+244,  212, "Quaké Paraná",  26, "800", FG, "middle")
    + T("pl-su", LM+244,  236, "[ Primary Logo Placeholder ]", 8, "400", MD, "middle")
    # Clear space
    + T("cs-lbl",LM,      364,  "CLEAR SPACE",    8, "700", MD, ls=2)
    + L("cs-r",  LM,      374,  LM+360, 374, LT)
    + R("cs-box",LM,      380,  360, 176, WH, 4, LT)
    + T("cs-x1", LM + 10, 396, "x", 8, "400", MD)
    + T("cs-x2", LM + 10, 538, "x", 8, "400", MD)
    + T("cs-x3", LM+332,  396, "x", 8, "400", MD)
    + T("cs-x4", LM+332,  538, "x", 8, "400", MD)
    + R("cs-lg", LM+68,   412, 224, 108, OW, 4, LT)
    + T("cs-lm", LM+180,  472, "Quaké",  16, "800", FG, "middle")
    + T("cs-no", LM,      572, "X = Height of the accent on the mark", 8, "400", MD)
    # Right column
    + T("sl-lbl",LM+548,   80,  "SECONDARY LOGO", 8, "700", MD, ls=2)
    + L("sl-r",  LM+548,   90,  RM, 90, LT)
    + R("sl-box",LM+548,   96,  288, 148, WH, 6, LT)
    + T("sl-mk", LM+692,  176, "Quaké",   18, "800", FG, "middle")
    + T("sl-su", LM+692,  200, "Paraná",  10, "700", MY, "middle")
    + T("ic-lbl",LM+868,   80,  "ICON / MARK",    8, "700", MD, ls=2)
    + R("ic-box",LM+868,   96,  148, 148, FG, 10)
    + T("ic-mk", LM+942,  182, "Q",       44, "800", MY, "middle")
    + T("ms-lbl",LM+548,  268,  "MINIMUM SIZE",   8, "700", MD, ls=2)
    + R("ms-box",LM+548,  280,  220, 84, WH, 4, LT)
    + T("ms-mk", LM+658,  330, "Quaké",   14, "800", FG, "middle")
    + T("ms-no", LM+548,  380, "25mm  /  70px minimum", 8, "400", MD)
    + T("ff-lbl",LM+548,  412,  "FILE FORMATS",   8, "700", MD, ls=2)
    + R("ff-ln", LM+548,  422,  48, 2, SO, 1)
    + T("ff-1",  LM+548,  444, "SVG — Digital / Web",    9, "400", MD)
    + T("ff-2",  LM+548,  462, "EPS — Print / Vendors",  9, "400", MD)
    + T("ff-3",  LM+548,  480, "PNG — Social / Digital", 9, "400", MD)
    + T("ff-4",  LM+548,  498, "AI  — Master Artwork",   9, "400", MD)
)

# ── 04  COLOUR PALETTE ────────────────────────────────────────────────
SW1_W = (CW - 9)  // 4    # 281  top-row swatch width
SW2_W = (CW - 6)  // 3    # 376  bottom-row swatch width
SW1_H = 192
SW2_H = 104
SY1   = 76
SY2   = SY1 + SW1_H + 88

TOP_COLS = [
    (FG, "FOREST GREEN",   "#005638", "R:0 G:86 B:56",     "C:91 M:0 Y:35 K:47"),
    (TR, "TOMATO RED",     "#DC4024", "R:220 G:64 B:36",   "C:0 M:71 Y:84 K:14"),
    (SO, "SUNSET ORANGE",  "#F38919", "R:243 G:137 B:25",  "C:0 M:44 Y:90 K:5"),
    (MY, "MUSTARD YELLOW", "#F0C039", "R:240 G:192 B:57",  "C:0 M:20 Y:76 K:6"),
]
BOT_COLS = [
    (KB, "KRAFT BEIGE",    "#E8B57A", "R:232 G:181 B:122", "C:0 M:22 Y:47 K:9"),
    (DB, "DEEP BROWN",     "#3B2A1A", "R:59 G:42 B:26",    "C:0 M:29 Y:56 K:77"),
    (OW, "OFF WHITE",      "#F7F4EF", "R:247 G:244 B:239", "C:0 M:1 Y:3 K:3"),
]
col_body = ""
for i, (col, name, hx, rgb, cmyk) in enumerate(TOP_COLS):
    sx  = LM + i * (SW1_W + 3)
    sc  = LT if col in (MY,) else None
    col_body += (
        R(f"sw{i}",  sx, SY1, SW1_W, SW1_H, col, 4, sc)
        + T(f"sn{i}", sx, SY1+SW1_H+18, name,  8, "700", DK)
        + T(f"sh{i}", sx, SY1+SW1_H+34, hx,    9, "700", FG)
        + T(f"sr{i}", sx, SY1+SW1_H+50, rgb,   8, "400", MD)
        + T(f"sc{i}", sx, SY1+SW1_H+66, cmyk,  8, "400", MD)
    )
for i, (col, name, hx, rgb, cmyk) in enumerate(BOT_COLS):
    sx  = LM + i * (SW2_W + 3)
    sc  = LT if col in (KB, OW) else None
    col_body += (
        R(f"swb{i}",  sx, SY2, SW2_W, SW2_H, col, 4, sc)
        + T(f"snb{i}", sx, SY2+SW2_H+18, name, 8, "700", DK)
        + T(f"shb{i}", sx, SY2+SW2_H+34, hx,   9, "700", FG)
        + T(f"srb{i}", sx, SY2+SW2_H+50, rgb,  8, "400", MD)
        + T(f"scb{i}", sx, SY2+SW2_H+66, cmyk, 8, "400", MD)
    )
pages["04-color-palette"] = INNER(4, "Color Palette", col_body)

# ── 05  TYPOGRAPHY ────────────────────────────────────────────────────
WEIGHTS = [("Light","300"),("Regular","400"),("Medium","500"),
           ("SemiBold","600"),("Bold","700"),("ExtraBold","800")]
ty_body = (
    T("pp-lbl",  LM,       78,  "PRIMARY TYPEFACE",              8, "700", MD, ls=2)
    + T("pp-nm", LM,      116,  "POPPINS",                      38, "800", FG, ls=2)
    + T("pp-aa", LM+460,   88,  "Aa",                           64, "800", FG)
    + L("pp-r",  LM,      132,  LM+560, 132, LT, 0.75)
)
for i, (name, wt) in enumerate(WEIGHTS):
    ty_body += T(f"pw{i}", LM, 156 + i*36, f"{name} — Aa Bb Cc 123", 12, wt, DK)
ty_body += (
    L("pp-a1",   LM, 376, LM + 560, 376, LT)
    + T("alph1", LM, 394, "A B C D E F G H I J K L M", 9, "400", MD)
    + T("alph2", LM, 410, "N O P Q R S T U V W X Y Z", 9, "400", MD)
    + T("alph3", LM, 426, "a b c d e f g h i j k l m n o p q r s t u v w x y z", 9, "400", MD)
    + T("alph4", LM, 442, "0 1 2 3 4 5 6 7 8 9  !  @  #  $  %  &amp;  *", 9, "400", MD)
    + L("pp-a2", LM, 454, LM + 560, 454, LT)
    # Right: Baloo 2
    + T("b2-lbl",  LM+620,  78,  "SECONDARY TYPEFACE (ACCENT / DISPLAY)", 8, "700", MD, ls=2)
    + T("b2-nm",   LM+620, 116,  "BALOO 2",    32, "800", TR, ls=2)
    + T("b2-aa",   LM+1060,  88,  "Aa",         64, "800", TR)
    + L("b2-r",    LM+620, 132,  RM, 132, LT, 0.75)
)
for i, (name, wt) in enumerate(WEIGHTS):
    ty_body += T(f"bw{i}", LM+620, 156 + i*36, f"{name} — Aa Bb Cc 123", 12, wt, DK)
USAGE = [
    ("Headings (H1–H3)",    "Poppins Bold / ExtraBold"),
    ("Subheadings (H4–H6)", "Poppins Medium / SemiBold"),
    ("Body Text",            "Poppins Regular"),
    ("Accents / Display",    "Baloo 2 SemiBold / Bold"),
]
ty_body += (
    L("us-top", LM, 476, RM, 476, LT, 1)
    + T("us-h1", LM,       494, "USAGE",   8, "700", MD, ls=2)
    + T("us-h2", LM + 400, 494, "TYPEFACE",8, "700", MD, ls=2)
)
for i, (sty, face) in enumerate(USAGE):
    uy = 514 + i * 28
    ty_body += (
        T(f"us{i}", LM,       uy, sty,  9, "400", MD)
        + T(f"uf{i}", LM+400, uy, face, 9, "700", DK)
        + L(f"ur{i}", LM,  uy+12, RM, uy+12, LT, 0.5)
    )
pages["05-typography"] = INNER(5, "Typography", ty_body)

# ── 06  VISUAL LANGUAGE ───────────────────────────────────────────────
ICON_SEC  = CW // 5
ICON_NMES = ["Bold", "Vibrant", "Friendly", "Modern", "Dynamic"]
ICON_COLS = [FG, MY, TR, FG, SO]
ICON_TC   = [WH, DK, WH, WH, WH]
ic_body   = (T("il-lbl", LM, 80, "ICON ILLUSTRATIONS", 8, "700", MD, ls=2)
             + L("il-r", LM, 90, RM, 90, LT))
for i, (nm, col, tc) in enumerate(zip(ICON_NMES, ICON_COLS, ICON_TC)):
    icx = LM + i * ICON_SEC + ICON_SEC // 2
    ic_body += (
        R(f"ic{i}", icx - 44, 104, 88, 88, col, 44)
        + T(f"it{i}", icx, 157, nm[0], 24, "800", tc, "middle")
        + T(f"il{i}", icx, 216, nm,    10, "700", DK, "middle")
    )

PAT_SZ    = 96
PAT_GAP   = 8
PAT_CNT   = 9
PAT_TOT   = PAT_CNT * PAT_SZ + (PAT_CNT - 1) * PAT_GAP
PAT_SX    = LM + (CW - PAT_TOT) // 2
PAT_Y     = 248
pt_body   = (T("pt-lbl", LM, 238, "PATTERNS &amp; GRAPHIC ELEMENTS", 8, "700", MD, ls=2)
             + L("pt-r",  LM, 248, RM, 248, LT))
for i in range(PAT_CNT):
    c1, c2, st = PDATA[i]
    px = PAT_SX + i * (PAT_SZ + PAT_GAP)
    pt_body += R(f"pt{i}", px, PAT_Y + 10, PAT_SZ, PAT_SZ, c1, 6)
    if st == "d":
        r = PAT_SZ // 3
        cx2, cy2 = px + PAT_SZ//2, PAT_Y + 10 + PAT_SZ//2
        pt_body += f'  <circle id="ptc{i}" cx="{cx2}" cy="{cy2}" r="{r}" fill="{c2}"/>\n'
    elif st == "x":
        pt_body += (f'  <line id="ptl{i}" x1="{px+16}" y1="{PAT_Y+PAT_SZ-6}" '
                    f'x2="{px+PAT_SZ-16}" y2="{PAT_Y+16}" stroke="{c2}" stroke-width="18"/>\n')
    else:
        pt_body += (f'  <path id="ptp{i}" d="M{px+PAT_SZ},{PAT_Y+10} '
                    f'A{PAT_SZ},{PAT_SZ} 0 0,0 {px},{PAT_Y+10+PAT_SZ} '
                    f'L{px+PAT_SZ},{PAT_Y+10+PAT_SZ} Z" fill="{c2}"/>\n')

SHP_Y  = 426
sh_body = (
    T("sh-lbl", LM, SHP_Y - 12, "SHAPES", 8, "700", MD, ls=2)
    + L("sh-r",  LM, SHP_Y - 2, RM, SHP_Y - 2, LT)
    + R("shp1",   LM,       SHP_Y + 8,  104, 104, FG,  16)
    + R("shp2",   LM+156,   SHP_Y + 32, 160,  60, TR,   6)
    + f'  <path id="shp3" d="M{LM+372},{SHP_Y+112} A76,76 0 0,0 {LM+524},{SHP_Y+112} Z" fill="{MY}"/>\n'
    + f'  <path id="shp4" d="M{LM+580},{SHP_Y+60} C{LM+616},{SHP_Y+38} {LM+652},{SHP_Y+82} '
      f'{LM+688},{SHP_Y+60} C{LM+724},{SHP_Y+38} {LM+760},{SHP_Y+82} '
      f'{LM+796},{SHP_Y+60}" fill="none" stroke="{FG}" stroke-width="5" stroke-linecap="round"/>\n'
    + T("sl1", LM + 56,  SHP_Y + 132, "Rounded Square", 8, "400", MD, "middle")
    + T("sl2", LM + 236, SHP_Y + 132, "Rectangle",      8, "400", MD, "middle")
    + T("sl3", LM + 448, SHP_Y + 132, "Half-Circle",    8, "400", MD, "middle")
    + T("sl4", LM + 688, SHP_Y + 132, "Wave",           8, "400", MD, "middle")
)
pages["06-visual-language"] = INNER(6, "Visual Language", ic_body + pt_body + sh_body)

# ── 07  PHOTOGRAPHY STYLE ─────────────────────────────────────────────
CHECKS_L = ["High contrast", "Warm tones", "Close-up details"]
CHECKS_R = ["Fresh ingredients", "Real moments", "Bold composition"]
ph_body  = (
    T("ps-i1", LM,  80, "Our photography is warm, vibrant and appetite-driven.", 10, "400", MD)
    + T("ps-i2", LM, 98, "Focus on real food, bold colours, strong lighting,",   10, "400", MD)
    + T("ps-i3", LM,116, "and authentic moments.",                                10, "400", MD)
    + L("ps-r",  LM,130, LM+440, 130, LT)
)
for i, chk in enumerate(CHECKS_L):
    py = 152 + i * 34
    ph_body += CHECK(f"pcl{i}", LM, py - 12, 18, FG) + T(f"pclt{i}", LM+26, py, chk, 9, "600", DK)
for i, chk in enumerate(CHECKS_R):
    py = 152 + i * 34
    ph_body += CHECK(f"pcr{i}", LM+224, py-12, 18, FG) + T(f"pcrt{i}", LM+250, py, chk, 9, "600", DK)
ph_body += (
    IMG("ph1",  LM+480,  72, 244, 212, "FOOD PHOTO", KB)
    + IMG("ph2",  LM+740,  72, 244, 212, "FOOD PHOTO", TR)
    + IMG("ph3",  LM+480, 300, 504, 248, "HERO FOOD PHOTO", KB)
)
pages["07-photography-style"] = INNER(7, "Photography Style", ph_body)

# ── 08  BRAND APPLICATION ─────────────────────────────────────────────
APP_COL_X = [LM, LM + 576]
APP_ROW_Y = [72, 352]
APP_ITEMS = [
    ("PACKAGING",   KB, "Cups, Boxes, Wrappers, Bags"),
    ("APPAREL",     FG, "T-Shirts, Caps, Aprons, Uniforms"),
    ("SIGNAGE",     FGD,"Exterior &amp; Interior Signage"),
    ("DIGITAL",     DB, "App, Website, Social Media"),
]
app_body = ""
for i, (label, col, desc) in enumerate(APP_ITEMS):
    ax = APP_COL_X[i % 2]
    ay = APP_ROW_Y[i // 2]
    app_body += (
        T(f"al{i}",   ax,      ay + 16, label,  9, "700", DK, ls=1.5)
        + R(f"alr{i}", ax,     ay + 22, 40, 2, SO, 1)
        + IMG(f"am{i}", ax,    ay + 32, 560, 232, f"{label} MOCKUP", col)
        + T(f"ad{i}",  ax,     ay + 32 + 232 + 14, desc, 8, "400", MD)
    )
pages["08-brand-application"] = INNER(8, "Brand Application", app_body)

# ── 09  DO'S &amp; DON'TS ─────────────────────────────────────────────
DO_W   = (CW - 3 * 16) // 4   # 272
DO_ITEMS   = ["Use the correct logo", "Maintain clear space",
               "Use approved colors",  "Ensure high contrast"]
DONT_ITEMS = ["Don't distort the logo", "Don't change the colors",
               "Don't rotate the logo",  "Don't add effects"]
dd_body = (
    R("do-bar",  LM,     72, 40, 40, FG, 4)
    + T("do-lbl", LM+52, 98, "DO",    14, "800", FG, ls=2)
    + L("do-r",   LM,   110, RM, 110, FG, 1.5)
)
for i, label in enumerate(DO_ITEMS):
    dx = LM + i * (DO_W + 16)
    dd_body += (
        R(f"dob{i}",   dx,     124, DO_W, 160, WH, 8, FG, 1.5)
        + R(f"dolg{i}", dx+12, 136, DO_W-24, 84, OW, 4)
        + T(f"dolm{i}", dx + DO_W//2, 185, "Quaké", 14, "800", FG, "middle")
        + CHECK(f"dok{i}", dx+12, 232, 20, FG)
        + T(f"dot{i}",  dx+40, 248, label, 8, "600", DK)
    )
dd_body += (
    R("dn-bar",   LM,    308, 40, 40, TR, 4)
    + T("dn-lbl", LM+52, 334, "DON'T",14, "800", TR, ls=2)
    + L("dn-r",   LM,    346, RM, 346, TR, 1.5)
)
for i, label in enumerate(DONT_ITEMS):
    dx = LM + i * (DO_W + 16)
    dd_body += (
        R(f"dnb{i}",   dx,    360, DO_W, 160, WH, 8, TR, 1.5)
        + R(f"dnlg{i}", dx+12, 372, DO_W-24, 84, OW, 4)
        + T(f"dnlm{i}", dx + DO_W//2, 421, "Quaké", 14, "800", FG, "middle")
        + CROSS(f"dnx{i}", dx+12, 468, 20, TR)
        + T(f"dnt{i}",  dx+40, 484, label, 8, "600", DK)
    )
pages["09-dos-and-donts"] = INNER(9, "Do's &amp; Don'ts", dd_body)

# ── 10  TONE OF VOICE ─────────────────────────────────────────────────
TOV_LINES = [
    "We're warm and welcoming",
    "We're bold and expressive",
    "We're real and honest",
    "We're confident and consistent",
]
PM_PAIRS = [
    ("Friendly",  "Professional", 160),
    ("Warm",      "Cool",         180),
    ("Bold",      "Subtle",       200),
    ("Playful",   "Serious",      140),
    ("Loud",      "Quiet",        120),
]
tov_body = (
    T("tov-1",  LM,     104, "WARM. BOLD.",        50, "800", TR, ls=-1)
    + T("tov-2", LM,    156, "CONFIDENT. REAL.",   50, "800", TR, ls=-1)
    + L("tov-r", LM,    172, LM + 740, 172, TR, 2)
    + T("tov-i1",LM,    200, "We speak like a friend who knows great food.",     10, "400", MD)
    + T("tov-i2",LM,    218, "Our tone is upbeat, honest and full of flavour.",  10, "400", MD)
    + L("tov-r2",LM,    234, LM + 560, 234, LT)
)
for i, line in enumerate(TOV_LINES):
    ty = 260 + i * 44
    tov_body += CHECK(f"tv{i}", LM, ty - 12, 20, FG) + T(f"tvt{i}", LM+32, ty, line, 11, "600", DK)

tov_body += (
    R("pm",    LM+700,  72, 436, 468, WH, 8, LT)
    + T("pm-h",LM+918, 112, "BRAND VOICE", 9, "700", MD, "middle", ls=2)
    + L("pm-r",LM+716, 124, RM - 16, 124, LT)
)
for i, (lft, rgt, fw) in enumerate(PM_PAIRS):
    py = 152 + i * 60
    tov_body += (
        T(f"pml{i}",  LM+716,      py + 14, lft,  9, "700", DK)
        + R(f"pmb{i}", LM+856,     py,      192, 20, LT, 10)
        + R(f"pmf{i}", LM+856,     py,      fw,  20, FG, 10)
        + T(f"pmr{i}", RM - 16,    py + 14, rgt,  9, "700", DK, "end")
    )
pages["10-tone-of-voice"] = INNER(10, "Tone of Voice", tov_body)

# ── 11  BRAND SUMMARY & THANK YOU ─────────────────────────────────────
pages["11-brand-summary"] = SVG(
    BG()
    + R("top-bar", 0, 0, W, 6, FG)
    # Left: summary text
    + T("bs-h",    LM,  80, "10.",            9, "800", TR)
    + T("bs-t",    LM+36,80, "BRAND SUMMARY", 9, "800", DK, ls=2)
    + L("bs-r",    LM,  92, LM + 500, 92, LT)
    + LB("bs-b",   LM, 108,
         [440,500,480,500,440,500,480,440,500,480,440,500,480],
         g=16, bh=8)
    + T("ty-1",    LM, 336, "THANK",         60, "800", MY, ls=-1)
    + T("ty-2",    LM, 400, "YOU!",          60, "800", MY, ls=-1)
    + R("ty-ln",   LM, 414, 164, 4,  SO, 2)
    + T("ty-s1",   LM, 444, "Quaké Paraná is more than a meal.",         10, "400", MD)
    + T("ty-s2",   LM, 462, "It's a bold, flavorful experience",         10, "400", MD)
    + T("ty-s3",   LM, 480, "served with warmth and speed.",             10, "400", MD)
    + T("ty-s4",   LM, 514, "This identity ensures we show up",          10, "400", MD)
    + T("ty-s5",   LM, 532, "consistently, everywhere.",                 10, "400", MD)
    # Right: decorative circles
    + f'  <circle id="dc1" cx="972"  cy="300" r="212" fill="{TR}"/>\n'
    + f'  <circle id="dc2" cx="1140" cy="430" r="168" fill="{MY}"/>\n'
    + f'  <circle id="dc3" cx="860"  cy="470" r="124" fill="{FG}"/>\n'
    + f'  <circle id="dc4" cx="1180" cy="248" r="84"  fill="{SO}"/>\n'
    + f'  <circle id="dc5" cx="760"  cy="296" r="60"  fill="{DB}"/>\n'
    # Footer
    + PSTRIP("ftr-pat", 0, H - 36, W, 36)
    + T("ftr-l", LM, H-13,
        "BRAND GUIDELINES  |  VERSION 1.0  |  2024", 8, "600", WH, ls=1)
    + T("ftr-r", RM, H-13, "QUAKÉ PARANÁ", 8, "700", MY, "end", ls=2)
)

# ── Write all files ───────────────────────────────────────────────────
for name, content in sorted(pages.items()):
    path = os.path.join(OUT, f"page-{name}.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  ✓  page-{name}.svg")

print(f"\n✅  {len(pages)} pages → {OUT}/")
