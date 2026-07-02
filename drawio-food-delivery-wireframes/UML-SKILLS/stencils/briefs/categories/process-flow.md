# Process & Flow — Category Design Brief

**Project:** UML-SKILLS Stencil Toolkit  
**Category ID:** `process-flow`  
**Shape count:** 11  
**Version:** 1.0  
**Template:** [../UI-UX_Design_Brief_Template.md](../UI-UX_Design_Brief_Template.md)  
**Glossary:** [../ui-design-glossary.md](../ui-design-glossary.md)  
**Design direction:** [./PRIMEREACT_DESIGN_DIRECTION.md](./PRIMEREACT_DESIGN_DIRECTION.md)

---

## 1. Overview & Objectives

- **Goal:** Present and render **Process & Flow** shapes with consistent PrimeReact enterprise aesthetics in the palette and on the diagram canvas.
- **Scope:** 11 stencil shapes — see [SHAPE_LIBRARY.md](../svg/SHAPE_LIBRARY.md).
- **Aesthetic:** PrimeReact-inspired enterprise UI — layered **surface** backgrounds, 6px **border-radius** on **cards**/**panels**, primary blue selection accent (`#3B82F6`), subtle **shadow-sm** elevation, compact **sidebar**/**tree** density, and 150–200ms **microinteractions**. See [PRIMEREACT_DESIGN_DIRECTION.md](./PRIMEREACT_DESIGN_DIRECTION.md).

## 2. Target Audience & Context

- **Personas:** Software architects, business analysts, developers, technical writers.
- **Usage:** Drag from palette **sidebar** onto canvas; edit via inspector **panel**; export via **dialog**.
- **Glossary terms:** **Flowchart**, **Decision**, **Process**, **Document**

## 3. Palette Presentation (ASCII)

```
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
```

## 4. Canvas Rendering Rules

| State | Stroke | Fill | Notes |
|-------|--------|------|-------|
| Default | `#e2e8f0` / `#334155` | `#ffffff` | surface-200 / surface-700 |
| Hover | `#94a3b8` | `#f8fafc` | surface-400 hint |
| Selected | `#3B82F6` | `#EFF6FF` | primary / primary-50 |
| Disabled | `#cbd5e1` | `#f1f5f9` | 50% opacity |
| Focus ring | — | — | `0 0 0 2px #BFDBFE` on wrapper |

- SVG source: `svg/shapes/process-flow/<shape-id>.svg`
- Regenerate assets: `python svg/scripts/generate_shapes.py --only process-flow`
- Sprite symbol: `svg/shapes/sprite.svg#process`

## 5. Shapes in this category

`process`, `flow-start`, `flow-end`, `flow-decision`, `document`, `data-parallelogram`, `predefined-process`, `manual-input`, … (+3 more)

## 6. Interaction & States

| State | When | PrimeReact-aligned requirement |
|-------|------|--------------------------------|
| **Default** | Placed on canvas | surface stroke/fill per tokens |
| **Hover** | Pointer over shape | Slight stroke darken; tile `surface-100` in palette |
| **Focus** | Keyboard selected | **Focus** ring like Prime **Button** |
| **Selected** | Marquee or click | Primary border — like **DataTable** row select |
| **Active** | Dragging/resizing | `shadow-md`, cursor affordance |
| **Disabled** | Locked layer | Muted + **tooltip** explaining lock |
| **Error** | Invalid connection | Prime **Message** severity error inline |
| **Loading** | Importing stencil | **Skeleton** tile placeholders in palette |

## 7. Accessibility

- Shape tiles: `aria-label` = shape name; draggable with keyboard alternative.
- Canvas: arrow-key nudge (1px, 10px with Shift); **tab order** through selection handles.
- Inspector fields: Prime **InputText** / **Dropdown** with visible **focus** rings.
- **Contrast ratio** ≥ 4.5:1 for labels on shape fills (WCAG AA).
- Honour `prefers-reduced-motion` for snap/guide animations.

## 8. Deliverables Checklist

- [ ] Palette **accordion** section for `process-flow`
- [ ] Thumbnail tiles for each shape (48×48, **border-radius** 6px)
- [ ] Canvas default + selected + **focus** states per shape
- [ ] Dark mode token overrides

---

_Reference glossary: [../ui-design-glossary.md](../ui-design-glossary.md)_
