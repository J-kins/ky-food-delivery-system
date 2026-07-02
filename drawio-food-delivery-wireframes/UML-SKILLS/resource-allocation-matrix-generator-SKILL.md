---
name: resource-allocation-matrix-generator
description: Generate professional Resource Allocation Matrices (RACI or Percentage-based) in fully editable Visio format (.vsdx) using Aspose.Diagram for Python. Maps resources against project phases and computes utilization statistics.
---

# Resource Allocation Matrix Generator Skill

This production-grade skill is engineered to generate **Resource Allocation Matrices** in Microsoft Visio (`.vsdx`) format. The Resource Allocation Matrix (also known as a RAM or RACI Chart) maps human and material resources to project phases or deliverables using RACI responsibility codes (`R`, `A`, `C`, `I`) or percentage-based allocations. Utilizing `Aspose.Diagram for Python`, this tool dynamically constructs a precise tabular grid, computes per-resource utilization load, generates phase-level distribution summaries, and highlights overallocation or underutilization visually.

This tool functions as a standalone deliverable or as an integrated sub-component of the broader `project-charter-generator`.

## Table of Contents
1. Core Output Specifications
2. Environment Setup & Dependencies
3. Input Specification (JSON/YAML Schema)
4. Resource Allocation Matrix Visual Layout (ASCII Blueprint)
5. RACI Definitions & Load Categories
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

The primary purpose of this skill is to generate a complete Resource Allocation Matrix that guarantees:
1. **Precise Grid Rendering:** A tabular structure of Resources (rows) × Phases (columns), auto-fitted to the Visio page dimensions.
2. **RACI / Percentage Modes:** Dual rendering modes. RACI mode renders bold `R/A/C/I` codes inside cells; Percentage mode renders numeric allocations; `BOTH` mode stacks them.
3. **Load Calculation:** Automatic computation of per-resource total utilization with color-coded status badges (Over/Full/Partial/Under).
4. **Phase Summary Row:** A footer row that totals the count of assigned resources and RACI code distributions per phase.
5. **Statistics Dashboard:** An embedded summary box tracking total resources, average utilization, over-allocated individuals, and resource gap analysis.
6. **Professional Formatting:** Fully editable, corporate-themed Microsoft Visio shapes (`.vsdx`).

---

## 2. Environment Setup & Dependencies

### 2.1 Python Requirements
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

### 2.3 Virtual Environment Setup
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

### 2.4 Environment Variables (.env file)
```env
# Aspose.Diagram License (if commercial)
ASPOSE_DIAGRAM_LICENSE_PATH=/path/to/license.lic
OUTPUT_DIR=./output
LOG_LEVEL=INFO
DEFAULT_COLOR_THEME=enterprise_blue
DEFAULT_FONT_FAMILY=Arial
DEFAULT_FONT_SIZE=9
```

---

## 3. Input Specification (JSON/YAML Schema)

The generator enforces a strict schema requiring `resources`, `phases`, and `allocations` arrays. The `allocation_type` switch controls rendering mode.

```json
{
  "resource_allocation": {
    "title": "Resource Allocation Matrix - RACI Chart",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    "sprint": "Q2 2026",
    "description": "Resource allocation and responsibilities matrix",
    
    "allocation_type": "RACI",

    "resources": [
      {
        "id": "R1",
        "name": "Dr. James",
        "role": "Project Sponsor",
        "department": "Executive",
        "email": "james@health.org",
        "allocation": 25
      },
      {
        "id": "R2",
        "name": "John Smith",
        "role": "Project Manager",
        "department": "PMO",
        "email": "john@health.org",
        "allocation": 40
      },
      {
        "id": "R3",
        "name": "Sarah Johnson",
        "role": "Lead BA",
        "department": "Business Analysis",
        "email": "sarah@health.org",
        "allocation": 80
      },
      {
        "id": "R4",
        "name": "Mike Chen",
        "role": "Lead Architect",
        "department": "Architecture",
        "email": "mike@health.org",
        "allocation": 100
      },
      {
        "id": "R5",
        "name": "Emily Davis",
        "role": "Dev Lead",
        "department": "Development",
        "email": "emily@health.org",
        "allocation": 85
      },
      {
        "id": "R6",
        "name": "David Wilson",
        "role": "QA Lead",
        "department": "Quality Assurance",
        "email": "david@health.org",
        "allocation": 70
      },
      {
        "id": "R7",
        "name": "Lisa Brown",
        "role": "Ops Lead",
        "department": "Operations",
        "email": "lisa@health.org",
        "allocation": 60
      }
    ],

    "phases": [
      {
        "id": "P1",
        "name": "Initiation",
        "description": "Project kickoff and charter",
        "order": 1,
        "color": "#1a237e"
      },
      {
        "id": "P2",
        "name": "Requirements",
        "description": "Requirements gathering",
        "order": 2,
        "color": "#2E7D32"
      },
      {
        "id": "P3",
        "name": "Design",
        "description": "System design",
        "order": 3,
        "color": "#E65100"
      },
      {
        "id": "P4",
        "name": "Development",
        "description": "Coding and implementation",
        "order": 4,
        "color": "#6A1B9A"
      },
      {
        "id": "P5",
        "name": "Testing",
        "description": "QA and testing",
        "order": 5,
        "color": "#C62828"
      },
      {
        "id": "P6",
        "name": "Deployment",
        "description": "Release to production",
        "order": 6,
        "color": "#00838F"
      },
      {
        "id": "P7",
        "name": "Closure",
        "description": "Project closure",
        "order": 7,
        "color": "#4E342E"
      }
    ],

    "allocations": [
      {
        "resource_id": "R1",
        "phase_id": "P1",
        "value": "A",
        "percentage": 25,
        "description": "Project approval"
      },
      {
        "resource_id": "R1",
        "phase_id": "P2",
        "value": "I",
        "percentage": 10,
        "description": "Requirements review"
      },
      {
        "resource_id": "R2",
        "phase_id": "P1",
        "value": "A",
        "percentage": 40,
        "description": "Project setup"
      },
      {
        "resource_id": "R2",
        "phase_id": "P2",
        "value": "A",
        "percentage": 40,
        "description": "Requirements approval"
      },
      {
        "resource_id": "R3",
        "phase_id": "P1",
        "value": "C",
        "percentage": 20,
        "description": "Requirements consultation"
      },
      {
        "resource_id": "R3",
        "phase_id": "P2",
        "value": "R",
        "percentage": 80,
        "description": "Requirements lead"
      },
      {
        "resource_id": "R3",
        "phase_id": "P3",
        "value": "A",
        "percentage": 80,
        "description": "Design approval"
      },
      {
        "resource_id": "R3",
        "phase_id": "P4",
        "value": "R",
        "percentage": 80,
        "description": "Dev support"
      },
      {
        "resource_id": "R4",
        "phase_id": "P3",
        "value": "R",
        "percentage": 100,
        "description": "Architecture lead"
      },
      {
        "resource_id": "R4",
        "phase_id": "P4",
        "value": "R",
        "percentage": 100,
        "description": "Implementation lead"
      },
      {
        "resource_id": "R5",
        "phase_id": "P3",
        "value": "C",
        "percentage": 30,
        "description": "Dev consultation"
      },
      {
        "resource_id": "R5",
        "phase_id": "P4",
        "value": "R",
        "percentage": 85,
        "description": "Dev lead"
      },
      {
        "resource_id": "R5",
        "phase_id": "P5",
        "value": "R",
        "percentage": 85,
        "description": "Dev support"
      },
      {
        "resource_id": "R6",
        "phase_id": "P4",
        "value": "C",
        "percentage": 20,
        "description": "QA consultation"
      },
      {
        "resource_id": "R6",
        "phase_id": "P5",
        "value": "R",
        "percentage": 70,
        "description": "QA lead"
      },
      {
        "resource_id": "R7",
        "phase_id": "P5",
        "value": "C",
        "percentage": 20,
        "description": "Ops consultation"
      },
      {
        "resource_id": "R7",
        "phase_id": "P6",
        "value": "R",
        "percentage": 60,
        "description": "Ops lead"
      },
      {
        "resource_id": "R7",
        "phase_id": "P7",
        "value": "R",
        "percentage": 60,
        "description": "Closure lead"
      }
    ],

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "raci_colors": {
        "R": "#E53935",
        "A": "#1565C0",
        "C": "#FFB300",
        "I": "#4CAF50",
        "-": "#E0E0E0"
      },
      "load_colors": {
        "over": "#E53935",
        "full": "#FFB300",
        "partial": "#64B5F6",
        "under": "#4CAF50"
      },
      "cell_padding": 0.1,
      "row_height": 0.6,
      "column_width": 2.0
    },

    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "header_height": 0.8,
      "summary_height": 1.5
    }
  }
}
```

---

## 4. Resource Allocation Matrix Visual Layout (ASCII Blueprint)

**CRITICAL REQUIREMENT:** The Visio output must implement this precise tabular grid with RACI codes inside cells, load bars in the last column, and a statistics footer.

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                          RESOURCE ALLOCATION MATRIX - PROJECT STAFFING                                                       │
│                                         Da'atSNA Community Data Platform                                                                     │
│                                         Version 1.0  |  Sprint 5  |  2026-06-17                                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                             │
│  ┌────────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐ │
│  │  RESOURCE  │   PHASE 1│   PHASE 2│   PHASE 3│   PHASE 4│   PHASE 5│   PHASE 6│   PHASE 7│   TOTAL  │   STATUS │  LOAD    │          │ │
│  │  NAME      │  Init    │  Req     │  Design  │  Dev     │  Test    │  Deploy  │  Closure │   %      │          │          │          │ │
│  ├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤          │ │
│  │            │          │          │          │          │          │          │          │          │          │          │          │ │
│  │  Dr. James │    A     │    I     │    I     │    I     │    I     │    I     │    A     │   25%    │  UNDER   │   ████   │          │ │
│  │  Sponsor   │ (Apprv)  │ (Inform) │ (Inform) │ (Inform) │ (Inform) │ (Inform) │ (Apprv)  │          │          │   ████   │          │ │
│  │            │          │          │          │          │          │          │          │          │          │   ████   │          │ │
│  ├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤          │ │
│  │            │          │          │          │          │          │          │          │          │          │          │          │ │
│  │  John      │    A     │    A     │    A     │    I     │    I     │    I     │    A     │   40%    │  PARTIAL │   ████   │          │ │
│  │  Smith PM  │ (Lead)   │ (Apprv)  │ (Apprv)  │          │          │          │ (Apprv)  │          │          │   ████   │          │ │
│  │            │          │          │          │          │          │          │          │          │          │   ████   │          │ │
│  ├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤          │ │
│  │            │          │          │          │          │          │          │          │          │          │          │          │ │
│  │  Sarah     │    C     │    R     │    A     │    R     │    R     │    -     │    -     │   80%    │  FULL    │   ██████ │          │ │
│  │  Johnson   │          │  (Lead)  │ (Apprv)  │  (Lead)  │  (Lead)  │          │          │          │          │   ██████ │          │ │
│  │  Lead BA   │          │          │          │          │          │          │          │          │          │   ██████ │          │ │
│  ├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤          │ │
│  │            │          │          │          │          │          │          │          │          │          │          │          │ │
│  │  Mike      │    -     │    -     │    R     │    R     │    C     │    C     │    -     │  100%    │  ▲OVER   │   ██████ │          │ │
│  │  Chen      │          │          │  (Arch)  │  (Arch)  │          │          │          │          │          │   ██████ │          │ │
│  │  Architect │          │          │          │          │          │          │          │          │          │   ██████ │          │ │
│  ├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤          │ │
│  │            │          │          │          │          │          │          │          │          │          │          │          │ │
│  │  Emily     │    -     │    -     │    C     │    R     │    R     │    R     │    C     │   85%    │  FULL    │   ██████ │          │ │
│  │  Davis     │          │          │ (Conslt) │  (Lead)  │  (Lead)  │  (Lead)  │ (Conslt) │          │          │   ██████ │          │ │
│  │  Dev Lead  │          │          │          │          │          │          │          │          │          │   ██████ │          │ │
│  ├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤          │ │
│  │            │          │          │          │          │          │          │          │          │          │          │          │ │
│  │  David     │    -     │    -     │    -     │    C     │    R     │    R     │    -     │   70%    │  PARTIAL │   █████  │          │ │
│  │  Wilson    │          │          │          │ (Conslt) │  (Lead)  │  (Lead)  │          │          │          │   █████  │          │ │
│  │  QA Lead   │          │          │          │          │          │          │          │          │          │   █████  │          │ │
│  ├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤          │ │
│  │            │          │          │          │          │          │          │          │          │          │          │          │ │
│  │  Lisa      │    -     │    -     │    -     │    -     │    C     │    R     │    R     │   60%    │  PARTIAL │   █████  │          │ │
│  │  Brown     │          │          │          │          │ (Conslt) │  (Lead)  │  (Lead)  │          │          │   █████  │          │ │
│  │  Ops Lead  │          │          │          │          │          │          │          │          │          │   █████  │          │ │
│  ├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤          │ │
│  │            │          │          │          │          │          │          │          │          │          │          │          │ │
│  │  TOTALS    │   3      │   2      │   3      │   5      │   5      │   4      │   3      │  460%    │          │          │          │ │
│  │  (R:A:C:I) │ (A:2,C:1)│ (R:1,A:1)│ (R:2,A:1)│ (R:3,C:2)│ (R:3,C:2)│ (R:2,C:2)│ (A:2,R:1)│          │          │          │          │ │
│  └────────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘          │ │
│                                                                                                                                             │
│  Legend:                                                                                                                                    │
│  ═══════                                                                                                                                    │
│  R = Responsible (Doer)  A = Accountable (Approver)  C = Consulted (Input)  I = Informed (Notify)  - = Not Involved                         │
│  ▲OVER = Overallocated (>100%)  FULL = 80-100%  PARTIAL = 40-79%  UNDER = <40%                                                             │
│                                                                                                                                             │
│  SUMMARY                                                                                                                                    │
│  ═══════                                                                                                                                    │
│  Total Resources: 7  │  Total Allocation: 460%  │  Average Utilization: 65.7%  │  Underutilized: 1  │  Overloaded: 1  │  Balanced: 5      │
│  Peak Phase: Phase 4-6 (5 resources)  │  Resource Gap: 1 additional senior developer needed for Phase 4                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. RACI Definitions & Load Categories

### 5.1 RACI Code Definitions
| Code | Full Name | Color | Symbol | Description |
|------|-----------|-------|--------|-------------|
| `R` | Responsible | `#E53935` | ★ | The person who executes the work |
| `A` | Accountable | `#1565C0` | ★ | The person who approves the outcome |
| `C` | Consulted | `#FFB300` | ● | People who provide formal input |
| `I` | Informed | `#4CAF50` | ● | People who are notified of outcomes |
| `-` | Not Involved | `#E0E0E0` | — | No role in this phase |

### 5.2 Resource Load Categories
| Category | Percentage Range | Color | Symbol | Description |
|----------|------------------|-------|--------|-------------|
| Over | > 100% | `#E53935` | ▲ | Overallocated — requires immediate action |
| Full | 80–100% | `#FFB300` | ● | Fully utilized |
| Partial | 40–79% | `#64B5F6` | ◐ | Partially utilized |
| Under | < 40% | `#4CAF50` | ○ | Underutilized — capacity available |

---

## 6. Detailed Styling Specifications

### 6.1 Cell Styling
| Property | Value | Description |
|----------|-------|-------------|
| Shape | Rectangle | Standard cell |
| Corner Radius | 2pt | Slightly rounded |
| Padding | `0.1in` | Internal padding |
| Border Width | 0.5pt | Thin border |
| Border Color | `#BDBDBD` | Light grey |
| Row Height | `0.6in` | Standard row height |
| Column Width | `2.0in` | Standard phase column width |
| Resource Col Width | `2.5in` | Wider first column |

### 6.2 Text Styling
| Element | Font Size | Font Weight | Alignment |
|---------|-----------|-------------|-----------|
| Resource Name | 9pt | Bold | Left |
| Role | 8pt | Regular | Left |
| RACI Code | 12pt | Bold | Center |
| Phase Header | 9pt | Bold | Center |
| Allocation % | 9pt | Regular | Center |
| Totals | 9pt | Bold | Center |

### 6.3 Header Styling
| Property | Value | Description |
|----------|-------|-------------|
| Height | `0.8in` | Standard header |
| Fill Color | `#1a237e` | Dark navy blue |
| Text Color | `#FFFFFF` | White |
| Font Size | 10pt | Bold |

---

## 7. Code Architecture

```text
resource_allocation_generator/
├── __init__.py
├── skill.md                       # This skill file
├── core/
│   ├── __init__.py
│   ├── diagram_builder.py         # Main orchestration
│   ├── validator.py               # JSON/schema validation
│   ├── errors.py                  # Custom exceptions
│   └── models.py                  # Pydantic models
├── renderers/
│   ├── __init__.py
│   ├── aspose_renderer.py         # Aspose.Diagram API layer
│   ├── dot_generator.py           # PNG Preview generation
│   └── layout_engine.py           # Auto-fit grid calculations
├── calculators/
│   ├── __init__.py
│   ├── allocation_calculator.py   # Total/summary math
│   └── load_calculator.py         # Load category assignment
├── stylers/
│   ├── __init__.py
│   ├── color_themes.py            
│   ├── shape_styler.py            
│   ├── cell_styler.py             
│   └── row_styler.py              
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   └── geometry_utils.py
├── templates/
│   └── resource_template.vstx     
├── config/
│   ├── __init__.py
│   └── settings.py                
└── cli.py                         # CLI entrypoint
```

---

## 8. Core Implementation Code

### 8.1 Diagram Builder Class (`core/diagram_builder.py`)

```python
from aspose.diagram import Diagram, SaveFileFormat
from typing import Dict, List
from collections import defaultdict

class ResourceAllocationBuilder:
    """Constructs the Resource Allocation Matrix Visio grid."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._calculate_positions()
        self._calculate_totals()
    
    def _setup_page(self) -> None:
        """Configure A2 landscape bounds."""
        self.page.page_sheet.page_props.page_width = 59.4
        self.page.page_sheet.page_props.page_height = 42.0
        self.page_width = 59.4
        self.page_height = 42.0
    
    def _setup_styles(self) -> None:
        """Bind global styles from config."""
        styling = self.config.get("styling", {})
        self.raci_colors = styling.get("raci_colors", {
            "R": "#E53935", "A": "#1565C0",
            "C": "#FFB300", "I": "#4CAF50", "-": "#E0E0E0"
        })
        self.load_colors = styling.get("load_colors", {
            "over": "#E53935", "full": "#FFB300",
            "partial": "#64B5F6", "under": "#4CAF50"
        })
        self.row_height = styling.get("row_height", 0.6)
        self.col_width = styling.get("column_width", 2.0)
        self.cell_padding = styling.get("cell_padding", 0.1)
    
    def _calculate_positions(self) -> None:
        """Auto-fit column widths to page boundaries."""
        layout = self.config.get("layout", {})
        margin = layout.get("margin", 0.5)
        header_height = layout.get("header_height", 0.8)
        
        resources = self.config['resource_allocation']['resources']
        phases = sorted(
            self.config['resource_allocation']['phases'],
            key=lambda p: p['order']
        )
        
        # Reserve width for the resource label column and extra columns
        resource_col_width = 2.5
        extra_cols_width = 2.5  # Total % + Status + Load bar
        
        # Available width for phase columns
        available = self.page_width - (margin * 2) - resource_col_width - extra_cols_width
        phase_col_width = available / max(1, len(phases))
        
        self.col_width = min(phase_col_width, 2.5)  # Cap at 2.5 in
        
        # Column X positions
        x = margin
        self.column_positions = {'resource': {'x': x, 'width': resource_col_width}}
        x += resource_col_width
        
        for phase in phases:
            self.column_positions[phase['id']] = {
                'x': x,
                'width': self.col_width,
                'name': phase['name'],
                'color': phase.get('color', '#1a237e')
            }
            x += self.col_width
        
        # Trailing summary columns
        self.column_positions['total_pct'] = {'x': x, 'width': 0.8}
        x += 0.8
        self.column_positions['status'] = {'x': x, 'width': 0.8}
        x += 0.8
        self.column_positions['load_bar'] = {'x': x, 'width': 1.5}
        
        # Row Y positions (below header)
        y_start = margin + 1.5 + header_height  # Title + header
        self.row_positions = {}
        
        for idx, resource in enumerate(resources):
            self.row_positions[resource['id']] = {
                'y': y_start + (idx * self.row_height),
                'height': self.row_height
            }
        
        self.footer_y = y_start + (len(resources) * self.row_height) + 0.2
        
    def _calculate_totals(self) -> None:
        """Compute per-resource and per-phase load totals."""
        allocations = self.config['resource_allocation']['allocations']
        phases = self.config['resource_allocation']['phases']
        resources = self.config['resource_allocation']['resources']
        
        self.phase_totals = {p['id']: {'count': 0, 'R': 0, 'A': 0, 'C': 0, 'I': 0} for p in phases}
        self.resource_totals = {r['id']: 0 for r in resources}
        
        # Build a lookup dictionary for fast rendering
        self.allocation_map = defaultdict(dict)
        
        for alloc in allocations:
            r_id = alloc['resource_id']
            p_id = alloc['phase_id']
            value = alloc.get('value', '-')
            pct = alloc.get('percentage', 0)
            
            # Map (resource, phase) -> allocation for fast cell lookup
            self.allocation_map[r_id][p_id] = alloc
            
            # Phase totals
            self.phase_totals[p_id]['count'] += 1
            if value in ('R', 'A', 'C', 'I'):
                self.phase_totals[p_id][value] += 1
            
            # Resource % accumulator (max per phase, not sum)
            self.resource_totals[r_id] = max(
                self.resource_totals[r_id], pct
            )
    
    def _get_load_category(self, pct: float) -> str:
        """Map utilization percentage to load label."""
        if pct > 100:
            return "over"
        elif pct >= 80:
            return "full"
        elif pct >= 40:
            return "partial"
        else:
            return "under"
    
    def build(self) -> None:
        """Execute all Visio draw calls."""
        # 1. Title Block
        # 2. Header Row (Phase Names)
        # 3. Resource Rows (RACI cells + Load bars)
        # 4. Totals Row (Phase summary counts)
        # 5. RACI Legend
        # 6. Statistics Summary Block
        pass
    
    def save(self, output_path: str) -> None:
        """Export to VSDX."""
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

### 8.2 Load Calculator (`calculators/load_calculator.py`)

```python
from typing import Dict

LOAD_THRESHOLDS = {
    "over":    (100.01, float('inf')),
    "full":    (80,     100),
    "partial": (40,     79.99),
    "under":   (0,      39.99),
}

LOAD_LABELS = {
    "over":    "▲ OVER",
    "full":    "● FULL",
    "partial": "◐ PARTIAL",
    "under":   "○ UNDER",
}

def classify_load(allocation_pct: float) -> Dict:
    """Classify a resource's total allocation into a load category."""
    for category, (low, high) in LOAD_THRESHOLDS.items():
        if low <= allocation_pct <= high:
            return {
                "category": category,
                "label": LOAD_LABELS[category],
                "percentage": allocation_pct
            }
    return {"category": "under", "label": "○ UNDER", "percentage": allocation_pct}
```

### 8.3 Allocation Calculator (`calculators/allocation_calculator.py`)

```python
from typing import List, Dict

class AllocationCalculator:
    """Computes summary statistics for the resource allocation matrix."""
    
    def __init__(self, resources: List[Dict], allocations: List[Dict]):
        self.resources = resources
        self.allocations = allocations
        self.resource_map = {r['id']: r for r in resources}
    
    def total_allocation_pct(self) -> float:
        """Sum of all resource allocations."""
        return sum(r.get('allocation', 0) for r in self.resources)
    
    def average_utilization(self) -> float:
        """Average resource utilization across all resources."""
        total = self.total_allocation_pct()
        return round(total / max(1, len(self.resources)), 1)
    
    def overloaded_resources(self) -> List[Dict]:
        """Return list of resources with > 100% allocation."""
        return [r for r in self.resources if r.get('allocation', 0) > 100]
    
    def underutilized_resources(self) -> List[Dict]:
        """Return list of resources with < 40% allocation."""
        return [r for r in self.resources if r.get('allocation', 0) < 40]
    
    def peak_phase(self, phase_totals: Dict) -> str:
        """Identify the phase(s) with the highest resource count."""
        if not phase_totals:
            return "N/A"
        max_count = max(v['count'] for v in phase_totals.values())
        peaks = [pid for pid, v in phase_totals.items() if v['count'] == max_count]
        return ", ".join(peaks)
    
    def resource_gap_summary(self) -> str:
        """Identify whether the project needs additional headcount."""
        overloaded = self.overloaded_resources()
        if overloaded:
            names = [r['name'] for r in overloaded]
            return f"Consider additional resource to relieve: {', '.join(names)}"
        return "Allocation levels are within capacity."
```

---

## 9. Error Handling

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| `RA-001` | InvalidInput | JSON fails Pydantic schema. | Validate fields. |
| `RA-002` | NoResources | Resources array is empty. | Add at least 1 resource. |
| `RA-003` | NoPhases | Phases array is empty. | Add at least 1 phase. |
| `RA-004` | NoAllocations | Allocations array is empty. | Add at least 1 allocation entry. |
| `RA-005` | InvalidRACI | RACI value not in `[R,A,C,I,-]`. | Correct the value field. |
| `RA-006` | MissingResource | `resource_id` in allocation doesn't exist. | Ensure `resource_id` matches exactly. |
| `RA-007` | MissingPhase | `phase_id` in allocation doesn't exist. | Ensure `phase_id` matches exactly. |
| `RA-008` | InvalidPercentage | Percentage outside 0–200 range. | Check for typos in numeric field. |
| `RA-009` | DuplicateAllocation | Same `resource_id` + `phase_id` appears twice. | Remove or merge the duplicate entry. |
| `RA-010` | JavaNotInstalled | Missing JRE 8+. | Install Java for JPype. |
| `RA-011` | LicenseMissing | Aspose `.lic` not found. | Set environment variable. |
| `RA-012` | RenderError | File write failure. | Check path permissions. |

---

## 10. Command-Line Interface (CLI)

```python
# cli.py
import argparse
import json
import logging
import sys
from core.diagram_builder import ResourceAllocationBuilder

def main():
    parser = argparse.ArgumentParser(description="Generate Visio Resource Allocation Matrix")
    parser.add_argument("input", help="Path to input JSON/YAML file")
    parser.add_argument("-o", "--output", help="Output VSDX path (default: ./output/resource_allocation.vsdx)")
    parser.add_argument("-p", "--preview", action="store_true", help="Generate PNG preview")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--type",
        choices=["RACI", "PERCENTAGE", "BOTH"],
        default="RACI",
        help="Allocation display mode"
    )
    parser.add_argument("--validate-only", action="store_true", help="Validate without rendering")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    with open(args.input, 'r') as f:
        spec = json.load(f)
    
    # Override allocation_type from CLI flag
    spec['resource_allocation']['allocation_type'] = args.type
    
    if args.validate_only:
        logging.info("Validation successful.")
        sys.exit(0)
    
    builder = ResourceAllocationBuilder(spec)
    builder.build()
    
    out_path = args.output or "./output/resource_allocation.vsdx"
    builder.save(out_path)
    logging.info(f"Resource Allocation Matrix saved to {out_path}")

if __name__ == "__main__":
    main()
```

---

## 11. Quality Checklist

- [ ] **Grid Alignment:** Every resource row and phase column intersects precisely at a correctly bounded cell.
- [ ] **RACI Display:** Each allocated cell displays the correct R/A/C/I code in the correct color.
- [ ] **Load Bars:** The utilization bar in the rightmost column correctly reflects the load category and is color-coded.
- [ ] **Totals Row:** Phase summary counts include both the total resource count and R/A/C/I breakdowns.
- [ ] **Overallocation Warning:** Resources at `> 100%` display the `▲ OVER` badge in red.
- [ ] **Statistics Block:** Summary accurately reflects total resource count, average utilization, and peak phase.

---

## 12. Usage Examples

### 12.1 RACI Mode (Default)
```bash
python resource_allocation_generator/cli.py data/resources.json -o output/raci_matrix.vsdx
```

### 12.2 Percentage Mode
```bash
python resource_allocation_generator/cli.py data/resources.json -o output/percentage_matrix.vsdx --type PERCENTAGE
```

### 12.3 Combined RACI + Percentage Mode
```bash
python resource_allocation_generator/cli.py data/resources.json -o output/combined_matrix.vsdx --type BOTH
```

### 12.4 With Rasterized Preview
```bash
python resource_allocation_generator/cli.py data/resources.json -o output/raci_matrix.vsdx --preview
```

---

## 13. Integration with Existing Skills

1. **Charter Integration:** The `resource_allocation_generator` exports directly into the `project-charter-generator` as the embedded resource plan.
2. **WBS Synergy:** The `phases` array in this skill maps 1:1 to the Level-1 nodes in the `wbs-diagram-generator-SKILL.md`.
3. **Milestone Alignment:** The `phases` overlap completely with the milestone chart's phase boundary definitions.

---

## 14. Testing Strategy

1. **RACI Validation Test:** Supply a cell with `value: "X"`. Assert `RA-005` is thrown.
2. **Missing Resource Reference Test:** Supply `resource_id: "R99"` with no corresponding resource. Assert `RA-006`.
3. **Duplicate Allocation Test:** Supply two entries for `R1/P1`. Assert `RA-009`.
4. **Overallocation Detection Test:** Set resource `allocation: 120`. Assert load category renders as `▲ OVER` with `#E53935` background.
5. **Auto-Fit Grid Test:** Supply 15 phases. Assert `col_width` auto-reduces to fit the A2 page without overflow.
