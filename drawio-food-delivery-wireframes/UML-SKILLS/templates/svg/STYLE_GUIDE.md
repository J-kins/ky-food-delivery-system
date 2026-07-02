# Diagram Template SVGs — Style Guide

Blank **canvas templates** (1920×1080) for starting new diagrams — distinct from individual **stencil shapes** in `stencils/svg/shapes/`.

**Aesthetic:** [PrimeReact Lara](../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md) — same tokens as the stencil library.

## Tokens

| Element | Value |
|---------|-------|
| Canvas background | `#ffffff` (surface-0) |
| Grid overlay | `#f8fafc` tint + `#e2e8f0` lines |
| Page border | `#e2e8f0` (surface-200) |
| Title bar | `#3B82F6` (primary) + white text |
| Placeholder stroke | `#94a3b8` dashed `8 5` |
| Guide lines | `#cbd5e1` dotted `4 4` |
| Labels | `#334155` / `#64748b` muted |
| Layer bands | `#EFF6FF` (primary-50) fill |
| Font | Inter, system-ui, sans-serif |

## Regenerate

```bash
cd templates/svg
python3 scripts/generate_templates.py
```

## Layout

```
templates/svg/
├── uml/                  # 14 templates
├── architecture/         # 16
├── infrastructure/       # 8
├── project-management/   # 12
├── stakeholder/          # 6
├── process-flow/         # 6
├── data/                 # 6
├── gis/                  # 5
├── cloud/                # 7
└── devops/               # 6
```

Inventory: `TEMPLATE_LIBRARY.json`
