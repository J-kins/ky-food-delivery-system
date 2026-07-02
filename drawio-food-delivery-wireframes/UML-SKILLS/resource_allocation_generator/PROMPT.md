# Resource Allocation Matrix Generator — Agent Prompt

Use this file to generate the input JSON required by the **Resource Allocation Matrix Generator**. Any agentic AI working on any project can follow this prompt to produce a valid `resource_allocation_input.json` that renders a Resources × Phases staffing matrix as a fully editable Visio file (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`resource_allocation_matrix` is listed** in `specifications.json → diagrams_to_generate`
3. Read [resource-allocation-matrix-generator-SKILL.md](../resource-allocation-matrix-generator-SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | Description |
|--------|--------|-------------|
| Resource allocation matrix | `.vsdx` | Resources (rows) × Phases (columns) with RACI codes, % load, status badges, phase totals |

## Output File Location

Save the generated input to:

```text
projects/<project-slug>/inputs/resource_allocation_input.json
```

Example: `projects/daatsna-community-data-platform/inputs/resource_allocation_input.json`

---

## Agent Instructions

You are a project staffing specialist. Your task is to generate a complete `resource_allocation_input.json` file for the Resource Allocation Matrix Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json` (especially `phases`, `stakeholders`, `budget`, `wbs`).
2. Define **resources** (rows) — people with roles and overall capacity `%`.
3. Define **phases** (columns) — project phases with colors and order.
4. Build **allocations** — one entry per resource × phase cell that is involved.
5. Set `allocation_type` (`RACI`, `PERCENTAGE`, or `BOTH`).
6. Validate against all rules in the Validation section.
7. Write the file to `projects/<project-slug>/inputs/resource_allocation_input.json`.
8. Return the complete JSON in a single code block and confirm the file path.

If `specifications.json` is missing, gather team members, phases, and involvement from the user — or infer from project type and list assumptions.

---

## Resource Allocation vs RACI Matrix

| Generator | Orientation | Focus |
|-----------|---------------|-------|
| **Resource Allocation** (this file) | Resources × **Phases** | Who is busy when; % utilization load |
| [RACI Matrix](../raci_matrix_generator/PROMPT.md) | **Tasks** × Roles | Who does what per deliverable |

Use Resource Allocation for staffing plans and capacity; use RACI Matrix for task accountability.

---

## Mapping from specifications.json

| specifications.json | resource_allocation_input.json | Notes |
|-----------------------|-------------------------------|-------|
| `project.name` | `resource_allocation.project_name` | Full project name |
| `project.version` | `resource_allocation.version` | e.g. `"1.0"` |
| `project.date` | `resource_allocation.date` | `YYYY-MM-DD` |
| `project.sponsor` | resource R1: Project Sponsor | Row |
| `project.manager` | resource R2: Project Manager | Row |
| `phases[]` | `phases[]` | Columns P1, P2, … |
| `stakeholders[]` | additional `resources[]` | Map by role/title |
| `budget.categories` (Personnel) | `resources[].allocation` | Infer FTE % from budget |

### Deriving resources from team/stakeholders

Create 5–10 resources with overall capacity (`allocation` = 0–100):

| Role | Typical allocation % |
|------|---------------------|
| Project Sponsor | 15–30 |
| Project Manager | 40–60 |
| Lead BA | 70–90 |
| Solution Architect | 80–100 |
| Dev Lead | 80–100 |
| QA Lead | 60–80 |
| Ops Lead | 50–70 |

### Deriving phases from specifications

Map `specifications.json → phases[]` directly:

```json
{
  "id": "P1",
  "name": "Initiation",
  "description": "Project kickoff and charter",
  "order": 1,
  "color": "#1a237e"
}
```

### Building allocations

One object per **active** resource × phase pair:

```json
{
  "resource_id": "R3",
  "phase_id": "P2",
  "value": "R",
  "percentage": 80,
  "description": "Requirements lead"
}
```

- `value`: `R`, `A`, `C`, `I`, or `-` (omit cell entirely if not involved, or use sparse allocations only for active cells)
- `percentage`: effort % for that phase (0–200; typical 10–100)
- Do **not** duplicate the same `resource_id` + `phase_id` pair (RA-009)

### Typical phase involvement pattern

| Resource | P1 Init | P2 Req | P3 Design | P4 Dev | P5 Test | P6 Deploy | P7 Close |
|----------|---------|--------|-----------|--------|---------|-----------|----------|
| Sponsor | A | I | I | I | I | I | A |
| PM | A/R | A | A | I | I | I | A |
| Lead BA | C | R | A | R | C | - | - |
| Architect | - | C | R | R | C | C | - |
| Dev Lead | - | - | C | R | R | R | C |
| QA Lead | - | - | - | C | R | R | - |
| Ops Lead | - | - | - | - | C | R | R |

---

## JSON Schema

Generate a complete JSON file with this structure:

```json
{
  "resource_allocation": {
    "title": "string - Diagram title",
    "project_name": "string - Full project name",
    "version": "string - Version (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",
    "sprint": "string - Optional period label (e.g., Q2 2026)",
    "description": "string - Optional description",
    "allocation_type": "string - RACI | PERCENTAGE | BOTH",

    "resources": [
      {
        "id": "string - R1, R2, ...",
        "name": "string - Person name",
        "role": "string - Job title",
        "department": "string - Department or organization",
        "email": "string - Optional email",
        "allocation": "number - Overall capacity 0-100"
      }
    ],

    "phases": [
      {
        "id": "string - P1, P2, ...",
        "name": "string - Phase name",
        "description": "string - Optional phase description",
        "order": "number - Column order left-to-right",
        "color": "string - Hex header color"
      }
    ],

    "allocations": [
      {
        "resource_id": "string - Must match resources[].id",
        "phase_id": "string - Must match phases[].id",
        "value": "string - R | A | C | I | -",
        "percentage": "number - 0-200 effort % for this phase",
        "description": "string - Optional cell note"
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

## Section Guidelines

### allocation_type

| Value | Displays |
|-------|----------|
| `RACI` | R/A/C/I codes in cells (default) |
| `PERCENTAGE` | Numeric % only |
| `BOTH` | RACI code + percentage stacked |

### Resources (rows)

- **Minimum 1, recommended 5–10**
- Unique `id`: `R1`, `R2`, …
- `allocation` = overall capacity benchmark (used for load status column)
- Include `name`, `role`, `department`

### Phases (columns)

- **Minimum 1, recommended 5–8**
- Map from `specifications.json → phases[]`
- Unique `id`: `P1`, `P2`, … with sequential `order`
- Assign colors from default phase palette

### Default phase colors

| Phase | Hex |
|-------|-----|
| Initiation | `#1a237e` |
| Requirements | `#2E7D32` |
| Design | `#E65100` |
| Development | `#6A1B9A` |
| Testing | `#C62828` |
| Deployment | `#00838F` |
| Closure | `#4E342E` |

### Allocations

- **Minimum 1 entry; recommended 15–40** (sparse — only active cells)
- No duplicate `resource_id` + `phase_id` pairs
- `value` must be `R`, `A`, `C`, `I`, or `-`
- `percentage` range: 0–200 (RA-008 if outside)
- Peak `percentage` per resource drives load category:
  - **Over** > 100%
  - **Full** 80–100%
  - **Partial** 40–79%
  - **Under** < 40%

### RACI codes (same as RACI matrix)

| Code | Meaning |
|------|---------|
| R | Responsible — executes work in this phase |
| A | Accountable — approves phase outcomes |
| C | Consulted — provides input |
| I | Informed — receives updates |
| - | Not involved in this phase |

Unlike the RACI Matrix generator, there is **no** exactly-one-A rule per row — accountability is per phase cell.

---

## Validation Rules

Fix every failure before writing the file:

1. All required fields populated
2. At least **1 resource**, **1 phase**, and **1 allocation**
3. All resource IDs unique; all phase IDs unique
4. Every `allocations[].resource_id` matches a `resources[].id`
5. Every `allocations[].phase_id` matches a `phases[].id`
6. No duplicate `resource_id` + `phase_id` pairs
7. `value` in `R`, `A`, `C`, `I`, `-` only
8. `percentage` between 0 and 200
9. `allocation_type` is `RACI`, `PERCENTAGE`, or `BOTH`
10. Dates in `YYYY-MM-DD` format
11. JSON is syntactically valid

Optional validation:

```bash
python resource_allocation_generator/cli.py projects/<project-slug>/inputs/resource_allocation_input.json --validate-only
```

---

## Quick Reference Card

| Section | Minimum | Maximum | Key Rule |
|---------|---------|---------|----------|
| Resources | 1 | 15 | Unique IDs; allocation 0–100 |
| Phases | 1 | 10 | Unique IDs; ordered |
| Allocations | 1 | — | No duplicate resource+phase |
| percentage | 0 | 200 | Per phase cell |
| Load status | (computed) | — | Max phase % per resource |

---

## After Generating Input

Run the generator:

```bash
# Render Visio matrix (RACI mode)
python resource_allocation_generator/cli.py projects/<project-slug>/inputs/resource_allocation_input.json \
  -o projects/<project-slug>/output/resource_allocation.vsdx

# Percentage-only mode
python resource_allocation_generator/cli.py projects/<project-slug>/inputs/resource_allocation_input.json \
  --type PERCENTAGE -o projects/<project-slug>/output/resource_allocation.vsdx

# Both RACI and percentage
python resource_allocation_generator/cli.py projects/<project-slug>/inputs/resource_allocation_input.json \
  --type BOTH -o projects/<project-slug>/output/resource_allocation.vsdx

# Validate only
python resource_allocation_generator/cli.py projects/<project-slug>/inputs/resource_allocation_input.json --validate-only
```

Reference schema: [resource-allocation-matrix-generator-SKILL.md](../resource-allocation-matrix-generator-SKILL.md) Section 3 (full Da'atSNA example with 7 resources × 7 phases).

---

## Integration Notes

- Pairs with [raci_matrix_generator/PROMPT.md](../raci_matrix_generator/PROMPT.md) — same RACI codes, different grid orientation.
- Personnel costs in [budget_breakdown_generator/PROMPT.md](../budget_breakdown_generator/PROMPT.md) should align with `resources[]`.
- Phases align with [gantt-chart-generator-SKILL.md](../gantt-chart-generator-SKILL.md) and [milestone_chart_generator/PROMPT.md](../milestone_chart_generator/PROMPT.md).
- Embedded in [project-charter-generator-SKILL.md](../project-charter-generator-SKILL.md) staffing section.

---

## Copy-Ready Agent Prompt

```
You are a project staffing specialist. Your task is to generate a complete resource_allocation_input.json file for the Resource Allocation Matrix Generator (Visio .vsdx output).

Read the project data from specifications.json or the project description below. Follow the JSON schema in resource_allocation_generator/PROMPT.md exactly. If information is not explicitly provided, derive resources from stakeholders and phases from specifications and list assumptions.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Software Development, Healthcare, Infrastructure]
**Timeline / Phases:** [LIST PROJECT PHASES]
**Team Members:** [LIST PEOPLE, ROLES, AND AVAILABILITY %]
**Phase Involvement:** [DESCRIBE WHO IS ACTIVE IN WHICH PHASES]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables

1. A complete, valid resource_allocation_input.json following the schema in resource_allocation_generator/PROMPT.md
2. Saved to projects/<project-slug>/inputs/resource_allocation_input.json
3. All validation rules satisfied

## Validation Rules

1. At least 1 resource, 1 phase, and 1 allocation entry
2. No duplicate resource_id + phase_id pairs in allocations[]
3. All resource_id and phase_id references must exist
4. RACI values: R, A, C, I, or - only
5. percentage between 0 and 200 for each allocation
6. resources[].allocation reflects overall capacity (0-100)
7. Set allocation_type to RACI (or PERCENTAGE/BOTH if requested)
8. Include sparse allocations only for active resource-phase cells

## Response Format

Return the complete resource_allocation_input.json in a single JSON code block AND write it to disk at projects/<project-slug>/inputs/resource_allocation_input.json.

Now, generate the resource_allocation_input.json for the project described above.
```
