# Port — Shape Design Brief

**Project:** UML-SKILLS Stencil Toolkit  
**Category:** UML Component & Deployment (`uml-component-deployment`)  
**Shape ID:** `port`  
**Asset type:** `marker` | **Delivery:** `generate`  
**SVG:** `../svg/shapes/uml-component-deployment/port.svg`  
**Version:** 1.0  
**Template:** [../UI-UX_Design_Brief_Template.md](../UI-UX_Design_Brief_Template.md)  
**Glossary:** [../ui-design-glossary.md](../ui-design-glossary.md)

---

## 1. Overview & Objectives

- **Goal:** Interaction point
- **Description:** Small square on component
- **Visual notation:** `□`
- **Aesthetic:** PrimeReact-aligned — clean strokes, **surface** fills, primary selection accent. See [PRIMEREACT_DESIGN_DIRECTION.md](../PRIMEREACT_DESIGN_DIRECTION.md).

## 2. Usage Context

- **Diagram types:** UML Component & Deployment diagrams.
- **Palette tile:** 48×48 **card** tile in `uml-component-deployment` **accordion** section.
- **Glossary terms:** **Component**, **Interface**, **Node**
- **Notes:** Auto-generated SVG — restyle with Prime tokens in `generate_shapes.py`. 

## 3. Layout & Structure (ASCII)

```
Marker node (initial/final/decision dot):
  ●  solid primary or surface-900 fill
  ◉  ring marker — stroke surface-700, fill surface-0

Selected: primary ring + focus-ring shadow.
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
| Label | **InputText** | `Port` |
| Stroke | **ColorPicker** | `#334155` |
| Fill | **ColorPicker** | `#ffffff` |
| Stroke width | **InputNumber** | 1.5 |
| Visible | **ToggleButton** | on |

## 7. Accessibility

- Tile `aria-label="Port"`; canvas shape `role="img"` with descriptive label.
- **Keyboard accessible** move/resize when selected.
- **Contrast ratio** check for text inside shape bounds.

## 8. Deliverables Checklist

- [ ] SVG asset at `../svg/shapes/uml-component-deployment/port.svg`
- [ ] Palette thumbnail (default + **hover** + **focus**)
- [ ] Canvas instance (default + selected)
- [ ] Listed in `sprite.svg` symbol `#port`

---

_Reference glossary: [../ui-design-glossary.md](../ui-design-glossary.md)_
