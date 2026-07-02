# Kanban Chart Generator — Agent Prompt

Use this file to generate the input JSON required by the **Kanban Chart Generator**. Any agentic AI working on any project can follow this prompt to produce a valid `kanban_input.json` that renders an agile workflow dashboard as a fully editable Visio file (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`kanban_chart` is listed** in `specifications.json → diagrams_to_generate`
3. Read [kanban-chart-generator-SKILL.md](../kanban-chart-generator-SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | Description |
|--------|--------|-------------|
| Kanban board | `.vsdx` | Workflow columns, swimlanes, work item cards, WIP limits, priority color coding |

## Output File Location

Save the generated input to:

```text
projects/<project-slug>/inputs/kanban_input.json
```

Example: `projects/daatsna-community-data-platform/inputs/kanban_input.json`

---

## Agent Instructions

You are an agile workflow documentation specialist. Your task is to generate a complete `kanban_input.json` file for the Kanban Chart Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json`, issue trackers, or the sprint/backlog described by the user.
2. Define workflow columns, swimlanes, and work item cards with current status.
3. Ensure every card's `status` matches a column ID and `swimlane_id` matches a swimlane ID.
4. Respect WIP limits — item count per column must not exceed `wip_limit` when set.
5. Validate against all rules in the Validation section.
6. Write the file to `projects/<project-slug>/inputs/kanban_input.json`.
7. Return the complete JSON in a single code block and confirm the file path.

If `specifications.json` is missing, gather project name, sprint, columns, and backlog items from the user — or infer from WBS/objectives and list assumptions.

---

## Mapping from specifications.json

| specifications.json | kanban_input.json | Notes |
|---------------------|-------------------|-------|
| `project.name` | `kanban_chart.project_name` | Full project name |
| `project.version` | `kanban_chart.version` | e.g. `"1.0"` |
| `project.date` | `kanban_chart.date` | `YYYY-MM-DD` |
| `wbs.branches[].children[]` | `work_items[]` | Work packages → cards |
| `objectives[]` | Features/Epics swimlane items | Strategic goals → feature cards |
| `risks[]` (high severity) | Bug/Task cards in Bugs swimlane | Blockers and defects |
| User sprint name | `kanban_chart.sprint` | e.g. `"Sprint 5"` |

### Deriving work items from WBS

For each WBS Level 2 work package, create a work item:

```json
{
  "id": "FEAT-001",
  "title": "<work package name>",
  "type": "Feature",
  "status": "<column based on estimated progress>",
  "priority": "Medium",
  "assignee": "<inferred team member or TBD>",
  "swimlane_id": "SL1"
}
```

Assign `status` based on project phase:

| Project phase | Typical column |
|---------------|----------------|
| Not started | `BACKLOG` |
| Planning complete | `SELECTED` |
| In analysis | `ANALYZE` |
| In development | `DEVELOP` |
| In QA | `TEST` |
| In review | `REVIEW` |
| Ready to release | `DEPLOY` |
| Complete | `DONE` |
| Blocked by risk/dependency | `BLOCKED` |

---

## JSON Schema

Generate a complete JSON file with this structure (aligned with `core/models.py`):

```json
{
  "kanban_chart": {
    "title": "string - Diagram title",
    "project_name": "string - Full project name",
    "version": "string - Version (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",
    "sprint": "string - Optional sprint label (e.g., Sprint 5)",
    "description": "string - Optional board description",

    "columns": [
      {
        "id": "string - Unique column ID (e.g., BACKLOG)",
        "name": "string - Display name",
        "description": "string - Optional column description",
        "wip_limit": "number or null - Max items in column; null = unlimited",
        "color": "string - Hex background color",
        "text_color": "string - Hex header text color",
        "order": "number - Left-to-right position (1, 2, 3, ...)"
      }
    ],

    "swimlanes": [
      {
        "id": "string - Unique swimlane ID (e.g., SL1)",
        "name": "string - Swimlane name",
        "color": "string - Hex label color",
        "text_color": "string - Hex text color",
        "icon": "string - Optional icon character"
      }
    ],

    "work_items": [
      {
        "id": "string - Unique item ID (e.g., FEAT-100, BUG-200)",
        "title": "string - Short card title",
        "type": "string - Feature | Bug | Task | Story | Epic",
        "status": "string - Must match a columns[].id exactly",
        "priority": "string - High | Medium | Low",
        "assignee": "string - Owner name",
        "swimlane_id": "string - Must match a swimlanes[].id exactly",
        "size": "number - Optional story points or effort",
        "tags": ["string - Optional labels"]
      }
    ],

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "card_width": 2.0,
      "card_height": 1.0,
      "show_wip_limits": true
    },

    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "cell_padding": 0.2
    }
  }
}
```

**Important:** Use `swimlane_id` (not `swimlane`). Use singular types: `Feature`, `Bug`, `Task` (not `Features`).

---

## Section Guidelines

### Columns

- **Minimum 3, recommended 5–9**
- Standard agile workflow (adapt to project):

| order | id | name | wip_limit | color | text_color |
|-------|-----|------|-----------|-------|------------|
| 1 | `BACKLOG` | Backlog | null | `#E3F2FD` | `#0D47A1` |
| 2 | `SELECTED` | Selected | 20 | `#FFF3E0` | `#E65100` |
| 3 | `ANALYZE` | Analyze | 5 | `#FFF9C4` | `#F57F17` |
| 4 | `DEVELOP` | Develop | 8 | `#E8F5E9` | `#1B5E20` |
| 5 | `TEST` | Test | 6 | `#F3E5F5` | `#4A148C` |
| 6 | `REVIEW` | Review | 4 | `#FCE4EC` | `#880E4F` |
| 7 | `DEPLOY` | Deploy | 3 | `#E0F7FA` | `#006064` |
| 8 | `DONE` | Done | null | `#E8F5E9` | `#1B5E20` |
| 9 | `BLOCKED` | Blocked | null | `#FFEBEE` | `#B71C1C` |

- Simpler boards can use: `BACKLOG` → `DEVELOP` → `DONE` (see sample input)
- Column IDs must be **UPPERCASE** or consistent identifiers; work item `status` must match exactly
- `order` values must be unique and sequential

### Swimlanes

- **Minimum 1, recommended 2–4**
- Standard swimlanes:

| id | name | color | icon |
|----|------|-------|------|
| `SL1` | Features | `#1a237e` | `★` |
| `SL2` | Bugs | `#C62828` | (optional) |
| `SL3` | Tasks | `#2E7D32` | `✓` |

- Map work item `type` to swimlane:
  - `Feature`, `Story`, `Epic` → Features swimlane
  - `Bug` → Bugs swimlane
  - `Task` → Tasks swimlane

### Work items

- **Minimum 1, recommended 8–30** for a realistic board
- ID prefixes: `FEAT-`, `BUG-`, `TASK-`, `STORY-`, `EPIC-`
- `priority`: `High`, `Medium`, or `Low` only
- `assignee`: required — use team member names or role names (e.g., `"Alice"`, `"Backend Lead"`)
- Distribute items across columns to reflect realistic workflow state
- **WIP limits are enforced** — count items per column; do not exceed `wip_limit`

### WIP limit rule

```text
For each column with wip_limit set:
  count(work_items where status == column.id) <= wip_limit
```

If you need more items in a column, either increase `wip_limit` or set it to `null`.

---

## Validation Rules

Fix every failure before writing the file:

1. All required fields populated
2. At least **1 column** and **1 swimlane**
3. At least **1 work item** (recommended)
4. All column IDs unique; all swimlane IDs unique; all work item IDs unique
5. Every work item `status` matches a `columns[].id` exactly
6. Every work item `swimlane_id` matches a `swimlanes[].id` exactly
7. Every work item `type` is one of: `Feature`, `Bug`, `Task`, `Story`, `Epic`
8. Every work item `priority` is one of: `High`, `Medium`, `Low`
9. Every work item has a non-empty `assignee`
10. WIP limits not exceeded per column
11. Dates in `YYYY-MM-DD` format (if provided)
12. JSON is syntactically valid

Optional validation:

```bash
python kanban_chart_generator/cli.py projects/<project-slug>/inputs/kanban_input.json --validate-only
```

---

## Quick Reference Card

| Section | Minimum | Maximum | Key Rule |
|---------|---------|---------|----------|
| Columns | 1 | 12 | Unique IDs; ordered |
| Swimlanes | 1 | 6 | Unique IDs |
| Work items | 1 | 50 | status + swimlane_id must exist |
| WIP limit | — | — | Item count ≤ limit per column |
| Priority | — | — | High / Medium / Low only |
| Type | — | — | Feature / Bug / Task / Story / Epic |

---

## After Generating Input

Run the generator:

```bash
# Render Visio Kanban board
python kanban_chart_generator/cli.py projects/<project-slug>/inputs/kanban_input.json \
  -o projects/<project-slug>/output/kanban_chart.vsdx

# Validate only
python kanban_chart_generator/cli.py projects/<project-slug>/inputs/kanban_input.json --validate-only
```

Reference implementation: [examples/sample_input.json](examples/sample_input.json)

---

## Integration Notes

- Complements [gantt-chart-generator-SKILL.md](../gantt-chart-generator-SKILL.md) (time-based) with state-based workflow view.
- Work items can be derived from the same WBS used for Gantt and CPM inputs.
- Embedded in [project-charter-generator-SKILL.md](../project-charter-generator-SKILL.md) agile dashboards.

---

## Copy-Ready Agent Prompt

```
You are an agile workflow documentation specialist. Your task is to generate a complete kanban_input.json file for the Kanban Chart Generator (Visio .vsdx output).

Read the project data from specifications.json, issue trackers, or the sprint/backlog described below. Follow the JSON schema in kanban_chart_generator/PROMPT.md exactly. If information is not explicitly provided, derive columns, swimlanes, and work items from WBS/objectives and list assumptions.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Sprint / Iteration:** [e.g., Sprint 5]
**Workflow Columns:** [LIST COLUMNS OR USE DEFAULT AGILE SET]
**Swimlanes:** [e.g., Features, Bugs, Tasks]
**Backlog Items:** [LIST WORK ITEMS WITH STATUS, PRIORITY, ASSIGNEE]
**WIP Limits:** [OPTIONAL LIMITS PER COLUMN]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables

1. A complete, valid kanban_input.json following the schema in kanban_chart_generator/PROMPT.md
2. Saved to projects/<project-slug>/inputs/kanban_input.json
3. All validation rules satisfied

## Validation Rules

1. At least 1 column, 1 swimlane, and 1 work item
2. Every work item status matches a columns[].id exactly
3. Every work item swimlane_id matches a swimlanes[].id exactly
4. Type: Feature, Bug, Task, Story, or Epic (singular)
5. Priority: High, Medium, or Low only
6. WIP limits not exceeded (item count per column ≤ wip_limit)
7. All work items have an assignee
8. Use swimlane_id (not swimlane)

## Response Format

Return the complete kanban_input.json in a single JSON code block AND write it to disk at projects/<project-slug>/inputs/kanban_input.json.

Now, generate the kanban_input.json for the project described above.
```
