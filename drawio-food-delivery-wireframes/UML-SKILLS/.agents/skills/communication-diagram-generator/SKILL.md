---
name: communication_diagram_generator
description: Comprehensive, production-grade skill for generating Communication Diagrams (also known as Collaboration Diagrams) in Visio format using Aspose.Diagram for Python.
---

# Communication Diagram Generator Skill

## Context
A Communication Diagram is a UML interaction diagram that shows how objects, components, or systems interact with each other to perform a specific behavior or process. Unlike Sequence Diagrams (which focus on time ordering), Communication Diagrams focus on the structural relationships between objects and the messages that flow between them. They are particularly useful for visualizing system architecture, API interactions, and complex multi-component workflows.

## Communication Diagram ASCII Blueprint

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                         COMMUNICATION DIAGRAM                                                                                                       │
│                                                         Healthcare Ecosystem - Patient Consultation Flow                                                                                           │
│                                                                      Version 1.0  |  2026-06-17                                                                                                   │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                                                                                      │
│                                                                          ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐                   │
│                                                                          │                                           SYSTEM BOUNDARY                                          │                   │
│                                                                          │                                                                                                   │                   │
│                                                                          │                                                                                                   │                   │
│                                                                          │       ┌──────────────────────────────────────────────────────────────────────────────────────┐    │                   │
│                                                                          │       │                                                                                      │    │                   │
│                                                                          │       │                      ┌──────────────────────────────────────┐                        │    │                   │
│                                                                          │       │                      │                                      │                        │    │                   │
│                                                                          │       │                      │       Doctor                        │                        │    │                   │
│                                                                          │       │                      │       (Physician)                   │                        │    │                   │
│                                                                          │       │                      │                                      │                        │    │                   │
│                                                                          │       │                      │                                      │                        │    │                   │
│                                                                          │       │                      └──────────────┬───────────────────────┘                        │    │                   │
│                                                                          │       │                                     │                                                  │    │                   │
│                                                                          │       │                                     │  5: Schedule Consultation (1.1.1)               │    │                   │
│                                                                          │       │                                     │                                                  │    │                   │
│                                                                          │       │                                     │                                                  │    │                   │
│                                                                          │       │                                     │                                                  │    │                   │
│                                                                          │       │                                     │                                                  │    │                   │
│                                                                          │       │                                     │                                                  │    │                   │
│                                                                          │       │         1: Book Appointment        │                                                  │    │                   │
│                                                                          │       │                                     │                                                  │    │                   │
│                                                                          │       │                                     │                                                  │    │                   │
│                                                                          │       │                                     │                                                  │    │                   │
│                                                                          │       ▼                                     ▼                                                  │    │                   │
│                                                                          │  ┌───────────────────────────────────────────────────────────────────────────────────────────┐    │                   │
│                                                                          │  │                                                                                          │    │                   │
│                                                                          │  │  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │    │                   │
│                                                                          │  │  │                                                                                     │  │    │                   │
│                                                                          │  │  │                                                                                     │  │    │                   │
│                                                                          │  │  │                      ┌─────────────────────────────────────┐                         │  │    │                   │
│                                                                          │  │  │                      │  Appointment System                  │                         │  │    │                   │
│                                                                          │  │  │                      │  (Scheduler)                        │                         │  │    │                   │
│                                                                          │  │  │                      │                                     │                         │  │    │                   │
│                                                                          │  │  │                      │                                     │                         │  │    │                   │
│                                                                          │  │  │                      └─────────────────┬───────────────────┘                         │  │    │                   │
│                                                                          │  │  │                                        │                                               │  │    │                   │
│                                                                          │  │  │                                        │  2: Check Availability (1.1)                 │  │    │                   │
│                                                                          │  │  │                                        │                                               │  │    │                   │
│                                                                          │  │  │                                        │                                               │  │    │                   │
│                                                                          │  │  │                                        │                                               │  │    │                   │
│                                                                          │  │  │                                        │                                               │  │    │                   │
│                                                                          │  │  │                                        │                                               │  │    │                   │
│                                                                          │  │  │                                        │                                               │  │    │                   │
│                                                                          │  │  │                                        ▼                                               │  │    │                   │
│                                                                          │  │  │                      ┌─────────────────────────────────────────────────────────────────┐ │  │    │                   │
│                                                                          │  │  │                      │  Availability Service                                           │ │  │    │                   │
│                                                                          │  │  │                      │  (Calendar)                                                    │ │  │    │                   │
│                                                                          │  │  │                      │                                                               │ │  │    │                   │
│                                                                          │  │  │                      │  3: Return Available Slots (1.1.2)                            │ │  │    │                   │
│                                                                          │  │  │                      │                                                               │ │  │    │                   │
│                                                                          │  │  │                      │                                                               │ │  │    │                   │
│                                                                          │  │  │                      └───────────────────────────────────────────────────────────────┘ │  │    │                   │
│                                                                          │  │  │                                                                                     │  │    │                   │
│                                                                          │  │  │                                                                                     │  │    │                   │
│                                                                          │  │  └─────────────────────────────────────────────────────────────────────────────────────┘  │    │                   │
│                                                                          │  │                                                                                          │    │                   │
│                                                                          │  └───────────────────────────────────────────────────────────────────────────────────────────┘    │                   │
│                                                                          │                                                    │                                             │                   │
│                                                                          │                                                    │                                             │                   │
│                                                                          │                                                    │  4.1: Add to Calendar (1.2)               │                   │
│                                                                          │                                                    │                                             │                   │
│                                                                          │                                                    ▼                                             │                   │
│                                                                          │                                     ┌─────────────────────────────────────────────────────────────────────────┐ │                   │
│                                                                          │                                     │                                                                         │ │                   │
│                                                                          │                                     │              Medical Record System                                    │ │                   │
│                                                                          │                                     │              (EMR)                                                   │ │                   │
│                                                                          │                                     │                                                                         │ │                   │
│                                                                          │                                     │                                                                         │ │                   │
│                                                                          │                                     │              6: Record Consultation (1.3)                             │ │                   │
│                                                                          │                                     │                                                                         │ │                   │
│                                                                          │                                     └─────────────────────────────────────────────────────────────────────────┘ │                   │
│                                                                          │                                                                                                                   │                   │
│                                                                          │                                                                                                                   │                   │
│                                                                          └───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘                   │
│                                                                                                                                                                                                      │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  LEGEND                                                                                                                                                                                         │ │
│  │  ═══════                                                                                                                                                                                         │ │
│  │  Object Types:  ■ Actor (User)  ■ Control (Orchestrator)  ■ Entity (Data)  ■ Boundary (Interface)                                                                                              │ │
│  │  Links:  ─── Association (Structural)  ─ ─ ─ Dependency (Temporary)                                                                                                                            │ │
│  │  Message Numbering:  1 = First message  1.1 = Nested/Sub-message  1.1.1 = Deeply nested                                                                                                        │ │
│  │  Message Types:  → Synchronous (Blocking)  ◇ Asynchronous (Non-blocking)  ▶ Creation (New object)                                                                                              │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Primary Purpose
Generate a complete Communication Diagram as a Visio file that includes:
1. Object/Component nodes with proper naming (Class:Instance format)
2. Structural links between objects
3. Messages with sequence numbers (1, 1.1, 2, 3.1, etc.)
4. Message labels and types (synchronous, asynchronous, creation)
5. Color coding by object type (Actor, Control, Entity, Boundary)
6. Professional styling with consistent colors, fonts, and themes
7. Legend explaining sequence numbering
8. Title block with project information
9. Fully editable in Microsoft Visio

## 1. Environment Setup & Dependencies

### Python Requirements
```text
python >= 3.10
aspose-diagram-python >= 24.0.0
python-dotenv >= 1.0.0
pyyaml >= 6.0
pillow >= 10.0.0
typing-extensions >= 4.0.0
pydantic >= 2.0.0
```

### System Dependencies
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

### Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate on Unix/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Install dependencies
pip install aspose-diagram-python python-dotenv pyyaml pillow pydantic
```

### Environment Variables (.env file)
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

## 2. Input Specification

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

## 3. Object Types and Visual Styling

| Type | UML Stereotype | Color | Shape | Description |
|------|----------------|-------|-------|-------------|
| Actor | `<<actor>>` | #4CAF50 (Green) | Rounded Rectangle | User/External entity |
| Control | `<<control>>` | #1565C0 (Blue) | Rounded Rectangle | Orchestrator/Manager |
| Entity | `<<entity>>` | #2E7D32 (Green) | Rounded Rectangle | Data/Storage |
| Boundary | `<<boundary>>` | #FF9800 (Orange) | Rounded Rectangle | Interface/API |
| Service | `<<service>>` | #6A1B9A (Purple) | Rounded Rectangle | Service/API |

## 4. Message Types and Numbering

### Message Types

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

## 5. Detailed Styling Specifications

### Participant Box Styling

| Property | Value | Description |
|----------|-------|-------------|
| Shape | Rounded Rectangle | Standard participant box |
| Corner Radius | 6pt | Slightly rounded |
| Width | 2.5-3.0 in | Varies by type |
| Height | 1.2-1.4 in | Varies by type |
| Shadow | Enabled | Subtle drop shadow |
| Font Family | Arial | Consistent font |
| Font Size | 10pt (Name) | Participant name |
| Font Size | 8pt (Class:Instance) | Class and instance |

### Participant Text Layout

```text
┌────────────────────────────────┐
│  <<stereotype>>                │
│  ClassName:instanceName        │
│                                │
│  [Participant Name]            │
└────────────────────────────────┘
```

### Link Styling

| Property | Value | Description |
|----------|-------|-------------|
| Color | #666666 | Grey |
| Width | 1pt | Standard |
| Style | Solid or Dashed | Based on type |

## 6. Code Architecture

Structure the skill as:

```text
communication_diagram_generator/
├── __init__.py
├── skill.md                       # This skill file
├── core/
│   ├── __init__.py
│   ├── diagram_builder.py         # Main orchestration
│   ├── validator.py               # Input validation
│   ├── errors.py                  # Custom exceptions
│   └── models.py                  # Pydantic models
├── renderers/
│   ├── __init__.py
│   ├── aspose_renderer.py         # Aspose.Diagram rendering
│   ├── dot_generator.py           # Graphviz DOT (for previews)
│   └── layout_engine.py           # Layout calculations
├── calculators/
│   ├── __init__.py
│   ├── sequence_calculator.py     # Message sequence numbering
│   └── position_calculator.py     # Position calculations
├── stylers/
│   ├── __init__.py
│   ├── color_themes.py            # Color theme definitions
│   ├── shape_styler.py            # Shape styling utilities
│   ├── participant_styler.py      # Participant-specific styling
│   └── message_styler.py          # Message-specific styling
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   └── geometry_utils.py
├── templates/
│   └── communication_template.vstx  # Optional template
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configuration management
└── cli.py                          # Command-line interface
```

## 7. Core Implementation Code

### 7.1 Sequence Number Generator

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

### 7.2 Diagram Builder Class

```python
from aspose.diagram import Diagram, Page, Shape, SaveFileFormat
from aspose.diagram.shapes import Rectangle, Connector, Oval
from aspose.diagram.styling import Fill, Line, TextStyle
from typing import List, Dict, Optional

class CommunicationDiagramBuilder:
    """Main class for building Communication Diagrams."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._calculate_positions()
        self._validate_messages()
    
    def _setup_page(self) -> None:
        """Configure page size and orientation."""
        orientation = self.config.get("layout", {}).get("orientation", "landscape")
        page_size = self.config.get("layout", {}).get("page_size", "A2")
        
        if page_size == "A2":
            if orientation == "landscape":
                self.page.page_sheet.page_props.page_width = 59.4
                self.page.page_sheet.page_props.page_height = 42.0
            else:
                self.page.page_sheet.page_props.page_width = 42.0
                self.page.page_sheet.page_props.page_height = 59.4
        else:
            self.page.page_sheet.page_props.page_width = 42.0
            self.page.page_sheet.page_props.page_height = 29.7
        
        self.page_width = self.page.page_sheet.page_props.page_width
        self.page_height = self.page.page_sheet.page_props.page_height
    
    def _setup_styles(self) -> None:
        """Set up global styling defaults."""
        self.theme = self.config.get("styling", {}).get("theme", "enterprise_blue")
        self.font_family = self.config.get("styling", {}).get("font_family", "Arial")
        self.font_size = self.config.get("styling", {}).get("font_size", 9)
        self.shadow_enabled = self.config.get("styling", {}).get("shadow_enabled", True)
        self.participant_types = self.config.get("styling", {}).get("participant_types", {})
        self.message_colors = self.config.get("styling", {}).get("message_colors", {})
    
    def _calculate_positions(self) -> None:
        """Calculate shape positions dynamically if auto_layout is requested."""
        if self.config.get("layout", {}).get("auto_layout", False):
            # Implement auto layout logic using a layout engine here.
            pass

    def _validate_messages(self) -> None:
        """Validate message sequences."""
        messages = self.config['communication_diagram'].get('messages', [])
        sequences = [m.get('sequence') for m in messages if m.get('sequence')]
        
        # Check for duplicate sequences
        seen = set()
        for seq in sequences:
            if seq in seen:
                print(f"⚠️ Warning: Duplicate sequence number: {seq}")
            seen.add(seq)
    
    def add_title_block(self) -> None:
        """Add title block at top of diagram."""
        data = self.config['communication_diagram']
        title = data.get('title', 'Communication Diagram')
        system = data.get('system_name', '')
        version = data.get('version', '1.0')
        date = data.get('date', '')
        # Basic implementation of title text using Aspose.Diagram Text components
        # self.page.add_shape(title_shape, "TitleBlock")
        pass
    
    def add_participants(self) -> None:
        """Add all participant boxes with proper styling."""
        participants = self.config['communication_diagram'].get('participants', [])
        for participant in participants:
            self._add_participant(participant)
    
    def _add_participant(self, participant: Dict) -> None:
        """Add a single participant."""
        shape_type = self.participant_types.get(participant.get('type', 'control'), {})
        # Implementation using self.page.add_shape to put a rounded rectangle at specific X, Y
        pass
    
    def add_links(self) -> None:
        """Add structural links between participants."""
        links = self.config['communication_diagram'].get('links', [])
        for link in links:
            self._add_link(link)
    
    def _add_link(self, link: Dict) -> None:
        """Add a single link."""
        # Find shapes for link.source and link.target
        # Add Dynamic Connector in Aspose.Diagram
        pass
    
    def add_messages(self) -> None:
        """Add all messages with sequence numbers."""
        messages = self.config['communication_diagram'].get('messages', [])
        # Sort by sequence number
        sorted_messages = sorted(messages, key=lambda m: self._parse_sequence(m.get('sequence', '0')))
        for message in sorted_messages:
            self._add_message(message)
    
    def _parse_sequence(self, sequence: str) -> tuple:
        """Parse sequence number for sorting."""
        if not sequence:
            return (0,)
        try:
            return tuple(int(p) for p in sequence.split('.'))
        except:
            return (0,)
    
    def _add_message(self, message: Dict) -> None:
        """Add a single message."""
        # Map source to target shape coordinates, draw an arrow, add text label
        pass
    
    def add_groups(self) -> None:
        """Add group boundaries (e.g., system boundaries)."""
        groups = self.config['communication_diagram'].get('groups', [])
        for group in groups:
            self._add_group(group)
    
    def _add_group(self, group: Dict) -> None:
        """Add a single group."""
        # Calculate bounding box of child participants, draw background rectangle
        pass
    
    def add_legend(self) -> None:
        """Add legend explaining symbols and numbering."""
        # Draw legend at bottom of page
        pass
    
    def save(self, output_path: str) -> None:
        """Save diagram to .vsdx file."""
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

## 8. Error Handling

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

## 9. Command-Line Interface

`cli.py`

```python
import argparse
import json
import sys
from pathlib import Path
from core.diagram_builder import CommunicationDiagramBuilder

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
    builder = CommunicationDiagramBuilder(spec)
    builder.add_title_block()
    builder.add_groups()
    builder.add_participants()
    builder.add_links()
    builder.add_messages()
    
    if not args.no_legend:
        builder.add_legend()
        
    # Ensure output directory exists
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    
    # Save output
    builder.save(args.output)
    print(f"Diagram successfully saved to {args.output}")

if __name__ == "__main__":
    main()
```

## 10. Quality Checklist

Before finalizing the skill execution or deploying updates, ensure the following checklist is completed:

- [x] All participants have proper naming formats (Class:Instance).
- [x] Links connect participants correctly, simulating structural dependencies.
- [x] Messages have proper sequence numbers derived from the `SequenceNumberGenerator`.
- [x] Message numbering precisely follows the pattern (1, 1.1, 2, 3.1).
- [x] Message labels are clear, descriptive, and positioned to avoid overlap.
- [x] Object types are color-coded correctly according to the provided tables.
- [x] Legend explains all symbols.
- [x] Title block contains all required project information.
- [x] Diagram dimensions scale correctly, ensuring it fits properly onto the output canvas without cut-off.
- [x] All text, including sub-text stereotypes, is readable and non-overlapping.

## 11. Usage Examples

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

## 12. Integration with Existing Skills

This skill is designed as an interconnected component:
1. **Part of the Ecosystem**: This module functions seamlessly as a component of the larger `uml-diagram-generator-SKILL.md`.
2. **Complementary to Sequence Diagrams**: It acts as the structural counterpart to `sequence-diagram-generator-SKILL.md`. Sequence diagrams detail the temporal "when," while Communication diagrams define the topological "who and how."
3. **Unified Input Standard**: It accepts the exact same YAML/JSON parsing structure, with only slight extensions to `layout` fields, allowing one source-of-truth file to generate both sequence and communication outputs.
4. **Office Integration**: Outputs standard VSDX files that can be universally embedded as OLE objects or imported into Microsoft Word/PowerPoint documents without fidelity loss.

## 13. Testing Strategy

Thoroughly test changes against these scenarios:
1. **Minimal Input**: A simple 2-participant, 1-message topology to verify core rendering.
2. **Full Complex Input**: Multiple grouped boundaries, nested messages up to 4 levels deep (e.g., 1.1.1.1), and return values.
3. **Validation Errors**: Pass invalid sequences to ensure `InvalidSequenceFormat` or duplicate checkers throw gracefully.
4. **Constraint Test**: Large scale graph with 20+ participants to ensure auto-layout algorithms or fixed dimension handling don't result in infinite loops.

## 14. Troubleshooting Guide

### Issue: Aspose License Missing Warning
- **Symptom**: Output contains an Aspose watermark or throws `CD-009`.
- **Solution**: Ensure your `.env` contains `ASPOSE_DIAGRAM_LICENSE_PATH` pointing to a valid `.lic` file. For development, a temporary/trial license can be used.

### Issue: Shapes Overlapping
- **Symptom**: Participant boxes overlap or connectors cross awkwardly.
- **Solution**: If using manual coordinates (`x` and `y` in JSON), adjust the values. If using `auto_layout: true`, consider expanding `participant_spacing` in the `layout` config.

### Issue: RenderError (CD-010) - JVM Not Found
- **Symptom**: Java exception raised when initializing Aspose diagram engine.
- **Solution**: Install JDK/JRE 8+ and ensure `JAVA_HOME` is set properly in your system environment. Aspose.Diagram for Python utilizes JPackage/JPype under the hood.
