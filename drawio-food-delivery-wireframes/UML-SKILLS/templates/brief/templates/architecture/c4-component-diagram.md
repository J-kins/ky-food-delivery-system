# C4 Component Diagram — Template Design Brief

**Project:** UML-SKILLS Diagram Template Library  
**Category:** Architecture Diagrams (`architecture`)  
**Template ID:** `c4-component-diagram`  
**Layout:** `c4_component`  
**SVG:** `../svg/architecture/26-c4-component-diagram-template.svg`  
**Version:** 1.0  
**Template:** [../../stencils/UI-UX_Design_Brief_Template.md](../../stencils/UI-UX_Design_Brief_Template.md)  
**Glossary:** [../../stencils/ui-design-glossary.md](../../stencils/ui-design-glossary.md)

---

## 1. Overview & Objectives

- **Goal:** Provide a ready-made blank canvas for **C4 Component Diagram** so users begin with correct structure, guides, and placeholder regions.
- **Description:** Components inside a container
- **Canvas size:** 1920×1080 (16:9 logical artboard).
- **Aesthetic:** PrimeReact Lara chrome on a professional diagram surface. See [../../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md](../../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md).

## 2. Usage Context

- **When to use:** Starting a new **Architecture Diagrams** diagram without building layout from scratch.
- **User flow:** Gallery card → **wizard** confirms name → canvas opens → user replaces placeholders with stencils from the shape library.
- **Glossary terms:** **Grid**, **System Context**, **Layer**

## 3. Layout & Structure (ASCII)

```
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
```

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

## 6. UI States (canvas)

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

## 7. Inspector Properties (Prime Panel)

| Property | Control | Default |
|----------|---------|---------|
| Project name | **InputText** | `<Project Name>` |
| Template title | read-only **InputText** | `C4 Component Diagram` |
| Page size | **Dropdown** | 1920×1080 |
| Show grid | **ToggleButton** | on |
| Snap to grid | **ToggleButton** | on |
| Confidential footer | **ToggleButton** | on |

## 8. Stencil Integration

- Placeholders map to stencil categories from `architecture` and related shape packs.
- Drag stencil from palette onto dashed region → placeholder converts to solid shape group.
- Guides suggest connector attachment points for relationship shapes.

## 9. Accessibility

- Canvas `aria-label="C4 Component Diagram template for project diagram"`.
- Each placeholder region named (e.g. "Class A placeholder").
- **Keyboard accessible** navigation between placeholders (Tab cycle).

## 10. Deliverables Checklist

- [ ] SVG at `../svg/architecture/26-c4-component-diagram-template.svg`
- [ ] Gallery thumbnail (default + **hover** + **focus**)
- [ ] Canvas mockup with 1–2 placeholders filled with stencils
- [ ] Listed in [../svg/TEMPLATE_LIBRARY.json](../svg/TEMPLATE_LIBRARY.json)

---

_Reference glossary: [../../stencils/ui-design-glossary.md](../../stencils/ui-design-glossary.md)_
