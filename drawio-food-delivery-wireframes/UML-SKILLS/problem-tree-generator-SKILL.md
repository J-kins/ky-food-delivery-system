---
name: problem-tree-generator
description: Generate professional Problem Tree Diagrams in fully editable Visio format (.vsdx) using Aspose.Diagram for Python. This skill maps root causes, core problems, direct effects, and long-term effects into a strict hierarchical visual layout.
---

# Problem Tree Diagram Generator

This production-grade skill is explicitly designed to generate **Problem Tree Diagrams** in Microsoft Visio (`.vsdx`) format. It relies on `Aspose.Diagram for Python` for native Visio shape generation and layout construction. It can operate as a standalone skill or be invoked as a sub-component of the `project-charter-generator` skill.

## Table of Contents
1. Core Output Specifications
2. Environment Setup & Dependencies
3. Input Specification (JSON/YAML Schema)
4. Problem Tree Visual Layout (ASCII Blueprint)
5. Detailed Styling Specifications
6. Code Architecture
7. Core Implementation Code
8. Error Handling
9. Command-Line Interface (CLI)
10. Quality Checklist
11. Usage Examples
12. Integration with Existing Skills
13. Testing Strategy

---

## 1. Core Output Specifications

The Primary Purpose of this skill is to generate a complete Problem Tree diagram as a Visio file that includes:
1. **ROOTS (bottom):** Underlying causes (5 boxes maximum).
2. **TRUNK (center):** Core problem statement (1 box).
3. **BRANCHES (middle):** Direct effects (4 boxes maximum).
4. **LEAF (top):** Long-term effects (3 boxes maximum).
5. All connected with properly routed directional arrows flowing bottom-up (Roots → Trunk → Branches → Leaf).
6. Professional styling with consistent colors, fonts, and themes.
7. Auto-generated Legend and title block.
8. Fully editable discrete shapes in Microsoft Visio.

---

## 2. Environment Setup & Dependencies

For this generator to operate, the host environment must strictly conform to these dependencies.

### 2.1 Python Requirements
The generator expects modern Python typing and validation libraries.
```text
python >= 3.10
aspose-diagram-python >= 24.0.0
python-dotenv >= 1.0.0
pyyaml >= 6.0
pillow >= 10.0.0
typing-extensions >= 4.0.0
pydantic >= 2.0.0
```

### 2.2 System Dependencies

**Java Runtime Environment (JRE) 8 or higher**
- Required for `Aspose.Diagram for Python` (it uses JPype to interface with Java).
- *Installation guide:*
  - Ubuntu: `sudo apt-get install default-jre`
  - macOS: `brew install openjdk`
  - Windows: Download from https://www.java.com/download/

**Graphviz (optional, for preview generation)**
- For generating PNG/SVG previews if requested via CLI flag.
- *Installation guide:*
  - Ubuntu: `sudo apt-get install graphviz`
  - macOS: `brew install graphviz`
  - Windows: Download from https://graphviz.org/download/

### 2.3 Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate on Unix/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Install dependencies
pip install aspose-diagram-python python-dotenv pyyaml pillow pydantic typing-extensions
```

### 2.4 Environment Variables (.env file)
```env
# Aspose.Diagram License (if commercial, to remove evaluation watermark)
ASPOSE_DIAGRAM_LICENSE_PATH=/path/to/license.lic

# Output directory
OUTPUT_DIR=./output

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Default styling
DEFAULT_COLOR_THEME=enterprise_blue
DEFAULT_FONT_FAMILY=Arial
DEFAULT_FONT_SIZE=10
```

---

## 3. Input Specification

The skill accepts a structured JSON or YAML payload validated by Pydantic models.

```json
{
  "problem_tree": {
    "title": "Da'atSNA Problem Tree",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    
    "core_problem": {
      "id": "TRUNK",
      "statement": "No integrated, offline-first platform exists that lets Ugandan communities collect, analyze, and visualize social network data",
      "description": "The central problem that the project aims to solve"
    },
    
    "roots": [
      {
        "id": "R1",
        "statement": "No accessible SNA tools designed for low-literacy, low-tech environments",
        "description": "Underlying cause 1"
      },
      {
        "id": "R2",
        "statement": "Lack of investment in local data infrastructure & training",
        "description": "Underlying cause 2"
      },
      {
        "id": "R3",
        "statement": "Policy-makers don't recognize the value of network data",
        "description": "Underlying cause 3"
      },
      {
        "id": "R4",
        "statement": "Cultural & language barriers in existing international tools",
        "description": "Underlying cause 4"
      },
      {
        "id": "R5",
        "statement": "No business model for sustainable data collection at community level",
        "description": "Underlying cause 5"
      }
    ],
    
    "branches": [
      {
        "id": "B1",
        "statement": "Cooperatives & savings groups can't identify their own influence",
        "description": "Direct effect 1"
      },
      {
        "id": "B2",
        "statement": "NGO & government interventions spread thinly instead of targeted at high-level leverage",
        "description": "Direct effect 2"
      },
      {
        "id": "B3",
        "statement": "Field researchers have no low-cost, offline way to collect network data",
        "description": "Direct effect 3"
      },
      {
        "id": "B4",
        "statement": "Existing SNA tools demand technical skill, constant internet & give no Uganda-specific data",
        "description": "Direct effect 4"
      }
    ],
    
    "leaf": [
      {
        "id": "L1",
        "statement": "Persistent exclusion of youth, women & informal workers from data-driven decision-making",
        "description": "Long-term effect 1"
      },
      {
        "id": "L2",
        "statement": "Informal economy stays largely invisible to policy & investment despite its economic importance",
        "description": "Long-term effect 2"
      },
      {
        "id": "L3",
        "statement": "Parish Development Model / Emyooga interventions under-perform for lack of target",
        "description": "Long-term effect 3"
      }
    ],
    
    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 10,
      "arrow_style": "curved",
      "shadow_enabled": true,
      "corner_radius": 8
    },
    
    "layout": {
      "orientation": "top_to_bottom",
      "page_size": "A3",
      "margin": 0.5,
      "node_spacing": 40,
      "rank_spacing": 60
    }
  }
}
```

---

## 4. Problem Tree Visual Layout (ASCII Blueprint)

The backend code calculates the bounding box and orthogonal connectors to match this exact logical layout:

```text
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PROBLEM TREE DIAGRAM                                   │
│                         Da'atSNA Community Data Platform                            │
│                         Version 1.0  |  2026-06-17                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│                    ┌─────────────────────────────────────────────┐                  │
│                    │         LEAF - Long-Term Effects            │                  │
│                    ├─────────────────────────────────────────────┤                  │
│                    │  L1: Persistent exclusion of youth, women   │                  │
│                    │      & informal workers from data-driven    │                  │
│                    │      decision-making                        │                  │
│                    ├─────────────────────────────────────────────┤                  │
│                    │  L2: Informal economy stays largely         │                  │
│                    │      invisible to policy & investment       │                  │
│                    ├─────────────────────────────────────────────┤                  │
│                    │  L3: PDM/Emyooga interventions under-perform│                  │
│                    │      for lack of targeting                  │                  │
│                    └───────────────────┬─────────────────────────┘                  │
│                                        │                                            │
│                                        │                                            │
│          ┌─────────────────────────────┼─────────────────────────────┐              │
│          │                             │                             │              │
│          ▼                             ▼                             ▼              │
│ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐        │
│ │    BRANCH - Direct   │ │    BRANCH - Direct   │ │    BRANCH - Direct   │        │
│ │    Effects           │ │    Effects           │ │    Effects           │        │
│ ├──────────────────────┤ ├──────────────────────┤ ├──────────────────────┤        │
│ │  B1: Cooperatives &  │ │  B2: NGO & gov       │ │  B3: Field           │        │
│ │  savings groups can't│ │  interventions spread│ │  researchers have no │        │
│ │  identify their own  │ │  thinly instead of   │ │  low-cost, offline   │        │
│ │  influence           │ │  targeted at high-   │ │  way to collect      │        │
│ │                      │ │  level leverage      │ │  network data        │        │
│ └──────────┬───────────┘ └──────────┬───────────┘ └──────────┬───────────┘        │
│            │                        │                        │                      │
│            └────────────────────────┼────────────────────────┘                      │
│                                     ▼                                               │
│                    ┌─────────────────────────────────────────────┐                  │
│                    │         TRUNK - Core Problem                │                  │
│                    ├─────────────────────────────────────────────┤                  │
│                    │  No integrated, offline-first platform      │                  │
│                    │  exists that lets Ugandan communities      │                  │
│                    │  collect, analyze, and visualize           │                  │
│                    │  social network data                        │                  │
│                    └───────────────────┬─────────────────────────┘                  │
│                                        │                                            │
│          ┌─────────────────────────────┼─────────────────────────────┐              │
│          │                             │                             │              │
│          ▼                             ▼                             ▼              │
│ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐        │
│ │    ROOT - Causes     │ │    ROOT - Causes     │ │    ROOT - Causes     │        │
│ ├──────────────────────┤ ├──────────────────────┤ ├──────────────────────┤        │
│ │  R1: No accessible   │ │  R2: Lack of         │ │  R3: Policy-makers   │        │
│ │  SNA tools designed  │ │  investment in local │ │  don't recognize     │        │
│ │  for low-literacy,   │ │  data infrastructure │ │  the value of        │        │
│ │  low-tech            │ │  & training          │ │  network data        │        │
│ │  environments        │ │                      │ │                      │        │
│ └──────────────────────┘ └──────────────────────┘ └──────────────────────┘        │
│                                                                                     │
│          ┌──────────────────────────────┐ ┌──────────────────────────────┐          │
│          │    ROOT - Causes             │ │    ROOT - Causes             │          │
│          ├──────────────────────────────┤ ├──────────────────────────────┤          │
│          │  R4: Cultural & language     │ │  R5: No business model for   │          │
│          │  barriers in existing        │ │  sustainable data collection │          │
│          │  international tools         │ │  at community level          │          │
│          └──────────────────────────────┘ └──────────────────────────────┘          │
│                                                                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  Legend:  ⚪ Roots (Causes)  🔷 TRUNK (Core Problem)  🔶 Branches (Effects)  🔺 LEAF│
│  (Long-term Effects)                                                                │
│  Arrows show causal direction: ROOTS → TRUNK → BRANCHES → LEAF                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Detailed Styling Specifications

### 5.1 Color Palette

| Element | Color Name | Hex Code | RGB | Usage |
|---------|------------|----------|-----|-------|
| Roots | Light Red | `#EF9A9A` | (239,154,154) | Background for root cause boxes |
| Roots Border | Red | `#E53935` | (229,57,53) | Border for root cause boxes |
| Roots Text | Dark Red | `#B71C1C` | (183,28,28) | Text in root cause boxes |
| TRUNK | Orange | `#FFCC80` | (255,204,128) | Background for core problem box |
| TRUNK Border | Dark Orange | `#F57C00` | (245,124,0) | Border for core problem box |
| TRUNK Text | Dark Orange | `#E65100` | (230,81,0) | Text in core problem box |
| Branches | Light Blue | `#90CAF9` | (144,202,249) | Background for direct effect boxes |
| Branches Border | Blue | `#1565C0` | (21,101,192) | Border for direct effect boxes |
| Branches Text | Dark Blue | `#0D47A1` | (13,71,161) | Text in direct effect boxes |
| LEAF | Light Green | `#A5D6A7` | (165,214,167) | Background for long-term effect boxes |
| LEAF Border | Green | `#2E7D32` | (46,125,50) | Border for long-term effect boxes |
| LEAF Text | Dark Green | `#1B5E20` | (27,94,32) | Text in long-term effect boxes |
| Connectors | Grey | `#666666` | (102,102,102) | Arrow lines |
| Connector Text | Dark Grey | `#444444` | (68,68,68) | Labels on arrows |
| Title | Dark Blue | `#1a237e` | (26,35,126) | Title text |
| Background | White | `#FFFFFF` | (255,255,255) | Page background |
| Legend | Light Grey | `#F5F5F5` | (245,245,245) | Legend background |

### 5.2 Box Styling

| Property | Value | Description |
|----------|-------|-------------|
| Shape | Rounded Rectangle | Use `shape_type="rectangle"` with corner rounding in Aspose |
| Corner Radius | 8pt | Rounded corners for all boxes |
| Shadow | Enabled | Subtle drop shadow: offset (2pt, 2pt), blur 4pt |
| Font Family | Arial | Professional, readable |
| Font Size | 10pt | Regular text |
| Font Size (Title) | 12pt | Bold, for box titles |
| Line Width | 1.5pt | Border thickness |
| Padding | 8pt | Internal padding for text |
| Text Alignment | Center | Horizontal and vertical centering |
| Text Wrapping | Wrap | Word wrap within box bounds |

### 5.3 Arrow Styling

| Property | Value | Description |
|----------|-------|-------------|
| Line Color | `#666666` | Grey lines |
| Line Width | 1pt | Standard connector width |
| Arrowhead | Filled triangle | Standard Visio arrowhead (`ArrowType.Triangle`) |
| Arrow Size | 8pt | Arrowhead size |
| Routing | Curved | Orthogonal routing with curve (`ConLineRouteExt`) |
| Label Font Size| 8pt | Smaller text for arrow labels |
| Label Color | `#444444` | Dark grey |
| Gap | 2pt | Gap between arrow and shape |

---

## 6. Code Architecture

Structure the standalone codebase as follows:

```text
problem_tree_generator/
├── __init__.py
├── skill.md                       # This skill file
├── core/
│   ├── __init__.py
│   ├── diagram_builder.py         # Main orchestration
│   ├── validator.py               # Input validation (Pydantic)
│   ├── errors.py                  # Custom exceptions
│   └── models.py                  # Pydantic models for JSON schema
├── renderers/
│   ├── __init__.py
│   ├── aspose_renderer.py         # Aspose.Diagram rendering API wrapper
│   ├── dot_generator.py           # Graphviz DOT (for SVG/PNG previews)
│   └── layout_engine.py           # Mathematics for grid coordinate placement
├── stylers/
│   ├── __init__.py
│   ├── color_themes.py            # Hex mappings
│   ├── shape_styler.py            # Aspose shape decorators
│   └── connector_styler.py        # Aspose line routing decorators
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   └── geometry_utils.py
├── templates/
│   └── problem_tree_template.vstx  # Stencil template (avoids drawing from scratch)
├── config/
│   ├── __init__.py
│   └── settings.py                 # dotenv loaders
└── cli.py                          # Command-line interface
```

---

## 7. Core Implementation Code

### 7.1 Diagram Builder Class (`core/diagram_builder.py`)

```python
from aspose.diagram import Diagram, Page, Shape, SaveFileFormat
from typing import List, Dict
import logging

class ProblemTreeBuilder:
    """Main class for building problem tree diagrams in Aspose.Diagram."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
    
    def _setup_page(self) -> None:
        """Configure page size and orientation."""
        page_size = self.config.get("layout", {}).get("page_size", "A3")
        # Set page dimensions in cm (Aspose defaults to inches, conversion required)
        if page_size == "A3":
            self.page.page_sheet.page_props.page_width.value = 16.53  # inches
            self.page.page_sheet.page_props.page_height.value = 11.69
        elif page_size == "A4":
            self.page.page_sheet.page_props.page_width.value = 11.69
            self.page.page_sheet.page_props.page_height.value = 8.27
        else:
            self.page.page_sheet.page_props.page_width.value = 16.53
            self.page.page_sheet.page_props.page_height.value = 11.69
    
    def _setup_styles(self) -> None:
        """Set up global styling defaults."""
        style_cfg = self.config.get("styling", {})
        self.theme = style_cfg.get("theme", "enterprise_blue")
        self.font_family = style_cfg.get("font_family", "Arial")
        self.font_size = style_cfg.get("font_size", 10)
        self.corner_radius = style_cfg.get("corner_radius", 8)
        self.shadow_enabled = style_cfg.get("shadow_enabled", True)
    
    def add_title_block(self, title: str, subtitle: str, version: str, date: str) -> None:
        """Add title block at top of diagram."""
        logging.debug(f"Adding title block: {title}")
        # Insert a background rectangle at top of page and append text blocks
        pass
    
    def add_roots(self, roots: List[Dict]) -> None:
        """Add root cause boxes at bottom."""
        # Calculate Y position near bottom margin, distribute X evenly
        pass
    
    def add_trunk(self, core_problem: Dict) -> None:
        """Add core problem box in center."""
        pass
    
    def add_branches(self, branches: List[Dict]) -> None:
        """Add direct effect boxes in middle."""
        pass
    
    def add_leaf(self, leaf_nodes: List[Dict]) -> None:
        """Add long-term effect boxes at top."""
        pass
    
    def add_connectors(self) -> None:
        """Add all directional arrows between boxes."""
        # Loop through root->trunk, trunk->branches, branches->leaf
        pass
    
    def add_legend(self) -> None:
        """Add legend explaining colors and symbols."""
        pass
    
    def save(self, output_path: str) -> None:
        """Save diagram to .vsdx file."""
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

### 7.2 Layout Engine (`renderers/layout_engine.py`)

```python
from typing import List, Dict

class LayoutEngine:
    """Calculates physical coordinates for all diagram elements."""
    
    def __init__(self, page_width: float, page_height: float):
        self.page_width = page_width
        self.page_height = page_height
        self.margin = 0.5  # inches
        self.box_height = 1.2 # inches
        
    def calculate_positions(self, spec: Dict) -> Dict:
        """Calculate (x, y, width, height) for all boxes.
        Returns a dict mapping Node ID to geometry specs."""
        positions = {}
        
        # Bottom-up Y coordinate assignment
        y_roots = self.margin + self.box_height / 2
        y_trunk = y_roots + 2.0
        y_branches = y_trunk + 2.0
        y_leaf = y_branches + 2.0
        
        positions.update(self._distribute_horizontal(spec['roots'], y_roots))
        positions[spec['core_problem']['id']] = self._center_box(y_trunk)
        positions.update(self._distribute_horizontal(spec['branches'], y_branches))
        positions.update(self._distribute_horizontal(spec['leaf'], y_leaf))
        
        return positions
    
    def _distribute_horizontal(self, nodes: List[Dict], y_pos: float) -> Dict:
        """Distributes a list of nodes evenly across the horizontal page space."""
        # Implementation divides (page_width - 2*margin) by len(nodes)
        pass

    def _center_box(self, y_pos: float) -> Dict:
        """Calculates X coordinate for the absolute center of the page."""
        return {"x": self.page_width / 2.0, "y": y_pos, "w": 2.5, "h": 1.5}
```

### 7.3 Shape Builder (`stylers/shape_styler.py`)

```python
class ShapeBuilder:
    """Creates styled shapes for the diagram via Aspose."""
    
    @staticmethod
    def create_rounded_rectangle(diagram, x: float, y: float, width: float, height: float,
                                  fill_color: str, border_color: str, 
                                  text: str, font_size: int = 10,
                                  corner_radius: int = 8,
                                  shadow: bool = True) -> int:
        """Create a styled rounded rectangle shape and return its internal ID."""
        # Implementation using Aspose.Diagram API
        # e.g. shape_id = diagram.add_shape(x, y, width, height, "Rectangle", 0)
        # shape = diagram.pages[0].shapes.get_shape(shape_id)
        # shape.fill.fill_foregnd.value = fill_color
        # shape.line.line_color.value = border_color
        pass
    
    @staticmethod
    def create_connector(diagram, source_id: int, target_id: int,
                         color: str = "#666666",
                         label: str = "") -> None:
        """Create a styled dynamic connector with arrowhead."""
        # shape = diagram.add_shape(...) 
        # diagram.pages[0].connect_shapes_via_connector(...)
        pass
```

---

## 8. Error Handling

For enterprise reliability, exceptions are caught, wrapped, and categorized into strict Error Codes.

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| `PT-001` | InvalidInput | Input JSON missing required fields | Validate against Pydantic schema in `validator.py` |
| `PT-002` | MissingCoreProblem| No core problem specified | Provide `core_problem` object |
| `PT-003` | TooManyRoots | More than 5 root causes | Reduce to max 5 to prevent horizontal overflow |
| `PT-004` | TooManyBranches | More than 4 direct effects | Reduce to max 4 |
| `PT-005` | TooManyLeaf | More than 3 long-term effects | Reduce to max 3 |
| `PT-006` | EmptyStatement | Box statement is empty | Provide text for all boxes |
| `PT-007` | JavaNotInstalled | Java runtime not found | Install JRE 8+ (JPype requires it) |
| `PT-008` | LicenseMissing | Aspose license missing | Configure `ASPOSE_DIAGRAM_LICENSE_PATH` or accept evaluation watermark |
| `PT-009` | LayoutError | Layout calculation failed | Check input geometry limits |
| `PT-010` | RenderError | Rendering failed | Check Aspose.Diagram installation |

---

## 9. Command-Line Interface (CLI)

The CLI offers explicit flags for validation, theme overrides, and debugging.

```python
# cli.py
import argparse
import json
import sys
import logging
from core.diagram_builder import ProblemTreeBuilder

def main():
    parser = argparse.ArgumentParser(
        description="Generate a Problem Tree Diagram in Visio format"
    )
    parser.add_argument("input", help="Path to input JSON/YAML specification file")
    parser.add_argument("-o", "--output", help="Output path (default: ./output/problem_tree.vsdx)")
    parser.add_argument("-p", "--preview", action="store_true", help="Generate PNG preview as well")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--validate-only", action="store_true", help="Only validate input, don't render")
    parser.add_argument("--theme", choices=["enterprise_blue", "dark_modern", "corporate_green", "material"], help="Color theme to use")
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    # Load input
    with open(args.input, 'r') as f:
        spec = json.load(f)
        
    # Validate
    from core.validator import validate_schema
    try:
        validate_schema(spec)
    except Exception as e:
        logging.error(f"PT-001 Validation Error: {e}")
        sys.exit(1)
        
    if args.validate_only:
        logging.info("Validation successful. Exiting.")
        sys.exit(0)
        
    # Apply overrides
    if args.theme:
        spec['problem_tree']['styling']['theme'] = args.theme
        
    # Build
    builder = ProblemTreeBuilder(spec['problem_tree'])
    # Execute build steps...
    out_path = args.output or "./output/problem_tree.vsdx"
    builder.save(out_path)
    logging.info(f"Successfully saved Visio diagram to {out_path}")

if __name__ == "__main__":
    main()
```

---

## 10. Quality Checklist

Before finalizing or delivering the diagram, verify:

- [ ] **Text Containment:** All boxes have proper text wrapping without overflowing shape boundaries.
- [ ] **Color Integrity:** Colors are consistent with the hex definitions in the Theme specifications.
- [ ] **Routing:** Connectors are properly orthogonally routed without messy diagonal intersections.
- [ ] **Causality:** Arrowheads face the correct direction (`ROOTS → TRUNK → BRANCHES → LEAF`).
- [ ] **Legend:** Legend block is present in the lower corner explaining all colors and node definitions.
- [ ] **Title Block:** Title block contains all requested metadata (Title, Project, Version, Date).
- [ ] **Fit to Page:** Diagram fits perfectly on an A3 or A4 page with appropriate margins.
- [ ] **Typography:** Fonts are strictly mapped to Arial 10pt (body) and 12pt (headers).
- [ ] **Shadows:** Drop shadow effects and corner radii are uniformly applied to all shape instances.

---

## 11. Usage Examples

### 11.1 Basic Generation
```bash
python problem_tree_generator/cli.py examples/daat_sna.json -o output/daat_tree.vsdx
```

### 11.2 Generation with PNG Preview (Requires Graphviz)
```bash
python problem_tree_generator/cli.py input.json -o output/tree.vsdx --preview
```

### 11.3 Validate Payload in CI/CD Pipeline
```bash
python problem_tree_generator/cli.py input.json --validate-only
```

### 11.4 Override Theme
```bash
python problem_tree_generator/cli.py input.json -o output/tree.vsdx --theme corporate_green
```

---

## 12. Integration with Existing Skills

This skill operates within a broader diagramming ecosystem:
1.  **Component of `project-charter-generator`:** The CLI can be invoked programmatically from `core/charter_builder.py` to generate the risk/problem analysis diagram.
2.  **Aligns with `uml-diagram-generator-SKILL.md`:** Uses the identical underlying JSON specification philosophy. If a user needs a Problem Tree represented as a pure UML Class Diagram instead of this specialized hierarchical model, fallback to the UML generator.
3.  **Embeddable Output:** The `--preview` flag rasterizes the layout to PNG/SVG using Graphviz so it can be securely embedded directly into Word/PDF documents by the upstream generator.

---

## 13. Testing Strategy

Maintain test reliability across major library updates by providing these test fixtures:

1.  **Minimal Input Test:** Feed JSON with exactly 1 Root, 1 Trunk, 1 Branch, and 1 Leaf. Assert generation succeeds.
2.  **Maximum Stress Test:** Feed JSON with 5 Roots, 4 Branches, 3 Leaves, and verbose paragraph text. Assert text wraps correctly and does not breach margins.
3.  **Validation Test (Missing Fields):** Remove `core_problem` block. Assert `PT-002` exception is raised.
4.  **Validation Test (Overflow):** Feed 8 Roots. Assert `PT-003` exception is raised.
5.  **Output Byte Hash Test:** Generate a `.vsdx` file with static mock data, unzip it, and hash `page1.xml`. Ensure the topological structure does not regress across releases.
