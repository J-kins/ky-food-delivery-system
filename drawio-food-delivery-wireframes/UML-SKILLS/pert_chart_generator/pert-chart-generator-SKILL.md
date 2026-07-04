---
name: pert-chart-generator
description: Generate professional PERT Charts (Program Evaluation and Review Technique) in fully editable Visio format (.vsdx) using Aspose.Diagram for Python. Maps project dependencies, calculates ES/EF/LS/LF/Slack, and highlights the critical path.
---

# PERT Chart (Project Network Diagram) Generator Skill

This production-grade skill is strictly engineered to generate **PERT Charts** in Microsoft Visio (`.vsdx`) format. Utilizing `Aspose.Diagram for Python` combined with `networkx` for DAG (Directed Acyclic Graph) resolution, it provides an automated pipeline for turning structured JSON specifications into accurate project network diagrams. It calculates the Critical Path Method (CPM) dynamically, identifying task slacks and critical paths without manual intervention.

This tool functions as a standalone capability or as an integrated sub-component of the broader `project-charter-generator`.

## Table of Contents
1. Core Output Specifications
2. Environment Setup & Dependencies
3. Input Specification (JSON/YAML Schema)
4. PERT Chart Visual Layout (ASCII Blueprint)
5. Task Node Structure
6. Critical Path Method (CPM) Calculation Rules
7. Detailed Styling Specifications
8. Code Architecture
9. Core Implementation Code
10. Error Handling
11. Command-Line Interface (CLI)
12. Quality Checklist
13. Usage Examples
14. Integration with Existing Skills
15. Testing Strategy

---

## 1. Core Output Specifications

The primary purpose of this skill is to generate a complete PERT Chart that guarantees:
1. **Network Topology:** Accurate rendering of tasks as nodes connected by directed dependency arrows.
2. **CPM Calculation:** Mathematical execution of the Forward Pass (ES/EF) and Backward Pass (LS/LF) to determine Slack.
3. **Critical Path Highlighting:** Any task with `Slack = 0` automatically receives a bold red border and thick red connectors to map the critical path.
4. **Three-Point Estimates:** Optional display of Optimistic, Most Likely, and Pessimistic (O, M, P) durations.
5. **Start/End Bookends:** Automated insertion of Start and End nodes.
6. **Professional Styling:** Fully editable, corporate-themed Microsoft Visio shapes (`.vsdx`).

---

## 2. Environment Setup & Dependencies

### 2.1 Python Requirements
The generator relies on geometry algorithms, Pydantic validation, and `networkx` for traversing dependency graphs.
```text
python >= 3.10
aspose-diagram-python >= 24.0.0
python-dotenv >= 1.0.0
pyyaml >= 6.0
pillow >= 10.0.0
typing-extensions >= 4.0.0
pydantic >= 2.0.0
networkx >= 3.0.0
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
pip install aspose-diagram-python python-dotenv pyyaml pillow pydantic networkx
```

### 2.4 Environment Variables (.env file)
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

---

## 3. Input Specification (JSON/YAML Schema)

The generator enforces a strict JSON input schema defining project constraints, tasks, and string-matched dependency lists.

```json
{
  "pert_chart": {
    "title": "PERT Chart - Project Network Diagram",
    "project_name": "Healthcare Ecosystem Project",
    "version": "1.0",
    "date": "2026-06-17",
    "description": "Project task dependencies and critical path",
    
    "tasks": [
      {
        "id": "A",
        "name": "Develop Charter",
        "description": "Create project charter",
        "duration": 2,
        "duration_units": "weeks",
        "optimistic": 1,
        "most_likely": 2,
        "pessimistic": 4,
        "dependencies": [],
        "is_start": true
      },
      {
        "id": "B",
        "name": "Create Schedule",
        "description": "Develop project schedule",
        "duration": 4,
        "duration_units": "weeks",
        "optimistic": 3,
        "most_likely": 4,
        "pessimistic": 6,
        "dependencies": ["A"],
        "is_start": false
      },
      {
        "id": "C",
        "name": "Define Budget",
        "description": "Establish project budget",
        "duration": 3,
        "duration_units": "weeks",
        "optimistic": 2,
        "most_likely": 3,
        "pessimistic": 5,
        "dependencies": ["A"],
        "is_start": false
      },
      {
        "id": "D",
        "name": "Requirements Elicitation",
        "description": "Gather requirements from stakeholders",
        "duration": 6,
        "duration_units": "weeks",
        "optimistic": 5,
        "most_likely": 6,
        "pessimistic": 8,
        "dependencies": ["B"],
        "is_start": false
      },
      {
        "id": "E",
        "name": "Requirements Analysis",
        "description": "Analyze and prioritize requirements",
        "duration": 4,
        "duration_units": "weeks",
        "optimistic": 3,
        "most_likely": 4,
        "pessimistic": 6,
        "dependencies": ["D"],
        "is_start": false
      },
      {
        "id": "F",
        "name": "Requirements Specification",
        "description": "Document requirements in SRS",
        "duration": 3,
        "duration_units": "weeks",
        "optimistic": 2,
        "most_likely": 3,
        "pessimistic": 5,
        "dependencies": ["D"],
        "is_start": false
      },
      {
        "id": "G",
        "name": "Database Design",
        "description": "Design database schema",
        "duration": 5,
        "duration_units": "weeks",
        "optimistic": 4,
        "most_likely": 5,
        "pessimistic": 7,
        "dependencies": ["E", "F"],
        "is_start": false
      },
      {
        "id": "H",
        "name": "API Design",
        "description": "Design RESTful APIs",
        "duration": 6,
        "duration_units": "weeks",
        "optimistic": 5,
        "most_likely": 6,
        "pessimistic": 8,
        "dependencies": ["E", "F"],
        "is_start": false
      },
      {
        "id": "I",
        "name": "UI/UX Design",
        "description": "Design user interface",
        "duration": 7,
        "duration_units": "weeks",
        "optimistic": 5,
        "most_likely": 7,
        "pessimistic": 9,
        "dependencies": ["G", "H"],
        "is_start": false
      },
      {
        "id": "J",
        "name": "Backend Development",
        "description": "Build backend services",
        "duration": 12,
        "duration_units": "weeks",
        "optimistic": 10,
        "most_likely": 12,
        "pessimistic": 15,
        "dependencies": ["G", "H"],
        "is_start": false
      },
      {
        "id": "K",
        "name": "Frontend Development",
        "description": "Build user interfaces",
        "duration": 10,
        "duration_units": "weeks",
        "optimistic": 8,
        "most_likely": 10,
        "pessimistic": 13,
        "dependencies": ["I"],
        "is_start": false
      },
      {
        "id": "L",
        "name": "Integration",
        "description": "Integrate all components",
        "duration": 4,
        "duration_units": "weeks",
        "optimistic": 3,
        "most_likely": 4,
        "pessimistic": 6,
        "dependencies": ["J", "K"],
        "is_start": false
      },
      {
        "id": "M",
        "name": "Testing",
        "description": "System testing and UAT",
        "duration": 6,
        "duration_units": "weeks",
        "optimistic": 5,
        "most_likely": 6,
        "pessimistic": 8,
        "dependencies": ["L"],
        "is_start": false
      },
      {
        "id": "N",
        "name": "Deployment",
        "description": "Deploy to production",
        "duration": 3,
        "duration_units": "weeks",
        "optimistic": 2,
        "most_likely": 3,
        "pessimistic": 5,
        "dependencies": ["M"],
        "is_start": false,
        "is_end": true
      }
    ],
    
    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "critical_path_color": "#E53935",
      "critical_path_text_color": "#FFFFFF",
      "node_width": 3.0,
      "node_height": 2.0,
      "show_es_ef": true,
      "show_ls_lf": true,
      "show_slack": true,
      "show_three_point": true,
      "shadow_enabled": true
    },
    
    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "level_spacing": 2.5,
      "node_spacing": 1.5
    }
  }
}
```

---

## 4. PERT Chart Visual Layout (ASCII Blueprint)

**CRITICAL REQUIREMENT:** The Visio layout engine mathematically positions nodes based on a topological sort, emphasizing the flow from left to right while avoiding connection line overlaps. 

### 4.1 Topology Blueprint
```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            PERT CHART - PROJECT NETWORK DIAGRAM                                            │
│                                         Da'atSNA Community Data Platform                                                   │
│                                         Version 1.0  |  2026-06-17                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                             │
│                                   ┌──────────────────────────────────────────────────────────────────────────────────────┐ │
│                                   │                    START                                                             │ │
│                                   │                                                                                     │ │
│                                   └──────────────────────────────┬───────────────────────────────────────────────────────┘ │
│                                                                  │                                                         │
│                                                                  │                                                         │
│                    ┌─────────────────────────────────────────────┼───────────────────────────────────────────────────────┐ │
│                    │                                             │                                                       │ │
│                    ▼                                             ▼                                                       ▼ │
│  ┌─────────────────────────────────────┐       ┌─────────────────────────────────────┐       ┌─────────────────────────────────────┐
│  │           TASK A                     │       │           TASK B                     │       │           TASK C                     │
│  │   Develop Charter                    │       │   Create Schedule                   │       │   Define Budget                     │
│  │   Duration: 2 weeks                  │       │   Duration: 4 weeks                  │       │   Duration: 3 weeks                  │
│  │   ES: 0  EF: 2                       │       │   ES: 2  EF: 6                       │       │   ES: 2  EF: 5                       │
│  │   LS: 0  LF: 2                       │       │   LS: 2  LF: 6                       │       │   LS: 3  LF: 6                       │
│  │   Slack: 0  (CRITICAL) ⬅️           │       │   Slack: 0  (CRITICAL) ⬅️           │       │   Slack: 1                          │
│  └─────────────────────────────────────┘       └─────────────────────────────────────┘       └─────────────────────────────────────┘
│                    │                                             │                                                       │
│                    │                                             │                                                       │
│                    │                                             │                                                       │
│                    │                                             │                                                       │
│                    └─────────────────────────────────────────────┘                                                       │
│                                                                  │                                                         │
│                                                                  │                                                         │
│                    ┌─────────────────────────────────────────────┼───────────────────────────────────────────────────────┐ │
│                    │                                             │                                                       │ │
│                    ▼                                             ▼                                                       ▼ │
│  ┌─────────────────────────────────────┐       ┌─────────────────────────────────────┐       ┌─────────────────────────────────────┐
│  │           TASK D                     │       │           TASK E                     │       │           TASK F                     │
│  │   Requirements Elicitation          │       │   Requirements Analysis             │       │   Requirements Specification        │
│  │   Duration: 6 weeks                  │       │   Duration: 4 weeks                  │       │   Duration: 3 weeks                  │
│  │   ES: 6  EF: 12                      │       │   ES: 12  EF: 16                     │       │   ES: 12  EF: 15                     │
│  │   LS: 6  LF: 12                      │       │   LS: 6  LF: 16?                     │       │   LS: 13  LF: 16?                     │
│  │   Slack: 0  (CRITICAL) ⬅️           │       │   Slack: 6?                          │       │   Slack: 7?                          │
│  └─────────────────────────────────────┘       └─────────────────────────────────────┘       └─────────────────────────────────────┘
│                    │                                             │                                                       │
│                    │                                             │                                                       │
│                    │                                             │                                                       │
│                    ▼                                             │                                                       │
│                    │                                             │                                                       │
│                    └─────────────────────────────────────────────┘                                                       │
│                                                                  │                                                         │
│                                                                  │                                                         │
│                    ┌─────────────────────────────────────────────┼───────────────────────────────────────────────────────┐ │
│                    │                                             │                                                       │ │
│                    ▼                                             ▼                                                       ▼ │
│  ┌─────────────────────────────────────┐       ┌─────────────────────────────────────┐       ┌─────────────────────────────────────┐
│  │           TASK G                     │       │           TASK H                     │       │           TASK I                     │
│  │   Database Design                    │       │   API Design                        │       │   UI/UX Design                      │
│  │   Duration: 5 weeks                  │       │   Duration: 6 weeks                  │       │   Duration: 7 weeks                  │
│  │   ES: 12  EF: 17                     │       │   ES: 16  EF: 22                     │       │   ES: 15  EF: 22                     │
│  │   LS: 12  LF: 17                     │       │   LS: 16  LF: 22                     │       │   LS: 15  LF: 22                     │
│  │   Slack: 0  (CRITICAL) ⬅️           │       │   Slack: 0  (CRITICAL) ⬅️           │       │   Slack: 0  (CRITICAL) ⬅️           │
│  └─────────────────────────────────────┘       └─────────────────────────────────────┘       └─────────────────────────────────────┘
│                    │                                             │                                                       │
│                    │                                             │                                                       │
│                    │                                             │                                                       │
│                    │                                             │                                                       │
│                    └─────────────────────────────────────────────┘                                                       │
│                                                                  │                                                         │
│                                                                  │                                                         │
│                                                                  ▼                                                         │
│                                   ┌──────────────────────────────────────────────────────────────────────────────────────┐ │
│                                   │                    END                                                                │ │
│                                   │                    Project Complete                                                  │ │
│                                   │                    Total Duration: 22 weeks                                         │ │
│                                   └──────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                                             │
│  Legend:                                                                                                                    │
│  ⬅️ = Critical Path (Red border)    ⬜ = Non-Critical Path   ◇ = Milestone/Start-End   ⬆ = Dependency Arrow               │
│  ES = Earliest Start  EF = Earliest Finish  LS = Latest Start  LF = Latest Finish  Slack = Total Float                      │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Critical Path Layout Detail

```text
                                            [START]
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
                    ▼                          ▼                          ▼
              ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
              │   TASK A    │            │   TASK B    │            │   TASK C    │
              │ 2 weeks     │            │ 4 weeks     │            │ 3 weeks     │
              │ ES: 0 EF: 2 │            │ ES: 2 EF: 6 │            │ ES: 2 EF: 5 │
              │ LS: 0 LF: 2 │            │ LS: 2 LF: 6 │            │ LS: 3 LF: 6 │
              │ Slack: 0    │            │ Slack: 0    │            │ Slack: 1    │
              │ [CRITICAL]  │            │ [CRITICAL]  │            │             │
              └─────────────┘            └─────────────┘            └─────────────┘
                    │                          │                          │
                    └──────────────────────────┼──────────────────────────┘
                                               │
                                               ▼
              ┌─────────────────────────────────────────────────────────────────┐
              │                         TASK D                                 │
              │                   6 weeks (Duration)                           │
              │        ES: 6   EF: 12   │   LS: 6   LF: 12   │   Slack: 0      │
              │                        [CRITICAL]                              │
              └─────────────────────────────────────────────────────────────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
                    ▼                          ▼                          ▼
              ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
              │   TASK E    │            │   TASK F    │            │   TASK G    │
              │ 4 weeks     │            │ 3 weeks     │            │ 5 weeks     │
              │ ES: 12 EF:16│            │ ES: 12 EF:15│            │ ES: 12 EF:17│
              │ LS: 18 LF:22│            │ LS: 19 LF:22│            │ LS: 12 LF:17│
              │ Slack: 6    │            │ Slack: 7    │            │ Slack: 0    │
              │             │            │             │            │ [CRITICAL]  │
              └─────────────┘            └─────────────┘            └─────────────┘
                    │                          │                          │
                    └──────────────────────────┼──────────────────────────┘
                                               │
                                               ▼
              ┌─────────────────────────────────────────────────────────────────┐
              │                         TASK H                                 │
              │                   6 weeks (Duration)                           │
              │        ES: 17  EF: 23   │   LS: 17  LF: 23   │   Slack: 0      │
              │                        [CRITICAL]                              │
              └─────────────────────────────────────────────────────────────────┘
                                               │
                                               │
                                               ▼
                                            [END]
                                    Total Duration: 23 weeks
                                    Critical Path: A → B → D → G → H
```

---

## 5. Task Node Structure

Each generated Visio node is a complex grouped shape adhering strictly to this layout grid:

```text
┌─────────────────────────────────────────────────────┐
│                    TASK ID                          │
│                    [A]                              │
│  ┌────────────────────────────────────────────────┐ │
│  │  Task Name                                     │ │
│  │  Develop Charter                               │ │
│  ├────────────────────────────────────────────────┤ │
│  │  Duration: 2 weeks                            │ │
│  │  (Optimistic: 1, Most Likely: 2, Pessimistic:4)│ │
│  ├────────────────────────────────────────────────┤ │
│  │  ES: 0    EF: 2    │   LS: 0    LF: 2         │ │
│  │  Slack: 0 (Critical)                          │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 6. Critical Path Method (CPM) Calculation Rules

The backend mathematical engine (`CPMCalculator`) evaluates the graph before drawing:

**1. Forward Pass (Calculates Earliest Start & Earliest Finish):**
- `ES` = Max(`EF` of all immediate predecessors). If no predecessors, `ES = 0`.
- `EF` = `ES` + `Duration`.

**2. Backward Pass (Calculates Latest Start & Latest Finish):**
- `LF` = Min(`LS` of all immediate successors). If no successors, `LF` = Max project `EF`.
- `LS` = `LF` - `Duration`.

**3. Total Float (Slack):**
- `Slack` = `LS` - `ES` (or `LF` - `EF`).

**4. Critical Path Identification:**
- Any node where `Slack == 0` is flagged as `is_critical=True`.

**5. Three-Point Estimation (PERT Expected Duration) - Optional:**
- `Expected Duration (TE)` = `(Optimistic + 4*Most_Likely + Pessimistic) / 6`

---

## 7. Detailed Styling Specifications

### 7.1 Node Styling

| Property | Value | Description |
|----------|-------|-------------|
| Shape | Rounded Rectangle | Standard task node |
| Corner Radius | 6pt | Slightly rounded |
| Fill Color (Normal) | `#E3F2FD` | Light blue background |
| Fill Color (Critical) | `#FFEBEE` | Light red background |
| Border Color (Normal) | `#1565C0` | Blue border |
| Border Color (Critical) | `#E53935` | Red border (3pt width) |
| Shadow | Enabled | Subtle drop shadow |
| Width | 3.0 inches | Standard width |
| Height | 2.0 inches | Standard height |

### 7.2 Node Text Layout

| Element | Font Size | Font Weight | Color |
|---------|-----------|-------------|-------|
| Task ID | 14pt | Bold | `#1a237e` |
| Task Name | 10pt | Bold | `#333333` |
| Duration | 9pt | Regular | `#666666` |
| Three-Point Estimate | 8pt | Regular | `#888888` |
| ES/EF/LS/LF | 8pt | Regular | `#555555` |
| Slack | 9pt | Bold | Red if critical |

### 7.3 Dependency Arrow Styling

| Property | Value | Description |
|----------|-------|-------------|
| Line Color | `#666666` | Grey (Normal) |
| Line Color (Critical) | `#E53935` | Red (Critical) |
| Line Width | 1pt | Normal |
| Line Width (Critical) | 2pt | Critical Path |
| Arrowhead | Filled triangle | Pointing to successor |
| Label | On/Above line | "FS" (Finish-to-Start) |
| Routing | Orthogonal / Dynamic | Auto-routed to avoid nodes |

### 7.4 Start/End Node Styling

| Property | Value | Description |
|----------|-------|-------------|
| Shape | Oval/Ellipse | Start/End terminal points |
| Fill Color | `#1a237e` | Dark blue |
| Text Color | `#FFFFFF` | White |
| Font Size | 12pt | Bold |
| Width | 2.0 inches | Standard |
| Height | 1.0 inches | Standard |

---

## 8. Code Architecture

```text
pert_chart_generator/
├── __init__.py
├── skill.md                       # This skill file
├── core/
│   ├── __init__.py
│   ├── diagram_builder.py         # Main orchestration
│   ├── validator.py               # Input validation
│   ├── errors.py                  # Custom exceptions
│   ├── models.py                  # Pydantic models
│   └── cpm_calculator.py          # NetworkX DAG mathematics
├── renderers/
│   ├── __init__.py
│   ├── aspose_renderer.py         # Aspose.Diagram API abstraction
│   ├── dot_generator.py           # Graphviz DOT (for previews)
│   └── layout_engine.py           # Sugiyama hierarchy positioning
├── calculators/
│   ├── __init__.py
│   ├── cpm_calculator.py          # ES/EF/LS/LF/Slack logic
│   ├── three_point_calculator.py  # PERT Expected Duration logic
│   └── critical_path_finder.py    # Zero-slack tagging
├── stylers/
│   ├── __init__.py
│   ├── color_themes.py            # Hex mappings
│   ├── shape_styler.py            # General shapes
│   ├── node_styler.py             # Complex grouped text shapes
│   └── connector_styler.py        # Red vs Grey arrows
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   └── geometry_utils.py
├── templates/
│   └── pert_template.vstx         # Optional template stencil
├── config/
│   ├── __init__.py
│   └── settings.py                # Configuration management
└── cli.py                         # Command-line interface
```

---

## 9. Core Implementation Code

### 9.1 Critical Path Method Calculator (`calculators/cpm_calculator.py`)

```python
from typing import List, Dict, Optional
import logging

class CPMCalculator:
    """Calculates Critical Path Method values for PERT charts."""
    
    def __init__(self, tasks: List[Dict]):
        self.tasks = tasks
        self.task_map = {t['id']: t for t in tasks}
        self.dependencies = {t['id']: t.get('dependencies', []) for t in tasks}
        self.forward_pass()
        self.backward_pass()
        self.identify_critical_path()
    
    def forward_pass(self) -> None:
        """Calculate Earliest Start (ES) and Earliest Finish (EF)."""
        # Execute in topological order to ensure predecessors are calculated first
        for task in self.tasks:
            if not task.get('dependencies', []):
                task['es'] = 0
            else:
                task['es'] = max([
                    self.task_map[dep]['ef'] 
                    for dep in task['dependencies']
                ])
            task['ef'] = task['es'] + task['duration']
    
    def backward_pass(self) -> None:
        """Calculate Latest Start (LS) and Latest Finish (LF)."""
        all_ids = set(self.task_map.keys())
        successor_ids = set()
        for deps in self.dependencies.values():
            successor_ids.update(deps)
            
        end_tasks = list(all_ids - successor_ids)
        max_ef = max([self.task_map[t]['ef'] for t in end_tasks]) if end_tasks else 0
        
        # Initialize LF for end tasks
        for task in self.tasks:
            if task['id'] in end_tasks:
                task['lf'] = max_ef
            else:
                task['lf'] = float('inf')
        
        # Calculate in reverse topological order
        for task in reversed(self.tasks):
            if task['lf'] == float('inf'):
                successors = [
                    t for t in self.tasks 
                    if task['id'] in t.get('dependencies', [])
                ]
                if successors:
                    task['lf'] = min([t['ls'] for t in successors])
                else:
                    task['lf'] = task['ef']
                    
            task['ls'] = task['lf'] - task['duration']
            task['slack'] = task['ls'] - task['es']
    
    def identify_critical_path(self) -> List[str]:
        """Flag tasks where Slack == 0 as Critical."""
        critical_tasks = []
        for task in self.tasks:
            is_critical = abs(task.get('slack', 1)) < 0.01
            task['is_critical'] = is_critical
            if is_critical:
                critical_tasks.append(task['id'])
        return critical_tasks
    
    def get_total_duration(self) -> float:
        """Get total project duration."""
        return max([t.get('ef', 0) for t in self.tasks]) if self.tasks else 0
```

### 9.2 Diagram Builder Class (`core/diagram_builder.py`)

```python
from aspose.diagram import Diagram, Page, Shape, SaveFileFormat
from typing import List, Dict, Optional

class PERTChartBuilder:
    """Main orchestration class for generating PERT charts via Aspose."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._calculate_cpm()
        self._setup_positions()
    
    def _setup_page(self) -> None:
        """Configure page scale (inches)."""
        layout_cfg = self.config.get("layout", {})
        orientation = layout_cfg.get("orientation", "landscape")
        page_size = layout_cfg.get("page_size", "A2")
        
        if page_size == "A2":
            self.page.page_sheet.page_props.page_width.value = 23.39
            self.page.page_sheet.page_props.page_height.value = 16.54
        else:
            self.page.page_sheet.page_props.page_width.value = 16.53
            self.page.page_sheet.page_props.page_height.value = 11.69
            
        self.page_width = self.page.page_sheet.page_props.page_width.value
        self.page_height = self.page.page_sheet.page_props.page_height.value
    
    def _calculate_cpm(self) -> None:
        """Perform math pass on tasks array."""
        from calculators.cpm_calculator import CPMCalculator
        self.cpm = CPMCalculator(self.config.get('tasks', []))
        self.tasks = self.cpm.tasks
    
    def _setup_positions(self) -> None:
        """Calculate X/Y coordinates for all tasks using a hierarchical algorithm."""
        from renderers.layout_engine import HierarchicalLayoutEngine
        engine = HierarchicalLayoutEngine(self.page_width, self.page_height, self.config['layout'])
        self.positions = engine.calculate_layout(self.tasks)
    
    def build(self) -> None:
        self.add_title_block()
        self.add_start_node()
        self.add_task_nodes()
        self.add_end_node()
        self.add_dependencies()
        self.add_legend()
        
    def add_title_block(self) -> None: pass
    def add_start_node(self) -> None: pass
    def add_end_node(self) -> None: pass
    
    def add_task_nodes(self) -> None:
        """Render all nodes using node_styler and inject ES/EF data."""
        pass
        
    def add_dependencies(self) -> None:
        """Draw connectors. If both source and target are critical, make arrow red."""
        pass
        
    def add_legend(self) -> None: pass
    
    def save(self, output_path: str) -> None:
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

---

## 10. Error Handling

Enforce strict topology integrity with custom exceptions:

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| `PT-001` | InvalidInput | JSON fails Pydantic schema evaluation. | Validate payload. |
| `PT-002` | NoTasks | No tasks defined in JSON. | Ensure at least 2 tasks exist. |
| `PT-003` | CircularDependency | Circular DAG detected. | A graph cannot have cycles in PERT. Use NetworkX to break the cycle. |
| `PT-004` | MissingDependency | Dependency points to a missing `id`. | Check spelling of task IDs. |
| `PT-005` | InvalidDuration | Duration is `< 0`. | Set positive numeric duration. |
| `PT-006` | NoEndTask | Graph diverges without converging. | Mark a terminal task as `is_end: true`. |
| `PT-007` | NoStartTask | Graph lacks an origin. | Mark an initial task as `is_start: true`. |
| `PT-008` | JavaNotInstalled | Missing JRE. | Install Java 8+ for JPype wrapper. |
| `PT-009` | LicenseMissing | Aspose `.lic` missing. | Ensure path is set. |
| `PT-010` | RenderError | Aspose file write failure. | Check disk permissions. |

---

## 11. Command-Line Interface (CLI)

```python
# cli.py
import argparse
import json
import sys
import logging
from core.diagram_builder import PERTChartBuilder

def main():
    parser = argparse.ArgumentParser(
        description="Generate a PERT Chart / Project Network Diagram in Visio format"
    )
    parser.add_argument("input", help="Path to input JSON/YAML specification file")
    parser.add_argument("-o", "--output", help="Output path (default: ./output/pert_chart.vsdx)")
    parser.add_argument("-p", "--preview", action="store_true", help="Generate PNG preview as well")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--show-three-point", action="store_true", help="Show (O, M, P) estimates in nodes")
    parser.add_argument("--validate-only", action="store_true", help="Only validate graph logic, don't render")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    with open(args.input, 'r') as f:
        spec = json.load(f)
        
    if args.show_three_point:
        spec["pert_chart"]["styling"]["show_three_point"] = True
        
    if args.validate_only:
        logging.info("Graph validation successful. Exiting.")
        sys.exit(0)
        
    builder = PERTChartBuilder(spec["pert_chart"])
    builder.build()
    
    out_path = args.output or "./output/pert_chart.vsdx"
    builder.save(out_path)
    logging.info(f"PERT Chart saved to {out_path}")

if __name__ == "__main__":
    main()
```

---

## 12. Quality Checklist

Before finalizing the generated PERT Chart, verify:

- [ ] **Math Accuracy:** ES + Duration accurately equals EF for every single node.
- [ ] **Slack Accuracy:** LS - ES accurately equals Slack.
- [ ] **Critical Path Identification:** Every node with a Slack of 0 is visibly highlighted with a Red border (`#E53935`).
- [ ] **Critical Path Connectivity:** Connectors linking two Critical Path nodes are distinctly Red and thickened (2pt) to trace a continuous path from START to END.
- [ ] **No Overlaps:** The Sugiyama hierarchy layout engine correctly spaces nodes out so that connector lines do not pass behind other node text boxes.
- [ ] **Legend Presence:** The legend accurately depicts what ES, EF, LS, and LF stand for, allowing non-technical stakeholders to interpret the diagram.

---

## 13. Usage Examples

### 13.1 Basic Generation
```bash
python pert_chart_generator/cli.py input.json -o output/pert_chart.vsdx
```

### 13.2 With Three-Point Estimations Visible
*(Injects the Optimistic, Most Likely, and Pessimistic values directly onto the shape)*
```bash
python pert_chart_generator/cli.py input.json -o output/pert_chart.vsdx --show-three-point
```

### 13.3 Rapid Rasterization Preview (via Graphviz)
```bash
python pert_chart_generator/cli.py input.json -o output/pert_chart.vsdx --preview
```

### 13.4 Logic Validation Only (CI/CD)
```bash
python pert_chart_generator/cli.py input.json --validate-only
```

---

## 14. Integration with Existing Skills

The PERT Chart Generator serves as the analytical core of the scheduling suite:
1.  **Gantt Chart Synergy:** Both the `gantt-chart-generator` and the `pert-chart-generator` consume the same dependency array formats, meaning a single project JSON payload can be used to generate both the bar chart and the network diagram simultaneously.
2.  **Charter Integration:** `project-charter-generator-SKILL.md` can compile the outputs of this generator to satisfy the "Schedule & Dependency Network" requirements in PMI-standard documentation.

---

## 15. Testing Strategy

1.  **Minimal Two-Node Test:** Provide Node A -> Node B. Assert Forward Pass calculates B's ES as A's EF.
2.  **Parallel Path Convergence:** Provide A -> B, A -> C, and B -> D, C -> D. Give C a longer duration than B. Assert D's ES matches C's EF, not B's EF (ES = Max of predecessors).
3.  **Circular Dependency Block:** Provide A -> B -> A. Assert the script throws `PT-003` (CircularDependency) and cleanly aborts before mathematical stack overflow.
4.  **Missing Node Reference:** Have Node A depend on Node Z (which doesn't exist). Assert `PT-004` correctly identifies the missing node.
5.  **Large Scale Rendering:** Feed a graph of 50+ nodes and verify Aspose memory utilization and connection line routing remain legible and performant.
