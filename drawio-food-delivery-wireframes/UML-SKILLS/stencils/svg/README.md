# UML & Architecture SVG Stencils

Consistent, reusable SVG shapes for UML and software architecture diagrams.

## Quick start

```bash
cd stencils/svg

# 1. Build inventory (SHAPE_LIBRARY.json + SHAPE_LIBRARY.md)
python3 scripts/build_inventory.py

# 2. Generate SVGs + consolidated sprite
python3 scripts/generate_shapes.py

# 3. Download cloud vendor icons only (AWS official icons)
python3 scripts/generate_shapes.py --download-only
```

## Output layout

```
stencils/svg/
├── SHAPE_LIBRARY.json      # Machine-readable catalog
├── SHAPE_LIBRARY.md        # Human-readable catalog
├── STYLE_GUIDE.md          # Consistency rules
├── shape_catalog.py        # Single source of truth
├── scripts/
│   ├── build_inventory.py
│   └── generate_shapes.py
└── shapes/
    ├── sprite.svg          # Consolidated <symbol> sprite
    ├── manifest.json       # Per-shape generation status
    └── <category>/
        └── <shape-id>.svg
```

## Delivery types

| Type | Meaning |
|------|---------|
| `generate` | Auto-generated with consistent style |
| `download` | Fetched from official icon packs (AWS, etc.) |
| `manual` | Hand-craft later (complex flowchart shapes) |
| `annotation` | Text convention only — no SVG file |

## Using the sprite

```html
<svg viewBox="0 0 80 80" width="80" height="80">
  <use href="shapes/sprite.svg#rectangle"/>
</svg>
```

## Consistency

All generated shapes follow [STYLE_GUIDE.md](./STYLE_GUIDE.md):

- Stroke `#1a1a1a`, width `1.5`
- Fill `#ffffff` (nodes)
- Standard viewBoxes per shape family

## Manual shapes to create

Shapes marked `manual` in the catalog (e.g. document, trapezoid, accept-signal, Azure/GCP icons) should be added to `shapes/<category>/` following the style guide, then re-run `generate_shapes.py` to refresh the sprite.
