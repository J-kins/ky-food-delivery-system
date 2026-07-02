# Multiplicity — Shape Design Brief

**Project:** UML-SKILLS Stencil Toolkit  
**Category:** UML Class Diagram (`uml-class`)  
**Shape ID:** `multiplicity`  
**Asset type:** `annotation` | **Delivery:** `annotation`  
**SVG:** `— (annotation)`  
**Version:** 1.0  
**Template:** [../UI-UX_Design_Brief_Template.md](../UI-UX_Design_Brief_Template.md)  
**Glossary:** [../ui-design-glossary.md](../ui-design-glossary.md)

---

## 1. Overview & Objectives

- **Goal:** Cardinality indicators
- **Description:** Text labels 1, *, 0..1
- **Visual notation:** `1, *`
- **Aesthetic:** PrimeReact-aligned — clean strokes, **surface** fills, primary selection accent. See [PRIMEREACT_DESIGN_DIRECTION.md](../PRIMEREACT_DESIGN_DIRECTION.md).

## 2. Usage Context

- **Diagram types:** UML Class Diagram diagrams.
- **Palette tile:** 48×48 **card** tile in `uml-class` **accordion** section.
- **Glossary terms:** **Card**, **Typography**, **Affordance**
- **Notes:** Text-only UML convention — render as inline label on canvas. 

## 3. Layout & Structure (ASCII)

```
Text annotation (no SVG asset — Prime InputText / inline label):
  {constraint}   or   [guard]   or   1..*

Rendered as muted caption (text-muted-color) near parent shape.
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
| Label | **InputText** | `Multiplicity` |
| Stroke | **ColorPicker** | `#334155` |
| Fill | **ColorPicker** | `#ffffff` |
| Stroke width | **InputNumber** | 1.5 |
| Visible | **ToggleButton** | on |

## 7. Accessibility

- Tile `aria-label="Multiplicity"`; canvas shape `role="img"` with descriptive label.
- **Keyboard accessible** move/resize when selected.
- **Contrast ratio** check for text inside shape bounds.

## 8. Deliverables Checklist

- [ ] SVG asset at `— (annotation)`
- [ ] Palette thumbnail (default + **hover** + **focus**)
- [ ] Canvas instance (default + selected)
- [ ] Listed in `sprite.svg` symbol `#multiplicity`

---

_Reference glossary: [../ui-design-glossary.md](../ui-design-glossary.md)_
