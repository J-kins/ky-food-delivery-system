---
name: project-charter-generator
description: Generate enterprise-grade Project Charters — Word document with native editable DrawingML shape diagrams, multi-page Visio analytical deck, and single-page executive Project Charter Summary Diagram. Consulting-quality styling per uml-diagram-generator-SKILL.md §11. Suitable for C-suite presentations, initiation workshops, and steering committee approvals.
---

# Project Charter Generator

This comprehensive skill orchestrates end-to-end Project Charter generation. It translates structured JSON/YAML input into a professional Word document with native editable shape diagrams, a multi-page editable Visio analytical deck, and an executive **Project Charter Summary Diagram** — a single-page Visio poster suitable for board approvals.

This is a **critical deliverable** that serves as the foundation for all project documentation.

## Design Philosophy

Every output must be:

| Principle | Requirement |
|-----------|-------------|
| **Visually stunning** | Enterprise palette, clean layouts, consulting-grade quality |
| **Enterprise-ready** | C-suite presentations and steering committee approvals |
| **Information-rich** | All charter elements clearly visible and organized |
| **Programmatic** | Fully automated — no manual Visio or Word tweaking |

**Design system authority:** Inherits mandatory standards from [`uml-diagram-generator-SKILL.md`](uml-diagram-generator-SKILL.md) §11 (page layout, typography, title block, legend, QA gates). This skill adds charter-specific section colors, tables, and diagram styling.

## Table of Contents

1. Core Output Specifications
2. Professional Design Standards
3. Project Charter Summary Diagram (ASCII Blueprint)
4. Environment Setup & Dependencies
5. Input Specification (JSON Schema)
6. Diagram Specifications (Analytical Diagrams)
7. Word Document Layout & Sections
8. Code Architecture & Implementation
9. Error Handling
10. Output Directory Structure
11. Quality Checklist
12. Diagram Visual Layouts (Analytical)
13. Usage Examples
14. Integration with Existing Skills
15. Testing Strategy
16. Troubleshooting Guide

---

## 1. Core Output Specifications

The skill guarantees two primary output artifacts:

### Output A: Word Document (with native editable shape diagrams)
- **Engine:** `python-docx` + custom DrawingML inserter (`word/drawingml_inserter.py`)
- **Content:** Full written charter — 13 sections, tables, bulleted lists.
- **Visuals:** Diagrams embedded as **native Word DrawingML shapes** (`wps:wsp` rectangles, text boxes, connectors inside `wpg:wgp` groups) — click-to-edit in Microsoft Word, **not** SVG or PNG images.
- **Diagram pipeline:**
  1. Agent authors `charter_diagram_<name>_input.json` (Graphviz or D2 description)
  2. Layout engine (`diagrams/layouts.py`) produces `{nodes, edges, title}` from payload
  3. `word/drawingml_inserter.py` converts layout → grouped DrawingML shapes in `.docx`
  4. SVG archive written to `output/diagrams/svg/` when Graphviz/D2 compiles successfully

### Output B: Visio Analytical Deck (multi-page `.vsdx`)
- **Engine:** `Aspose.Diagram for Python` (`aspose-diagram` + JRE via JPype)
- **Content:** Seven charter analytical diagrams as separate Visio pages.
- **License:** Set `ASPOSE_DIAGRAM_LICENSE_PATH` in `.env` to remove evaluation watermarks.
- **Features:** Editable shapes via `Page.addText`, connectors, layouts from `diagrams/layouts.py`.
- **QA gate:** Minimum `.vsdx` size ≥ 5 KB (`MIN_VSDX_BYTES`).

### Output C: Project Charter Summary Diagram (single-page `.vsdx`)
- **Engine:** `Aspose.Diagram` via `diagrams/charter_summary_builder.py` (target)
- **Content:** Executive one-page poster — Vision, Overview, Objectives, Scope, Stakeholders, Constraints/Assumptions, Milestones, Budget, Approvals.
- **Page:** A2 landscape (59.4 × 42.0 in), margin 0.5 in.
- **Use case:** Steering committee kickoff, board approval, PMO wall chart.
- **Input:** Same narrative payload as Word/Visio (`project`, `vision`, `objectives`, `scope`, etc.) — no separate diagram description files required.

---

## 2. Professional Design Standards

### 2.1 Inherited Base Standards

Apply all settings from [`uml-diagram-generator-SKILL.md`](uml-diagram-generator-SKILL.md) §11:

- Page: **A2 landscape** for Visio; **A4** for Word
- Font: **Arial** (Visio), **Calibri** (Word body)
- Title block: `#1a237e` background, white text
- QA: Word ≥ 8 KB; Visio deck ≥ 5 KB

### 2.2 Project Charter Styling Configuration

```yaml
project_charter_styling:
  page:
    size: "A2"
    orientation: "landscape"
    margin: 0.5
    background_color: "#FFFFFF"
    grid_enabled: false

  colors:
    primary: "#1a237e"
    secondary: "#1565C0"
    tertiary: "#64B5F6"
    background: "#FFFFFF"
    text: "#333333"
    subtle: "#F5F5F5"
    accent: "#FFB300"
    success: "#2E7D32"
    warning: "#E65100"
    critical: "#C62828"

    sections:
      vision:         { bg: "#E3F2FD", border: "#1565C0", text: "#0D47A1" }
      overview:       { bg: "#F5F5F5", border: "#78909C", text: "#333333" }
      objectives:     { bg: "#E8F5E9", border: "#2E7D32", text: "#1B5E20" }
      scope:          { bg: "#FFF3E0", border: "#E65100", text: "#BF360C" }
      stakeholders:   { bg: "#F3E5F5", border: "#6A1B9A", text: "#4A148C" }
      constraints:    { bg: "#FFEBEE", border: "#C62828", text: "#B71C1C" }
      milestones:     { bg: "#E0F7FA", border: "#00838F", text: "#006064" }
      budget:         { bg: "#FFF8E1", border: "#FFB300", text: "#F57F17" }
      approvals:      { bg: "#F5F5F5", border: "#78909C", text: "#333333" }

  typography:
    font_family: "Arial"
    title:       { size: 22, weight: bold, color: "#1a237e", uppercase: true }
    subtitle:    { size: 14, weight: bold, color: "#1565C0" }
    section_header: { size: 12, weight: bold, color: "#FFFFFF", uppercase: true }
    table_header:   { size: 10, weight: bold, color: "#FFFFFF" }
    table_cell:     { size: 9,  weight: normal, color: "#333333" }
    body:           { size: 9,  weight: normal, color: "#333333" }

  section_box:
    corner_radius: 6
    border: { style: solid, width: 1.0, color: "#E0E0E0" }
    header_height: 0.6
    section_gap: 0.3

  table:
    header_fill: "#1a237e"
    header_text: "#FFFFFF"
    alternating_rows: { even: "#F8F9FA", odd: "#FFFFFF" }
    border: { width: 0.5, color: "#BDBDBD" }

  word_document:
    body_font: "Calibri"
    body_size: 11
    heading1: { font: "Calibri Light", size: 16, color: "#1a237e" }
    margins_cm: 2.54
    figure_width_inches: 6.0
    embed_format: "svg_xml"          # never PNG
```

### 2.3 Anti-Patterns (Do NOT)

- PNG raster diagrams embedded in Word (use native DrawingML via `word/drawingml_inserter.py`)
- `aspose.diagram` import (use `asposediagram.api` via JPype)
- Accepting sub-threshold output files as success
- Inconsistent section colors between Summary Diagram and Word tables
- Missing confidentiality footer on executive poster

---

## 3. Project Charter Summary Diagram (ASCII Blueprint)

**CRITICAL:** The single-page executive diagram stacks all charter sections vertically on A2 landscape. Each section has a colored header bar and content box per Section 2.2.

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    PROJECT CHARTER                                                            │
│                              Da'atSNA Community Data Platform                                                 │
│                       Version 1.0  |  2026-06-17  |  Confidential                                            │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  VISION (#E3F2FD)                                                                                             │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  To empower Ugandan communities with data-driven decision-making through an offline-first SNA platform │  │
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│  PROJECT OVERVIEW (#F5F5F5)                                                                                  │
│  │ Sponsor: Dr. James Okello          │ Manager: John Smith          │ Start: 2026-01-01 │ End: 2026-12-31 │  │
│  OBJECTIVES (#E8F5E9)                                                                                         │
│  │ ID     │ Objective                                      │ Measurable Criteria                        │  │
│  │ OBJ-01 │ Build integrated SNA platform                  │ 90% user adoption in pilot communities     │  │
│  │ OBJ-02 │ Enable offline data collection                 │ < 10% data loss in offline mode            │  │
│  SCOPE (#FFF3E0)                                                                                              │
│  │ IN SCOPE: Patient Reg • EMR • Lab • Billing    │  OUT OF SCOPE: Inventory • HR • AI Diagnostics   │  │
│  STAKEHOLDERS (#F3E5F5)                                                                                      │
│  │ S-001 │ Dr. James Okello │ Sponsor │ Ministry of Health │ Project success, policy alignment          │  │
│  CONSTRAINTS & ASSUMPTIONS (#FFEBEE)                                                                          │
│  │ Constraints: $59,400 budget • Uganda DPA compliance    │ Assumptions: Mobile access • MoH data access │  │
│  MILESTONES (#E0F7FA)                                                                                         │
│  │ M1 Charter Approved 2026-01-15 │ M2 Requirements 2026-04-15 │ M3 Design 2026-06-15 │ M4 Go-Live 2026-12-15│
│  BUDGET SUMMARY (#FFF8E1)                                                                                     │
│  │ Personnel $31,000 52% │ Hardware $18,500 31% │ Software $1,500 │ Training $3,000 │ TOTAL $59,400       │  │
│  APPROVALS (#F5F5F5)                                                                                          │
│  │ Sponsor: Dr. James Okello │ PM: John Smith │ Steering: Dr. Sarah Nambi │ Signature ___ Date ___        │  │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  Page 1 of 1                          CONFIDENTIAL - Internal Use Only                                        │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Layout regions (top → bottom):**

| Priority | Section | Height driver |
|----------|---------|---------------|
| 1 | Title block | Fixed 1.2 in |
| 2 | Vision | 1.2 in + text wrap |
| 3 | Project Overview | 2.0 in (key-value pairs) |
| 4 | Objectives | 1.0 + 0.5 × row count |
| 5 | Scope | 2.5 in (two-column bullets) |
| 6 | Stakeholders | 1.0 + 0.5 × row count |
| 7 | Constraints & Assumptions | 2.0 in |
| 8 | Milestones | 1.0 + 0.5 × row count |
| 9 | Budget Summary | 3.5 in (table + distribution) |
| 10 | Approvals | 2.0 in |
| 11 | Footer | Fixed 0.5 in |

---

## 4. Environment Setup & Dependencies

For this generator to operate reliably across massive corporate environments, strict adherence to the environment setup is required.

### System Requirements
*   **Python:** 3.10+
*   **Graphviz:** Required for compiling `format: "graphviz"` diagram descriptions to SVG (`dot -Tsvg`).
    *   *Ubuntu/Debian:* `sudo apt-get install graphviz`
    *   *macOS:* `brew install graphviz`
*   **D2 (optional):** Alternative compiler for `format: "d2"` diagram descriptions.
    *   Install from [d2lang.com](https://d2lang.com) and set `D2_PATH` in `.env`.
*   **Java Runtime Environment (JRE):** Version 11+. Required by `aspose-diagram` (JPype).
*   **LibreOffice/soffice:** Optional, used as a fallback engine for DOCX to PDF conversion if native tools are unavailable.

### Python Dependencies (`requirements.txt`)
Create a strict virtual environment to prevent dependency conflicts:

```bash
python3.10 -m venv charter_env
source charter_env/bin/activate
pip install -r requirements.txt
```

**requirements.txt:**
```text
pydantic>=2.0.0
python-docx>=1.1.0
python-dotenv>=1.0.0
graphviz>=0.20.1
PyYAML>=6.0.1
aspose-diagram>=23.10.0
JPype1>=1.5.0
```

### Environment Variables (`.env`)
Create a `.env` file in the root directory to store system-specific paths and licenses:

```env
# Graphviz Binaries
GRAPHVIZ_DOT_PATH=/usr/local/bin/dot

# D2 CLI (optional)
D2_PATH=d2

# Aspose License Path (Required to remove watermarks on .vsdx output)
ASPOSE_DIAGRAM_LICENSE_PATH=/opt/licenses/Aspose.Diagram.lic

# Output configurations
DEFAULT_CHARTER_OUTPUT_DIR=./output
```

### Docker Setup
For sandbox execution, use the following `Dockerfile`:

```dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y \
    graphviz \
    libgraphviz-dev \
    default-jre \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["python", "cli.py"]
```

---

## 5. Input Specification (JSON/YAML Schema)

The generator accepts a structured payload plus **seven required diagram description files** (see [project_charter_generator/PROMPT.md](project_charter_generator/PROMPT.md)).

### 5.1 Shared narrative (four split files)

`charter_project_input.json`, `charter_content_input.json`, `charter_people_input.json`, `charter_schedule_risk_input.json`

### 5.2 Diagram descriptions (seven split files — required for Word)

Each file contains a `diagram_description` object. The compiler produces Graphviz `.dot` or D2 `.d2` source, then a layout dict for native Word DrawingML embedding (SVG archive optional).

| File | Purpose |
|------|---------|
| `charter_diagram_problem_tree_input.json` | Problem tree (§9.2) |
| `charter_diagram_stakeholder_matrix_input.json` | Power-interest matrix (§5.2) |
| `charter_diagram_scope_boundary_input.json` | Scope boundary (§4.4) |
| `charter_diagram_org_chart_input.json` | Org chart (§7.2) |
| `charter_diagram_milestone_timeline_input.json` | Timeline (§10.2) |
| `charter_diagram_risk_matrix_input.json` | Risk matrix (§9.3) |
| `charter_diagram_system_context_input.json` | System context (§6.2) |

**Diagram description schema:**

```json
{
  "diagram_description": {
    "id": "problem_tree",
    "title": "Problem Tree",
    "format": "graphviz",
    "engine": "dot",
    "rankdir": "TB",
    "caption": "Figure 4: Problem Tree",
    "nodes": [
      { "id": "TRUNK", "label": "Core problem", "fill": "#FFCC80", "border": "#F57C00" }
    ],
    "edges": [
      { "from": "RSK-01", "to": "TRUNK", "color": "#666666" }
    ],
    "source": null
  }
}
```

Set `"format": "d2"` and provide either structured nodes/edges or raw `"source": "direction: down\n..."`.

Merged MAIN files include `"diagram_descriptions": { "problem_tree": {...}, ... }`.

### 5.3 Combined MAIN payload (excerpt)

```json
{
  "project": {
    "name": "Healthcare Integration Platform",
    "sponsor": "Jane Doe, VP Engineering",
    "manager": "John Smith",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "department": "IT Innovations",
    "version": "1.0"
  },
  "vision": {
    "statement": "To create a seamless, interoperable healthcare data exchange.",
    "mission": "Unify patient records across 5 regional hospitals."
  },
  "objectives": [
    {
      "id": "OBJ-01",
      "description": "Reduce data retrieval time.",
      "measurable_criteria": "Under 2 seconds per query."
    }
  ],
  "scope": {
    "in_scope": ["Patient demographics", "Billing records"],
    "out_of_scope": ["HR systems", "Payroll"],
    "boundaries": "The system ends at the hospital firewall."
  },
  "stakeholders": [
    {
      "id": "SH-01",
      "name": "Dr. House",
      "role": "Chief of Medicine",
      "organization": "General Hospital",
      "power": "High",
      "interest": "High",
      "expectations": "Zero downtime during shifts."
    }
  ],
  "constraints": ["Must comply with HIPAA regulations.", "Budget capped at $2M."],
  "assumptions": ["Existing APIs will not deprecate."],
  "risks": [
    {
      "id": "RSK-01",
      "description": "Data migration failure",
      "likelihood": 3,
      "impact": 5,
      "mitigation": "Perform dual-writes during transition."
    }
  ],
  "milestones": [
    {
      "id": "M1",
      "name": "Phase 1 Complete",
      "date": "2024-04-01",
      "deliverable": "Architecture signed off."
    }
  ],
  "budget": {
    "total": 2000000,
    "currency": "USD",
    "breakdown": {
      "personnel": 1000000,
      "hardware": 300000,
      "software": 500000,
      "training": 100000,
      "contingency": 100000
    }
  },
  "success_criteria": ["System handles 10k TPS.", "User adoption > 80%."],
  "approvals": [
    {
      "role": "Sponsor",
      "name": "Jane Doe",
      "date": "2023-12-15"
    }
  ],
  "diagrams": {
    "problem_tree": {},
    "stakeholder_map": {},
    "system_context": {},
    "org_chart": {},
    "scope_boundary": {},
    "milestone_timeline": {}
  }
}
```

### 5.4 Project Charter Summary Diagram input (single-page)

The Summary Diagram consumes the same narrative fields as Word — wrapped under `project_charter` or the flat MAIN schema:

```json
{
  "project_charter": {
    "title": "Project Charter",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    "confidentiality": "Confidential - Internal Use Only",
    "vision": {
      "statement": "To empower Ugandan communities with data-driven decision-making..."
    },
    "overview": {
      "department": "Health Informatics",
      "sponsor": "Dr. James Okello (Ministry of Health)",
      "manager": "John Smith (PMO)",
      "start_date": "2026-01-01",
      "end_date": "2026-12-31"
    },
    "objectives": [
      { "id": "OBJ-01", "description": "...", "criteria": "90% user adoption" }
    ],
    "scope": {
      "in_scope": ["Patient Registration System", "EMR"],
      "out_of_scope": ["Inventory Management", "HR Management"]
    },
    "stakeholders": [
      { "id": "S-001", "name": "Dr. James Okello", "role": "Project Sponsor",
        "organization": "Ministry of Health", "expectations": "Project success" }
    ],
    "constraints": ["Fixed budget of $59,400"],
    "assumptions": ["Community members have access to basic mobile devices"],
    "milestones": [
      { "id": "M1", "name": "Charter Approved", "date": "2026-01-15", "description": "..." }
    ],
    "budget": {
      "total": 59400, "currency": "USD", "exchange_rate": 3700,
      "categories": [
        { "name": "Personnel", "total": 31000, "percentage": 52.2 }
      ]
    },
    "approvals": [
      { "role": "Project Sponsor", "name": "Dr. James Okello", "signature": "", "date": "" }
    ]
  }
}
```

Flat MAIN schema (`project`, `vision`, `objectives`, …) is also accepted — `CharterLayoutCalculator` normalizes both forms.

---
## 6. Diagram Specifications (Analytical Diagrams)

*(See **Section 12: Diagram Visual Layouts** for exact ASCII blueprints.)*

### 6.1 Problem Tree Diagram (Graphviz + Aspose.Diagram)
*   **Layout Engine:** `dot` (Hierarchical, top-to-bottom).
*   **Structure:**
    *   **LEAF (top):** Long-term effects. Max 3 boxes. Color: `#A5D6A7` (Green).
    *   **BRANCHES (middle):** Direct effects. Max 4 boxes. Color: `#90CAF9` (Blue).
    *   **TRUNK (center):** Core problem. Exactly 1 box. Color: `#FFCC80` (Orange).
    *   **ROOTS (bottom):** Root causes. Max 5 boxes. Color: `#EF9A9A` (Red).
*   **Box Styling:**
    *   Shape: Rounded rectangle (`rx=8`, `ry=8`).
    *   Font: Arial/Helvetica, 10pt for labels.
    *   Border: Solid, 1.5pt, matching fill color.
    *   Shadow: Subtle drop shadow (offset 2, blur 4) via Visio properties or SVG filters.
*   **Connections:** Directed arrows from ROOTS → TRUNK → BRANCHES → LEAF.
*   **Arrow Styling:** Solid, Color `#666666`, Width 1pt.

### 6.2 Stakeholder Power-Interest Matrix (Graphviz + Aspose.Diagram)
*   **Layout Engine:** `neato` or custom coordinate mapping.
*   **Layout:** 2x2 grid. Power (Y-axis), Interest (X-axis).
*   **Quadrants:**
    *   **High Power, High Interest (Top Right):** RED - "Key Players"
    *   **High Power, Low Interest (Top Left):** ORANGE - "Keep Satisfied"
    *   **Low Power, High Interest (Bottom Right):** YELLOW - "Keep Informed"
    *   **Low Power, Low Interest (Bottom Left):** GREEN - "Monitor"
*   **Contents:** Each quadrant contains stakeholder names and roles. Graphviz subgraphs (`cluster`) represent quadrants.
*   **Styling:** Solid grey grid lines, bold quadrant labels in corners, stakeholder icons next to names.

### 6.3 System Context Diagram (Graphviz + Aspose.Diagram)
*   **Layout Engine:** `circo` or `fdp` (Center with surrounding entities).
*   **Center Box:** E.g., "Healthcare Ecosystem". Filled with a blue gradient.
*   **External Entities:** Arranged radially.
    *   Patients (top-left)
    *   Doctors (top-right)
    *   Ministry of Health (right)
    *   Insurance Companies (bottom-right)
    *   Pharmacies (bottom-left)
    *   Laboratories (left)
*   **Connections:** Bidirectional or directional arrows with bold text data flow labels (e.g., "Prescriptions", "Billing").
*   **Styling:** System box with heavy shadow, entities with simple rounded rectangles.

### 6.4 Project Organizational Chart (Graphviz + Aspose.Diagram)
*   **Layout Engine:** `dot` (Strict hierarchical tree, top-to-bottom).
*   **Structure:**
    *   Top: Project Sponsor
    *   Second: Project Manager
    *   Third: Team Leads (Analysis, Architecture, QA)
    *   Bottom: Team members
*   **Styling:**
    *   Manager roles: `#1565C0` (Blue fill), White text.
    *   Team leads: `#64B5F6` (Light blue fill), Dark text.
    *   Team members: `#FFFFFF` (White background), `#1565C0` border.

### 6.5 Scope Boundary Diagram (Graphviz + Aspose.Diagram)
*   **Layout Engine:** `fdp` with concentric clusters.
*   **Layout:** Concentric circle or ellipse.
*   **Inner Area:** In-scope items listed as distinct nodes inside a `cluster_in_scope` with `#4CAF50` (Green) background tint.
*   **Outer Area:** Out-of-scope items listed in a surrounding `cluster_out_scope` with `#EF9A9A` (Red) tint.
*   **Boundary Line:** The `cluster_in_scope` boundary must be Dashed, thick (3pt), color `#1565C0`.
*   **Legend:** Clear top-right legend block.

### 6.6 Milestone Timeline (Graphviz + Aspose.Diagram)
*   **Layout Engine:** `dot` with `rankdir=LR` (Left to Right).
*   **Structure:**
    *   Horizontal spine representing the timeline.
    *   Milestone nodes attached above the spine with date labels.
    *   Phase box intervals attached below the spine.
    *   Arrows representing strict dependencies between milestones.
*   **Styling:** Clean, minimal, using Primary Blue `#1565C0` for the timeline spine.

---

## 7. Word Document Layout & Sections

Word styling is defined in **Section 2.2** (`word_document` block). The `python-docx` builder constructs the document in this sequence:

```text
PROJECT CHARTER
[Project Name]
[Version] | [Date]

TABLE OF CONTENTS
(Generated automatically using Word field codes {TOC \o "1-3" \h \z \u})

1. EXECUTIVE SUMMARY
   - Auto-generated paragraph blending project name, sponsor, and vision.
   - Key highlights (budget, timeframe).

2. PROJECT OVERVIEW
   - 2.1 Project Name
   - 2.2 Project Sponsor
   - 2.3 Project Manager  
   - 2.4 Department/Division
   - 2.5 Start Date
   - 2.6 End Date

3. VISION & OBJECTIVES
   - 3.1 Vision Statement (Bold, Italic)
   - 3.2 Mission Statement
   - 3.3 SMART Objectives (Rendered as a styled Table)
     | ID | Objective | Measurable Criteria |

4. SCOPE
   - 4.1 In-Scope (Bullet list)
   - 4.2 Out-of-Scope (Bullet list)
   - 4.4 Scope Diagram (Embedded **DrawingML shape** diagram, captioned "Figure 1: Scope Boundaries")

5. STAKEHOLDERS
   - 5.1 Stakeholder Register (Table)
     | ID | Name | Role | Power | Interest |
   - 5.2 Stakeholder Matrix (Embedded **DrawingML shape** diagram, captioned)

6. SYSTEM CONTEXT
   - 6.1 Description
   - 6.2 Context Diagram (Embedded **DrawingML shape** diagram, captioned)

7. PROJECT ORGANIZATION
   - 7.1 Team Structure
   - 7.2 Org Chart (Embedded **DrawingML shape** diagram, captioned)

8. CONSTRAINTS & ASSUMPTIONS
   - 8.1 Constraints (Bullet list)
   - 8.2 Assumptions (Bullet list)

9. RISKS
   - 9.1 Risk Register (Table with conditional cell shading based on Impact)
     | ID | Risk | Likelihood | Impact | Mitigation |
   - 9.2 Problem Tree Analysis (Embedded **DrawingML shape** diagram, captioned)

10. MILESTONES
    - 10.1 Milestone Schedule (Table)
      | ID | Milestone | Date | Deliverable |
    - 10.2 Timeline (Embedded **DrawingML shape** diagram, captioned)

11. BUDGET
    - 11.1 Budget Breakdown (Table)
      | Category | Amount |
    - 11.2 Budget Summary (Table — pie chart optional in Word; full chart in Summary Diagram)

12. SUCCESS CRITERIA
    - Bullet list of success criteria.

13. APPROVALS
    - 13.1 Sign-off Table
      | Role | Name | Signature | Date |

APPENDICES
   - A. Detailed Risk Register
   - B. Detailed Stakeholder Analysis
   - C. Glossary
```

---

## 8. Code Architecture & Implementation

```text
project_charter_generator/
├── cli.py                          # merge + build subcommands
├── core/
│   ├── charter_builder.py          # build_charter() orchestrator
│   ├── input_merger.py             # Merge split JSON → MAIN files
│   ├── validator.py                # validate_payload()
│   ├── models.py
│   └── errors.py                   # PC-001…PC-010
├── diagrams/
│   ├── description_schema.py       # Diagram description pydantic models
│   ├── source_builder.py           # JSON → DOT or D2 source
│   ├── xml_pipeline.py             # DOT/D2 → SVG XML
│   ├── word_diagram_pipeline.py    # Compile descriptions for Word
│   ├── auto_descriptions.py        # Fallback auto-generate from narrative
│   ├── aspose_renderer.py          # Multi-page Visio deck (7 pages)
│   ├── layouts.py                  # layout_*() for analytical diagrams
│   └── charter_summary_builder.py  # Single-page executive poster
├── schedulers/
│   └── charter_layout_calculator.py # Section Y-position calculator
├── word/
│   ├── document_builder.py         # 13-section Word doc
│   ├── drawingml_inserter.py       # Embed native editable shapes in .docx
│   ├── svg_inserter.py             # PNG fallback only (SVG not visible in Word)
│   └── styler.py
├── config/
│   └── settings.py                 # Graphviz, D2, Aspose license
└── examples/split/                 # Da'atSNA sample inputs
```

**Pipeline:** `cli.py build` → `validate_payload()` → `build_charter()` → Word (DrawingML shapes) + Visio deck + Summary Diagram.

### 8.1 Orchestrator (`core/charter_builder.py`)

```python
MIN_DOCX_BYTES = 8_000
MIN_VSDX_BYTES = 5_000

def build_charter(json_payload, output_dir, word_only=False, visio_only=False):
    validate_payload(json_payload)
    if not visio_only:
        word_diagrams = compile_word_diagrams(json_payload, output_dir)
        build_word_document(json_payload, word_diagrams, f"{output_dir}/project-charter.docx")
    if not word_only:
        build_visio_deck(json_payload, {}, f"{output_dir}/visio/project-charter.vsdx")
        build_charter_summary(json_payload, f"{output_dir}/visio/charter-summary.vsdx")
        verify_all_outputs(outputs)
```

### 8.2 Charter Layout Calculator (`schedulers/charter_layout_calculator.py`)

Computes vertical section placement for the single-page Summary Diagram:

```python
@dataclass
class CharterSection:
    id: str
    title: str
    height: float
    x: float
    y: float
    width: float

class CharterLayoutCalculator:
    def __init__(self, page_width=59.4, page_height=42.0, margin=0.5):
        self.available_width = page_width - (margin * 2)
        self.current_y = page_height - margin - 1.5  # below title block

    def calculate_section_heights(self, data: dict) -> Dict[str, float]:
        return {
            "vision": 1.2,
            "overview": 2.0,
            "objectives": 1.0 + len(data.get("objectives", [])) * 0.5 + 0.3,
            "scope": 2.5,
            "stakeholders": 1.0 + len(data.get("stakeholders", [])) * 0.5 + 0.3,
            "constraints": 2.0,
            "milestones": 1.0 + len(data.get("milestones", [])) * 0.5 + 0.3,
            "budget": 3.5,
            "approvals": 2.0,
        }

    def add_section(self, section_id, title, height) -> CharterSection:
        section = CharterSection(section_id, title, height, self.margin, self.current_y, self.available_width)
        self.current_y -= height + 0.3
        return section
```

### 8.3 Visio Renderers

**Multi-page deck** (`diagrams/aspose_renderer.py` → `build_visio_deck()`):

- Uses `asposediagram.api` via JPype — not `from aspose.diagram import …`
- Seven pages from `layouts.py`: problem tree, stakeholder matrix, scope, org chart, milestone timeline, risk matrix, system context

**Summary Diagram** (`diagrams/charter_summary_builder.py`):

1. `CharterLayoutCalculator` computes section Y positions
2. For each section: colored header bar + content box via `add_rectangle()`
3. Tables: objectives, stakeholders, milestones, budget, approvals
4. Footer: confidentiality notice
5. Output: `visio/charter-summary.vsdx` — verified via Aspose reload

### 8.4 Word + SVG Pipeline

```python
# diagrams/word_diagram_pipeline.py
word_diagrams = compile_word_diagrams(payload, output_dir)  # → {id: svg_path}

# word/drawingml_inserter.py — embeds native editable shapes, not images
insert_svg_figure(doc, svg_path, width_inches=6.0, caption="Figure 1: Scope Boundaries")
```

### 8.5 Color Palette Reference

All hex codes are defined in **Section 2.2**. Analytical diagram tier colors live in `diagrams/layouts.py` (`TIER_COLORS`, `QUADRANT_STYLES`, `RISK_COLORS`).

---

## 9. Error Handling

To ensure absolute reliability in automated environments, all failures must raise specific `CharterGenerationError` exceptions mapped to strict error codes.

| Error Code | Description | Resolution |
|---|---|---|
| `PC-001` | Invalid input JSON schema | Validate against schema using `jsonschema`. |
| `PC-002` | Missing required field | Check field presence in `core/validator.py`. |
| `PC-003` | Invalid field value | Check format (e.g., YYYY-MM-DD for dates). |
| `PC-004` | Graphviz not installed | Ensure `dot` is in PATH. Catch `FileNotFoundError` on `subprocess.run(['dot'])`. |
| `PC-005` | Java not installed | Required by Aspose. Check JRE installation. |
| `PC-006` | Aspose.Diagram license missing | Configure `.env` `ASPOSE_DIAGRAM_LICENSE_PATH`. |
| `PC-007` | Word document generation failed | Catch `docx` library exceptions. |
| `PC-008` | Diagram rendering timeout | Increase `subprocess` timeout limit. |
| `PC-009` | Insufficient disk space | Catch `IOError` during save. Free up space. |
| `PC-010` | Permission denied | Catch `PermissionError`. Verify directory permissions. |

---

## 10. Output Directory Structure

The CLI will produce a strictly defined directory tree for the user:

```text
output/
├── project-charter.docx          # Primary Word document
├── project-charter.pdf            # PDF version (if LibreOffice is present)
├── diagrams/
│   ├── source/                   # .dot / .d2 compiled from descriptions
│   └── svg/                      # SVG archive (reference; Word uses DrawingML shapes)
├── visio/
│   ├── project-charter.vsdx      # Aspose 7-page analytical deck
│   └── charter-summary.vsdx      # Single-page executive poster (target)
└── artifacts/
    ├── input.json                 # Backup of parsed input payload
    ├── positions.json             # Cached Graphviz coordinate layouts
    └── logs/                      # Verbose debug logs
```

---

## 11. Quality Checklist

### Visual
- [ ] Professional color palette used consistently (Section 2.2)
- [ ] All Summary Diagram sections properly labeled with colored headers
- [ ] Clean white backgrounds; subtle shadows on section boxes
- [ ] No text overflow in Visio shapes or Word tables
- [ ] All fonts Arial (Visio) / Calibri (Word)
- [ ] Title block `#1a237e` on Summary Diagram

### Content
- [ ] Vision statement clear and concise
- [ ] All key stakeholders listed with roles and expectations
- [ ] Objectives are SMART with measurable criteria
- [ ] Scope clearly defined (in-scope / out-of-scope)
- [ ] Constraints and assumptions documented
- [ ] Milestones with dates and descriptions
- [ ] Budget breakdown complete with totals
- [ ] Approval section with signature lines

### Layout
- [ ] Summary Diagram sections logically ordered top → bottom
- [ ] Proper spacing between sections (0.3 in gap)
- [ ] Tables correctly aligned with alternating row colors
- [ ] Analytical diagrams render without Graphviz syntax errors
- [ ] Word document contains all 13 H1 sections
- [ ] Footer with confidentiality notice on Summary Diagram

### Professional / QA
- [ ] Consulting-grade visual quality suitable for executives
- [ ] Word embeds native DrawingML shapes — not PNG raster images
- [ ] Visio deck (`.vsdx`) ≥ 5 KB; Word (`.docx`) ≥ 8 KB
- [ ] Visio opens natively without repair prompts
- [ ] All shapes discrete and editable (not flat images)
- [ ] Consistent colors across Word tables and Visio diagrams

---

## 12. Diagram Visual Layouts (Analytical)

These ASCII blueprints dictate the exact visual layout for both the Graphviz calculations and the Aspose.Diagram rendering logic. 

### 12.1 Problem Tree Diagram

```text
                               ┌──────────────────────────┐
                               │      LEAF - Effects      │
                               ├──────────────────────────┤
                               │  Persistent exclusion    │
                               │  of youth, women &       │
                               │  informal workers        │
                               └────────────┬─────────────┘
                                            │
                               ┌────────────┴─────────────┐
                               │  Informal economy stays  │
                               │  invisible to policy     │
                               └────────────┬─────────────┘
                                            │
                     ┌──────────────────────┼──────────────────────┐
                     │                      │                      │
          ┌──────────┴──────────┐ ┌────────┴────────┐ ┌──────────┴──────────┐
          │    BRANCH: Direct   │ │   BRANCH: NGO   │ │    BRANCH: Field    │
          │    Effects 1        │ │   Targeting     │ │    Researchers      │
          ├─────────────────────┤ ├─────────────────┤ ├─────────────────────┤
          │  Cooperatives can't │ │  Interventions  │ │  No low-cost tools  │
          │  identify influence │ │  poorly targeted│ │  for offline data   │
          └─────────────────────┘ └─────────────────┘ └─────────────────────┘
```
*   **Box Dimensions:** 30x6 chars (approx 200x80 pixels).
*   **Color Coding:** LEAF `[LIGHT GREEN]`, BRANCH `[BLUE]`, TRUNK `[ORANGE]`, ROOTS `[LIGHT RED]`.
*   **Connectors:** Orthogonal (`routingStyle=RightAngle`).
*   **Legend:** None required.
*   **Relationships:** Directed arrows flowing upwards from ROOTS to LEAF.

### 12.2 Stakeholder Power-Interest Matrix

```text
                             HIGH POWER
                     ┌────────────────────────────┐
                     │   HIGH POWER / HIGH INTEREST│
                     │   ┌───────────────────────┐ │
                     │   │  • Project Sponsor    │ │
                     │   │  • Ministry of Health │ │
                     │   │  • Hospital CEO       │ │
                     │   └───────────────────────┘ │
                     │                            │
                     │   HIGH POWER / LOW INTEREST │
                     │   ┌───────────────────────┐ │
                     │   │  • Insurance Company  │ │
                     │   │  • Board of Directors │ │
                     │   └───────────────────────┘ │
                     └────────────────────────────┘
                                         HIGH INTEREST
```
*   **Dimensions:** 2x2 grid, each quadrant ~40x15 chars.
*   **Color Coding:** HP/HI `[RED]`, HP/LI `[ORANGE]`, LP/HI `[AMBER]`, LP/LI `[GREEN]`.
*   **Connectors:** None (Grid layout).
*   **Legend:** Top-Right corner of diagram.
*   **Relationships:** Implicit by spatial placement.

### 12.3 System Context Diagram

```text
                        ┌──────────────────┐
                        │    Patients      │
                        └────────┬─────────┘
                                 │  ┌──────────┐
                                 ▼  │   Data   │
                   ┌──────────────────────────────┐
                   │                              │
    ┌──────────────┤      HEALTHCARE             ├──────────────┐
    │              │      ECOSYSTEM              │              │
    │  Doctors     │                              │  Lab Systems │
    └──────────────┤                              ├──────────────┘
                   │                              │
                   └──────────────────────────────┘
                        │                │
                        ▼                ▼
                    ┌──────────┐   ┌──────────┐
                    │ Pharm.   │   │Ministry  │
                    └──────────┘   └──────────┘
```
*   **Box Dimensions:** Center System (40x10), External Entities (20x4).
*   **Color Coding:** Center `[PRIMARY BLUE Gradient]`, Entities `[LIGHT BLUE]`.
*   **Connectors:** Direct/Straight lines.
*   **Legend:** Bottom-Left.
*   **Relationships:** Bidirectional data flows with text labels.

### 12.4 Project Organizational Chart

```text
                        ┌──────────────────────────┐
                        │    Project Sponsor       │
                        └───────────┬──────────────┘
                                    │
                        ┌───────────┴──────────────┐
                        │    Project Manager       │
                        └───────────┬──────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
    ┌─────────┴─────────┐ ┌─────────┴─────────┐ ┌─────────┴─────────┐
    │  Analysis Team    │ │  Architecture     │ │  Development      │
    │  Lead: Alice      │ │  Lead: Bob        │ │  Lead: Charlie    │
    ├───────────────────┤ ├───────────────────┤ ├───────────────────┤
    │  • Analyst 1      │ │  • Solution Arch  │ │  • Dev Lead       │
    │  • Analyst 2      │ │  • Data Arch      │ │  • Senior Dev     │
    └───────────────────┘ └───────────────────┘ └───────────────────┘
```
*   **Box Dimensions:** 25x8 chars.
*   **Color Coding:** Managers `[PRIMARY BLUE]`, Leads `[LIGHT BLUE]`, Members `[WHITE]`.
*   **Connectors:** Orthogonal.
*   **Legend:** None required.
*   **Relationships:** Hierarchical reporting lines (top-down).

### 12.5 Scope Boundary Diagram

```text
                    ┌─────────────────────────────┐
                    │     OUT OF SCOPE (RED)      │
                    │                             │
                    │   ┌───────────────────────┐ │
                    │   │   IN SCOPE (GREEN)    │ │
                    │   │                       │ │
                    │   │  • Patient Reg        │ │
                    │   │  • Appointments       │ │
                    │   │  • EMR                │ │
                    │   │  • Prescriptions      │ │
                    │   │  • Lab Integration    │ │
                    │   │                       │ │
                    │   └───────────────────────┘ │
                    │                             │
                    │   • Inventory System        │
                    │   • HR Management           │
                    │   • Advanced AI             │
                    └─────────────────────────────┘
```
*   **Dimensions:** Concentric bounding boxes/circles.
*   **Color Coding:** Inner `[GREEN]`, Outer `[RED]`.
*   **Connectors:** None.
*   **Legend:** Top-Right.
*   **Relationships:** Spatial containment.

### 12.6 Milestone Timeline

```text
    ┌──────────────────────────────────────────────────────────────────┐
    │   PHASE 1      │   PHASE 2      │   PHASE 3      │   PHASE 4   │
    │   Discovery    │   Design       │   Develop      │   Deploy    │
    └──────────────────────────────────────────────────────────────────┘
    │    │           │    │           │    │           │    │        │
    ▼    ▼           ▼    ▼           ▼    ▼           ▼    ▼        ▼
    ●────●───────────●────●───────────●────●───────────●────●────────●
    │    │           │    │           │    │           │    │        │
    │    │           │    │           │    │           │    │        │
    │    │           │    │           │    │           │    │        │
    │  M1            M2   M3          M4   M5          M6   M7      M8
    │  Feb 15        Mar 1 Mar 15     Apr 1 Apr 15    May 1 Jun 15  Jun 30
    │
    │  Legend: ● = Milestone, │ = Phase Boundary
    └──────────────────────────────────────────────────────────────────┘
```
*   **Dimensions:** Variable width based on duration.
*   **Color Coding:** Spine `[PRIMARY BLUE]`, Markers `[DARK BLUE]`.
*   **Connectors:** Straight horizontal line.
*   **Legend:** Bottom-Left.
*   **Relationships:** Sequential dependencies.

### 12.7 Risk Matrix (Heat Map)

```text
                     IMPACT
                    1    2    3    4    5
                  ┌────┬────┬────┬────┬────┐
                5 │    │    │    │    │ ██ │  CRITICAL
                  ├────┼────┼────┼────┼────┤
                4 │    │    │    │ ██ │ ██ │  HIGH
    LIKELIHOOD  3 ├────┼────┼────┼────┼────┤
                2 │    │    │ ██ │ ██ │ ██ │  MEDIUM
                  ├────┼────┼────┼────┼────┤
                1 │    │ ██ │ ██ │ ██ │ ██ │  LOW
                  └────┴────┴────┴────┴────┘
```
*   **Dimensions:** 5x5 grid cells.
*   **Color Coding:** Critical `[RED]`, High `[ORANGE]`, Medium `[AMBER]`, Low `[GREEN]`.
*   **Connectors:** None.
*   **Legend:** Right side.
*   **Relationships:** Coordinate mapping based on Likelihood/Impact.

---

## 13. Usage Examples

### 13.1 Merge split inputs into MAIN files
```bash
cd project_charter_generator
python cli.py merge examples/split --validate
```

### 13.2 Build full charter (Word + Visio deck)
```bash
python cli.py build examples/split/charter_input.json -o ./output
```

### 13.3 Word document only
```bash
python cli.py build examples/split/charter_word_input.json -o ./output --word-only
```

### 13.4 Visio deck only
```bash
python cli.py build examples/split/charter_visio_input.json -o ./output --visio-only
```

### 13.5 Validate without building
```bash
python cli.py build examples/split/charter_input.json --validate-only -v
```

### 13.6 National Integrated Healthcare Ecosystem sample
```bash
python cli.py build national-integrated-healthcare-ecosystem/inputs/charter_input.json \
  -o national-integrated-healthcare-ecosystem/output
```

---

## 14. Integration with Existing Skills

The Project Charter Generator integrates with sibling skills in the UML-SKILLS suite:

| Charter section | Downstream skill | Output |
|-----------------|------------------|--------|
| Schedule & milestones | `gantt-chart-generator-SKILL.md` | Gantt `.vsdx` |
| Critical path | `cpm-network-diagram-generator-SKILL.md` | CPM network `.vsdx` |
| Budget breakdown | `budget-breakdown-generator-SKILL.md` | Budget Visio + Excel |
| Communication flows | `communication-diagram-generator-SKILL.md` | Collaboration `.vsdx` |
| UML architecture | `uml-diagram-generator-SKILL.md` | Class/sequence `.vsdx` |

Charter `milestones` and `budget` JSON blocks pipe directly to downstream CLIs.

---

## 15. Testing Strategy

1. **Merge test:** Nine split files → three MAIN files; shared sections identical across Word/Visio/combined MAIN.
2. **Validation test:** Missing `vision.statement` triggers `PC-002`.
3. **DrawingML pipeline:** All seven diagrams produce layout dicts with ≥1 node each; DOCX contains `wordprocessingGroup` elements.
4. **Word QA:** Output `.docx` ≥ 8 KB; all 13 sections present.
5. **Visio deck QA:** Output `.vsdx` ≥ 5 KB; seven pages render.
6. **Summary Diagram height:** `CharterLayoutCalculator` fits all sections within A2 height (42 in).
7. **Color consistency:** Section header fills match Section 2.2 hex codes.
8. **Cross-file consistency:** Stakeholder IDs match between register table and stakeholder matrix diagram.

---

## 16. Troubleshooting Guide

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Graphviz `dot` not recognized (`PC-004`) | Graphviz not in PATH | `brew install graphviz` / `apt-get install graphviz` |
| Visio evaluation watermark (`PC-006`) | Missing Aspose license | Set `ASPOSE_DIAGRAM_LICENSE_PATH` in `.env` |
| `.vsdx` < 5 KB | JVM/Aspose failure | Install JRE 11+; verify `aspose-diagram` + `JPype1` |
| `.docx` < 8 KB | Word build failed silently | Run with `-v`; check `word/document_builder.py` logs |
| Blank TOC in Word | Field codes not updated | Open in Word → right-click TOC → Update Field |
| Diagrams not editable in Word | Used PNG/SVG image embed | Use `word/drawingml_inserter.py` for native shapes |
| Section overflow on Summary Diagram | Too many stakeholders/objectives | Increase section height calc or split to page 2 |
| Wrong import error | `aspose.diagram` | Use `asposediagram.api` via JPype (Section 8.3) |
| Diagram description missing | Split file not authored | Create all seven `charter_diagram_*_input.json` files |
| Merge mismatch | Split files out of sync | Re-run `cli.py merge --validate` |

**Validation-only:**

```bash
python cli.py build examples/split/charter_input.json --validate-only -v
```

**End-to-end test:**

```bash
cd project_charter_generator
.venv/bin/python cli.py build examples/split/charter_input.json -o ./output -v
```

**For deeper diagram layout issues, consult [`uml-diagram-generator-SKILL.md`](uml-diagram-generator-SKILL.md) §11.**
