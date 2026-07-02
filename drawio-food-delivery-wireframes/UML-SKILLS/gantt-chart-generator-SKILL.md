---
name: gantt-chart-generator
description: Generate enterprise-grade Gantt Charts as Visio (.vsdx) using Aspose.Diagram for Python. Renders phase-grouped task lists, timeline bars, milestones, dependencies, and progress overlays with consulting-quality styling per uml-diagram-generator-SKILL.md §11. Suitable for executive presentations, steering committees, and PMO dashboards.
---

# Gantt Chart Generator Skill

This production-grade skill generates **Gantt Charts** in Microsoft Visio (`.vsdx`) format. It turns structured JSON into project schedule visualizations with timeline mathematics, phase roll-ups, task hierarchy, dependency routing, milestones, and optional progress overlays.

Functions as a standalone deliverable or as a sub-component of `project-charter-generator`, `cpm-network-diagram-generator`, and `milestone-chart-generator`.

## Design Philosophy

Every output must be:

| Principle | Requirement |
|-----------|-------------|
| **Visually stunning** | Enterprise phase palette, clean grid, consistent branding |
| **Enterprise-ready** | Boardroom presentations and PMO dashboards |
| **Technically precise** | Proportional bars, correct dates, dependencies, milestones |
| **Programmatic** | Fully automated — no manual Visio tweaking |

**Design system authority:** Inherits mandatory standards from [`uml-diagram-generator-SKILL.md`](uml-diagram-generator-SKILL.md) §11 (page layout, typography, title block, legend, connector routing, QA). This skill adds Gantt-specific phase colors, task bars, and timeline grid styling.

## Table of Contents

1. Core Output Specifications
2. Professional Design Standards
3. Environment Setup & Dependencies
4. Input Specification (JSON/YAML Schema)
5. Gantt Chart Visual Layout (ASCII Blueprint)
6. Task Hierarchy & Level Definitions
7. Phase Color Palette
8. Code Architecture
9. Core Implementation
10. Error Handling
11. Command-Line Interface (CLI)
12. Quality Checklist
13. Usage Examples
14. Integration with Existing Skills
15. Testing Strategy
16. Troubleshooting Guide

---

## 1. Core Output Specifications

The primary purpose of this skill is to generate a complete Gantt Chart that guarantees:
1. **Task Hierarchy:** Proper indentation of Phases, Level 1, Level 2, and Level 3 tasks on the left-hand task list axis.
2. **Timeline Mathematics:** Accurate rendering of the X-axis mapping calendar days to physical inches to ensure proportional bar lengths.
3. **Bar Positioning:** Start and End dates correctly translated into X-coordinate offsets and bar widths.
4. **Milestones & Dependencies:** Diamond milestone markers mapped to specific dates, with orthogonal dependency lines (`Finish-to-Start`) dynamically routing between task bars.
5. **Phase Groupings:** Roll-up summary bars colored according to the phase palette.
6. **Professional Styling:** Enterprise-themed Visio output — title block `#1a237e`, phase-colored bars, amber milestones.

---

## 2. Professional Design Standards

### 2.1 Inherited Base Standards

Apply all settings from [`uml-diagram-generator-SKILL.md`](uml-diagram-generator-SKILL.md) §11:

- Page: **A2 landscape** (59.4 × 42.0 in), margin **0.5 cm**
- Font: **Arial** (9pt task list, 8pt timeline, 11pt title)
- Title block: `#1a237e` background, white text
- Connectors: orthogonal dependency routing
- QA: minimum `.vsdx` size ≥ 4 KB

### 2.2 Gantt Chart Styling Configuration

```yaml
gantt_chart_styling:
  page:
    size: "A2"
    orientation: "landscape"
    margin: 0.5
    background_color: "#FFFFFF"
    grid_enabled: true
    grid_color: "#F0F0F0"
    grid_spacing: "weeks"          # weeks | months | days

  phase_colors:
    initiation:    { fill: "#1565C0", light: "#E3F2FD", border: "#0D47A1" }
    requirements:  { fill: "#2E7D32", light: "#E8F5E9", border: "#1B5E20" }
    design:        { fill: "#E65100", light: "#FFF3E0", border: "#BF360C" }
    development:   { fill: "#6A1B9A", light: "#F3E5F5", border: "#4A148C" }
    testing:       { fill: "#C62828", light: "#FFEBEE", border: "#B71C1C" }
    deployment:    { fill: "#00838F", light: "#E0F7FA", border: "#006064" }
    closure:         { fill: "#4E342E", light: "#EFEBE9", border: "#3E2723" }

  task_list:
    width: 12.0                    # inches — left pane (implementation default)
    row_height: 0.6
    font_family: "Arial"
    font_size: 9
    indent_per_level: 0.5
    alternating_rows: { even: "#F8F9FA", odd: "#FFFFFF" }

  timeline:
    header_height: 0.8
    axis_fill: "#ECEFF1"
    axis_border: "#90A4AE"

  task_bar:
    height: 0.4
    corner_radius: 3
    progress_fill: "#2E7D32"       # overlay when 0 < completion < 100
    critical_fill: "#C62828"

  dependency:
    color: "#666666"
    width: 1.0
    types:
      FS: { color: "#1565C0", label: "FS" }
      SS: { color: "#2E7D32", label: "SS" }
      FF: { color: "#E65100", label: "FF" }
      SF: { color: "#6A1B9A", label: "SF" }

  milestone:
    fill: "#FFB300"
    stroke: "#E65100"
    size: 0.45

  title_block:
    height: 1.2
    background: "#1a237e"
    text_color: "#FFFFFF"

  legend:
    enabled: true
    position: "bottom"
    items: [task_bar, milestone, dependency, progress, critical_path]
```

### 2.3 Anti-Patterns (Do NOT)

- Non-proportional bar widths (must scale linearly with duration)
- Task names misaligned with bars on Y-axis
- Phase colors inconsistent between list and bars
- Using `aspose.diagram` import (use `asposediagram.api` via JPype)
- Accepting sub-4KB `.vsdx` as success
- Comic Sans or unlabeled colors

---

## 3. Environment Setup & Dependencies

### 3.1 Python Requirements
```text
python >= 3.10
aspose-diagram>=23.10.0
JPype1>=1.5.0
pydantic>=2.0.0
python-dotenv>=1.0.0
python-dateutil>=2.8.0
pyyaml>=6.0
```

### 3.2 System Dependencies

**Java Runtime Environment (JRE) 11+**
- Required for `Aspose.Diagram for Python` (JPype).

### 3.3 Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate on Unix/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Install dependencies
pip install aspose-diagram JPype1 pydantic python-dotenv python-dateutil pyyaml
```

### 3.4 Environment Variables (.env file)
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
DEFAULT_FONT_SIZE=9
```

---

## 4. Input Specification (JSON/YAML Schema)

The generator enforces a strict JSON input schema defining project constraints, nested phase/task arrays, milestones, and dependencies.

```json
{
  "gantt_chart": {
    "title": "Gantt Chart - Project Schedule",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    "start_date": "2026-01-01",
    "end_date": "2026-12-31",
    
    "phases": [
      {
        "id": "P1",
        "name": "Project Management",
        "description": "Overall project governance",
        "color": "#1565C0",
        "text_color": "#FFFFFF",
        "tasks": [
          {
            "id": "T1.1",
            "name": "Planning",
            "description": "Project planning",
            "start": "2026-01-01",
            "end": "2026-02-28",
            "completion": 100,
            "dependencies": [],
            "level": 1
          },
          {
            "id": "T1.1.1",
            "name": "Develop Charter",
            "description": "Create project charter",
            "start": "2026-01-01",
            "end": "2026-01-15",
            "completion": 100,
            "dependencies": [],
            "level": 2
          },
          {
            "id": "T1.1.2",
            "name": "Create Schedule",
            "description": "Develop project schedule",
            "start": "2026-01-16",
            "end": "2026-02-15",
            "completion": 100,
            "dependencies": ["T1.1.1"],
            "level": 2
          },
          {
            "id": "T1.1.3",
            "name": "Define Budget",
            "description": "Establish project budget",
            "start": "2026-01-16",
            "end": "2026-02-28",
            "completion": 100,
            "dependencies": ["T1.1.1"],
            "level": 2
          },
          {
            "id": "T1.2",
            "name": "Monitoring",
            "description": "Track project progress",
            "start": "2026-03-01",
            "end": "2026-04-30",
            "completion": 50,
            "dependencies": ["T1.1"],
            "level": 1
          },
          {
            "id": "T1.3",
            "name": "Reporting",
            "description": "Status reporting",
            "start": "2026-04-01",
            "end": "2026-05-31",
            "completion": 25,
            "dependencies": ["T1.1"],
            "level": 1
          }
        ]
      },
      {
        "id": "P2",
        "name": "Requirements Engineering",
        "description": "Gather and document requirements",
        "color": "#2E7D32",
        "text_color": "#FFFFFF",
        "tasks": [
          {
            "id": "T2.1",
            "name": "Elicitation",
            "description": "Gather requirements",
            "start": "2026-02-01",
            "end": "2026-03-31",
            "completion": 100,
            "dependencies": ["T1.1"],
            "level": 1
          },
          {
            "id": "T2.1.1",
            "name": "Stakeholder Interviews",
            "description": "Conduct interviews",
            "start": "2026-02-01",
            "end": "2026-02-28",
            "completion": 100,
            "dependencies": ["T1.1"],
            "level": 2
          },
          {
            "id": "T2.1.2",
            "name": "Questionnaires",
            "description": "Design and distribute surveys",
            "start": "2026-02-01",
            "end": "2026-03-15",
            "completion": 100,
            "dependencies": ["T1.1"],
            "level": 2
          },
          {
            "id": "T2.1.3",
            "name": "Workshops",
            "description": "Facilitate workshops",
            "start": "2026-03-01",
            "end": "2026-03-31",
            "completion": 100,
            "dependencies": ["T2.1.1"],
            "level": 2
          },
          {
            "id": "T2.2",
            "name": "Analysis",
            "description": "Analyze requirements",
            "start": "2026-03-15",
            "end": "2026-04-30",
            "completion": 75,
            "dependencies": ["T2.1"],
            "level": 1
          },
          {
            "id": "T2.3",
            "name": "Specification",
            "description": "Document requirements",
            "start": "2026-04-01",
            "end": "2026-05-15",
            "completion": 50,
            "dependencies": ["T2.2"],
            "level": 1
          }
        ]
      },
      {
        "id": "P3",
        "name": "System Design",
        "description": "Design the system",
        "color": "#E65100",
        "text_color": "#FFFFFF",
        "tasks": [
          {
            "id": "T3.1",
            "name": "Database Design",
            "description": "Design database schema",
            "start": "2026-03-01",
            "end": "2026-04-30",
            "completion": 60,
            "dependencies": ["T2.3"],
            "level": 1
          },
          {
            "id": "T3.2",
            "name": "API Design",
            "description": "Design RESTful APIs",
            "start": "2026-04-01",
            "end": "2026-05-31",
            "completion": 40,
            "dependencies": ["T2.3"],
            "level": 1
          },
          {
            "id": "T3.3",
            "name": "UI/UX Design",
            "description": "Design user interface",
            "start": "2026-04-15",
            "end": "2026-06-15",
            "completion": 30,
            "dependencies": ["T2.3"],
            "level": 1
          }
        ]
      },
      {
        "id": "P4",
        "name": "Development",
        "description": "Build the system",
        "color": "#6A1B9A",
        "text_color": "#FFFFFF",
        "tasks": [
          {
            "id": "T4.1",
            "name": "Backend Development",
            "description": "Build backend services",
            "start": "2026-05-01",
            "end": "2026-07-31",
            "completion": 20,
            "dependencies": ["T3.1", "T3.2"],
            "level": 1
          },
          {
            "id": "T4.2",
            "name": "Frontend Development",
            "description": "Build user interfaces",
            "start": "2026-06-01",
            "end": "2026-08-31",
            "completion": 15,
            "dependencies": ["T3.3"],
            "level": 1
          },
          {
            "id": "T4.3",
            "name": "Integration",
            "description": "Integrate external systems",
            "start": "2026-07-01",
            "end": "2026-08-31",
            "completion": 10,
            "dependencies": ["T4.1"],
            "level": 1
          }
        ]
      },
      {
        "id": "P5",
        "name": "Testing",
        "description": "Validate system quality",
        "color": "#C62828",
        "text_color": "#FFFFFF",
        "tasks": [
          {
            "id": "T5.1",
            "name": "Unit Testing",
            "description": "Write and execute unit tests",
            "start": "2026-07-01",
            "end": "2026-08-31",
            "completion": 10,
            "dependencies": ["T4.1"],
            "level": 1
          },
          {
            "id": "T5.2",
            "name": "Integration Testing",
            "description": "Test integrated components",
            "start": "2026-08-01",
            "end": "2026-09-30",
            "completion": 0,
            "dependencies": ["T4.3"],
            "level": 1
          },
          {
            "id": "T5.3",
            "name": "System Testing",
            "description": "Full system validation",
            "start": "2026-09-01",
            "end": "2026-10-31",
            "completion": 0,
            "dependencies": ["T5.2"],
            "level": 1
          }
        ]
      },
      {
        "id": "P6",
        "name": "Deployment",
        "description": "Deploy and transition system",
        "color": "#00838F",
        "text_color": "#FFFFFF",
        "tasks": [
          {
            "id": "T6.1",
            "name": "Infrastructure",
            "description": "Setup infrastructure",
            "start": "2026-08-01",
            "end": "2026-09-15",
            "completion": 0,
            "dependencies": ["T4.3"],
            "level": 1
          },
          {
            "id": "T6.2",
            "name": "Deployment",
            "description": "Deploy application",
            "start": "2026-09-01",
            "end": "2026-10-15",
            "completion": 0,
            "dependencies": ["T6.1"],
            "level": 1
          },
          {
            "id": "T6.3",
            "name": "Cutover",
            "description": "Transition to operations",
            "start": "2026-10-01",
            "end": "2026-11-30",
            "completion": 0,
            "dependencies": ["T6.2"],
            "level": 1
          }
        ]
      }
    ],
    
    "milestones": [
      {
        "id": "M1",
        "name": "Charter Approved",
        "date": "2026-01-15",
        "description": "Project charter signed off"
      },
      {
        "id": "M2",
        "name": "Requirements Complete",
        "date": "2026-05-15",
        "description": "All requirements documented"
      },
      {
        "id": "M3",
        "name": "Design Complete",
        "date": "2026-06-15",
        "description": "All designs finalized"
      },
      {
        "id": "M4",
        "name": "Development Complete",
        "date": "2026-08-31",
        "description": "All development completed"
      },
      {
        "id": "M5",
        "name": "Testing Complete",
        "date": "2026-10-31",
        "description": "All testing completed"
      },
      {
        "id": "M6",
        "name": "Project Go-Live",
        "date": "2026-11-30",
        "description": "System is live"
      }
    ],
    
    "dependencies": [
      {
        "from": "T1.1.1",
        "to": "T1.1.2",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T1.1.1",
        "to": "T1.1.3",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T1.1",
        "to": "T2.1",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T2.1.1",
        "to": "T2.1.3",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T2.1",
        "to": "T2.2",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T2.2",
        "to": "T2.3",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T2.3",
        "to": "T3.1",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T2.3",
        "to": "T3.2",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T2.3",
        "to": "T3.3",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T3.1",
        "to": "T4.1",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T3.2",
        "to": "T4.1",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T3.3",
        "to": "T4.2",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T4.1",
        "to": "T4.3",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T4.1",
        "to": "T5.1",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T4.3",
        "to": "T5.2",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T5.2",
        "to": "T5.3",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T4.3",
        "to": "T6.1",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T6.1",
        "to": "T6.2",
        "type": "finish-to-start",
        "label": "FS"
      },
      {
        "from": "T6.2",
        "to": "T6.3",
        "type": "finish-to-start",
        "label": "FS"
      }
    ],
    
    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "header_height": 1.2,
      "task_row_height": 0.4,
      "timeline_height": 4.0,
      "show_percent_complete": true,
      "show_dependencies": true,
      "show_milestones": true,
      "shadow_enabled": true
    },
    
    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.3,
      "task_list_width": 6.0,
      "timeline_width": 18.0,
      "months_to_show": 12
    }
  }
}
```

---

## 5. Gantt Chart Visual Layout (ASCII Blueprint)

**CRITICAL REQUIREMENT:** The Visio layout engine mathematically scales dates linearly across the `timeline_width` to conform exactly to these spatial blueprints.

### 5.1 Enterprise Gantt Layout (Phase-Grouped)

**CRITICAL:** Dates scale linearly across the timeline width. Task rows align 1:1 with bars.

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    GANTT CHART - PROJECT SCHEDULE                                                           │
│              Healthcare Ecosystem - Development Timeline  │  Version 1.0  │  2026-06-17                                    │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  TASK LIST                          │ JAN │ FEB │ MAR │ APR │ MAY │ JUN │ JUL │ AUG │ SEP │ OCT │ NOV │ DEC │              │
│  ───────────────────────────────────│─────│─────│─────│─────│─────│─────│─────│─────│─────│─────│─────│─────│              │
│  PHASE 1: INITIATION (#1565C0)      │ ███ │ ███ │ ███ │     │     │     │     │     │     │     │     │     │              │
│  ├─ 1.1 Project Charter             │ ███ │     │     │     │     │     │     │     │     │     │     │     │              │
│  ├─ 1.2 Team Assembly               │     │ ███ │     │     │     │     │     │     │     │     │     │     │              │
│  └─ 1.4 Plan Approval               │     │     │ ███ │     │     │     │     │     │     │     │     │     │              │
│  PHASE 2: REQUIREMENTS (#2E7D32)    │     │ ███ │ ███ │ ███ │     │     │     │     │     │     │     │     │              │
│  ├─ 2.1 Elicitation                 │     │ ███ │ ███ │     │     │     │     │     │     │     │     │     │              │
│  └─ 2.3 Specification               │     │     │     │ ███ │     │     │     │     │     │     │     │     │              │
│  PHASE 3: DESIGN (#E65100)          │     │     │ ███ │ ███ │ ███ │     │     │     │     │     │     │     │              │
│  PHASE 4: DEVELOPMENT (#6A1B9A)     │     │     │     │ ███ │ ███ │ ███ │ ███ │ ███ │     │     │     │     │              │
│  PHASE 5: TESTING (#C62828)         │     │     │     │     │     │ ███ │ ███ │ ███ │ ███ │     │     │     │              │
│  PHASE 6: DEPLOYMENT (#00838F)     │     │     │     │     │     │     │     │     │ ███ │ ███ │ ███ │     │              │
│  PHASE 7: CLOSURE (#4E342E)          │     │     │     │     │     │     │     │     │     │     │ ███ │ ███ │ ███ │              │
│  MILESTONES                         │     │     │     │     │     │     │     │     │     │     │     │     │              │
│  ◆ M1: Charter Approved             │ ◆   │     │     │     │     │     │     │     │     │     │     │     │              │
│  ◆ M2: Requirements Complete        │     │     │ ◆   │     │     │     │     │     │     │     │     │     │              │
│  ◆ M6: Go-Live                      │     │     │     │     │     │     │     │     │     │ ◆   │     │     │              │
│  ───────────────────────────────────│─────│─────│─────│─────│─────│─────│─────│─────│─────│─────│─────│─────│              │
│  LEGEND: ███ Task  ◆ Milestone  → Dependency  ▓ Progress overlay  ■ Critical (#C62828)                                      │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Layout regions:**

| Region | Width | Content |
|--------|-------|---------|
| Title block | Full width top | `#1a237e` — title, project, version, date |
| Task list (left) | 12 in | Phase headers + indented tasks |
| Timeline (right) | Remaining | Month/week grid + bars + milestones |
| Legend | Bottom | Symbols used in diagram |

### 5.2 Detailed Phase-Grouped Layout (Reference)
```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                      GANTT CHART                                                         │
│                                                    Project Schedule                                                      │
│                                                2026-01-01 to 2026-12-31                                                  │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  TASKS                       │  JAN  │  FEB  │  MAR  │  APR  │  MAY  │  JUN  │  JUL  │  AUG  │  SEP  │  OCT  │  NOV  │  DEC  │
│──────────────────────────────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│
│  Project Management          │  ████  │  ████  │  ████  │       │       │       │       │       │       │       │       │       │
│   ├─ 1.1 Planning            │  ████  │  ████  │       │       │       │       │       │       │       │       │       │       │
│   │   ├─ Charter             │  ████  │       │       │       │       │       │       │       │       │       │       │       │
│   │   ├─ Schedule            │       │  ████  │       │       │       │       │       │       │       │       │       │       │
│   │   └─ Budget              │       │  ████  │       │       │       │       │       │       │       │       │       │       │
│   ├─ 1.2 Monitoring          │       │       │  ████  │  ████  │       │       │       │       │       │       │       │       │
│   └─ 1.3 Reporting           │       │       │       │  ████  │  ████  │       │       │       │       │       │       │       │
│──────────────────────────────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│
│  Requirements Engineering   │       │  ████  │  ████  │  ████  │       │       │       │       │       │       │       │       │
│   ├─ 2.1 Elicitation        │       │  ████  │  ████  │       │       │       │       │       │       │       │       │       │
│   │   ├─ Interviews         │       │  ████  │       │       │       │       │       │       │       │       │       │       │
│   │   ├─ Questionnaires     │       │  ████  │       │       │       │       │       │       │       │       │       │       │
│   │   └─ Workshops          │       │       │  ████  │       │       │       │       │       │       │       │       │       │
│   ├─ 2.2 Analysis           │       │       │  ████  │  ████  │       │       │       │       │       │       │       │       │
│   └─ 2.3 Specification      │       │       │       │  ████  │       │       │       │       │       │       │       │       │
│──────────────────────────────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│
│  System Design              │       │       │  ████  │  ████  │  ████  │       │       │       │       │       │       │       │
│   ├─ 3.1 Database Design    │       │       │  ████  │  ████  │       │       │       │       │       │       │       │       │
│   ├─ 3.2 API Design         │       │       │       │  ████  │  ████  │       │       │       │       │       │       │       │
│   └─ 3.3 UI/UX Design       │       │       │       │  ████  │  ████  │       │       │       │       │       │       │       │
│──────────────────────────────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│
│  Development                │       │       │       │  ████  │  ████  │  ████  │  ████  │       │       │       │       │       │
│   ├─ 4.1 Backend            │       │       │       │  ████  │  ████  │  ████  │       │       │       │       │       │       │
│   ├─ 4.2 Frontend           │       │       │       │       │  ████  │  ████  │  ████  │       │       │       │       │       │
│   └─ 4.3 Integration        │       │       │       │       │       │  ████  │  ████  │       │       │       │       │       │
│──────────────────────────────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│
│  Testing                    │       │       │       │       │       │  ████  │  ████  │  ████  │       │       │       │       │
│   ├─ 5.1 Unit Testing       │       │       │       │       │       │  ████  │  ████  │       │       │       │       │       │
│   ├─ 5.2 Integration Tests  │       │       │       │       │       │       │  ████  │  ████  │       │       │       │       │
│   └─ 5.3 System Testing     │       │       │       │       │       │       │       │  ████  │       │       │       │       │
│──────────────────────────────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│
│  Deployment                 │       │       │       │       │       │       │       │  ████  │  ████  │       │       │       │
│   ├─ 6.1 Infrastructure     │       │       │       │       │       │       │       │  ████  │       │       │       │       │
│   ├─ 6.2 Deployment         │       │       │       │       │       │       │       │  ████  │       │       │       │       │
│   └─ 6.3 Cutover            │       │       │       │       │       │       │       │       │  ████  │       │       │       │
│──────────────────────────────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│
│  MILESTONES                  │       │       │       │       │       │       │       │       │       │       │       │       │
│  ● M1: Charter Approved     │  ◆    │       │       │       │       │       │       │       │       │       │       │       │
│  ● M2: Requirements Done    │       │       │  ◆    │       │       │       │       │       │       │       │       │       │
│  ● M3: Design Complete      │       │       │       │       │  ◆    │       │       │       │       │       │       │       │
│  ● M4: Development Done     │       │       │       │       │       │       │       │  ◆    │       │       │       │       │
│  ● M5: Testing Complete     │       │       │       │       │       │       │       │       │  ◆    │       │       │       │
│  ● M6: Project Go-Live      │       │       │       │       │       │       │       │       │       │  ◆    │       │       │
│──────────────────────────────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│───────│
│  DEPENDENCIES                │       │       │       │       │       │       │       │       │       │       │       │       │
│  Charter → Planning         │  ─────┼───────│       │       │       │       │       │       │       │       │       │       │
│  Requirements → Design      │       │       │  ─────┼───────│       │       │       │       │       │       │       │       │
│  Design → Development       │       │       │       │       │  ─────┼───────│       │       │       │       │       │       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Task Hierarchy & Level Definitions

Task list indentation logic driven by the `level` property:

| Level | Indentation | Format | Example |
|-------|-------------|--------|---------|
| **Phase** | 0 spaces | BOLD, Colored bar background spanning the whole chart width | "PHASE 1: PROJECT MANAGEMENT" |
| **Level 1** | 2 spaces | Regular text | "├─ 1.1 Planning" |
| **Level 2** | 4 spaces | Regular text | "│ ├─ 1.1.1 Develop Charter" |
| **Level 3** | 6 spaces | Regular text | "│ │ └─ 1.1.1.1 Subtask" |

---

## 7. Phase Color Palette

Assign distinct visual domains per phase (Section 2.2). Implementation uses `phase.color` from input JSON. Full styling (bars, milestones, dependencies, legend) is defined in **Section 2.2**.

| Phase | Color Name | Hex Code | Text Color |
|-------|------------|----------|------------|
| Project Management | Blue | `#1565C0` | `#FFFFFF` |
| Requirements | Green | `#2E7D32` | `#FFFFFF` |
| System Design | Orange | `#E65100` | `#FFFFFF` |
| Development | Purple | `#6A1B9A` | `#FFFFFF` |
| Testing | Red | `#C62828` | `#FFFFFF` |
| Deployment | Teal | `#00838F` | `#FFFFFF` |
| Security *(if used)* | Dark Blue | `#1a237e` | `#FFFFFF` |
| Training *(if used)* | Amber | `#FF8F00` | `#333333` |

---

## 8. Code Architecture

```text
gantt_chart_generator/
├── __init__.py
├── cli.py                         # CLI entry point
├── PROMPT.md
├── requirements.txt
├── .env.example
├── config/
│   └── settings.py                # License, PAGE_SIZES_IN, apply_aspose_diagram_license()
├── core/
│   ├── gantt_builder.py           # build_gantt_chart() orchestrator + MIN_VSDX_BYTES QA
│   ├── diagram_builder.py         # GanttChartBuilder — draw pipeline
│   ├── validator.py               # validate_gantt() Pydantic validation
│   ├── models.py                  # GanttChartSpec, Phase, Task, Milestone models
│   └── errors.py                  # GanttError codes GC-001…GC-010
├── schedulers/
│   └── timeline_calculator.py     # date_to_x(), calculate_bar(), phase roll-up
├── renderers/
│   └── aspose_renderer.py         # JPype + asposediagram.api helpers
├── examples/
│   └── sample_input.json
└── scripts/
    └── run_example.py             # End-to-end smoke test
```

**Pipeline:** `cli.py` → `validate_gantt()` → `build_gantt_chart()` → `GanttChartBuilder.build()` → `asp.save_diagram()`.

---

## 9. Core Implementation

### 9.1 Orchestrator (`core/gantt_builder.py`)

```python
MIN_VSDX_BYTES = 4_000

def build_gantt_chart(spec_dict: Dict[str, Any], output_path: str) -> str:
    apply_aspose_diagram_license()
    spec = validate_gantt(spec_dict)
    builder = GanttChartBuilder(spec.gantt_chart.model_dump())
    builder.build()
    builder.save(output_path)
    if Path(output_path).stat().st_size < MIN_VSDX_BYTES:
        raise RuntimeError(f"Gantt chart too small: {output_path}")
    return output_path
```

### 9.2 Timeline Calculator (`schedulers/timeline_calculator.py`)

Maps calendar dates to physical X coordinates on an A2 landscape page:

```python
class TimelineCalculator:
    def __init__(self, config: Dict[str, Any]):
        self.left_pane_width = 12.0
        self.chart_width = self.total_width - self.left_pane_width - (2 * self.margin)
        self.pixels_per_day = self.chart_width / self.total_days

    def date_to_x(self, date_str: str) -> float:
        delta_days = max(0, min((parser.parse(date_str) - self.start_date).days, self.total_days))
        return self.chart_start_x + (delta_days * self.pixels_per_day)

    def calculate_bar(self, start_str: str, end_str: str) -> Dict[str, float]:
        start_x = self.date_to_x(start_str)
        end_x = self.date_to_x(end_str)
        width = max(0.1, end_x - start_x)
        return {"x": start_x + width / 2, "start_x": start_x, "width": width}
```

### 9.3 Diagram Builder (`core/diagram_builder.py`)

Drawing order:

1. `_draw_header()` — title block `#1a237e`
2. `_draw_timeline_axis()` — date range + vertical grid lines
3. For each phase: `_draw_phase()` roll-up bar, then `_draw_task()` for nested tasks
4. `_draw_milestones()` — amber diamond markers on timeline
5. `_draw_dependencies()` — orthogonal FS connectors between recorded item positions
6. `_draw_summary()` — footer with phase/task/milestone counts

Key behaviors:

- Phase roll-up spans earliest task start → latest task end via `calculate_phase_rollup()`
- Progress overlay (`#2E7D32`) when `0 < completion < 100` and `show_percent_complete` is true
- Task indentation: `level * 0.5` inches in left pane
- Dependencies route: end of predecessor → start of successor (orthogonal elbow)

### 9.4 Aspose Renderer (`renderers/aspose_renderer.py`)

**CRITICAL:** Use `asposediagram.api` via JPype — not `from aspose.diagram import …`.

```python
import jpype
if not jpype.isJVMStarted():
    jpype.startJVM(convertStrings=False)
import asposediagram.api as api

diagram = api.Diagram()
page = diagram.getPages().get(0)
shape = page.addText(x, y, w, h, text)
shape.getFill().getFillForegnd().setValue("#1565C0")
diagram.save(output_path, api.SaveFileFormat.VSDX)
```

Helpers: `new_diagram()`, `add_rectangle()`, `draw_line()`, `save_diagram()`.

---

## 10. Error Handling

Define comprehensive error codes to prevent broken timelines or layout corruption:

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| `GC-001` | InvalidInput | Input JSON missing required fields. | Validate payload against Pydantic schema. |
| `GC-002` | NoPhases | Zero phases defined in JSON. | Ensure at least one phase block exists. |
| `GC-003` | NoTasks | A defined phase contains zero tasks. | Add tasks or remove empty phase. |
| `GC-004` | InvalidDateRange | `start_date` occurs chronologically after `end_date`. | Reverse dates. |
| `GC-005` | InvalidDependency| The `dependencies` array references a Task ID that does not exist. | Verify node ID spelling. |
| `GC-006` | CircularDependency| Task A waits for Task B, which waits for Task A. | Implement Directed Acyclic Graph (DAG) checker. Break the cycle. |
| `GC-007` | TaskOverlap | Task start date is physically before the project start date. | Shift project `start_date` earlier or clamp task date. |
| `GC-008` | JavaNotInstalled | Missing JRE. | Install Java 11+ for JPype wrapper. |
| `GC-009` | LicenseMissing | Aspose `.lic` missing. | Configure `.env` or accept evaluation watermark. |
| `GC-010` | RenderError | Aspose internal exception writing file. | Check log output. |

---

## 11. Command-Line Interface (CLI)

```bash
python gantt_chart_generator/cli.py INPUT [-o OUTPUT] [-v] [--show-progress] [--validate-only]
```

| Flag | Description |
|------|-------------|
| `input` | Path to JSON or YAML gantt specification |
| `-o`, `--output` | Output `.vsdx` path (default: `./output/gantt_chart.vsdx`) |
| `-v`, `--verbose` | DEBUG logging |
| `--show-progress` | Sets `styling.show_percent_complete = true` |
| `--validate-only` | Validate schema without rendering |

Supports `.json`, `.yaml`, and `.yml` input files.

---

## 12. Quality Checklist

Before finalizing the generated Gantt Chart, verify:

### Visual
- [ ] Professional color palette used consistently (Section 2.2)
- [ ] Phase colors match across task list, bars, and legend
- [ ] Title block `#1a237e` with white text
- [ ] Clean white background with subtle grid lines
- [ ] All fonts Arial/Helvetica at prescribed sizes
- [ ] No text overflow in task names or bar labels

### Structural
- [ ] Task list rows align 1:1 with timeline bars on Y-axis
- [ ] Phase rows visually distinct with roll-up bars
- [ ] Task indentation follows `level` (0=phase, 1=task, 2=subtask)
- [ ] Milestone diamonds positioned on correct dates
- [ ] Dependencies connect predecessor end → successor start (FS)
- [ ] Timeline axis shows project date range

### Data
- [ ] All task dates within `start_date`…`end_date`
- [ ] Dependencies reference existing task IDs
- [ ] No circular dependencies (GC-006)
- [ ] Progress overlays match `completion` percentages
- [ ] Phase roll-ups span min start → max end of child tasks
- [ ] Each phase has at least one task

### Professional / QA
- [ ] Consulting-grade visual quality suitable for executives
- [ ] Consistent spacing between rows and grid lines
- [ ] Summary footer shows phase/task/milestone counts
- [ ] Output `.vsdx` ≥ 4 KB (`MIN_VSDX_BYTES`)
- [ ] Opens cleanly in Microsoft Visio without repair prompts

---

## 13. Usage Examples

### 13.1 Basic Generation
```bash
cd gantt_chart_generator
python cli.py examples/sample_input.json -o output/gantt_chart.vsdx
```

### 13.2 Generate with Progress Overlays
```bash
python cli.py examples/sample_input.json -o output/gantt_progress.vsdx --show-progress
```

### 13.3 Schema Validation Only
```bash
python cli.py examples/sample_input.json --validate-only -v
```

### 13.4 End-to-End Smoke Test
```bash
cd gantt_chart_generator
../project_charter_generator/.venv/bin/python scripts/run_example.py
```

### 13.5 Healthcare Ecosystem Sample
```bash
python cli.py ../project_charter_generator/national-integrated-healthcare-ecosystem/inputs/gantt_input.json \
  -o output/nihe_gantt.vsdx --show-progress
```

---

## 14. Integration with Existing Skills

The Gantt Chart Generator seamlessly integrates with:
1.  **Project Charter Generator:** `project-charter-generator-SKILL.md` can extract the "Schedule & Milestones" JSON block and pipe it directly to this CLI to generate the `.vsdx` schedule exhibit automatically attached to the charter appendix.
2.  **Shared Geometry Utilities:** Utilizes the exact same Aspose scaling engine as the `wbs-diagram-generator`, ensuring font sizes, borders, and shadows visually match across the entire project documentation suite.

---

## 15. Testing Strategy

1. **Date Math Test:** Task Feb 1 → Mar 1 (non-leap year) bar width equals 28 × `pixels_per_day`.
2. **Proportional Duration:** 60-day bar is exactly twice the width of a 30-day bar.
3. **Circular DAG Test:** T1 → T2 → T3 → T1 triggers `GC-006` before rendering.
4. **Out of Bounds Test:** Task start before `start_date` is clamped by `date_to_x()` (GC-007).
5. **Empty Phase Test:** Phase with zero tasks still renders header without crash.
6. **MIN_VSDX_BYTES:** Assert output ≥ 4 KB after successful build.
7. **Progress Overlay:** Task at 50% completion shows green overlay at half bar width.

---

## 16. Troubleshooting Guide

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `.vsdx` < 4 KB | JVM/Aspose failure | Install JRE 11+; set `ASPOSE_DIAGRAM_LICENSE_PATH` in `.env` |
| `Aspose.Diagram is not available` | Missing JPype or Java | `pip install aspose-diagram JPype1`; verify `java -version` |
| `Validation failed` (GC-001) | Schema mismatch | Run `--validate-only -v`; check required `gantt_chart` fields |
| `GC-005` InvalidDependency | Typo in `dependencies` array | Match IDs to `tasks[].id` within phases |
| Bars misaligned with names | Row height drift | Ensure `_draw_task()` and left pane use same `current_y` |
| Bars too narrow/wide | Wrong page size | Confirm A2 landscape (59.4 × 42.0 in) in `layout.page_size` |
| No progress overlay | Flag not set | Use `--show-progress` or set `styling.show_percent_complete: true` |
| Dependencies missing | ID not in `item_positions` | Ensure predecessor task was drawn before dependent |
| Wrong import error | `aspose.diagram` | Use `asposediagram.api` via JPype (Section 9.4) |
| Evaluation watermark | No license file | Copy `.lic` to path in `ASPOSE_DIAGRAM_LICENSE_PATH` |

**Validation-only:**

```bash
python gantt_chart_generator/cli.py examples/sample_input.json --validate-only -v
```

**End-to-end test:**

```bash
cd gantt_chart_generator
../project_charter_generator/.venv/bin/python scripts/run_example.py
```
