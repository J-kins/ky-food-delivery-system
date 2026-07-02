---
name: milestone-chart-generator
description: Generate professional Milestone Charts in fully editable Visio format (.vsdx) using Aspose.Diagram for Python. Maps project phases and key milestones along a horizontal chronological timeline.
---

# Milestone Chart Generator Skill

This production-grade skill generates **Milestone Charts** in Microsoft Visio (`.vsdx`) format. Unlike a standard Gantt Chart that tracks durations of specific tasks, a Milestone Chart focuses on major project events, deliverables, and decision points mapped across a timeline. Utilizing `Aspose.Diagram for Python` combined with `python-dateutil`, it dynamically calculates chronological positions, places milestone diamond markers, generates phase-grouped timeline bands, and highlights the project's critical path milestones.

This tool functions as a standalone capability or as an integrated sub-component of the broader `project-charter-generator`.

## Table of Contents
1. Core Output Specifications
2. Environment Setup & Dependencies
3. Input Specification (JSON/YAML Schema)
4. Milestone Chart Visual Layout (ASCII Blueprint)
5. Milestone Categories and Colors
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

The primary purpose of this skill is to generate a complete Milestone Chart that guarantees:
1. **Chronological Timeline:** A precisely calculated horizontal axis displaying months and years.
2. **Phase Groupings:** Colored horizontal bands demarcating the duration of high-level project phases (e.g., Initiation, Design, Development).
3. **Milestone Markers:** Diamond-shaped nodes representing exact milestone dates, connected to the timeline.
4. **Critical Path Emphasis:** Distinct visual styling (e.g., stars or red coloring) for milestones deemed "critical".
5. **Detailed Legend & Tables:** An automated data table listing the exact dates, categories, and descriptions of every milestone, alongside a critical milestone summary.
6. **Professional Styling:** Fully editable, corporate-themed Microsoft Visio shapes (`.vsdx`).

---

## 2. Environment Setup & Dependencies

### 2.1 Python Requirements
The generator relies heavily on robust date manipulation.
```text
python >= 3.10
aspose-diagram-python >= 24.0.0
python-dotenv >= 1.0.0
pyyaml >= 6.0
pillow >= 10.0.0
typing-extensions >= 4.0.0
pydantic >= 2.0.0
dateutil >= 2.8.0
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
pip install aspose-diagram-python python-dotenv pyyaml pillow pydantic python-dateutil
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

The generator enforces a strict schema requiring both `phases` (for top-level timeline groupings) and `milestones` (for specific dates).

```json
{
  "milestone_chart": {
    "title": "Milestone Chart - Project Schedule",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    "start_date": "2026-01-01",
    "end_date": "2027-03-15",
    "description": "Key project milestones and deliverables",
    
    "phases": [
      {
        "id": "P1",
        "name": "Initiation",
        "start": "2026-01-01",
        "end": "2026-02-28",
        "color": "#1a237e",
        "text_color": "#FFFFFF"
      },
      {
        "id": "P2",
        "name": "Requirements",
        "start": "2026-03-01",
        "end": "2026-05-15",
        "color": "#2E7D32",
        "text_color": "#FFFFFF"
      },
      {
        "id": "P3",
        "name": "Design",
        "start": "2026-05-16",
        "end": "2026-06-15",
        "color": "#E65100",
        "text_color": "#FFFFFF"
      },
      {
        "id": "P4",
        "name": "Development",
        "start": "2026-06-16",
        "end": "2026-09-30",
        "color": "#6A1B9A",
        "text_color": "#FFFFFF"
      },
      {
        "id": "P5",
        "name": "Testing",
        "start": "2026-10-01",
        "end": "2026-11-15",
        "color": "#C62828",
        "text_color": "#FFFFFF"
      },
      {
        "id": "P6",
        "name": "Deployment",
        "start": "2026-11-16",
        "end": "2026-12-15",
        "color": "#00838F",
        "text_color": "#FFFFFF"
      },
      {
        "id": "P7",
        "name": "Closure",
        "start": "2026-12-16",
        "end": "2027-02-28",
        "color": "#4E342E",
        "text_color": "#FFFFFF"
      }
    ],
    
    "milestones": [
      {
        "id": "M1",
        "name": "Project Charter Approved",
        "description": "Project charter signed off by sponsor",
        "date": "2026-01-15",
        "phase": "P1",
        "is_critical": true,
        "category": "Governance"
      },
      {
        "id": "M2",
        "name": "Project Plan Approved",
        "description": "Detailed project plan approved",
        "date": "2026-02-15",
        "phase": "P1",
        "is_critical": false,
        "category": "Governance"
      },
      {
        "id": "M3",
        "name": "Team Assembled",
        "description": "Full project team on board",
        "date": "2026-02-28",
        "phase": "P1",
        "is_critical": false,
        "category": "Resource"
      },
      {
        "id": "M4",
        "name": "Requirements Complete",
        "description": "SRS approved by all stakeholders",
        "date": "2026-05-15",
        "phase": "P2",
        "is_critical": true,
        "category": "Requirements"
      },
      {
        "id": "M5",
        "name": "Design Complete",
        "description": "SDD approved by architecture team",
        "date": "2026-06-15",
        "phase": "P3",
        "is_critical": true,
        "category": "Design"
      },
      {
        "id": "M6",
        "name": "Prototype Available",
        "description": "Working prototype for user testing",
        "date": "2026-07-31",
        "phase": "P4",
        "is_critical": false,
        "category": "Development"
      },
      {
        "id": "M7",
        "name": "Development Complete",
        "description": "Feature freeze - all code complete",
        "date": "2026-09-30",
        "phase": "P4",
        "is_critical": true,
        "category": "Development"
      },
      {
        "id": "M8",
        "name": "Testing Complete",
        "description": "All testing phases completed",
        "date": "2026-10-31",
        "phase": "P5",
        "is_critical": false,
        "category": "QA"
      },
      {
        "id": "M9",
        "name": "UAT Sign-off",
        "description": "User acceptance testing approved",
        "date": "2026-11-15",
        "phase": "P5",
        "is_critical": true,
        "category": "QA"
      },
      {
        "id": "M10",
        "name": "Go-Live",
        "description": "System deployed to production",
        "date": "2026-12-15",
        "phase": "P6",
        "is_critical": true,
        "category": "Deployment"
      },
      {
        "id": "M11",
        "name": "Operations Handover",
        "description": "Operations team takes over",
        "date": "2027-01-15",
        "phase": "P7",
        "is_critical": false,
        "category": "Transition"
      },
      {
        "id": "M12",
        "name": "Training Complete",
        "description": "All users trained",
        "date": "2027-02-15",
        "phase": "P7",
        "is_critical": false,
        "category": "Training"
      },
      {
        "id": "M13",
        "name": "Project Closure",
        "description": "Lessons learned and project closed",
        "date": "2027-02-28",
        "phase": "P7",
        "is_critical": true,
        "category": "Closure"
      },
      {
        "id": "M14",
        "name": "Final Report",
        "description": "Final project report submitted",
        "date": "2027-03-15",
        "phase": "P7",
        "is_critical": false,
        "category": "Closure"
      }
    ],
    
    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "critical_color": "#E53935",
      "phase_bar_height": 0.4,
      "milestone_size": 0.25,
      "show_critical_star": true,
      "show_phase_bands": true,
      "shadow_enabled": true
    },
    
    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "timeline_height": 4.0,
      "details_height": 3.0,
      "summary_height": 1.5
    }
  }
}
```

---

## 4. Milestone Chart Visual Layout (ASCII Blueprint)

**CRITICAL REQUIREMENT:** The Visio output must map the nodes precisely across the horizontal timeline in accordance with this structure.

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                         MILESTONE CHART - PROJECT SCHEDULE                                                                │
│                                                    Healthcare Ecosystem Project                                                                            │
│                                                    2026-01-01 to 2027-02-28                                                                                │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                                          │
│  PHASE 1               PHASE 2                PHASE 3                PHASE 4                PHASE 5                PHASE 6                PHASE 7      │
│  Initiation            Requirements           Design                 Development            Testing                Deployment             Closure      │
│  ████████████████████  ██████████████████████  ████████████████████   ██████████████████████  ████████████████████   ████████████████████   ██████████   │
│                                                                                                                                                          │
│         ★               ★                      ★                      ★                      ★                      ★                      ★            │
│         M1              M4                     M5                     M7                     M9                     M10                    M13           │
│         │               │                      │                      │                      │                      │                      │            │
│         │               │                      │                      │                      │                      │                      │            │
│         ▼               ▼                      ▼                      ▼                      ▼                      ▼                      ▼            │
│  ──────♦────────────────♦──────────────────────♦──────────────────────♦──────────────────────♦──────────────────────♦──────────────────────♦─────── │
│         │               │                      │                      │                      │                      │                      │            │
│         │               │                      │                      │                      │                      │                      │            │
│         │               │                      │                      │                      │                      │                      │            │
│   M2    M3              │                      │                      │                      │                      M12                   M14         │
│         │               │                      │                      │                      │                      │                      │            │
│         │               │                      │                      │                      │                      │                      │            │
│         ▼               ▼                      ▼                      ▼                      ▼                      ▼                      ▼            │
│  ──────♦───────────────♦──────────────────────♦──────────────────────♦──────────────────────♦──────────────────────♦──────────────────────♦─────── │
│         │               │                      │                      │                      │                      │                      │            │
│         │               M6                     M8                     M11                                                                              │
│         │               │                      │                      │                                                                                │
│         ▼               ▼                      ▼                      ▼                                                                                │
│  ──────♦───────────────♦──────────────────────♦──────────────────────♦────────────────────────────────────────────────────────────────────────────── │
│         │               │                      │                      │                                                                                │
│         │               │                      │                      │                                                                                │
│         ▼               ▼                      ▼                      ▼                                                                                │
│  JAN    FEB   MAR       APR   MAY   JUN        JUL   AUG   SEP        OCT   NOV   DEC        JAN   FEB   MAR        APR   MAY   JUN        JUL   AUG  │
│  2026   2026   2026     2026   2026   2026      2026   2026   2026      2026   2026   2026      2027   2027   2027      2027   2027   2027      2027   2027 │
│                                                                                                                                                          │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  MILESTONE DETAILS                                                                                                                                │ │
│  │  ═══════════════════                                                                                                                               │ │
│  │  ★  M1  Jan 15, 2026   Project Charter Approved                                                                                                  │ │
│  │     M2  Feb 15, 2026   Project Plan Approved                                                                                                      │ │
│  │     M3  Feb 28, 2026   Team Fully Assembled                                                                                                       │ │
│  │  ★  M4  May 15, 2026   Requirements Complete (SRS Approved)                                                                                     │ │
│  │  ★  M5  Jun 15, 2026   Design Complete (SDD Approved)                                                                                           │ │
│  │     M6  Jul 31, 2026   Working Prototype Available                                                                                                │ │
│  │  ★  M7  Sep 30, 2026   Development Complete (Feature Freeze)                                                                                    │ │
│  │     M8  Oct 31, 2026   All Testing Completed                                                                                                      │ │
│  │  ★  M9  Nov 15, 2026   UAT Sign-off Received                                                                                                    │ │
│  │  ★  M10 Dec 15, 2026   System Go-Live / Production Deployment                                                                                   │ │
│  │     M11 Jan 15, 2027   Operations Handover Complete                                                                                              │ │
│  │     M12 Feb 15, 2027   Training Complete                                                                                                         │ │
│  │  ★  M13 Feb 28, 2027   Project Closure / Lessons Learned                                                                                        │ │
│  │     M14 Mar 15, 2027   Final Report Submitted                                                                                                    │ │
│  │                                                                                                                                                    │ │
│  │  Critical Milestones Summary:                                                                                                                    │ │
│  │  ═══════════════════════════                                                                                                                     │ │
│  │  ★ M1  Charter Approved          ★ M4  Requirements Complete          ★ M5  Design Complete                                                     │ │
│  │  ★ M7  Development Complete       ★ M9  UAT Sign-off                  ★ M10 Go-Live                                                             │ │
│  │  ★ M13 Project Closure                                                                                                                                 │
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Milestone Categories and Colors

To visually track themes, categories dictate milestone base colors (unless overridden by Critical Status).

| Category | Color | Symbol | Description |
|----------|-------|--------|-------------|
| Governance | `#1a237e` | ★ | Strategic/Decision milestones |
| Requirements | `#2E7D32` | ● | Requirements-related milestones |
| Design | `#E65100` | ● | Design-related milestones |
| Development | `#6A1B9A` | ● | Development-related milestones |
| QA | `#C62828` | ● | Quality/testing milestones |
| Deployment | `#00838F` | ● | Deployment-related milestones |
| Transition | `#4E342E` | ● | Handover/transition milestones |
| Closure | `#4E342E` | ★ | Project closure milestones |

---

## 6. Detailed Styling Specifications

### 6.1 Timeline Styling
| Property | Value | Description |
|----------|-------|-------------|
| Line Color | `#333333` | Dark grey timeline |
| Line Width | 2pt | Thick horizontal spine |
| Month Labels | 8pt, Regular | Month names below the timeline |
| Year Labels | 8pt, Bold | Year labels placed below month names |
| Phase Bands | `0.4in` height | Colored bars spanning duration at the top |
| Phase Labels | 8pt, Bold | Phase names embedded in bands |

### 6.2 Milestone Styling
| Property | Normal | Critical | Description |
|----------|--------|----------|-------------|
| Shape | Diamond | Diamond / Star | Connector points on timeline |
| Size | `0.25in` | `0.3in` | Emphasize critical path |
| Fill Color | `#FFB300` | `#E53935` | Amber / Red |
| Border Color | `#E65100` | `#B71C1C` | Orange / Dark Red |
| Border Width | 1.5pt | 2pt | Thicker |
| Shadow | Enabled | Enabled | Drop shadow |
| Label | Below | Below | Vertical callouts |
| Text Color | `#333333` | `#E53935` | Contrast text |

### 6.3 Phase Band Styling
| Property | Value | Description |
|----------|-------|-------------|
| Height | `0.4in` | Uniform track height |
| Fill Color | Varies by phase | Passed from JSON `color` field |
| Text Color | `#FFFFFF` | Contrasting white |
| Font Size | 8pt | Small |
| Corner Radius | 2pt | Smooth edges |

---

## 7. Code Architecture

```text
milestone_chart_generator/
├── __init__.py
├── skill.md                       # This skill file
├── core/
│   ├── __init__.py
│   ├── diagram_builder.py         # Main orchestration & layout
│   ├── validator.py               # Input validation (Date ranges)
│   ├── errors.py                  # Custom exceptions
│   └── models.py                  # Pydantic schema models
├── renderers/
│   ├── __init__.py
│   ├── aspose_renderer.py         # Visio shape abstractions
│   ├── dot_generator.py           # PNG Preview generation
│   └── layout_engine.py           # Collision detection logic
├── calculators/
│   ├── __init__.py
│   ├── timeline_calculator.py     # Date-to-pixels math
│   └── milestone_calculator.py    # Offset generation for callouts
├── stylers/
│   ├── __init__.py
│   ├── color_themes.py            
│   ├── shape_styler.py            
│   ├── phase_styler.py            
│   └── milestone_styler.py        
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   └── date_utils.py              # Month/Year spanning math
├── templates/
│   └── milestone_template.vstx    # Base stencil library
├── config/
│   ├── __init__.py
│   └── settings.py                
└── cli.py                         # Argument parser
```

---

## 8. Core Implementation Code

### 8.1 Diagram Builder Class (`core/diagram_builder.py`)

```python
from aspose.diagram import Diagram, SaveFileFormat
from typing import List, Dict
from datetime import datetime, timedelta

class MilestoneChartBuilder:
    """Main class for building Visio Milestone Charts via chronological mapping."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._calculate_timeline()
        self._calculate_positions()
    
    def _setup_page(self) -> None:
        """Configure A2 landscape bounding box."""
        layout = self.config.get("layout", {})
        orientation = layout.get("orientation", "landscape")
        page_size = layout.get("page_size", "A2")
        
        # A2 Landscape default
        width, height = 59.4, 42.0 
        
        self.page.page_sheet.page_props.page_width = width
        self.page.page_sheet.page_props.page_height = height
        
        self.page_width = width
        self.page_height = height
    
    def _setup_styles(self) -> None:
        """Initialize global chart parameters."""
        styling = self.config.get("styling", {})
        self.theme = styling.get("theme", "enterprise_blue")
        self.critical_color = styling.get("critical_color", "#E53935")
        self.phase_bar_height = styling.get("phase_bar_height", 0.4)
        self.milestone_size = styling.get("milestone_size", 0.25)
    
    def _calculate_timeline(self) -> None:
        """Calculate geometric pixel mapping for chronological span."""
        chart_data = self.config.get('milestone_chart', {})
        start_str = chart_data.get('start_date', '2026-01-01')
        end_str = chart_data.get('end_date', '2027-12-31')
        
        self.start_date = datetime.strptime(start_str, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_str, "%Y-%m-%d")
        
        self.total_days = (self.end_date - self.start_date).days + 1
        
        margin = self.config.get("layout", {}).get("margin", 0.5)
        # Allocate width with padding
        self.timeline_width = self.page_width - (margin * 2) - 1.0
        self.day_width = self.timeline_width / max(1, self.total_days)
        
        self.months = self._get_month_positions()
    
    def _get_month_positions(self) -> List[Dict]:
        """Group timeline into month boundaries."""
        months = []
        current = self.start_date
        while current <= self.end_date:
            month_start = current
            if current.month == 12:
                next_month = datetime(current.year + 1, 1, 1)
            else:
                next_month = datetime(current.year, current.month + 1, 1)
                
            month_end = next_month - timedelta(days=1)
            
            days_from_start = (current - self.start_date).days
            x_pos = days_from_start * self.day_width
            
            months.append({
                'year': current.year,
                'month': current.month,
                'month_name': current.strftime('%b'),
                'year_label': str(current.year) if current.month == 1 else '',
                'x': x_pos,
                'width': ((month_end - month_start).days + 1) * self.day_width
            })
            current = next_month
        return months
    
    def _calculate_positions(self) -> None:
        """Determine X coordinates for phases and milestones."""
        margin = self.config.get("layout", {}).get("margin", 0.5)
        self.timeline_y = margin + 4.0 # Baseline height for timeline spine
        
        self.milestone_positions = {}
        self.phase_positions = {}
        
        # Phase grouping calculation
        for phase in self.config['milestone_chart'].get('phases', []):
            p_start = datetime.strptime(phase['start'], "%Y-%m-%d")
            p_end = datetime.strptime(phase['end'], "%Y-%m-%d")
            
            x_start = (p_start - self.start_date).days * self.day_width
            p_width = ((p_end - p_start).days + 1) * self.day_width
            
            self.phase_positions[phase['id']] = {
                'x': x_start,
                'width': p_width
            }
            
        # Milestone pinning calculation
        for milestone in self.config['milestone_chart'].get('milestones', []):
            m_date = datetime.strptime(milestone['date'], "%Y-%m-%d")
            x_pos = (m_date - self.start_date).days * self.day_width
            
            self.milestone_positions[milestone['id']] = {
                'x': x_pos,
                'date': milestone['date']
            }
            
    def build(self) -> None:
        """Orchestrate Visio shape drawing."""
        # 1. Draw Title
        # 2. Draw Phase Bands
        # 3. Draw Timeline Spine
        # 4. Loop over milestones -> Draw Diamonds & Vertical Callout lines
        # 5. Draw the embedded tabular Data Section
        pass
        
    def save(self, output_path: str) -> None:
        """Export VSDX."""
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

---

## 9. Error Handling

Enforce chronological constraints and logical grouping with custom exceptions:

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| `MC-001` | InvalidInput | JSON fails Pydantic schema rules. | Validate required fields. |
| `MC-002` | NoPhases | Phases array is empty. | Add at least 1 Phase. |
| `MC-003` | NoMilestones | Milestones array is empty. | Add at least 1 Milestone. |
| `MC-004` | InvalidDateRange | Project `start_date` > `end_date`. | Ensure chronological flow. |
| `MC-005` | MilestoneOutsideRange | Milestone date exists prior to project start or after end. | Update milestone date or expand project boundaries. |
| `MC-006` | PhaseOverlap | Phases overlap on the timeline track. | Ensure sequential phase boundaries. |
| `MC-007` | DuplicateMilestoneID | Multiple milestones share an `id`. | Enforce unique alphanumeric IDs. |
| `MC-008` | JavaNotInstalled | Missing JRE 8+. | Install Java for `jpype`. |
| `MC-009` | LicenseMissing | Aspose `.lic` missing. | Pass environment variable. |
| `MC-010` | RenderError | Visio file write failed. | Check path write permissions. |

---

## 10. Command-Line Interface (CLI)

```python
# cli.py
import argparse
import json
import logging
import sys
from core.diagram_builder import MilestoneChartBuilder

def main():
    parser = argparse.ArgumentParser(description="Generate a Visio Milestone Chart")
    parser.add_argument("input", help="Path to input JSON/YAML file")
    parser.add_argument("-o", "--output", help="Output VSDX path (default: ./output/milestone_chart.vsdx)")
    parser.add_argument("-p", "--preview", action="store_true", help="Generate PNG preview")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--show-category", action="store_true", help="Append category legends")
    parser.add_argument("--validate-only", action="store_true", help="Validate date spans without drawing")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    with open(args.input, 'r') as f:
        spec = json.load(f)
        
    if args.validate_only:
        # Pydantic validation and date-boundary checks happen here
        logging.info("Validation successful.")
        sys.exit(0)
        
    builder = MilestoneChartBuilder(spec)
    builder.build()
    
    out_path = args.output or "./output/milestone_chart.vsdx"
    builder.save(out_path)
    logging.info(f"Milestone Chart saved to {out_path}")

if __name__ == "__main__":
    main()
```

---

## 11. Quality Checklist

Before finalizing output, verify:

- [ ] **Chronology:** `start_date` and `end_date` properly construct the geometric spine.
- [ ] **Data Mapping:** No milestones fall off the edge of the visible diagram.
- [ ] **Visual Distinction:** Critical Milestones (`is_critical: true`) render with distinct Red coloring and larger sizing (`0.3in`).
- [ ] **Phase Alignment:** The phase boxes successfully map their total duration above the milestone spine.
- [ ] **Legend Generation:** The text table correctly tabulates every milestone.
- [ ] **Text Overflow:** Vertical callout labels do not bleed into the timeline or adjacent markers (use collision offset logic if necessary).

---

## 12. Usage Examples

### 12.1 Standard Execution
```bash
python milestone_chart_generator/cli.py data/milestones.json -o output/Q3_milestones.vsdx
```

### 12.2 Rasterized Preview Mode
```bash
python milestone_chart_generator/cli.py data/milestones.json -o output/Q3_milestones.vsdx --preview
```

### 12.3 CI/CD Integration (Validation Only)
Ensures date formatting and logical bounds are sound without consuming Aspose rendering times.
```bash
python milestone_chart_generator/cli.py data/milestones.json --validate-only
```

---

## 13. Integration with Existing Skills

The Milestone Chart Generator complements other project management tools:
1. **Gantt Synergy:** Milestones defined here map accurately as zero-duration tasks inside the `gantt-chart-generator-SKILL.md`.
2. **Charter Embedding:** Automatically outputted by the main orchestrator (`project-charter-generator-SKILL.md`) for the executive summary section.

---

## 14. Testing Strategy

1. **Boundary Test:** Supply a milestone exactly on `start_date`. Assert X-coordinate maps precisely to left margin.
2. **OutOfBounds Test:** Supply a milestone dated prior to `start_date`. Assert exception `MC-005` is raised.
3. **Collision Test:** Supply two milestones on the exact same date. Assert that vertical callouts offset properly (e.g., one renders above the timeline, one below, to prevent text overlay).
4. **Phase Overlap Test:** Provide `Phase 1` ending Feb 28, and `Phase 2` starting Feb 15. Assert `MC-006` is thrown.
5. **Load Test:** Generate a chart containing > 50 milestones to verify Visio bounding box scaling logic.
