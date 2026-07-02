# UML & Architecture SVG Stencil — Style Guide

Consistent rendering rules for all shapes in `stencils/svg/shapes/`.

**UI chrome aesthetic:** [PrimeReact](https://primereact.org/) (Lara theme) — see [briefs/PRIMEREACT_DESIGN_DIRECTION.md](../briefs/PRIMEREACT_DESIGN_DIRECTION.md).

---

## PrimeReact design tokens (shape rendering)

| Token | Light value | SVG / CSS usage |
|-------|-------------|-----------------|
| Primary | `#3B82F6` | Selected stroke, active connector |
| Primary tint | `#EFF6FF` | Selected fill |
| Surface 0 | `#ffffff` | Default node fill |
| Surface 50 | `#f8fafc` | Canvas background |
| Surface 200 | `#e2e8f0` | Default stroke, palette tile border |
| Surface 700 | `#334155` | Labels, default node stroke |
| Text muted | `#64748b` | Stereotypes, multiplicity |
| Border radius | `6px` | Rounded rectangles (actions, states) |
| Focus ring | `0 0 0 2px #BFDBFE` | Selected control wrapper |

Dark mode: use Lara Dark surfaces (`#0f172a` canvas, `#1e293b` fill); re-test **contrast ratio**.

---

## Canvas

| Property | Value | Notes |
|----------|-------|-------|
| Default viewBox | `0 0 80 80` | Node shapes |
| Connector viewBox | `0 0 120 24` | Horizontal connectors |
| Wide viewBox | `0 0 120 80` | Class boxes, swimlanes |
| Padding | 8px inset from viewBox edge | Keeps stroke fully visible |

## Stroke & Fill (default / unselected)

| Property | Value |
|----------|-------|
| Stroke colour | `#334155` (surface-700) |
| Stroke width | `1.5` (nodes), `1.25` (connectors) |
| Fill (nodes) | `#ffffff` (surface-0) |
| Fill (markers) | `#334155` for solid dots |
| Fill (none) | `none` for lines, interfaces, actors outline |
| Line cap | `round` |
| Line join | `round` |

## Selected state (on canvas)

| Property | Value |
|----------|-------|
| Stroke | `#3B82F6` (primary), width `2` |
| Fill | `#EFF6FF` (primary-50) |

## Typography (labelled shapes)

| Property | Value |
|----------|-------|
| Font family | `Inter, system-ui, -apple-system, Segoe UI, sans-serif` |
| Font size | `12px` (labels), `10px` (stereotypes) |
| Text colour | `#334155` |
| Stereotype style | `<<stereotype>>` guillemets, `#64748b` |

## Corners & Radii

| Shape | Radius |
|-------|--------|
| Rounded rectangle / action / state | `6` (PrimeReact md) |
| Palette thumbnail tile | `6` |
| Use case oval | `rx=50%` of height |
| Class box compartments | square corners (`0`) |

## Connector dash patterns

| Type | `stroke-dasharray` |
|------|-------------------|
| Solid | none |
| Dashed | `6 4` |
| Dotted | `2 3` |

## Arrowheads

Use SVG `<marker>` definitions shared via `defs/markers.svg`:

- `arrow-filled` — synchronous message, solid flow
- `arrow-open` — asynchronous message
- `arrow-hollow-triangle` — inheritance / generalization
- `diamond-hollow` — aggregation
- `diamond-filled` — composition

## File naming

```
shapes/<category-id>/<shape-id>.svg
```

Example: `shapes/basic-geometric/rectangle.svg`

## Sprite consolidation

`shapes/sprite.svg` contains `<symbol id="{shape-id}">` for each generated shape.

```html
<svg viewBox="0 0 80 80">
  <use href="../shapes/sprite.svg#rectangle" width="80" height="80"/>
</svg>
```

## Delivery status

| Status | Meaning |
|--------|---------|
| `generated` | Created by `scripts/generate_shapes.py` |
| `manual` | Hand-crafted; not auto-generated |
| `download` | Fetched from external pack (cloud vendor icons) |
| `annotation` | Text convention only — no SVG file |

## Related docs

- [PRIMEREACT_DESIGN_DIRECTION.md](../briefs/PRIMEREACT_DESIGN_DIRECTION.md)
- [UI-UX_Design_Brief_Template.md](../UI-UX_Design_Brief_Template.md)
- [ui-design-glossary.md](../ui-design-glossary.md)
- [briefs/BRIEFS_INDEX.md](../briefs/BRIEFS_INDEX.md)
