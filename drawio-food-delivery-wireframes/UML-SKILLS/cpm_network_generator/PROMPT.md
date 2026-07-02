# CPM Network Diagram Generator — Agent Prompt

Use this file to generate the input JSON required by the **CPM Network Diagram Generator**. Any agentic AI working on any project can follow this prompt to produce a valid `cpm_network_input.json` that renders an Activity-on-Node (AON) Critical Path Method network diagram as a fully editable Visio file (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`cpm_network` is listed** in `specifications.json → diagrams_to_generate`
3. Read [cpm-network-diagram-generator-SKILL.md](../cpm-network-diagram-generator-SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | Description |
|--------|--------|-------------|
| CPM network diagram | `.vsdx` | AON activity nodes with ES/EF/LS/LF, slack, critical path highlighting, dependency arrows |
| CPM calculations | (embedded) | Forward/backward pass, total float, free float, critical path identification |

## Output File Location

Save the generated input to:

```text
projects/<project-slug>/inputs/cpm_network_input.json
```

Example: `projects/daatsna-community-data-platform/inputs/cpm_network_input.json`

---

## Agent Instructions

You are a project scheduling specialist. Your task is to generate a complete `cpm_network_input.json` file for the CPM Network Diagram Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json` (especially `wbs`, `phases`, `milestones`, and timeline).
2. Decompose the project into activities with durations and predecessor dependencies.
3. Build a directed acyclic graph (DAG) — no cycles allowed.
4. Validate against all rules in the Validation section.
5. Write the file to `projects/<project-slug>/inputs/cpm_network_input.json`.
6. Return the complete JSON in a single code block and confirm the file path.

If `specifications.json` is missing, gather project name, activities, durations, and dependencies from the user — or infer from WBS/milestones and list assumptions.

---

## Mapping from specifications.json

Transform project schedule data into CPM activities:

| specifications.json | cpm_network_input.json | Notes |
|-----------------------|------------------------|-------|
| `project.name` | `cpm_network.project_name` | Full project name |
| `project.version` | `cpm_network.version` | e.g. `"1.0"` |
| `project.date` | `cpm_network.date` | `YYYY-MM-DD` |
| `project.description` | `cpm_network.description` | Brief context |
| `wbs.branches[]` | activities (Level 1) | Major phases become activity groups |
| `wbs.branches[].children[]` | activities (Level 2) | Work packages become activities |
| `phases[]` | duration_units, sequencing | Phase order informs predecessor chains |
| `milestones[]` | optional zero-duration nodes | Can model as `duration: 0` activities |

### Deriving activities from WBS

1. Create a **Start** node (`id: "S"`, `duration: 0`, `is_start: true`).
2. Map each WBS Level 1 branch to one or more activities.
3. Map WBS Level 2 children to individual activities with realistic durations.
4. Chain activities using Finish-to-Start (`FS`) dependencies by default.
5. Where WBS branches run in parallel, give them the same predecessor but no dependency on each other.
6. Where branches merge (e.g., Integration depends on Backend + Frontend), list multiple predecessors.
7. Create an **End** node (`id: "END"`, `duration: 0`, `is_end: true`) fed by the final activity.

### Estimating durations

When dates are available but durations are not:

```text
duration (weeks) = ceil((end_date - start_date).days / 7)
```

Default to `duration_units: "weeks"`. Use `"days"` for short projects.

---

## JSON Schema

Generate a complete JSON file with this structure:

```json
{
  "cpm_network": {
    "title": "string - Diagram title",
    "project_name": "string - Full project name",
    "version": "string - Version (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",
    "description": "string - Brief description",

    "activities": [
      {
        "id": "string - Unique activity ID (e.g., A, B, S, END)",
        "name": "string - Activity name",
        "description": "string - Optional detailed description",
        "duration": "number - Duration in duration_units (0 for milestones)",
        "duration_units": "string - weeks | days (default: weeks)",
        "predecessors": "array - See Predecessor Format below",
        "is_start": "boolean - true for project start node",
        "is_end": "boolean - true for project end node"
      }
    ],

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "critical_path_color": "#E53935",
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

### Predecessor format

Predecessors accept two forms:

**Shorthand** (Finish-to-Start, lag 0):

```json
"predecessors": ["A", "B"]
```

**Full object** (explicit type and lag):

```json
"predecessors": [
  {"id": "A", "type": "FS", "lag": 0},
  {"id": "B", "type": "SS", "lag": 2}
]
```

| Type | Meaning | Use when |
|------|---------|----------|
| `FS` | Finish-to-Start | Successor starts after predecessor finishes (default) |
| `SS` | Start-to-Start | Successor starts when predecessor starts |
| `FF` | Finish-to-Finish | Successor finishes when predecessor finishes |
| `SF` | Start-to-Finish | Successor finishes when predecessor starts (rare) |

`lag` is an integer offset in the same units as `duration_units` (can be negative).

---

## Section Guidelines

### Activities

- **Minimum 2, recommended 8–20** (including Start/End nodes)
- Every activity needs a unique `id` (single letters `A`–`Z` or short codes like `S`, `END`)
- Exactly one activity should have `is_start: true` (typically `S` with `duration: 0`)
- Exactly one activity should have `is_end: true` (typically `END` with `duration: 0`)
- Start node: `predecessors: []`
- End node: predecessor is the final project activity
- All other activities must have at least one predecessor
- Durations must be ≥ 0; use `0` for milestones/start/end nodes

### Typical software project activity chain

```text
S → Charter → Schedule → Requirements → Design → Development → Integration → Testing → Deployment → END
```

Parallel paths example:

```text
        → Requirements Analysis (E) ─┐
Requirements (D) ─                  ├→ Database Design (G) → ...
        → Requirements Spec (F) ────┘

        → Backend Dev (J) ─┐
Integration prep ─        ├→ Integration (L) → ...
        → Frontend Dev (K) ┘
```

### Dependency defaults

- Use `FS` with `lag: 0` unless the user specifies otherwise
- Prefer shorthand `"predecessors": ["A"]` for simple FS links
- Use full objects when type is not FS or lag ≠ 0

### Styling and layout

- Use defaults unless the user requests changes
- Critical path nodes are auto-highlighted red by the generator (no manual flag needed)

---

## Validation Rules

Fix every failure before writing the file:

1. All required fields populated — no empty `id` or `name`
2. At least **2 activities**
3. All activity IDs unique
4. Every predecessor references an existing activity ID
5. **No cycles** — the network must be a directed acyclic graph (DAG)
6. Exactly one `is_start: true` and one `is_end: true` (recommended)
7. Start node has empty predecessors; all non-start activities have ≥ 1 predecessor
8. All non-end activities must eventually lead to the end node (connected graph)
9. `duration` ≥ 0 for all activities
10. Dependency `type` is one of: `FS`, `SS`, `FF`, `SF`
11. `lag` is an integer
12. Dates in `YYYY-MM-DD` format
13. JSON is syntactically valid

Optional validation:

```bash
python cpm_network_generator/cli.py projects/<project-slug>/inputs/cpm_network_input.json --validate-only
```

---

## Quick Reference Card

| Section | Minimum | Maximum | Key Rule |
|---------|---------|---------|----------|
| Activities | 2 | 50 | Unique IDs; DAG only |
| Predecessors per activity | 0 (start only) | — | All refs must exist |
| Dependency types | FS (default) | FS/SS/FF/SF | No cycles |
| Start/End nodes | 1 each (recommended) | — | duration: 0 |

---

## Example Activity Set (abbreviated)

```text
S (Start, dur=0)
  → A: Develop Charter (2w)
    → B: Create Schedule (4w) ──→ D: Requirements Elicitation (6w)
    → C: Define Budget (3w)          ├→ E: Req Analysis (4w) ─┐
                                     └→ F: Req Spec (3w) ─────┼→ G: DB Design (5w)
                                                              → H: API Design (6w)
                                                                  ├→ I: UI/UX (7w) → K: Frontend (10w) ─┐
                                                                  └→ J: Backend (12w) ──────────────────┼→ L: Integration (4w)
                                                                                                         → M: Testing (6w)
                                                                                                           → N: Deployment (3w)
                                                                                                             → END (dur=0)
```

---

## After Generating Input

Run the generator:

```bash
# Render Visio diagram
python cpm_network_generator/cli.py projects/<project-slug>/inputs/cpm_network_input.json \
  --output-dir projects/<project-slug>/output

# Validate only
python cpm_network_generator/cli.py projects/<project-slug>/inputs/cpm_network_input.json --validate-only
```

Output: `projects/<project-slug>/output/cpm_diagram.vsdx`

Reference implementation: [examples/sample_input.json](examples/sample_input.json)

---

## Integration Notes

- The same activity list can feed [gantt-chart-generator-SKILL.md](../gantt-chart-generator-SKILL.md) with minimal transformation.
- CPM uses **deterministic durations**; for probabilistic (optimistic/likely/pessimistic) estimates, use [pert-chart-generator-SKILL.md](../pert-chart-generator-SKILL.md) instead.

---

## Copy-Ready Agent Prompt

```
You are a project scheduling specialist. Your task is to generate a complete cpm_network_input.json file for the CPM Network Diagram Generator (Visio .vsdx output with critical path calculation).

Read the project data from specifications.json or the project description below. Follow the JSON schema in cpm_network_generator/PROMPT.md exactly. If information is not explicitly provided, derive activities from WBS/phases and list assumptions.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Software Development, Healthcare, Infrastructure]
**Timeline:** [START DATE - END DATE]
**Major Phases / WBS:** [LIST PHASES OR WORK PACKAGES]
**Known Dependencies:** [DESCRIBE WHICH ACTIVITIES DEPEND ON WHICH]
**Parallel Work Streams:** [LIST ANY PARALLEL TRACKS]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables

1. A complete, valid cpm_network_input.json following the schema in cpm_network_generator/PROMPT.md
2. Saved to projects/<project-slug>/inputs/cpm_network_input.json
3. All validation rules satisfied

## Validation Rules

1. At least 2 activities with unique IDs
2. Include Start (S, duration 0) and End (END, duration 0) nodes
3. Every predecessor ID references an existing activity
4. No cycles in the dependency graph
5. Default to FS dependencies with lag 0
6. Realistic durations in weeks (or days for short projects)
7. Parallel branches share a predecessor but not each other
8. Merge points list all required predecessors

## Response Format

Return the complete cpm_network_input.json in a single JSON code block AND write it to disk at projects/<project-slug>/inputs/cpm_network_input.json.

Now, generate the cpm_network_input.json for the project described above.
```
