#!/usr/bin/env python3
"""
Generate UI/UX design briefs for the UML stencil toolkit.

Output:
  briefs/system/*.md           — application-level briefs
  briefs/categories/*.md       — per-category briefs (15)
  briefs/shapes/<cat>/<id>.md  — per-shape briefs (~204)
  briefs/BRIEFS_INDEX.md

Design direction: PrimeReact (Lara) enterprise UI aesthetics.
Template: ../UI-UX_Design_Brief_Template.md
Glossary: ../ui-design-glossary.md
"""
from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
BRIEFS = Path(__file__).resolve().parent
SVG_ROOT = ROOT / "svg"
sys.path.insert(0, str(SVG_ROOT))

from shape_catalog import CATEGORIES, Shape  # noqa: E402

OUT_SYSTEM = BRIEFS / "system"
OUT_CATEGORIES = BRIEFS / "categories"
OUT_SHAPES = BRIEFS / "shapes"
INDEX = BRIEFS / "BRIEFS_INDEX.md"

TEMPLATE = "../UI-UX_Design_Brief_Template.md"
GLOSSARY = "../ui-design-glossary.md"
PRIMEREACT = "./PRIMEREACT_DESIGN_DIRECTION.md"
STYLE = "../svg/STYLE_GUIDE.md"

PRIMEREACT_BLURB = (
    "PrimeReact-inspired enterprise UI — layered **surface** backgrounds, "
    "6px **border-radius** on **cards**/**panels**, primary blue selection accent (`#3B82F6`), "
    "subtle **shadow-sm** elevation, compact **sidebar**/**tree** density, and "
    "150–200ms **microinteractions**. See [PRIMEREACT_DESIGN_DIRECTION.md](./PRIMEREACT_DESIGN_DIRECTION.md)."
)

# ASCII templates for shape families on canvas (PrimeReact-styled selection)
ASCII_SHAPE: Dict[str, str] = {
    "shape": """```
Palette thumbnail (Prime Panel tile, 48×48):
+--------------------------------+
|  [shape preview]               |  <- surface-0, border surface-200
|  Rectangle                     |  <- 12px label, muted if inactive
+--------------------------------+

On canvas — selected (primary affordance):
+--------------------------------+
|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  primary-50 fill
|░░  +------------------+  ░░░░░░|  primary stroke 2px
|░░  | Class / Node     |  ░░░░░░|
|░░  +------------------+  ░░░░░░|
|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
+--------------------------------+
```""",
    "connector": """```
Connector on canvas (default stroke surface-700):
  Node A  ───────────────▶  Node B

Selected connector (primary-color stroke):
  Node A  ═══════════════▶  Node B   [handles at endpoints]

Toolbar (Prime Toolbar) — active line tool highlighted primary.
```""",
    "marker": """```
Marker node (initial/final/decision dot):
  ●  solid primary or surface-900 fill
  ◉  ring marker — stroke surface-700, fill surface-0

Selected: primary ring + focus-ring shadow.
```""",
    "annotation": """```
Text annotation (no SVG asset — Prime InputText / inline label):
  {constraint}   or   [guard]   or   1..*

Rendered as muted caption (text-muted-color) near parent shape.
```""",
}

ASCII_SYSTEM: Dict[str, str] = {
    "stencil-system": """```
+------------------------------------------------------------------------+
| STENCIL SYSTEM — PrimeReact app shell                                  |
+----------+-------------------------------------------------------------+
| Sidebar  | Toolbar + Menubar (File Edit View Arrange)                  |
| Accordion|-------------------------------------------------------------|
| 15 cats  | Infinite canvas | minimap (optional) | rulers (optional)  |
| search   |                                                             |
| tree     | Multi-select | snap grid | alignment guides                |
+----------+----------+--------------------------------------------------+
|          | Inspector TabView | Toast top-right | Dialog export        |
+------------------------------------------------------------------------+
```""",
    "stencil-palette-ui": """```
+-- Shape Palette (Prime Sidebar + Accordion) --+
| [🔍 Search shapes................] [filter]|
|----------------------------------------------|
| > Basic Geometric          (16)              |
|   [▭] [▭r] [◻] [◯] [◇] ...  scroll grid     |
| > UML Class                (16)              |
|   [class] [interface] [enum] ...             |
| > Architecture             (20)              |
|----------------------------------------------|
| Drag tile → canvas  |  Double-click to insert|
| Hover: surface-100  |  Active: primary ring |
+----------------------------------------------+
```""",
    "diagram-canvas-ui": """```
+-- Diagram Canvas (Prime Panel content area) --+
| Toolbar: | pointer | hand | connector v | zoom |
|------------------------------------------------|
| · · · · · · · · · · · · · · ·  surface-50 grid |
| · ·  +-------+  ───────▶  +-------+  · · · · |
| · ·  |Service|             | DB    |  · · · · |
| · ·  +-------+             +-------+  · · · · |
| · · · · · · · · · · · · · · · · · · · · · · · |
|------------------------------------------------|
| ContextMenu on right-click | marquee select    |
+------------------------------------------------+
```""",
    "export-dialog-ui": """```
+-- Export Dialog (Prime Dialog) -------------+
| Export Diagram                        [ x ] |
|---------------------------------------------|
| Format:  ( ) PNG  (•) SVG  ( ) PDF         |
| Scale:   [ 100% v ]   Include background   |
| [ ] Embed fonts    [ ] Prime theme tokens   |
|---------------------------------------------|
| Preview thumbnail (Card, surface-100)       |
|---------------------------------------------|
|              [ Cancel ]  [ Export -> ]      |
+---------------------------------------------+
```""",
}

CATEGORY_GLOSSARY: Dict[str, Tuple[str, ...]] = {
    "basic-geometric": ("Grid", "Alignment", "Container", "Visual Hierarchy"),
    "uml-class": ("Card", "Typography", "Affordance", "Progressive Disclosure"),
    "uml-use-case": ("Container", "Actor", "Boundary", "Use Case"),
    "uml-sequence": ("Timeline", "Interaction", "Focus", "Microinteraction"),
    "uml-activity": ("Wizard", "Decision", "Swimlane", "Flow"),
    "uml-state-machine": ("State", "Transition", "Visual Hierarchy"),
    "uml-component-deployment": ("Component", "Interface", "Node", "Deployment"),
    "uml-package": ("Folder", "Namespace", "Taxonomy"),
    "architecture": ("Card", "Grid", "System Context", "Microservice"),
    "data-database": ("Data Grid", "Table", "Relationship"),
    "cloud-architecture": ("Cloud", "Region", "Service", "Card"),
    "infrastructure-network": ("Network", "Subnet", "Firewall", "Topology"),
    "process-flow": ("Flowchart", "Decision", "Process", "Document"),
    "connector-line": ("Connector", "Arrow", "Dependency", "Line"),
    "miscellaneous": ("Legend", "Note", "Annotation", "Title Block"),
}

CATEGORY_ASCII: Dict[str, str] = {
    "basic-geometric": """```
Category strip in palette (Prime Accordion header):
> Basic Geometric                                    [16]

Tile grid (4 cols, gap 8px, Card-like tiles):
[▭ rect] [▭ rnd] [◻ sq] [◯ cir] [◇ dia] [⬡ hex] [⬢ cyl] [📁 folder]
[── line] [──▶ arr] [─ ─ dash] [· · dot]
```""",
    "uml-class": """```
Palette section + canvas example:
> UML Class

[class 3-comp] [<<interface>>] [<<enumeration>>] [*abstract*]

Canvas:
┌─────────────┐         ┌─────────────┐
│ Order       │◇────────│ Customer    │
├─────────────┤         └─────────────┘
│ + id: int   │
└─────────────┘
```""",
    "uml-sequence": """```
Canvas (lifelines on surface-50, activation bars primary-50):
┌────┐      ┌────┐      ┌────┐
│ UI │      │ API│      │ DB │
└─┬──┘      └─┬──┘      └─┬──┘
  │──request──▶│           │
  │            │──query───▶│
  │◀──response─│◀──rows────│
```""",
}


def _category_ascii(cat_id: str) -> str:
    return CATEGORY_ASCII.get(cat_id, ASCII_SHAPE["shape"])


def _shape_ascii(shape: Shape) -> str:
    if shape.asset_type in ASCII_SHAPE:
        return ASCII_SHAPE[shape.asset_type]
    return ASCII_SHAPE["shape"]


def _tokens_block() -> str:
    return """| State | Stroke | Fill | Notes |
|-------|--------|------|-------|
| Default | `#e2e8f0` / `#334155` | `#ffffff` | surface-200 / surface-700 |
| Hover | `#94a3b8` | `#f8fafc` | surface-400 hint |
| Selected | `#3B82F6` | `#EFF6FF` | primary / primary-50 |
| Disabled | `#cbd5e1` | `#f1f5f9` | 50% opacity |
| Focus ring | — | — | `0 0 0 2px #BFDBFE` on wrapper |"""


def _states_table() -> str:
    return """| State | When | PrimeReact-aligned requirement |
|-------|------|--------------------------------|
| **Default** | Placed on canvas | surface stroke/fill per tokens |
| **Hover** | Pointer over shape | Slight stroke darken; tile `surface-100` in palette |
| **Focus** | Keyboard selected | **Focus** ring like Prime **Button** |
| **Selected** | Marquee or click | Primary border — like **DataTable** row select |
| **Active** | Dragging/resizing | `shadow-md`, cursor affordance |
| **Disabled** | Locked layer | Muted + **tooltip** explaining lock |
| **Error** | Invalid connection | Prime **Message** severity error inline |
| **Loading** | Importing stencil | **Skeleton** tile placeholders in palette |"""


def _a11y_block() -> str:
    return """- Shape tiles: `aria-label` = shape name; draggable with keyboard alternative.
- Canvas: arrow-key nudge (1px, 10px with Shift); **tab order** through selection handles.
- Inspector fields: Prime **InputText** / **Dropdown** with visible **focus** rings.
- **Contrast ratio** ≥ 4.5:1 for labels on shape fills (WCAG AA).
- Honour `prefers-reduced-motion` for snap/guide animations."""


def _system_brief(key: str, title: str, goal: str, personas: str, flow: str) -> str:
    ascii_block = ASCII_SYSTEM[key]
    return f"""# {title} — UI/UX Design Brief

**Project:** UML-SKILLS Stencil Toolkit  
**Area:** System / application chrome  
**Version:** 1.0  
**Template:** [{TEMPLATE}]({TEMPLATE})  
**Glossary:** [{GLOSSARY}]({GLOSSARY})  
**Design direction:** [{PRIMEREACT}]({PRIMEREACT})

---

## 1. Overview & Objectives

- **Goal:** {goal}
- **UX objectives:** Enterprise **task success rate**, low cognitive load, keyboard-efficient diagramming, excellent **legibility** on dense diagrams.
- **Aesthetic:** {PRIMEREACT_BLURB}

## 2. Target Audience & User Journey

- **Personas:** {personas}
- **Primary flow:** {flow}
- **Glossary terms:** **Sidebar**, **Toolbar**, **Panel**, **Dialog**, **Toast**, **Grid**, **Affordance**

## 3. Layout & Structure (ASCII wireframe)

{ascii_block}

## 4. PrimeReact Component Mapping

| Region | PrimeReact component | Notes |
|--------|---------------------|-------|
| Navigation | **Sidebar**, **Accordion**, **Tree** | 15 shape categories |
| Commands | **Toolbar**, **Button**, **SplitButton** | Icon + label tools |
| Canvas | **Panel** (content) | `surface-50` background |
| Inspector | **Panel**, **TabView**, **InputText** | Property editing |
| Feedback | **Toast**, **Dialog**, **ConfirmDialog** | Export, errors |
| Search | **IconField**, **InputText** | Filter palette |

## 5. Typography & Spacing

- **Font:** Inter, system-ui fallback — matches PrimeReact Lara.
- Body 14px; canvas labels 12px; inspector labels 12px **muted**.
- **Padding:** 12px panel body; 8px palette tile gap; **margin** 16px between sidebar and canvas.

## 6. Colour & Tokens

{_tokens_block()}

Full token map: [PRIMEREACT_DESIGN_DIRECTION.md]({PRIMEREACT}) and [STYLE_GUIDE.md]({STYLE}).

## 7. Interaction & Microinteractions

- Palette tile **hover** 150ms `ease-out` background transition.
- Drag from palette: ghost preview at 60% **opacity**; snap **microinteraction** 200ms.
- **Toast** on export success (top-right, 3s).
- **Dialog** entry 250ms; honour `prefers-reduced-motion`.

## 8. UI States

{_states_table()}

## 9. Accessibility (WCAG 2.1 AA)

{_a11y_block()}

## 10. Deliverables Checklist

- [ ] Light + dark PrimeReact theme variants
- [ ] Desktop + tablet **breakpoint** (collapsible **sidebar** to **drawer**)
- [ ] State matrix for palette, canvas selection, export **dialog**
- [ ] Figma components mirroring PrimeReact patterns
- [ ] Developer handoff: React + PrimeReact component map

---

_Reference glossary: [{GLOSSARY}]({GLOSSARY})_
"""


def _category_brief(cat_id: str, cat_name: str, shapes: List[Shape]) -> str:
    glossary = ", ".join(f"**{g}**" for g in CATEGORY_GLOSSARY.get(cat_id, ("Visual Hierarchy", "Grid")))
    shape_list = ", ".join(f"`{s.id}`" for s in shapes[:8])
    if len(shapes) > 8:
        shape_list += f", … (+{len(shapes) - 8} more)"
    return f"""# {cat_name} — Category Design Brief

**Project:** UML-SKILLS Stencil Toolkit  
**Category ID:** `{cat_id}`  
**Shape count:** {len(shapes)}  
**Version:** 1.0  
**Template:** [{TEMPLATE}]({TEMPLATE})  
**Glossary:** [{GLOSSARY}]({GLOSSARY})  
**Design direction:** [{PRIMEREACT}]({PRIMEREACT})

---

## 1. Overview & Objectives

- **Goal:** Present and render **{cat_name}** shapes with consistent PrimeReact enterprise aesthetics in the palette and on the diagram canvas.
- **Scope:** {len(shapes)} stencil shapes — see [SHAPE_LIBRARY.md](../svg/SHAPE_LIBRARY.md).
- **Aesthetic:** {PRIMEREACT_BLURB}

## 2. Target Audience & Context

- **Personas:** Software architects, business analysts, developers, technical writers.
- **Usage:** Drag from palette **sidebar** onto canvas; edit via inspector **panel**; export via **dialog**.
- **Glossary terms:** {glossary}

## 3. Palette Presentation (ASCII)

{_category_ascii(cat_id)}

## 4. Canvas Rendering Rules

{_tokens_block()}

- SVG source: `svg/shapes/{cat_id}/<shape-id>.svg`
- Regenerate assets: `python svg/scripts/generate_shapes.py --only {cat_id}`
- Sprite symbol: `svg/shapes/sprite.svg#{shapes[0].id if shapes else 'id'}`

## 5. Shapes in this category

{shape_list}

## 6. Interaction & States

{_states_table()}

## 7. Accessibility

{_a11y_block()}

## 8. Deliverables Checklist

- [ ] Palette **accordion** section for `{cat_id}`
- [ ] Thumbnail tiles for each shape (48×48, **border-radius** 6px)
- [ ] Canvas default + selected + **focus** states per shape
- [ ] Dark mode token overrides

---

_Reference glossary: [{GLOSSARY}]({GLOSSARY})_
"""


def _shape_brief(shape: Shape, cat_id: str, cat_name: str) -> str:
    glossary_terms = CATEGORY_GLOSSARY.get(cat_id, ("Affordance", "Visual Hierarchy"))
    glossary = ", ".join(f"**{g}**" for g in glossary_terms[:3])
    svg_path = f"../svg/shapes/{cat_id}/{shape.id}.svg" if shape.delivery != "annotation" else "— (annotation)"
    delivery_note = {
        "generate": "Auto-generated SVG — restyle with Prime tokens in `generate_shapes.py`.",
        "manual": "Hand-crafted SVG required — follow [STYLE_GUIDE.md](../svg/STYLE_GUIDE.md).",
        "annotation": "Text-only UML convention — render as inline label on canvas.",
    }.get(shape.delivery, "")

    return f"""# {shape.name} — Shape Design Brief

**Project:** UML-SKILLS Stencil Toolkit  
**Category:** {cat_name} (`{cat_id}`)  
**Shape ID:** `{shape.id}`  
**Asset type:** `{shape.asset_type}` | **Delivery:** `{shape.delivery}`  
**SVG:** `{svg_path}`  
**Version:** 1.0  
**Template:** [{TEMPLATE}]({TEMPLATE})  
**Glossary:** [{GLOSSARY}]({GLOSSARY})

---

## 1. Overview & Objectives

- **Goal:** {shape.purpose}
- **Description:** {shape.description}
- **Visual notation:** `{shape.visual}`
- **Aesthetic:** PrimeReact-aligned — clean strokes, **surface** fills, primary selection accent. See [PRIMEREACT_DESIGN_DIRECTION.md](../PRIMEREACT_DESIGN_DIRECTION.md).

## 2. Usage Context

- **Diagram types:** {cat_name} diagrams.
- **Palette tile:** 48×48 **card** tile in `{cat_id}` **accordion** section.
- **Glossary terms:** {glossary}
- **Notes:** {delivery_note} {shape.notes or ""}

## 3. Layout & Structure (ASCII)

{_shape_ascii(shape)}

## 4. PrimeReact Token Mapping

{_tokens_block()}

## 5. UI States (on canvas)

{_states_table()}

## 6. Inspector Properties (Prime Panel fields)

| Property | Control | Default |
|----------|---------|---------|
| Label | **InputText** | `{shape.name}` |
| Stroke | **ColorPicker** | `#334155` |
| Fill | **ColorPicker** | `#ffffff` |
| Stroke width | **InputNumber** | 1.5 |
| Visible | **ToggleButton** | on |

## 7. Accessibility

- Tile `aria-label="{shape.name}"`; canvas shape `role="img"` with descriptive label.
- **Keyboard accessible** move/resize when selected.
- **Contrast ratio** check for text inside shape bounds.

## 8. Deliverables Checklist

- [ ] SVG asset at `{svg_path}`
- [ ] Palette thumbnail (default + **hover** + **focus**)
- [ ] Canvas instance (default + selected)
- [ ] Listed in `sprite.svg` symbol `#{shape.id}`

---

_Reference glossary: [{GLOSSARY}]({GLOSSARY})_
"""


SYSTEM_BRIEFS = [
    ("stencil-system", "Stencil System", "End-to-end diagramming app shell for UML & architecture stencils.",
     "Enterprise architects, developers, BA/PMs creating technical diagrams.",
     "Open app → browse palette → compose diagram → inspect properties → export SVG/PNG."),
    ("stencil-palette-ui", "Stencil Palette UI", "Left sidebar for discovering and inserting shapes.",
     "Power users who need fast shape lookup across 200+ stencils.",
     "Search/filter → expand category → drag or double-click shape → place on canvas."),
    ("diagram-canvas-ui", "Diagram Canvas UI", "Central infinite canvas with tools, grid, and selection.",
     "Diagram authors placing and connecting shapes.",
     "Select tool → place/move shapes → connector tool → link nodes → multi-select → align."),
    ("export-dialog-ui", "Export Dialog UI", "Export finished diagrams to SVG, PNG, or PDF.",
     "Authors sharing diagrams in docs, slides, or wikis.",
     "File → Export → choose format → preview → confirm → **toast** success."),
]


def write_index() -> None:
    lines = [
        "# UML Stencil Toolkit — Design Briefs Index",
        "",
        f"**Design direction:** [PrimeReact](https://primereact.org/) (Lara) enterprise UI",
        "",
        "References:",
        f"- [{TEMPLATE}]({TEMPLATE})",
        f"- [{GLOSSARY}]({GLOSSARY})",
        f"- [{PRIMEREACT}]({PRIMEREACT})",
        f"- [svg/STYLE_GUIDE.md](../svg/STYLE_GUIDE.md)",
        "",
        "Regenerate: `python briefs/generate_briefs.py`",
        "",
        "## System briefs",
        "",
    ]
    for key, title, *_ in SYSTEM_BRIEFS:
        lines.append(f"- [{title}](./system/{key}.md)")
    lines += ["", "## Category briefs", ""]
    for cat in CATEGORIES:
        lines.append(f"- [{cat.name}](./categories/{cat.id}.md) — {len(cat.shapes)} shapes")
    total = sum(len(c.shapes) for c in CATEGORIES)
    lines += [
        "",
        "## Shape briefs",
        "",
        f"**{total}** shape briefs under `briefs/shapes/<category>/<shape-id>.md`",
        "",
        "See [svg/SHAPE_LIBRARY.md](../svg/SHAPE_LIBRARY.md) for the full catalog.",
    ]
    INDEX.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    OUT_SYSTEM.mkdir(parents=True, exist_ok=True)
    OUT_CATEGORIES.mkdir(parents=True, exist_ok=True)
    OUT_SHAPES.mkdir(parents=True, exist_ok=True)

    for key, title, goal, personas, flow in SYSTEM_BRIEFS:
        (OUT_SYSTEM / f"{key}.md").write_text(
            _system_brief(key, title, goal, personas, flow), encoding="utf-8"
        )

    shape_count = 0
    for cat in CATEGORIES:
        (OUT_CATEGORIES / f"{cat.id}.md").write_text(
            _category_brief(cat.id, cat.name, cat.shapes), encoding="utf-8"
        )
        cat_dir = OUT_SHAPES / cat.id
        cat_dir.mkdir(parents=True, exist_ok=True)
        for shape in cat.shapes:
            (cat_dir / f"{shape.id}.md").write_text(
                _shape_brief(shape, cat.id, cat.name), encoding="utf-8"
            )
            shape_count += 1

    write_index()
    print(f"Wrote {len(SYSTEM_BRIEFS)} system briefs")
    print(f"Wrote {len(CATEGORIES)} category briefs")
    print(f"Wrote {shape_count} shape briefs")
    print(f"Index: {INDEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
