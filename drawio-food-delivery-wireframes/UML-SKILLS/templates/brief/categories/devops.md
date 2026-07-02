# DevOps & CI/CD Diagrams — Category Design Brief

**Project:** UML-SKILLS Diagram Template Library  
**Category ID:** `devops`  
**Template count:** 6  
**Version:** 1.0  
**Template:** [../../stencils/UI-UX_Design_Brief_Template.md](../../stencils/UI-UX_Design_Brief_Template.md)  
**Glossary:** [../../stencils/ui-design-glossary.md](../../stencils/ui-design-glossary.md)  
**Design direction:** [../../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md](../../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md)

---

## 1. Overview & Objectives

- **Goal:** Help users start **devops & ci/cd diagrams** quickly with pre-structured blank canvases that match industry diagram conventions.
- **Scope:** 6 template SVGs — see [../svg/TEMPLATE_LIBRARY.json](../svg/TEMPLATE_LIBRARY.json).
- **Aesthetic:** PrimeReact-inspired enterprise UI — layered **surface** backgrounds, 6px **border-radius** on **cards**/**panels**, primary blue accent (`#3B82F6`), subtle elevation, compact gallery density, and 150–200ms **microinteractions**. See [PRIMEREACT_DESIGN_DIRECTION.md](../../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md).
- **Companion assets:** Stencil shapes from [../../stencils/svg/SHAPE_LIBRARY.md](../../stencils/svg/SHAPE_LIBRARY.md) fill placeholders on the canvas.

## 2. Target Audience & Context

- **Personas:** Enterprise architects, BAs, PMs, developers, data engineers (varies by sub-type).
- **Usage:** Gallery → select template → name project → replace dashed placeholders with stencil shapes.
- **Glossary terms:** **Pipeline**, **Stage**, **Loop**, **Observability**

## 3. Gallery Presentation (ASCII)

```
Gallery category strip:
> DevOps & CI/CD Diagrams

Card grid of template thumbnails (16:9 preview, primary CTA "Use template").
```

## 4. Template Canvas Chrome (shared)

All templates in this category share:

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

- SVG folder: `svg/devops/`
- Regenerate: `python svg/scripts/generate_templates.py --only devops`

## 5. Templates in this category

`cicd-pipeline`, `devops-architecture`, `gitops-architecture`, `observability-architecture`, `infrastructure-as-code`, `service-mesh-architecture`

## 6. Interaction & States

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

## 7. Accessibility

- Gallery cards: `aria-label` = template title; keyboard selectable grid.
- Placeholders: `role="region"` with `aria-label` describing intended content.
- Title bar: heading level 1 for template name; project name editable field labelled.
- **Contrast ratio** ≥ 4.5:1 for footer and placeholder labels (WCAG AA).
- Honour `prefers-reduced-motion` for gallery hover and drop-target animations.

## 8. Deliverables Checklist

- [ ] Gallery **accordion** or tab per top-level category
- [ ] Thumbnail preview per template (render SVG at 320×180)
- [ ] Canvas placeholder states (empty → hover → filled)
- [ ] Dark mode token overrides for grid and title bar

---

_Reference glossary: [../../stencils/ui-design-glossary.md](../../stencils/ui-design-glossary.md)_
