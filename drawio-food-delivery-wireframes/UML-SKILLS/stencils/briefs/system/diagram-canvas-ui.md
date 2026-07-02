# Diagram Canvas UI — UI/UX Design Brief

**Project:** UML-SKILLS Stencil Toolkit  
**Area:** System / application chrome  
**Version:** 1.0  
**Template:** [../UI-UX_Design_Brief_Template.md](../UI-UX_Design_Brief_Template.md)  
**Glossary:** [../ui-design-glossary.md](../ui-design-glossary.md)  
**Design direction:** [./PRIMEREACT_DESIGN_DIRECTION.md](./PRIMEREACT_DESIGN_DIRECTION.md)

---

## 1. Overview & Objectives

- **Goal:** Central infinite canvas with tools, grid, and selection.
- **UX objectives:** Enterprise **task success rate**, low cognitive load, keyboard-efficient diagramming, excellent **legibility** on dense diagrams.
- **Aesthetic:** PrimeReact-inspired enterprise UI — layered **surface** backgrounds, 6px **border-radius** on **cards**/**panels**, primary blue selection accent (`#3B82F6`), subtle **shadow-sm** elevation, compact **sidebar**/**tree** density, and 150–200ms **microinteractions**. See [PRIMEREACT_DESIGN_DIRECTION.md](./PRIMEREACT_DESIGN_DIRECTION.md).

## 2. Target Audience & User Journey

- **Personas:** Diagram authors placing and connecting shapes.
- **Primary flow:** Select tool → place/move shapes → connector tool → link nodes → multi-select → align.
- **Glossary terms:** **Sidebar**, **Toolbar**, **Panel**, **Dialog**, **Toast**, **Grid**, **Affordance**

## 3. Layout & Structure (ASCII wireframe)

```
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
```

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

| State | Stroke | Fill | Notes |
|-------|--------|------|-------|
| Default | `#e2e8f0` / `#334155` | `#ffffff` | surface-200 / surface-700 |
| Hover | `#94a3b8` | `#f8fafc` | surface-400 hint |
| Selected | `#3B82F6` | `#EFF6FF` | primary / primary-50 |
| Disabled | `#cbd5e1` | `#f1f5f9` | 50% opacity |
| Focus ring | — | — | `0 0 0 2px #BFDBFE` on wrapper |

Full token map: [PRIMEREACT_DESIGN_DIRECTION.md](./PRIMEREACT_DESIGN_DIRECTION.md) and [STYLE_GUIDE.md](../svg/STYLE_GUIDE.md).

## 7. Interaction & Microinteractions

- Palette tile **hover** 150ms `ease-out` background transition.
- Drag from palette: ghost preview at 60% **opacity**; snap **microinteraction** 200ms.
- **Toast** on export success (top-right, 3s).
- **Dialog** entry 250ms; honour `prefers-reduced-motion`.

## 8. UI States

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

## 9. Accessibility (WCAG 2.1 AA)

- Shape tiles: `aria-label` = shape name; draggable with keyboard alternative.
- Canvas: arrow-key nudge (1px, 10px with Shift); **tab order** through selection handles.
- Inspector fields: Prime **InputText** / **Dropdown** with visible **focus** rings.
- **Contrast ratio** ≥ 4.5:1 for labels on shape fills (WCAG AA).
- Honour `prefers-reduced-motion` for snap/guide animations.

## 10. Deliverables Checklist

- [ ] Light + dark PrimeReact theme variants
- [ ] Desktop + tablet **breakpoint** (collapsible **sidebar** to **drawer**)
- [ ] State matrix for palette, canvas selection, export **dialog**
- [ ] Figma components mirroring PrimeReact patterns
- [ ] Developer handoff: React + PrimeReact component map

---

_Reference glossary: [../ui-design-glossary.md](../ui-design-glossary.md)_
