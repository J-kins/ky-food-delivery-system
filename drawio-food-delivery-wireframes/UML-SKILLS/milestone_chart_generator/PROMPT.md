# Milestone Chart Generator — Agent Prompt

Use this file to generate the input JSON required by the **Milestone Chart Generator**. Any agentic AI working on any project can follow this prompt to produce a valid `milestone_input.json` that renders a chronological milestone timeline as a fully editable Visio file (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`milestone_chart` is listed** in `specifications.json → diagrams_to_generate`
3. Read [milestone-chart-generator-SKILL.md](../milestone-chart-generator-SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | Description |
|--------|--------|-------------|
| Milestone chart | `.vsdx` | Horizontal timeline, phase bands, diamond milestone markers, critical path emphasis, details table |

## Output File Location

Save the generated input to:

```text
projects/<project-slug>/inputs/milestone_input.json
```

Example: `projects/daatsna-community-data-platform/inputs/milestone_input.json`

---

## Agent Instructions

You are a project scheduling specialist. Your task is to generate a complete `milestone_input.json` file for the Milestone Chart Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json` (especially `phases`, `milestones`, and project dates).
2. Map phases to timeline bands and milestones to dated events.
3. Assign categories and critical flags.
4. Validate against all rules in the Validation section.
5. Write the file to `projects/<project-slug>/inputs/milestone_input.json`.
6. Return the complete JSON in a single code block and confirm the file path.

If `specifications.json` is missing, gather project name, timeline, phases, and key milestones from the user — or infer from project type and list assumptions.

---

## Mapping from specifications.json

Direct mapping — this generator aligns closely with the master spec:

| specifications.json | milestone_input.json | Notes |
|---------------------|----------------------|-------|
| `project.name` | `milestone_chart.project_name` | Full project name |
| `project.version` | `milestone_chart.version` | e.g. `"1.0"` |
| `project.date` | `milestone_chart.date` | `YYYY-MM-DD` |
| `project.start_date` | `milestone_chart.start_date` | Timeline start |
| `project.end_date` | `milestone_chart.end_date` | Timeline end |
| `project.description` | `milestone_chart.description` | Brief context |
| `phases[]` | `milestone_chart.phases[]` | Direct map: id, name, start, end, color |
| `milestones[]` | `milestone_chart.milestones[]` | Direct map: id, name, date, is_critical, description |

### Phase mapping

```json
{
  "id": "<phases[].id>",
  "name": "<phases[].name>",
  "start": "<phases[].start>",
  "end": "<phases[].end>",
  "color": "<phases[].color>",
  "text_color": "#FFFFFF"
}
```

### Milestone mapping

```json
{
  "id": "<milestones[].id>",
  "name": "<milestones[].name>",
  "description": "<milestones[].description>",
  "date": "<milestones[].date>",
  "phase": "<matching phase id based on date>",
  "is_critical": "<milestones[].is_critical>",
  "category": "<inferred from milestone name/phase>"
}
```

### Assigning `phase` to milestones

Match each milestone date to the phase whose `start`–`end` range contains it. If a milestone falls on a phase boundary, assign it to the phase it completes or launches.

### Inferring `category`

| Milestone theme | category |
|-----------------|----------|
| Charter, plan, governance | `Governance` |
| Requirements, SRS | `Requirements` |
| Architecture, design, SDD | `Design` |
| Build, development, prototype | `Development` |
| Testing, UAT, QA | `QA` |
| Deploy, go-live, release | `Deployment` |
| Handover, operations | `Transition` |
| Training | `Training` |
| Closure, final report | `Closure` |
| Team, staffing | `Resource` |
| Default | `General` |

---

## JSON Schema

Generate a complete JSON file with this structure:

```json
{
  "milestone_chart": {
    "title": "string - Diagram title",
    "project_name": "string - Full project name",
    "version": "string - Version (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",
    "start_date": "string - Project timeline start (YYYY-MM-DD)",
    "end_date": "string - Project timeline end (YYYY-MM-DD)",
    "description": "string - Optional brief description",

    "phases": [
      {
        "id": "string - Unique phase ID (e.g., P1)",
        "name": "string - Phase name",
        "start": "string - Phase start (YYYY-MM-DD)",
        "end": "string - Phase end (YYYY-MM-DD)",
        "color": "string - Hex color for phase band",
        "text_color": "string - Hex text color (typically #FFFFFF)"
      }
    ],

    "milestones": [
      {
        "id": "string - Unique ID (e.g., M1)",
        "name": "string - Milestone name",
        "description": "string - Optional detailed description",
        "date": "string - Milestone date (YYYY-MM-DD)",
        "phase": "string - Optional phase ID this milestone belongs to",
        "is_critical": "boolean - true for critical path milestones",
        "category": "string - e.g., Governance, Requirements, Design, QA, Deployment, Closure"
      }
    ],

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "timeline_height": 1.0,
      "milestone_size": 0.5,
      "critical_color": "#E53935"
    },

    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5
    }
  }
}
```

---

## Section Guidelines

### Project timeline

- `start_date` must be strictly before `end_date`
- Match `specifications.json → project.start_date` and `project.end_date`
- All phase and milestone dates must fall within this range

### Phases

- **Minimum 1, recommended 3–8**
- Phases should be sequential and cover the project timeline
- Avoid overlapping phase date ranges when possible
- Each phase: `start` ≤ `end`
- Phase dates must be within `start_date`–`end_date`

### Default phase color palette

| Phase type | Hex | text_color |
|------------|-----|------------|
| Initiation / Planning | `#1a237e` | `#FFFFFF` |
| Requirements | `#2E7D32` | `#FFFFFF` |
| Design | `#E65100` | `#FFFFFF` |
| Development | `#6A1B9A` | `#FFFFFF` |
| Testing | `#C62828` | `#FFFFFF` |
| Deployment | `#00838F` | `#FFFFFF` |
| Closure | `#4E342E` | `#FFFFFF` |

### Milestones

- **Minimum 1, recommended 3–15**
- Map directly from `specifications.json → milestones[]`
- Dates must be within project timeline
- Mark `is_critical: true` for:
  - Charter/plan approval
  - Requirements sign-off
  - Design approval
  - Development complete / feature freeze
  - UAT sign-off
  - Go-live / production deployment
  - Project closure
- Include 2–4 non-critical milestones per phase for detail (team assembled, prototype, training complete, etc.)
- Milestone IDs: `M1`, `M2`, … or match spec IDs (`M1`, etc.)

### Typical software project milestones

```text
M1  Charter Approved          (critical, Governance)
M2  Requirements Complete     (critical, Requirements)
M3  Design Complete           (critical, Design)
M4  Development Complete      (critical, Development)
M5  UAT Sign-off              (critical, QA)
M6  Go-Live                   (critical, Deployment)
M7  Project Closure           (critical, Closure)
```

---

## Validation Rules

Fix every failure before writing the file:

1. All required fields populated — `start_date`, `end_date`, `project_name`
2. `start_date` strictly before `end_date`
3. At least **1 phase** and **1 milestone** (recommended)
4. All phase IDs unique; all milestone IDs unique
5. All dates in `YYYY-MM-DD` format
6. Every phase: `start` ≤ `end`
7. Every phase: `start` ≥ project `start_date` and `end` ≤ project `end_date`
8. Every milestone date within project `start_date`–`end_date`
9. `is_critical` is boolean
10. JSON is syntactically valid

Optional validation:

```bash
python milestone_chart_generator/cli.py projects/<project-slug>/inputs/milestone_input.json --validate-only
```

---

## Quick Reference Card

| Section | Minimum | Maximum | Key Rule |
|---------|---------|---------|----------|
| Phases | 1 | 8 | Dates within project timeline |
| Milestones | 1 | 20 | Dates within project timeline |
| Critical milestones | 3 | — | is_critical: true |
| Phase overlap | — | — | Avoid overlapping ranges |

---

## After Generating Input

Run the generator:

```bash
# Render Visio milestone chart
python milestone_chart_generator/cli.py projects/<project-slug>/inputs/milestone_input.json \
  -o projects/<project-slug>/output/milestone_chart.vsdx

# Validate only
python milestone_chart_generator/cli.py projects/<project-slug>/inputs/milestone_input.json --validate-only
```

Reference implementation: [examples/sample_input.json](examples/sample_input.json)

---

## Integration Notes

- Milestones in this file align with [gantt-chart-generator-SKILL.md](../gantt-chart-generator-SKILL.md) milestone markers.
- Phases match `specifications.json → phases[]` used by Gantt and project charter.
- Complements [cpm-network-diagram-generator-SKILL.md](../cpm-network-diagram-generator-SKILL.md) (activity network) with executive-level event timeline.

---

## Copy-Ready Agent Prompt

```
You are a project scheduling specialist. Your task is to generate a complete milestone_input.json file for the Milestone Chart Generator (Visio .vsdx output).

Read the project data from specifications.json or the project description below. Follow the JSON schema in milestone_chart_generator/PROMPT.md exactly. If information is not explicitly provided, derive phases and milestones from the project timeline and list assumptions.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Software Development, Healthcare, Infrastructure]
**Timeline:** [START DATE - END DATE]
**Phases:** [LIST PHASES WITH START/END DATES]
**Key Milestones:** [LIST MILESTONES WITH DATES AND CRITICAL FLAG]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables

1. A complete, valid milestone_input.json following the schema in milestone_chart_generator/PROMPT.md
2. Saved to projects/<project-slug>/inputs/milestone_input.json
3. All validation rules satisfied

## Validation Rules

1. start_date strictly before end_date
2. At least 1 phase and 1 milestone
3. All milestone dates within project start_date–end_date
4. All phase dates within project start_date–end_date
5. Each phase: start ≤ end
6. Mark governance, requirements, design, go-live, and closure milestones as is_critical: true
7. Assign category based on milestone theme
8. Link milestones to phases via phase field when possible

## Response Format

Return the complete milestone_input.json in a single JSON code block AND write it to disk at projects/<project-slug>/inputs/milestone_input.json.

Now, generate the milestone_input.json for the project described above.
```
