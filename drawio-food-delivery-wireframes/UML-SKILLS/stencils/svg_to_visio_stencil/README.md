# SVG to Visio Stencil Converter

Production Python package that converts the UML-SKILLS SVG shape library into a Microsoft Visio stencil (`.vssx`) using **Aspose.Diagram** (JPype + Java).

## Requirements

- Python 3.10+
- Java JRE 11+
- Dependencies: see `requirements.txt`

```bash
pip install -r svg_to_visio_stencil/requirements.txt
```

## Usage

From the `stencils/` directory:

```bash
# Full conversion (168 SVG shapes → single .vssx)
python -m svg_to_visio_stencil.main -c svg_to_visio_stencil/config.json

# Validate configuration only
python -m svg_to_visio_stencil.main -c svg_to_visio_stencil/config.json --validate-only

# Verbose logging
python -m svg_to_visio_stencil.main -c svg_to_visio_stencil/config.json -v

# Single category
python -m svg_to_visio_stencil.main --category uml-class

# One stencil per category
python -m svg_to_visio_stencil.main --per-category

# Also generate .vstx template
python -m svg_to_visio_stencil.main --create-template
```

## Output

| File | Description |
|------|-------------|
| `output/uml-architecture-stencil.vssx` | Combined stencil with all masters |
| `output/uml-architecture-template.vstx` | Optional blank template |
| `svg_to_visio_stencil/logs/` | Conversion logs |

## Architecture

```
svg_to_visio_stencil/
├── main.py              # CLI entry point
├── config.py            # Config + SHAPE_LIBRARY/manifest merge
├── svg_parser.py        # SVG → structured elements (incl. markers)
├── shape_converter.py   # Elements → Visio masters via drawRectangle/Line/etc.
├── visio_builder.py     # Aspose JVM bootstrap + low-level helpers
├── metadata_manager.py  # Connection points + custom properties
├── stencil_builder.py   # Batch orchestration + progress bar
├── template_builder.py  # Optional .vstx output
└── utils.py             # Coordinates, colors, logging
```

## Notes

- Uses `asposediagram.api` via JPype (same pattern as other UML-SKILLS generators).
- SVGs are parsed and drawn with native Visio geometry (not rasterized).
- Master `NameU` is the shape id (unique); `Name` is the display label.
- Annotation-only shapes (no SVG file) are skipped automatically.
- `sprite.svg` is excluded by default.
