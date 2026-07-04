# SVG Template to Visio Diagram Converter

Modular Python system for converting data-driven SVG templates to Visio diagrams (.vsdx, .vstx, .vssx).

## Architecture

```
scripts/
├── main.py                          # Orchestrator (entry point)
├── base/                            # Core conversion framework
│   ├── __init__.py
│   ├── json_parser.py               # Extract JSON data from SVG
│   ├── diagram_converter.py         # Base converter class
│   └── visio_builder.py            # Visio shape/connector management
├── project-management/              # PM diagram converters
│   ├── __init__.py
│   ├── gantt_chart.py              # Gantt chart converter
│   ├── project_charter.py          # Project charter converter
│   ├── wbs.py                      # Work Breakdown Structure
│   └── risk_matrix.py              # Risk matrix converter
├── sitemaps/                        # Sitemap converters
│   ├── __init__.py
│   └── sitemap_converter.py        # Sitemap hierarchy converter
└── utils/                           # Shared utilities
    └── __init__.py                  # Logging, path resolution
```

## Design

### Data-Driven Architecture

Each SVG template contains **embedded JSON data** that drives both web and Visio rendering:

```xml
<svg>
  <script type="application/json" id="gantt-data">
  {
    "projectName": "Food Delivery System",
    "tasks": [...],
    "timeline": {...},
    "designTokens": {...},
    "metadata": {...}
  }
  </script>
</svg>
```

### Single Source of Truth

- **Web rendering**: JavaScript reads JSON, populates SVG
- **Visio rendering**: Python reads same JSON, generates shapes and connectors
- **Consistency**: Both outputs derive from identical data

### Modular Converters

Each diagram type has its own converter:

| Diagram | Converter | Location | Data Schema |
|---------|-----------|----------|-------------|
| Gantt Chart | `GanttChartConverter` | `project-management/gantt_chart.py` | Timeline, phases, tasks, progress |
| Project Charter | `ProjectCharterConverter` | `project-management/project_charter.py` | Project info, stakeholders, budget |
| WBS | `WBSConverter` | `project-management/wbs.py` | Hierarchical task structure |
| Risk Matrix | `RiskMatrixConverter` | `project-management/risk_matrix.py` | Risk items, probability/impact |
| Sitemap | `SitemapConverter` | `sitemaps/sitemap_converter.py` | Page hierarchy, user flows |

## Base Classes

### `BaseDiagramConverter`

Abstract base class for all converters. Subclasses must implement:

```python
class MyDiagramConverter(BaseDiagramConverter):
    def render_diagram(self) -> None:
        """Subclass-specific rendering logic."""
        data = self.get_data()
        tokens = self.get_design_tokens()
        
        # Use self.builder to add shapes/connectors
        self.builder.add_shape(...)
        self.builder.add_connector(...)
```

**Available methods:**

- `get_data()` → Parsed JSON from template
- `get_design_tokens(mode='lightMode')` → Design tokens dictionary
- `get_summary()` → Conversion statistics

### `JSONDataParser`

Extracts and validates embedded JSON from SVG templates:

```python
template = JSONDataParser.parse_svg_template(svg_path)
print(template.data)           # Parsed JSON
print(template.design_tokens)  # Design tokens
print(template.metadata)       # Project metadata
```

### `VisioBuilder`

Manages Visio diagram construction:

```python
builder = VisioBuilder(output_path, "My Diagram")

# Add shapes
builder.add_shape(
    "rectangle",
    x=0.5, y=0.5,
    width=2.0, height=0.5,
    text="Task Label",
    style={"fill": "#E5E5E5", "stroke": "#1A1A1A"}
)

# Add connectors
builder.add_connector(from_shape_id=0, to_shape_id=1)

# Generate output
output_path = builder.build()
```

## Usage

### Single File Conversion

```bash
# Auto-detect diagram type from filename
python main.py -i template.svg -o output.vsdx

# Explicit diagram type
python main.py -i gantt.svg -o gantt.vsdx -d gantt-chart

# Verbose logging
python main.py -i template.svg -o output.vsdx -v
```

### Batch Conversion

```bash
# Convert all SVG files in directory
python main.py --batch ./templates/svg/project-management \
               --output-dir ./output/vsdx

# Custom file pattern
python main.py --batch ./templates/svg \
               --output-dir ./output \
               -p "*-dynamic.svg"
```

### List Supported Types

```bash
python main.py --list-types
```

Output:
```
Supported diagram types:
  - gantt-chart
  - gantt-project
  - gantt-resource
  - project-charter
  - risk-matrix
  - sitemap
  - wbs
  - work-breakdown-structure
```

## Creating Custom Converters

1. Create converter file in appropriate category folder:

```python
# sitemaps/my_diagram.py
from ..base import BaseDiagramConverter

class MyDiagramConverter(BaseDiagramConverter):
    def render_diagram(self) -> None:
        data = self.get_data()
        tokens = self.get_design_tokens()
        
        # Add shapes and connectors using self.builder
        self.builder.add_shape(...)
```

2. Register in main.py:

```python
from my_category import MyDiagramConverter

CONVERTER_REGISTRY = {
    ...
    "my-diagram": MyDiagramConverter,
    ...
}
```

3. Use immediately:

```bash
python main.py -i my-template.svg -o my-diagram.vsdx -d my-diagram
```

## Integration with Existing Stencil Code

The base converter leverages patterns from `/stencils/svg_to_visio_stencil/`:

- **SVG Parsing**: Similar XML parsing via ElementTree
- **Design Tokens**: Light/dark mode support matching brand guidelines
- **Shape Management**: Consistent shape/connector abstraction
- **Configuration**: JSON-based metadata and styling

Key differences:

- **Template-focused**: Works with SVG templates, not shape libraries
- **Data-driven**: Reads embedded JSON, not file manifests
- **Modular**: Individual diagram converters, not universal shape conversion
- **Dual-rendering**: Design tokens support web + Visio simultaneously

## Dependencies

Required packages:

```
lxml              # XML parsing
svg.path          # SVG path parsing (from existing stencils)
vsdx              # Visio file generation (future integration)
```

Optional for enhanced functionality:

```
aspose-diagram    # Advanced Visio features
python-pptx       # Alternative Visio generation
```

## Implementation Status

- ✅ Base converter framework (JSON parsing, Visio builder)
- ✅ Project management converters (Gantt, Charter, WBS, Risk Matrix)
- ✅ Sitemap converter
- ✅ Main orchestrator with CLI
- ⏳ Actual Visio generation (placeholder ready for library integration)
- ⏳ Template generation (.vstx, .vssx)
- ⏳ Advanced styling (gradients, images, effects)

## Future Enhancements

1. **Visio Library Integration**: Use `vsdx` or `aspose-diagram` for actual generation
2. **Template Generation**: Create .vstx and .vssx from diagrams
3. **Advanced Styling**: Gradients, images, connectors with custom shapes
4. **Performance**: Caching, parallel batch processing
5. **Validation**: Schema validation for SVG templates
6. **Web UI**: Interactive converter with preview

## Testing

```bash
# Test single conversion
python main.py -i ../svg/project-management/gantt-chart-dynamic.svg \
               -o test_output.vsdx -v

# Test batch conversion
python main.py --batch ../svg/project-management \
               --output-dir ./test_output -v
```

## Logging

Conversion logs are written to:
- **Console**: Real-time progress and errors
- **File**: `logs/conversion.log` (structured details)

Example:
```
2024-01-15 10:30:45 - svg_to_visio - INFO - Converting gantt-chart-dynamic.svg (gantt-chart)
2024-01-15 10:30:46 - svg_to_visio - DEBUG - Parsed template: Food Delivery System
2024-01-15 10:30:46 - svg_to_visio - DEBUG - Phase: Planning & Design (completed)
2024-01-15 10:30:47 - svg_to_visio - INFO - Conversion successful: 15 shapes, 8 connectors
```

## Contributing

To add a new diagram type:

1. **Identify category** (project-management, sitemaps, etc.)
2. **Create converter** in category folder
3. **Implement `render_diagram()`** method
4. **Register** in `CONVERTER_REGISTRY`
5. **Update README** with schema info
6. **Test** batch and single-file conversions

