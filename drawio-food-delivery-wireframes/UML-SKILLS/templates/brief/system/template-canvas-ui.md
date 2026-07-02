# Template Canvas UI — UI/UX Design Brief

**Project:** UML-SKILLS Diagram Template Library  
**Area:** System / application chrome  
**Version:** 1.0  
**Template:** [../../stencils/UI-UX_Design_Brief_Template.md](../../stencils/UI-UX_Design_Brief_Template.md)  
**Glossary:** [../../stencils/ui-design-glossary.md](../../stencils/ui-design-glossary.md)  
**Design direction:** [../../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md](../../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md)

---

## 1. Overview & Objectives

- **Goal:** Active 1920×1080 artboard with grid, placeholders, and stencil drop targets.
- **UX objectives:** Fast template selection, clear placeholder affordance, seamless stencil insertion, excellent **legibility** on large-format canvases.
- **Aesthetic:** PrimeReact-inspired enterprise UI — layered **surface** backgrounds, 6px **border-radius** on **cards**/**panels**, primary blue accent (`#3B82F6`), subtle elevation, compact gallery density, and 150–200ms **microinteractions**. See [PRIMEREACT_DESIGN_DIRECTION.md](../../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md).

## 2. Target Audience & User Journey

- **Personas:** Authors filling in a template with real diagram content.
- **Primary flow:** Pan/zoom canvas → select placeholder → drag stencil → connect → edit labels → save.
- **Glossary terms:** **Wizard**, **Card**, **Panel**, **Dialog**, **Grid**, **Affordance**, **Progressive Disclosure**

## 3. Layout & Structure (ASCII wireframe)

```
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
```

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

| Element | Token | Value |
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
| Selected placeholder | primary stroke | `#3B82F6` 2px |

Full reference: [../svg/STYLE_GUIDE.md](../svg/STYLE_GUIDE.md) and [../../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md](../../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md).

## 7. Interaction & Microinteractions

- Gallery card **hover** 150ms `ease-out` elevation (`shadow-sm`).
- **Wizard** step transition 250ms; honour `prefers-reduced-motion`.
- Drop stencil on placeholder: 200ms primary-50 flash confirmation.
- **Toast** on diagram created (top-right, 3s).

## 8. UI States

| State | When | PrimeReact-aligned requirement |
|-------|------|--------------------------------|
| **Default** | Template opened | Dashed placeholders visible on grid |
| **Hover** | Pointer over placeholder | Stroke darken; subtle surface-100 fill |
| **Focus** | Keyboard on placeholder | **Focus** ring `#BFDBFE` on wrapper |
| **Selected** | Placeholder chosen for edit | Primary border — ready to replace |
| **Active** | Dragging stencil onto placeholder | Drop target highlight primary-50 |
| **Filled** | Stencil placed | Solid stroke; placeholder dash removed |
| **Empty** | Project name unset | Subtitle shows `<Project Name>` literal |
| **Loading** | Template SVG loading | **Skeleton** canvas preview in gallery |

## 9. Accessibility (WCAG 2.1 AA)

- Gallery cards: `aria-label` = template title; keyboard selectable grid.
- Placeholders: `role="region"` with `aria-label` describing intended content.
- Title bar: heading level 1 for template name; project name editable field labelled.
- **Contrast ratio** ≥ 4.5:1 for footer and placeholder labels (WCAG AA).
- Honour `prefers-reduced-motion` for gallery hover and drop-target animations.

## 10. Deliverables Checklist

- [ ] Light + dark PrimeReact theme variants
- [ ] Gallery responsive **grid** (3–4 columns desktop, 1–2 mobile)
- [ ] State matrix: gallery card, canvas placeholder, filled slot
- [ ] Integration with stencil palette documented
- [ ] Figma artboard components at 1920×1080

---

_Reference glossary: [../../stencils/ui-design-glossary.md](../../stencils/ui-design-glossary.md)_
