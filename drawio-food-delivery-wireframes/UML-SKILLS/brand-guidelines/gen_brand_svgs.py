#!/usr/bin/env python3
"""Brand Guidelines SVG Template Generator — 32 pages"""
import os

OUT = "/mnt/user-data/outputs/brand-guidelines"
os.makedirs(OUT, exist_ok=True)

W, H = 1280, 720
FF   = "'Helvetica Neue', Helvetica, Arial, sans-serif"
LM   = 72
RM   = W - 72

# ── Palette ──────────────────────────────────────────────────────────
G   = "#556B4E"
GD  = "#3E5139"
GL  = "#8CA47A"
GP  = "#D4E0CE"
WH  = "#FFFFFF"
DK  = "#1A1A1A"
MD  = "#6B6B6B"
LT  = "#DDDDDD"
VL  = "#F5F5F5"
RED = "#C04444"

# ── Base helpers ─────────────────────────────────────────────────────
def SVG(body):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
        + body
        + '</svg>\n'
    )

def BG(c=WH):
    return f'  <rect id="bg" width="{W}" height="{H}" fill="{c}"/>\n'

def T(tid, x, y, txt, sz=11, wt="400", col=DK, anc="start", ls=0):
    ls_a = f' letter-spacing="{ls}"' if ls else ""
    return f'  <text id="{tid}" x="{x}" y="{y}" font-family="{FF}" font-size="{sz}" font-weight="{wt}" fill="{col}" text-anchor="{anc}"{ls_a}>{txt}</text>\n'

def R(rid, x, y, w, h, col=WH, rx=0, sc=None, sw=0.5):
    st = f' stroke="{sc}" stroke-width="{sw}"' if sc else ""
    return f'  <rect id="{rid}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" rx="{rx}"{st}/>\n'

def L(lid, x1, y1, x2, y2, col=LT, sw=0.5):
    return f'  <line id="{lid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}"/>\n'

def C(cid, cx, cy, r, col=G, fc="none", sw=0.75, op=1):
    op_a = f' opacity="{op}"' if op < 1 else ""
    return f'  <circle id="{cid}" cx="{cx}" cy="{cy}" r="{r}" fill="{fc}" stroke="{col}" stroke-width="{sw}"{op_a}/>\n'

def IMG(iid, x, y, w, h, lbl="IMAGE"):
    cx, cy = x + w // 2, y + h // 2
    return (
        f'  <g id="{iid}">\n'
        f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{VL}" rx="2" stroke="{LT}" stroke-width="0.5"/>\n'
        f'    <line x1="{x}" y1="{y}" x2="{x+w}" y2="{y+h}" stroke="{LT}" stroke-width="0.75"/>\n'
        f'    <line x1="{x+w}" y1="{y}" x2="{x}" y2="{y+h}" stroke="{LT}" stroke-width="0.75"/>\n'
        f'    <text x="{cx}" y="{cy+4}" font-family="{FF}" font-size="9" fill="{MD}" text-anchor="middle">{lbl}</text>\n'
        f'  </g>\n'
    )

def LBLOCKS(bid, x, y, widths, gap=15, bh=8, col=LT):
    out = [f'  <g id="{bid}">\n']
    for i, w in enumerate(widths):
        out.append(f'    <rect x="{x}" y="{y + i*gap}" width="{w}" height="{bh}" rx="1.5" fill="{col}"/>\n')
    out.append('  </g>\n')
    return "".join(out)

def HDR(n, sec="BRAND GUIDELINES"):
    return (
        f'  <g id="header">\n'
        f'    <text x="{LM}" y="36" font-family="{FF}" font-size="8" fill="{MD}" letter-spacing="2.5">{sec}</text>\n'
        f'    <text x="{RM}" y="36" font-family="{FF}" font-size="8" fill="{MD}" text-anchor="end">{str(n).zfill(2)}</text>\n'
        f'    <line x1="{LM}" y1="48" x2="{RM}" y2="48" stroke="{LT}" stroke-width="0.5"/>\n'
        f'  </g>\n'
    )

def FTR():
    return (
        f'  <g id="footer">\n'
        f'    <line x1="{LM}" y1="{H-44}" x2="{RM}" y2="{H-44}" stroke="{LT}" stroke-width="0.5"/>\n'
        f'    <text x="{LM}" y="{H-26}" font-family="{FF}" font-size="8" fill="{MD}" letter-spacing="1.5">YOUR COMPANY</text>\n'
        f'    <text x="{RM}" y="{H-26}" font-family="{FF}" font-size="8" fill="{MD}" text-anchor="end" letter-spacing="1">BRAND GUIDELINES 2024</text>\n'
        f'  </g>\n'
    )

def INNER(n, sec_lbl, title, body, subtitle=""):
    sub = T("subtitle", LM, 130, subtitle, 11, "400", MD) if subtitle else ""
    return SVG(
        BG()
        + R("accent-bar", 0, 0, 6, H, G)
        + HDR(n, sec_lbl)
        + T("pg-title", LM, 108, title, 24, "700", DK, ls=-0.5)
        + sub
        + L("title-accent", LM, 142, LM + 52, 142, G, 2)
        + body
        + FTR()
    )

def SECT(n, title, d1="", d2="", d3=""):
    nz  = str(n).zfill(2)
    LW  = 380
    d1  = d1 or "This section outlines the standards and guidelines"
    d2  = d2 or "for consistent use across all brand applications"
    d3  = d3 or "and communications."
    return SVG(
        BG()
        + R("panel",    0, 0,      LW, H,  G)
        + R("panel-dk", 0, H - 56, LW, 56, GD)
        + f'  <text id="ghost" x="-20" y="500" font-family="{FF}" font-size="280" '
          f'font-weight="800" fill="{WH}" opacity="0.05">{nz}</text>\n'
        + T("logo",       40, 56,       "&#x25B2;  YOUR BRAND", 10, "700", WH, ls=1.5)
        + T("sect-num",   40, H - 32,   nz,                     12, "700", WH)
        + L("sect-rule",  40, H - 18,   140,        H - 18,     "rgba(255,255,255,0.3)")
        + T("sect-title", 40, H - 4,    f"{title}.", 22, "700", WH, ls=-0.5)
        + T("r-eyebrow",  LW + 56, 220, f"SECTION {nz}",  8, "400", MD, ls=3)
        + T("r-heading",  LW + 56, 296, f"{title}.",      52, "800", DK, ls=-2)
        + L("r-rule",     LW + 56, 318, LW + 300, 318)
        + T("r-d1", LW + 56, 354, d1, 11, "400", MD)
        + T("r-d2", LW + 56, 372, d2, 11, "400", MD)
        + T("r-d3", LW + 56, 390, d3, 11, "400", MD)
        + FTR()
    )

# ════════════════════════════════════════════════════════════════════
# PAGE DEFINITIONS
# ════════════════════════════════════════════════════════════════════
pages = {}

# ── 01  COVER ────────────────────────────────────────────────────────
dots = "".join(
    f'<circle cx="{880 + j*22}" cy="{80 + i*22}" r="2" fill="{G}"/>'
    for i in range(7) for j in range(7)
)
pages["01-cover"] = SVG(
    BG()
    + R("panel",    0, 0,      440, H,  G)
    + R("panel-dk", 0, H - 56, 440, 56, GD)
    + C("deco1", 330, H - 90, 190, GL, "none", 0.75, 0.18)
    + C("deco2", 330, H - 90, 110, GL, "none", 0.5,  0.12)
    + T("logo",      48, 56,  "&#x25B2;  YOUR BRAND",       10, "700", WH, ls=1.5)
    + T("t1",        48, 264, "Brand",                       72, "800", WH, ls=-2)
    + T("t2",        48, 344, "Guide",                       72, "800", WH, ls=-2)
    + T("t3",        48, 424, "lines",                       72, "800", WH, ls=-2)
    + L("t-rule", 48, 448, 260, 448, "rgba(255,255,255,0.28)")
    + T("tagline",   48, 472, "COMPANY PROFILE", 9,  "400", "rgba(255,255,255,0.55)", ls=3)
    + T("conf",      48, H-34,"CONFIDENTIAL",    8,  "400", "rgba(255,255,255,0.35)", ls=2)
    + T("info-hdr",  508, 108, "DOCUMENT INFORMATION", 8, "400", MD, ls=3)
    + L("i-rule",    508, 122, 820, 122)
    + T("co-lbl",    508, 172, "Company",                   9,  "400", MD)
    + T("co-val",    508, 196, "Your Company Name",         16, "600", DK)
    + T("pr-lbl",    508, 248, "Project",                   9,  "400", MD)
    + T("pr-val",    508, 272, "Brand Identity Guidelines", 16, "600", DK)
    + T("vr-lbl",    508, 324, "Version",                   9,  "400", MD)
    + T("vr-val",    508, 348, "Version 1.0 — 2024",        16, "600", DK)
    + T("by-lbl",    508, 400, "Prepared by",               9,  "400", MD)
    + T("by-val",    508, 424, "Design Team",               16, "600", DK)
    + T("ct-lbl",    508, 476, "Contact",                   9,  "400", MD)
    + T("ct-val",    508, 500, "hello@yourcompany.com",     16, "600", DK)
    + f'  <g id="dot-grid" opacity="0.1">{dots}</g>\n'
)

# ── 02  WELCOME MESSAGE ───────────────────────────────────────────────
pages["02-welcome"] = INNER(2, "WELCOME", "Welcome Message",
    T("greeting", LM, 176, "Dear Partners &amp; Collaborators,", 13, "600", DK)
    + R("accent-greeting", LM, 181, 52, 2, G, 1)
    + LBLOCKS("body", LM, 200, [420,440,400,440,420,440,400,440,420,420,440,400,440,420,440], gap=18, bh=9)
    + T("sig-name",  LM, 548, "First Last Name",          13, "700", DK)
    + T("sig-title", LM, 568, "Chief Executive Officer",  9,  "400", MD)
    + L("sig-r",     LM, 582, LM + 168, 582)
    + T("sig-co",    LM, 600, "COMPANY NAME", 8, "400", MD, ls=1.5)
    + IMG("photo", 680, 72, 260, 340, "PORTRAIT PHOTO")
    + T("photo-cap", 810, 432, "Name &amp; Title", 9, "400", MD, "middle")
)

# ── 03  TABLE OF CONTENTS ─────────────────────────────────────────────
toc = [
    ("01","Logo",            "Identity &amp; usage rules",       "05"),
    ("02","Typography",      "Fonts &amp; type hierarchy",        "09"),
    ("03","Color System",    "Brand color palette",               "13"),
    ("04","Stationery",      "Printed materials",                 "17"),
    ("05","Iconography",     "Icon style &amp; library",          "21"),
    ("06","Logo Placement",  "Application guidelines",            "25"),
    ("07","Image &amp; Brand","Photography &amp; imagery",        "29"),
]
toc_body = ""
for i, (num, title, desc, pg) in enumerate(toc):
    col_x = LM if i < 4 else LM + 560
    by    = 176 + (i % 4) * 112
    toc_body += (
        T(f"tn{num}", col_x,       by,      num,   9,  "700", G,  ls=1)
        + T(f"tt{num}", col_x,     by + 22, title, 15, "700", DK)
        + T(f"td{num}", col_x,     by + 42, desc,  9,  "400", MD)
        + L(f"tr{num}", col_x,     by + 56, col_x + 280, by + 56)
        + T(f"tp{num}", col_x+280, by + 22, pg,    11, "600", MD, "end")
    )
pages["03-toc"] = INNER(3, "OVERVIEW", "Table of Contents", toc_body)

# ── 04  ABOUT US ──────────────────────────────────────────────────────
col_w = [192, 192, 192, 192]
col_x = [LM, LM + 240, LM + 480, LM + 720]
hdrs  = ["Our Story", "Our Vision", "Our Mission", "Our Values"]
about_body = ""
for i in range(4):
    about_body += (
        T(f"ab-hd{i}", col_x[i], 176, hdrs[i], 11, "700", DK)
        + L(f"ab-r{i}", col_x[i], 190, col_x[i] + col_w[i], 190, G, 1.5)
        + LBLOCKS(f"ab-b{i}", col_x[i], 204, [col_w[i], col_w[i]-12, col_w[i], col_w[i]-20,
                                                col_w[i], col_w[i]-8, col_w[i], col_w[i]-16,
                                                col_w[i], col_w[i]-12, col_w[i]], gap=16, bh=8)
    )
pages["04-about"] = INNER(4, "INTRODUCTION", "About Us", about_body)

# ── 05  SECTION — LOGO ────────────────────────────────────────────────
pages["05-section-logo"] = SECT(1, "Logo",
    "This section outlines standards for our",
    "logo usage, spacing, backgrounds, and",
    "all permitted colour combinations."
)

# ── 06  LOGO BACKGROUND ───────────────────────────────────────────────
bgs   = [WH, VL, DK, G]
bsc   = [LT, LT, None, None]
logos = ["&#x25B2; LOGO", "&#x25B2; LOGO", "&#x25B2; LOGO", "&#x25B2; LOGO"]
lcs   = [DK, DK, WH, WH]
lbls  = ["White", "Off White", "Near Black", "Brand Green"]
logo_bg_body = (
    T("desc", LM, 168, "Our logo may only appear on the following approved backgrounds.", 11, "400", MD)
)
for i in range(4):
    bx = LM + i * 280
    sc = bsc[i]
    logo_bg_body += R(f"bg{i}", bx, 200, 248, 160, bgs[i], 3, sc)
    logo_bg_body += T(f"lm{i}", bx + 124, 285, logos[i], 14, "700", lcs[i], "middle")
    logo_bg_body += T(f"ll{i}", bx + 124, 382, lbls[i], 9, "400", MD, "middle")

logo_bg_body += (
    T("dnt-hdr", LM, 412, "Incorrect Usage", 10, "700", DK)
    + R("dnt-bar", LM, 425, 36, 2, RED, 1)
    + R("ic1", LM,       440, 192, 120, "#E8E0D0", 3, LT)
    + R("ic2", LM + 216, 440, 192, 120, "#FFEEEE", 3, LT)
    + R("ic3", LM + 432, 440, 192, 120, "#DDEEFF", 3, LT)
    + T("im1", LM + 96,       505, "&#x25B2; LOGO", 12, "700", "#A09080", "middle")
    + T("im2", LM + 96 + 216, 505, "&#x25B2; LOGO", 12, "700", "#CC9988", "middle")
    + T("im3", LM + 96 + 432, 505, "&#x25B2; LOGO", 12, "700", "#88AACC", "middle")
    + T("ix1", LM + 96,       578, "&#x2715;  Pattern background", 8, "400", RED, "middle")
    + T("ix2", LM + 96 + 216, 578, "&#x2715;  Unapproved colour",  8, "400", RED, "middle")
    + T("ix3", LM + 96 + 432, 578, "&#x2715;  Insufficient contrast",8, "400", RED, "middle")
)
pages["06-logo-background"] = INNER(6, "01  LOGO", "Logo Background", logo_bg_body)

# ── 07  LOGO DESIGN ───────────────────────────────────────────────────
pages["07-logo-design"] = INNER(7, "01  LOGO", "Logo Design",
    T("desc", LM, 168, "The master logo consists of the logomark and wordmark, used together.", 11, "400", MD)
    + IMG("logo-main", LM, 192, 480, 252, "PRIMARY LOGO")
    + T("var-hdr",  LM + 544, 192, "Logo Variations", 10, "700", DK)
    + L("var-rule", LM + 544, 206, LM + 744, 206, G, 1.5)
    + IMG("logo-v1", LM + 544, 224, 248, 100, "HORIZONTAL")
    + IMG("logo-v2", LM + 544, 344, 248, 100, "STACKED")
    + T("cs-hdr",  LM,       472, "Clear Space",   10, "700", DK)
    + L("cs-rule", LM,       485, LM + 120, 485, G, 1.5)
    + T("cs-d1",   LM,       505, "Maintain clear space equal to", 9, "400", MD)
    + T("cs-d2",   LM,       521, "the height of the mark.",       9, "400", MD)
    + T("ms-hdr",  LM + 280, 472, "Minimum Size",  10, "700", DK)
    + L("ms-rule", LM + 280, 485, LM + 400, 485, G, 1.5)
    + T("ms-d1",   LM + 280, 505, "Digital: 24px height min.", 9, "400", MD)
    + T("ms-d2",   LM + 280, 521, "Print:   8mm height min.",  9, "400", MD)
    + T("fo-hdr",  LM + 544, 472, "File Formats",  10, "700", DK)
    + L("fo-rule", LM + 544, 485, LM + 744, 485, G, 1.5)
    + T("fo-d1",   LM + 544, 505, "SVG — Digital / Web",      9, "400", MD)
    + T("fo-d2",   LM + 544, 521, "EPS — Print / Vendors",    9, "400", MD)
    + T("fo-d3",   LM + 544, 537, "PNG — Social / Screens",   9, "400", MD)
)

# ── 08  BRAND LOGO IDENTIFICATION ────────────────────────────────────
pages["08-logo-identification"] = INNER(8, "01  LOGO", "Brand Logo Identification",
    T("desc", LM, 168, "Understanding the logo anatomy and its individual components.", 11, "400", MD)
    + IMG("logo-ann", LM, 192, 560, 296, "LOGO ANATOMY / ANNOTATED")
    + T("c-hdr",  LM + 620, 192, "Components", 10, "700", DK)
    + L("c-rule", LM + 620, 206, LM + 820, 206, G, 1.5)
    + T("c1-n",   LM + 620, 252, "A",                         14, "700", G)
    + T("c1-t",   LM + 644, 252, "Logomark / Symbol",         10, "700", DK)
    + T("c1-d",   LM + 644, 268, "The primary graphic mark",  9,  "400", MD)
    + L("c1-r",   LM + 620, 284, LM + 820, 284)
    + T("c2-n",   LM + 620, 312, "B",                         14, "700", G)
    + T("c2-t",   LM + 644, 312, "Wordmark / Brand Name",     10, "700", DK)
    + T("c2-d",   LM + 644, 328, "Primary typeface, brand weight", 9, "400", MD)
    + L("c2-r",   LM + 620, 344, LM + 820, 344)
    + T("c3-n",   LM + 620, 372, "C",                         14, "700", G)
    + T("c3-t",   LM + 644, 372, "Tagline (optional)",        10, "700", DK)
    + T("c3-d",   LM + 644, 388, "Used in extended identity only", 9, "400", MD)
    + L("c3-r",   LM + 620, 404, LM + 820, 404)
    + T("c4-n",   LM + 620, 432, "D",                         14, "700", G)
    + T("c4-t",   LM + 644, 432, "Clear Space Zone",          10, "700", DK)
    + T("c4-d",   LM + 644, 448, "Protected buffer around logo", 9, "400", MD)
    + L("c4-r",   LM + 620, 464, LM + 820, 464)
    + T("c5-n",   LM + 620, 492, "E",                         14, "700", G)
    + T("c5-t",   LM + 644, 492, "Colour Lockup",             10, "700", DK)
    + T("c5-d",   LM + 644, 508, "Approved colour versions",  9,  "400", MD)
)

# ── 09  SECTION — TYPOGRAPHY ─────────────────────────────────────────
pages["09-section-typography"] = SECT(2, "Typography",
    "Our typographic system establishes a",
    "clear visual hierarchy that communicates",
    "confidence and precision."
)

# ── 10  PRIMARY FONT ──────────────────────────────────────────────────
weights = [("Extra Bold", "800"), ("Bold", "700"), ("Semi Bold", "600"),
           ("Regular", "400"), ("Light", "300")]
typo_body = (
    T("desc", LM, 168, "Our primary typeface is used for headlines, display text, and key messaging.", 11, "400", MD)
    + T("big-aa", LM, 400, "Aa", 168, "800", DK, ls=-5)
    + T("fn-lbl",  LM + 480, 200, "PRIMARY TYPEFACE", 8, "400", MD, ls=3)
    + T("fn-name", LM + 480, 240, "Your Display Font", 28, "700", DK, ls=-0.5)
    + L("fn-rule", LM + 480, 260, LM + 740, 260)
)
for i, (name, wt) in enumerate(weights):
    typo_body += T(f"w{i}", LM + 480, 296 + i * 28, f"{name} — Aa Bb Cc Dd", 13, wt, DK)
typo_body += (
    L("alpha-r1", LM, 436, LM + 1136, 436)
    + T("alpha-uc", LM, 456, "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z", 11, "400", MD)
    + T("alpha-lc", LM, 474, "a b c d e f g h i j k l m n o p q r s t u v w x y z", 11, "400", MD)
    + T("nums",     LM, 492, "0 1 2 3 4 5 6 7 8 9   !  @  #  $  %  &amp;  *  (  )", 11, "400", MD)
    + L("alpha-r2", LM, 504, LM + 1136, 504)
)
pages["10-typography-primary"] = INNER(10, "02  TYPOGRAPHY", "Company Primary Font", typo_body)

# ── 11  SECONDARY FONT ────────────────────────────────────────────────
weights2 = [("Bold", "700"), ("Regular", "400"), ("Italic Regular", "400"), ("Light", "300")]
typo2 = (
    T("desc", LM, 168, "Our secondary typeface complements the primary and is used for body copy and UI.", 11, "400", MD)
    + T("big-aa", LM, 400, "Aa", 168, "400", MD, ls=-5)
    + T("fn-lbl",  LM + 480, 200, "SECONDARY TYPEFACE", 8, "400", MD, ls=3)
    + T("fn-name", LM + 480, 240, "Your Body Font",      28, "400", DK, ls=-0.5)
    + L("fn-rule", LM + 480, 260, LM + 740, 260)
)
for i, (name, wt) in enumerate(weights2):
    typo2 += T(f"w{i}", LM + 480, 296 + i * 28, f"{name} — Aa Bb Cc Dd", 13, wt, DK)
typo2 += (
    L("alpha-r1", LM, 436, LM + 1136, 436)
    + T("alpha-uc", LM, 456, "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z", 11, "400", MD)
    + T("alpha-lc", LM, 474, "a b c d e f g h i j k l m n o p q r s t u v w x y z", 11, "400", MD)
    + T("nums",     LM, 492, "0 1 2 3 4 5 6 7 8 9   !  @  #  $  %  &amp;  *  (  )", 11, "400", MD)
    + L("alpha-r2", LM, 504, LM + 1136, 504)
)
pages["11-typography-secondary"] = INNER(11, "02  TYPOGRAPHY", "Company Secondary Font", typo2)

# ── 12  TYPOGRAPHY SCALE ─────────────────────────────────────────────
ts_items = [
    ("H1 — Display / 48pt / Extra Bold",  "Heading One",   38, "800", -1),
    ("H2 — Title / 32pt / Bold",          "Heading Two",   28, "700", -0.5),
    ("H3 — Section / 22pt / Semi Bold",   "Heading Three", 20, "600", 0),
    ("Body / 11pt / Regular",             None,            11, "400", 0),
    ("Caption / 9pt / Regular",           None,             9, "400", 0),
]
ts_body = L("ts-top", LM, 164, LM + 560, 164)
ts_y = 168
for lbl, sample, sz, wt, ls in ts_items:
    ts_body += T(f"ts-lbl-{sz}", LM, ts_y + 18, lbl, 8, "400", MD)
    if sample:
        ts_body += T(f"ts-s-{sz}", LM, ts_y + 18 + sz + 4, sample, sz, wt, DK, ls=ls)
        ts_y += 24 + sz + 14
    else:
        ts_body += LBLOCKS(f"ts-b-{sz}", LM, ts_y + 24, [480, 560, 520, 560], gap=16, bh=sz-2,
                           col=LT if sz > 9 else G)
        ts_y += 24 + 5 * 16 + 8
    ts_body += L(f"ts-r-{sz}", LM, ts_y, LM + 560, ts_y)

ts_body += (
    T("fp-hdr",   LM + 624, 164, "Type Hierarchy &amp; Pairing", 10, "700", DK)
    + L("fp-rule",  LM + 624, 178, LM + 844, 178, G, 1.5)
    + T("fp-l1",    LM + 624, 216, "PRIMARY",   8, "400", MD, ls=2)
    + T("fp-v1",    LM + 624, 244, "Headlines", 22, "800", DK, ls=-0.5)
    + T("fp-u1",    LM + 624, 264, "H1, H2, Display, Key messaging", 9, "400", MD)
    + L("fp-d1",    LM + 624, 284, LM + 844, 284)
    + T("fp-l2",    LM + 624, 312, "SECONDARY", 8, "400", MD, ls=2)
    + T("fp-v2",    LM + 624, 340, "Body Copy", 22, "400", DK)
    + T("fp-u2",    LM + 624, 360, "H3, body, captions, labels",  9, "400", MD)
    + L("fp-d2",    LM + 624, 380, LM + 844, 380)
    + T("sp-hdr",   LM + 624, 408, "Line Height &amp; Spacing",   10, "700", DK)
    + L("sp-rule",  LM + 624, 422, LM + 844, 422, G, 1.5)
    + T("sp-1",     LM + 624, 448, "Display:  1.1x",  9, "400", MD)
    + T("sp-2",     LM + 624, 466, "Heading:  1.25x", 9, "400", MD)
    + T("sp-3",     LM + 624, 484, "Body:     1.6x",  9, "400", MD)
    + T("sp-4",     LM + 624, 502, "Caption:  1.4x",  9, "400", MD)
    + T("ltr-hdr",  LM + 868, 164, "Letter Spacing",  10, "700", DK)
    + L("ltr-rule", LM + 868, 178, LM + 1068, 178, G, 1.5)
    + T("ltr-1",    LM + 868, 216, "Display:  -2 to -4",   9, "400", MD)
    + T("ltr-2",    LM + 868, 234, "Heading:  -0.5 to -1", 9, "400", MD)
    + T("ltr-3",    LM + 868, 252, "Body:     0",           9, "400", MD)
    + T("ltr-4",    LM + 868, 270, "Label:    +1.5 to +3", 9, "400", MD)
)
pages["12-typography-scale"] = INNER(12, "02  TYPOGRAPHY", "Typography", ts_body)

# ── 13  SECTION — COLOR ───────────────────────────────────────────────
pages["13-section-color"] = SECT(3, "Colour",
    "Our colour palette reflects our brand",
    "personality — natural, considered, and",
    "precise in its application."
)

# ── 14  PRIMARY COLORS ────────────────────────────────────────────────
pri_colors = [
    (G,   "Brand Green",  "PRIMARY",  "#556B4E", "C20 M0 Y27 K58"),
    (DK,  "Near Black",   "DARK",     "#1A1A1A", "C0 M0 Y0 K90"),
    (WH,  "Pure White",   "LIGHT",    "#FFFFFF",  "C0 M0 Y0 K0"),
    (MD,  "Mid Grey",     "NEUTRAL",  "#6B6B6B", "C0 M0 Y0 K58"),
]
pri_body = T("desc", LM, 168, "Our primary brand colours form the foundation of our visual identity.", 11, "400", MD)
for i, (col, name, role, hex_v, cmyk) in enumerate(pri_colors):
    bx = LM + i * 290
    sc = LT if col in [WH] else None
    pri_body += (
        R(f"sw{i}", bx, 196, 258, 188, col, 3, sc)
        + T(f"sr{i}", bx, 402, role, 8, "400", MD, ls=1.5)
        + T(f"sn{i}", bx, 422, name, 13, "700", DK)
        + T(f"sh{i}", bx, 440, hex_v, 9, "400", MD)
        + T(f"sc{i}", bx, 458, f"CMYK: {cmyk}", 8, "400", MD)
    )
pages["14-color-primary"] = INNER(14, "03  COLOR SYSTEM", "Company Primary Colors", pri_body)

# ── 15  SECONDARY COLORS ─────────────────────────────────────────────
sec_colors = [
    (GL,  "Sage Light",   "SECONDARY", "#8CA47A", "C15 M0 Y26 K35"),
    (GP,  "Pale Green",   "TINT",      "#D4E0CE", "C7 M0 Y10 K13"),
    (GD,  "Deep Forest",  "SHADE",     "#3E5139", "C24 M0 Y30 K68"),
    (VL,  "Off White",    "SURFACE",   "#F5F5F5", "C0 M0 Y0 K4"),
]
sec_body = T("desc", LM, 168, "Secondary palette supports and complements primary colours in extended applications.", 11, "400", MD)
for i, (col, name, role, hex_v, cmyk) in enumerate(sec_colors):
    bx = LM + i * 290
    sc = LT if col in [GP, VL] else None
    sec_body += (
        R(f"sw{i}", bx, 196, 258, 188, col, 3, sc)
        + T(f"sr{i}", bx, 402, role, 8, "400", MD, ls=1.5)
        + T(f"sn{i}", bx, 422, name, 13, "700", DK)
        + T(f"sh{i}", bx, 440, hex_v, 9, "400", MD)
        + T(f"sc{i}", bx, 458, f"CMYK: {cmyk}", 8, "400", MD)
    )
sec_body += (
    f'  <defs>\n'
    f'    <linearGradient id="g-grad" x1="0" y1="0" x2="1" y2="0">\n'
    f'      <stop offset="0%"   stop-color="{GD}"/>\n'
    f'      <stop offset="50%"  stop-color="{G}"/>\n'
    f'      <stop offset="100%" stop-color="{GP}"/>\n'
    f'    </linearGradient>\n'
    f'  </defs>\n'
    f'  <rect x="{LM}" y="482" width="1136" height="44" fill="url(#g-grad)" rx="3"/>\n'
    + T("grad-lbl", LM, 548, "Brand colour gradient — for approved gradient applications only", 9, "400", MD)
)
pages["15-color-secondary"] = INNER(15, "03  COLOR SYSTEM", "Company Secondary Colors", sec_body)

# ── 16  ANALOGOUS COLOR ───────────────────────────────────────────────
ratio_items = [
    (G,  "Brand Green",   "Primary",        "60%", 220),
    (DK, "Near Black",    "Secondary",      "30%", 146),
    (MD, "Mid Grey",      "Supporting",     "7%",   34),
    (GP, "Pale Green",    "Accent / Tint",  "3%",   15),
]
ana_body = T("desc", LM, 168, "Colour usage ratios and combination guidelines for all brand communications.", 11, "400", MD)
ana_body += IMG("pie", LM, 196, 296, 296, "COLOR RATIO CHART")
ana_body += T("rt-hdr",  LM + 360, 196, "Colour Usage Ratio", 10, "700", DK)
ana_body += L("rt-rule", LM + 360, 210, LM + 580, 210, G, 1.5)
for i, (col, name, role, pct, bar_w) in enumerate(ratio_items):
    ry = 236 + i * 72
    ana_body += (
        R(f"rb{i}", LM + 360, ry, bar_w, 24, col, 2)
        + T(f"rp{i}", LM + 360 + bar_w + 16, ry + 17, pct, 11, "700", DK)
        + T(f"rn{i}", LM + 360, ry + 42, f"{name} — {role}", 9, "400", MD)
    )
sw_colors = [(G, "Brand Green", "#556B4E"), (GL, "Sage Light", "#8CA47A"),
             (GP, "Pale Green",  "#D4E0CE"), (GD, "Deep Forest","#3E5139")]
for i, (col, name, hex_v) in enumerate(sw_colors):
    sx = LM + 660
    sy = 196 + i * 96
    ana_body += (
        R(f"as{i}", sx, sy, 96, 72, col, 3)
        + T(f"an{i}", sx + 112, sy + 22, name,  10, "700", DK)
        + T(f"ah{i}", sx + 112, sy + 40, hex_v,  9, "400", MD)
    )
ana_body += T("an-note1", LM + 360, 538, "These ratios apply to print and digital", 9, "400", MD)
ana_body += T("an-note2", LM + 360, 556, "materials across all brand channels.",    9, "400", MD)
pages["16-color-analogous"] = INNER(16, "03  COLOR SYSTEM", "Analogous Color", ana_body)

# ── 17  SECTION — STATIONERY ──────────────────────────────────────────
pages["17-section-stationery"] = SECT(4, "Stationery",
    "Standards for printed stationery ensure",
    "consistent brand representation across",
    "all physical touchpoints."
)

# ── 18  STATIONERY — BUSINESS CARD ───────────────────────────────────
pages["18-stationery-bizcard"] = INNER(18, "04  STATIONERY", "Stationery Guideline",
    T("sub-hdr", LM, 168, "Business Card", 11, "400", MD)
    + T("lbl-f",  LM,       208, "Front", 9, "400", MD, ls=1)
    + R("cf",     LM,       220, 360, 220, WH, 3, LT)
    + R("cf-top", LM,       220, 360, 52,  G, 3)
    + T("cf-l",   LM + 16,  254, "&#x25B2;  BRAND", 10, "700", WH)
    + T("cf-n",   LM + 16,  322, "First Last Name",  13, "700", DK)
    + T("cf-t",   LM + 16,  342, "Job Title",         9, "400", MD)
    + T("cf-e",   LM + 16,  400, "hello@company.com", 8, "400", MD)
    + T("cf-p",   LM + 16,  418, "+1 (000) 000-0000", 8, "400", MD)
    + T("cf-w",   LM + 16,  436, "www.company.com",   8, "400", MD)
    + T("lbl-b",  LM + 408, 208, "Back",              9, "400", MD, ls=1)
    + R("cb",     LM + 408, 220, 360, 220, G, 3)
    + T("cb-l",   LM + 588, 338, "&#x25B2;  BRAND",  14, "700", WH, "middle")
    + T("sp-hdr", LM + 820, 208, "Specifications",   10, "700", DK)
    + L("sp-r",   LM + 820, 222, LM + 1020, 222, G, 1.5)
    + T("sp1",    LM + 820, 256, "Size:      85mm &#xD7; 55mm",    9, "400", MD)
    + T("sp2",    LM + 820, 274, "Material:  350gsm silk",          9, "400", MD)
    + T("sp3",    LM + 820, 292, "Finish:    Soft-touch matt",      9, "400", MD)
    + T("sp4",    LM + 820, 310, "Bleed:     3mm all sides",        9, "400", MD)
    + T("sp5",    LM + 820, 328, "Print:     CMYK + Spot UV",       9, "400", MD)
    + T("sp6",    LM + 820, 346, "Typeface:  Primary / 7pt min",    9, "400", MD)
    + T("sp7",    LM + 820, 364, "Colour:    Brand Green / White",  9, "400", MD)
)

# ── 19  STATIONERY — LETTERHEAD ───────────────────────────────────────
pages["19-stationery-letterhead"] = INNER(19, "04  STATIONERY", "Company Stationery Guideline",
    T("sub-hdr",   LM, 168, "Letterhead — A4 Portrait", 11, "400", MD)
    + T("lbl-lh",  LM,       208, "Layout Preview", 9, "400", MD, ls=1)
    + R("lh",      LM,       220, 280, 400, WH, 2, LT)
    + R("lh-top",  LM,       220, 280, 44,  G, 2)
    + T("lh-logo", LM + 14,  248, "&#x25B2;  BRAND", 9, "700", WH)
    + LBLOCKS("lh-b", LM + 14, 288, [228, 252, 232, 252, 220, 252, 232, 252, 228, 252, 220, 252, 228], gap=14, bh=6)
    + R("lh-ftr",  LM,       572, 280, 48, VL, 2)
    + LBLOCKS("lh-f", LM + 14, 584, [200, 160, 180], gap=12, bh=5)
    + T("ls-hdr",  LM + 344, 208, "Layout Grid",       10, "700", DK)
    + L("ls-r",    LM + 344, 222, LM + 544, 222, G, 1.5)
    + T("ls1",     LM + 344, 252, "Paper:    A4 (210 &#xD7; 297mm)", 9, "400", MD)
    + T("ls2",     LM + 344, 270, "Margins:  20mm all sides",         9, "400", MD)
    + T("ls3",     LM + 344, 288, "Header:   20mm height",            9, "400", MD)
    + T("ls4",     LM + 344, 306, "Footer:   15mm height",            9, "400", MD)
    + T("ls5",     LM + 344, 324, "Columns:  Single column",          9, "400", MD)
    + T("ty-hdr",  LM + 344, 372, "Typography Rules",  10, "700", DK)
    + L("ty-r",    LM + 344, 386, LM + 544, 386, G, 1.5)
    + T("ty1",     LM + 344, 416, "Address:  8pt Regular",             9, "400", MD)
    + T("ty2",     LM + 344, 434, "Body:     10pt / 16pt leading",     9, "400", MD)
    + T("ty3",     LM + 344, 452, "Date:     9pt Semi Bold",           9, "400", MD)
    + T("fo-hdr",  LM + 640, 208, "File Formats",      10, "700", DK)
    + L("fo-r",    LM + 640, 222, LM + 840, 222, G, 1.5)
    + T("fo1",     LM + 640, 252, "InDesign (.indd)",       9, "400", MD)
    + T("fo2",     LM + 640, 270, "PDF/X-1a (Print ready)", 9, "400", MD)
    + T("fo3",     LM + 640, 288, "Word (.docx)",            9, "400", MD)
    + T("fo4",     LM + 640, 306, "Illustrator (.ai)",       9, "400", MD)
)

# ── 20  STATIONERY — ENVELOPE ─────────────────────────────────────────
pages["20-stationery-envelope"] = INNER(20, "04  STATIONERY", "Stationery Guideline",
    T("sub-hdr",  LM, 168, "Envelope &amp; Notepad", 11, "400", MD)
    + T("lbl-env",LM, 208, "DL Envelope", 9, "400", MD, ls=1)
    + R("env",    LM,     220, 500, 296, WH, 4, LT)
    + R("env-top",LM,     220, 500,   5, G, 4)
    + T("env-lg", LM + 20, 288, "&#x25B2;  YOUR BRAND",  10, "700", DK)
    + T("env-a1", LM + 20, 378, "First Last Name",         9, "400", MD)
    + T("env-a2", LM + 20, 394, "123 Street Address",      9, "400", MD)
    + T("env-a3", LM + 20, 410, "City, State 00000",       9, "400", MD)
    + T("env-a4", LM + 20, 426, "Country",                 9, "400", MD)
    + L("env-fl", LM, 364, LM + 500, 364)
    + T("lbl-np", LM + 560, 208, "Notepad", 9, "400", MD, ls=1)
    + R("np",     LM + 560, 220, 184, 248, WH, 3, LT)
    + R("np-top", LM + 560, 220, 184,  32, G, 3)
    + T("np-lg",  LM + 576, 241, "&#x25B2; BRAND", 8, "700", WH)
    + LBLOCKS("np-l", LM + 576, 268, [148, 132, 148, 132, 148, 132, 148, 132, 148], gap=16, bh=6)
    + T("sp-hdr", LM + 800, 208, "Envelope Specs", 10, "700", DK)
    + L("sp-r",   LM + 800, 222, LM + 1000, 222, G, 1.5)
    + T("sp1",    LM + 800, 252, "DL:     220 &#xD7; 110mm", 9, "400", MD)
    + T("sp2",    LM + 800, 270, "C5:     229 &#xD7; 162mm", 9, "400", MD)
    + T("sp3",    LM + 800, 288, "C4:     324 &#xD7; 229mm", 9, "400", MD)
    + T("sp4",    LM + 800, 306, "Weight: 100gsm uncoated",   9, "400", MD)
    + T("sp5",    LM + 800, 324, "Print:  1-col (green bar)", 9, "400", MD)
    + T("np-sp",  LM + 800, 372, "Notepad Specs",  10, "700", DK)
    + L("np-sr",  LM + 800, 386, LM + 1000, 386, G, 1.5)
    + T("nsp1",   LM + 800, 416, "Size:   A5 (148 &#xD7; 210mm)", 9, "400", MD)
    + T("nsp2",   LM + 800, 434, "Pages:  50 sheets",              9, "400", MD)
    + T("nsp3",   LM + 800, 452, "Cover:  350gsm silk",            9, "400", MD)
)

# ── 21  SECTION — ICONOGRAPHY ─────────────────────────────────────────
pages["21-section-iconography"] = SECT(5, "Iconography",
    "Our icon system provides a consistent",
    "visual language for UI, print, and",
    "presentation applications."
)

# ── Icon helper ───────────────────────────────────────────────────────
ICON_LABELS = [
    "Home","Search","User","Settings","Mail","Bell","Heart","Star",
    "Calendar","File","Folder","Download","Upload","Share","Link","Lock",
    "Camera","Image","Video","Music","Map","Phone","Message","Cart",
    "Check","Close","Arrow","Menu","Plus","Filter","Sort","Dots",
]

def icon_grid(gid, bg_col, fg_col, rx=10):
    out = [f'  <g id="{gid}">\n']
    for idx, lbl in enumerate(ICON_LABELS):
        col = idx % 8
        row = idx // 8
        ix  = LM + col * 144
        iy  = 176 + row * 104
        out.append(
            f'    <g id="{gid}-{idx}">\n'
            f'      <rect x="{ix}" y="{iy}" width="60" height="60" rx="{rx}" '
            f'fill="{bg_col}" stroke="{LT}" stroke-width="0.5"/>\n'
            f'      <line x1="{ix+15}" y1="{iy+30}" x2="{ix+45}" y2="{iy+30}" '
            f'stroke="{fg_col}" stroke-width="2"/>\n'
            f'      <line x1="{ix+30}" y1="{iy+15}" x2="{ix+30}" y2="{iy+45}" '
            f'stroke="{fg_col}" stroke-width="2"/>\n'
            f'      <text x="{ix+30}" y="{iy+80}" font-family="{FF}" font-size="8" '
            f'fill="{MD}" text-anchor="middle">{lbl}</text>\n'
            f'    </g>\n'
        )
    out.append('  </g>\n')
    return "".join(out)

pages["22-icons-01"] = INNER(22, "05  ICONOGRAPHY", "Icon Example 01",
    T("desc",  LM, 168, "Line icon set — 2px stroke, rounded ends, 60&#xD7;60px grid.", 11, "400", MD)
    + icon_grid("line-icons", VL, MD, rx=8)
    + T("style", LM, 618, "Style: Line  /  Stroke: 2px  /  Corner: Rounded  /  Grid: 60&#xD7;60px  /  Sizes: 16, 24, 32, 48px", 8, "400", MD)
)

def icon_grid_filled(gid, bg_col, fg_col):
    out = [f'  <g id="{gid}">\n']
    for idx, lbl in enumerate(ICON_LABELS):
        col = idx % 8
        row = idx // 8
        ix  = LM + col * 144
        iy  = 176 + row * 104
        out.append(
            f'    <g id="{gid}-{idx}">\n'
            f'      <rect x="{ix}" y="{iy}" width="60" height="60" rx="8" fill="{bg_col}"/>\n'
            f'      <rect x="{ix+15}" y="{iy+15}" width="30" height="30" rx="4" fill="{fg_col}"/>\n'
            f'      <text x="{ix+30}" y="{iy+80}" font-family="{FF}" font-size="8" '
            f'fill="{MD}" text-anchor="middle">{lbl}</text>\n'
            f'    </g>\n'
        )
    out.append('  </g>\n')
    return "".join(out)

pages["23-icons-02"] = INNER(23, "05  ICONOGRAPHY", "Icon Example 02",
    T("desc",  LM, 168, "Filled icon set — solid style, same grid as line set.", 11, "400", MD)
    + icon_grid_filled("fill-icons", G, WH)
    + T("style", LM, 618, "Style: Filled  /  Color: Brand Green  /  Grid: 60&#xD7;60px  /  Sizes: 16, 24, 32, 48px", 8, "400", MD)
)

def icon_grid_duo(gid):
    out = [f'  <g id="{gid}">\n']
    for idx, lbl in enumerate(ICON_LABELS):
        col = idx % 8
        row = idx // 8
        ix  = LM + col * 144
        iy  = 176 + row * 104
        out.append(
            f'    <g id="{gid}-{idx}">\n'
            f'      <rect x="{ix}" y="{iy}" width="60" height="60" rx="8" fill="{GP}"/>\n'
            f'      <rect x="{ix+12}" y="{iy+12}" width="36" height="36" rx="4" fill="{GL}" opacity="0.6"/>\n'
            f'      <rect x="{ix+20}" y="{iy+20}" width="20" height="20" rx="2" fill="{GD}"/>\n'
            f'      <text x="{ix+30}" y="{iy+80}" font-family="{FF}" font-size="8" '
            f'fill="{MD}" text-anchor="middle">{lbl}</text>\n'
            f'    </g>\n'
        )
    out.append('  </g>\n')
    return "".join(out)

pages["24-icons-03"] = INNER(24, "05  ICONOGRAPHY", "Icon Example 03",
    T("desc",  LM, 168, "Duotone icon set — two-tone style using primary and tint colours.", 11, "400", MD)
    + icon_grid_duo("duo-icons")
    + T("style", LM, 618, "Style: Duotone  /  BG: Pale Green  /  FG: Deep Forest  /  Grid: 60&#xD7;60px", 8, "400", MD)
)

# ── 25  SECTION — LOGO PLACEMENT ─────────────────────────────────────
pages["25-section-logo-placement"] = SECT(6, "Placement",
    "Correct placement of the logo ensures",
    "brand recognition and maintains visual",
    "integrity across all applications."
)

# ── 26  LOGO PLACEMENT — LIGHT ────────────────────────────────────────
lp_light = [
    (WH, LT, DK, "White"),
    (VL, LT, DK, "Off White"),
    (GP, None, GD, "Pale Green"),
]
lp_body = T("desc", LM, 168, "Preferred logo placement on light, white, and tinted backgrounds.", 11, "400", MD)
for i, (col, sc, lc, lbl) in enumerate(lp_light):
    bx = LM + i * 384
    lp_body += (
        R(f"ex{i}", bx, 200, 352, 236, col, 3, sc)
        + T(f"el{i}", bx + 176, 324, "&#x25B2;  LOGO", 14, "700", lc, "middle")
        + T(f"en{i}", bx + 176, 456, lbl, 9, "400", MD, "middle")
    )
lp_body += (
    T("r-hdr",  LM, 484, "Placement Rules", 10, "700", DK)
    + L("r-ln",   LM, 498, LM + 180, 498, G, 1.5)
    + T("r1", LM, 520, "&#x2022;  Position logo in the top-left corner for all documents and stationery", 9, "400", MD)
    + T("r2", LM, 538, "&#x2022;  Centre logo on packaging, promotional, and signage materials",          9, "400", MD)
    + T("r3", LM, 556, "&#x2022;  Maintain minimum clear space equal to the height of the mark",          9, "400", MD)
    + T("r4", LM, 574, "&#x2022;  Never rotate, stretch, recolour, or alter the logo",                    9, "400", MD)
)
pages["26-logo-placement-light"] = INNER(26, "06  LOGO PLACEMENT", "Logo Placement", lp_body)

# ── 27  LOGO PLACEMENT — DARK ─────────────────────────────────────────
lp_dark = [
    (DK,  None, WH, "Near Black"),
    (G,   None, WH, "Brand Green"),
    (GD,  None, WH, "Deep Forest"),
]
lp_dark_body = T("desc", LM, 168, "Logo placement on dark, brand green, and photographic backgrounds.", 11, "400", MD)
for i, (col, sc, lc, lbl) in enumerate(lp_dark):
    bx = LM + i * 384
    lp_dark_body += (
        R(f"ex{i}", bx, 200, 352, 236, col, 3, sc)
        + T(f"el{i}", bx + 176, 324, "&#x25B2;  LOGO", 14, "700", lc, "middle")
        + T(f"en{i}", bx + 176, 456, lbl, 9, "400", MD, "middle")
    )
lp_dark_body += (
    T("r-hdr",  LM, 484, "Reversed Logo",  10, "700", DK)
    + L("r-ln",   LM, 498, LM + 140, 498, G, 1.5)
    + T("r1", LM, 520, "&#x2022;  Use white (reversed) logo on all dark backgrounds", 9, "400", MD)
    + T("r2", LM, 538, "&#x2022;  Never use green logo on dark — check contrast (WCAG AA 4.5:1 min)", 9, "400", MD)
    + T("r3", LM, 556, "&#x2022;  On photography, use a semi-transparent green or dark overlay", 9, "400", MD)
    + T("r4", LM, 574, "&#x2022;  Reversed logo file: logo-reversed-white.svg / .eps / .png", 9, "400", MD)
)
pages["27-logo-placement-dark"] = INNER(27, "06  LOGO PLACEMENT", "Logo Placement", lp_dark_body)

# ── 28  CONTACT ───────────────────────────────────────────────────────
def contact_card(cid, x, y, dept, name, role, detail1, detail2):
    return (
        R(f"cc{cid}",  x, y, 468, 168, VL, 3)
        + R(f"cct{cid}", x, y, 8, 168, G, 3)
        + T(f"cd{cid}", x + 28, y + 44, dept,    10, "700", DK)
        + T(f"cn{cid}", x + 28, y + 68, name,    13, "600", DK)
        + T(f"cr{cid}", x + 28, y + 88, role,     9, "400", MD)
        + T(f"ce{cid}", x + 28, y + 116, detail1, 9, "400", G)
        + T(f"cp{cid}", x + 28, y + 134, detail2, 9, "400", MD)
    )

pages["28-contact"] = INNER(28, "CONTACT", "Contact Part",
    T("desc", LM, 168, "For brand usage enquiries, please contact the relevant team below.", 11, "400", MD)
    + contact_card(1, LM, 200, "Brand &amp; Design", "First Last", "Brand Manager",
                   "brand@yourcompany.com", "+1 (000) 000-0000")
    + contact_card(2, LM + 524, 200, "Marketing &amp; Comms", "First Last", "Marketing Director",
                   "marketing@yourcompany.com", "+1 (000) 000-0000")
    + contact_card(3, LM, 400, "Digital &amp; Social", "@yourcompany", "Social Media Handle",
                   "Instagram / LinkedIn / Twitter", "Facebook / YouTube")
    + contact_card(4, LM + 524, 400, "Head Office", "Your Company HQ", "Main Office",
                   "123 Street, City, Country", "www.yourcompany.com")
)

# ── 29  SECTION — IMAGE & BRANDING ───────────────────────────────────
pages["29-section-image"] = SECT(7, "Image",
    "Photography and visual storytelling",
    "standards for consistent brand",
    "representation across all channels."
)

# ── 30  IMAGE & BRANDING 01 ───────────────────────────────────────────
ib_dos = ["Natural light", "Authentic moments", "Brand palette tones", "Human connection"]
ib_don = ["Heavy filters", "Staged/stock feel", "Off-brand colours", "Over-saturated"]
pages["30-image-branding-01"] = INNER(30, "07  IMAGE &amp; BRANDING", "Image &amp; Branding System",
    T("desc", LM, 168, "Photography style guidelines and approved visual directions for the brand.", 11, "400", MD)
    + IMG("hero", LM, 192, 576, 360, "HERO IMAGE")
    + IMG("sm1",  LM + 632, 192, 256, 164, "LIFESTYLE")
    + IMG("sm2",  LM + 632, 388, 256, 164, "PRODUCT")
    + T("do-hdr",  LM,       576, "&#x2714;  Do",     10, "700", GL)
    + T("dont-hdr",LM + 540, 576, "&#x2715;  Don't",  10, "700", RED)
    + "".join(
        T(f"do{i}", LM,       596 + i * 17, f"&#x2022;  {d}", 9, "400", MD)
        for i, d in enumerate(ib_dos)
    )
    + "".join(
        T(f"dn{i}", LM + 540, 596 + i * 17, f"&#x2022;  {d}", 9, "400", MD)
        for i, d in enumerate(ib_don)
    )
)

# ── 31  IMAGE & BRANDING 02 ───────────────────────────────────────────
social = [
    ("Instagram Square",  "1080 &#xD7; 1080px"),
    ("Instagram Story",   "1080 &#xD7; 1920px"),
    ("LinkedIn Header",   "1584 &#xD7; 396px"),
    ("Twitter Header",    "1500 &#xD7; 500px"),
    ("Facebook Cover",    "820 &#xD7; 312px"),
    ("Profile Picture",   "400 &#xD7; 400px"),
]
ib2_body = (
    T("desc", LM, 168, "Branded photography overlay system and social media size specifications.", 11, "400", MD)
    + IMG("img1", LM,       200, 296, 200, "PHOTO 01")
    + R("ov1",   LM,       356, 296, 44, G, 2)
    + T("ol1",   LM + 148, 384, "&#x25B2;  BRAND", 10, "700", WH, "middle")
    + IMG("img2", LM + 360, 200, 296, 200, "PHOTO 02")
    + R("ov2",   LM + 360, 356, 296, 44, GD, 2)
    + T("ol2",   LM + 508, 384, "&#x25B2;  BRAND", 10, "700", WH, "middle")
    + IMG("img3", LM + 720, 200, 296, 200, "PHOTO 03")
    + R("ov3",   LM + 720, 356, 296, 44, DK, 2)
    + T("ol3",   LM + 868, 384, "&#x25B2;  BRAND", 10, "700", WH, "middle")
    + T("cl1",   LM + 148, 464, "Standard Overlay", 9, "400", MD, "middle")
    + T("cl2",   LM + 508, 464, "Dark Overlay",     9, "400", MD, "middle")
    + T("cl3",   LM + 868, 464, "Minimal Overlay",  9, "400", MD, "middle")
    + T("ss-hdr", LM, 500, "Social Media Specifications", 10, "700", DK)
    + L("ss-r",   LM, 514, LM + 320, 514, G, 1.5)
)
for i, (plat, size) in enumerate(social):
    col = LM if i < 3 else LM + 600
    sy  = 536 + (i % 3) * 26
    ib2_body += T(f"ss{i}", col, sy, f"{plat}: {size}", 9, "400", MD)
pages["31-image-branding-02"] = INNER(31, "07  IMAGE &amp; BRANDING", "Image &amp; Branding System", ib2_body)

# ── 32  THANK YOU ─────────────────────────────────────────────────────
tdots = "".join(
    f'<circle cx="{LM + 420 + j*22}" cy="{72 + i*22}" r="2" fill="{G}"/>'
    for i in range(8) for j in range(8)
)
pages["32-thanks"] = SVG(
    BG()
    + R("panel",    W - 440, 0,      440, H,  G)
    + R("panel-dk", W - 440, H - 56, 440, 56, GD)
    + C("dc1", W - 440 + 100, 120, 200, GL, "none", 0.75, 0.2)
    + C("dc2", W - 440 + 100, 120, 120, GL, "none", 0.5,  0.14)
    + T("logo",     LM, 56,  "&#x25B2;  YOUR BRAND", 10, "700", MD, ls=1.5)
    + T("t1",       LM, 264, "Thank",  80, "800", DK,  ls=-2.5)
    + T("t2",       LM, 352, "You.",   80, "800", G,   ls=-2.5)
    + L("t-rule",   LM, 376, LM + 296, 376)
    + T("td1",      LM, 408, "This document is the sole property",         11, "400", MD)
    + T("td2",      LM, 426, "of Your Company Name and is intended",       11, "400", MD)
    + T("td3",      LM, 444, "for approved and licensed use only.",         11, "400", MD)
    + T("yr",       LM, 488, "&#x00A9; 2024 Your Company Name",             9, "400", MD, ls=0.5)
    + T("rights",   LM, 506, "All rights reserved.",                        9, "400", MD, ls=0.5)
    + T("rp1",  W - 380, H - 80, "BRAND GUIDELINES",    9, "700", WH, ls=2)
    + T("rp2",  W - 380, H - 60, "VERSION 1.0 — 2024",  8, "400", "rgba(255,255,255,0.55)", ls=1)
    + f'  <g id="dot-grid" opacity="0.09">{tdots}</g>\n'
)

# ════════════════════════════════════════════════════════════════════
# Write all files
# ════════════════════════════════════════════════════════════════════
for name, content in sorted(pages.items()):
    path = os.path.join(OUT, f"page-{name}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓  {path}")

print(f"\n✅  Generated {len(pages)} SVG pages  →  {OUT}/")
