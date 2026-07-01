# drawio XML & File-Organization Guide

If you already have a separate drawio-generation skill/tool, use it for the
actual XML mechanics and treat this file only as the **style and organization
spec** it should follow. If you don't have one, this file is also a complete
enough reference to hand-author or script the `.drawio` file directly — start
from `assets/pattern-templates.drawio`, which already contains three fully
built, valid example frames (open it in https://app.diagrams.net or the
desktop app to see them).

## 1. File & page organization

One `.drawio` file, multiple **pages** (tabs along the bottom). Don't put
every screen on one page — it becomes unreadable. Recommended page split:

1. `00 - Cover & Legend` — title, the 5 required screens checklist, a small
   key explaining the grayscale + accent-color convention, and a thumbnail
   index of every other page.
2. `01 - Auth & Onboarding`
3. `02 - Customer App`
4. `03 - Kitchen Staff`
5. `04 - Delivery Rider`
6. `05 - Restaurant Manager`
7. `06 - Administrator`
8. `07 - Customer Support`

Within a page, lay frames out left-to-right in the order a user would
encounter them, and draw a numbered, labeled arrow between frames for the
primary flow (e.g. `Login → Home → Restaurant Details → Food Details → Cart →
Checkout → Payment → Confirmation → Order Tracking`). Label each arrow with
the action that causes the transition, e.g. "Tap menu item". This is what
turns a pile of screens into a wireframe **of the system**, not just a
gallery — make sure this step actually happens, it's easy to skip.

## 2. Canvas / frame sizes

| Context | Frame size (px) | Notes |
|---|---|---|
| Mobile (Customer, Rider, Kitchen-if-tablet) | 360 × 780 | Put a thin gray title bar with the screen name directly above each frame, outside it, so it reads as a label not part of the UI. |
| Desktop (Manager, Admin, Support, Kitchen-if-web) | 1440 × 900 | Same labeling convention above the frame. |
| Modals (Pattern J/M) | size to content, typically 360–480 wide | Draw the dimmed background as a large light-gray rectangle *behind* the modal card, same frame size as the screen it overlays, so it's clear which screen it interrupts. |

Space frames at least 80px apart so flow arrows have room to be drawn cleanly.

## 3. mxCell id rules

Cell ids only need to be unique **within one `<diagram>` page**, not across
the whole file (each page is its own root). Prefix every id with a short
screen code to avoid accidental collisions when copy-pasting frames within a
page, e.g. `login_email`, `home_card0_img`, `admin_kpi2`. The template file
already follows this (`lg_`, `hm_`, `ad_` prefixes).

## 4. Style cheat-sheet (copy these strings exactly)

These are the exact `style=` values used in `assets/pattern-templates.drawio`.
Reuse them so every screen looks consistent.

| Element | Style string |
|---|---|
| Screen frame (outer border) | `rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontSize=13;fontStyle=1;` |
| Frame label (text above frame) | `text;html=1;align=center;verticalAlign=middle;fontSize=16;fontStyle=1;` |
| Status bar | `rounded=0;whiteSpace=wrap;html=1;fillColor=#EFEFEF;strokeColor=#CCCCCC;fontSize=9;align=right;spacingRight=8;fontColor=#666666;` |
| Top app bar | `rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=none;align=left;spacingLeft=12;fontSize=13;fontStyle=1;verticalAlign=middle;` |
| Heading | `text;html=1;align=center;verticalAlign=middle;fontSize=18;fontStyle=1;` |
| Subtext / caption | `text;html=1;align=center;verticalAlign=middle;fontSize=11;fontColor=#666666;` |
| Image / illustration placeholder | `rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=6 4;fillColor=#FAFAFA;strokeColor=#999999;fontColor=#999999;fontSize=11;align=center;verticalAlign=middle;` |
| Input field | `rounded=1;arcSize=14;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;align=left;spacingLeft=12;verticalAlign=middle;fontSize=12;fontColor=#999999;` |
| Primary button (filled) | `rounded=1;arcSize=14;whiteSpace=wrap;html=1;fillColor=#4A6FA5;strokeColor=none;fontColor=#FFFFFF;fontStyle=1;align=center;verticalAlign=middle;fontSize=13;` |
| Outline / secondary button | `rounded=1;arcSize=14;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;align=center;verticalAlign=middle;fontSize=13;` |
| Text link | `text;html=1;align=center;verticalAlign=middle;fontSize=11;fontColor=#4A6FA5;` |
| Chip / filter pill | `rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#F0F0F0;strokeColor=#CCCCCC;align=center;verticalAlign=middle;fontSize=10;` |
| Card (list item container) | `rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#DDDDDD;verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;fontSize=11;` |
| Bottom-nav item (inactive) | `text;html=1;align=center;verticalAlign=middle;fontSize=10;` |
| Bottom-nav item (active) | `text;html=1;align=center;verticalAlign=middle;fontSize=10;fontStyle=1;fontColor=#4A6FA5;` |
| Section label | `text;html=1;align=left;verticalAlign=middle;fontSize=13;fontStyle=1;` |
| Sidebar background (desktop) | `rounded=0;whiteSpace=wrap;html=1;fillColor=#1F2A37;strokeColor=none;` |
| Sidebar nav item (active background) | `rounded=0;whiteSpace=wrap;html=1;fillColor=#374151;strokeColor=none;` |
| Sidebar nav item text | `text;html=1;align=left;verticalAlign=middle;fontSize=12;fontColor=#D1D5DB;spacingLeft=12;` |
| KPI / stat card | `rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#F9FAFB;strokeColor=#E5E7EB;align=left;spacingLeft=12;verticalAlign=top;spacingTop=10;fontSize=11;` |
| Table header cell | `rounded=0;whiteSpace=wrap;html=1;fillColor=#F3F4F6;strokeColor=#E5E7EB;align=left;spacingLeft=8;fontSize=10;fontStyle=1;` |
| Table row (even) | `rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#E5E7EB;align=left;spacingLeft=8;fontSize=10;` |
| Table row (odd / zebra) | `rounded=0;whiteSpace=wrap;html=1;fillColor=#FAFAFA;strokeColor=#E5E7EB;align=left;spacingLeft=8;fontSize=10;` |
| Status badge (pill) | `rounded=1;arcSize=40;whiteSpace=wrap;html=1;fillColor=#E7F3E8;strokeColor=none;fontColor=#1F7A33;align=center;verticalAlign=middle;fontSize=9;fontStyle=1;` |
| Flow arrow between screens | edge style `edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#333333;fontSize=10;` with the action label as the edge's `value` |
| Dimmed modal background | `rounded=0;whiteSpace=wrap;html=1;fillColor=#000000;opacity=15;strokeColor=none;` placed behind (lower in z-order / earlier in the XML) the modal card |

Color palette in use — don't introduce others:
`#FFFFFF` (surfaces), `#000000` (text/borders), `#999999`/`#CCCCCC`/`#E5E7EB`/`#DDDDDD`
(grays for borders/secondary text/dividers), `#F9FAFB`/`#F3F4F6`/`#FAFAFA`
(very light gray fills), `#1F2A37`/`#374151` (dark sidebar only), `#4A6FA5`
(the one accent — primary buttons + links + active nav state only), `#1F7A33`
on `#E7F3E8` (status-success badge only — fine to reuse the same two colors
inverted/relabeled for warning/error badges if you need them, e.g. amber or
red, but keep it to one extra pair, don't rainbow the badges).

## 5. Parent/child coordinates — the one rule that breaks diagrams if missed

When a child cell's `parent` attribute is another **vertex** (e.g. the screen
frame), its `<mxGeometry x y>` is **relative to that parent's top-left
corner**, not the page. When `parent="1"` (the default layer), coordinates
are absolute page coordinates. Always set every screen's outer frame to
`parent="1"`, then every element inside that screen to `parent="<frame_id>"`
with coordinates relative to the frame (0,0 = top-left of the phone/desktop
frame). This is exactly what `pattern-templates.drawio` does — copy that
structure for every new screen rather than recalculating absolute page
coordinates by hand.

## 6. Optional: drawio's built-in Mockup shape library

drawio/diagrams.net ships a "Mockups" shape category (More Shapes → Mockups,
or search the shape panel for "mockup") with ready-made wireframe components
— phone frames, nav bars, real-looking buttons/checkboxes, browser chrome,
etc. If it's available in your environment, feel free to swap it in for nicer
results. It is **not required** — the plain-rectangle style cheat-sheet above
already produces a complete, consistent wireframe and is guaranteed to render
correctly with no special shape libraries enabled, which matters more for a
deliverable you'll be submitting/grading than visual polish.

## 7. Build order

1. Open `assets/pattern-templates.drawio`. Confirm it renders correctly first
   — if it doesn't open cleanly, something about the target drawio version
   differs and you should debug that before generating 90 more screens the
   same way.
2. Create the 8 pages listed in §1.
3. Build the 🔴 REQUIRED screens first, on their respective pages, using the
   matching pattern.
4. Work through 🟠 CORE, then 🟡 RECOMMENDED, per `screen-inventory.md`.
5. Add the flow arrows last, once the screens they connect actually exist.
6. Do a final pass: every frame has a label above it, every page has a
   consistent frame size, no stray default-blue drawio shapes (everything
   should be grayscale + the one accent color).
