# Zigzag Line — Shape Design Brief

**Project:** UML-SKILLS Stencil Toolkit  
**Category:** Connector & Line Types (`connector-line`)  
**Shape ID:** `zigzag-line`  
**Asset type:** `connector` | **Delivery:** `generate`  
**SVG:** `../svg/shapes/connector-line/zigzag-line.svg`  
**Version:** 1.0  
**Template:** [../UI-UX_Design_Brief_Template.md](../UI-UX_Design_Brief_Template.md)  
**Glossary:** [../ui-design-glossary.md](../ui-design-glossary.md)

---

## 1. Overview & Objectives

- **Goal:** Interrupting flow
- **Description:** Zigzag connector
- **Visual notation:** `╲╱╲╱╲`
- **Aesthetic:** PrimeReact-aligned — clean strokes, **surface** fills, primary selection accent. See [PRIMEREACT_DESIGN_DIRECTION.md](../PRIMEREACT_DESIGN_DIRECTION.md).

## 2. Usage Context

- **Diagram types:** Connector & Line Types diagrams.
- **Palette tile:** 48×48 **card** tile in `connector-line` **accordion** section.
- **Glossary terms:** **Connector**, **Arrow**, **Dependency**
- **Notes:** Auto-generated SVG — restyle with Prime tokens in `generate_shapes.py`. 

## 3. Layout & Structure (ASCII)

```
Connector on canvas (default stroke surface-700):
  Node A  ───────────────▶  Node B

Selected connector (primary-color stroke):
  Node A  ═══════════════▶  Node B   [handles at endpoints]

Toolbar (Prime Toolbar) — active line tool highlighted primary.
```

## 4. PrimeReact Token Mapping

| State | Stroke | Fill | Notes |
|-------|--------|------|-------|
| Default | `#e2e8f0` / `#334155` | `#ffffff` | surface-200 / surface-700 |
| Hover | `#94a3b8` | `#f8fafc` | surface-400 hint |
| Selected | `#3B82F6` | `#EFF6FF` | primary / primary-50 |
| Disabled | `#cbd5e1` | `#f1f5f9` | 50% opacity |
| Focus ring | — | — | `0 0 0 2px #BFDBFE` on wrapper |

## 5. UI States (on canvas)

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

## 6. Inspector Properties (Prime Panel fields)

| Property | Control | Default |
|----------|---------|---------|
| Label | **InputText** | `Zigzag Line` |
| Stroke | **ColorPicker** | `#334155` |
| Fill | **ColorPicker** | `#ffffff` |
| Stroke width | **InputNumber** | 1.5 |
| Visible | **ToggleButton** | on |

## 7. Accessibility

- Tile `aria-label="Zigzag Line"`; canvas shape `role="img"` with descriptive label.
- **Keyboard accessible** move/resize when selected.
- **Contrast ratio** check for text inside shape bounds.

## 8. Deliverables Checklist

- [ ] SVG asset at `../svg/shapes/connector-line/zigzag-line.svg`
- [ ] Palette thumbnail (default + **hover** + **focus**)
- [ ] Canvas instance (default + selected)
- [ ] Listed in `sprite.svg` symbol `#zigzag-line`

---

_Reference glossary: [../ui-design-glossary.md](../ui-design-glossary.md)_
