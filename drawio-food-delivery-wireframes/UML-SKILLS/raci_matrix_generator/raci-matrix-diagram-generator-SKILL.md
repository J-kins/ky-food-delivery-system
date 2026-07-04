---
name: raci-matrix-diagram-generator
description: Generate professional RACI Matrix (Responsibility Assignment Matrix) diagrams in fully editable Visio format (.vsdx) using Aspose.Diagram for Python. Maps Tasks (rows) against Roles (columns) with color-coded R/A/C/I codes and auto-computes gap analysis.
---

# RACI Matrix Diagram Generator Skill

This production-grade skill generates **RACI Matrices (Responsibility Assignment Matrices)** in Microsoft Visio (`.vsdx`) format. Where the Resource Allocation Matrix (`resource-allocation-matrix-generator`) focuses on *percentage-based load distribution*, the RACI Matrix focuses exclusively on *categorical accountability mapping* — Who is **Responsible**, who is **Accountable**, who is **Consulted**, and who is **Informed** for each project task or deliverable.

Utilizing `Aspose.Diagram for Python`, this tool mathematically constructs a color-coded tabular grid of Tasks (rows) × Roles (columns), validates that every task has exactly one Accountable party, detects responsibility gaps, and generates a statistical summary.

This tool functions as a standalone deliverable or as an integrated sub-component of the broader `project-charter-generator`.

## Table of Contents
1. Core Output Specifications
2. Environment Setup & Dependencies
3. Input Specification (JSON/YAML Schema)
4. RACI Matrix Visual Layout (ASCII Blueprint)
5. RACI Definitions & Validation Rules
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

The primary purpose of this skill is to generate a complete RACI Matrix that guarantees:
1. **Task × Role Grid:** A precise tabular grid — Tasks on rows, Roles on columns — auto-fitted to the Visio page.
2. **Color-Coded Cells:** Each cell filled with the RACI code-specific color: Red for R, Blue for A, Amber for C, Green for I, and neutral grey for `-`.
3. **Phase Grouping:** Tasks grouped by phase with a distinct phase separator row.
4. **Accountability Validation:** Every task row is validated to contain exactly one `A`. Any missing or duplicate `A` flags an error.
5. **Column Totals:** A footer row showing `R:X A:Y C:Z I:W` distribution counts per role.
6. **Gap Analysis:** An automated summary detecting overloaded roles, underutilized roles, tasks without `R`, and tasks without `A`.
7. **Professional Formatting:** Fully editable, corporate-themed Microsoft Visio shapes (`.vsdx`).

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

The generator enforces a strict schema requiring `roles` (columns) and `tasks` (rows), each with an embedded `raci` dictionary mapping Role IDs to RACI codes.

```json
{
  "raci_matrix": {
    "title": "RACI Matrix - Responsibility Assignment",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    "sprint": "Sprint 5",
    "description": "RACI matrix showing roles and responsibilities",

    "roles": [
      {
        "id": "R1",
        "name": "Project Sponsor",
        "person": "Dr. James",
        "department": "Executive",
        "color": "#1a237e",
        "text_color": "#FFFFFF",
        "order": 1
      },
      {
        "id": "R2",
        "name": "Project Manager",
        "person": "John Smith",
        "department": "PMO",
        "color": "#1565C0",
        "text_color": "#FFFFFF",
        "order": 2
      },
      {
        "id": "R3",
        "name": "Lead BA",
        "person": "Sarah Johnson",
        "department": "Business Analysis",
        "color": "#2E7D32",
        "text_color": "#FFFFFF",
        "order": 3
      },
      {
        "id": "R4",
        "name": "Solution Architect",
        "person": "Mike Chen",
        "department": "Architecture",
        "color": "#E65100",
        "text_color": "#FFFFFF",
        "order": 4
      },
      {
        "id": "R5",
        "name": "Dev Lead",
        "person": "Emily Davis",
        "department": "Development",
        "color": "#6A1B9A",
        "text_color": "#FFFFFF",
        "order": 5
      },
      {
        "id": "R6",
        "name": "QA Lead",
        "person": "David Wilson",
        "department": "Quality Assurance",
        "color": "#C62828",
        "text_color": "#FFFFFF",
        "order": 6
      },
      {
        "id": "R7",
        "name": "Ops Lead",
        "person": "Lisa Brown",
        "department": "Operations",
        "color": "#00838F",
        "text_color": "#FFFFFF",
        "order": 7
      },
      {
        "id": "R8",
        "name": "UX Lead",
        "person": "Tom Adams",
        "department": "UX Design",
        "color": "#4E342E",
        "text_color": "#FFFFFF",
        "order": 8
      },
      {
        "id": "R9",
        "name": "Security Officer",
        "person": "Anna Kim",
        "department": "Security",
        "color": "#B71C1C",
        "text_color": "#FFFFFF",
        "order": 9
      },
      {
        "id": "R10",
        "name": "Compliance Officer",
        "person": "Mark Okonkwo",
        "department": "Compliance",
        "color": "#4A148C",
        "text_color": "#FFFFFF",
        "order": 10
      }
    ],

    "tasks": [
      {
        "id": "T1",
        "name": "Project Charter Development",
        "description": "Create and approve project charter",
        "phase": "Initiation",
        "phase_order": 1,
        "order": 1,
        "raci": {
          "R1": "A", "R2": "C", "R3": "C", "R4": "C",
          "R5": "I", "R6": "I", "R7": "I", "R8": "I",
          "R9": "C", "R10": "C"
        }
      },
      {
        "id": "T2",
        "name": "Team Assembly",
        "description": "Recruit and onboard project team",
        "phase": "Initiation",
        "phase_order": 1,
        "order": 2,
        "raci": {
          "R1": "I", "R2": "R", "R3": "C", "R4": "I",
          "R5": "I", "R6": "I", "R7": "C", "R8": "I",
          "R9": "I", "R10": "I"
        }
      },
      {
        "id": "T3",
        "name": "Requirements Elicitation",
        "description": "Gather requirements from stakeholders",
        "phase": "Requirements",
        "phase_order": 2,
        "order": 3,
        "raci": {
          "R1": "I", "R2": "I", "R3": "R", "R4": "C",
          "R5": "I", "R6": "I", "R7": "I", "R8": "C",
          "R9": "C", "R10": "A"
        }
      },
      {
        "id": "T4",
        "name": "Requirements Analysis",
        "description": "Analyze and prioritize requirements",
        "phase": "Requirements",
        "phase_order": 2,
        "order": 4,
        "raci": {
          "R1": "I", "R2": "I", "R3": "R", "R4": "C",
          "R5": "I", "R6": "I", "R7": "I", "R8": "C",
          "R9": "C", "R10": "C"
        }
      },
      {
        "id": "T5",
        "name": "Requirements Specification",
        "description": "Document requirements in SRS",
        "phase": "Requirements",
        "phase_order": 2,
        "order": 5,
        "raci": {
          "R1": "I", "R2": "A", "R3": "R", "R4": "C",
          "R5": "I", "R6": "I", "R7": "I", "R8": "C",
          "R9": "C", "R10": "C"
        }
      },
      {
        "id": "T6",
        "name": "System Design",
        "description": "Design system architecture",
        "phase": "Design",
        "phase_order": 3,
        "order": 6,
        "raci": {
          "R1": "I", "R2": "I", "R3": "A", "R4": "R",
          "R5": "C", "R6": "I", "R7": "I", "R8": "C",
          "R9": "C", "R10": "C"
        }
      },
      {
        "id": "T7",
        "name": "Database Design",
        "description": "Design database schema",
        "phase": "Design",
        "phase_order": 3,
        "order": 7,
        "raci": {
          "R1": "I", "R2": "I", "R3": "C", "R4": "R",
          "R5": "C", "R6": "I", "R7": "I", "R8": "I",
          "R9": "C", "R10": "C"
        }
      },
      {
        "id": "T8",
        "name": "API Design",
        "description": "Design RESTful APIs",
        "phase": "Design",
        "phase_order": 3,
        "order": 8,
        "raci": {
          "R1": "I", "R2": "I", "R3": "C", "R4": "A",
          "R5": "R", "R6": "I", "R7": "I", "R8": "I",
          "R9": "C", "R10": "C"
        }
      },
      {
        "id": "T9",
        "name": "UI/UX Design",
        "description": "Design user interface",
        "phase": "Design",
        "phase_order": 3,
        "order": 9,
        "raci": {
          "R1": "I", "R2": "I", "R3": "C", "R4": "C",
          "R5": "I", "R6": "I", "R7": "I", "R8": "R",
          "R9": "C", "R10": "C"
        }
      },
      {
        "id": "T10",
        "name": "Backend Development",
        "description": "Build backend services",
        "phase": "Development",
        "phase_order": 4,
        "order": 10,
        "raci": {
          "R1": "I", "R2": "I", "R3": "C", "R4": "A",
          "R5": "R", "R6": "C", "R7": "C", "R8": "I",
          "R9": "C", "R10": "I"
        }
      },
      {
        "id": "T11",
        "name": "Frontend Development",
        "description": "Build user interfaces",
        "phase": "Development",
        "phase_order": 4,
        "order": 11,
        "raci": {
          "R1": "I", "R2": "I", "R3": "C", "R4": "C",
          "R5": "A", "R6": "C", "R7": "I", "R8": "R",
          "R9": "C", "R10": "I"
        }
      },
      {
        "id": "T12",
        "name": "System Testing",
        "description": "Test the integrated system",
        "phase": "Testing",
        "phase_order": 5,
        "order": 12,
        "raci": {
          "R1": "I", "R2": "I", "R3": "C", "R4": "C",
          "R5": "C", "R6": "R", "R7": "C", "R8": "I",
          "R9": "C", "R10": "A"
        }
      },
      {
        "id": "T13",
        "name": "Deployment",
        "description": "Deploy to production",
        "phase": "Deployment",
        "phase_order": 6,
        "order": 13,
        "raci": {
          "R1": "I", "R2": "I", "R3": "I", "R4": "C",
          "R5": "C", "R6": "C", "R7": "R", "R8": "I",
          "R9": "C", "R10": "A"
        }
      },
      {
        "id": "T14",
        "name": "Training",
        "description": "Train end users",
        "phase": "Deployment",
        "phase_order": 6,
        "order": 14,
        "raci": {
          "R1": "I", "R2": "I", "R3": "C", "R4": "I",
          "R5": "I", "R6": "I", "R7": "A", "R8": "C",
          "R9": "I", "R10": "I"
        }
      },
      {
        "id": "T15",
        "name": "Project Closure",
        "description": "Complete lessons learned and close project",
        "phase": "Closure",
        "phase_order": 7,
        "order": 15,
        "raci": {
          "R1": "A", "R2": "R", "R3": "C", "R4": "C",
          "R5": "C", "R6": "C", "R7": "C", "R8": "I",
          "R9": "C", "R10": "C"
        }
      }
    ],

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "raci_colors": {
        "R": "#E53935",
        "R_text": "#FFFFFF",
        "A": "#1565C0",
        "A_text": "#FFFFFF",
        "C": "#FFB300",
        "C_text": "#333333",
        "I": "#4CAF50",
        "I_text": "#FFFFFF",
        "-": "#E0E0E0",
        "-_text": "#757575"
      },
      "phase_header_color": "#37474F",
      "phase_header_text": "#FFFFFF",
      "cell_padding": 0.08,
      "row_height": 0.55,
      "task_col_width": 2.8,
      "role_col_width": 1.4,
      "show_descriptions": true,
      "show_phase_grouping": true,
      "shadow_enabled": false
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

## 4. RACI Matrix Visual Layout (ASCII Blueprint)

**CRITICAL REQUIREMENT:** The grid must render Tasks as rows and Roles as columns. Phase separator rows break the matrix into logical groups. The last column displays the total number of assigned roles per task.

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                      RACI MATRIX - RESPONSIBILITY ASSIGNMENT                                                                          │
│                                                Da'atSNA Community Data Platform                                                                                      │
│                                                Version 1.0  |  Sprint 5  |  2026-06-17                                                                              │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                                                      │
│  ┌────────────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────┐ │
│  │                    │   Project    │   Project   │   Lead BA   │  Solution   │  Dev Lead   │  QA Lead    │   Ops Lead  │   UX Lead   │  Security   │      │ │
│  │    TASKS           │   Sponsor    │   Manager   │  (Sarah)    │  Architect   │  (Emily)    │  (David)    │   (Lisa)    │   (Tom)     │   Officer   │ TOT. │ │
│  │                    │   (Dr.J)     │   (John)    │             │   (Mike)     │             │             │             │             │   (Anna)    │      │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │ ► PHASE 1: INITIATION                                                                                                                                     │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │  Project Charter   │  ████ A ████ │  ████ C ████ │  ████ C ████ │  ████ C ████ │  ████ I ████ │  ████ I ████ │  ████ I ████ │  ████ I ████ │  ████ C ████ │  6   │ │
│  │  Development       │              │              │              │              │              │              │              │              │              │      │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │  Team Assembly     │  ████ I ████ │  ████ R ████ │  ████ C ████ │  ████ I ████ │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ I ████ │  ████ I ████ │  4   │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │ ► PHASE 2: REQUIREMENTS                                                                                                                                   │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │  Requirements      │  ████ I ████ │  ████ I ████ │  ████ R ████ │  ████ C ████ │  ████ I ████ │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ C ████ │  6   │ │
│  │  Elicitation       │              │              │              │              │              │              │              │              │              │      │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │  Requirements      │  ████ I ████ │  ████ I ████ │  ████ R ████ │  ████ C ████ │  ████ I ████ │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ C ████ │  6   │ │
│  │  Analysis          │              │              │              │              │              │              │              │              │              │      │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │  Requirements      │  ████ I ████ │  ████ A ████ │  ████ R ████ │  ████ C ████ │  ████ I ████ │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ C ████ │  6   │ │
│  │  Specification     │              │              │              │              │              │              │              │              │              │      │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │ ► PHASE 3: DESIGN                                                                                                                                         │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │  System Design     │  ████ I ████ │  ████ I ████ │  ████ A ████ │  ████ R ████ │  ████ C ████ │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ C ████ │  6   │ │
│  │  Database Design   │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ R ████ │  ████ C ████ │  ████ I ████ │  ████ I ████ │  ████ I ████ │  ████ C ████ │  5   │ │
│  │  API Design        │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ A ████ │  ████ R ████ │  ████ I ████ │  ████ I ████ │  ████ I ████ │  ████ C ████ │  5   │ │
│  │  UI/UX Design      │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ C ████ │  ████ I ████ │  ████ I ████ │  ████ I ████ │  ████ R ████ │  ████ C ████ │  4   │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │ ► PHASE 4: DEVELOPMENT                                                                                                                                    │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │  Backend Dev       │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ A ████ │  ████ R ████ │  ████ C ████ │  ████ C ████ │  ████ I ████ │  ████ C ████ │  6   │ │
│  │  Frontend Dev      │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ C ████ │  ████ A ████ │  ████ C ████ │  ████ I ████ │  ████ R ████ │  ████ C ████ │  6   │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │ ► PHASE 5-7: TESTING / DEPLOYMENT / CLOSURE                                                                                                               │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │  System Testing    │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ C ████ │  ████ C ████ │  ████ R ████ │  ████ C ████ │  ████ I ████ │  ████ C ████ │  7   │ │
│  │  Deployment        │  ████ I ████ │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ C ████ │  ████ C ████ │  ████ R ████ │  ████ I ████ │  ████ C ████ │  6   │ │
│  │  Training          │  ████ I ████ │  ████ I ████ │  ████ C ████ │  ████ I ████ │  ████ I ████ │  ████ I ████ │  ████ A ████ │  ████ C ████ │  ████ I ████ │  4   │ │
│  │  Project Closure   │  ████ A ████ │  ████ R ████ │  ████ C ████ │  ████ C ████ │  ████ C ████ │  ████ C ████ │  ████ C ████ │  ████ I ████ │  ████ C ████ │  7   │ │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────┤ │
│  │  TOTALS            │  R:0  A:2    │  R:1  A:1    │  R:3  A:1    │  R:3  A:3    │  R:2  A:2    │  R:1  A:0    │  R:1  A:1    │  R:2  A:0    │  R:0  A:0    │  75  │ │
│  │                    │  C:2  I:11   │  C:2  I:12   │  C:9  I:3    │  C:8  I:4    │  C:6  I:7    │  C:8  I:6    │  C:7  I:7    │  C:4  I:9    │  C:12 I:3    │      │ │
│  └────────────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────┘ │
│                                                                                                                                                                      │
│  Legend:                                                                                                                                                             │
│  ═══════                                                                                                                                                             │
│  ████ R ████ = Responsible (#E53935)  ████ A ████ = Accountable (#1565C0)  ████ C ████ = Consulted (#FFB300)  ████ I ████ = Informed (#4CAF50)                      │
│                                                                                                                                                                      │
│  SUMMARY                                                                                                                                                             │
│  ═══════                                                                                                                                                             │
│  Total Tasks: 15  │  Total Roles: 9  │  Total Assignments: 75  │  Avg Assignments/Task: 5.0  │  RACI Complete: Yes                                                   │
│  R Count: 13  │  A Count: 10  │  C Count: 58  │  I Count: 49  │  Gaps: 0 tasks without A  │  Gaps: 4 tasks without R                                               │
│  Overloaded: R3/R4 (12+ assignments)  │  Underutilized: R9 Security (0 R, 0 A)  │  Gap Flag: T2 missing A-code                                                      │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. RACI Definitions & Validation Rules

### 5.1 RACI Code Definitions
| Code | Full Name | Fill Color | Text Color | Description |
|------|-----------|------------|------------|-------------|
| `R` | Responsible | `#E53935` | `#FFFFFF` | The person who executes the work. Every task must have at least 1 R. |
| `A` | Accountable | `#1565C0` | `#FFFFFF` | The single person who approves the result. Every task must have exactly 1 A. |
| `C` | Consulted | `#FFB300` | `#333333` | People who are formally consulted. Two-way communication. |
| `I` | Informed | `#4CAF50` | `#FFFFFF` | People who receive status updates. One-way communication. |
| `-` | Not Involved | `#E0E0E0` | `#757575` | No assignment for this role/task combination. |

### 5.2 Critical Validation Rules
The skill enforces the following RACI integrity rules before rendering:

| Rule ID | Name | Description |
|---------|------|-------------|
| `RULE-01` | Single Accountable | Every task must have **exactly 1** Accountable (`A`). More than one `A` per task = error `RM-005`. Zero `A` per task = error `RM-006`. |
| `RULE-02` | At Least One Responsible | Every task should have at least 1 Responsible (`R`). Zero `R` = warning flag in gap analysis. |
| `RULE-03` | No Empty Rows | Every task row must have at least 1 assignment (not all `-`). |
| `RULE-04` | Valid RACI Values | Only `R`, `A`, `C`, `I`, `-` are permitted. |
| `RULE-05` | Role Reference Integrity | Each `raci` dictionary key must match an existing Role ID. |

---

## 6. Detailed Styling Specifications

### 6.1 Cell Styling
| Property | Value | Description |
|----------|-------|-------------|
| Shape | Rectangle | Standard cell |
| Corner Radius | 0pt | Flat — tabular feel |
| Padding | `0.08in` | Tight internal padding |
| Border Width | 0.5pt | Grid lines |
| Border Color | `#BDBDBD` | Light grey |
| Row Height | `0.55in` | Standard row |
| Task Col Width | `2.8in` | Wider left label column |
| Role Col Width | `1.4in` | Per-role column |

### 6.2 Text Styling
| Element | Font Size | Weight | Alignment |
|---------|-----------|--------|-----------|
| Task Name | 9pt | Bold | Left |
| RACI Code | 12pt | Bold | Center |
| Role Name | 8pt | Bold | Center |
| Person Name | 8pt | Regular | Center |
| Phase Header | 9pt | Bold | Left |
| Totals | 8pt | Regular | Center |

### 6.3 Phase Separator Row
| Property | Value | Description |
|----------|-------|-------------|
| Fill Color | `#37474F` | Dark slate grey |
| Text Color | `#FFFFFF` | White |
| Font Weight | Bold | |
| Prefix | `►` | Arrow indicator |
| Height | `0.35in` | Compact separator |

---

## 7. Code Architecture

```text
raci_matrix_generator/
├── __init__.py
├── skill.md                       # This skill file
├── core/
│   ├── __init__.py
│   ├── diagram_builder.py         # Main grid orchestration
│   ├── validator.py               # RACI integrity checks (RULE-01 through RULE-05)
│   ├── errors.py                  # Custom exceptions
│   └── models.py                  # Pydantic schema models
├── renderers/
│   ├── __init__.py
│   ├── aspose_renderer.py         # Aspose.Diagram shape abstraction
│   ├── dot_generator.py           # PNG preview generation
│   └── layout_engine.py           # Auto-fit column width calculations
├── calculators/
│   ├── __init__.py
│   ├── raci_calculator.py         # Count R/A/C/I per row and column
│   └── gap_analyzer.py            # Identify missing R, missing A, overloaded roles
├── stylers/
│   ├── __init__.py
│   ├── color_themes.py            
│   ├── shape_styler.py            
│   ├── cell_styler.py             
│   └── phase_styler.py            
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   └── geometry_utils.py
├── templates/
│   └── raci_template.vstx         
├── config/
│   ├── __init__.py
│   └── settings.py                
└── cli.py                         
```

---

## 8. Core Implementation Code

### 8.1 Diagram Builder (`core/diagram_builder.py`)

```python
from aspose.diagram import Diagram, SaveFileFormat
from typing import Dict, List
from collections import defaultdict

class RACIMatrixBuilder:
    """Constructs the RACI Matrix Visio grid with phase grouping."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._validate_raci()
        self._calculate_positions()
        self._calculate_counts()
    
    def _setup_page(self) -> None:
        """Configure A2 landscape page bounds."""
        self.page.page_sheet.page_props.page_width = 59.4
        self.page.page_sheet.page_props.page_height = 42.0
        self.page_width = 59.4
        self.page_height = 42.0
    
    def _setup_styles(self) -> None:
        """Bind global styles."""
        styling = self.config.get("styling", {})
        self.raci_colors = styling.get("raci_colors", {
            "R": "#E53935", "R_text": "#FFFFFF",
            "A": "#1565C0", "A_text": "#FFFFFF",
            "C": "#FFB300", "C_text": "#333333",
            "I": "#4CAF50", "I_text": "#FFFFFF",
            "-": "#E0E0E0", "-_text": "#757575"
        })
        self.row_height = styling.get("row_height", 0.55)
        self.task_col_width = styling.get("task_col_width", 2.8)
        self.role_col_width = styling.get("role_col_width", 1.4)
    
    def _validate_raci(self) -> None:
        """Enforce RULE-01 through RULE-05 before rendering."""
        tasks = self.config['raci_matrix']['tasks']
        valid_codes = {"R", "A", "C", "I", "-"}
        role_ids = {r['id'] for r in self.config['raci_matrix']['roles']}
        
        for task in tasks:
            raci = task.get('raci', {})
            
            # RULE-04: Valid values only
            for role_id, code in raci.items():
                if code not in valid_codes:
                    raise ValueError(f"RM-004: Invalid RACI code '{code}' in task '{task['id']}'.")
            
            # RULE-05: Role reference integrity
            for role_id in raci.keys():
                if role_id not in role_ids:
                    raise ValueError(f"RM-007: Role '{role_id}' in task '{task['id']}' not found in roles list.")
            
            # RULE-01: Exactly 1 Accountable
            accountable_count = sum(1 for v in raci.values() if v == 'A')
            if accountable_count > 1:
                raise ValueError(f"RM-005: Task '{task['id']}' has {accountable_count} Accountable roles. Only 1 is allowed.")
            if accountable_count == 0:
                raise ValueError(f"RM-006: Task '{task['id']}' has no Accountable role. Every task must have exactly 1 A.")
    
    def _calculate_positions(self) -> None:
        """Auto-fit grid to A2 page."""
        layout = self.config.get("layout", {})
        margin = layout.get("margin", 0.5)
        
        roles = sorted(self.config['raci_matrix']['roles'], key=lambda r: r['order'])
        
        # Compute role column width auto-fit
        available = self.page_width - (margin * 2) - self.task_col_width - 0.8  # 0.8 for Total col
        auto_width = available / max(1, len(roles))
        self.role_col_width = min(auto_width, 1.6)
        
        x = margin
        self.col_positions = {'task': {'x': x, 'width': self.task_col_width}}
        x += self.task_col_width
        
        for role in roles:
            self.col_positions[role['id']] = {'x': x, 'width': self.role_col_width}
            x += self.role_col_width
        
        self.col_positions['total'] = {'x': x, 'width': 0.8}
        
        # Row positions with phase grouping
        y_start = margin + 1.5 + layout.get("header_height", 0.8)
        tasks = sorted(self.config['raci_matrix']['tasks'], key=lambda t: (t['phase_order'], t['order']))
        
        self.row_positions = {}
        current_phase = None
        y = y_start
        
        for task in tasks:
            if task['phase'] != current_phase:
                # Phase separator row
                current_phase = task['phase']
                self.row_positions[f"PHASE_{task['phase']}"] = {
                    'y': y,
                    'height': 0.35,
                    'type': 'phase_header',
                    'name': task['phase'],
                    'phase_order': task['phase_order']
                }
                y += 0.35
            
            self.row_positions[task['id']] = {
                'y': y,
                'height': self.row_height,
                'type': 'task'
            }
            y += self.row_height
        
        self.footer_y = y + 0.2
    
    def _calculate_counts(self) -> None:
        """Compute per-role and per-task RACI distribution counts."""
        roles = self.config['raci_matrix']['roles']
        tasks = self.config['raci_matrix']['tasks']
        
        self.role_counts = {r['id']: {'R': 0, 'A': 0, 'C': 0, 'I': 0} for r in roles}
        self.task_totals = {}
        
        for task in tasks:
            raci = task.get('raci', {})
            assigned = sum(1 for v in raci.values() if v != '-')
            self.task_totals[task['id']] = assigned
            
            for role_id, code in raci.items():
                if code in ('R', 'A', 'C', 'I') and role_id in self.role_counts:
                    self.role_counts[role_id][code] += 1
    
    def build(self) -> None:
        """Execute all Aspose draw calls."""
        # 1. Title block
        # 2. Header row (role names + person names)
        # 3. Phase separator rows
        # 4. Task rows with RACI cells
        # 5. Footer totals row
        # 6. Legend block
        # 7. Summary / Gap Analysis block
        pass
    
    def save(self, output_path: str) -> None:
        """Export to VSDX."""
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

### 8.2 RACI Calculator (`calculators/raci_calculator.py`)

```python
from typing import List, Dict

class RACICalculator:
    """Aggregates RACI statistics for summary sections."""
    
    def __init__(self, tasks: List[Dict], roles: List[Dict]):
        self.tasks = tasks
        self.roles = roles
    
    def total_assignments(self) -> int:
        """Count all non-empty RACI cell assignments."""
        return sum(
            sum(1 for v in t.get('raci', {}).values() if v != '-')
            for t in self.tasks
        )
    
    def average_per_task(self) -> float:
        """Average number of assignments per task."""
        n = len(self.tasks)
        return round(self.total_assignments() / max(1, n), 1)
    
    def role_summary(self) -> Dict:
        """Per-role distribution counts."""
        summary = {r['id']: {'R': 0, 'A': 0, 'C': 0, 'I': 0, 'total': 0} for r in self.roles}
        for task in self.tasks:
            for role_id, code in task.get('raci', {}).items():
                if code in ('R', 'A', 'C', 'I') and role_id in summary:
                    summary[role_id][code] += 1
                    summary[role_id]['total'] += 1
        return summary
```

### 8.3 Gap Analyzer (`calculators/gap_analyzer.py`)

```python
from typing import List, Dict

class GapAnalyzer:
    """Identifies RACI completeness gaps and role utilization anomalies."""
    
    def __init__(self, tasks: List[Dict], roles: List[Dict]):
        self.tasks = tasks
        self.roles = roles
    
    def tasks_missing_r(self) -> List[str]:
        """Tasks with no Responsible assigned."""
        return [
            t['name'] for t in self.tasks
            if 'R' not in t.get('raci', {}).values()
        ]
    
    def tasks_missing_a(self) -> List[str]:
        """Tasks with no Accountable assigned."""
        return [
            t['name'] for t in self.tasks
            if 'A' not in t.get('raci', {}).values()
        ]
    
    def overloaded_roles(self, role_summary: Dict, threshold: int = 10) -> List[str]:
        """Roles with more than `threshold` assignments."""
        return [
            role_id for role_id, counts in role_summary.items()
            if counts['total'] > threshold
        ]
    
    def underutilized_roles(self, role_summary: Dict) -> List[str]:
        """Roles with zero R and zero A assignments."""
        return [
            role_id for role_id, counts in role_summary.items()
            if counts['R'] == 0 and counts['A'] == 0
        ]
    
    def generate_report(self, role_summary: Dict) -> Dict:
        """Generate a comprehensive gap analysis report."""
        missing_r = self.tasks_missing_r()
        missing_a = self.tasks_missing_a()
        overloaded = self.overloaded_roles(role_summary)
        underutilized = self.underutilized_roles(role_summary)
        
        return {
            "raci_complete": len(missing_a) == 0,
            "tasks_missing_r": missing_r,
            "tasks_missing_a": missing_a,
            "overloaded_roles": overloaded,
            "underutilized_roles": underutilized,
            "gaps_detected": len(missing_r) + len(missing_a) + len(underutilized)
        }
```

---

## 9. Error Handling

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| `RM-001` | InvalidInput | JSON fails Pydantic schema. | Ensure correct JSON fields. |
| `RM-002` | NoRoles | Roles array is empty. | Define at least 1 role. |
| `RM-003` | NoTasks | Tasks array is empty. | Define at least 1 task. |
| `RM-004` | InvalidRACICode | RACI code not in `[R,A,C,I,-]`. | Correct the code. |
| `RM-005` | MultipleAccountable | Task has more than 1 `A`. | Keep exactly 1 Accountable per task. |
| `RM-006` | MissingAccountable | Task has 0 `A` codes. | Add exactly 1 `A` per task. |
| `RM-007` | MissingRoleReference | RACI dict key does not match any Role ID. | Verify role `id` spelling. |
| `RM-008` | JavaNotInstalled | Missing JRE 8+. | Install Java for JPype. |
| `RM-009` | LicenseMissing | Aspose `.lic` not found. | Set environment variable. |
| `RM-010` | RenderError | File write failure. | Check path permissions. |

---

## 10. Command-Line Interface (CLI)

```python
# cli.py
import argparse
import json
import logging
import sys
from core.diagram_builder import RACIMatrixBuilder

def main():
    parser = argparse.ArgumentParser(description="Generate Visio RACI Matrix")
    parser.add_argument("input", help="Path to input JSON/YAML file")
    parser.add_argument("-o", "--output", help="Output VSDX path (default: ./output/raci_matrix.vsdx)")
    parser.add_argument("-p", "--preview", action="store_true", help="Generate PNG preview")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--validate-only", action="store_true", help="Validate RACI rules without rendering")
    parser.add_argument("--gap-report", action="store_true", help="Print gap analysis report to stdout")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    with open(args.input, 'r') as f:
        spec = json.load(f)
    
    if args.validate_only:
        builder = RACIMatrixBuilder(spec)  # Validation runs in __init__
        logging.info("RACI validation passed. All rules satisfied.")
        sys.exit(0)
    
    builder = RACIMatrixBuilder(spec)
    builder.build()
    
    out_path = args.output or "./output/raci_matrix.vsdx"
    builder.save(out_path)
    logging.info(f"RACI Matrix saved to {out_path}")

if __name__ == "__main__":
    main()
```

---

## 11. Quality Checklist

- [ ] **RULE-01 Enforced:** Every task row contains exactly one blue `A` cell.
- [ ] **RULE-02 Warning:** Tasks without any `R` are flagged in the gap analysis but do not block rendering.
- [ ] **Phase Separators:** `► PHASE X: NAME` rows correctly interrupt the task flow.
- [ ] **Color Accuracy:** R=Red, A=Blue, C=Amber, I=Green cells are accurately colored.
- [ ] **Totals Row:** Footer accurately shows `R:X A:Y C:Z I:W` per role column.
- [ ] **Gap Analysis Block:** Summary correctly enumerates overloaded and underutilized roles.

---

## 12. Usage Examples

### 12.1 Standard RACI Rendering
```bash
python raci_matrix_generator/cli.py data/raci.json -o output/raci_matrix.vsdx
```

### 12.2 Validation Pass (CI/CD Gate)
```bash
python raci_matrix_generator/cli.py data/raci.json --validate-only
```

### 12.3 Gap Report
```bash
python raci_matrix_generator/cli.py data/raci.json --gap-report
```

---

## 13. Integration with Existing Skills

1. **Charter Integration:** This RACI Matrix is the official responsibility assignment embedded by the `project-charter-generator`.
2. **RAM Complement:** The `resource-allocation-matrix-generator` tracks *utilization percentages* across phases; this skill tracks *categorical responsibilities* across tasks.

---

## 14. Testing Strategy

1. **RULE-01 Violation Test:** Supply a task with two `A` codes. Assert `RM-005` is raised.
2. **RULE-01 Missing Test:** Supply a task with zero `A` codes. Assert `RM-006` is raised.
3. **Invalid Code Test:** Supply `"R5": "X"`. Assert `RM-004`.
4. **Missing Role Reference Test:** Supply `"R99": "R"` with no `R99` in roles. Assert `RM-007`.
5. **Gap Analyzer Test:** Supply a matrix where Security officer has only `I` assignments. Assert `underutilized_roles` contains the Security role ID.
