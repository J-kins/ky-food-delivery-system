# RACI Matrix Generator — Agent Prompt

Use this file to generate the input JSON required by the **RACI Matrix Generator**. Any agentic AI working on any project can follow this prompt to produce a valid `raci_input.json` that renders a Responsibility Assignment Matrix as a fully editable Visio file (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`raci_matrix` is listed** in `specifications.json → diagrams_to_generate`
3. Read [raci-matrix-diagram-generator-SKILL.md](../raci-matrix-diagram-generator-SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | Description |
|--------|--------|-------------|
| RACI matrix | `.vsdx` | Tasks × Roles grid with color-coded R/A/C/I cells, phase grouping, column totals, gap analysis |

## Output File Location

Save the generated input to:

```text
projects/<project-slug>/inputs/raci_input.json
```

Example: `projects/daatsna-community-data-platform/inputs/raci_input.json`

---

## Agent Instructions

You are a project governance specialist. Your task is to generate a complete `raci_input.json` file for the RACI Matrix Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json` (especially `phases`, `wbs`, `stakeholders`, `project`).
2. Define **roles** (columns) from project team and key stakeholders.
3. Define **tasks** (rows) from WBS work packages grouped by phase.
4. Assign RACI codes per task × role — enforce exactly one `A` per task.
5. Validate against all rules in the Validation section.
6. Write the file to `projects/<project-slug>/inputs/raci_input.json`.
7. Return the complete JSON in a single code block and confirm the file path.

If `specifications.json` is missing, gather roles, tasks, and accountability from the user — or infer from project type and list assumptions.

---

## RACI Code Definitions

| Code | Name | Meaning |
|------|------|---------|
| `R` | Responsible | Does the work — at least 1 per task (recommended) |
| `A` | Accountable | Approves outcome — **exactly 1 per task (required)** |
| `C` | Consulted | Two-way input before decisions |
| `I` | Informed | One-way status updates |
| `-` | Not involved | No role in this task |

### Default cell colors (auto-applied)

| Code | Fill | Text |
|------|------|------|
| R | `#E53935` | `#FFFFFF` |
| A | `#1565C0` | `#FFFFFF` |
| C | `#FFB300` | `#333333` |
| I | `#4CAF50` | `#FFFFFF` |
| - | `#E0E0E0` | `#757575` |

---

## Mapping from specifications.json

| specifications.json | raci_input.json | Notes |
|---------------------|-----------------|-------|
| `project.name` | `raci_matrix.project_name` | Full project name |
| `project.version` | `raci_matrix.version` | e.g. `"1.0"` |
| `project.date` | `raci_matrix.date` | `YYYY-MM-DD` |
| `project.sponsor` | role: Project Sponsor | Column R1 typically |
| `project.manager` | role: Project Manager | Column R2 typically |
| `stakeholders[]` | additional `roles[]` | Map by role/title to columns |
| `phases[]` | task `phase`, `phase_order` | Group rows by phase |
| `wbs.branches[]` | tasks (level 1) | Major deliverables |
| `wbs.branches[].children[]` | tasks (level 2) | Work packages |

### Deriving roles from stakeholders

Map 5–12 distinct **roles** (not every stakeholder — consolidate by function):

| Typical role | Source |
|--------------|--------|
| Project Sponsor | `project.sponsor` |
| Project Manager | `project.manager` |
| Lead BA / Requirements | stakeholder with analysis role |
| Solution Architect | technical stakeholder |
| Dev Lead | development stakeholder |
| QA Lead | testing stakeholder |
| Ops / Deployment Lead | operations stakeholder |
| UX Lead | design stakeholder |
| Security Officer | regulatory/security stakeholder |
| Compliance Officer | compliance stakeholder |

Use `id`: `R1`, `R2`, … `R10` with sequential `order`.

### Deriving tasks from WBS

For each WBS work package, create a task row:

```json
{
  "id": "T1",
  "name": "Project Charter Development",
  "description": "Create and approve project charter",
  "phase": "Initiation",
  "phase_order": 1,
  "order": 1,
  "raci": {
    "R1": "A",
    "R2": "C",
    "R3": "C",
    "R4": "-",
    "R5": "I"
  }
}
```

Include **every role id** in each task's `raci` object (use `-` for not involved).

### Typical accountability patterns

| Task type | Accountable (A) | Responsible (R) |
|-----------|-----------------|-----------------|
| Charter / governance | Sponsor | PM |
| Requirements | PM or Compliance | Lead BA |
| Architecture / design | Solution Architect | Solution Architect |
| Development | Dev Lead or Architect | Dev Lead |
| Testing | QA Lead | QA Lead |
| Deployment | Ops Lead | Ops Lead |
| Closure | Sponsor | PM |

Sponsor and PM are usually `I` (Informed) on execution tasks, `C` (Consulted) on design decisions.

---

## JSON Schema

Generate a complete JSON file with this structure:

```json
{
  "raci_matrix": {
    "title": "string - Diagram title",
    "project_name": "string - Full project name",
    "version": "string - Version (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",
    "sprint": "string - Optional sprint/phase label",
    "description": "string - Optional description",

    "roles": [
      {
        "id": "string - R1, R2, ...",
        "name": "string - Role title",
        "person": "string - Person name",
        "department": "string - Department or organization",
        "color": "string - Hex column header color",
        "text_color": "string - Hex text color",
        "order": "number - Column order left-to-right"
      }
    ],

    "tasks": [
      {
        "id": "string - T1, T2, ...",
        "name": "string - Task name",
        "description": "string - Optional task description",
        "phase": "string - Phase name for grouping",
        "phase_order": "number - Phase sort order",
        "order": "number - Row sort order within matrix",
        "raci": {
          "R1": "string - R | A | C | I | -",
          "R2": "string - R | A | C | I | -"
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
      "show_phase_grouping": true,
      "show_descriptions": true
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

## Section Guidelines

### Roles (columns)

- **Minimum 3, recommended 5–12**
- Unique `id` and sequential `order` (1, 2, 3, …)
- Each role needs `name`, `person`, `department`
- Assign distinct header colors from default palette

### Tasks (rows)

- **Minimum 1, recommended 10–20**
- Group by `phase` with matching `phase_order`
- `order` is global sort key (1, 2, 3, … across all phases)
- Unique task `id`: `T1`, `T2`, …
- One row per meaningful deliverable or work package

### RACI assignments per task

- **RULE-01:** Exactly **one** `A` per task — enforced at render time (RM-005/RM-006)
- **RULE-02:** At least one `R` per task — strongly recommended (gap analysis flags missing R)
- **RULE-03:** Not all `-` — at least one assignment per row
- **RULE-04:** Only `R`, `A`, `C`, `I`, `-` allowed
- **RULE-05:** Every key in `raci{}` must match a `roles[].id`

### Standard software project phases

```text
1 Initiation       → Charter, Team Assembly
2 Requirements     → Elicitation, Analysis, Specification
3 Design           → System Design, Database, API, UI/UX
4 Development      → Backend, Frontend, Integration
5 Testing          → Unit, Integration, System, UAT
6 Deployment       → Infrastructure, Deploy, Training
7 Closure          → Handover, Lessons Learned, Closure
```

---

## Validation Rules

Fix every failure before writing the file:

1. All required fields populated
2. At least **1 role** and **1 task**
3. All role IDs unique; all task IDs unique
4. Every task has **exactly one** `A` in its `raci` values
5. Every `raci` key matches a defined role ID
6. Only valid codes: `R`, `A`, `C`, `I`, `-`
7. Each task row has at least one non-`-` assignment
8. Recommended: each task has at least one `R`
9. Dates in `YYYY-MM-DD` format
10. JSON is syntactically valid

Optional validation:

```bash
python raci_matrix_generator/cli.py projects/<project-slug>/inputs/raci_input.json --validate-only
```

---

## Quick Reference Card

| Section | Minimum | Maximum | Key Rule |
|---------|---------|---------|----------|
| Roles | 3 | 15 | Unique IDs; ordered |
| Tasks | 1 | 30 | Grouped by phase |
| A per task | 1 | 1 | Exactly one Accountable |
| R per task | 1 | many | At least one Responsible |
| RACI codes | — | — | R, A, C, I, - only |

---

## After Generating Input

Run the generator:

```bash
# Render Visio RACI matrix
python raci_matrix_generator/cli.py projects/<project-slug>/inputs/raci_input.json \
  -o projects/<project-slug>/output/raci_matrix.vsdx

# Gap analysis report
python raci_matrix_generator/cli.py projects/<project-slug>/inputs/raci_input.json \
  --validate-only --gap-report

# Validate only
python raci_matrix_generator/cli.py projects/<project-slug>/inputs/raci_input.json --validate-only
```

Reference schema: [raci-matrix-diagram-generator-SKILL.md](../raci-matrix-diagram-generator-SKILL.md) Section 3 (full Da'atSNA example with 15 tasks × 10 roles).

---

## Integration Notes

- Complements [resource-allocation-matrix-generator-SKILL.md](../resource-allocation-matrix-generator-SKILL.md) (percentage load vs categorical accountability).
- Roles align with [stakeholder-diagram-generator-SKILL.md](../stakeholder-diagram-generator-SKILL.md) stakeholder register.
- Tasks align with [wbs-diagram-generator-SKILL.md](../wbs-diagram-generator-SKILL.md) and [gantt-chart-generator-SKILL.md](../gantt-chart-generator-SKILL.md).
- Embedded in [project-charter-generator-SKILL.md](../project-charter-generator-SKILL.md) governance section.

---

## Copy-Ready Agent Prompt

```
You are a project governance specialist. Your task is to generate a complete raci_input.json file for the RACI Matrix Generator (Visio .vsdx output).

Read the project data from specifications.json or the project description below. Follow the JSON schema in raci_matrix_generator/PROMPT.md exactly. If information is not explicitly provided, derive roles from stakeholders and tasks from WBS/phases and list assumptions.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Software Development, Healthcare, Infrastructure]
**Key Roles:** [LIST PROJECT ROLES AND PEOPLE]
**Major Tasks / WBS:** [LIST DELIVERABLES BY PHASE]
**Accountability Notes:** [WHO OWNS WHICH DECISIONS]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables

1. A complete, valid raci_input.json following the schema in raci_matrix_generator/PROMPT.md
2. Saved to projects/<project-slug>/inputs/raci_input.json
3. All validation rules satisfied

## Validation Rules

1. At least 3 roles and 1 task (recommended 10+ tasks)
2. Every task has exactly ONE A (Accountable) — no more, no less
3. Every task should have at least one R (Responsible)
4. RACI codes: R, A, C, I, or - only
5. Every raci{} key must match a roles[].id
6. Include all role IDs in each task's raci object
7. Group tasks by phase with phase_order and order fields
8. Not all cells may be - for any single task row

## Response Format

Return the complete raci_input.json in a single JSON code block AND write it to disk at projects/<project-slug>/inputs/raci_input.json.

Now, generate the raci_input.json for the project described above.
```
