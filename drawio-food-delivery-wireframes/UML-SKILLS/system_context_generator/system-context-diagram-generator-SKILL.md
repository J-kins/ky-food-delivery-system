---
name: system-context-diagram-generator
description: Generate professional System Context Diagrams (Level 0) in fully editable Visio format (.vsdx) using Aspose.Diagram for Python. This skill maps the system boundary, external entities, and data flows in a precise, standardized layout.
---

# System Context Diagram (Level 0) Generator

This production-grade skill is specifically engineered to generate **System Context Diagrams (Level 0)** in Microsoft Visio (`.vsdx`) format. Leveraging `Aspose.Diagram for Python`, it provides an automated pipeline for turning structured JSON specifications into accurate architectural context maps showing a central system and its interacting external environments.

This tool functions as a standalone capability or as an integrated sub-component of the broader `project-charter-generator`.

## Table of Contents
1. Core Output Specifications
2. Environment Setup & Dependencies
3. Input Specification (JSON/YAML Schema)
4. System Context Visual Layout (ASCII Blueprint)
5. External Entity Types and Positioning
6. Detailed Styling Specifications
7. Code Architecture
8. Core Implementation Code
9. Error Handling
10. Command-Line Interface (CLI)
11. Quality Checklist
12. Usage Examples
13. Integration with Existing Skills
14. Testing Strategy

---

## 1. Core Output Specifications

The primary purpose of this skill is to generate a comprehensive Level 0 Context Diagram that guarantees:
1. **Central System Box:** A clearly defined central boundary representing the target system (e.g., Healthcare Ecosystem).
2. **External Entities:** Accurate spatial placement of users, external systems, organizations, and regulatory bodies surrounding the core system.
3. **Data Flows:** Explicit directional or bi-directional arrows connecting external entities to the central system, fully labeled with data formats.
4. **System Boundaries:** Proper dashed demarcation lines encapsulating the core system logic.
5. **Professional Styling:** Fully editable, corporate-themed Microsoft Visio shapes (`.vsdx`), complete with legends and title blocks.

---

## 2. Environment Setup & Dependencies

For this generator to operate, the host environment must strictly conform to these dependencies.

### 2.1 Python Requirements
The generator relies heavily on mathematical geometry logic and Pydantic validation.
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
- Required for `Aspose.Diagram for Python` (interfacing via JPype).
- *Installation guide:*
  - Ubuntu: `sudo apt-get install default-jre`
  - macOS: `brew install openjdk`
  - Windows: Download from https://www.java.com/download/

**Graphviz (optional, for preview generation)**
- For generating rasterized PNG/SVG previews if requested.
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

## 3. Input Specification (JSON/YAML Schema)

The generator enforces a strict JSON input schema to define spatial and logical relationships.

```json
{
  "system_context": {
    "title": "Healthcare Ecosystem System Context Diagram",
    "system_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    "description": "A community-driven data platform for Ugandan healthcare stakeholders",
    
    "system": {
      "id": "SYSTEM",
      "name": "Healthcare Ecosystem",
      "description": "Central platform for healthcare data collection, analysis, and visualization",
      "boundary_style": "double_line"
    },
    
    "external_entities": [
      {
        "id": "E1",
        "name": "Patients",
        "type": "user",
        "description": "End users accessing healthcare services",
        "position": "top-left",
        "data_flows": [
          {
            "direction": "bidirectional",
            "label": "Patient Data (Registration, Medical Records)",
            "data_type": "JSON"
          }
        ]
      },
      {
        "id": "E2",
        "name": "Doctors",
        "type": "user",
        "description": "Healthcare providers",
        "position": "left",
        "data_flows": [
          {
            "direction": "bidirectional",
            "label": "Consultation Requests, Patient Information",
            "data_type": "JSON/XML"
          }
        ]
      },
      {
        "id": "E3",
        "name": "Pharmacies",
        "type": "system",
        "description": "Dispensing and inventory services",
        "position": "bottom-left",
        "data_flows": [
          {
            "direction": "bidirectional",
            "label": "Prescriptions, Medication Inventory",
            "data_type": "JSON"
          }
        ]
      },
      {
        "id": "E4",
        "name": "Laboratories",
        "type": "system",
        "description": "Testing and diagnostic services",
        "position": "right",
        "data_flows": [
          {
            "direction": "bidirectional",
            "label": "Lab Orders, Test Results",
            "data_type": "HL7/FHIR"
          }
        ]
      },
      {
        "id": "E5",
        "name": "Ministry of Health",
        "type": "organization",
        "description": "Regulatory body",
        "position": "bottom-right",
        "data_flows": [
          {
            "direction": "bidirectional",
            "label": "Regulatory Reports, Compliance Data",
            "data_type": "PDF/CSV"
          }
        ]
      },
      {
        "id": "E6",
        "name": "Insurance Companies",
        "type": "organization",
        "description": "Claims and payment processors",
        "position": "right",
        "data_flows": [
          {
            "direction": "bidirectional",
            "label": "Insurance Claims, Payment Processing",
            "data_type": "EDI/XML"
          }
        ]
      },
      {
        "id": "E7",
        "name": "External Systems",
        "type": "system",
        "description": "HIS, National Health Database",
        "position": "bottom",
        "data_flows": [
          {
            "direction": "bidirectional",
            "label": "Health Data Exchange, National Integration",
            "data_type": "FHIR/HL7"
          }
        ]
      },
      {
        "id": "E8",
        "name": "Payment Gateways",
        "type": "system",
        "description": "Financial transaction processing",
        "position": "bottom",
        "data_flows": [
          {
            "direction": "bidirectional",
            "label": "Payment Transactions, Receipts",
            "data_type": "JSON"
          }
        ]
      }
    ],
    
    "system_boundary": {
      "type": "rectangle",
      "line_style": "dashed",
      "line_width": 2,
      "color": "#1a237e",
      "label": "System Boundary"
    },
    
    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 10,
      "arrow_style": "orthogonal",
      "shadow_enabled": true,
      "corner_radius": 8
    },
    
    "layout": {
      "orientation": "landscape",
      "page_size": "A3",
      "margin": 0.5,
      "system_box_width": 8.0,
      "system_box_height": 6.0,
      "entity_spacing": 1.5
    }
  }
}
```

---

## 4. System Context Visual Layout (ASCII Blueprint)

**CRITICAL REQUIREMENT:** The Visio layout engine mathematically routes boxes to conform exactly to these spatial blueprints.

### 4.1 Generic System Layout Blueprint
```text
                              ┌─────────────────────────────┐
                              │      External Entity       │
                              │      [Entity Name]         │
                              │      [Description]         │
                              └──────────────┬──────────────┘
                                             │
                                    ┌────────┴────────┐
                                    │   Data Flow     │
                                    │   [Label]       │
                                    └────────┬────────┘
                                             │
                                             ▼
                    ┌─────────────────────────────────────────────────────┐
                    │                                                     │
                    │                  SYSTEM BOUNDARY                    │
                    │    ┌───────────────────────────────────────────┐   │
                    │    │                                           │   │
     ┌──────────────┼────┤         HEALTHCARE ECOSYSTEM             ├───┼──────────────┐
     │              │    │                                           │   │              │
     │  External    │    │      System Name                          │   │  External    │
     │  Entity      │    │      [System Name]                       │   │  Entity      │
     │  [Name]      │    │                                           │   │  [Name]      │
     │              │    └───────────────────────────────────────────┘   │              │
     └──────────────┘                                                    └──────────────┘
                    │                                                     │
                    │                                                     │
                    └─────────────────────────────────────────────────────┘
                                             │
                                             │
                                    ┌────────┴────────┐
                                    │   Data Flow     │
                                    │   [Label]       │
                                    └────────┬────────┘
                                             │
                                             ▼
                              ┌─────────────────────────────┐
                              │      External Entity       │
                              │      [Entity Name]         │
                              │      [Description]         │
                              └─────────────────────────────┘
```

### 4.2 Detailed Healthcare Ecosystem Blueprint
```text
                              ┌──────────────────────────────────┐
                              │          PATIENTS               │
                              │   (End Users / Beneficiaries)   │
                              └────────────────┬─────────────────┘
                                               │
                                    ┌──────────┴──────────┐
                                    │  Patient Data      │
                                    │  Registration,     │
                                    │  Medical Records   │
                                    └──────────┬──────────┘
                                               │
                                               ▼
┌─────────────────────────────┐    ┌─────────────────────────────────────┐    ┌─────────────────────────────┐
│                             │    │                                     │    │                             │
│      DOCTORS               │    │          HEALTHCARE                  │    │      LABORATORIES           │
│   (Healthcare Providers)   │◄───┤          ECOSYSTEM                  ├───►│   (Testing Services)        │
│                             │    │                                     │    │                             │
│  ┌───────────────────────┐ │    │   ┌─────────────────────────────┐  │    │  ┌───────────────────────┐ │
│  │ Consultation Requests │ │    │   │                             │  │    │  │ Lab Orders & Results  │ │
│  │ Patient Information   │ │    │   │  Da'atSNA Community         │  │    │  │ Test Reports          │ │
│  └───────────────────────┘ │    │   │  Data Platform             │  │    │  └───────────────────────┘ │
│                             │    │   │                             │  │    │                             │
└─────────────────────────────┘    │   └─────────────────────────────┘  │    └─────────────────────────────┘
                                    │                                     │
                                    │                                     │
                                    │                                     │
┌─────────────────────────────┐    │   ┌─────────────────────────────┐  │    ┌─────────────────────────────┐
│                             │    │   │   System Boundary            │  │    │                             │
│      PHARMACIES             │◄───┤   └─────────────────────────────┘  ├───►│      INSURANCE              │
│   (Dispensing Services)     │    │                                     │    │   (Claims Processing)       │
│                             │    │                                     │    │                             │
│  ┌───────────────────────┐ │    │                                     │    │  ┌───────────────────────┐ │
│  │ Prescriptions         │ │    │                                     │    │  │ Insurance Claims      │ │
│  │ Medication Inventory  │ │    │                                     │    │  │ Payment Processing    │ │
│  └───────────────────────┘ │    │                                     │    │  └───────────────────────┘ │
│                             │    │                                     │    │                             │
└─────────────────────────────┘    │                                     │    └─────────────────────────────┘
                                    │                                     │
                                    │                                     │
┌─────────────────────────────┐    │                                     │    ┌─────────────────────────────┐
│                             │    │                                     │    │                             │
│      MINISTRY OF HEALTH     │◄───┤                                     ├───►│      EXTERNAL SYSTEMS       │
│    (Regulatory Body)        │    │                                     │    │   (HIS, National Database)  │
│                             │    │                                     │    │                             │
│  ┌───────────────────────┐ │    │                                     │    │  ┌───────────────────────┐ │
│  │ Regulatory Reports    │ │    │                                     │    │  │ Health Data Exchange  │ │
│  │ Compliance Data       │ │    │                                     │    │  │ National Integration  │ │
│  └───────────────────────┘ │    │                                     │    │  └───────────────────────┘ │
│                             │    │                                     │    │                             │
└─────────────────────────────┘    └─────────────────────────────────────┘    └─────────────────────────────┘
                                               │
                                               │
                                               ▼
                              ┌──────────────────────────────────┐
                              │     PAYMENT GATEWAYS             │
                              │   (Financial Processing)         │
                              └──────────────────────────────────┘
```

---

## 5. External Entity Types and Positioning

Each node type leverages specific icon conventions and semantic colors to instantly telegraph system interactions.

| Type | Icon / Shape Overlay | Color | Typical Position |
|------|----------------------|-------|------------------|
| **User** | Person icon | `#4CAF50` (Green) | Top, Left |
| **System** | Server icon | `#2196F3` (Blue) | Right, Bottom |
| **Organization**| Building icon | `#FF9800` (Orange) | Bottom, Right |
| **Regulatory** | Shield icon | `#F44336` (Red) | Bottom, Right |

---

## 6. Detailed Styling Specifications

### 6.1 Color Palette

| Element | Color Name | Hex Code | RGB | Usage |
|---------|------------|----------|-----|-------|
| System Box Fill | Light Blue | `#E3F2FD` | (227,242,253) | System background |
| System Box Border | Dark Blue | `#1565C0` | (21,101,192) | System border |
| System Box Text | Dark Blue | `#0D47A1` | (13,71,161) | System name |
| External Entity Fill| Light Grey | `#F5F5F5` | (245,245,245) | Entity background |
| External Entity Border| Grey | `#78909C` | (120,144,156) | Entity border |
| External Entity Text| Dark Grey | `#37474F` | (55,71,79) | Entity name |
| User Entity | Green | `#4CAF50` | (76,175,80) | User types color |
| System Entity | Blue | `#2196F3` | (33,150,243) | System types color |
| Org Entity | Orange | `#FF9800` | (255,152,0) | Organization color |
| Regulatory Entity | Red | `#F44336` | (244,67,54) | Regulatory color |
| Data Flow Line | Grey | `#666666` | (102,102,102) | Arrow lines |
| Data Flow Label | Dark Grey | `#444444` | (68,68,68) | Arrow labels |
| System Boundary | Dark Blue | `#1a237e` | (26,35,126) | Dashed boundary |
| Title | Dark Blue | `#1a237e` | (26,35,126) | Title text |
| Background | White | `#FFFFFF` | (255,255,255) | Page background |
| Legend | Light Grey | `#F5F5F5` | (245,245,245) | Legend background |

### 6.2 Arrow/Data Flow Styling

| Property | Value | Description |
|----------|-------|-------------|
| Line Color | `#666666` | Grey lines |
| Line Width | 1pt | Standard connector width |
| Arrowhead | Filled triangle | Standard Visio arrowhead |
| Arrow Size | 8pt | Arrowhead size |
| Routing | Orthogonal | Right-angle routing for clean lines |
| Label Font Size | 8pt | Smaller text for arrow labels |
| Label Color | `#444444` | Dark grey |
| Label Position | Middle | Centered on the line |
| Bi-directional | Two arrowheads | Both ends have arrowheads if flow goes both ways |

---

## 7. Code Architecture

```text
system_context_generator/
├── __init__.py
├── skill.md                       # This skill file
├── core/
│   ├── __init__.py
│   ├── diagram_builder.py         # Main orchestration
│   ├── validator.py               # Input validation (JSON schemas)
│   ├── errors.py                  # Custom exceptions
│   └── models.py                  # Pydantic models
├── renderers/
│   ├── __init__.py
│   ├── aspose_renderer.py         # Aspose.Diagram rendering API
│   ├── dot_generator.py           # Graphviz DOT (for SVG/PNG previews)
│   └── layout_engine.py           # Grid mathematics for absolute coordinate calculations
├── stylers/
│   ├── __init__.py
│   ├── color_themes.py            # Color theme definitions
│   ├── shape_styler.py            # Box rendering utilities
│   ├── entity_styler.py           # Sub-classes for User/Org icons
│   └── connector_styler.py        # Connector and label styling
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   └── geometry_utils.py
├── templates/
│   └── system_context_template.vstx  # Native Visio stencil template
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configuration management (dotenv)
└── cli.py                          # Command-line interface
```

---

## 8. Core Implementation Code

### 8.1 Diagram Builder Class (`core/diagram_builder.py`)

```python
from aspose.diagram import Diagram, Page, Shape, SaveFileFormat
from typing import List, Dict, Optional
import logging

class SystemContextBuilder:
    """Main class for building system context diagrams (Level 0)."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._setup_positions()
    
    def _setup_page(self) -> None:
        """Configure page size and orientation."""
        layout_cfg = self.config.get("layout", {})
        orientation = layout_cfg.get("orientation", "landscape")
        page_size = layout_cfg.get("page_size", "A3")
        
        # Aspose works in inches internally by default
        if page_size == "A3":
            if orientation == "landscape":
                self.page.page_sheet.page_props.page_width.value = 16.53
                self.page.page_sheet.page_props.page_height.value = 11.69
            else:
                self.page.page_sheet.page_props.page_width.value = 11.69
                self.page.page_sheet.page_props.page_height.value = 16.53
    
    def _setup_styles(self) -> None:
        """Set up global styling defaults."""
        style_cfg = self.config.get("styling", {})
        self.theme = style_cfg.get("theme", "enterprise_blue")
        self.font_family = style_cfg.get("font_family", "Arial")
        self.font_size = style_cfg.get("font_size", 10)
        self.corner_radius = style_cfg.get("corner_radius", 8)
    
    def _setup_positions(self) -> None:
        """Calculate exact coordinate mapping for all elements."""
        from renderers.layout_engine import LayoutEngine
        self.layout_engine = LayoutEngine(
            self.page.page_sheet.page_props.page_width.value, 
            self.page.page_sheet.page_props.page_height.value
        )
        self.positions = self.layout_engine.calculate_positions(self.config)
    
    def build(self) -> None:
        """Execute the drawing pipeline."""
        sys_cfg = self.config["system"]
        self.add_title_block(
            self.config["title"], 
            sys_cfg["description"], 
            self.config["version"], 
            self.config["date"]
        )
        self.add_system_boundary()
        self.add_system_box(sys_cfg)
        self.add_external_entities(self.config["external_entities"])
        self.add_data_flows(self.config["external_entities"])
        self.add_legend()

    def add_title_block(self, title: str, subtitle: str, version: str, date: str) -> None:
        # Implementation via Aspose geometry logic
        pass

    def add_system_boundary(self) -> None:
        # Drawing a dashed rectangle wrapping the system logic
        pass
    
    def add_system_box(self, system: Dict) -> None:
        # Drawing the solid center system box
        pass
    
    def add_external_entities(self, entities: List[Dict]) -> None:
        # Draw external entities using spatial map
        pass
    
    def add_data_flows(self, entities: List[Dict]) -> None:
        # Route connectors with Arrow types
        pass
    
    def add_legend(self) -> None:
        pass
    
    def save(self, output_path: str) -> None:
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

### 8.2 Layout Engine (`renderers/layout_engine.py`)

```python
from typing import Dict, List

class LayoutEngine:
    """Calculates absolute (x, y, w, h) physical coordinates for all diagram elements."""
    
    def __init__(self, page_width: float, page_height: float):
        self.page_width = page_width
        self.page_height = page_height
        self.margin = 0.5  # inches
    
    def calculate_positions(self, spec: Dict) -> Dict:
        """Calculate bounds for the core system box and surrounding entities."""
        positions = {}
        
        # Absolute center alignment for System Box
        layout_cfg = spec.get("layout", {})
        system_width = layout_cfg.get("system_box_width", 8.0)
        system_height = layout_cfg.get("system_box_height", 6.0)
        system_x = (self.page_width - system_width) / 2
        system_y = (self.page_height - system_height) / 2
        
        positions["system"] = {
            "x": system_x,
            "y": system_y,
            "width": system_width,
            "height": system_height
        }
        
        entities = spec.get("external_entities", [])
        for entity in entities:
            positions[entity["id"]] = self._calculate_entity_position(entity, positions["system"])
        
        return positions
    
    def _calculate_entity_position(self, entity: Dict, sys_pos: Dict) -> Dict:
        """Determine X/Y coordinates based on compass-point directives."""
        pos = entity.get("position", "right")
        spacing = entity.get("spacing", 1.5)
        width = entity.get("width", 3.5)
        height = entity.get("height", 2.5)
        
        # Matrix grid placement
        if pos == "top-left":
            x = sys_pos["x"] - width - spacing
            y = sys_pos["y"] - height - spacing
        elif pos == "top":
            x = sys_pos["x"] + (sys_pos["width"] - width) / 2
            y = sys_pos["y"] - height - spacing
        elif pos == "top-right":
            x = sys_pos["x"] + sys_pos["width"] + spacing
            y = sys_pos["y"] - height - spacing
        elif pos == "left":
            x = sys_pos["x"] - width - spacing
            y = sys_pos["y"] + (sys_pos["height"] - height) / 2
        elif pos == "right":
            x = sys_pos["x"] + sys_pos["width"] + spacing
            y = sys_pos["y"] + (sys_pos["height"] - height) / 2
        elif pos == "bottom-left":
            x = sys_pos["x"] - width - spacing
            y = sys_pos["y"] + sys_pos["height"] + spacing
        elif pos == "bottom":
            x = sys_pos["x"] + (sys_pos["width"] - width) / 2
            y = sys_pos["y"] + sys_pos["height"] + spacing
        elif pos == "bottom-right":
            x = sys_pos["x"] + sys_pos["width"] + spacing
            y = sys_pos["y"] + sys_pos["height"] + spacing
        else:
            x = sys_pos["x"] + sys_pos["width"] + spacing
            y = sys_pos["y"] + (sys_pos["height"] - height) / 2
            
        return {"x": x, "y": y, "width": width, "height": height}
```

### 8.3 Shape Builder (`stylers/shape_styler.py`)

```python
class ShapeBuilder:
    """Wraps Aspose.Diagram primitive creation."""
    
    @staticmethod
    def create_entity_box(diagram, x: float, y: float, width: float, height: float,
                          fill_color: str, border_color: str, 
                          text: str) -> int:
        """Create a styled entity box and return its shape ID."""
        # shape_id = diagram.add_shape(x, y, width, height, "Rectangle", 0)
        # Apply hex colors, shadows, and text blocks...
        return 1
    
    @staticmethod
    def create_system_box(diagram, x: float, y: float, width: float, height: float,
                          fill_color: str, border_color: str,
                          text: str) -> int:
        """Create the central system box with a heavy border."""
        # Implementation
        return 2
    
    @staticmethod
    def create_data_flow(diagram, source_id: int, target_id: int,
                         color: str, label: str, bidirectional: bool) -> None:
        """Route dynamic connector with orthogonal rules and labeled midpoint."""
        # Configure ConLineRouteExt for orthogonal lines
        pass
```

---

## 9. Error Handling

Define comprehensive error codes to prevent silent failures during batch generation pipelines:

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| `SC-001` | InvalidInput | JSON fails strict Pydantic schema validation. | Validate against schema prior to execution. |
| `SC-002` | NoSystemDefined | The central `system` block is missing. | Provide system name and description. |
| `SC-003` | NoExternalEntities | Zero external entities specified. | A Level 0 Context diagram requires at least one interaction. |
| `SC-004` | InvalidPosition | Invalid compass string in payload. | Use strictly: `top-left`, `top`, `top-right`, `left`, `right`, `bottom-left`, `bottom`, `bottom-right`. |
| `SC-005` | MissingDataFlow | Entity lacks interactions. | Define at least one data flow per entity. |
| `SC-006` | InvalidDataType | Unknown data format tag. | Use standard tags: `JSON`, `XML`, `HL7`, `FHIR`, `CSV`, `PDF`, `EDI`. |
| `SC-007` | JavaNotInstalled | Missing Java dependency for JPype. | Install JRE 8+. |
| `SC-008` | LicenseMissing | Aspose `.lic` file missing. | Ensure `.env` is configured properly. |
| `SC-009` | LayoutError | Shapes overlap fatally. | Adjust grid padding and `entity_spacing` params. |
| `SC-010` | RenderError | Visio file write failed. | Verify directory permissions and disk space. |

---

## 10. Command-Line Interface (CLI)

```python
# cli.py
import argparse
import json
import sys
import logging
from core.diagram_builder import SystemContextBuilder

def main():
    parser = argparse.ArgumentParser(
        description="Generate a System Context Diagram (Level 0) in Visio format"
    )
    parser.add_argument("input", help="Path to input JSON/YAML specification file")
    parser.add_argument("-o", "--output", help="Output path (default: ./output/system_context.vsdx)")
    parser.add_argument("-p", "--preview", action="store_true", help="Generate PNG preview as well")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--validate-only", action="store_true", help="Only validate input, don't render")
    parser.add_argument("--theme", choices=["enterprise_blue", "dark_modern", "corporate_green", "material"], help="Color theme to use")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    with open(args.input, 'r') as f:
        spec = json.load(f)
    
    if args.validate_only:
        # Run Pydantic validations here
        logging.info("Validation successful. Exiting.")
        sys.exit(0)
        
    builder = SystemContextBuilder(spec["system_context"])
    builder.build()
    
    out_path = args.output or "./output/system_context.vsdx"
    builder.save(out_path)
    logging.info(f"Context Diagram saved to {out_path}")

if __name__ == "__main__":
    main()
```

---

## 11. Quality Checklist

Before finalizing the skill or delivering its output, strictly verify:

- [ ] System box is perfectly centered on the page.
- [ ] External entities never overlap and adhere to compass positioning rules.
- [ ] Data flow arrows never cross the system boundary text; they terminate at the boundary box.
- [ ] Arrow labels are centered, horizontally aligned when possible, and readable against the background.
- [ ] System boundary (dashed line) is drawn and labeled clearly.
- [ ] A Legend successfully enumerates the entity colors (User, System, Org, Regulatory).
- [ ] Title block includes Title, Project, Version, and Timestamp.
- [ ] The overall diagram scales cleanly to fit a single A3 sheet without distortion.
- [ ] Opening the file in native Microsoft Visio produces zero XML repair warnings.

---

## 12. Usage Examples

### 12.1 Basic Generation
```bash
python system_context_generator/cli.py input.json -o output/system_context.vsdx
```

### 12.2 Rasterized Previews (For Web/Markdown Embedding)
```bash
python system_context_generator/cli.py input.json -o output/system_context.vsdx --preview
```

### 12.3 Automated Pipeline Validation
```bash
python system_context_generator/cli.py input.json --validate-only
```

### 12.4 Theme Overrides
```bash
python system_context_generator/cli.py input.json -o output/context.vsdx --theme corporate_green
```

---

## 13. Integration with Existing Skills

This generator plays a critical role in the documentation ecosystem:
1.  **Project Charter Generator (`project-charter-generator-SKILL.md`):** This is the authoritative engine for generating the "Section 6. System Context" figure inside the Word document artifact.
2.  **Shared Layout Math:** It utilizes the same foundational positioning algebra found in `uml-diagram-generator-SKILL.md`. 
3.  **Cross-compatible Schema:** The external entity JSON format maps cleanly to the `external_system` nodes found in standard component diagrams.

---

## 14. Testing Strategy

Prevent architectural regressions by running these unit and functional tests:

1.  **Minimal Input Test:** System + exactly 1 Entity. Ensure drawing succeeds without grid-balancing errors.
2.  **Maximum Stress Test:** System + 8 distinct Entities across all compass points (`top-left` to `bottom-right`). Ensure zero overlapping bounding boxes.
3.  **Data Flow Typology Test:** Inject uni-directional and bi-directional JSON specs simultaneously. Assert correct rendering of single vs. double `ArrowType.Triangle` endpoints.
4.  **Exception Validation:** Delete the `system` block from the JSON. Assert the script strictly returns error `SC-002` rather than a generic KeyError.
5.  **Geometry Assertions:** Run Python unit tests against `LayoutEngine.calculate_positions()` to confirm the computed `system_x` is mathematically equal to `(page_width - system_width) / 2`.
