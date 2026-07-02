# Gantt Chart Generator — Agent Prompt

Use this file to generate the input JSON required by the **Gantt Chart Generator**. Any agentic AI working on any project can follow this prompt to produce a valid `gantt_input.json` that renders a professional Gantt chart as a fully editable Visio file (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`gantt_chart` is listed** in `specifications.json → diagrams_to_generate`
3. Read [gantt-chart-generator-SKILL.md](../gantt-chart-generator-SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | Description |
|--------|--------|-------------|
| Gantt chart | `.vsdx` | Phase-grouped task list, timeline bars, milestones, dependency arrows, optional progress overlay |

## Output File Location

Save the generated input to:

```text
projects/<project-slug>/inputs/gantt_input.json
```

Example: `projects/daatsna-community-data-platform/inputs/gantt_input.json`

---

## Agent Instructions

You are a project scheduling specialist. Your task is to generate a complete `gantt_input.json` file for the Gantt Chart Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json` (especially `phases`, `milestones`, `wbs`, and project dates).
2. Map phases and WBS work packages into nested tasks with calendar start/end dates.
3. Wire Finish-to-Start dependencies between tasks and milestones.
4. Validate against all rules in the Validation section.
5. Write the file to `projects/<project-slug>/inputs/gantt_input.json`.
6. Return the complete JSON in a single code block and confirm the file path.

If `specifications.json` is missing, gather project name, timeline, phases, tasks, and milestones from the user — or infer from WBS and list assumptions.

---

## Mapping from specifications.json

| specifications.json | gantt_input.json | Notes |
|---------------------|------------------|-------|
| `project.name` | `gantt_chart.project_name` | Full project name |
| `project.version` | `gantt_chart.version` | e.g. `"1.0"` |
| `project.date` | `gantt_chart.date` | `YYYY-MM-DD` |
| `project.start_date` | `gantt_chart.start_date` | Project timeline start |
| `project.end_date` | `gantt_chart.end_date` | Project timeline end |
| `phases[]` | `gantt_chart.phases[]` | One Gantt phase per spec phase |
| `phases[].id` | `phases[].id` | e.g. `"P1"` |
| `phases[].name` | `phases[].name` | Phase name |
| `phases[].start` / `phases[].end` | task date bounds | Tasks must fall within phase window |
| `phases[].color` | `phases[].color` | Hex from spec or default palette |
| `wbs.branches[]` | phase tasks (level 1) | Major deliverables |
| `wbs.branches[].children[]` | nested tasks (level 2+) | Work packages |
| `milestones[]` | `gantt_chart.milestones[]` | Diamond markers on timeline |

### Deriving tasks from WBS

1. For each `phases[]` entry, create a matching Gantt phase block.
2. Map each WBS Level 1 branch under that phase to a **level 1** task (`T{n}.1`, `T{n}.2`, …).
3. Map WBS Level 2 children to **level 2** tasks (`T{n}.1.1`, `T{n}.1.2`, …).
4. Assign `start` and `end` dates that:
   - Fall within `gantt_chart.start_date` – `gantt_chart.end_date`
   - Fit inside the parent phase date range
   - Respect dependencies (successor starts on or after predecessor ends for FS)
5. Set `completion` based on project progress (0 for future, 100 for past, partial for in-progress).

### Task ID convention

```text
Phase P1 → tasks T1.1, T1.1.1, T1.1.2, T1.2, …
Phase P2 → tasks T2.1, T2.1.1, …
Milestones → M1, M2, M3, …
```

### Mapping from CPM network (if available)

If `cpm_network_input.json` exists, convert CPM activities to Gantt tasks:

| CPM field | Gantt field |
|-----------|-------------|
| `activities[].id` | `tasks[].id` (prefix with phase, e.g. `T3.1`) |
| `activities[].name` | `tasks[].name` |
| `activities[].duration` + ES | `start` / `end` dates | Compute from project start + ES/duration |
| predecessor chain | `dependencies[]` | FS mapping: `"dependencies": ["T1.1.1"]` |

---

## JSON Schema

Generate a complete JSON file with this structure:

```json
{
  "gantt_chart": {
    "title": "string - Diagram title",
    "project_name": "string - Full project name",
    "version": "string - Version (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",
    "start_date": "string - Project start (YYYY-MM-DD)",
    "end_date": "string - Project end (YYYY-MM-DD)",

    "phases": [
      {
        "id": "string - Unique phase ID (e.g., P1)",
        "name": "string - Phase name",
        "description": "string - Optional phase description",
        "color": "string - Hex color (e.g., #1565C0)",
        "text_color": "string - Hex color (typically #FFFFFF)",
        "tasks": [
          {
            "id": "string - Unique task ID (e.g., T1.1, T1.1.1)",
            "name": "string - Task name",
            "description": "string - Optional task description",
            "start": "string - Start date (YYYY-MM-DD)",
            "end": "string - End date (YYYY-MM-DD)",
            "completion": "number - 0 to 100 percent complete",
            "dependencies": ["string - Task or milestone IDs"],
            "level": "number - 1, 2, or 3 (indentation depth)"
          }
        ]
      }
    ],

    "milestones": [
      {
        "id": "string - Unique ID (e.g., M1)",
        "name": "string - Milestone name",
        "date": "string - Milestone date (YYYY-MM-DD)",
        "dependencies": ["string - Optional task IDs this milestone depends on"]
      }
    ],

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "bar_height": 0.4,
      "row_height": 0.6,
      "show_percent_complete": false,
      "critical_path_color": "#E53935"
    },

    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "grid_spacing": "weeks"
    }
  }
}
```

**Note:** Task-level `dependencies[]` is the primary dependency mechanism. Do not add a separate top-level `dependencies` array unless the generator is extended to support it — the current validator reads dependencies from tasks and milestones only.

---

## Section Guidelines

### Project timeline

- `start_date` must be strictly before `end_date`
- All task dates should fall within the project timeline
- Match `specifications.json → project.start_date` and `project.end_date`

### Phases

- **Minimum 1 phase, recommended 3–8**
- Each phase must contain at least 1 task
- Assign colors from the default palette (see below)
- Phase bar span is auto-calculated from earliest task start to latest task end

### Default phase color palette

| Phase type | Hex | text_color |
|------------|-----|------------|
| Project Management | `#1565C0` | `#FFFFFF` |
| Requirements | `#2E7D32` | `#FFFFFF` |
| System Design | `#E65100` | `#FFFFFF` |
| Development | `#6A1B9A` | `#FFFFFF` |
| Testing | `#C62828` | `#FFFFFF` |
| Deployment | `#00838F` | `#FFFFFF` |
| Security | `#1a237e` | `#FFFFFF` |
| Training | `#FF8F00` | `#333333` |

### Tasks

- **Minimum 1 task per phase, recommended 3–15 total per phase**
- `level` controls left-pane indentation:
  - `1` — work package (e.g., Planning, Elicitation)
  - `2` — sub-task (e.g., Develop Charter, Stakeholder Interviews)
  - `3` — detailed sub-task (rare)
- `start` must be on or before `end`
- `completion`: integer 0–100
  - Past tasks: `100`
  - Future tasks: `0`
  - In-progress: realistic partial (e.g., `50`, `75`)
- `dependencies[]`: list of task/milestone IDs that must complete/start first (Finish-to-Start implied)

### Milestones

- **Minimum 0, recommended 3–8**
- Map from `specifications.json → milestones[]`
- `date` must be within project timeline
- Mark critical milestones from spec (`is_critical: true` → include as key milestones)
- `dependencies[]` optionally links milestone to preceding tasks

### Typical software project phases

```text
P1: Project Management    → Planning, Monitoring, Reporting
P2: Requirements          → Elicitation, Analysis, Specification
P3: System Design         → Database, API, UI/UX
P4: Development           → Backend, Frontend, Integration
P5: Testing               → Unit, Integration, System, UAT
P6: Deployment            → Infrastructure, Deploy, Cutover
```

---

## Validation Rules

Fix every failure before writing the file:

1. All required fields populated
2. At least **1 phase** with at least **1 task** each
3. `start_date` strictly before `end_date`
4. All task IDs unique across the entire chart (including milestones)
5. All dates in `YYYY-MM-DD` format
6. Every task: `start` ≤ `end`
7. Every task: `0 ≤ completion ≤ 100`
8. Every entry in `dependencies[]` references an existing task or milestone ID
9. No circular dependencies (task A → B → A)
10. JSON is syntactically valid

Optional validation:

```bash
python gantt_chart_generator/cli.py projects/<project-slug>/inputs/gantt_input.json --validate-only
```

---

## Quick Reference Card

| Section | Minimum | Maximum | Key Rule |
|---------|---------|---------|----------|
| Phases | 1 | 8 | ≥ 1 task each |
| Tasks per phase | 1 | — | Unique IDs |
| Task levels | 1 | 3 | Controls indentation |
| Milestones | 0 | 15 | Dates within timeline |
| Completion | 0 | 100 | Integer percent |

---

## After Generating Input

Run the generator:

```bash
# Render Visio Gantt chart
python gantt_chart_generator/cli.py projects/<project-slug>/inputs/gantt_input.json \
  -o projects/<project-slug>/output/gantt_chart.vsdx

# Show completion progress on bars
python gantt_chart_generator/cli.py projects/<project-slug>/inputs/gantt_input.json \
  -o projects/<project-slug>/output/gantt_chart.vsdx --show-progress

# Validate only
python gantt_chart_generator/cli.py projects/<project-slug>/inputs/gantt_input.json --validate-only
```

Reference implementation: [examples/sample_input.json](examples/sample_input.json)

---

## Integration Notes

- Shares schedule data with [cpm-network-diagram-generator-SKILL.md](../cpm-network-diagram-generator-SKILL.md) — CPM uses durations; Gantt uses calendar dates.
- Milestones align with [milestone-chart-generator-SKILL.md](../milestone-chart-generator-SKILL.md).
- Embedded in [project-charter-generator-SKILL.md](../project-charter-generator-SKILL.md) deliverables.

---

## Copy-Ready Agent Prompt

```
You are a project scheduling specialist. Your task is to generate a complete gantt_input.json file for the Gantt Chart Generator (Visio .vsdx output).

Read the project data from specifications.json or the project description below. Follow the JSON schema in gantt_chart_generator/PROMPT.md exactly. If information is not explicitly provided, derive phases, tasks, and dates from WBS/milestones and list assumptions.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Software Development, Healthcare, Infrastructure]
**Timeline:** [START DATE - END DATE]
**Phases:** [LIST PROJECT PHASES]
**Major Tasks / WBS:** [LIST WORK PACKAGES AND SUB-TASKS]
**Milestones:** [LIST KEY MILESTONES WITH DATES]
**Dependencies:** [DESCRIBE WHICH TASKS DEPEND ON WHICH]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables

1. A complete, valid gantt_input.json following the schema in gantt_chart_generator/PROMPT.md
2. Saved to projects/<project-slug>/inputs/gantt_input.json
3. All validation rules satisfied

## Validation Rules

1. At least 1 phase, each with at least 1 task
2. start_date strictly before end_date
3. All task IDs unique; dates in YYYY-MM-DD format
4. Task start ≤ end; completion 0–100
5. All dependency IDs reference existing tasks or milestones
6. Task dates within project timeline
7. Use level 1 for work packages, level 2 for sub-tasks
8. Map milestones from specifications with matching dates

## Response Format

Return the complete gantt_input.json in a single JSON code block AND write it to disk at projects/<project-slug>/inputs/gantt_input.json.

Now, generate the gantt_input.json for the project described above.
```
