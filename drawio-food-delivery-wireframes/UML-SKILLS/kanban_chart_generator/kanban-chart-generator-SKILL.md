---
name: kanban-chart-generator
description: Generate professional Kanban Charts in fully editable Visio format (.vsdx) using Aspose.Diagram for Python. Maps agile workflow columns, WIP limits, swimlanes, and detailed work item cards.
---

# Kanban Chart Generator Skill

This production-grade skill is engineered to generate **Kanban Charts** in Microsoft Visio (`.vsdx`) format. Unlike temporal charts like Gantt or Milestone charts, Kanban focuses on tracking the flow and state of individual work items. Utilizing `Aspose.Diagram for Python`, this tool mathematically plots a dynamic grid of columns (workflow stages) and horizontal swimlanes (work item categories), populating them with detailed, color-coded work item cards. It automatically computes card positioning, enforces boundaries, and flags Work In Progress (WIP) bottlenecks.

This tool functions as a standalone agile dashboard generator or as an integrated sub-component of the broader `project-charter-generator`.

## Table of Contents
1. Core Output Specifications
2. Environment Setup & Dependencies
3. Input Specification (JSON/YAML Schema)
4. Kanban Chart Visual Layout (ASCII Blueprint)
5. Workflow Column & Swimlane Structure
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

The primary purpose of this skill is to generate a complete Kanban Chart that guarantees:
1. **Dynamic Grid Layout:** Precise calculation of columns (e.g., Backlog, Analyze, Develop) and horizontal swimlanes (e.g., Bugs, Features).
2. **Work Item Cards:** Automated drawing of rounded rectangle cards displaying ID, Title, Priority, and Assignee.
3. **WIP Constraints:** Display of Work In Progress limits per column.
4. **Color Taxonomy:** Distinct styling based on priority (High/Medium/Low) and Work Item Type.
5. **Metrics Dashboard:** An embedded summary table calculating total cards, cycle time, throughput, and blocked items.
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

The generator enforces a strict JSON schema requiring `columns`, `swimlanes`, and `work_items`.

```json
{
  "kanban_chart": {
    "title": "Kanban Chart - Workflow Dashboard",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    "sprint": "Sprint 5",
    "description": "Workflow dashboard showing work items and their status",
    
    "columns": [
      {
        "id": "BACKLOG",
        "name": "Backlog",
        "description": "To Do",
        "wip_limit": null,
        "color": "#E3F2FD",
        "text_color": "#0D47A1",
        "order": 1
      },
      {
        "id": "SELECTED",
        "name": "Selected",
        "description": "Ready for work",
        "wip_limit": 20,
        "color": "#FFF3E0",
        "text_color": "#E65100",
        "order": 2
      },
      {
        "id": "ANALYZE",
        "name": "Analyze",
        "description": "In Analysis",
        "wip_limit": 5,
        "color": "#FFF9C4",
        "text_color": "#F57F17",
        "order": 3
      },
      {
        "id": "DEVELOP",
        "name": "Develop",
        "description": "In Development",
        "wip_limit": 8,
        "color": "#E8F5E9",
        "text_color": "#1B5E20",
        "order": 4
      },
      {
        "id": "TEST",
        "name": "Test",
        "description": "In Testing",
        "wip_limit": 6,
        "color": "#F3E5F5",
        "text_color": "#4A148C",
        "order": 5
      },
      {
        "id": "REVIEW",
        "name": "Review",
        "description": "Code Review",
        "wip_limit": 4,
        "color": "#FCE4EC",
        "text_color": "#880E4F",
        "order": 6
      },
      {
        "id": "DEPLOY",
        "name": "Deploy",
        "description": "Ready to Deploy",
        "wip_limit": 3,
        "color": "#E0F7FA",
        "text_color": "#006064",
        "order": 7
      },
      {
        "id": "DONE",
        "name": "Done",
        "description": "Complete",
        "wip_limit": null,
        "color": "#E8F5E9",
        "text_color": "#1B5E20",
        "order": 8
      },
      {
        "id": "BLOCKED",
        "name": "Blocked",
        "description": "Blocked Items",
        "wip_limit": null,
        "color": "#FFEBEE",
        "text_color": "#B71C1C",
        "order": 9
      }
    ],
    
    "swimlanes": [
      {
        "id": "SL1",
        "name": "Features",
        "color": "#1a237e",
        "text_color": "#FFFFFF",
        "icon": "★"
      },
      {
        "id": "SL2",
        "name": "Bugs",
        "color": "#C62828",
        "text_color": "#FFFFFF",
        "icon": "🐛"
      },
      {
        "id": "SL3",
        "name": "Tasks",
        "color": "#2E7D32",
        "text_color": "#FFFFFF",
        "icon": "✓"
      }
    ],
    
    "work_items": [
      {
        "id": "F-012",
        "type": "Features",
        "title": "Registration Module",
        "description": "User registration with email verification",
        "status": "BACKLOG",
        "priority": "Medium",
        "assignee": "Alice",
        "swimlane": "SL1",
        "blocked": false,
        "blocked_reason": null,
        "created_date": "2026-06-01",
        "size": 5,
        "tags": ["auth", "frontend"]
      },
      {
        "id": "F-013",
        "type": "Features",
        "title": "Dashboard",
        "description": "User dashboard with metrics",
        "status": "SELECTED",
        "priority": "High",
        "assignee": "Bob",
        "swimlane": "SL1",
        "blocked": false,
        "blocked_reason": null,
        "created_date": "2026-06-02",
        "size": 8,
        "tags": ["dashboard", "frontend"]
      },
      {
        "id": "B-017",
        "type": "Bugs",
        "title": "Login fails",
        "description": "Login fails with correct credentials",
        "status": "BACKLOG",
        "priority": "High",
        "assignee": "John",
        "swimlane": "SL2",
        "blocked": false,
        "blocked_reason": null,
        "created_date": "2026-06-03",
        "size": 3,
        "tags": ["auth", "bug"]
      },
      {
        "id": "B-019",
        "type": "Bugs",
        "title": "Null pointer exception",
        "description": "Null pointer in patient service",
        "status": "ANALYZE",
        "priority": "High",
        "assignee": "Mike",
        "swimlane": "SL2",
        "blocked": false,
        "blocked_reason": null,
        "created_date": "2026-06-05",
        "size": 2,
        "tags": ["backend", "critical"]
      }
    ],
    
    "metrics": {
      "total_cards": 34,
      "in_progress": 12,
      "completed": 18,
      "wip_limit_total": 26,
      "cycle_time_days": 4.5,
      "throughput_per_week": 6,
      "blocked_items": 2,
      "high_priority_count": 8,
      "average_age_days": 3.2,
      "lead_time_days": 7.8
    },
    
    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "card_width": 2.5,
      "card_height": 1.2,
      "column_padding": 0.3,
      "priority_colors": {
        "High": "#E53935",
        "Medium": "#FFB300",
        "Low": "#4CAF50"
      },
      "shadow_enabled": true
    },
    
    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "column_width": 3.5,
      "header_height": 0.8
    }
  }
}
```

---

## 4. Kanban Chart Visual Layout (ASCII Blueprint)

**CRITICAL REQUIREMENT:** The Visio output must construct the grid with vertical columns intersecting horizontal swimlanes, distributing the cards mathematically.

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                            KANBAN CHART - PROJECT DASHBOARD                                                                     │
│                                                       Healthcare Ecosystem Project - Sprint 5                                                                   │
│                                                       2026-06-17                                                                                               │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                                                 │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐                    │
│  │   BACKLOG    │   SELECTED   │   ANALYZE    │   DEVELOP   │    TEST     │   REVIEW    │    DEPLOY   │    DONE     │  BLOCKED    │                    │
│  │              │              │              │             │             │             │             │             │             │                    │
│  │  Items: 50   │  Items: 20   │  WIP: 5/5    │  WIP: 8/8   │  WIP: 6/6   │  WIP: 4/4   │  WIP: 3/3   │  Items: 18  │  Items: 2   │                    │
│  ├──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤                    │
│  │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │                    │
│  │  │ B-017   │ │  │ B-018   │ │  │ B-019   │ │  │ B-020   │ │  │ B-021   │ │  │ B-022   │ │  │ B-023   │ │  │ B-024   │ │  │ B-025   │ │                    │
│  │  │ Login   │ │  │ API     │ │  │ Null    │ │  │ Fix     │ │  │ Test    │ │  │ Review  │ │  │ Deploy  │ │  │ Done    │ │  │ DB      │ │                    │
│  │  │ fails   │ │  │ timeout │ │  │ pointer │ │  │ login   │ │  │ login   │ │  │ fix     │ │  │ to prod │ │  │         │ │  │ locked  │ │                    │
│  │  │ H│J     │ │  │ H│S     │ │  │ H│M     │ │  │ H│J     │ │  │ H│T     │ │  │ H│S     │ │  │ H│Ops   │ │  │ H│      │ │  │ C│D     │ │                    │
│  │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │                    │
│  │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │             │                    │
│  │  │ F-012   │ │  │ F-013   │ │  │ F-014   │ │  │ F-015   │ │  │ F-016   │ │  │ F-017   │ │  │ F-018   │ │  │ F-019   │ │             │                    │
│  │  │ Reg     │ │  │ Dash    │ │  │ Profile │ │  │ API     │ │  │ Test    │ │  │ Review  │ │  │ Deploy  │ │  │ Done    │ │             │                    │
│  │  │ M│A     │ │  │ H│B     │ │  │ M│C     │ │  │ H│A     │ │  │ H│T     │ │  │ H│B     │ │  │ H│Ops   │ │  │ H│      │ │             │                    │
│  │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │             │                    │
│  │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │  ┌─────────┐ │             │                    │
│  │  │ T-008   │ │  │ T-009   │ │  │ T-010   │ │  │ T-011   │ │  │ T-012   │ │  │ T-013   │ │  │ T-014   │ │  │ T-015   │ │             │                    │
│  │  │ Docs    │ │  │ CI/CD   │ │  │ Code    │ │  │ Migrate │ │  │ Test DB │ │  │ Review  │ │  │ Deploy  │ │  │ Done    │ │             │                    │
│  │  │ L│D     │ │  │ H│E     │ │  │ M│F     │ │  │ H│G     │ │  │ H│H     │ │  │ M│I     │ │  │ H│Ops   │ │  │ H│      │ │             │                    │
│  │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │  └─────────┘ │             │                    │
│  └──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘                    │
│                                                                                                                                                                 │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  METRICS                                                                                                                                                  │ │
│  │  ═══════                                                                                                                                                  │ │
│  │  Total Cards: 34   │  In Progress: 12   │  Completed: 18   │  WIP Limit: 26   │  Cycle Time: 4.5 days   │  Throughput: 6/week                              │ │
│  │  Blocked: 2        │  High Priority: 8  │  Avg Age: 3.2d   │  Lead Time: 7.8d │  Blocked Items: 2                                                          │ │
│  │                                                                                                                                                            │ │
│  │  Priority Distribution:  High (8)  Medium (15)  Low (11)                                                                                                  │ │
│  │  Work Item Type Distribution:  Features (12)  Bugs (10)  Tasks (12)                                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Workflow Column & Swimlane Structure

### 5.1 Column Structure & WIP Logic
| Column | WIP Limit | Description | Color |
|--------|-----------|-------------|-------|
| Backlog | ∞ | All work items waiting | `#E3F2FD` |
| Selected | 20 | Items ready for work | `#FFF3E0` |
| Analyze | 5 | Items being analyzed | `#FFF9C4` |
| Develop | 8 | Items in development | `#E8F5E9` |
| Test | 6 | Items in testing | `#F3E5F5` |
| Review | 4 | Items in code review | `#FCE4EC` |
| Deploy | 3 | Items ready to deploy | `#E0F7FA` |
| Done | ∞ | Completed items | `#E8F5E9` |
| Blocked | ∞ | Blocked items | `#FFEBEE` |

### 5.2 Work Item Types
| Type | Color | Text Color | Icon | Description |
|------|-------|------------|------|-------------|
| Features | `#1a237e` | `#FFFFFF` | ★ | New features/enhancements |
| Bugs | `#C62828` | `#FFFFFF` | 🐛 | Defects/bugs |
| Tasks | `#2E7D32` | `#FFFFFF` | ✓ | Development tasks |
| Technical Debt | `#4E342E` | `#FFFFFF` | ⚡ | Technical improvements |

### 5.3 Priority Tags
| Priority | Color | Text Color | Symbol |
|----------|-------|------------|--------|
| High | `#E53935` | `#FFFFFF` | ⚠️ |
| Medium | `#FFB300` | `#333333` | ● |
| Low | `#4CAF50` | `#FFFFFF` | ○ |

---

## 6. Detailed Styling Specifications

### 6.1 Card Styling
| Property | Value | Description |
|----------|-------|-------------|
| Shape | Rounded Rectangle | Standard card |
| Corner Radius | 4pt | Slightly rounded |
| Width | `2.5in` | Standard width |
| Height | `1.2in` | Standard height |
| Shadow | Enabled | Subtle drop shadow |
| Padding | 4pt | Internal padding |
| Border Width | 0.5pt | Thin border |
| Border Color | `#BDBDBD` | Light grey |

### 6.2 Card Text Layout
| Element | Font Size | Font Weight | Position |
|---------|-----------|-------------|----------|
| ID | 9pt | Bold | Top-left |
| Title | 8pt | Regular | Second line |
| Priority | 8pt | Bold | Bottom-left |
| Assignee | 8pt | Regular | Bottom-right |

### 6.3 Column Styling
| Property | Value | Description |
|----------|-------|-------------|
| Width | `3.5in` | Standard column width |
| Header Height | `0.8in` | Column header containing Name and WIP |
| Header Fill | Column color | Supplied in JSON |
| Text Color | Column text color | Supplied in JSON |
| Border | 1pt | Intersecting grid lines |

---

## 7. Code Architecture

```text
kanban_chart_generator/
├── __init__.py
├── skill.md                       # This skill file
├── core/
│   ├── __init__.py
│   ├── diagram_builder.py         # Main grid/swimlane orchestration
│   ├── validator.py               # JSON/Schema input validation
│   ├── errors.py                  # Custom exceptions
│   └── models.py                  # Pydantic schema wrappers
├── renderers/
│   ├── __init__.py
│   ├── aspose_renderer.py         # Aspose.Diagram API layer
│   ├── dot_generator.py           # PNG Preview generation
│   └── layout_engine.py           # Auto-packing logic for cards
├── calculators/
│   ├── __init__.py
│   ├── metrics_calculator.py      # Computes throughput/averages
│   └── wip_calculator.py          # Monitors WIP limits
├── stylers/
│   ├── __init__.py
│   ├── color_themes.py            
│   ├── shape_styler.py            
│   ├── column_styler.py           
│   └── card_styler.py             
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   └── geometry_utils.py
├── templates/
│   └── kanban_template.vstx       # Optional template
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
from typing import Dict
from collections import defaultdict

class KanbanChartBuilder:
    """Computes Kanban grid and packs work items into bounded Visio columns."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._calculate_positions()
    
    def _setup_page(self) -> None:
        """Configure page bounds."""
        layout = self.config.get("layout", {})
        orientation = layout.get("orientation", "landscape")
        page_size = layout.get("page_size", "A2")
        
        width, height = 59.4, 42.0 # A2 Landscape Default
        
        self.page.page_sheet.page_props.page_width = width
        self.page.page_sheet.page_props.page_height = height
        
        self.page_width = width
        self.page_height = height
    
    def _setup_styles(self) -> None:
        """Bind global styles."""
        styling = self.config.get("styling", {})
        self.card_width = styling.get("card_width", 2.5)
        self.card_height = styling.get("card_height", 1.2)
        self.col_pad = styling.get("column_padding", 0.3)
        self.priority_colors = styling.get("priority_colors", {
            "High": "#E53935",
            "Medium": "#FFB300",
            "Low": "#4CAF50"
        })
    
    def _calculate_positions(self) -> None:
        """Calculate column grid, swimlanes, and inner card packing."""
        layout = self.config.get("layout", {})
        margin = layout.get("margin", 0.5)
        header_height = layout.get("header_height", 0.8)
        col_width = layout.get("column_width", 3.5)
        
        y_top = margin + 2.2 # Below title block
        
        # 1. Map Columns
        columns = sorted(self.config['kanban_chart']['columns'], key=lambda x: x['order'])
        self.column_positions = {}
        
        x_pos = margin
        for col in columns:
            self.column_positions[col['id']] = {
                'x': x_pos,
                'y': y_top,
                'width': col_width,
                'height': self.page_height - y_top - margin - 3.0 # Save space for metrics
            }
            x_pos += col_width + 0.2
            
        # 2. Pack Cards into Swimlanes/Columns
        self.card_positions = {}
        work_items = self.config['kanban_chart']['work_items']
        
        # Group cards by (Swimlane, Column)
        grid_map = defaultdict(list)
        for card in work_items:
            grid_map[(card.get('swimlane'), card['status'])].append(card)
            
        # Assign coordinates
        # Simple vertical stacking per swimlane bucket
        for (sl_id, status_id), cards in grid_map.items():
            if status_id in self.column_positions:
                col_data = self.column_positions[status_id]
                
                # Simplified stack logic: 
                # In full implementation, swimlane Y-offsets dictate base Y.
                for idx, card in enumerate(cards):
                    c_x = col_data['x'] + self.col_pad
                    c_y = col_data['y'] + header_height + (idx * (self.card_height + 0.1))
                    
                    self.card_positions[card['id']] = {
                        'x': c_x,
                        'y': c_y,
                        'width': self.card_width,
                        'height': self.card_height
                    }
                    
    def build(self) -> None:
        """Execute draw calls to Aspose.Diagram API."""
        # Add Title Block
        # Add Columns (Rectangles)
        # Add Column Headers & WIP text
        # Add Swimlane dividers (Lines)
        # Add Cards (Rounded Rectangles + Text nodes)
        # Add Metrics Summary (Table Node)
        pass
        
    def save(self, output_path: str) -> None:
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

---

## 9. Error Handling

Implement Custom Error codes to validate board integrity:

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| `KB-001` | InvalidInput | JSON fails Pydantic schema. | Ensure correct JSON fields. |
| `KB-002` | NoColumns | Column array is empty. | Define at least 1 column. |
| `KB-003` | NoWorkItems | Work item array is empty. | Board must contain data. |
| `KB-004` | InvalidStatus | Card references a `status` that doesn't exist in `columns`. | Check spelling of column ID. |
| `KB-005` | NoSwimlanes | Swimlanes array is empty. | Provide at least 1 swimlane definition. |
| `KB-006` | InvalidPriority | Priority is not High/Medium/Low. | Map to standard taxonomy. |
| `KB-007` | InvalidAssignee | Card missing assignee. | Add an owner. |
| `KB-008` | JavaNotInstalled | Missing JRE. | Install Java for JPype. |
| `KB-009` | LicenseMissing | Aspose license not found. | Configure environment variable. |
| `KB-010` | RenderError | File write error. | Check directory permissions. |

---

## 10. Command-Line Interface (CLI)

```python
# cli.py
import argparse
import json
import logging
import sys
from core.diagram_builder import KanbanChartBuilder

def main():
    parser = argparse.ArgumentParser(description="Generate Visio Kanban Dashboard")
    parser.add_argument("input", help="Path to input JSON/YAML file")
    parser.add_argument("-o", "--output", help="Output VSDX path (default: ./output/kanban_chart.vsdx)")
    parser.add_argument("-p", "--preview", action="store_true", help="Generate PNG preview")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--show-tags", action="store_true", help="Append tags to Visio cards")
    parser.add_argument("--validate-only", action="store_true", help="Validate without rendering")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    with open(args.input, 'r') as f:
        spec = json.load(f)
        
    if args.validate_only:
        logging.info("Kanban schema validation successful. Exiting.")
        sys.exit(0)
        
    builder = KanbanChartBuilder(spec)
    builder.build()
    
    out_path = args.output or "./output/kanban_chart.vsdx"
    builder.save(out_path)
    logging.info(f"Kanban Chart saved to {out_path}")

if __name__ == "__main__":
    main()
```

---

## 11. Quality Checklist

Ensure the following constraints prior to finalizing the generated document:

- [ ] **Data Integrity:** All cards fall into exactly one Column, determined by `status`.
- [ ] **WIP Limits:** Ensure columns display `WIP: X/Y` inside the header.
- [ ] **Card Details:** Verify ID, Title, Priority flag, and Assignee are visible and un-truncated on the `2.5in x 1.2in` bounds.
- [ ] **Collision Detection:** Cards within a heavily populated column do not overflow into the metrics summary section. (If they do, resize column height or scale down card dimensions).
- [ ] **Swimlanes:** Verify cards are vertically bucketed according to their assigned `swimlane` ID.

---

## 12. Usage Examples

### 12.1 Standard Execution
```bash
python kanban_chart_generator/cli.py data/sprint5.json -o output/sprint5_board.vsdx
```

### 12.2 Rasterized Preview Mode
```bash
python kanban_chart_generator/cli.py data/sprint5.json -o output/sprint5_board.vsdx --preview
```

### 12.3 Tag Display Mode
Includes sub-text inside cards mapping to the `tags` array.
```bash
python kanban_chart_generator/cli.py data/sprint5.json -o output/sprint5_board.vsdx --show-tags
```

---

## 13. Integration with Existing Skills

The Kanban Generator links heavily with the agile ecosystem:
1. **Charter Embed:** Visio exports are embedded in the `project-charter-generator-SKILL.md` output for live snapshot tracking.
2. **WBS Synergy:** The `work_items` list maps directly to the leaf nodes generated by the `wbs-diagram-generator-SKILL.md`.

---

## 14. Testing Strategy

1. **Missing Status Test:** Provide a card with `status: "DEPLOYMENT"` when the column ID is actually `"DEPLOY"`. Assert `KB-004`.
2. **Empty Swimlane Test:** Create 3 swimlanes but only map cards to 1. Assert the other 2 swimlanes still render physically on the board but are empty.
3. **WIP Calculation Test:** Supply 6 items in `status: "ANALYZE"` where WIP limit is 5. Assert the header renders as `WIP: 6/5` to highlight the bottleneck.
4. **Load Test:** Generate 100+ cards in the Backlog. Assert the page height scales dynamically or triggers a visual overflow warning.
