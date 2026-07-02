# PERT Chart Generator — Agent Prompt

Use this file to generate the input JSON required by the **PERT Chart Generator**. Any agentic AI working on any project can follow this prompt to produce a valid `pert_input.json` that renders a Program Evaluation and Review Technique network diagram as a fully editable Visio file (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`pert_chart` is listed** in `specifications.json → diagrams_to_generate`
3. Read [pert-chart-generator-SKILL.md](../pert-chart-generator-SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | Description |
|--------|--------|-------------|
| PERT network diagram | `.vsdx` | Task nodes, dependency arrows, ES/EF/LS/LF/slack, critical path highlighting |
| Three-point estimates | (optional) | Optimistic, Most Likely, Pessimistic durations on nodes |

## Output File Location

Save the generated input to:

```text
projects/<project-slug>/inputs/pert_input.json
```

Example: `projects/daatsna-community-data-platform/inputs/pert_input.json`

---

## Agent Instructions

You are a project scheduling specialist. Your task is to generate a complete `pert_input.json` file for the PERT Chart Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json` (especially `wbs`, `phases`, and timeline).
2. Decompose the project into tasks with durations, dependencies, and optional three-point estimates.
3. Build a directed acyclic graph (DAG) — no cycles allowed.
4. Validate against all rules in the Validation section.
5. Write the file to `projects/<project-slug>/inputs/pert_input.json`.
6. Return the complete JSON in a single code block and confirm the file path.

If `specifications.json` is missing, gather project name, activities, durations, and dependencies from the user — or infer from WBS/phases and list assumptions.

---

## PERT vs CPM — When to Use This Generator

| Use PERT (`pert_input.json`) | Use CPM (`cpm_network_input.json`) |
|------------------------------|-------------------------------------|
| Uncertain durations (O/M/P estimates) | Fixed deterministic durations |
| Probabilistic scheduling | Advanced dependency types (FS/SS/FF/SF) with lag |
| Expected duration: `(O + 4M + P) / 6` | Activity-on-Node with explicit lag |

Both produce network diagrams with critical path calculation. Use PERT when task durations have uncertainty.

---

## Mapping from specifications.json

| specifications.json | pert_input.json | Notes |
|-----------------------|-----------------|-------|
| `project.name` | `pert_chart.project_name` | Full project name |
| `project.version` | `pert_chart.version` | e.g. `"1.0"` |
| `project.date` | `pert_chart.date` | `YYYY-MM-DD` |
| `project.description` | `pert_chart.description` | Brief context |
| `wbs.branches[]` | tasks (Level 1) | Major deliverables |
| `wbs.branches[].children[]` | tasks (Level 2) | Work packages |

### Deriving tasks from WBS

1. Map each WBS work package to a task with a single-letter or short ID (`A`, `B`, … or `T1`, `T2`).
2. Chain dependencies using Finish-to-Start logic via the `dependencies[]` string array.
3. Estimate duration in weeks (or days for short projects).
4. Add three-point estimates when duration is uncertain.

### Three-point estimate rules

When providing `optimistic`, `most_likely`, and `pessimistic`:

```text
Expected Duration (TE) = (optimistic + 4 × most_likely + pessimistic) / 6
```

Set `duration` to `TE` (rounded) or to `most_likely`. Ensure:

```text
optimistic ≤ most_likely ≤ pessimistic
```

Example for a 2-week task:

```json
{
  "duration": 2,
  "optimistic": 1,
  "most_likely": 2,
  "pessimistic": 4
}
```

### Mapping from CPM network (if available)

If `cpm_network_input.json` exists, convert directly:

| CPM field | PERT field |
|-----------|------------|
| `cpm_network.activities[]` | `pert_chart.tasks[]` |
| `activities[].id` | `tasks[].id` |
| `activities[].name` | `tasks[].name` |
| `activities[].duration` | `tasks[].duration` |
| `predecessors[].id` or string predecessor | `tasks[].dependencies[]` |

Add O/M/P estimates to CPM activities when converting to PERT. CPM predecessor objects collapse to simple ID strings (FS implied).

---

## JSON Schema

Generate a complete JSON file with this structure:

```json
{
  "pert_chart": {
    "title": "string - Diagram title",
    "project_name": "string - Full project name",
    "version": "string - Version (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",
    "description": "string - Optional brief description",

    "tasks": [
      {
        "id": "string - Unique task ID (e.g., A, B, C)",
        "name": "string - Task name",
        "description": "string - Optional detailed description",
        "duration": "number - Expected duration (weeks or days)",
        "duration_units": "string - weeks | days (default: weeks)",
        "optimistic": "number - Optional best-case duration",
        "most_likely": "number - Optional most probable duration",
        "pessimistic": "number - Optional worst-case duration",
        "dependencies": ["string - Predecessor task IDs"],
        "is_start": "boolean - Optional; true for first task(s)"
      }
    ],

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "show_three_point": false
    },

    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "node_width": 2.0,
      "node_height": 1.2,
      "horizontal_spacing": 1.0,
      "vertical_spacing": 1.0
    }
  }
}
```

**Note:** Dependencies are simple string arrays (Finish-to-Start implied). Unlike CPM, PERT does not support FS/SS/FF/SF types or lag in the input schema.

---

## Section Guidelines

### Tasks

- **Minimum 2, recommended 6–16**
- Every task needs a unique `id`
- Entry tasks (no predecessors): `dependencies: []` — mark one with `is_start: true` if desired
- Terminal task: the last task in the critical chain (no successors in the graph)
- `duration` must be ≥ 0
- Parallel branches share a predecessor but not each other
- Merge points list all required predecessors

### Typical software project task chain

```text
A: Develop Charter (2w) → B: Create Schedule (4w) ──→ D: Requirements (6w)
                      └→ C: Define Budget (3w) ────────────────┘ (parallel)
D → E: Req Analysis (4w) ─┐
D → F: Req Spec (3w) ─────┼→ G: Database Design (5w) → H: API Design (6w) → ...
                          └→ (merge)
... → J: Backend (12w) ─┐
    → K: Frontend (10w) ─┼→ L: Integration (4w) → M: Testing (6w) → N: Deployment (3w)
```

### Duration estimation from project timeline

When phase dates are available:

```text
duration (weeks) = max(1, ceil((phase_end - phase_start).days / 7 / num_tasks_in_phase))
```

### Three-point estimates

- Provide O/M/P for **all tasks** or **none** — mixed is acceptable but less consistent
- Set `styling.show_three_point: true` to display O/M/P on the diagram (or use CLI `--show-three-point`)
- If O/M/P omitted, `duration` alone is sufficient (sample input works this way for some tasks)

---

## Validation Rules

Fix every failure before writing the file:

1. All required fields populated — every task needs `id`, `name`, `duration`
2. At least **2 tasks**
3. All task IDs unique
4. Every entry in `dependencies[]` references an existing task ID
5. **No cycles** — graph must be a directed acyclic graph (DAG)
6. All `duration` values ≥ 0
7. If O/M/P provided: `optimistic ≤ most_likely ≤ pessimistic`
8. If O/M/P provided: `duration` should equal `(O + 4M + P) / 6` or `most_likely` (± rounding)
9. Dates in `YYYY-MM-DD` format (if provided)
10. JSON is syntactically valid

Optional validation:

```bash
python pert_chart_generator/cli.py projects/<project-slug>/inputs/pert_input.json --validate-only
```

---

## Quick Reference Card

| Section | Minimum | Maximum | Key Rule |
|---------|---------|---------|----------|
| Tasks | 2 | 50 | Unique IDs; DAG only |
| Dependencies | 0 (entry tasks) | — | All refs must exist |
| Duration | ≥ 0 | — | weeks or days |
| O/M/P | optional | — | O ≤ M ≤ P |
| Critical path | (computed) | — | Slack = 0 auto-highlighted |

---

## After Generating Input

Run the generator:

```bash
# Render Visio PERT chart
python pert_chart_generator/cli.py projects/<project-slug>/inputs/pert_input.json \
  -o projects/<project-slug>/output/pert_chart.vsdx

# Show three-point estimates on nodes
python pert_chart_generator/cli.py projects/<project-slug>/inputs/pert_input.json \
  -o projects/<project-slug>/output/pert_chart.vsdx --show-three-point

# Validate only
python pert_chart_generator/cli.py projects/<project-slug>/inputs/pert_input.json --validate-only
```

Reference implementation: [examples/sample_input.json](examples/sample_input.json)

---

## Integration Notes

- Sibling to [cpm-network-diagram-generator-SKILL.md](../cpm-network-diagram-generator-SKILL.md) — same network concept, PERT adds uncertainty.
- Task list converts to [gantt-chart-generator-SKILL.md](../gantt-chart-generator-SKILL.md) when dates are assigned.
- Embedded in [project-charter-generator-SKILL.md](../project-charter-generator-SKILL.md) schedule appendices.

---

## Copy-Ready Agent Prompt

```
You are a project scheduling specialist. Your task is to generate a complete pert_input.json file for the PERT Chart Generator (Visio .vsdx output with critical path and optional three-point estimates).

Read the project data from specifications.json or the project description below. Follow the JSON schema in pert_chart_generator/PROMPT.md exactly. If information is not explicitly provided, derive tasks from WBS/phases and list assumptions.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Software Development, Healthcare, Infrastructure]
**Timeline:** [START DATE - END DATE]
**Major Activities / WBS:** [LIST WORK PACKAGES]
**Known Dependencies:** [DESCRIBE TASK DEPENDENCIES]
**Duration Uncertainty:** [NOTE IF O/M/P ESTIMATES ARE NEEDED]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables

1. A complete, valid pert_input.json following the schema in pert_chart_generator/PROMPT.md
2. Saved to projects/<project-slug>/inputs/pert_input.json
3. All validation rules satisfied

## Validation Rules

1. At least 2 tasks with unique IDs
2. Every dependency ID references an existing task
3. No cycles in the dependency graph
4. duration ≥ 0 for all tasks
5. If optimistic/most_likely/pessimistic provided: O ≤ M ≤ P
6. duration ≈ (O + 4M + P) / 6 when three-point estimates are used
7. Parallel branches share a predecessor; merge points list all predecessors
8. dependencies[] uses simple task ID strings (FS implied)

## Response Format

Return the complete pert_input.json in a single JSON code block AND write it to disk at projects/<project-slug>/inputs/pert_input.json.

Now, generate the pert_input.json for the project described above.
```
