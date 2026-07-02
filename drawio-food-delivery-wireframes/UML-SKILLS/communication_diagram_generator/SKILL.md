---
name: communication-diagram-generator
description: Generate enterprise-grade UML Communication Diagrams (Collaboration Diagrams) as Visio (.vsdx) files using Aspose.Diagram for Python. Outputs follow mandatory design standards from uml-diagram-generator-SKILL.md §11 plus communication-specific styling (participant types, message numbering, system boundaries, legends). Suitable for executive presentations, architecture reviews, and technical documentation.
---

# Communication Diagram Generator Skill

## Context

A **Communication Diagram** (UML Collaboration Diagram) shows how objects, components, or systems interact to perform a behavior. Unlike Sequence Diagrams (time-ordered lifelines), Communication Diagrams emphasize **structural relationships** and **numbered messages** flowing between participants. Use for system architecture, API interactions, and multi-component workflows.

## Design Philosophy

Every output must be:

| Principle | Requirement |
|-----------|-------------|
| **Visually stunning** | Enterprise palette, clean layout, consistent branding |
| **Enterprise-ready** | C-suite presentations and architecture reviews |
| **Technically precise** | UML-compliant notation, correct stereotypes and message types |
| **Programmatic** | Fully automated — no manual Visio tweaking |

**Design system authority:** Inherits mandatory standards from [`uml-diagram-generator-SKILL.md`](../uml-diagram-generator-SKILL.md) §11 (page layout, typography, title block, legend, connector routing, QA). This skill adds UML participant types, message numbering, and system-boundary styling.

## Table of Contents

1. Primary Purpose & Output
2. Professional Design Standards
3. Communication Diagram Layout (ASCII Blueprint)
4. Environment Setup & Dependencies
5. Input Specification
6. UML Object Types, Links & Messages
7. Code Architecture
8. Core Implementation
9. Error Handling
10. Command-Line Interface
11. Quality Checklist
12. Usage Examples
13. Integration with Existing Skills
14. Testing Strategy
15. Troubleshooting Guide

---

## 1. Primary Purpose & Output

Generate a complete Communication Diagram as a **Visio `.vsdx`** file that includes:

1. Object/participant nodes with UML naming (`<<stereotype>>`, `Class:instance`, display name)
2. Structural links between participants (association, dependency, aggregation, composition)
3. Messages with hierarchical sequence numbers (`1`, `1.1`, `1.1.1`, `2`, …)
4. Message labels and types (synchronous, asynchronous, creation, return)
5. Color coding by participant type (Actor, Control, Entity, Boundary, Service)
6. System boundary groups enclosing related participants
7. Professional title block, legend, and optional footer
8. Fully editable in Microsoft Visio

**Rendering pipeline** (`core/diagram_builder.py`):

```text
Title block → System boundaries → Participants → Structural links → Messages → Legend
```

---

## 2. Professional Design Standards

### 2.1 Inherited Base Standards

Apply all settings from [`uml-diagram-generator-SKILL.md`](../uml-diagram-generator-SKILL.md) §11:

- Page: **A2 landscape** (59.4 × 42.0 in), margin **0.5 cm**
- Font: **Arial** (10pt participant names, 8pt stereotypes, 9pt sequence numbers)
- Title block: `#1a237e` background, white text
- Connectors: orthogonal routing preferred; label white backing when on lines
- QA: minimum `.vsdx` size ≥ 4 KB; validate participant/message references

### 2.2 Communication Diagram Styling Configuration

```yaml
communication_diagram_styling:
  page:
    size: "A2"
    orientation: "landscape"
    margin: 0.5
    background_color: "#FFFFFF"

  participants:
    actor:
      fill_color: "#4CAF50"
      stroke_color: "#2E7D32"
      text_color: "#FFFFFF"
      width: 2.5
      height: 1.2
      corner_radius: 8
    control:
      fill_color: "#1565C0"
      stroke_color: "#0D47A1"
      text_color: "#FFFFFF"
      width: 3.0
      height: 1.4
      corner_radius: 8
    entity:
      fill_color: "#2E7D32"
      stroke_color: "#1B5E20"
      text_color: "#FFFFFF"
      width: 3.0
      height: 1.4
      corner_radius: 8
    boundary:
      fill_color: "#FF9800"
      stroke_color: "#E65100"
      text_color: "#FFFFFF"
      width: 3.0
      height: 1.4
      corner_radius: 8
    service:
      fill_color: "#6A1B9A"
      stroke_color: "#4A148C"
      text_color: "#FFFFFF"

  links:
    association:  { line_style: solid,  color: "#666666", width: 1.0, end_arrow: none }
    dependency:   { line_style: dashed, color: "#666666", width: 1.0, end_arrow: open }
    aggregation:  { line_style: solid,  color: "#666666", width: 1.0, end_arrow: diamond_hollow }
    composition:  { line_style: solid,  color: "#666666", width: 1.0, end_arrow: diamond_filled }

  messages:
    synchronous:  { color: "#1a237e", line_style: solid,  arrow: filled }
    asynchronous: { color: "#6A1B9A", line_style: dashed, arrow: filled }
    creation:     { color: "#E65100", line_style: dotted, arrow: filled }
    return:       { color: "#2E7D32", line_style: dashed, arrow: open }

  sequence_numbers:
    font_size: 9
    font_weight: bold
    color: "#1a237e"
    background: "#FFFFFF"
    format: "{number}"   # 1, 1.1, 1.1.1

  system_boundary:
    line_style: dashed
    color: "#1565C0"
    width: 2.0
    fill_color: "#E3F2FD"
    label: { font_size: 12, weight: bold, color: "#1565C0" }

  title_block:
    height: 1.2
    background: "#1a237e"
    text_color: "#FFFFFF"
    font: "Arial"

  legend:
    enabled: true
    position: "bottom"
    background: "#F5F5F5"
    border: { color: "#BDBDBD", width: 0.5 }

  footer:
    enabled: true
    confidentiality: "CONFIDENTIAL - Internal Use Only"
    page_number: "Page {page} of {total}"
```

Default theme `enterprise_blue` is defined in `stylers/color_themes.py` and matches the above.

### 2.3 Anti-Patterns (Do NOT)

- Comic Sans or decorative fonts
- Unlabeled participant colors
- Duplicate sequence numbers
- Messages without source/target participant IDs
- Lines cutting through participant boxes without routing
- Missing legend on multi-type diagrams
- Accepting sub-4KB `.vsdx` as success
- Using `aspose.diagram` import (use `asposediagram.api` via JPype)

---

## 3. Communication Diagram Layout (ASCII Blueprint)

**CRITICAL:** This blueprint defines the exact layout. Implementers must follow panel positions and legend content.

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    COMMUNICATION DIAGRAM                                                                     │
│              Healthcare Ecosystem - Patient Consultation Flow  │  Version 1.0  │  2026-06-17                                  │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                              │
│                          ┌─────────────────────────────────────────────────────────────────────────────────────────────┐     │
│                          │  SYSTEM BOUNDARY — Healthcare System  (dashed #1565C0, fill #E3F2FD)                          │     │
│                          │                                                                                               │     │
│                          │     ┌─────────────────────┐                                                                       │     │
│                          │     │  Doctor             │  <<actor>>  #4CAF50                                               │     │
│                          │     │  (Physician)        │                                                                       │     │
│                          │     └──────────┬──────────┘                                                                       │     │
│                          │                │  5: Schedule Consultation (1.1.1)                                               │     │
│                          │                │                                                                                   │     │
│     ┌────────────────────┼────────────────┼───────────────────────────────────────────────────────────────────────────┐   │     │
│     │  Patient Portal    │                │                                                           │               │   │     │
│     │  <<actor>> #4CAF50 │  1: Book Appt  │                                                           │               │   │     │
│     └─────────┬──────────┘                │                                                           │               │   │     │
│               │                           ▼                                                           │               │   │     │
│               │              ┌────────────────────────────┐                                         │               │   │     │
│               │              │  Appointment System        │  <<control>> #1565C0                    │               │   │     │
│               │              │  (Scheduler)               │                                         │               │   │     │
│               │              └─────────────┬──────────────┘                                         │               │   │     │
│               │                            │  2: Check Availability (1.1)                          │               │   │     │
│               │                            ▼                                                         │               │   │     │
│               │              ┌────────────────────────────┐                                           │               │   │     │
│               │              │  Availability Service      │  <<entity>> #2E7D32                      │               │   │     │
│               │              │  (Calendar)                │                                           │               │   │     │
│               │              │  3: Return Slots (1.1.2)   │                                           │               │   │     │
│               │              └────────────────────────────┘                                           │               │   │     │
│               │                            │  4.1: Add to Calendar (1.2)                              │               │   │     │
│               │                            ▼                                                         │               │   │     │
│               │              ┌────────────────────────────┐                                           │               │   │     │
│               │              │  Medical Record System     │  <<entity>> #2E7D32                      │               │   │     │
│               │              │  (EMR)                     │                                           │               │   │     │
│               │              │  6: Record Consultation    │                                           │               │   │     │
│               │              └────────────────────────────┘                                           │               │   │     │
│               └─────────────────────────────────────────────────────────────────────────────────────────┘               │   │     │
│                          └─────────────────────────────────────────────────────────────────────────────────────────────┘     │
│                                                                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  LEGEND                                                                                                                 │  │
│  │  Object Types:  ■ Actor  ■ Control  ■ Entity  ■ Boundary  ■ Service                                                    │  │
│  │  Links:  ─── Association   ─ ─ ─ Dependency   ◇─ Aggregation   ■─ Composition                                          │  │
│  │  Messages:  → Synchronous (#1a237e)   ◇ Asynchronous (#6A1B9A)   ▶ Creation (#E65100)   ← Return (#2E7D32)          │  │
│  │  Numbering:  1 = top-level   1.1 = nested   1.1.1 = deeply nested                                                    │  │
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│  Footer: Page 1 of 1  │  CONFIDENTIAL - Internal Use Only  │  Healthcare Ecosystem                                          │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Layout regions:**

| Region | Position | Styling |
|--------|----------|---------|
| Title block | Top | `#1a237e`, Arial bold 14pt |
| System boundary | Behind participants | Dashed `#1565C0`, fill `#E3F2FD` |
| Participants | User-defined `x`,`y` or auto-layout | Type colors from Section 2.2 |
| Structural links | Between participants | Grey `#666666`, no arrowheads |
| Messages | On links | Number + label, type-colored arrows |
| Legend | Bottom | All symbols used in diagram |

---

## 4. Environment Setup & Dependencies

### 4.1 Python Requirements
```text
python >= 3.10
aspose-diagram>=23.10.0
JPype1>=1.5.0
pydantic>=2.0.0
python-dotenv>=1.0.0
pyyaml>=6.0
```

### 4.2 System Dependencies
```text
Java Runtime Environment (JRE) 8 or higher
  - Required for Aspose.Diagram for Python
  - Installation guide:
    - Ubuntu: sudo apt-get install default-jre
    - macOS: brew install openjdk
    - Windows: Download from https://www.java.com/download/

Graphviz (optional, for preview generation)
  - For generating PNG/SVG previews
  - Installation:
    - Ubuntu: sudo apt-get install graphviz
    - macOS: brew install graphviz
    - Windows: Download from https://graphviz.org/download/
```

### 4.3 Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate on Unix/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Install dependencies
pip install aspose-diagram JPype1 pydantic python-dotenv pyyaml
```

### 4.4 Environment Variables (.env file)
```env
# Aspose.Diagram License (if commercial)
ASPOSE_DIAGRAM_LICENSE_PATH=/path/to/license.lic

# Output directory
OUTPUT_DIR=./output

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Default styling
DEFAULT_COLOR_THEME=enterprise_blue
DEFAULT_FONT_FAMILY=Arial
DEFAULT_FONT_SIZE=9
```

## 5. Input Specification

The skill accepts the following input structure (JSON/YAML):

```json
{
  "communication_diagram": {
    "title": "Communication Diagram - Patient Consultation",
    "system_name": "Healthcare Ecosystem",
    "version": "1.0",
    "date": "2026-06-17",
    "description": "Patient consultation booking and management flow",
    
    "participants": [
      {
        "id": "P1",
        "name": "Patient",
        "class_name": "Patient",
        "instance_name": "patient",
        "type": "actor",
        "color": "#4CAF50",
        "text_color": "#FFFFFF",
        "x": 8.0,
        "y": 15.0,
        "width": 2.5,
        "height": 1.2,
        "stereotype": "<<actor>>"
      },
      {
        "id": "P2",
        "name": "Appointment System",
        "class_name": "AppointmentSystem",
        "instance_name": "scheduler",
        "type": "control",
        "color": "#1565C0",
        "text_color": "#FFFFFF",
        "x": 15.0,
        "y": 10.0,
        "width": 3.0,
        "height": 1.4,
        "stereotype": "<<control>>"
      },
      {
        "id": "P3",
        "name": "Availability Service",
        "class_name": "AvailabilityService",
        "instance_name": "calendar",
        "type": "entity",
        "color": "#2E7D32",
        "text_color": "#FFFFFF",
        "x": 22.0,
        "y": 15.0,
        "width": 3.0,
        "height": 1.4,
        "stereotype": "<<entity>>"
      },
      {
        "id": "P4",
        "name": "Doctor",
        "class_name": "Doctor",
        "instance_name": "physician",
        "type": "actor",
        "color": "#4CAF50",
        "text_color": "#FFFFFF",
        "x": 28.0,
        "y": 10.0,
        "width": 2.5,
        "height": 1.2,
        "stereotype": "<<actor>>"
      },
      {
        "id": "P5",
        "name": "Medical Record System",
        "class_name": "MedicalRecordSystem",
        "instance_name": "emr",
        "type": "entity",
        "color": "#2E7D32",
        "text_color": "#FFFFFF",
        "x": 22.0,
        "y": 25.0,
        "width": 3.0,
        "height": 1.4,
        "stereotype": "<<entity>>"
      }
    ],
    
    "links": [
      {
        "id": "L1",
        "source": "P1",
        "target": "P2",
        "type": "association",
        "label": "",
        "line_style": "solid"
      },
      {
        "id": "L2",
        "source": "P2",
        "target": "P3",
        "type": "association",
        "label": "",
        "line_style": "solid"
      },
      {
        "id": "L3",
        "source": "P2",
        "target": "P4",
        "type": "association",
        "label": "",
        "line_style": "solid"
      },
      {
        "id": "L4",
        "source": "P2",
        "target": "P5",
        "type": "association",
        "label": "",
        "line_style": "solid"
      },
      {
        "id": "L5",
        "source": "P4",
        "target": "P5",
        "type": "dependency",
        "label": "",
        "line_style": "dashed"
      }
    ],
    
    "messages": [
      {
        "id": "M1",
        "source": "P1",
        "target": "P2",
        "sequence": "1",
        "label": "Book Appointment",
        "type": "synchronous",
        "return_value": "confirmation",
        "guard": null
      },
      {
        "id": "M2",
        "source": "P2",
        "target": "P3",
        "sequence": "1.1",
        "label": "Check Availability",
        "type": "synchronous",
        "return_value": "slots",
        "guard": null
      },
      {
        "id": "M3",
        "source": "P3",
        "target": "P2",
        "sequence": "1.1.1",
        "label": "Return Available Slots",
        "type": "synchronous",
        "return_value": "List<Slot>",
        "guard": null
      },
      {
        "id": "M4",
        "source": "P2",
        "target": "P1",
        "sequence": "1.2",
        "label": "Show Available Slots",
        "type": "synchronous",
        "return_value": null,
        "guard": null
      },
      {
        "id": "M5",
        "source": "P1",
        "target": "P2",
        "sequence": "1.3",
        "label": "Select Slot and Book",
        "type": "synchronous",
        "return_value": "Booking",
        "guard": null
      },
      {
        "id": "M6",
        "source": "P2",
        "target": "P4",
        "sequence": "1.4",
        "label": "Schedule Consultation",
        "type": "synchronous",
        "return_value": null,
        "guard": null
      },
      {
        "id": "M7",
        "source": "P2",
        "target": "P5",
        "sequence": "1.5",
        "label": "Record Booking",
        "type": "synchronous",
        "return_value": null,
        "guard": null
      },
      {
        "id": "M8",
        "source": "P4",
        "target": "P5",
        "sequence": "2",
        "label": "Record Consultation",
        "type": "synchronous",
        "return_value": null,
        "guard": "consultation_complete"
      }
    ],
    
    "groups": [
      {
        "id": "G1",
        "name": "System Boundary",
        "color": "#E3F2FD",
        "border_color": "#1565C0",
        "participants": ["P2", "P3", "P4", "P5"],
        "label": "Healthcare System"
      }
    ],
    
    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "participant_types": {
        "actor": {
          "color": "#4CAF50",
          "text_color": "#FFFFFF",
          "shape": "rectangle",
          "corner_radius": 6
        },
        "control": {
          "color": "#1565C0",
          "text_color": "#FFFFFF",
          "shape": "rectangle",
          "corner_radius": 6
        },
        "entity": {
          "color": "#2E7D32",
          "text_color": "#FFFFFF",
          "shape": "rectangle",
          "corner_radius": 6
        },
        "boundary": {
          "color": "#FF9800",
          "text_color": "#FFFFFF",
          "shape": "rectangle",
          "corner_radius": 6
        }
      },
      "message_colors": {
        "synchronous": "#1a237e",
        "asynchronous": "#6A1B9A",
        "creation": "#E65100",
        "return": "#2E7D32"
      },
      "shadow_enabled": true,
      "link_width": 1
    },
    
    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "participant_spacing": 3.0,
      "message_spacing": 0.5,
      "auto_layout": false
    }
  }
}
```

## 6. UML Object Types, Links & Messages

### 6.1 Participant Types

| Type | UML Stereotype | Color | Shape | Description |
|------|----------------|-------|-------|-------------|
| Actor | `<<actor>>` | #4CAF50 (Green) | Rounded Rectangle | User/External entity |
| Control | `<<control>>` | #1565C0 (Blue) | Rounded Rectangle | Orchestrator/Manager |
| Entity | `<<entity>>` | #2E7D32 (Green) | Rounded Rectangle | Data/Storage |
| Boundary | `<<boundary>>` | #FF9800 (Orange) | Rounded Rectangle | Interface/API |
| Service | `<<service>>` | #6A1B9A (Purple) | Rounded Rectangle | Service/API |

### 6.2 Message Types and Numbering

| Type | Symbol | Color | Arrow Style | Description |
|------|--------|-------|-------------|-------------|
| Synchronous | → | #1a237e | Solid with arrow | Caller waits for response |
| Asynchronous | ◇ | #6A1B9A | Dashed with arrow | Caller continues immediately |
| Creation | ▶ | #E65100 | Dotted with arrow | Creates new object |
| Return | ← | #2E7D32 | Dashed arrow | Returns value to caller |

### Message Numbering System

| Pattern | Example | Description |
|---------|---------|-------------|
| Top-level | 1, 2, 3 | First-level messages |
| Nested | 1.1, 1.2, 2.1 | Messages within a message |
| Deeply nested | 1.1.1, 1.1.2, 2.1.1 | Third-level messages |
| Conditional | 1.1a, 1.1b | Alternative paths |

### 6.3 Participant Text Layout

```text
┌────────────────────────────────┐
│  <<stereotype>>                │
│  ClassName:instanceName        │
│                                │
│  [Participant Name]            │
└────────────────────────────────┘
```

### 6.4 Link Styling

| Property | Value | Description |
|----------|-------|-------------|
| Color | #666666 | Grey |
| Width | 1pt | Standard |
| Style | Solid or Dashed | Based on type |

## 7. Code Architecture

Structure the skill as:

```text
communication_diagram_generator/
├── __init__.py
├── SKILL.md
├── PROMPT.md
├── core/
│   ├── comm_builder.py            # Orchestrator: validate + build + size check
│   ├── diagram_builder.py         # Aspose rendering pipeline
│   ├── validator.py
│   ├── errors.py
│   └── models.py
├── renderers/
│   ├── aspose_renderer.py         # JVM-backed asposediagram.api helpers
│   └── layout_engine.py
├── calculators/
│   ├── sequence_calculator.py
│   └── position_calculator.py
├── stylers/
│   ├── color_themes.py            # enterprise_blue theme (Section 2.2)
│   ├── participant_styler.py
│   └── message_styler.py
├── config/
│   └── settings.py                # PAGE_SIZES_IN, license
├── scripts/
│   └── run_example.py
└── cli.py
```

## 8. Core Implementation

### 8.1 Orchestrator (`core/comm_builder.py`)

```python
from core.comm_builder import build_communication_diagram

build_communication_diagram(spec_dict, "output/communication_diagram.vsdx")
# Validates input, applies Aspose license, builds diagram, enforces MIN_VSDX_BYTES >= 4000
```

### 8.2 Sequence Number Generator (`calculators/sequence_calculator.py`)

```python
class SequenceNumberGenerator:
    """Generates and manages message sequence numbers."""
    
    def __init__(self):
        self.sequence_stack = []
        self.message_counters = {}
    
    def start_new_sequence(self) -> str:
        """Start a new top-level sequence."""
        self.sequence_stack = []
        return self._generate_number()
    
    def _generate_number(self) -> str:
        """Generate the next sequence number."""
        if not self.sequence_stack:
            # Start with 1
            self.sequence_stack.append(1)
            self.message_counters[str(1)] = 0
        else:
            # Increment the last level
            last_level = self.sequence_stack[-1]
            new_value = last_level + 1
            self.sequence_stack[-1] = new_value
            self.message_counters[str(new_value)] = 0
        
        return '.'.join(map(str, self.sequence_stack))
    
    def add_nested_message(self, parent_sequence: str) -> str:
        """Add a nested message under a parent sequence."""
        # Parse parent sequence
        parts = [int(p) for p in parent_sequence.split('.')]
        self.sequence_stack = parts
        
        # Add a new level
        if len(self.sequence_stack) >= 1:
            # Add 1 at the next level
            self.sequence_stack.append(1)
        
        return '.'.join(map(str, self.sequence_stack))
    
    def reset(self) -> None:
        """Reset the sequence generator."""
        self.sequence_stack = []
        self.message_counters = {}
```

### 8.3 Diagram Builder (`core/diagram_builder.py`)

Uses **JVM-backed** `asposediagram.api` via `renderers/aspose_renderer.py`:

```python
from renderers import aspose_renderer as asp
from stylers.color_themes import get_theme, participant_fill
from config.settings import PAGE_SIZES_IN, apply_aspose_diagram_license

class CommunicationDiagramBuilder:
    """Enterprise communication diagram — see Section 3 ASCII blueprint."""

    def __init__(self, spec: dict):
        self.config = spec["communication_diagram"]
        self.theme = get_theme(self.config.get("styling", {}).get("theme", "enterprise_blue"))
        self.positions = PositionCalculator(...).calculate(self.config["participants"])

    def build(self, include_legend: bool = True) -> None:
        apply_aspose_diagram_license()
        self.diagram = asp.new_diagram()
        self.page = self.diagram.getPages().get(0)
        self._setup_page()          # A2 landscape from PAGE_SIZES_IN
        self.add_title_block()      # #1a237e bar
        self.add_groups()           # System boundaries behind participants
        self.add_participants()     # Type-colored rounded rectangles
        self.add_links()            # Structural links, no arrowheads
        self.add_messages()         # Numbered connectors with labels
        if include_legend:
            self.add_legend()

    def save(self, output_path: str) -> None:
        asp.save_diagram(self.diagram, output_path)
```

**Participant rendering** — `asp.add_rectangle()` with coordinates in inches, centered on `(x, y)`:

```python
asp.add_rectangle(
    page, x=pos["x"], y=pos["y"], w=pos["w"], h=pos["h"],
    text=build_participant_label(participant),
    fill_color=participant_fill(self.theme, participant["type"], participant.get("color")),
    text_color=participant_text_color(self.theme, participant["type"]),
    border_color=stroke_for_type(participant["type"]),
    font_family="Arial", font_size=9.0, font_bold=True,
)
```

**Message connectors** — edge-to-edge routing via `_edge_points()`, orthogonal `draw_line` segments, label at midpoint with white backing.

## 9. Error Handling

Define comprehensive error codes to handle diagram generation anomalies:

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| CD-001 | InvalidInput | Input JSON missing required fields | Validate against schema |
| CD-002 | NoParticipants | No participants defined | Add at least one participant |
| CD-003 | NoMessages | No messages defined | Add at least one message |
| CD-004 | InvalidParticipantRef | Message references non-existent participant | Check participant IDs |
| CD-005 | DuplicateSequence | Duplicate sequence number | Use unique sequences |
| CD-006 | InvalidSequenceFormat | Invalid sequence number format | Use format like 1, 1.1, 1.1.1 |
| CD-007 | CircularDependency | Circular message dependency | Check message flow |
| CD-008 | JavaNotInstalled | Java runtime not found | Install JRE 8+ |
| CD-009 | LicenseMissing | Aspose license missing | Configure license or use trial |
| CD-010 | RenderError | Rendering failed | Check Aspose.Diagram installation |

### Error Models

```python
class DiagramError(Exception):
    """Base class for all diagram exceptions."""
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")

class InvalidInputError(DiagramError):
    def __init__(self, message: str = "Input JSON missing required fields"):
        super().__init__("CD-001", message)

class InvalidParticipantRefError(DiagramError):
    def __init__(self, message: str = "Message references non-existent participant"):
        super().__init__("CD-004", message)
```

## 10. Command-Line Interface

`cli.py`

```python
import argparse
import json
import sys
from pathlib import Path
from core.comm_builder import build_communication_diagram

def main():
    parser = argparse.ArgumentParser(
        description="Generate a Communication Diagram in Visio format"
    )
    parser.add_argument(
        "input", 
        help="Path to input JSON/YAML specification file"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Output path (default: ./output/communication_diagram.vsdx)",
        default="./output/communication_diagram.vsdx"
    )
    parser.add_argument(
        "-p", "--preview", 
        action="store_true",
        help="Generate PNG preview as well"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--no-legend", 
        action="store_true",
        help="Skip legend generation"
    )
    parser.add_argument(
        "--validate-only", 
        action="store_true",
        help="Only validate input, don't render"
    )
    
    args = parser.parse_args()
    
    # Load input
    try:
        with open(args.input, 'r') as f:
            if args.input.endswith('.yaml') or args.input.endswith('.yml'):
                import yaml
                spec = yaml.safe_load(f)
            else:
                spec = json.load(f)
    except Exception as e:
        print(f"Error loading input file: {e}")
        sys.exit(1)
        
    if args.validate_only:
        print("Validation successful!")
        sys.exit(0)
    
    # Build diagram
    # Ensure output directory exists
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    build_communication_diagram(spec, args.output)
    print(f"Diagram successfully saved to {args.output}")

if __name__ == "__main__":
    main()
```

## 11. Quality Checklist

Run before delivering any communication diagram.

### Visual

- [ ] Enterprise color palette (Section 2.2) applied consistently
- [ ] Arial font throughout; no decorative fonts
- [ ] Title block present (`#1a237e`, white text)
- [ ] Clean white background; subtle borders only
- [ ] No text overflow in participant boxes
- [ ] Legend includes all object types, link styles, and message types used

### UML compliance

- [ ] Participants use correct stereotypes (`<<actor>>`, `<<control>>`, etc.)
- [ ] Class:instance format where applicable
- [ ] Links typed correctly (association, dependency, aggregation, composition)
- [ ] Message sequence numbers unique and properly nested (`1`, `1.1`, `1.1.1`)
- [ ] Message types styled per Section 2.2 (sync, async, creation, return)
- [ ] All messages reference valid participant IDs

### Layout

- [ ] Participants positioned for readability (no overlapping boxes)
- [ ] System boundary encloses correct participants
- [ ] Message labels readable with white backing on connectors
- [ ] Diagram fits A2 landscape without clipping

### Output integrity

- [ ] `.vsdx` ≥ 4 KB
- [ ] Opens in Microsoft Visio without repair warnings
- [ ] Sequence order matches business flow when sorted numerically

## 12. Usage Examples

### Basic Usage
```bash
python communication_diagram_generator/cli.py input.json -o output/communication_diagram.vsdx
```

### With Preview
```bash
python communication_diagram_generator/cli.py input.json -o output/communication_diagram.vsdx --preview
```

### Skip Legend
```bash
python communication_diagram_generator/cli.py input.json -o output/communication_diagram.vsdx --no-legend
```

### Validate Only
```bash
python communication_diagram_generator/cli.py input.json --validate-only
```

## 13. Integration with Existing Skills

1. **Parent skill**: Component of [`uml-diagram-generator-SKILL.md`](../uml-diagram-generator-SKILL.md); inherits §11 design standards.
2. **Sequence diagrams**: Structural counterpart to sequence-diagram skills — same JSON participants/messages, different layout.
3. **Project charter**: Embed `.vsdx` in charter Visio deck or reference from Word deliverable.
4. **Office integration**: Standard VSDX for Word/PowerPoint embedding without fidelity loss.

## 14. Testing Strategy

Thoroughly test changes against these scenarios:
1. **Minimal Input**: A simple 2-participant, 1-message topology to verify core rendering.
2. **Full Complex Input**: Multiple grouped boundaries, nested messages up to 4 levels deep (e.g., 1.1.1.1), and return values.
3. **Validation Errors**: Pass invalid sequences to ensure `InvalidSequenceFormat` or duplicate checkers throw gracefully.
4. **Constraint Test**: Large scale graph with 20+ participants to ensure auto-layout algorithms or fixed dimension handling don't result in infinite loops.

## 15. Troubleshooting Guide

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `.vsdx` < 4 KB | JVM/Aspose failure | Install JRE 11+; set `ASPOSE_DIAGRAM_LICENSE_PATH` |
| `CD-008` JavaNotInstalled | No JRE | `brew install openjdk` or `apt install default-jre` |
| `CD-004` InvalidParticipantRef | Bad message source/target ID | Match IDs to `participants[].id` |
| `CD-005` DuplicateSequence | Repeated sequence numbers | Use unique `1`, `1.1`, `2`, … values |
| Shapes overlapping | Manual `x`,`y` too close | Increase spacing or set `auto_layout: true` |
| Wrong import `aspose.diagram` | Incorrect package | Use `asposediagram.api` via JPype (Section 8.3) |
| Aspose watermark | No license | Configure `ASPOSE_DIAGRAM_LICENSE_PATH` in `.env` |
| Messages cross through boxes | No orthogonal routing | Adjust positions; use `_edge_points()` edge routing |

**Validation-only:**

```bash
python communication_diagram_generator/cli.py examples/sample_input.json --validate-only -v
```

**End-to-end test:**

```bash
cd communication_diagram_generator
../project_charter_generator/.venv/bin/python scripts/run_example.py
```
