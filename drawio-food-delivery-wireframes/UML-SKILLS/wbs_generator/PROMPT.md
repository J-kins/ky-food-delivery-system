# WBS Diagram Generator — Agent Prompt

Use this file to generate the input JSON required by the **Work Breakdown Structure (WBS) Diagram Generator**. Any agentic AI working on any project can follow this prompt to produce a valid `wbs_input.json` that renders a hierarchical WBS tree (Level 0–3) as a fully editable Visio file (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`wbs_diagram` is listed** in `specifications.json → diagrams_to_generate`
3. Read [wbs-diagram-generator-SKILL.md](../wbs-diagram-generator-SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | Description |
|--------|--------|-------------|
| WBS diagram | `.vsdx` | Top-down tree: Project (L0) → Phases (L1) → Work packages (L2) → Tasks (L3) |

## Output File Location

Save the generated input to:

```text
projects/<project-slug>/inputs/wbs_input.json
```

Example: `projects/daatsna-community-data-platform/inputs/wbs_input.json`

---

## Agent Instructions

You are a project decomposition specialist. Your task is to generate a complete `wbs_input.json` file for the WBS Diagram Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json` (especially `wbs`, `phases`, `project`, `objectives`).
2. Build **`levels`** metadata (level_0 through level_3 styling config).
3. Build **`branches[]`** recursive tree — Level 1 phases with Level 2 work packages and Level 3 tasks.
4. Assign PMI numbering (`1`, `1.1`, `1.1.1`) and `level` integers (1–3).
5. Add `description` on every node; `effort_hours` on Level 3 tasks.
6. Set `styling` and `layout`.
7. Validate against all rules in the Validation section.
8. Write the file to `projects/<project-slug>/inputs/wbs_input.json`.
9. Return the complete JSON in a single code block and confirm the file path.

If `specifications.json` is missing, gather project scope and deliverables from the user — or infer from project type and list assumptions.

---

## Mapping from specifications.json

| specifications.json | wbs_input.json | Notes |
|-----------------------|----------------|-------|
| `project.name` | `wbs.project_name` | Full project name |
| `project.name` | `wbs.levels.level_0.name` | Root box label |
| `project.description` | `wbs.description` | Diagram subtitle |
| `project.version` | `wbs.version` | e.g. `"1.0"` |
| `project.date` | `wbs.date` | `YYYY-MM-DD` |
| `wbs.level_0` | `wbs.levels.level_0` | **Move** under `levels`; add colors |
| `wbs.branches[]` | `wbs.branches[]` | Expand to full L1→L2→L3 tree |
| `phases[]` | Level 1 branch names | Align L1 with project phases when WBS is sparse |
| `objectives[]` | Level 2/3 task themes | Decompose objectives into work packages |

### Schema shape difference

`specifications.json` uses a **flat** WBS:

```json
{
  "wbs": {
    "level_0": { "id": "0", "name": "Project Name" },
    "branches": [ { "id": "1", "name": "...", "level": 1, "children": [...] } ]
  }
}
```

The generator input **wraps level_0 inside `levels`** and adds level styling metadata:

```json
{
  "wbs": {
    "title": "Work Breakdown Structure",
    "project_name": "...",
    "levels": {
      "level_0": { "id": "0", "name": "...", "color": "#1a237e", ... },
      "level_1": { "name": "Phases/Deliverables", "color": "#1565C0", ... },
      "level_2": { ... },
      "level_3": { ... }
    },
    "branches": [ ... ]
  }
}
```

### Expanding a sparse specifications WBS

If `specifications.json → wbs.branches[]` only has Level 1–2:

1. Keep Level 1 branches aligned with `phases[]` names where possible.
2. **Add Level 3 tasks** under each Level 2 work package (2–4 tasks each).
3. Add `description` to every node.
4. Add `effort_hours` (integer) to every Level 3 leaf.

### Standard software-project Level 1 branches

When inferring from project type, use 5–7 Level 1 phases:

| ID | Branch | Maps to phase |
|----|--------|---------------|
| 1 | Project Management | Initiation / governance |
| 2 | Requirements Engineering | Requirements |
| 3 | System Design | Design |
| 4 | Development | Development |
| 5 | Testing | Testing |
| 6 | Deployment & Training | Deployment |
| 7 | Closure | Closure (optional) |

---

## JSON Schema

Generate a complete JSON file with this structure:

```json
{
  "wbs": {
    "title": "string - Diagram title",
    "project_name": "string - Full project name",
    "version": "string - Version (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",
    "description": "string - WBS scope description",

    "levels": {
      "level_0": {
        "id": "0",
        "name": "string - Project root name",
        "description": "string - Project summary",
        "color": "#1a237e",
        "text_color": "#FFFFFF"
      },
      "level_1": {
        "name": "Phases/Deliverables",
        "color": "#1565C0",
        "text_color": "#FFFFFF",
        "shape_style": "rounded_rectangle"
      },
      "level_2": {
        "name": "Work Packages",
        "color": "#64B5F6",
        "text_color": "#333333",
        "shape_style": "rounded_rectangle"
      },
      "level_3": {
        "name": "Tasks/Activities",
        "color": "#FFFFFF",
        "text_color": "#333333",
        "border_color": "#64B5F6",
        "shape_style": "rounded_rectangle"
      }
    },

    "branches": [
      {
        "id": "string - Level 1: 1, 2, 3, ...",
        "name": "string - Phase or major deliverable",
        "description": "string - Required",
        "level": 1,
        "children": [
          {
            "id": "string - Level 2: 1.1, 1.2, ...",
            "name": "string - Work package",
            "description": "string - Required",
            "level": 2,
            "children": [
              {
                "id": "string - Level 3: 1.1.1, 1.1.2, ...",
                "name": "string - Task name",
                "description": "string - Required",
                "level": 3,
                "effort_hours": "number - Estimated hours"
              }
            ]
          }
        ]
      }
    ],

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 10,
      "layout_style": "tree | org_chart",
      "shadow_enabled": true,
      "corner_radius": 6,
      "box_spacing": 0.3
    },

    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "level_spacing": 1.5,
      "box_height": 0.8
    }
  }
}
```

---

## Section Guidelines

### WBS levels (maximum depth 4: L0–L3)

| Level | Role | ID format | Example | Max children |
|-------|------|-----------|---------|--------------|
| 0 | Project root | `0` | Healthcare Ecosystem Project | 1 |
| 1 | Phase / deliverable | `1`, `2`, … | 1. Project Management | 6 |
| 2 | Work package | `1.1`, `1.2`, … | 1.1 Planning | 8 |
| 3 | Task / activity | `1.1.1`, `1.1.2`, … | 1.1.1 Develop Charter | 10 |

**No Level 4** — nesting beyond Level 3 raises `WB-004`.

### Numbering rules (PMI standard)

- Level 1 IDs: sequential integers `1`, `2`, `3`, …
- Level 2 IDs: `{parent}.{n}` → `1.1`, `1.2`, `2.1`
- Level 3 IDs: `{parent}.{n}` → `1.1.1`, `1.1.2`
- IDs must match hierarchy — `1.2.3` parent is `1.2`, root branch is `1`
- Display format in diagram: `{id} {name}` (e.g. `1.1.1 Develop Charter`)

### Node fields

| Field | L0 | L1 | L2 | L3 |
|-------|----|----|----|-----|
| `id` | ✓ | ✓ | ✓ | ✓ |
| `name` | ✓ | ✓ | ✓ | ✓ |
| `description` | ✓ | ✓ **required** | ✓ **required** | ✓ **required** |
| `level` | — | 1 | 2 | 3 |
| `children` | — | ✓ | ✓ | — (leaves) |
| `effort_hours` | — | — | — | ✓ recommended |

### Level colors (defaults — match `renderers/layout_engine.py`)

| Level | Fill | Text |
|-------|------|------|
| 0 | `#1a237e` | `#FFFFFF` |
| 1 | `#1565C0` | `#FFFFFF` |
| 2 | `#64B5F6` | `#333333` |
| 3 | `#FFFFFF` | `#333333` (border `#64B5F6`) |

### Layout

| `layout_style` | Description |
|----------------|-------------|
| `tree` | Standard top-down widespread tree (default) |
| `org_chart` | Compact org-chart routing |

| `page_size` | Use when |
|-------------|----------|
| `A2` | Default — large WBS (6+ L1 branches) |
| `A3` | Small WBS (≤4 L1 branches) |

Increase `level_spacing` or `box_spacing` if nodes overlap (`WB-009`).

---

## Validation Rules

Fix every failure before writing the file:

1. Root key must be `wbs` (CLI reads `spec["wbs"]`)
2. `levels.level_0` present with `id: "0"` and non-empty `name` (`WB-002`, `WB-003`)
3. At least **1 Level 1 branch** in `branches[]`
4. **3–6 Level 1 branches** recommended for software projects
5. Each branch has **2–4 Level 2** children with **2–4 Level 3** tasks each
6. All node IDs unique across the tree (`WB-005`)
7. ID hierarchy consistent — child ID starts with parent ID prefix
8. `level` field matches depth (1, 2, or 3 in branches)
9. Every L1/L2/L3 node has non-empty `description` (`WB-006`)
10. No nesting deeper than Level 3 (`WB-004`)
11. Level 3 leaves include `effort_hours` (positive integer)
12. Dates in `YYYY-MM-DD` format
13. JSON is syntactically valid

Optional validation:

```bash
python wbs_generator/cli.py projects/<project-slug>/inputs/wbs_input.json --validate-only
```

---

## Quick Reference Card

| Section | Minimum | Maximum | Key Rule |
|---------|---------|---------|----------|
| Level 0 | 1 | 1 | id = `"0"` |
| Level 1 branches | 1 | 6 | IDs: 1, 2, 3… |
| Level 2 per branch | 1 | 8 | IDs: n.m |
| Level 3 per package | 1 | 10 | IDs: n.m.k; effort_hours |
| Tree depth | L0–L3 | L0–L3 | No Level 4 |

---

## After Generating Input

Run the generator:

```bash
# Render Visio WBS diagram
python wbs_generator/cli.py \
  projects/<project-slug>/inputs/wbs_input.json \
  -o projects/<project-slug>/output/wbs_diagram.vsdx

# Org-chart layout style
python wbs_generator/cli.py \
  projects/<project-slug>/inputs/wbs_input.json \
  --layout org_chart \
  -o projects/<project-slug>/output/wbs_diagram.vsdx

# PNG preview (requires Graphviz)
python wbs_generator/cli.py \
  projects/<project-slug>/inputs/wbs_input.json \
  -o projects/<project-slug>/output/wbs_diagram.vsdx --preview

# Validate only
python wbs_generator/cli.py \
  projects/<project-slug>/inputs/wbs_input.json --validate-only
```

Reference schema: [wbs-diagram-generator-SKILL.md](../wbs-diagram-generator-SKILL.md) Section 3 (full Da'atSNA healthcare example with 6 Level 1 branches).

---

## Integration Notes

- **`specifications.json → wbs`** maps nearly 1:1 after restructuring `level_0` into `levels` and expanding Level 3 tasks.
- [gantt_chart_generator/PROMPT.md](../gantt_chart_generator/PROMPT.md) — Gantt tasks derive from the same WBS branches.
- [cpm_network_generator/PROMPT.md](../cpm_network_generator/PROMPT.md) / [pert_chart_generator/PROMPT.md](../pert_chart_generator/PROMPT.md) — network activities align with Level 3 tasks.
- [raci_matrix_generator/PROMPT.md](../raci_matrix_generator/PROMPT.md) — RACI task rows map to Level 2/3 WBS nodes.
- [project_charter_generator/PROMPT.md](../project_charter_generator/PROMPT.md) — embeds WBS from the same payload.

### Generator implementation note

`wbs_generator/` currently implements `renderers/layout_engine.py` (Reingold-Tilford-style tree layout). Full CLI and diagram builder are documented in the SKILL; layout uses Level 0 at top, children branching downward.

---

## Copy-Ready Agent Prompt

```
You are a project decomposition specialist. Your task is to generate a complete wbs_input.json file for the WBS Diagram Generator (Visio .vsdx output).

Read the project data from specifications.json or the project description below. Follow the JSON schema in wbs_generator/PROMPT.md exactly. If information is not explicitly provided, derive the WBS from project phases, objectives, and domain conventions.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Software Development, Healthcare Platform]
**Phases / Deliverables:** [LIST MAJOR PHASES]
**Work Packages:** [LIST OR REQUEST INFERENCE]
**Tasks:** [LIST OR REQUEST INFERENCE FOR LEVEL 3 LEAVES]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables

1. A complete, valid wbs_input.json following the schema in wbs_generator/PROMPT.md
2. Saved to projects/<project-slug>/inputs/wbs_input.json
3. All validation rules satisfied

## Validation Rules

1. Root key: wbs
2. levels.level_0 with id "0" and project name
3. levels.level_1 through level_3 styling metadata included
4. branches[]: 3-6 Level 1 phases, each with 2-4 Level 2 work packages, each with 2-4 Level 3 tasks
5. PMI numbering: 1, 1.1, 1.1.1 — IDs must match hierarchy
6. level field: 1, 2, or 3 on every branch node
7. description on every L1/L2/L3 node; effort_hours on every L3 task
8. No Level 4 nesting
9. Move specifications wbs.level_0 into wbs.levels.level_0 (do not leave level_0 at wbs root)

## Response Format

Return the complete wbs_input.json in a single JSON code block AND write it to disk at projects/<project-slug>/inputs/wbs_input.json.

Now, generate the wbs_input.json for the project described above.
```
