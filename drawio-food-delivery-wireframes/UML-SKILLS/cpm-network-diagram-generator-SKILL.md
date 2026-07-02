---
name: cpm-network-diagram-generator
description: Generate enterprise-grade CPM (Critical Path Method) Network Diagrams as Visio (.vsdx) using Aspose.Diagram for Python. Computes ES, EF, LS, LF, slack, free float, and critical path; renders Activity-on-Node topology with consulting-quality styling per uml-diagram-generator-SKILL.md §11. Supports FS/SS/FF/SF dependencies with lag.
---

# CPM Network Diagram (Critical Path Method) Generator Skill

This production-grade skill generates **CPM Network Diagrams** in Microsoft Visio (`.vsdx`) format. It maps **Activity-on-Node (AON)** networks for deterministic project scheduling, calculates Earliest/Latest Start/Finish (ES, EF, LS, LF), Total Float (Slack), and Free Float, and automatically highlights the critical path with enterprise styling.

It supports dependency types **FS, SS, FF, SF** with lag offsets. Functions as a standalone deliverable or as a sub-component of `project-charter-generator`, `gantt-chart-generator`, and `wbs-diagram-generator`.

## Design Philosophy

Every output must be:

| Principle | Requirement |
|-----------|-------------|
| **Visually stunning** | Enterprise palette, critical path in red, clean AON layout |
| **Enterprise-ready** | C-suite presentations and project schedule reviews |
| **Technically precise** | Correct forward/backward pass, slack, critical path |
| **Programmatic** | Fully automated — no manual Visio tweaking |

**Design system authority:** Inherits mandatory standards from [`uml-diagram-generator-SKILL.md`](uml-diagram-generator-SKILL.md) §11 (page layout, typography, title block, legend, connector routing, QA). This skill adds CPM-specific node formatting and critical-path highlighting.

## Table of Contents

1. Core Output Specifications
2. Professional Design Standards
3. Environment Setup & Dependencies
4. Input Specification (JSON/YAML Schema)
5. CPM Network Visual Layout (ASCII Blueprint)
6. Activity Node Structure
7. Critical Path Method (CPM) Calculation Rules
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

The primary purpose of this skill is to generate a complete CPM Network Diagram that guarantees:
1. **AON Topology:** Accurate rendering of tasks as nodes using the standard Activity-On-Node convention.
2. **CPM Calculation:** Full deterministic execution of Forward and Backward passes accommodating for advanced dependencies (`FS`, `SS`, `FF`, `SF`) and lag offsets.
3. **Float & Slack:** Precise calculation of Total Float (Slack) and Free Float.
4. **Critical Path Highlighting:** Distinct visual tracking of the critical path(s) using bold red connectors and thickened red node borders.
5. **Path Summary Block:** Automated generation of a summary legend detailing the primary critical path sequence, project total duration, and secondary/tertiary paths with their respective slacks.
6. **Professional Styling:** Enterprise-themed Visio shapes — critical nodes `#FFEBEE` / `#C62828`, normal nodes `#E3F2FD` / `#1565C0`.

---

## 2. Professional Design Standards

### 2.1 Inherited Base Standards

Apply all settings from [`uml-diagram-generator-SKILL.md`](uml-diagram-generator-SKILL.md) §11:

- Page: **A2 landscape** (59.4 × 42.0 in), margin **0.5 cm**
- Font: **Arial** (14pt activity ID, 10pt name, 8–9pt CPM values)
- Title block: `#1a237e` background, white text
- Connectors: orthogonal routing; critical edges `#C62828` width 2.5pt
- QA: minimum `.vsdx` size ≥ 4 KB

### 2.2 CPM Network Styling Configuration

```yaml
cpm_network_styling:
  page:
    size: "A2"
    orientation: "landscape"
    margin: 0.5
    background_color: "#FFFFFF"

  activity_node:
    normal:
      fill_color: "#E3F2FD"
      stroke_color: "#1565C0"
      stroke_width: 1.5
      width: 3.2
      height: 2.2
      corner_radius: 6
    critical:
      fill_color: "#FFEBEE"
      stroke_color: "#C62828"
      stroke_width: 3.0
    start_end:
      fill_color: "#1a237e"
      stroke_color: "#1a237e"
      text_color: "#FFFFFF"
      corner_radius: 20

  dependencies:
    normal:  { color: "#666666", width: 1.0, arrow: filled }
    critical: { color: "#C62828", width: 2.5, arrow: filled }

  node_text:
    activity_id:  { size: 14, weight: bold, color: "#1a237e" }
    activity_name: { size: 10, weight: bold, color: "#333333" }
    duration:     { size: 9, color: "#666666" }
    es_ef_ls_lf:  { size: 8, color: "#555555" }
    slack_critical: { size: 9, weight: bold, color: "#C62828" }
    slack_normal:   { size: 9, color: "#333333" }
    predecessors: { size: 8, color: "#888888" }

  title_block:
    height: 1.2
    background: "#1a237e"
    text_color: "#FFFFFF"

  legend:
    enabled: true
    position: "top_left"
    width: 4.5

  summary_box:
    enabled: true
    position: "bottom"
    shows: [critical_path_sequence, total_duration, non_critical_paths]
```

### 2.3 Anti-Patterns (Do NOT)

- Wrong CPM math (hardcoded ES/EF instead of calculated)
- Critical path not highlighted (`slack == 0` must use red border)
- Comic Sans or unlabeled colors
- Circular dependencies (AON must be a DAG)
- Using `aspose.diagram` import (use `asposediagram.api` via JPype)
- Accepting sub-4KB `.vsdx` as success

---

## 3. Environment Setup & Dependencies

### 3.1 Python Requirements
The generator uses Kahn's algorithm for topological sorting (no external graph library required).
```text
python >= 3.10
aspose-diagram>=23.10.0
JPype1>=1.5.0
pydantic>=2.0.0
python-dotenv>=1.0.0
pyyaml>=6.0
```

### 3.2 System Dependencies

**Java Runtime Environment (JRE) 8 or higher**
- Required for `Aspose.Diagram for Python` (interfacing via JPype).
- *Installation guide:*
  - Ubuntu: `sudo apt-get install default-jre`
  - macOS: `brew install openjdk`
  - Windows: Download from https://www.java.com/download/

### 3.3 Virtual Environment Setup
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

### 3.4 Environment Variables (.env file)
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

## 4. Input Specification (JSON/YAML Schema)

The generator enforces a strict JSON schema that allows complex predecessor definitions including `type` (FS/SS/FF/SF) and `lag` values.

```json
{
  "cpm_network": {
    "title": "CPM Network Diagram - Critical Path Method",
    "project_name": "Healthcare Ecosystem Project",
    "version": "1.0",
    "date": "2026-06-17",
    "description": "Activity network diagram with critical path",
    
    "activities": [
      {
        "id": "A",
        "name": "Develop Charter",
        "description": "Create project charter",
        "duration": 2,
        "duration_units": "weeks",
        "predecessors": [],
        "is_start": true,
        "lag": 0
      },
      {
        "id": "B",
        "name": "Create Schedule",
        "description": "Develop project schedule",
        "duration": 4,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "A", "type": "FS", "lag": 0}
        ],
        "is_start": false
      },
      {
        "id": "C",
        "name": "Define Budget",
        "description": "Establish project budget",
        "duration": 3,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "A", "type": "FS", "lag": 0}
        ],
        "is_start": false
      },
      {
        "id": "D",
        "name": "Requirements Elicitation",
        "description": "Gather requirements from stakeholders",
        "duration": 6,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "B", "type": "FS", "lag": 0}
        ],
        "is_start": false
      },
      {
        "id": "E",
        "name": "Requirements Analysis",
        "description": "Analyze and prioritize requirements",
        "duration": 4,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "D", "type": "FS", "lag": 0}
        ],
        "is_start": false
      },
      {
        "id": "F",
        "name": "Requirements Specification",
        "description": "Document requirements in SRS",
        "duration": 3,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "D", "type": "FS", "lag": 0}
        ],
        "is_start": false
      },
      {
        "id": "G",
        "name": "Database Design",
        "description": "Design database schema",
        "duration": 5,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "E", "type": "FS", "lag": 0},
          {"id": "F", "type": "FS", "lag": 0}
        ],
        "is_start": false
      },
      {
        "id": "H",
        "name": "API Design",
        "description": "Design RESTful APIs",
        "duration": 6,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "G", "type": "FS", "lag": 0}
        ],
        "is_start": false
      },
      {
        "id": "I",
        "name": "UI/UX Design",
        "description": "Design user interface",
        "duration": 7,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "H", "type": "FS", "lag": 0}
        ],
        "is_start": false
      },
      {
        "id": "J",
        "name": "Backend Development",
        "description": "Build backend services",
        "duration": 12,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "H", "type": "FS", "lag": 0}
        ],
        "is_start": false
      },
      {
        "id": "K",
        "name": "Frontend Development",
        "description": "Build user interfaces",
        "duration": 10,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "I", "type": "FS", "lag": 0}
        ],
        "is_start": false
      },
      {
        "id": "L",
        "name": "Integration",
        "description": "Integrate all components",
        "duration": 4,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "J", "type": "FS", "lag": 0},
          {"id": "K", "type": "FS", "lag": 0}
        ],
        "is_start": false
      },
      {
        "id": "M",
        "name": "Testing",
        "description": "System testing and UAT",
        "duration": 6,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "L", "type": "FS", "lag": 0}
        ],
        "is_start": false
      },
      {
        "id": "N",
        "name": "Deployment",
        "description": "Deploy to production",
        "duration": 3,
        "duration_units": "weeks",
        "predecessors": [
          {"id": "M", "type": "FS", "lag": 0}
        ],
        "is_start": false,
        "is_end": true
      }
    ],
    
    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "critical_path_color": "#C62828",
      "critical_path_text_color": "#FFFFFF",
      "node_width": 3.2,
      "node_height": 2.2,
      "show_es_ef": true,
      "show_ls_lf": true,
      "show_slack": true,
      "show_predecessors": true,
      "shadow_enabled": true
    },
    
    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "level_spacing": 3.0,
      "node_spacing": 1.5
    }
  }
}
```

---

## 5. CPM Network Visual Layout (ASCII Blueprint)

**CRITICAL REQUIREMENT:** The Activity-on-Node structure requires tasks to be displayed inside nodes, unlike Activity-on-Arrow diagrams.

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                          CPM NETWORK DIAGRAM - CRITICAL PATH METHOD                                                 │
│                                         Da'atSNA Community Data Platform                                                            │
│                                         Version 1.0  |  2026-06-17                                                                  │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                      │
│   Legend:                                                                                                                            │
│   ⬅️ = Critical Path (Red)   ⬜ = Non-Critical Path   ◇ = Milestone/Start-End   ⬆ = Dependency Arrow                                 │
│   ES = Earliest Start  EF = Earliest Finish  LS = Latest Start  LF = Latest Finish  Slack = Total Float                              │
│   💡 = Activity Node Format: [ID] | Duration | ES | EF | LS | LF | Slack                                                             │
│                                                                                                                                      │
│                                                ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│                                                │                           START                                                  │ │
│                                                │                           [S]                                                    │ │
│                                                │                     ES: 0  EF: 0                                                  │ │
│                                                │                     LS: 0  LF: 0                                                  │ │
│                                                └───────────────────────────────┬─────────────────────────────────────────────────┘ │
│                                                                                │                                                     │
│                                ┌───────────────────────────────────────────────┼───────────────────────────────────────────────┐      │
│                                │                                               │                                               │      │
│                                ▼                                               ▼                                               ▼      │
│  ┌───────────────────────────────────────────────────────┐   ┌───────────────────────────────────────────────────────┐   ┌───────────────────────────────────────────────────────┐
│  │                    TASK A                             │   │                    TASK B                             │   │                    TASK C                             │
│  │          [A] Develop Charter                         │   │          [B] Create Schedule                         │   │          [C] Define Budget                          │
│  │          Duration: 2 weeks                           │   │          Duration: 4 weeks                           │   │          Duration: 3 weeks                           │
│  │          ES: 0    EF: 2                              │   │          ES: 2    EF: 6                              │   │          ES: 2    EF: 5                              │
│  │          LS: 0    LF: 2                              │   │          LS: 2    LF: 6                              │   │          LS: 3    LF: 6                              │
│  │          Slack: 0  [CRITICAL] ⬅️                    │   │          Slack: 0  [CRITICAL] ⬅️                    │   │          Slack: 1                                    │
│  │          Predecessors: None                         │   │          Predecessors: A                              │   │          Predecessors: A                              │
│  └───────────────────────────────────────────────────────┘   └───────────────────────────────────────────────────────┘   └───────────────────────────────────────────────────────┘
│                                │                                               │                                               │
│                                └───────────────────────────────────────────────┼───────────────────────────────────────────────┘      │
│                                                                                │                                                     │
│                                                                                ▼                                                     │
│                          ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│                          │                              TASK D                                                                   │ │
│                          │                    [D] Requirements Elicitation                                                      │ │
│                          │                    Duration: 6 weeks                                                                │ │
│                          │                    ES: 6    EF: 12                                                                   │ │
│                          │                    LS: 6    LF: 12                                                                   │ │
│                          │                    Slack: 0  [CRITICAL] ⬅️                                                          │ │
│                          │                    Predecessors: B                                                                   │ │
│                          └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │                                                     │
│                                          ┌─────────────────────────────────────┼─────────────────────────────────────┐            │
│                                          │                                     │                                     │            │
│                                          ▼                                     ▼                                     ▼            │
│  ┌───────────────────────────────────────────────────────┐   ┌───────────────────────────────────────────────────────┐   ┌───────────────────────────────────────────────────────┐
│  │                    TASK E                             │   │                    TASK F                             │   │                    TASK G                             │
│  │          [E] Requirements Analysis                    │   │          [F] Requirements Specification               │   │          [G] Database Design                          │
│  │          Duration: 4 weeks                           │   │          Duration: 3 weeks                           │   │          Duration: 5 weeks                           │
│  │          ES: 12    EF: 16                            │   │          ES: 12    EF: 15                            │   │          ES: 16    EF: 21                            │
│  │          LS: 18    LF: 22                            │   │          LS: 19    LF: 22                            │   │          LS: 16    LF: 21                            │
│  │          Slack: 6                                    │   │          Slack: 7                                    │   │          Slack: 0  [CRITICAL] ⬅️                    │
│  │          Predecessors: D                             │   │          Predecessors: D                             │   │          Predecessors: E, F                          │
│  └───────────────────────────────────────────────────────┘   └───────────────────────────────────────────────────────┘   └───────────────────────────────────────────────────────┘
│                                          │                                     │                                     │
│                                          └─────────────────────────────────────┼─────────────────────────────────────┘            │
│                                                                                │                                                     │
│                                                                                ▼                                                     │
│                          ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│                          │                              TASK H                                                                   │ │
│                          │                    [H] API Design                                                                   │ │
│                          │                    Duration: 6 weeks                                                                │ │
│                          │                    ES: 21    EF: 27                                                                  │ │
│                          │                    LS: 21    LF: 27                                                                  │ │
│                          │                    Slack: 0  [CRITICAL] ⬅️                                                          │ │
│                          │                    Predecessors: G                                                                   │ │
│                          └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │                                                     │
│                                          ┌─────────────────────────────────────┼─────────────────────────────────────┐            │
│                                          │                                     │                                     │            │
│                                          ▼                                     ▼                                     ▼            │
│  ┌───────────────────────────────────────────────────────┐   ┌───────────────────────────────────────────────────────┐   ┌───────────────────────────────────────────────────────┐
│  │                    TASK I                             │   │                    TASK J                             │   │                    TASK K                             │
│  │          [I] UI/UX Design                            │   │          [J] Backend Development                      │   │          [K] Frontend Development                     │
│  │          Duration: 7 weeks                           │   │          Duration: 12 weeks                          │   │          Duration: 10 weeks                          │
│  │          ES: 27    EF: 34                            │   │          ES: 27    EF: 39                            │   │          ES: 34    EF: 44                            │
│  │          LS: 27    LF: 34                            │   │          LS: 27    LF: 39                            │   │          LS: 34    LF: 44                            │
│  │          Slack: 0  [CRITICAL] ⬅️                    │   │          Slack: 0  [CRITICAL] ⬅️                    │   │          Slack: 0  [CRITICAL] ⬅️                    │
│  │          Predecessors: H                             │   │          Predecessors: H                             │   │          Predecessors: I                             │
│  └───────────────────────────────────────────────────────┘   └───────────────────────────────────────────────────────┘   └───────────────────────────────────────────────────────┘
│                                          │                                     │                                     │
│                                          └─────────────────────────────────────┼─────────────────────────────────────┘            │
│                                                                                │                                                     │
│                                                                                ▼                                                     │
│                          ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│                          │                              TASK L                                                                   │ │
│                          │                    [L] Integration                                                                   │ │
│                          │                    Duration: 4 weeks                                                                │ │
│                          │                    ES: 44    EF: 48                                                                  │ │
│                          │                    LS: 44    LF: 48                                                                  │ │
│                          │                    Slack: 0  [CRITICAL] ⬅️                                                          │ │
│                          │                    Predecessors: J, K                                                               │ │
│                          └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │                                                     │
│                          ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│                          │                              TASK M                                                                   │ │
│                          │                    [M] Testing                                                                       │ │
│                          │                    Duration: 6 weeks                                                                │ │
│                          │                    ES: 48    EF: 54                                                                  │ │
│                          │                    LS: 48    LF: 54                                                                  │ │
│                          │                    Slack: 0  [CRITICAL] ⬅️                                                          │ │
│                          │                    Predecessors: L                                                                   │ │
│                          └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │                                                     │
│                                                                                ▼                                                     │
│                          ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│                          │                              TASK N                                                                   │ │
│                          │                    [N] Deployment                                                                    │ │
│                          │                    Duration: 3 weeks                                                                │ │
│                          │                    ES: 54    EF: 57                                                                  │ │
│                          │                    LS: 54    LF: 57                                                                  │ │
│                          │                    Slack: 0  [CRITICAL] ⬅️                                                          │ │
│                          │                    Predecessors: M                                                                   │ │
│                          └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │                                                     │
│                                                                                ▼                                                     │
│                                                ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│                                                │                          END                                                     │ │
│                                                │                          [E]                                                    │ │
│                                                │                    ES: 57  EF: 57                                              │ │
│                                                │                    LS: 57  LF: 57                                              │ │
│                                                └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                                                      │
│  Critical Path Summary:                                                                                                              │
│  ═══════════════════════                                                                                                             │
│  Critical Path: A → B → D → G → H → I → K → L → M → N  (alt: … → H → J → L → M → N)                                                │
│  Total Project Duration: 57 weeks                                                                                                   │
│                                                                                                                                      │
│  Non-Critical Paths:                                                                                                                 │
│  ────────────────────                                                                                                                │
│  Path: A → C (Slack: 1 week on C)                                                                                                   │
│  Path: D → E → G (Slack: 6 weeks on E)                                                                                              │
│  Path: D → F → G (Slack: 7 weeks on F)                                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Activity Node Structure

Unlike PERT, the CPM generator uses an expanded Activity Node Format mapping out all float values clearly:

```text
┌─────────────────────────────────────────────────────┐
│                 [A]  Develop Charter                │
│  ┌────────────────────────────────────────────────┐ │
│  │  Duration: 2 weeks                            │ │
│  ├────────────────────────────────────────────────┤ │
│  │  ES: 0    EF: 2    │   LS: 0    LF: 2         │ │
│  │  Slack: 0  [CRITICAL]                         │ │
│  ├────────────────────────────────────────────────┤ │
│  │  Predecessors: None                           │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 7. Critical Path Method (CPM) Calculation Rules

CPM calculations require complex handling of standard dependencies and their lags.

### Dependency Types & Lag Math
| Type | Math Rule | Description |
|------|-----------|-------------|
| **FS** | `ES(succ) >= EF(pred) + Lag` | Successor starts after predecessor finishes (Standard) |
| **SS** | `ES(succ) >= ES(pred) + Lag` | Successor starts after predecessor starts |
| **FF** | `EF(succ) >= EF(pred) + Lag` | Successor finishes after predecessor finishes |
| **SF** | `EF(succ) >= ES(pred) + Lag` | Successor finishes after predecessor starts |

### Standard Pass Algorithms
1. **Forward Pass (Early Values):** Computes `ES` and `EF`. Evaluates all predecessors and selects the constraint that forces the latest possible early start/finish.
2. **Backward Pass (Late Values):** Computes `LS` and `LF`. Evaluates all successors and selects the constraint that forces the earliest possible late start/finish.
3. **Total Float (Slack):** `LS - ES` or `LF - EF`. The amount of time an activity can be delayed without delaying the project END date.
4. **Free Float:** `Min(ES of all immediate successors) - EF`. The amount of time an activity can be delayed without delaying the early start of any immediate successor.

**Visual styling** for nodes, connectors, and legend: see **Section 2.2**.

### Activity Node Quick Reference

| Property | Normal | Critical |
|----------|--------|----------|
| Fill | `#E3F2FD` | `#FFEBEE` |
| Border | `#1565C0` 1.5pt | `#C62828` 3pt |
| Connector | `#666666` 1pt | `#C62828` 2.5pt |

---

## 8. Code Architecture

```text
cpm_network_generator/
├── SKILL.md                       # Canonical skill (repo root: cpm-network-diagram-generator-SKILL.md)
├── PROMPT.md
├── core/
│   ├── cpm_builder.py             # Orchestrator: validate + build + size check
│   ├── diagram_builder.py         # CPMNetworkBuilder — Aspose rendering
│   ├── validator.py
│   ├── errors.py                  # CycleDetectedError, etc.
│   └── models.py
├── calculators/
│   └── cpm_calculator.py          # Forward/backward pass, FS/SS/FF/SF + lag
├── renderers/
│   ├── aspose_renderer.py         # JVM-backed asposediagram.api helpers
│   └── layout_engine.py           # DAG level-based node placement
├── config/
│   └── settings.py                # PAGE_SIZES_IN, license
├── scripts/
│   └── run_example.py
└── cli.py
```

---

## 9. Core Implementation

### 9.1 Orchestrator (`core/cpm_builder.py`)

```python
from core.cpm_builder import build_cpm_network

build_cpm_network(spec_dict, "output/cpm_diagram.vsdx")
# Validates, applies Aspose license, renders, enforces MIN_VSDX_BYTES >= 4000
```

### 9.2 CPM Calculator (`calculators/cpm_calculator.py`)

Uses **Kahn's algorithm** for topological sort (no networkx dependency). Supports string or object predecessors.

```python
from calculators.cpm_calculator import CPMCalculator
from core.errors import CycleDetectedError

cpm = CPMCalculator(activities)  # mutates activities in-place with es/ef/ls/lf/slack
critical = [a for a in cpm.activities if a.get("is_critical")]
duration = max(a.get("ef", 0) for a in cpm.activities)
```

### 9.3 Visio Builder (`core/diagram_builder.py`)

```python
from renderers import aspose_renderer as asp
from calculators.cpm_calculator import CPMCalculator
from renderers.layout_engine import LayoutEngine

class CPMNetworkBuilder:
    def build(self) -> None:
        self.cpm = CPMCalculator(self.config["activities"])
        self.diagram = asp.new_diagram()
        self.page = self.diagram.getPages().get(0)
        self._setup_page()                    # A2 from PAGE_SIZES_IN
        self.positions = LayoutEngine(...).calculate()
        # Title block (#1a237e)
        # Activity nodes — critical: #FFEBEE/#C62828, normal: #E3F2FD/#1565C0
        # Dependency arrows — critical edges red 2.5pt
        # Critical path summary box at bottom

    def save(self, path: str) -> None:
        asp.save_diagram(self.diagram, path)
```

**Node text format** (`_format_node_text`):

```text
[A] Develop Charter
Duration: 2 wks
ES: 0    EF: 2
LS: 0    LF: 2
Slack: 0  [CRITICAL]
Predecessors: None
```

---

## 10. Error Handling

Enforce mathematical constraints with custom exceptions:

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| `CPM-001` | InvalidInput | Pydantic schema rejection. | Fix JSON payload. |
| `CPM-002` | NoActivities | Empty activities list. | Provide at least 2 activities. |
| `CPM-003` | CycleDetected | Kahn's algorithm failed to sort topological order. | AON cannot have cycles. Break the loop. |
| `CPM-004` | MissingReference| Predecessor points to missing `id`. | Check spelling of predecessor IDs. |
| `CPM-005` | InvalidLag | Lag value is a non-number. | Set integer lag (e.g., `-2`, `0`, `5`). |
| `CPM-006` | InvalidDepType | Type is not `FS`, `SS`, `FF`, or `SF`. | Correct the dependency `type` enum. |
| `CPM-008` | JavaNotInstalled| Missing JRE. | Install Java 8+ for JPype wrapper. |
| `CPM-009` | LicenseMissing | Aspose `.lic` missing. | Ensure path is set. |
| `CPM-010` | RenderError | Aspose file write failure. | Check disk permissions. |

---

## 11. Command-Line Interface (CLI)

```python
# cli.py — uses build_cpm_network orchestrator
# Usage:
#   python cli.py examples/sample_input.json
#   python cli.py examples/sample_input.json --validate-only -v
#   python cli.py examples/sample_input.json -o ./output -v

from core.cpm_builder import build_cpm_network
from core.validator import validate

payload = load_input(path)
validate(payload)
if validate_only:
    return
build_cpm_network(payload, str(output_dir / "cpm_diagram.vsdx"))
```

---

## 12. Quality Checklist

Run before delivering any CPM network diagram.

### Visual

- [ ] Enterprise palette (Section 2.2) — normal `#E3F2FD`/`#1565C0`, critical `#FFEBEE`/`#C62828`
- [ ] Arial font throughout; activity ID bold `#1a237e`
- [ ] Title block present (`#1a237e`)
- [ ] Legend explains critical vs non-critical, ES/EF/LS/LF/slack notation
- [ ] Critical path summary box at bottom with sequence and total duration
- [ ] No text overflow in activity nodes
- [ ] Connectors orthogonal; critical edges red and thicker

### Technical (CPM math)

- [ ] Forward pass: ES/EF correct for FS, SS, FF, SF + lag
- [ ] Backward pass: LS/LF correct; slack = LS − ES
- [ ] Critical activities flagged where `abs(slack) < 0.01`
- [ ] Free float = min(successor ES) − EF
- [ ] Total duration = max(EF) of terminal activities
- [ ] No circular dependencies (DAG)
- [ ] All predecessor IDs exist

### Layout

- [ ] Activities flow top-to-bottom or left-to-right by level
- [ ] Start activities at top; terminal activities toward bottom
- [ ] Parallel branches (e.g. E/F from D) visually distinct
- [ ] All activities connected to network

### Output integrity

- [ ] `.vsdx` ≥ 4 KB
- [ ] Opens in Visio without repair warnings
- [ ] Calculated values on nodes match calculator output

---

## 13. Usage Examples

### 13.1 Basic Generation
```bash
python cpm_network_generator/cli.py examples/sample_input.json -o output/
# Writes output/cpm_diagram.vsdx
```

### 13.2 Logic Validation Only (CI/CD)
```bash
python cpm_network_generator/cli.py examples/sample_input.json --validate-only -v
```

### 13.3 End-to-End Example
```bash
cd cpm_network_generator
../project_charter_generator/.venv/bin/python scripts/run_example.py
```

---

## 14. Integration with Existing Skills

1. **Parent skill:** Inherits design standards from [`uml-diagram-generator-SKILL.md`](uml-diagram-generator-SKILL.md) §11.
2. **Gantt synergy:** Activity JSON maps to `gantt-chart-generator` task payloads — same schedule, different view.
3. **PERT counterpart:** CPM uses deterministic durations; PERT uses probabilistic (optimistic/most likely/pessimistic).
4. **Project charter:** Embed `.vsdx` in charter Visio deck or Word deliverable.

---

## 15. Testing Strategy

1. **Standard FS Test:** A → B (FS). Assert `ES(B) == EF(A)`.
2. **SS with Lag Test:** A → B (SS, lag 2). Assert `ES(B) == ES(A) + 2`.
3. **FF Test:** A → B (FF). Assert `EF(B) == EF(A)`.
4. **Cyclic Failure:** A → B → A. Assert `CycleDetectedError` raised.
5. **Free Float Test:** A → B, A → C with different durations. Assert B's free float uses min successor ES − EF(B).
6. **Critical Path Visual:** All `slack == 0` nodes have `#C62828` border in output.
7. **Sample E2E:** `scripts/run_example.py` produces ≥ 4 KB `.vsdx`.

---

## 16. Troubleshooting Guide

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `.vsdx` < 4 KB | JVM/Aspose failure | Install JRE 11+; set `ASPOSE_DIAGRAM_LICENSE_PATH` |
| `CycleDetectedError` (CPM-003) | Circular predecessor chain | Remove cycle — AON must be acyclic |
| `CPM-004` MissingReference | Typo in predecessor ID | Match `predecessors` to `activities[].id` |
| Wrong ES/EF values | SS/FF/SF not modeled | Use `{"id":"A","type":"FS","lag":0}` object form |
| Critical path not red | `is_critical` not set | Re-run calculator; check slack tolerance 0.01 |
| Nodes overlapping | Too many activities per level | Increase `level_spacing` / `node_spacing` in `layout` |
| Wrong import error | `aspose.diagram` | Use `asposediagram.api` via JPype (Section 9.3) |
| Slack ≠ LS − ES | Backward pass order | Ensure topological sort before backward pass |

**Validation-only:**

```bash
python cpm_network_generator/cli.py examples/sample_input.json --validate-only -v
```

**End-to-end test:**

```bash
cd cpm_network_generator
../project_charter_generator/.venv/bin/python scripts/run_example.py
```
