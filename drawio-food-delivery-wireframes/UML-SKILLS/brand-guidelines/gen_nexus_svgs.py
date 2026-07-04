#!/usr/bin/env python3
"""NEXUS — Technical Brand Guidelines SVG Generator
12 pages · Palantir-inspired dark navy aesthetic"""
import os

OUT = "/mnt/user-data/outputs/nexus-brand-guidelines"
os.makedirs(OUT, exist_ok=True)

W, H = 1280, 720
# Display typeface (geometric sans — Space Grotesk style)
FD = "'Space Grotesk','DM Sans','GT Walsheim','Helvetica Neue',Arial,sans-serif"
# Body / label typeface (neutral precision sans — Inter style)
FB = "'Inter','IBM Plex Sans','DM Sans','Helvetica Neue',Arial,sans-serif"
LM, RM = 72, 1208

# ── Brand colours ─────────────────────────────────────────────────────
BG  = "#182638"   # Deep Navy  — primary background
BG2 = "#1F3050"   # Panel Navy — cards / panels
BG3 = "#243860"   # Elevated   — secondary panels
WH  = "#FFFFFF"   # White      — primary text / line art
AC  = "#7BAFD4"   # Blue Accent
MT  = "#8FA8C0"   # Muted      — secondary text
DM  = "#4A6880"   # Dim        — low-emphasis elements
LN  = "#2A3D58"   # Line       — borders / dividers
HL  = "#C5DFF0"   # Highlight  — bright accent / callouts
GR  = "#4DB87A"   # Success
RD  = "#D95050"   # Error

# ── Core SVG helpers ──────────────────────────────────────────────────
def SVG(b):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n{b}</svg>\n')

def BKG(c=BG): return f'  <rect id="bg" width="{W}" height="{H}" fill="{c}"/>\n'

def R(i,x,y,w,h,c=BG,rx=0,sc=None,sw=1):
    s=f' stroke="{sc}" stroke-width="{sw}"' if sc else ""
    return f'  <rect id="{i}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" rx="{rx}"{s}/>\n'

def L(i,x1,y1,x2,y2,c=LN,sw=0.75):
    return f'  <line id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"/>\n'

def T(i,x,y,t,sz=10,wt="400",c=WH,a="start",ls=0,ff=None):
    la=f' letter-spacing="{ls}"' if ls else ""
    return (f'  <text id="{i}" x="{x}" y="{y}" font-family="{ff or FB}" '
            f'font-size="{sz}" font-weight="{wt}" fill="{c}" text-anchor="{a}"{la}>{t}</text>\n')

def TD(i,x,y,t,sz=11,wt="700",c=WH,a="start",ls=0):
    """Display-weight text"""
    return T(i,x,y,t,sz,wt,c,a,ls,FD)

def LB(i,x,y,ws,g=14,bh=7,c=LN):
    o=[f'  <g id="{i}">\n']
    for j,w in enumerate(ws):
        o.append(f'    <rect x="{x}" y="{y+j*g}" width="{w}" height="{bh}" fill="{c}"/>\n')
    o.append('  </g>\n'); return "".join(o)

def IMG(i,x,y,w,h,lbl="",bg=BG2):
    cx,cy=x+w//2,y+h//2
    return (f'  <g id="{i}">\n'
            f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}" stroke="{LN}" stroke-width="0.75"/>\n'
            f'    <line x1="{x+10}" y1="{y+10}" x2="{x+w-10}" y2="{y+h-10}" stroke="{LN}" stroke-width="0.5"/>\n'
            f'    <line x1="{x+w-10}" y1="{y+10}" x2="{x+10}" y2="{y+h-10}" stroke="{LN}" stroke-width="0.5"/>\n'
            +(f'    <text x="{cx}" y="{cy+4}" font-family="{FB}" font-size="8" fill="{DM}" '
              f'text-anchor="middle" letter-spacing="2">{lbl.upper()}</text>\n' if lbl else "")
            +'  </g>\n')

def CHECK(i,x,y,sz=18,c=GR):
    r=sz//2
    return (f'  <circle id="{i}-c" cx="{x+r}" cy="{y+r}" r="{r}" fill="none" stroke="{c}" stroke-width="1.25"/>\n'
            f'  <text id="{i}-t" x="{x+r}" y="{y+r+4}" font-family="{FB}" font-size="{max(7,sz-9)}" '
            f'font-weight="600" fill="{c}" text-anchor="middle">&#10003;</text>\n')

def CROSS(i,x,y,sz=18,c=RD):
    r=sz//2
    return (f'  <circle id="{i}-c" cx="{x+r}" cy="{y+r}" r="{r}" fill="none" stroke="{c}" stroke-width="1.25"/>\n'
            f'  <text id="{i}-t" x="{x+r}" y="{y+r+4}" font-family="{FB}" font-size="{max(7,sz-7)}" '
            f'font-weight="600" fill="{c}" text-anchor="middle">&#215;</text>\n')

# ── Technical illustration helpers ────────────────────────────────────
def GRID(pid,x=0,y=0,w=W,h=H,sp=48,col="rgba(255,255,255,0.032)"):
    o=[f'  <g id="{pid}">\n']
    for gx in range(x,x+w+sp,sp):
        o.append(f'    <line x1="{gx}" y1="{y}" x2="{gx}" y2="{y+h}" stroke="{col}" stroke-width="0.5"/>\n')
    for gy in range(y,y+h+sp,sp):
        o.append(f'    <line x1="{x}" y1="{gy}" x2="{x+w}" y2="{gy}" stroke="{col}" stroke-width="0.5"/>\n')
    o.append('  </g>\n'); return "".join(o)

# Deterministic dot positions (avoids random module)
_DOTS=[(-0.55,0.12),(-0.15,0.30),(0.42,0.18),(0.68,0.55),(-0.48,0.70),
       (0.22,0.78),(-0.32,0.88),(0.58,0.82),(-0.28,0.42),(0.35,0.60),
       (-0.62,0.52),(0.10,0.38),(0.50,0.25),(-0.70,0.30),(0.20,0.55),(-0.05,0.80)]
_DR  =[1.5,2.0,2.0,2.5,1.5,2.0,1.5,2.0,2.5,1.5,2.0,1.5,1.5,2.0,2.0,1.5]

def CYLINDER(pid,cx,cy,rx,h,ry=None,col=WH,op=1.0,ndots=10,layers=2,bgc=BG,sw=1.2):
    """Technical 3-D database / data-store cylinder"""
    if ry is None: ry=max(6,rx//7)
    o=[f'  <g id="{pid}" opacity="{op}">\n']
    # Subtle volume fill
    o.append(f'    <rect x="{cx-rx}" y="{cy}" width="{rx*2}" height="{h}" fill="{col}" opacity="0.035"/>\n')
    # Vertical sides
    o.append(f'    <line x1="{cx-rx}" y1="{cy}" x2="{cx-rx}" y2="{cy+h}" stroke="{col}" stroke-width="{sw}"/>\n')
    o.append(f'    <line x1="{cx+rx}" y1="{cy}" x2="{cx+rx}" y2="{cy+h}" stroke="{col}" stroke-width="{sw}"/>\n')
    # Bottom ellipse (bg fill for 3-D depth)
    o.append(f'    <ellipse cx="{cx}" cy="{cy+h}" rx="{rx}" ry="{ry}" fill="{bgc}" stroke="{col}" stroke-width="{sw}"/>\n')
    # Internal dashed layer planes
    for li in range(1,layers+1):
        ly=cy+h*li//(layers+1)
        o.append(f'    <ellipse cx="{cx}" cy="{ly}" rx="{rx}" ry="{ry}" fill="none" '
                 f'stroke="{col}" stroke-width="0.7" stroke-dasharray="5,4" opacity="0.38"/>\n')
    # Top ellipse (bg fill to cap the cylinder)
    o.append(f'    <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{bgc}" stroke="{col}" stroke-width="{sw}"/>\n')
    # Data-point dots
    for di in range(min(ndots,len(_DOTS))):
        fx,fy=_DOTS[di]
        dx=int(cx+fx*(rx-8))
        dy=int(cy+ry+int(fy*(h-2*ry)))
        if cy+ry<dy<cy+h-ry:
            o.append(f'    <circle cx="{dx}" cy="{dy}" r="{_DR[di%len(_DR)]}" fill="{col}" opacity="0.82"/>\n')
    o.append('  </g>\n'); return "".join(o)

def LOGO(pid,cx,cy,size,col=WH,sw=1.5):
    """Nexus concentric-target logo mark"""
    s=size; ex=s*0.32
    o=[f'  <g id="{pid}">\n']
    o.append(f'    <circle cx="{cx}" cy="{cy}" r="{s}" fill="none" stroke="{col}" stroke-width="{sw}"/>\n')
    o.append(f'    <circle cx="{cx}" cy="{cy}" r="{s*0.54}" fill="none" stroke="{col}" stroke-width="{sw*0.6}" opacity="0.65"/>\n')
    o.append(f'    <circle cx="{cx}" cy="{cy}" r="{s*0.13}" fill="{col}"/>\n')
    o.append(f'    <line x1="{cx}" y1="{cy-s}" x2="{cx}" y2="{cy-s-ex}" stroke="{col}" stroke-width="{sw}"/>\n')
    o.append(f'    <line x1="{cx}" y1="{cy+s}" x2="{cx}" y2="{cy+s+ex}" stroke="{col}" stroke-width="{sw}"/>\n')
    o.append(f'    <line x1="{cx-s}" y1="{cy}" x2="{cx-s-ex}" y2="{cy}" stroke="{col}" stroke-width="{sw}"/>\n')
    o.append(f'    <line x1="{cx+s}" y1="{cy}" x2="{cx+s+ex}" y2="{cy}" stroke="{col}" stroke-width="{sw}"/>\n')
    o.append('  </g>\n'); return "".join(o)

def ANNOT(pid,lx,ly,ax,ay,label,col=MT):
    """Dashed annotation line from text label to target point"""
    return (f'  <g id="{pid}">\n'
            f'    <text x="{lx}" y="{ly}" font-family="{FB}" font-size="8" fill="{col}" letter-spacing="0.5">{label}</text>\n'
            f'    <line x1="{lx+len(label)*4+2}" y1="{ly-3}" x2="{ax}" y2="{ay}" '
            f'stroke="{col}" stroke-width="0.75" stroke-dasharray="3,3"/>\n'
            f'    <circle cx="{ax}" cy="{ay}" r="2" fill="{col}"/>\n'
            f'  </g>\n')

def LOCK(pid,cx,cy,col=WH,sz=18):
    """Simple padlock icon"""
    hw=sz//2; hh=sz//2
    return (f'  <g id="{pid}">\n'
            f'    <rect x="{cx-hw}" y="{cy}" width="{sz}" height="{hh+4}" rx="2" '
            f'fill="none" stroke="{col}" stroke-width="0.85"/>\n'
            f'    <path d="M{cx-hw*0.55},{cy} A{hw*0.55},{hh*0.8} 0 0,1 {cx+hw*0.55},{cy}" '
            f'fill="none" stroke="{col}" stroke-width="0.85"/>\n'
            f'    <circle cx="{cx}" cy="{cy+hh//2+2}" r="2" fill="{col}"/>\n'
            f'  </g>\n')

def HDR(n,title):
    nz=str(n).zfill(2)
    return (L("htp",0,0,W,0,WH,0.5)
            +T("hn",LM,40,f"{nz}",8,"400",DM,ls=1)
            +T("hd",LM+26,40,"·",8,"400",DM)
            +T("ht",LM+42,40,title.upper(),8,"600",MT,ls=3)
            +T("hbr",RM,40,"NEXUS",8,"700",DM,"end",ls=4)
            +L("hdiv",LM,50,RM,50,LN,0.5))

def FTR():
    return (L("fdiv",LM,H-40,RM,H-40,LN,0.5)
            +T("fl",LM,H-20,"NEXUS BRAND GUIDELINES  ·  VERSION 1.0  ·  2024",8,"400",DM,ls=1)
            +T("fr",RM,H-20,"nexus.io",8,"400",DM,"end",ls=1))

def INNER(n,title,body):
    return SVG(BKG()+GRID("bg-g")+HDR(n,title)+body+FTR())

# ════════════════════════════════════════════════════════════════════
pages={}

# ── 01  COVER ─────────────────────────────────────────────────────────
LPW=560   # left panel width
pages["01-cover"]=SVG(
    BKG()+GRID("bg-g")
    # ── Left panel ──
    +LOGO("lm",LM+14,42,11,WH,1.2)
    +T("lm-nm",LM+42,50,"NEXUS",8,"700",MT,ls=4)
    +T("lm-se",LM+96,50,"·  BRAND GUIDELINES",7,"400",DM,ls=2)
    # Large display headline
    +TD("h1",LM,224,"Brand",  72,"700",WH,ls=-2)
    +TD("h2",LM,306,"Guide",  72,"700",WH,ls=-2)
    +TD("h3",LM,388,"lines →",72,"700",WH,ls=-2)
    +L("hdash",LM,428,LM+72,428,WH,1.5)
    +T("sub",LM,454,"Data. Precision. Insight.",11,"400",MT)
    +T("s1",LM,H-56,"TECHNOLOGY  ·  SECURITY  ·  INTELLIGENCE",7,"600",DM,ls=2)
    +T("s2",LM,H-38,"nexus.io",7,"400",DM,ls=1)
    # ── Divider ──
    +L("div",LPW,0,LPW,H,LN,0.75)
    # ── Right panel ──
    +R("rp",LPW,0,W-LPW,H,BG2)
    +GRID("rp-g",LPW,0,W-LPW,H,48,"rgba(255,255,255,0.022)")
    # Column headers
    +T("c1n",LPW+44,58,"01",8,"400",MT,ls=2)
    +T("c1t",LPW+44,74,"Original Data Asset",8,"400",DM)
    +T("c2n",1072,58,"02",8,"400",MT,ls=2)
    +T("c2t",1072,74,"Post-Deletion Data Asset",8,"400",DM)
    # Left cylinder (original data — many dots)
    +CYLINDER("cy1",764,84,108,396,16,WH,1.0,14,3,BG2,1.25)
    # Right cylinder (processed — fewer dots)
    +CYLINDER("cy2",1148,140,72,280,11,WH,0.85,7,2,BG2,1.0)
    # Flow / connection
    +f'  <path id="flow" d="M872,300 C940,300 980,310 1075,310" fill="none" stroke="{MT}" stroke-width="0.85" stroke-dasharray="4,3"/>\n'
    +f'  <polygon id="flow-tip" points="1070,306 1076,310 1070,314" fill="{MT}"/>\n'
    # Lock icon + label
    +LOCK("lock",970,278,WH,20)
    +T("lock-l",994,290,"SECURE",7,"600",MT,ls=2)
    # Annotations
    +ANNOT("a1",LPW+44,62,732,84,"Data ↓",DM)
    +ANNOT("a2",LPW+44,506,730,480,"Deletion Process ↑",DM)
    +FTR()
)

# ── 02  BRAND ESSENCE ─────────────────────────────────────────────────
pages["02-brand-essence"]=INNER(2,"Brand Essence",
    # Three-column layout: Mission | Principles | Vision
    # ── Mission ──
    T("mh",LM,84,"MISSION",7,"700",DM,ls=3)
    +L("mr",LM,94,LM+352,94,LN)
    +TD("mt",LM,136,"We build systems",22,"700",WH,ls=-0.5)
    +TD("mt2",LM,162,"of precision and",22,"700",WH,ls=-0.5)
    +TD("mt3",LM,188,"clarity.",22,"700",WH,ls=-0.5)
    +L("mr2",LM,208,LM+60,208,MT,1.5)
    +LB("mb",LM,224,[316,356,336,356,316,336,356,316],g=16,bh=8)
    # ── Divider ──
    +L("d1",LM+392,72,LM+392,H-60,LN)
    # ── Core Principles ──
    +T("ph",LM+420,84,"CORE PRINCIPLES",7,"700",DM,ls=3)
    +L("pr",LM+420,94,LM+772,94,LN)
    +f'  <g id="principles">\n'
    +f'    <circle cx="{LM+432}" cy="128" r="4" fill="none" stroke="{AC}" stroke-width="1"/>\n'
    +T("p1",LM+448,133,"Transparency",10,"600",WH)
    +LB("p1b",LM+448,142,[240,280,256],g=14,bh=7)
    +f'    <circle cx="{LM+432}" cy="212" r="4" fill="none" stroke="{AC}" stroke-width="1"/>\n'
    +T("p2",LM+448,217,"Accuracy",10,"600",WH)
    +LB("p2b",LM+448,226,[240,280,256],g=14,bh=7)
    +f'    <circle cx="{LM+432}" cy="296" r="4" fill="none" stroke="{AC}" stroke-width="1"/>\n'
    +T("p3",LM+448,301,"Security",10,"600",WH)
    +LB("p3b",LM+448,310,[240,280,256],g=14,bh=7)
    +f'    <circle cx="{LM+432}" cy="380" r="4" fill="none" stroke="{AC}" stroke-width="1"/>\n'
    +T("p4",LM+448,385,"Scalability",10,"600",WH)
    +LB("p4b",LM+448,394,[240,280,256],g=14,bh=7)
    +f'    <line x1="{LM+432}" y1="132" x2="{LM+432}" y2="208" stroke="{LN}" stroke-width="0.75"/>\n'
    +f'    <line x1="{LM+432}" y1="216" x2="{LM+432}" y2="292" stroke="{LN}" stroke-width="0.75"/>\n'
    +f'    <line x1="{LM+432}" y1="300" x2="{LM+432}" y2="376" stroke="{LN}" stroke-width="0.75"/>\n'
    +f'  </g>\n'
    # ── Divider ──
    +L("d2",LM+812,72,LM+812,H-60,LN)
    # ── Vision ──
    +T("vh",LM+840,84,"VISION",7,"700",DM,ls=3)
    +L("vr",LM+840,94,RM,94,LN)
    +R("vbox",LM+840,112,RM-LM-840,280,BG2,2,LN,0.75)
    +LOGO("v-logo",LM+840+(RM-LM-840)//2,248,40,MT,0.75)
    +T("vt1",LM+856,436,"To become the definitive",10,"400",MT)
    +T("vt2",LM+856,454,"infrastructure for human-scale",10,"400",MT)
    +T("vt3",LM+856,472,"data intelligence.",10,"400",MT)
    +LB("vb",LM+840,500,[316,356,280],g=16,bh=7)
)

# ── 03  LOGO SYSTEM ───────────────────────────────────────────────────
pages["03-logo-system"]=INNER(3,"Logo System",
    # Primary lockup
    T("pl-lbl",LM,80,"PRIMARY LOCKUP",7,"700",DM,ls=3)
    +L("pl-r",LM,90,LM+480,90,LN)
    +R("pl-box",LM,100,480,220,BG2,2,LN,0.75)
    +LOGO("pl-lg",LM+100,212,40,WH,1.5)
    +TD("pl-nm",LM+164,200,"NEXUS",28,"700",WH,ls=4)
    +T("pl-tg",LM+164,222,"Data Intelligence Platform",9,"400",MT,ls=0.5)
    # Colour variants
    +T("cv-lbl",LM,344,"COLOUR VARIANTS",7,"700",DM,ls=3)
    +L("cv-r",LM,354,LM+480,354,LN)
    +R("cv1",LM,364,148,100,BG,2,LN,0.75)
    +LOGO("cv1-l",LM+52,414,18,WH,1.2)+T("cv1-t",LM+74,425,"On Dark",7,"400",DM,"middle")
    +R("cv2",LM+164,364,148,100,WH,2,LN,0.75)
    +LOGO("cv2-l",LM+216,414,18,BG,1.2)+T("cv2-t",LM+238,425,"On Light",7,"400",DM,"middle")
    +R("cv3",LM+328,364,148,100,AC,2,LN,0.75)
    +LOGO("cv3-l",LM+380,414,18,WH,1.2)+T("cv3-t",LM+402,425,"On Accent",7,"400",DM,"middle")
    # Anatomy annotations
    +T("an-lbl",LM+540,80,"LOGO ANATOMY",7,"700",DM,ls=3)
    +L("an-r",LM+540,90,RM,90,LN)
    +R("an-box",LM+540,100,RM-LM-540,220,BG2,2,LN,0.75)
    +LOGO("an-lg",LM+540+(RM-LM-540)//2,212,52,WH,1.5)
    # Annotation callouts
    +ANNOT("ann1",LM+548,108,LM+540+(RM-LM-540)//2-52,212,"Outer ring",MT)
    +ANNOT("ann2",LM+548,132,LM+540+(RM-LM-540)//2,212,"Centre node",MT)
    +ANNOT("ann3",RM-96,108,LM+540+(RM-LM-540)//2+52,212,"Cross-hairs",MT)
    # Clear space
    +T("cs-lbl",LM+540,344,"CLEAR SPACE",7,"700",DM,ls=3)
    +L("cs-r",LM+540,354,RM,354,LN)
    +R("cs-box",LM+540,364,220,160,BG2,2,LN,0.75)
    +LOGO("cs-lg",LM+540+110,444,24,WH,1.0)
    # X markers for clear space
    +T("cs-x1",LM+548,376,"x",8,"400",DM)
    +T("cs-x2",LM+548,504,"x",8,"400",DM)
    +T("cs-x3",LM+738,376,"x",8,"400",DM)
    +T("cs-x4",LM+738,504,"x",8,"400",DM)
    +T("cs-note",LM+540,540,"X = diameter of centre node",8,"400",DM)
    # Min size
    +T("ms-lbl",LM+796,344,"MINIMUM SIZE",7,"700",DM,ls=3)
    +L("ms-r",LM+796,354,RM,354,LN)
    +R("ms-box",LM+796,364,RM-LM-796,80,BG2,2,LN,0.75)
    +LOGO("ms-lg",LM+844,404,14,WH,1.0)
    +TD("ms-nm",LM+876,408,"NEXUS",10,"700",WH,ls=3)
    +T("ms-d",LM+796,460,"24px min height (digital)",8,"400",DM)
    +T("ms-p",LM+796,476,"8mm min height (print)",8,"400",DM)
)

# ── 04  COLOUR PALETTE ────────────────────────────────────────────────
# Primary chips
PRI=[
    (BG,  "Deep Navy",    "#182638","R:24 G:38 B:56",  "PRIMARY BACKGROUND"),
    (BG2, "Panel Navy",   "#1F3050","R:31 G:48 B:80",  "PANELS / CARDS"),
    (WH,  "White",        "#FFFFFF","R:255 G:255 B:255","TEXT / LINE ART"),
    (AC,  "Blue Accent",  "#7BAFD4","R:123 G:175 B:212","HIGHLIGHTS / LINKS"),
]
# Secondary chips
SEC=[
    (BG3, "Elevated",  "#243860","Support surface"),
    (MT,  "Muted",     "#8FA8C0","Secondary text"),
    (DM,  "Dim",       "#4A6880","Low-emphasis"),
    (LN,  "Line",      "#2A3D58","Borders/dividers"),
    (HL,  "Highlight", "#C5DFF0","Callouts/hover"),
    (GR,  "Success",   "#4DB87A","Positive states"),
    (RD,  "Error",     "#D95050","Error states"),
]
CW1=(RM-LM-12)//4
CH1=148
SY1=80

pal_body=""
for i,(col,name,hx,rgb,role) in enumerate(PRI):
    sx=LM+i*(CW1+4)
    pal_body+=(R(f"pw{i}",sx,SY1,CW1,CH1,col,2,LN if col in(WH,) else None,0.5)
               +LOGO(f"pw{i}-l",sx+CW1//2,SY1+CH1//2,CH1//8,BG if col==WH else WH,0.9)
               +T(f"pn{i}",sx,SY1+CH1+18,name,9,"700",WH)
               +T(f"ph{i}",sx,SY1+CH1+34,hx,9,"600",AC)
               +T(f"pr{i}",sx,SY1+CH1+50,rgb,8,"400",DM)
               +T(f"prl{i}",sx,SY1+CH1+66,role,7,"600",MT,ls=2))

SY2=SY1+CH1+88
SCW=(RM-LM-24)//7
pal_body+=T("sl",LM,SY2-16,"SUPPORTING PALETTE",7,"700",DM,ls=3)+L("slr",LM,SY2-6,RM,SY2-6,LN)
for i,(col,name,hx,role) in enumerate(SEC):
    sx=LM+i*(SCW+4)
    pal_body+=(R(f"sc{i}",sx,SY2,SCW,64,col,2,LN if col in(WH,HL) else None,0.5)
               +T(f"sn{i}",sx,SY2+80,name,8,"700",WH)
               +T(f"sh{i}",sx,SY2+96,hx,8,"600",AC)
               +T(f"sr{i}",sx,SY2+112,role,7,"400",DM))

# Colour rules panel
pal_body+=(T("cr-h",LM,SY2+136,"USAGE RULES",7,"700",DM,ls=3)
           +L("cr-r",LM,SY2+146,RM,SY2+146,LN)
           +R("cr1",LM,SY2+156,232,48,BG2,2,AC,1)+T("cr1t",LM+12,SY2+185,"White on Deep Navy ✓",9,"400",WH)
           +R("cr2",LM+248,SY2+156,232,48,BG,2,LN,0.5)+T("cr2t",LM+260,SY2+185,"Accent on Navy ✓",9,"400",AC)
           +R("cr3",LM+496,SY2+156,232,48,WH,2,LN,0.5)+T("cr3t",LM+508,SY2+185,"Navy on White ✓",9,"400",BG)
           +R("cr4",LM+744,SY2+156,232,48,BG,2,LN,0.5)
           +T("cr4t",LM+756,SY2+185,"Deep Navy on Navy ✗",9,"400",BG3))
pages["04-color-palette"]=INNER(4,"Color Palette",pal_body)

# ── 05  TYPOGRAPHY ────────────────────────────────────────────────────
WGTS=[("ExtraBold","800"),("Bold","700"),("SemiBold","600"),
      ("Medium","500"),("Regular","400"),("Light","300")]
ty_body=(
    T("fd-lbl",LM,78,"DISPLAY TYPEFACE",7,"700",DM,ls=3)
    +TD("fd-nm",LM,122,"Space Grotesk",36,"700",WH,ls=-1)
    +TD("fd-aa",LM+460,94,"Ag",60,"700",AC)
    +L("fd-r",LM,136,LM+540,136,LN)
    +T("fd-d1",LM,156,"Geometric precision sans. Clean, confident,",9,"400",DM)
    +T("fd-d2",LM,172,"engineered for clarity at every scale.",9,"400",DM)
    +T("fd-dl",LM,192,"fonts.google.com/specimen/Space+Grotesk  ·  Free",7,"400",DM,ls=0.5)
    +L("fd-r2",LM,204,LM+540,204,LN)
)
for i,(nm,wt) in enumerate(WGTS):
    ty_body+=TD(f"fw{i}",LM,228+i*36,f"{nm}  —  Aa Bb Cc 0123",12,wt,WH,ls=-0.25)
ty_body+=(
    L("al1",LM,448,LM+540,448,LN,0.5)
    +T("alA",LM,466,"A B C D E F G H I J K L M N O P Q R S T U V W X Y Z",8,"400",DM)
    +T("ala",LM,482,"a b c d e f g h i j k l m n o p q r s t u v w x y z",8,"400",DM)
    +T("aln",LM,498,"0 1 2 3 4 5 6 7 8 9   !   @   #   $   %   &amp;",8,"400",DM)
    +L("al2",LM,510,LM+540,510,LN,0.5)
    # Body font
    +T("fb-lbl",LM+600,78,"BODY TYPEFACE",7,"700",DM,ls=3)
    +T("fb-nm",LM+600,122,"Inter",36,"700",WH,ls=-1,ff=FB)
    +T("fb-aa",LM+1060,94,"Ag",60,"700",MT,ff=FB)
    +L("fb-r",LM+600,136,RM,136,LN)
    +T("fb-d1",LM+600,156,"Neutral utility sans. Maximum legibility,",9,"400",DM)
    +T("fb-d2",LM+600,172,"zero friction at small sizes.",9,"400",DM)
    +T("fb-dl",LM+600,192,"fonts.google.com/specimen/Inter  ·  Free",7,"400",DM,ls=0.5)
    +L("fb-r2",LM+600,204,RM,204,LN)
)
for i,(nm,wt) in enumerate(WGTS):
    ty_body+=T(f"bw{i}",LM+600,228+i*36,f"{nm}  —  Aa Bb Cc 0123",12,wt,WH,ls=-0.25)
# Usage table
ty_body+=(
    L("us-top",LM,526,RM,526,LN,1)
    +T("ush1",LM,544,"STYLE",7,"700",DM,ls=2)+T("ush2",LM+360,544,"TYPEFACE",7,"700",DM,ls=2)+T("ush3",RM,544,"SIZE",7,"700",DM,"end",ls=2)
)
US=[("Display / H1","Space Grotesk ExtraBold 800","64–96px"),
    ("Heading H2","Space Grotesk Bold 700","32–48px"),
    ("Heading H3","Space Grotesk SemiBold 600","20–28px"),
    ("Body","Inter Regular 400","14–16px"),
    ("Label / Caption","Inter SemiBold 600","10–12px")]
for i,(s,f,z) in enumerate(US):
    uy=562+i*26
    ty_body+=(T(f"us{i}",LM,uy,s,8,"400",MT)
              +T(f"uf{i}",LM+360,uy,f,8,"600",WH)
              +T(f"uz{i}",RM,uy,z,8,"400",AC,"end"))
pages["05-typography"]=INNER(5,"Typography",ty_body)

# ── 06  VISUAL LANGUAGE ───────────────────────────────────────────────
# Show illustration style: 3 cylinders in states + annotation examples
vl_body=(
    T("il-h",LM,76,"ILLUSTRATION STYLE — DATA STORE SYSTEM",7,"700",DM,ls=3)
    +L("il-r",LM,86,RM,86,LN)
    # Three cylinders: Full · Filtered · Empty
    +T("c1l",LM+96,104,"FULL",7,"600",DM,ls=2)
    +CYLINDER("vc1",LM+160,108,88,360,12,WH,1.0,12,3,BG,1.2)
    +T("c2l",LM+440,104,"FILTERED",7,"600",DM,ls=2)
    +CYLINDER("vc2",LM+520,108,88,360,12,WH,0.75,6,3,BG,1.0)
    +T("c3l",LM+740,104,"PROCESSED",7,"600",DM,ls=2)
    +CYLINDER("vc3",LM+820,108,88,360,12,AC,0.6,3,3,BG,0.85)
    # Flow arrows between cylinders
    +f'  <path id="f1" d="M{LM+248},288 C{LM+300},288 {LM+360},288 {LM+432},288" fill="none" stroke="{LN}" stroke-width="1.0" stroke-dasharray="4,3"/>\n'
    +f'  <polygon points="{LM+427},284 {LM+433},288 {LM+427},292" fill="{LN}"/>\n'
    +f'  <path id="f2" d="M{LM+608},288 C{LM+660},288 {LM+700},288 {LM+732},288" fill="none" stroke="{LN}" stroke-width="1.0" stroke-dasharray="4,3"/>\n'
    +f'  <polygon points="{LM+727},284 {LM+733},288 {LM+727},292" fill="{LN}"/>\n'
    # Annotations
    +ANNOT("va1",LM+60,108,LM+160,120,"Data ingestion",DM)
    +ANNOT("va2",LM+60,480,LM+160,468,"Storage volume",DM)
    +ANNOT("va3",LM+300,480,LM+432,420,"Filter layer",DM)
    +ANNOT("va4",LM+600,104,LM+608,120,"Processing",DM)
    # Grid background note
    +R("gn",LM,536,520,100,BG2,2,LN,0.75)
    +GRID("gn-g",LM,536,520,100,24,"rgba(255,255,255,0.06)")
    +T("gnt",LM+20,560,"Background grid — 48px spacing",8,"400",DM)
    +T("gnt2",LM+20,578,"opacity 3.2% · always below content layer",8,"400",DM)
    # Dot scale
    +R("ds",LM+556,536,200,100,BG2,2,LN,0.75)
    +f'  <circle cx="{LM+596}" cy="{LM+536-72+100//2}" r="1.5" fill="{WH}" opacity="0.82"/>\n'
    +f'  <circle cx="{LM+628}" cy="{LM+536-72+100//2}" r="2.0" fill="{WH}" opacity="0.82"/>\n'
    +f'  <circle cx="{LM+660}" cy="{LM+536-72+100//2}" r="2.5" fill="{WH}" opacity="0.82"/>\n'
    +T("dsl",LM+596,612,"1.5px",7,"400",DM,"middle")+T("dsm",LM+628,612,"2.0px",7,"400",DM,"middle")
    +T("dss",LM+660,612,"2.5px",7,"400",DM,"middle")
    +T("dstt",LM+556,598,"Data-point dot scale",8,"400",DM)
    # Line weights
    +R("lw",LM+792,536,380,100,BG2,2,LN,0.75)
    +f'  <line x1="{LM+812}" y1="574" x2="{LM+1020}" y2="574" stroke="{WH}" stroke-width="0.75"/>\n'
    +f'  <line x1="{LM+812}" y1="598" x2="{LM+1020}" y2="598" stroke="{WH}" stroke-width="1.25"/>\n'
    +f'  <line x1="{LM+812}" y1="622" x2="{LM+1020}" y2="622" stroke="{WH}" stroke-width="2.0"/>\n'
    +T("lw1",LM+1024,576,"0.75px  ·  secondary",7,"400",DM)
    +T("lw2",LM+1024,600,"1.25px  ·  primary",7,"400",DM)
    +T("lw3",LM+1024,624,"2.00px  ·  emphasis",7,"400",DM)
)
pages["06-visual-language"]=INNER(6,"Visual Language",vl_body)

# ── 07  ICONOGRAPHY ───────────────────────────────────────────────────
ICON_DATA=[
    # (id, name, path_d or special)
    ("database","Database",
     f"M12,8 A12,5 0 0,1 -12,8 A12,5 0 0,1 12,8 M-12,8 L-12,24 A12,5 0 0,0 12,24 L12,8 M-12,16 A12,5 0 0,0 12,16"),
    ("lock","Security","M-8,0 L-8,12 A8,6 0 0,0 8,12 L8,0 M-5,0 A5,7 0 0,1 5,0"),
    ("node","Network Node","M0,-16 L14,8 L-14,8 Z M0,0 m-3,0 a3,3 0 1,0 6,0 a3,3 0 1,0 -6,0"),
    ("flow","Data Flow","M-16,0 L16,0 M10,-5 L16,0 L10,5 M-16,-8 A8,8 0 0,1 -8,-16"),
    ("shield","Shield","M0,-16 L12,-8 L12,4 A12,12 0 0,1 0,14 A12,12 0 0,1 -12,4 L-12,-8 Z"),
    ("target","Target","M0,-16 A16,16 0 0,1 0,16 A16,16 0 0,1 0,-16 M0,-9 A9,9 0 0,1 0,9 A9,9 0 0,1 0,-9 M0,-3 A3,3 0 0,1 0,3 A3,3 0 0,1 0,-3"),
    ("chart","Analytics","M-14,8 L-6,-4 L2,2 L14,-10 M-14,12 L14,12"),
    ("clock","Latency","M0,-14 A14,14 0 0,1 0,14 A14,14 0 0,1 0,-14 M0,-14 L0,0 L8,6"),
    ("cloud","Cloud","M-12,4 A8,8 0 0,1 -4,-4 A10,10 0 0,1 10,-4 A6,6 0 0,1 12,8 L-12,8 Z"),
    ("code","Code","M-10,-8 L-16,0 L-10,8 M10,-8 L16,0 L10,8 M4,-10 L-4,10"),
    ("api","API","M-14,-4 L-14,4 M-14,0 L-6,0 M6,-8 L6,8 M6,0 L14,0 M14,-8 L14,8"),
    ("key","Access","M-12,0 A6,6 0 0,1 0,0 L14,0 L14,8 L10,8 L10,4 L6,4 L6,8 L2,8 L2,0"),
]
ic_body=T("ic-lbl",LM,76,"ICON SYSTEM  ·  LINE WEIGHT 1.25PX  ·  24×24PX GRID",7,"700",DM,ls=3)+L("ic-r",LM,86,RM,86,LN)
COLS=6; ICON_SZ=112; ICON_CX=40
for i,(iid,name,d) in enumerate(ICON_DATA):
    col=i%COLS; row=i//COLS
    ix=LM+col*ICON_SZ+ICON_CX
    iy=108+row*156
    ic_body+=R(f"ib{i}",ix-40,iy,80,80,BG2,2,LN,0.75)
    ic_body+=f'  <path id="ic-{iid}" d="{d}" transform="translate({ix+0},{iy+40})" fill="none" stroke="{WH}" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/>\n'
    ic_body+=T(f"in{i}",ix,iy+96,name,8,"400",DM,"middle")
pages["07-iconography"]=INNER(7,"Iconography",ic_body)

# ── 08  GRID &amp; LAYOUT ─────────────────────────────────────────────
COLS_N=12; COL_W=(RM-LM-(COLS_N-1)*8)//COLS_N
gl_body=(
    T("gl-h",LM,76,"LAYOUT GRID  ·  12-COLUMN  ·  8PX GUTTER",7,"700",DM,ls=3)
    +L("gl-r",LM,86,RM,86,LN)
)
# 12 column markers
for ci in range(COLS_N):
    cx=LM+ci*(COL_W+8)
    gl_body+=(R(f"gc{ci}",cx,100,COL_W,260,"rgba(123,175,212,0.07)",0,AC,0.4)
              +T(f"gn{ci}",cx+COL_W//2,376,str(ci+1),7,"400",DM,"middle"))
# Spacing scale
gl_body+=T("sp-h",LM,408,"SPACING SCALE  ·  BASE 8PX",7,"700",DM,ls=3)+L("sp-r",LM,418,RM,418,LN)
SP=[4,8,12,16,24,32,48,64,96]
for si,sv in enumerate(SP):
    sx=LM+si*128
    gl_body+=(R(f"sp{si}",sx,432,sv,sv,AC,0)+T(f"spl{si}",sx,432+sv+16,f"{sv}px",7,"400",DM))
# Margin note
gl_body+=(T("mg-h",LM,548,"MARGINS",7,"700",DM,ls=3)
          +R("mg-box",LM,560,RM-LM,80,BG2,2,LN,0.75)
          +GRID("mg-g",LM,560,RM-LM,80,24,"rgba(255,255,255,0.04)")
          +R("mg-l",LM,560,64,80,AC,0)+T("mg-lt",LM+32,604,"64px",7,"700",BG,"middle")
          +R("mg-r",RM-64,560,64,80,AC,0)+T("mg-rt",RM-32,604,"64px",7,"700",BG,"middle")
          +T("mg-d",LM+84,604,"← Margin  ·  64px minimum on all sides  ·  Margin →",8,"400",DM))
pages["08-grid-layout"]=INNER(8,"Grid &amp; Layout",gl_body)

# ── 09  LIGHT MODE / PRINT ────────────────────────────────────────────
LBG="#F4F6F8"   # Light background
LBG2="#E8ECF0"  # Light panel
LDARK="#182638" # Dark text on light
LACC="#3A7BAA"  # Darker accent for print

lm_body=(
    T("lm-h",LM,76,"LIGHT MODE  ·  PRINT  ·  DOCUMENT",7,"700","#6B7F90",ls=3)
    +L("lm-r",LM,86,RM,86,"#BCC8D4")
    # Light mode sample
    +R("lm-bg",LM,100,RM-LM,480,LBG,2,"#C8D4DC",0.75)
    +LOGO("lm-logo",LM+60,180,18,LDARK,1.2)
    +TD("lm-nm",LM+96,188,"NEXUS",16,"700",LDARK,ls=3)
    +L("lm-d1",LM+40,210,LM+300,210,"#BCC8D4",0.75)
    +TD("lm-h1",LM+40,246,"Designing for",26,"700",LDARK,ls=-0.5)
    +TD("lm-h2",LM+40,276,"Data Precision",26,"700",LDARK,ls=-0.5)
    +L("lm-hl",LM+40,292,LM+120,292,LACC,1.5)
    +LB("lm-b",LM+40,308,[280,320,300,320,280],g=15,bh=7,c="#BCC8D4")
    +R("lm-btn1",LM+40,424,120,36,LDARK,2)
    +T("lm-bt1",LM+100,448,"Get Started",9,"600","#F0F4F8","middle")
    +R("lm-btn2",LM+176,424,120,36,LBG,2,"#8FA8C0",0.75)
    +T("lm-bt2",LM+236,448,"Learn more",9,"600","#3A5A7A","middle")
    # Right side: document layout preview
    +R("doc-bg",LM+400,112,520,456,WH,2,"#C8D4DC",0.75)
    +R("doc-hdr",LM+400,112,520,48,LBG2,2,"#C8D4DC",0.75)
    +LOGO("doc-lg",LM+432,136,12,LDARK,1.0)
    +TD("doc-nm",LM+458,140,"NEXUS",10,"700",LDARK,ls=3)
    +LB("doc-nav",LM+620,127,[48,48,48,48],g=60,bh=10,c="#BCC8D4")
    +LB("doc-b1",LM+420,176,[420,460,440,460,420,440,460,420,460,440],g=15,bh=8,c="#C8D4DC")
    +R("doc-img",LM+420,340,200,120,LBG2,2,"#C8D4DC",0.75)
    +CYLINDER("doc-cy",LM+520,356,40,88,6,LDARK,0.25,4,2,WH,0.75)
    +LB("doc-b2",LM+636,340,[192,160,192,160,176],g=15,bh=8,c="#C8D4DC")
    # Colour note
    +T("ln-h",LM,604,"LIGHT MODE COLOURS",7,"700","#6B7F90",ls=3)
    +L("ln-r",LM,614,RM,614,"#BCC8D4",0.5)
    +R("lc1",LM,622,80,48,LBG,2,"#C8D4DC",0.5)+T("lc1t",LM+40,670,"F4F6F8",7,"400","#6B7F90","middle")
    +R("lc2",LM+96,622,80,48,LBG2,2,"#C8D4DC",0.5)+T("lc2t",LM+136,670,"E8ECF0",7,"400","#6B7F90","middle")
    +R("lc3",LM+192,622,80,48,LDARK,2)+T("lc3t",LM+232,670,"182638",7,"400","#6B7F90","middle")
    +R("lc4",LM+288,622,80,48,LACC,2)+T("lc4t",LM+328,670,"3A7BAA",7,"400","#6B7F90","middle")
    +R("lc5",LM+384,622,80,48,WH,2,"#C8D4DC",0.5)+T("lc5t",LM+424,670,"FFFFFF",7,"400","#6B7F90","middle")
)
pages["09-light-mode"]=SVG(R("bg",0,0,W,H,LBG)+HDR(9,"Light Mode / Print")+lm_body+FTR())

# ── 10  BRAND APPLICATION ─────────────────────────────────────────────
APP=[
    ("REPORT / DOCUMENT", BG2, "Annual data reports,\nwhitepapers, briefings"),
    ("PRESENTATION",      BG3, "Decks, pitch slides,\nboard materials"),
    ("DASHBOARD / UI",    BG,  "Data interfaces,\nmonitoring systems"),
    ("PRINT / SIGNAGE",   LN,  "Physical collateral,\nevent materials"),
]
ap_body=""
for i,(lbl,col,desc) in enumerate(APP):
    ax=[LM,LM+584][i%2]; ay=[68,368][i//2]
    ap_body+=(T(f"al{i}",ax,ay+18,lbl,7,"700",DM,ls=2)
              +L(f"ar{i}",ax,ay+26,ax+40,ay+26,AC,1.25)
              +IMG(f"am{i}",ax,ay+36,548,232,lbl,col)
              +CYLINDER(f"ac{i}",ax+460,ay+100+48,32,88,5,WH,0.3,3,1,col,0.75)
              +LOGO(f"alo{i}",ax+36,ay+72,12,WH,0.8)
              +T(f"ad{i}",ax,ay+288,desc.replace('\n',' · '),8,"400",DM))
pages["10-brand-application"]=INNER(10,"Brand Application",ap_body)

# ── 11  DO'S &amp; DON'TS ─────────────────────────────────────────────
DW=(RM-LM-3*16)//4
DO_I=["Use the correct logo file","Maintain full clear space",
       "Apply approved colour system","Preserve all line weights"]
DN_I=["Never distort the logo","Never alter the colours",
       "Never crop or mask the mark","Never add effects or shadows"]
dd_body=(
    T("do-h",LM,72,"DO",11,"700",GR,ls=2,ff=FD)
    +T("do-s",LM+40,72,"— follow these rules every time",9,"400",DM)
    +L("do-r",LM,82,RM,82,GR,0.75)
)
for i,lbl in enumerate(DO_I):
    dx=LM+i*(DW+16)
    dd_body+=(R(f"dob{i}",dx,92,DW,168,BG2,2,GR,0.75)
              +R(f"dolg{i}",dx+12,104,DW-24,80,BG,2,LN,0.5)
              +LOGO(f"dol{i}",dx+DW//2,144,18,WH,0.9)
              +CHECK(f"dok{i}",dx+12,186,18,GR)
              +T(f"dot{i}",dx+38,201,lbl,8,"600",MT))
dd_body+=(T("dn-h",LM,298,"DON'T",11,"700",RD,ls=2,ff=FD)
          +T("dn-s",LM+64,298,"— these break the system",9,"400",DM)
          +L("dn-r",LM,308,RM,308,RD,0.75))
for i,lbl in enumerate(DN_I):
    dx=LM+i*(DW+16)
    dd_body+=(R(f"dnb{i}",dx,318,DW,168,BG2,2,RD,0.75)
              +R(f"dnlg{i}",dx+12,330,DW-24,80,BG,2,LN,0.5)
              +LOGO(f"dnl{i}",dx+DW//2,370,18,WH,0.9)
              +CROSS(f"dnx{i}",dx+12,412,18,RD)
              +T(f"dnt{i}",dx+38,427,lbl,8,"600",MT))
# Golden rule
dd_body+=(L("gr-t",LM,516,RM,516,LN)
          +R("gr-box",LM,524,RM-LM,80,BG2,0,LN,0.75)
          +T("gr-h",LM+24,548,"GOLDEN RULE",7,"700",AC,ls=3)
          +T("gr-t1",LM+24,568,"The logo and visual system are non-negotiable. Always request approved files",9,"400",MT)
          +T("gr-t2",LM+24,586,"from the brand team. Never recreate or approximate from screenshots.",9,"400",MT))
pages["11-dos-and-donts"]=INNER(11,"Do's &amp; Don'ts",dd_body)

# ── 12  BRAND SUMMARY  /  THANK YOU ───────────────────────────────────
pages["12-brand-summary"]=SVG(
    BKG()+GRID("bg-g")
    +L("tp",0,0,W,0,WH,0.5)
    +T("n12",LM,40,"12.",8,"400",DM,ls=1)
    +T("s12",LM+36,40,"BRAND SUMMARY",8,"600",MT,ls=3)
    +T("r12",RM,40,"NEXUS",8,"700",DM,"end",ls=4)
    +L("hdiv",LM,50,RM,50,LN,0.5)
    # Left: text summary
    +T("bs-hdr",LM,84,"12.",8,"600",DM)+T("bs-tl",LM+28,84,"BRAND SUMMARY",8,"700",DM,ls=3)
    +L("bs-r",LM,94,LM+480,94,LN)
    +LB("bs-b",LM,108,[420,480,452,480,420,480,452,420,480,452,420,480],g=15,bh=8)
    +TD("ty1",LM,300,"Thank",60,"700",WH,ls=-2)
    +TD("ty2",LM,364,"You.",60,"700",AC,ls=-2)
    +L("ty-r",LM,380,LM+140,380,MT,1.5)
    +T("ty-s1",LM,406,"NEXUS represents a commitment to precision,",9,"400",DM)
    +T("ty-s2",LM,424,"clarity and intelligence at scale.",9,"400",DM)
    +T("ty-s3",LM,452,"This system ensures we show up with intention",9,"400",DM)
    +T("ty-s4",LM,470,"— everywhere, consistently.",9,"400",DM)
    +T("ty-yr",LM,514,"© 2024 NEXUS  ·  All rights reserved",7,"400",DM,ls=0.5)
    +T("ty-c",LM,530,"brand@nexus.io  ·  nexus.io",7,"400",DM,ls=0.5)
    # Right: Technical cylinder composition
    +CYLINDER("tc1",920,72,120,380,18,WH,1.0,14,3,BG,1.25)
    +CYLINDER("tc2",1100,180,72,240,11,WH,0.6,6,2,BG,0.85)
    +CYLINDER("tc3",1168,300,40,120,7,AC,0.45,4,1,BG,0.7)
    +f'  <path id="tc-f1" d="M1040,280 C1060,280 1070,280 1028,280" fill="none" stroke="{LN}" stroke-width="0.75" stroke-dasharray="3,3"/>\n'
    +LOGO("ty-logo",LM+240,600,18,DM,0.75)
    +L("fdiv",LM,H-40,RM,H-40,LN,0.5)
    +T("fl",LM,H-20,"NEXUS BRAND GUIDELINES  ·  VERSION 1.0  ·  2024",8,"400",DM,ls=1)
    +T("fr",RM,H-20,"nexus.io",8,"400",DM,"end",ls=1)
)

# ── Write all files ───────────────────────────────────────────────────
for name,content in sorted(pages.items()):
    path=os.path.join(OUT,f"page-{name}.svg")
    with open(path,"w",encoding="utf-8") as fh:
        fh.write(content)
    print(f"  ✓  page-{name}.svg")

print(f"\n✅  {len(pages)} pages → {OUT}/")
