#!/usr/bin/env python3
"""
Generate UI/UX design briefs for the diagram template library (86 templates).

Output:
  brief/system/*.md              — application-level briefs (4)
  brief/categories/*.md          — per-category briefs (10)
  brief/templates/<cat>/<id>.md  — per-template briefs (86)
  brief/BRIEFS_INDEX.md

Design direction: PrimeReact (Lara) — see stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md
Template: ../../stencils/UI-UX_Design_Brief_Template.md
Glossary: ../../stencils/ui-design-glossary.md
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

BRIEFS = Path(__file__).resolve().parent
TEMPLATES_ROOT = BRIEFS.parent
SVG_ROOT = TEMPLATES_ROOT / "svg"
sys.path.insert(0, str(SVG_ROOT))

from template_catalog import Template, all_templates  # noqa: E402

OUT_SYSTEM = BRIEFS / "system"
OUT_CATEGORIES = BRIEFS / "categories"
OUT_TEMPLATES = BRIEFS / "templates"
INDEX = BRIEFS / "BRIEFS_INDEX.md"

TEMPLATE_REF = "../../stencils/UI-UX_Design_Brief_Template.md"
GLOSSARY = "../../stencils/ui-design-glossary.md"
PRIMEREACT = "../../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md"
STYLE = "../svg/STYLE_GUIDE.md"
LIBRARY = "../svg/TEMPLATE_LIBRARY.json"
STENCIL_LIBRARY = "../../stencils/svg/SHAPE_LIBRARY.md"

PRIMEREACT_BLURB = (
    "PrimeReact-inspired enterprise UI — layered **surface** backgrounds, "
    "6px **border-radius** on **cards**/**panels**, primary blue accent (`#3B82F6`), "
    "subtle elevation, compact gallery density, and 150–200ms **microinteractions**. "
    "See [PRIMEREACT_DESIGN_DIRECTION.md]({PRIMEREACT})."
).format(PRIMEREACT=PRIMEREACT)

CATEGORY_NAMES: Dict[str, str] = {
    "uml": "UML Diagrams",
    "architecture": "Architecture Diagrams",
    "infrastructure": "Infrastructure Diagrams",
    "project-management": "Project Management Diagrams",
    "stakeholder": "Stakeholder Diagrams",
    "process-flow": "Process & Flow Diagrams",
    "data": "Data & Database Diagrams",
    "gis": "GIS Diagrams",
    "cloud": "Cloud Architecture Diagrams",
    "devops": "DevOps & CI/CD Diagrams",
}

CATEGORY_GLOSSARY: Dict[str, Tuple[str, ...]] = {
    "uml": ("Card", "Container", "Visual Hierarchy", "Progressive Disclosure"),
    "architecture": ("Grid", "System Context", "Layer", "Visual Hierarchy"),
    "infrastructure": ("Network", "Topology", "Container", "Grid"),
    "project-management": ("Timeline", "Data Grid", "Wizard", "Progress Indicator"),
    "stakeholder": ("Matrix", "Quadrant", "Relationship", "Data Grid"),
    "process-flow": ("Swimlane", "Flow", "Decision", "Wizard"),
    "data": ("Data Grid", "Entity", "Relationship", "Pipeline"),
    "gis": ("Map", "Legend", "Layer", "Flow"),
    "cloud": ("Region", "Service", "Grid", "Migration"),
    "devops": ("Pipeline", "Stage", "Loop", "Observability"),
}

LAYOUT_ASCII: Dict[str, str] = {
    "class_diagram": """```
Template canvas (UML class layout):
+-- [UML Class Diagram]  <Project Name> · Template ------------+
| · grid ·  ┌─────────┐              ┌─────────┐              |
|           │ ClassA  │──1──────────*│ ClassB  │              |
|           │+ attrs  │              │+ attrs  │              |
|           └─────────┘              └─────────┘              |
|                    ┌─────────┐                              |
|                    │ ClassC  │   dashed = placeholder       |
|                    └─────────┘   dotted  = guide line        |
|                                    [ Legend ]                |
+--------------------------------------------------------------+
```""",
    "sequence_diagram": """```
Template canvas (sequence layout):
+-- [UML Sequence Diagram] -----------------------------------+
|  ┌───┐    ┌───┐    ┌───┐    ┌───┐                           |
|  │Obj│    │Obj│    │Obj│    │Obj│   lifeline headers        |
|  └─┬─┘    └─┬─┘    └─┬─┘    └─┬─┘                           |
|    │ - - - -│- - - - │- - - - │   sync() / async() guides   |
|    │░░░░░░░░│        │        │   ░░ = activation placeholder|
|    │        │────────▶        │                              |
+--------------------------------------------------------------+
```""",
    "layered_stack": """```
Template canvas (layered architecture):
+-- [Layered Architecture] ------------------------------------+
| ┌─ Presentation layer ─────────────────────────────────┐  |
| │  [ placeholder components ]                             │  |
| ├─ Business layer ───────────────────────────────────────┤  |
| │  [ placeholder components ]                             │  |
| ├─ Data layer ───────────────────────────────────────────┤  |
| │  [ placeholder components ]                             │  |
| └─ Integration layer ────────────────────────────────────┘  |
+--------------------------------------------------------------+
```""",
    "gantt": """```
Template canvas (Gantt):
+-- [Gantt Chart] ---------------------------------------------+
| Task List          │ Q1      Q2      Q3      Q4  (timeline) |
|────────────────────┼────────────────────────────────────────|
| Task 1             │ ████████░░░░░░░░                        |
| Task 2             │     ░░░░████████                      |
| Task 3             │         ░░░░░░████████                |
+--------------------------------------------------------------+
```""",
    "quadrant_matrix": """```
Template canvas (2×2 matrix):
+-- [Power–Interest Matrix] -----------------------------------+
|              │ Manage Closely │ Keep Satisfied              |
|──────────────┼────────────────┼─────────────────────────────|
| High Power   │                │                             |
|──────────────┼────────────────┼─────────────────────────────|
| Low Power    │ Keep Informed  │ Monitor                     |
+--------------------------------------------------------------+
```""",
    "raci_matrix": """```
Template canvas (RACI grid):
+-- [RACI Matrix] ---------------------------------------------+
| Roles →  │ PM    │ BA    │ Dev   │ QA    │ Ops             |
|──────────┼───────┼───────┼───────┼───────┼─────────────────|
| Task 1   │       │       │       │       │  R/A/C/I cells  |
| Task 2   │       │       │       │       │                 |
| Task 3   │       │       │       │       │                 |
+--------------------------------------------------------------+
```""",
    "matrix": """```
Template canvas (grid matrix):
+-- [Matrix template] -----------------------------------------+
|         │ Col 1   │ Col 2   │ Col 3   │ ...                 |
|─────────┼─────────┼─────────┼─────────┼─────────────────────|
| Row 1   │         │         │         │                     |
| Row 2   │         │         │         │   empty cells =     |
| Row 3   │         │         │         │   fill-in areas     |
+--------------------------------------------------------------+
```""",
}

DEFAULT_TEMPLATE_ASCII = """```
Template canvas (1920×1080 logical):
+-- [Template Title]  <Project Name> · Template ---------------+
| · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · |
| · ·  ┌ - - - - - - - - - - - - - - ┐  · · · · · · · · · · · |
| · ·  │   Placeholder area          │  · · guide line - - -  |
| · ·  │   (dashed border)           │  · · · · · · · · · · · |
| · ·  └ - - - - - - - - - - - - - - ┘  · · · · · · · · · · · |
| · · · · · · · · · · · · · · · · · · · · · · [ Legend ] · · |
| CONFIDENTIAL — Internal          <Project Name> · Version 1.0|
+--------------------------------------------------------------+
```"""

ASCII_SYSTEM: Dict[str, str] = {
    "template-system": """```
+------------------------------------------------------------------------+
| DIAGRAM STUDIO — PrimeReact shell (templates + stencils)               |
+----------+-------------------------------------------------------------+
| Sidebar  | Toolbar: [New] [Open] [Save] | zoom | export                |
| Gallery  |-------------------------------------------------------------|
| OR       |  ACTIVE TEMPLATE CANVAS (1920×1080)                         |
| Stencils |  [primary title bar]  <Project Name>                        |
| TabView  |  grid + dashed placeholders + legend + footer               |
+----------+----------+--------------------------------------------------+
|          | Inspector TabView | Toast | Dialog (new diagram wizard)     |
+------------------------------------------------------------------------+
```""",
    "template-gallery-ui": """```
+-- Template Gallery (Prime DataView / Card grid) ----------+
| [🔍 Search templates........................] [category v] |
|------------------------------------------------------------|
| ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        |
| │ thumb 16:9   │ │ thumb 16:9   │ │ thumb 16:9   │        |
| │ UML Class    │ │ C4 Context   │ │ Gantt Chart  │        |
| │ Diagram      │ │              │ │              │        |
| │ [Use]        │ │ [Use]        │ │ [Use]        │        |
| └──────────────┘ └──────────────┘ └──────────────┘        |
| Categories: UML | Architecture | PM | Cloud | DevOps ...  |
+------------------------------------------------------------+
```""",
    "template-canvas-ui": """```
+-- Active Template Canvas ----------------------------------+
| Toolbar: pointer | pan | stencil insert | replace placeholder|
|-------------------------------------------------------------|
| [■■ Template Title Bar — primary #3B82F6]                   |
| <Project Name> · Template                                   |
|-------------------------------------------------------------|
| · · surface-50 grid (50px) · · · · · · · · · · · · · · · · |
|   ┌ - - - placeholder - - - ┐    - - - guide - - -         |
|   │  Drop stencil here        │                              |
|   └ - - - - - - - - - - - - - ┘                              |
| Snap to grid | alignment guides | placeholder highlight     |
+-------------------------------------------------------------+
```""",
    "new-diagram-wizard-ui": """```
+-- New Diagram Wizard (Prime Dialog / Steps) ----------------+
| New Diagram                                           [ x ] |
| Step 1 of 3 — Choose template                               |
|-------------------------------------------------------------|
| Category: [ UML Diagrams        v ]                         |
|                                                             |
| ( ) UML Class Diagram     ( ) UML Sequence Diagram          |
| ( ) UML Use Case Diagram  ( ) ...                           |
|-------------------------------------------------------------|
| Step 2: Project name [________________________]             |
| Step 3: Page size    [ 1920×1080 (16:9) v ]                 |
|                                                             |
|              [ Cancel ]              [ Create Diagram -> ]  |
+-------------------------------------------------------------+
```""",
}

CATEGORY_ASCII: Dict[str, str] = {
    "uml": """```
Gallery category strip:
> UML Diagrams (14 templates)

Card thumbnails:
[Class] [Sequence] [Use Case] [Activity] [State] [Component] ...
```""",
    "architecture": """```
Gallery category strip:
> Architecture Diagrams (16 templates)

Card thumbnails:
[Enterprise] [C4 Context] [Microservices] [Hexagonal] [Clean] ...
```""",
    "project-management": """```
Gallery category strip:
> Project Management (12 templates)

Card thumbnails:
[Charter] [WBS] [Gantt] [PERT] [Risk Matrix] [Roadmap] ...
```""",
}


def _tokens_block() -> str:
    return """| Element | Token | Value |
|---------|-------|-------|
| Canvas background | surface-0 | `#ffffff` |
| Grid tint | surface-50 | `#f8fafc` |
| Grid lines | surface-200 | `#e2e8f0` |
| Page border | surface-200 | `#e2e8f0` |
| Title bar | primary | `#3B82F6` |
| Title text | on-primary | `#ffffff` |
| Subtitle | primary-50 | `#EFF6FF` |
| Placeholder stroke | placeholder | `#94a3b8` dashed |
| Guide lines | guide | `#cbd5e1` dotted |
| Labels | surface-700 / muted | `#334155` / `#64748b` |
| Layer bands | primary-50 fill | `#EFF6FF` |
| Selected placeholder | primary stroke | `#3B82F6` 2px |"""


def _states_table() -> str:
    return """| State | When | PrimeReact-aligned requirement |
|-------|------|--------------------------------|
| **Default** | Template opened | Dashed placeholders visible on grid |
| **Hover** | Pointer over placeholder | Stroke darken; subtle surface-100 fill |
| **Focus** | Keyboard on placeholder | **Focus** ring `#BFDBFE` on wrapper |
| **Selected** | Placeholder chosen for edit | Primary border — ready to replace |
| **Active** | Dragging stencil onto placeholder | Drop target highlight primary-50 |
| **Filled** | Stencil placed | Solid stroke; placeholder dash removed |
| **Empty** | Project name unset | Subtitle shows `<Project Name>` literal |
| **Loading** | Template SVG loading | **Skeleton** canvas preview in gallery |"""


def _a11y_block() -> str:
    return """- Gallery cards: `aria-label` = template title; keyboard selectable grid.
- Placeholders: `role="region"` with `aria-label` describing intended content.
- Title bar: heading level 1 for template name; project name editable field labelled.
- **Contrast ratio** ≥ 4.5:1 for footer and placeholder labels (WCAG AA).
- Honour `prefers-reduced-motion` for gallery hover and drop-target animations."""


def _template_ascii(template: Template) -> str:
    if template.layout in LAYOUT_ASCII:
        return LAYOUT_ASCII[template.layout]
    if "matrix" in template.layout:
        return LAYOUT_ASCII["matrix"]
    return DEFAULT_TEMPLATE_ASCII


def _category_ascii(cat_id: str) -> str:
    return CATEGORY_ASCII.get(cat_id, """```
Gallery category strip:
> {name}

Card grid of template thumbnails (16:9 preview, primary CTA "Use template").
```""".format(name=CATEGORY_NAMES.get(cat_id, cat_id)))


def _system_brief(key: str, title: str, goal: str, personas: str, flow: str) -> str:
    return f"""# {title} — UI/UX Design Brief

**Project:** UML-SKILLS Diagram Template Library  
**Area:** System / application chrome  
**Version:** 1.0  
**Template:** [{TEMPLATE_REF}]({TEMPLATE_REF})  
**Glossary:** [{GLOSSARY}]({GLOSSARY})  
**Design direction:** [{PRIMEREACT}]({PRIMEREACT})

---

## 1. Overview & Objectives

- **Goal:** {goal}
- **UX objectives:** Fast template selection, clear placeholder affordance, seamless stencil insertion, excellent **legibility** on large-format canvases.
- **Aesthetic:** {PRIMEREACT_BLURB}

## 2. Target Audience & User Journey

- **Personas:** {personas}
- **Primary flow:** {flow}
- **Glossary terms:** **Wizard**, **Card**, **Panel**, **Dialog**, **Grid**, **Affordance**, **Progressive Disclosure**

## 3. Layout & Structure (ASCII wireframe)

{ASCII_SYSTEM[key]}

## 4. PrimeReact Component Mapping

| Region | PrimeReact component | Notes |
|--------|---------------------|-------|
| Template browse | **DataView**, **Card** | 86 templates, category filter |
| New diagram | **Dialog**, **Steps** | 3-step **wizard** |
| Canvas | **Panel** | 1920×1080 logical artboard |
| Stencil insert | **Sidebar**, **DragDrop** | From stencil library |
| Inspector | **TabView**, **InputText** | Project name, page meta |
| Feedback | **Toast**, **ConfirmDialog** | Save, export |

## 5. Typography & Spacing

- **Font:** Inter, system-ui — matches PrimeReact Lara and stencil toolkit.
- Template title 22px semibold; subtitle 12px; placeholder labels 13px; footer 11px **muted**.
- Canvas margin 40px; grid 50px; title bar height 56px; **border-radius** 6px.

## 6. Design Tokens (template chrome)

{_tokens_block()}

Full reference: [{STYLE}]({STYLE}) and [{PRIMEREACT}]({PRIMEREACT}).

## 7. Interaction & Microinteractions

- Gallery card **hover** 150ms `ease-out` elevation (`shadow-sm`).
- **Wizard** step transition 250ms; honour `prefers-reduced-motion`.
- Drop stencil on placeholder: 200ms primary-50 flash confirmation.
- **Toast** on diagram created (top-right, 3s).

## 8. UI States

{_states_table()}

## 9. Accessibility (WCAG 2.1 AA)

{_a11y_block()}

## 10. Deliverables Checklist

- [ ] Light + dark PrimeReact theme variants
- [ ] Gallery responsive **grid** (3–4 columns desktop, 1–2 mobile)
- [ ] State matrix: gallery card, canvas placeholder, filled slot
- [ ] Integration with stencil palette documented
- [ ] Figma artboard components at 1920×1080

---

_Reference glossary: [{GLOSSARY}]({GLOSSARY})_
"""


def _category_brief(cat_id: str, templates: List[Template]) -> str:
    name = CATEGORY_NAMES.get(cat_id, cat_id)
    glossary = ", ".join(f"**{g}**" for g in CATEGORY_GLOSSARY.get(cat_id, ("Visual Hierarchy", "Grid")))
    template_list = ", ".join(f"`{t.id}`" for t in templates[:6])
    if len(templates) > 6:
        template_list += f", … (+{len(templates) - 6} more)"
    return f"""# {name} — Category Design Brief

**Project:** UML-SKILLS Diagram Template Library  
**Category ID:** `{cat_id}`  
**Template count:** {len(templates)}  
**Version:** 1.0  
**Template:** [{TEMPLATE_REF}]({TEMPLATE_REF})  
**Glossary:** [{GLOSSARY}]({GLOSSARY})  
**Design direction:** [{PRIMEREACT}]({PRIMEREACT})

---

## 1. Overview & Objectives

- **Goal:** Help users start **{name.lower()}** quickly with pre-structured blank canvases that match industry diagram conventions.
- **Scope:** {len(templates)} template SVGs — see [{LIBRARY}]({LIBRARY}).
- **Aesthetic:** {PRIMEREACT_BLURB}
- **Companion assets:** Stencil shapes from [{STENCIL_LIBRARY}]({STENCIL_LIBRARY}) fill placeholders on the canvas.

## 2. Target Audience & Context

- **Personas:** Enterprise architects, BAs, PMs, developers, data engineers (varies by sub-type).
- **Usage:** Gallery → select template → name project → replace dashed placeholders with stencil shapes.
- **Glossary terms:** {glossary}

## 3. Gallery Presentation (ASCII)

{_category_ascii(cat_id)}

## 4. Template Canvas Chrome (shared)

All templates in this category share:

{_tokens_block()}

- SVG folder: `svg/{cat_id}/`
- Regenerate: `python svg/scripts/generate_templates.py --only {cat_id}`

## 5. Templates in this category

{template_list}

## 6. Interaction & States

{_states_table()}

## 7. Accessibility

{_a11y_block()}

## 8. Deliverables Checklist

- [ ] Gallery **accordion** or tab per top-level category
- [ ] Thumbnail preview per template (render SVG at 320×180)
- [ ] Canvas placeholder states (empty → hover → filled)
- [ ] Dark mode token overrides for grid and title bar

---

_Reference glossary: [{GLOSSARY}]({GLOSSARY})_
"""


def _template_brief(template: Template) -> str:
    cat_name = CATEGORY_NAMES.get(template.category, template.category)
    glossary_terms = CATEGORY_GLOSSARY.get(template.category, ("Affordance", "Grid"))
    glossary = ", ".join(f"**{g}**" for g in glossary_terms[:3])
    svg_path = f"../svg/{template.output_path}"

    return f"""# {template.title} — Template Design Brief

**Project:** UML-SKILLS Diagram Template Library  
**Category:** {cat_name} (`{template.category}`)  
**Template ID:** `{template.id}`  
**Layout:** `{template.layout}`  
**SVG:** `{svg_path}`  
**Version:** 1.0  
**Template:** [{TEMPLATE_REF}]({TEMPLATE_REF})  
**Glossary:** [{GLOSSARY}]({GLOSSARY})

---

## 1. Overview & Objectives

- **Goal:** Provide a ready-made blank canvas for **{template.title}** so users begin with correct structure, guides, and placeholder regions.
- **Description:** {template.description}
- **Canvas size:** 1920×1080 (16:9 logical artboard).
- **Aesthetic:** PrimeReact Lara chrome on a professional diagram surface. See [{PRIMEREACT}]({PRIMEREACT}).

## 2. Usage Context

- **When to use:** Starting a new **{cat_name}** diagram without building layout from scratch.
- **User flow:** Gallery card → **wizard** confirms name → canvas opens → user replaces placeholders with stencils from the shape library.
- **Glossary terms:** {glossary}

## 3. Layout & Structure (ASCII)

{_template_ascii(template)}

## 4. Template Chrome Elements

| Element | Present | Notes |
|---------|---------|-------|
| Title bar | Yes | Primary `#3B82F6`, template name centred |
| Project subtitle | Yes | `<Project Name> · Template` placeholder |
| Alignment grid | Yes | 50px spacing, surface-200 lines |
| Page border | Yes | 40px margin, 8px **border-radius** |
| Placeholder regions | Yes | Dashed `#94a3b8` — diagram-specific layout |
| Connection guides | Yes | Dotted lines where relationships expected |
| Legend area | Yes | Bottom-right dashed box |
| Footer | Yes | Confidential notice + project metadata |

## 5. Design Tokens

{_tokens_block()}

## 6. UI States (canvas)

{_states_table()}

## 7. Inspector Properties (Prime Panel)

| Property | Control | Default |
|----------|---------|---------|
| Project name | **InputText** | `<Project Name>` |
| Template title | read-only **InputText** | `{template.title}` |
| Page size | **Dropdown** | 1920×1080 |
| Show grid | **ToggleButton** | on |
| Snap to grid | **ToggleButton** | on |
| Confidential footer | **ToggleButton** | on |

## 8. Stencil Integration

- Placeholders map to stencil categories from `{template.category}` and related shape packs.
- Drag stencil from palette onto dashed region → placeholder converts to solid shape group.
- Guides suggest connector attachment points for relationship shapes.

## 9. Accessibility

- Canvas `aria-label="{template.title} template for project diagram"`.
- Each placeholder region named (e.g. "Class A placeholder").
- **Keyboard accessible** navigation between placeholders (Tab cycle).

## 10. Deliverables Checklist

- [ ] SVG at `{svg_path}`
- [ ] Gallery thumbnail (default + **hover** + **focus**)
- [ ] Canvas mockup with 1–2 placeholders filled with stencils
- [ ] Listed in [{LIBRARY}]({LIBRARY})

---

_Reference glossary: [{GLOSSARY}]({GLOSSARY})_
"""


SYSTEM_BRIEFS = [
    (
        "template-system",
        "Template System",
        "End-to-end diagram studio combining 86 blank templates with the stencil shape library.",
        "Architects, PMs, BAs, and engineers who start diagrams from standards-based layouts.",
        "Open app → browse template gallery OR open stencil editor → pick template → name project → compose → export.",
    ),
    (
        "template-gallery-ui",
        "Template Gallery UI",
        "Browsable catalog of 86 diagram templates organized by category.",
        "Users who need the right starting layout (UML, architecture, Gantt, RACI, etc.).",
        "Filter category → preview thumbnail → Use template → wizard collects project name.",
    ),
    (
        "template-canvas-ui",
        "Template Canvas UI",
        "Active 1920×1080 artboard with grid, placeholders, and stencil drop targets.",
        "Authors filling in a template with real diagram content.",
        "Pan/zoom canvas → select placeholder → drag stencil → connect → edit labels → save.",
    ),
    (
        "new-diagram-wizard-ui",
        "New Diagram Wizard UI",
        "Guided flow to pick a template and initialise project metadata.",
        "First-time and returning users creating a new diagram file.",
        "File → New → choose category → pick template → enter project name → Create.",
    ),
]


def write_index(by_category: Dict[str, List[Template]]) -> None:
    lines = [
        "# Diagram Template Library — Design Briefs Index",
        "",
        "**Design direction:** [PrimeReact](https://primereact.org/) (Lara) enterprise UI",
        "",
        "References:",
        f"- [{TEMPLATE_REF}]({TEMPLATE_REF})",
        f"- [{GLOSSARY}]({GLOSSARY})",
        f"- [{PRIMEREACT}]({PRIMEREACT})",
        f"- [{STYLE}]({STYLE})",
        f"- [{LIBRARY}]({LIBRARY})",
        "",
        "Regenerate: `python brief/generate_briefs.py`",
        "",
        "## System briefs",
        "",
    ]
    for key, title, *_ in SYSTEM_BRIEFS:
        lines.append(f"- [{title}](./system/{key}.md)")
    lines += ["", "## Category briefs", ""]
    for cat_id in sorted(by_category):
        name = CATEGORY_NAMES.get(cat_id, cat_id)
        lines.append(f"- [{name}](./categories/{cat_id}.md) — {len(by_category[cat_id])} templates")
    total = sum(len(v) for v in by_category.values())
    lines += [
        "",
        "## Template briefs",
        "",
        f"**{total}** template briefs under `brief/templates/<category>/<template-id>.md`",
        "",
        f"See [{LIBRARY}]({LIBRARY}) for the full catalog.",
    ]
    INDEX.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    OUT_SYSTEM.mkdir(parents=True, exist_ok=True)
    OUT_CATEGORIES.mkdir(parents=True, exist_ok=True)
    OUT_TEMPLATES.mkdir(parents=True, exist_ok=True)

    templates = all_templates()
    by_category: Dict[str, List[Template]] = defaultdict(list)
    for t in templates:
        by_category[t.category].append(t)

    for key, title, goal, personas, flow in SYSTEM_BRIEFS:
        (OUT_SYSTEM / f"{key}.md").write_text(
            _system_brief(key, title, goal, personas, flow), encoding="utf-8"
        )

    for cat_id, cat_templates in sorted(by_category.items()):
        (OUT_CATEGORIES / f"{cat_id}.md").write_text(
            _category_brief(cat_id, cat_templates), encoding="utf-8"
        )
        cat_dir = OUT_TEMPLATES / cat_id
        cat_dir.mkdir(parents=True, exist_ok=True)
        for template in cat_templates:
            (cat_dir / f"{template.id}.md").write_text(
                _template_brief(template), encoding="utf-8"
            )

    write_index(by_category)
    print(f"Wrote {len(SYSTEM_BRIEFS)} system briefs")
    print(f"Wrote {len(by_category)} category briefs")
    print(f"Wrote {len(templates)} template briefs")
    print(f"Index: {INDEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
