# Project Charter Generator — Agent Prompt

Use this file to generate the input JSON required by the **Project Charter Generator**. This generator produces a **Word document** (`.docx` with **native editable DrawingML shape diagrams**) and a **multi-page Visio deck** (`.vsdx`) via **Aspose.Diagram**. You must create **sixteen files**:

- **Four shared data files** (narrative content)
- **Seven diagram description files** (Graphviz or D2 source specs — **required for Word**)
- **Two Word-specific files** (styling + Word MAIN)
- **Two Visio-specific files** (Visio overrides + Visio MAIN)
- **One combined MAIN** (full package)

Any agentic AI working on any project can follow this prompt to produce valid inputs.

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`project_charter` is listed** in `specifications.json → diagrams_to_generate`
3. **Graphviz** (`dot` in PATH) or **D2 CLI** for compiling diagram descriptions to SVG XML
4. **Aspose.Diagram** + JRE for editable `.vsdx` output (see [project-charter-generator-SKILL.md](../project-charter-generator-SKILL.md))
5. Read the SKILL for rendering details after input is ready

## What This Generator Produces

| Output | Format | Input MAIN file |
|--------|--------|-----------------|
| Project charter (Word) | `.docx` | `charter_word_input.json` |
| Embedded diagrams (Word) | **Native DrawingML shapes** (editable boxes/connectors) | `charter_diagram_*_input.json` → layout engine → `word/drawingml_inserter.py` |
| Diagram archive (optional) | SVG XML | Graphviz/D2 → `output/diagrams/svg/` |
| Visio deck | `.vsdx` | `charter_visio_input.json` |
| Both | `.docx` + `.vsdx` | `charter_input.json` |

### Word diagram pipeline (mandatory)

```text
charter_diagram_<name>_input.json   (diagram description JSON)
        │
        ├─ format: "graphviz"  →  .dot source  →  dot -Tsvg  →  .svg (archive)
        └─ format: "d2"        →  .d2 source  →  d2 compile →  .svg (archive)
        │
        ▼
diagrams/layouts.py  →  layout dict {nodes, edges, title}
        │
        ▼
word/drawingml_inserter.py  →  native wps:wsp / wpg:wgp shapes in .docx
                              (click-to-edit rectangles, text, connectors — NOT images)
```

Word diagrams are **native DrawingML shapes**, not SVG or PNG images. SVG files are written to `output/diagrams/svg/` for reference. PNG is used only as a fallback if layout data is unavailable.

| Word section | Shared data file |
|--------------|------------------|
| §1 Executive Summary, §2 Overview | `charter_project_input.json` |
| §3 Vision & Objectives, §12 Success Criteria | `charter_content_input.json` |
| §4 Scope | `charter_content_input.json → scope` |
| §5 Stakeholders, §7 Organization | `charter_people_input.json` |
| §8 Constraints & Assumptions, §11 Budget, §13 Approvals | `charter_content_input.json` |
| §9 Risks, §10 Milestones | `charter_schedule_risk_input.json` |

| Visio page | Shared / Visio data |
|------------|---------------------|
| Problem tree | `charter_diagram_problem_tree_input.json` + Aspose layout |
| Stakeholder matrix | `charter_diagram_stakeholder_matrix_input.json` |
| System context | `charter_diagram_system_context_input.json` |
| Org chart | `charter_diagram_org_chart_input.json` |
| Scope boundary | `charter_diagram_scope_boundary_input.json` |
| Milestone timeline | `charter_diagram_milestone_timeline_input.json` |
| Risk matrix | `charter_diagram_risk_matrix_input.json` |

---

## Output File Locations — READ THIS FIRST

All files live under `projects/<project-slug>/inputs/`:

### Shared data (used by Word, Visio, and combined MAIN)

| File | Purpose |
|------|---------|
| `charter_project_input.json` | Project header — name, sponsor, manager, dates, department, version |
| `charter_content_input.json` | Vision, objectives, scope, constraints, assumptions, success criteria, budget, approvals |
| `charter_people_input.json` | Stakeholder register + project team (org chart) |
| `charter_schedule_risk_input.json` | Risks + milestones |

### Word bundle — diagram descriptions (required)

| File | Diagram | Word section |
|------|---------|--------------|
| `charter_diagram_problem_tree_input.json` | Problem tree | §9.2 |
| `charter_diagram_stakeholder_matrix_input.json` | Power-interest matrix | §5.2 |
| `charter_diagram_scope_boundary_input.json` | Scope boundary | §4.4 |
| `charter_diagram_org_chart_input.json` | Org chart | §7.2 |
| `charter_diagram_milestone_timeline_input.json` | Milestone timeline | §10.2 |
| `charter_diagram_risk_matrix_input.json` | Risk matrix | §9.3 |
| `charter_diagram_system_context_input.json` | System context | §6.2 |
| `charter_word_styling_input.json` | Word presentation | — |
| **`charter_word_input.json`** | **Word MAIN** | — |

### Visio bundle

| File | Purpose |
|------|---------|
| `charter_visio_diagrams_input.json` | Per-diagram overrides in `diagrams{}` + Visio deck options |
| **`charter_visio_input.json`** | **Visio MAIN** — merge for Visio-focused runs |

### Combined

| File | Purpose |
|------|---------|
| **`charter_input.json`** | **Full MAIN** — merge for Word + Visio together |

Example paths (Da'atSNA):

```text
projects/daatsna-community-data-platform/inputs/
├── charter_project_input.json              ← shared header
├── charter_content_input.json              ← shared narrative
├── charter_people_input.json               ← shared people
├── charter_schedule_risk_input.json        ← shared risks + milestones
├── charter_diagram_problem_tree_input.json       ← Word diagram (Graphviz/D2)
├── charter_diagram_stakeholder_matrix_input.json
├── charter_diagram_scope_boundary_input.json
├── charter_diagram_org_chart_input.json
├── charter_diagram_milestone_timeline_input.json
├── charter_diagram_risk_matrix_input.json
├── charter_diagram_system_context_input.json
├── charter_word_styling_input.json         ← Word only
├── charter_word_input.json                 ← Word MAIN
├── charter_visio_diagrams_input.json       ← Visio only
├── charter_visio_input.json                ← Visio MAIN
└── charter_input.json                      ← Combined MAIN
```

### How the sixteen files relate

```text
specifications.json
        │
        ├─► STEP 1–4   shared narrative split files
        ├─► STEP 5–11  charter_diagram_*_input.json  (7 diagram descriptions)
        ├─► STEP 12    charter_word_styling_input.json
        └─► STEP 13    charter_visio_diagrams_input.json
        │
        ├─► MERGE → charter_word_input.json    (includes diagram_descriptions{})
        ├─► MERGE → charter_visio_input.json
        └─► MERGE → charter_input.json
        │
        ▼
   cli.py build → Word (.docx + DrawingML shapes) + Visio (.vsdx via Aspose)
```

**Shared data rule:** `project`, `vision`, `objectives`, `scope`, `stakeholders`, `team`, `risks`, `milestones`, `budget`, and related arrays must be **identical** across `charter_word_input.json`, `charter_visio_input.json`, and `charter_input.json`. Author once in the split files, then copy into each merge.

---

## Merge rules

All MAIN files use the flat `CharterSpec` top-level structure (no wrapper key).

### Word MAIN — `charter_word_input.json`

```json
{
  "project": { /* charter_project_input.json */ },
  "vision": { /* charter_content_input.json */ },
  "objectives": [ /* charter_content_input.json */ ],
  "scope": { /* charter_content_input.json */ },
  "stakeholders": [ /* charter_people_input.json */ ],
  "team": [ /* charter_people_input.json */ ],
  "constraints": [ /* charter_content_input.json */ ],
  "assumptions": [ /* charter_content_input.json */ ],
  "risks": [ /* charter_schedule_risk_input.json */ ],
  "milestones": [ /* charter_schedule_risk_input.json */ ],
  "budget": { /* charter_content_input.json */ },
  "success_criteria": [ /* charter_content_input.json */ ],
  "approvals": [ /* charter_content_input.json */ ],
  "diagrams": {
    "problem_tree": {},
    "stakeholder_map": {},
    "system_context": {},
    "org_chart": {},
    "scope_boundary": {},
    "milestone_timeline": {}
  },
  "word_document": { /* charter_word_styling_input.json → word_document (optional) */ },
  "diagram_descriptions": {
    "problem_tree": { /* charter_diagram_problem_tree_input.json → diagram_description */ },
    "stakeholder_matrix": { /* ... */ },
    "scope_boundary": { /* ... */ },
    "org_chart": { /* ... */ },
    "milestone_timeline": { /* ... */ },
    "risk_matrix": { /* ... */ },
    "system_context": { /* ... */ }
  }
}
```

Word builder compiles each `diagram_descriptions` entry through the layout engine → **native DrawingML shapes** embedded in the document. SVG archive written when Graphviz/D2 is available.

### Visio MAIN — `charter_visio_input.json`

```json
{
  "project": { /* same as Word MAIN */ },
  "vision": { /* ... */ },
  "objectives": [ /* ... */ ],
  "scope": { /* ... */ },
  "stakeholders": [ /* ... */ ],
  "team": [ /* ... */ ],
  "constraints": [ /* ... */ ],
  "assumptions": [ /* ... */ ],
  "risks": [ /* ... */ ],
  "milestones": [ /* ... */ ],
  "budget": { /* ... */ },
  "success_criteria": [ /* ... */ ],
  "approvals": [ /* ... */ ],
  "diagrams": { /* charter_visio_diagrams_input.json → diagrams */ },
  "visio_deck": { /* charter_visio_diagrams_input.json → visio_deck (optional) */ }
}
```

Visio builder reads `diagrams{}` overrides when non-empty; otherwise auto-derives layouts from shared data (see Diagram auto-generation). Omit `word_document` from the Visio MAIN.

### Combined MAIN — `charter_input.json`

Superset merge: all shared sections + `diagrams{}` + optional `word_document` + optional `visio_deck`.

```bash
python -c "
from project_charter_generator.core.charter_builder import build_charter
import json
build_charter(json.load(open('projects/<slug>/inputs/charter_input.json')),
              'projects/<slug>/output')
"
```

---

## Diagram description JSON schema (required — one file per diagram)

Each `charter_diagram_<name>_input.json` wraps a single `diagram_description` object. The agent **must author all seven files**. Set `"format": "graphviz"` (default) or `"d2"`. Provide either structured `nodes`/`edges` **or** raw `source` text.

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
      {
        "id": "TRUNK",
        "label": "Core problem statement",
        "shape": "box",
        "fill": "#FFCC80",
        "border": "#F57C00",
        "text_color": "#E65100"
      }
    ],
    "edges": [
      { "from": "RSK-01", "to": "TRUNK", "label": "", "color": "#666666" }
    ],
    "source": null
  }
}
```

### Raw source override (Graphviz or D2)

When `source` is non-null, the compiler uses it directly:

```json
{
  "diagram_description": {
    "id": "scope_boundary",
    "title": "Scope Boundary",
    "format": "graphviz",
    "source": "digraph scope { rankdir=LR; ... }"
  }
}
```

```json
{
  "diagram_description": {
    "id": "system_context",
    "title": "System Context",
    "format": "d2",
    "source": "direction: right\nsystem: Da'atSNA Platform\nclinics -> system: FHIR"
  }
}
```

### Required diagram files

| File | `diagram_description.id` |
|------|--------------------------|
| `charter_diagram_problem_tree_input.json` | `problem_tree` |
| `charter_diagram_stakeholder_matrix_input.json` | `stakeholder_matrix` |
| `charter_diagram_scope_boundary_input.json` | `scope_boundary` |
| `charter_diagram_org_chart_input.json` | `org_chart` |
| `charter_diagram_milestone_timeline_input.json` | `milestone_timeline` |
| `charter_diagram_risk_matrix_input.json` | `risk_matrix` |
| `charter_diagram_system_context_input.json` | `system_context` |

Derive nodes/edges from shared narrative files. IDs in diagram descriptions must match stakeholder, risk, milestone, and team IDs in shared data.

---

## Agent Instructions

You are a project management documentation specialist. Your task is to generate **sixteen JSON files** (thirteen split + three merged MAIN).

### Your workflow

1. Read `projects/<project-slug>/specifications.json` as the primary source.
2. **Create shared files** (steps 1–4): project → content → people → schedule/risk.
3. **Create all seven `charter_diagram_*_input.json` files** — Graphviz or D2 diagram descriptions for Word.
4. **Create `charter_word_styling_input.json`** — Word presentation config.
5. **Create `charter_visio_diagrams_input.json`** — Visio deck overrides (optional).
6. **Run merge** → `charter_word_input.json`, `charter_visio_input.json`, `charter_input.json`.
7. Validate cross-file consistency (narrative + diagram node IDs).
8. Write all thirteen split files and three MAIN files; confirm paths.

```bash
python project_charter_generator/cli.py merge projects/<slug>/inputs --validate
python project_charter_generator/cli.py build projects/<slug>/inputs/charter_input.json -o projects/<slug>/output
```

If `specifications.json` is missing, run [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md) first, or gather charter fields from the user and list assumptions.

### Critical rules

- **Sixteen files on disk** — thirteen split files plus three merged MAIN files.
- **Seven diagram description files required** — Word will not build without `diagram_descriptions`.
- **Graphviz or D2** — compiles diagram descriptions to SVG archive; Word uses layout → DrawingML shapes.
- **Shared data stays in sync** — narrative sections identical across all three MAIN files.

---

## Mapping from specifications.json

The charter input is a **superset** of `specifications.json` with additional governance sections.

| specifications.json | Target file | Transform |
|---------------------|-------------|-----------|
| `project.*` | `charter_project_input.json` | Direct map (add `department` if missing) |
| `vision.*` | `charter_content_input.json` | Direct map |
| `objectives[]` | `charter_content_input.json` | Direct map |
| `stakeholders[]` | `charter_people_input.json` | Map `role`; collapse `power`/`interest` Medium → High or Low |
| `risks[]` | `charter_schedule_risk_input.json` | `name` → `description`; `probability` → `likelihood`; drop `score` |
| `milestones[]` | `charter_schedule_risk_input.json` | Add `deliverable` from `description` |
| `budget` | `charter_content_input.json` | Flatten `categories[]` → `breakdown{}` |
| — | `charter_content_input.json → scope` | **Add** — derive from WBS and project description |
| — | `charter_content_input.json → constraints` | **Add** — from risks, budget limits, timeline |
| — | `charter_content_input.json → assumptions` | **Add** — infer 3–5 project assumptions |
| — | `charter_content_input.json → success_criteria` | **Add** — from objectives' measurable criteria |
| — | `charter_content_input.json → approvals` | **Add** — sponsor, manager sign-off |
| — | `charter_people_input.json → team` | **Add** — org structure for org chart |
| — | `charter_visio_diagrams_input.json` | **Add** — optional diagram overrides |

### Stakeholder power/interest collapse

Charter model accepts only `High` or `Low`:

| specifications value | charter value |
|---------------------|---------------|
| High | High |
| Medium | High (if power) or Low (if interest) — use judgment |
| Low | Low |

### Risk field mapping

```json
{
  "id": "R-001",
  "description": "<risks[].name>: <risks[].description>",
  "likelihood": "<risks[].probability>",
  "impact": "<risks[].impact>",
  "mitigation": "<risks[].mitigation>"
}
```

### Budget mapping

From `specifications.json → budget.categories[]`:

```json
{
  "total": 59400,
  "currency": "USD",
  "breakdown": {
    "personnel": 31000,
    "hardware": 18500,
    "software": 1500,
    "training": 3000,
    "contingency": 5400
  }
}
```

Map category names to breakdown keys; sum must equal `total`.

---

## Shared file schemas

### `charter_project_input.json`

```json
{
  "project": {
    "name": "string - Full project name",
    "sponsor": "string - Project sponsor name and title",
    "manager": "string - Project manager name",
    "start_date": "string - YYYY-MM-DD",
    "end_date": "string - YYYY-MM-DD",
    "department": "string - Department/Division",
    "version": "string - e.g., 1.0"
  }
}
```

### `charter_content_input.json`

```json
{
  "vision": {
    "statement": "string - Vision statement",
    "mission": "string - Mission statement"
  },
  "objectives": [
    {
      "id": "OBJ-01",
      "description": "string",
      "measurable_criteria": "string"
    }
  ],
  "scope": {
    "in_scope": ["string"],
    "out_of_scope": ["string"],
    "boundaries": "string"
  },
  "constraints": ["string"],
  "assumptions": ["string"],
  "success_criteria": ["string"],
  "budget": {
    "total": 59400,
    "currency": "USD",
    "breakdown": {
      "personnel": 31000,
      "hardware": 18500,
      "software": 1500,
      "training": 3000,
      "contingency": 5400
    }
  },
  "approvals": [
    { "role": "Sponsor", "name": "Jane Doe", "date": "YYYY-MM-DD" }
  ]
}
```

### `charter_people_input.json`

```json
{
  "stakeholders": [
    {
      "id": "SH-01",
      "name": "string",
      "role": "string",
      "organization": "string",
      "power": "High",
      "interest": "High",
      "expectations": "string"
    }
  ],
  "team": [
    {
      "id": "SPONSOR",
      "name": "string",
      "role": "Project Sponsor",
      "reports_to": null
    },
    {
      "id": "PM",
      "name": "string",
      "role": "Project Manager",
      "reports_to": "SPONSOR"
    }
  ]
}
```

If `team[]` is empty, the generator synthesizes sponsor + manager from `charter_project_input.json`.

### `charter_schedule_risk_input.json`

```json
{
  "risks": [
    {
      "id": "RSK-01",
      "description": "string",
      "likelihood": 3,
      "impact": 5,
      "mitigation": "string"
    }
  ],
  "milestones": [
    {
      "id": "M1",
      "name": "string",
      "date": "YYYY-MM-DD",
      "deliverable": "string",
      "is_critical": false
    }
  ]
}
```

---

## Word file schemas

### `charter_word_styling_input.json`

Optional presentation config. Not enforced by current validator; consumed by future Word builder options.

```json
{
  "word_document": {
    "template": "word_template.docx",
    "figure_width_inches": 6.0,
    "include_toc": true,
    "include_appendices": true,
    "body_font": "Calibri",
    "body_size_pt": 11,
    "sections": {
      "system_context": true,
      "budget_chart": true
    }
  }
}
```

### `charter_word_input.json` (Word MAIN)

Merge all shared sections + empty `diagrams{}` + optional `word_document`. Pass to `build_charter` when regenerating Word output only (future `--word-only` flag).

---

## Visio file schemas

### `charter_visio_diagrams_input.json`

Embed contents from sibling generator inputs when available. Leave `{}` to auto-derive from shared data.

```json
{
  "diagrams": {
    "problem_tree": { /* problem_tree_input.json → problem_tree, or {} */ },
    "stakeholder_map": { /* stakeholder_input.json, or {} */ },
    "system_context": { /* system_context input, or {} */ },
    "org_chart": {},
    "scope_boundary": {},
    "milestone_timeline": { /* milestone_input.json, or {} */ }
  },
  "visio_deck": {
    "page_size": "A3",
    "orientation": "landscape",
    "include_risk_matrix": true,
    "theme": "corporate_blue"
  }
}
```

### Diagram auto-generation

When `diagrams{}` blocks are empty, layouts derive from shared data:

| Diagram | Auto-derived from |
|---------|-------------------|
| Problem tree | `risks[]` → roots; `objectives[]` → branches; `success_criteria[]` → leaf; `vision.statement` → trunk fallback |
| Stakeholder matrix | `stakeholders[]` |
| Milestone timeline | `milestones[]` |
| Scope boundary | `scope.in_scope[]`, `scope.out_of_scope[]` |
| Org chart | `team[]` or `project.sponsor` + `project.manager` |
| Risk matrix | `risks[]` |

For production-quality diagrams, embed dedicated inputs:

| Override key | Source PROMPT |
|--------------|---------------|
| `diagrams.problem_tree` | [problem_tree_generator/PROMPT.md](../problem_tree_generator/PROMPT.md) |
| `diagrams.stakeholder_map` | [stakeholder_diagram_generator/PROMPT.md](../stakeholder_diagram_generator/PROMPT.md) |
| `diagrams.system_context` | [system_context_generator/PROMPT.md](../system_context_generator/PROMPT.md) |
| `diagrams.milestone_timeline` | [milestone_chart_generator/PROMPT.md](../milestone_chart_generator/PROMPT.md) |

### `charter_visio_input.json` (Visio MAIN)

Merge all shared sections + `diagrams{}` + optional `visio_deck`. Omit `word_document`.

---

## Combined MAIN — `charter_input.json`

Full merge of all sections. Use for generating **both** Word and Visio in one run.

---

## Section Guidelines

### Required fields (validator enforced)

- `project.name` — non-empty
- `vision.statement` — non-empty

### Recommended minimums

| Section | File | Minimum |
|---------|------|---------|
| Objectives | `charter_content_input.json` | 3 |
| Stakeholders | `charter_people_input.json` | 5 |
| Risks | `charter_schedule_risk_input.json` | 3 |
| Milestones | `charter_schedule_risk_input.json` | 3 |
| Scope in_scope | `charter_content_input.json` | 3 |
| Scope out_of_scope | `charter_content_input.json` | 2 |
| Constraints | `charter_content_input.json` | 2 |
| Assumptions | `charter_content_input.json` | 3 |
| Success criteria | `charter_content_input.json` | 3 |
| Approvals | `charter_content_input.json` | 2 |
| Team | `charter_people_input.json` | 2 |

### Word document sections produced

1. Executive Summary
2. Project Overview
3. Vision & Objectives
4. Scope (+ scope boundary diagram)
5. Stakeholders (+ power-interest matrix)
6. System Context (+ context diagram if provided)
7. Project Organization (+ org chart)
8. Constraints & Assumptions
9. Risks (+ problem tree diagram)
10. Milestones (+ timeline diagram)
11. Budget
12. Success Criteria
13. Approvals

---

## Validation Rules

### Cross-file consistency

1. Shared sections identical across `charter_word_input.json`, `charter_visio_input.json`, and `charter_input.json`
2. `charter_word_input.json` includes `word_document` (optional); `charter_visio_input.json` includes populated `diagrams{}` and optional `visio_deck`
3. `charter_input.json` is the superset (shared + `diagrams{}` + `word_document` + `visio_deck`)
4. Stakeholder IDs in `diagrams.stakeholder_map` match `charter_people_input.json`
5. Milestone IDs in `diagrams.milestone_timeline` match `charter_schedule_risk_input.json`

### Per-section rules

6. `project.name` and `vision.statement` populated
7. All dates in `YYYY-MM-DD` format
8. Unique IDs within objectives, stakeholders, risks, milestones
9. Stakeholder `power` and `interest`: `High` or `Low` only
10. Risk `likelihood` and `impact`: integers 1–5
11. Budget `breakdown` sums to `total` (± rounding)
12. Milestone dates within `project.start_date`–`project.end_date`
13. Team `reports_to` references existing team member IDs or `null`
14. JSON syntactically valid

Optional validation:

```bash
python -c "
from project_charter_generator.core.validator import validate_payload
import json
validate_payload(json.load(open('projects/<slug>/inputs/charter_input.json')))
print('OK')
"
```

---

## Quick Reference Card

| File | Bundle | Used by |
|------|--------|---------|
| `charter_project_input.json` | Shared | All merges |
| `charter_content_input.json` | Shared | All merges |
| `charter_people_input.json` | Shared | All merges |
| `charter_schedule_risk_input.json` | Shared | All merges |
| `charter_word_styling_input.json` | Word | Word + combined MAIN |
| `charter_word_input.json` | **Word MAIN** | Word `.docx` |
| `charter_visio_diagrams_input.json` | Visio | Visio + combined MAIN |
| `charter_visio_input.json` | **Visio MAIN** | Visio `.vsdx` |
| `charter_input.json` | **Combined MAIN** | Full package |

---

## After Generating Input

Run the charter builder with the appropriate MAIN file:

```python
from project_charter_generator.core.charter_builder import build_charter
import json

# Full package (Word + Visio) — use combined MAIN
with open("projects/<project-slug>/inputs/charter_input.json") as f:
    build_charter(json.load(f), "projects/<project-slug>/output")

# Word-focused edit — re-merge charter_word_input.json, then use combined MAIN
# (current build_charter always produces both outputs; --word-only / --visio-only planned)
```

Expected output:

```text
projects/<project-slug>/output/
├── project-charter.docx
├── diagrams/
│   ├── source/          ← .dot or .d2 compiled from diagram descriptions
│   │   ├── problem_tree.dot
│   │   └── ...
│   └── svg/             ← SVG archive (reference; Word uses DrawingML shapes)
│       ├── problem_tree.svg
│       └── ...
└── visio/
    └── project-charter.vsdx   ← Aspose.Diagram multi-page deck
```

When editing: update the relevant split file(s), re-merge the affected MAIN file(s), then re-run the builder.

---

## Assembly Workflow (recommended)

When per-diagram inputs already exist:

```text
1. specifications.json              → shared split files (steps 1–4)
2. problem_tree_input.json          → charter_visio_diagrams_input.json → diagrams.problem_tree
3. stakeholder_input.json           → charter_people_input.json + diagrams.stakeholder_map
4. system_context input             → diagrams.system_context
5. milestone_input.json             → charter_schedule_risk_input.json + diagrams.milestone_timeline
6. charter_word_styling_input.json  → Word bundle
7. Merge → charter_word_input.json, charter_visio_input.json, charter_input.json
```

---

## Integration Notes

- **Orchestrator skill** — runs after individual diagram inputs are ready, or standalone from `specifications.json` alone.
- Shares data with every generator PROMPT in `projects/<project-slug>/inputs/`.
- Problem tree in charter auto-maps risks → roots; for a proper causal tree use [problem_tree_generator/PROMPT.md](../problem_tree_generator/PROMPT.md) and embed via `charter_visio_diagrams_input.json`.
- [project_charter_generator/PROMPT.md](PROMPT.md) budget section aligns with [budget_breakdown_generator/PROMPT.md](../budget_breakdown_generator/PROMPT.md).

---

## Copy-Ready Agent Prompt

```
You are a project management documentation specialist. Your task is to generate SIXTEEN JSON files for the Project Charter Generator (Word .docx with native DrawingML shape diagrams + Aspose Visio .vsdx).

Read specifications.json or the project description below. Follow project_charter_generator/PROMPT.md exactly.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Software Development, Healthcare]
**Sponsor / Manager:** [NAMES AND ROLES]
**Timeline:** [START DATE - END DATE]
**Vision / Mission:** [STATEMENTS]
**Scope:** [IN-SCOPE AND OUT-OF-SCOPE ITEMS]
**Team Structure:** [ORG CHART ROLES]

## Source File (required)

Path: projects/<project-slug>/specifications.json

## Deliverables — YOU MUST CREATE ALL SIXTEEN FILES

### Shared data (author first)
1. charter_project_input.json
2. charter_content_input.json
3. charter_people_input.json
4. charter_schedule_risk_input.json

### Diagram descriptions (required for Word — Graphviz or D2)
5. charter_diagram_problem_tree_input.json
6. charter_diagram_stakeholder_matrix_input.json
7. charter_diagram_scope_boundary_input.json
8. charter_diagram_org_chart_input.json
9. charter_diagram_milestone_timeline_input.json
10. charter_diagram_risk_matrix_input.json
11. charter_diagram_system_context_input.json

### Word + Visio bundles
12. charter_word_styling_input.json
13. charter_visio_diagrams_input.json

### MAIN merges (via cli.py merge)
14. charter_word_input.json
15. charter_visio_input.json
16. charter_input.json

## Workflow

1. Map specifications.json to shared split files 1–4
2. Author all seven diagram description files (Graphviz nodes/edges or raw DOT/D2 source)
3. Write Word styling (12) and Visio overrides (13)
4. Merge all splits into MAIN files 14–16 (must include diagram_descriptions{})
5. Verify narrative and diagram IDs reconcile

## Validation Rules

1. Sixteen files on disk — seven diagram description files are mandatory
2. Each diagram_description uses format graphviz or d2 — never png
3. project.name and vision.statement non-empty
4. Shared narrative identical across all three MAIN files
5. Diagram node IDs reference valid stakeholder/risk/milestone/team IDs

## Response Format

Confirm all sixteen file paths. Report diagram format (graphviz/d2) per diagram file.

Return charter_input.json (combined MAIN) in a final JSON code block.

Now, generate all sixteen project charter input JSON files.
```
