---
name: prompt-skill-generator
description: Generate a complete specifications.json and project folder structure for any project so downstream UML-SKILLS diagram generators can run. Use when starting a new project, when the user asks for specifications.json, project specs for diagrams, stakeholder maps, Gantt charts, risk matrices, WBS, or any prompt that needs structured input for the diagram generation skills in this repository — even if they never say "specifications" explicitly, e.g. "set up my project for diagram generation" or "create the input files for a project charter."
---

# Prompt & Specifications Generator

A meta-skill that turns **any project description** — from a user prompt, README, charter draft, or codebase — into a validated `specifications.json` file and the folder layout required by every diagram generator in this repository.

This skill is the **mandatory first step** before invoking any downstream generator skill (`stakeholder-diagram-generator`, `gantt-chart-generator`, `risk-matrix-diagram-generator`, etc.). Do not call those skills until `specifications.json` exists and passes validation.

## Table of Contents

1. Core Workflow
2. When to Use This Skill
3. Project Intake (Any Project, Any Context)
4. Output Directory Structure
5. specifications.json Schema
6. Section Guidelines
7. Validation Rules
8. Diagram-to-Skill Mapping
9. Downstream File Generation
10. Quick Reference Card
11. Worked Example (Da'atSNA)
12. Agent Response Format

---

## 1. Core Workflow

Follow this sequence every time:

```
Gather project info → Draft specifications.json → Validate → Write files → (Optional) Split per-skill inputs
```

1. **Gather project information** using the intake checklist in Section 3. Read the user's prompt, project README, existing docs, or codebase. Infer missing fields; document assumptions in a brief comment block at the top of your response (not inside the JSON).
2. **Draft `specifications.json`** following the schema in Section 5 and guidelines in Section 6.
3. **Validate** against every rule in Section 7 before writing any file.
4. **Write the file** to `projects/<project-slug>/specifications.json` (see Section 4).
5. **Optionally split** into per-skill input JSON files if the user wants to run individual generators immediately (Section 9).
6. **Present** the file path, a summary of what was inferred, and which downstream skills can now run.

---

## 2. When to Use This Skill

Use this skill when:

- The user asks to generate `specifications.json` or "project specifications"
- A new project needs diagram inputs (stakeholder register, Gantt, risk matrix, WBS, etc.)
- Another skill in this repo needs structured JSON but none exists yet
- The user describes a project and wants "all the diagrams" or a project charter
- You are working in an unfamiliar repo and need to bootstrap diagram inputs from available context

Do **not** skip this skill and hand-craft per-diagram JSON files separately — one `specifications.json` is the single source of truth.

---

## 3. Project Intake (Any Project, Any Context)

Collect as much as possible from the user. When fields are missing, infer from project type and context.

### Required intake fields

| Field | Source | Fallback if missing |
|-------|--------|---------------------|
| Project Name | User prompt / README / package name | Derive from repo or folder name |
| Project Type | User prompt | Infer (Software, Healthcare, Social Enterprise, Infrastructure, etc.) |
| Project Description | User prompt / README | 1–2 sentences from repo purpose |
| Key Stakeholders | User prompt / org chart / CODEOWNERS | Infer 5–8 realistic roles for the domain |
| Key Objectives | User prompt / README goals / issues | Derive 3–5 SMART objectives from scope |
| Timeline | User prompt / milestones in docs | Default 12-month window from today's date |
| Budget | User prompt / grant docs | Estimate from scope and team size |

### Intake prompt template

When the user has not provided enough detail, ask using this template (fill what you already know):

```markdown
## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Software Development, Healthcare, Social Enterprise]
**Project Description:** [INSERT PROJECT DESCRIPTION]
**Key Stakeholders:** [LIST STAKEHOLDERS OR DESCRIBE]
**Key Objectives:** [LIST OBJECTIVES]
**Timeline:** [START DATE - END DATE]
**Budget:** [TOTAL BUDGET AND CURRENCY]
```

If the user prefers not to answer, proceed with reasonable inferences and list every assumption in your response.

### Project slug rules

Derive `<project-slug>` from the project name:

- Lowercase
- Replace spaces and apostrophes with hyphens
- Remove special characters
- Example: `Da'atSNA Community Data Platform` → `daatsna-community-data-platform`

---

## 4. Output Directory Structure

Create this layout under the repository root (or the user's specified projects root):

```text
projects/
└── <project-slug>/
    ├── specifications.json          ← REQUIRED (this skill's primary output)
    ├── assumptions.md               ← OPTIONAL (list inferred values)
    └── inputs/                      ← OPTIONAL (per-skill split files)
        ├── stakeholder_input.json
        ├── gantt_input.json
        ├── risk_matrix_input.json
        ├── wbs_input.json
        ├── budget_input.json
        ├── milestone_input.json
        └── ...
```

**Primary deliverable:** `projects/<project-slug>/specifications.json`

---

## 5. specifications.json Schema

Generate a complete JSON file with this exact top-level structure. Replace every placeholder with real project data.

```json
{
  "project": {
    "name": "string - Full project name",
    "description": "string - Brief project description",
    "version": "string - Version number (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",
    "department": "string - Department/Division",
    "sponsor": "string - Project sponsor name",
    "manager": "string - Project manager name",
    "start_date": "string - Start date (YYYY-MM-DD)",
    "end_date": "string - End date (YYYY-MM-DD)"
  },

  "vision": {
    "statement": "string - Vision statement (one line)",
    "mission": "string - Mission statement (one line)"
  },

  "objectives": [
    {
      "id": "string - Unique ID (e.g., OBJ-01)",
      "description": "string - Objective description",
      "measurable_criteria": "string - How to measure success"
    }
  ],

  "stakeholders": [
    {
      "id": "string - Unique ID (e.g., S-001)",
      "name": "string - Full name",
      "role": "string - Job title or role",
      "organization": "string - Organization/Department",
      "category": "string - Internal or External",
      "power": "string - High, Medium, or Low",
      "interest": "string - High, Medium, or Low",
      "influence": "string - High, Medium, or Low",
      "legitimacy": "string - High, Medium, or Low",
      "urgency": "string - High, Medium, or Low",
      "expectations": "string - What they expect from the project",
      "engagement_strategy": "string - Manage Closely, Keep Satisfied, Keep Informed, or Monitor",
      "contact": "string - Email or contact info (optional)"
    }
  ],

  "risks": [
    {
      "id": "string - Unique ID (e.g., R-001)",
      "name": "string - Risk name",
      "description": "string - Detailed description",
      "probability": "number - 1 to 5 (1=Rare, 5=Almost Certain)",
      "impact": "number - 1 to 5 (1=Minor, 5=Catastrophic)",
      "score": "number - Probability x Impact (calculated)",
      "mitigation": "string - Mitigation strategy",
      "owner": "string - Risk owner (optional)"
    }
  ],

  "milestones": [
    {
      "id": "string - Unique ID (e.g., M1)",
      "name": "string - Milestone name",
      "date": "string - Date (YYYY-MM-DD)",
      "description": "string - Brief description",
      "is_critical": "boolean - true or false"
    }
  ],

  "budget": {
    "total": "number - Total budget amount",
    "currency": "string - Currency code (e.g., USD, UGX, EUR)",
    "categories": [
      {
        "id": "string - Unique ID (e.g., PERSONNEL)",
        "name": "string - Category name",
        "total": "number - Category total",
        "items": [
          {
            "name": "string - Item name",
            "qty": "number - Quantity",
            "unit_cost": "number - Cost per unit",
            "total": "number - Total (qty x unit_cost)"
          }
        ]
      }
    ]
  },

  "phases": [
    {
      "id": "string - Unique ID (e.g., P1)",
      "name": "string - Phase name",
      "start": "string - Start date (YYYY-MM-DD)",
      "end": "string - End date (YYYY-MM-DD)",
      "color": "string - Hex color code (e.g., #1a237e)"
    }
  ],

  "wbs": {
    "level_0": {
      "id": "string - Always '0'",
      "name": "string - Project name"
    },
    "branches": [
      {
        "id": "string - Level 1 ID (e.g., 1, 2, 3)",
        "name": "string - Phase/Deliverable name",
        "level": "number - Always 1",
        "children": [
          {
            "id": "string - Level 2 ID (e.g., 1.1, 1.2)",
            "name": "string - Work package name",
            "level": "number - Always 2"
          }
        ]
      }
    ]
  },

  "diagrams_to_generate": [
    "string - List of diagram types to generate"
  ],

  "output_formats": ["vsdx", "png", "svg", "xlsx"]
}
```

### Allowed values for `diagrams_to_generate`

| Key | Downstream skill file |
|-----|----------------------|
| `stakeholder_register` | `stakeholder-diagram-generator-SKILL.md` |
| `power_interest_matrix` | `stakeholder-diagram-generator-SKILL.md` |
| `influence_network` | `stakeholder-diagram-generator-SKILL.md` |
| `salience_model` | `stakeholder-diagram-generator-SKILL.md` |
| `stakeholder_map` | `stakeholder-diagram-generator-SKILL.md` |
| `risk_matrix` | `risk-matrix-diagram-generator-SKILL.md` |
| `milestone_chart` | `milestone-chart-generator-SKILL.md` |
| `wbs_diagram` | `wbs-diagram-generator-SKILL.md` |
| `budget_breakdown` | `budget-breakdown-generator-SKILL.md` |
| `gantt_chart` | `gantt-chart-generator-SKILL.md` |
| `pert_chart` | `pert-chart-generator-SKILL.md` |
| `cpm_network` | `cpm-network-diagram-generator-SKILL.md` |
| `kanban_chart` | `kanban-chart-generator-SKILL.md` |
| `system_context` | `system-context-diagram-generator-SKILL.md` |
| `communication_diagram` | `communication_diagram_generator/SKILL.md` |
| `problem_tree` | `problem-tree-generator-SKILL.md` |
| `raci_matrix` | `raci-matrix-diagram-generator-SKILL.md` |
| `resource_allocation_matrix` | `resource-allocation-matrix-generator-SKILL.md` |
| `project_charter` | `project-charter-generator-SKILL.md` |
| `uml_diagram` | `uml-diagram-generator-SKILL.md` |

When in doubt, include all diagrams relevant to the project type. Software projects typically need: `stakeholder_register`, `power_interest_matrix`, `risk_matrix`, `gantt_chart`, `wbs_diagram`, `budget_breakdown`, `milestone_chart`, `system_context`.

---

## 6. Section Guidelines

### 1. Project

- **name**: Full, official project name
- **description**: 1–2 sentences explaining what the project does
- **start_date / end_date**: Realistic timeline based on project scope
- **sponsor / manager**: Actual names if known; otherwise infer appropriate roles
- **date**: Use today's date in `YYYY-MM-DD` format

### 2. Vision

- **statement**: One sentence, aspirational
- **mission**: One sentence, actionable

### 3. Objectives

- **Minimum 3, maximum 8**
- Must be SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
- Each objective must have clear measurable criteria

### 4. Stakeholders

- **Minimum 5, maximum 15**
- Mix of Internal and External
- Cover categories where relevant: Executive, Management, Technical, Clinical, Regulatory, Financial, Community
- Power / Interest / Influence / Legitimacy / Urgency: `High`, `Medium`, or `Low` only
- Engagement strategy must match Power–Interest mapping (see Section 7)

### 5. Risks

- **Minimum 3, maximum 10**
- Probability and Impact: integers 1–5 (1 = lowest, 5 = highest)
- **score** = probability × impact (must be calculated, not guessed)
- Include mitigation strategy for each

### 6. Milestones

- **Minimum 3, maximum 15**
- Mix of critical (`is_critical: true`) and non-critical
- Dates must fall within project timeline

### 7. Budget

- Realistic total for project scope
- **Minimum 3 categories, maximum 8** (e.g., Personnel, Equipment, Software, Travel, Contingency)
- Each item `total` = `qty × unit_cost`; category `total` = sum of items; `budget.total` = sum of categories

### 8. Phases

- **Minimum 3, maximum 8**
- Each phase needs a hex color code
- Phases must cover the entire project timeline without gaps

### 9. WBS

- Level 0 = project name (id `"0"`)
- Level 1 = major phases/deliverables (3–6 items)
- Level 2 = work packages under each Level 1 branch
- IDs follow PMI numbering: `1`, `1.1`, `1.2`, `2`, `2.1`, etc.

### 10. Diagrams to Generate

- List every diagram type needed for this project
- Only use keys from the allowed list in Section 5

---

## 7. Validation Rules

Run this checklist before writing the file. Fix every failure.

1. All required fields populated — no empty strings, no null values
2. Dates in `YYYY-MM-DD` format
3. All IDs unique within their section
4. Stakeholder engagement strategies match Power–Interest mapping:
   - High Power + High Interest → `"Manage Closely"`
   - High Power + Low Interest → `"Keep Satisfied"`
   - Low Power + High Interest → `"Keep Informed"`
   - Low Power + Low Interest → `"Monitor"`
   - Medium values: use closest quadrant logic and stay consistent
5. Risk `score` = `probability × impact` for every risk
6. WBS IDs follow proper numbering hierarchy
7. Budget arithmetic correct at item, category, and total levels
8. Phase dates sequential, non-overlapping, within `project.start_date`–`project.end_date`
9. Milestone dates within project timeline
10. JSON is syntactically valid (no trailing commas, proper quoting)

Optional validation command if Python is available:

```bash
python3 -c "import json; json.load(open('projects/<project-slug>/specifications.json'))"
```

---

## 8. Diagram-to-Skill Mapping

After `specifications.json` is written, invoke downstream skills based on `diagrams_to_generate`:

| diagrams_to_generate key | Read this skill next |
|--------------------------|---------------------|
| `stakeholder_register`, `power_interest_matrix`, `influence_network`, `salience_model`, `stakeholder_map` | [stakeholder-diagram-generator-SKILL.md](stakeholder-diagram-generator-SKILL.md) |
| `risk_matrix` | [risk-matrix-diagram-generator-SKILL.md](risk-matrix-diagram-generator-SKILL.md) |
| `gantt_chart` | [gantt-chart-generator-SKILL.md](gantt-chart-generator-SKILL.md) |
| `wbs_diagram` | [wbs-diagram-generator-SKILL.md](wbs-diagram-generator-SKILL.md) |
| `budget_breakdown` | [budget-breakdown-generator-SKILL.md](budget-breakdown-generator-SKILL.md) |
| `milestone_chart` | [milestone-chart-generator-SKILL.md](milestone-chart-generator-SKILL.md) |
| `pert_chart` | [pert-chart-generator-SKILL.md](pert-chart-generator-SKILL.md) |
| `cpm_network` | [cpm-network-diagram-generator-SKILL.md](cpm-network-diagram-generator-SKILL.md) |
| `kanban_chart` | [kanban-chart-generator-SKILL.md](kanban-chart-generator-SKILL.md) |
| `system_context` | [system-context-diagram-generator-SKILL.md](system-context-diagram-generator-SKILL.md) |
| `communication_diagram` | [communication_diagram_generator/SKILL.md](communication_diagram_generator/SKILL.md) |
| `problem_tree` | [problem-tree-generator-SKILL.md](problem-tree-generator-SKILL.md) |
| `raci_matrix` | [raci-matrix-diagram-generator-SKILL.md](raci-matrix-diagram-generator-SKILL.md) |
| `resource_allocation_matrix` | [resource-allocation-matrix-generator-SKILL.md](resource-allocation-matrix-generator-SKILL.md) |
| `project_charter` | [project-charter-generator-SKILL.md](project-charter-generator-SKILL.md) |
| `uml_diagram` | [uml-diagram-generator-SKILL.md](uml-diagram-generator-SKILL.md) |

Each downstream skill expects its own input JSON shape. Section 9 explains how to map fields from `specifications.json`.

---

## 9. Downstream File Generation

When the user wants to run generators immediately, split `specifications.json` into per-skill input files under `projects/<project-slug>/inputs/`.

### Stakeholder diagrams (`stakeholder_input.json`)

Map `stakeholders[]` to the stakeholder register format. Use `"title"` instead of `"role"`. Set `"engagement_strategy": "auto"` to let the generator classify from power/interest.

```json
{
  "stakeholder_register": {
    "title": "Stakeholder Register",
    "project_name": "<project.name>",
    "version": "<project.version>",
    "stakeholders": [ /* mapped from specifications.stakeholders */ ]
  }
}
```

See [stakeholder_diagram_generator/examples/sample_input.json](stakeholder_diagram_generator/examples/sample_input.json) for the full shape.

### Gantt chart (`gantt_input.json`)

Map `phases`, `milestones`, and `wbs.branches` into tasks with start/end dates and dependencies. See [gantt_chart_generator/examples/sample_input.json](gantt_chart_generator/examples/sample_input.json).

### Risk matrix (`risk_matrix_input.json`)

Map `risks[]` directly. See [risk-matrix-diagram-generator-SKILL.md](risk-matrix-diagram-generator-SKILL.md) Section 3.

### WBS diagram (`wbs_input.json`)

Map `wbs` directly. See [wbs-diagram-generator-SKILL.md](wbs-diagram-generator-SKILL.md) Section 3.

### Budget breakdown (`budget_input.json`)

Map `budget` directly. See [budget_breakdown_generator/examples/sample_input.json](budget_breakdown_generator/examples/sample_input.json).

### Milestone chart (`milestone_input.json`)

Map `milestones[]` and `phases[]`. See [milestone_chart_generator/examples/sample_input.json](milestone_chart_generator/examples/sample_input.json).

Only create split files for diagrams listed in `diagrams_to_generate`.

---

## 10. Quick Reference Card

| Section | Minimum | Maximum | Key Field |
|---------|---------|---------|-----------|
| Objectives | 3 | 8 | measurable_criteria |
| Stakeholders | 5 | 15 | engagement_strategy |
| Risks | 3 | 10 | score (P × I) |
| Milestones | 3 | 15 | is_critical |
| Budget Categories | 3 | 8 | total (must sum) |
| Phases | 3 | 8 | color (hex) |
| WBS Level 1 | 3 | 6 | children |

---

## 11. Worked Example (Da'atSNA)

**Input provided by user:**

| Field | Value |
|-------|-------|
| Project Name | Da'atSNA Community Data Platform |
| Project Type | Software Development / Social Enterprise |
| Description | A community-driven data platform for Ugandan communities to collect, analyze, and visualize social network data offline |
| Stakeholders | Ministry of Health Uganda, Community Leaders, NGOs, Developers, Researchers |
| Objectives | Build offline-first SNA platform; Empower communities with data skills; Enable evidence-based decision-making |
| Timeline | 2026-01-01 – 2026-12-31 |
| Budget | $59,400 USD |

**Expected output path:** `projects/daatsna-community-data-platform/specifications.json`

**Expected diagrams_to_generate:**

```json
[
  "stakeholder_register",
  "power_interest_matrix",
  "influence_network",
  "salience_model",
  "stakeholder_map",
  "risk_matrix",
  "milestone_chart",
  "wbs_diagram",
  "budget_breakdown",
  "gantt_chart",
  "system_context"
]
```

For a complete reference implementation, see the sample inputs across this repository (all use Da'atSNA as the example project).

---

## 12. Agent Response Format

When completing this skill, respond with:

1. **Assumptions** — bullet list of anything inferred (only if applicable)
2. **File written** — full path to `specifications.json`
3. **Validation summary** — confirm all Section 7 rules passed
4. **Next steps** — which downstream skills to invoke, in recommended order:
   1. `prompt-skill-generator` (this skill) ← you are here
   2. Individual diagram skills based on `diagrams_to_generate`
   3. `project-charter-generator` if a full charter document is needed

Return the complete `specifications.json` content in a single JSON code block **and** write it to disk. Do not return JSON only in chat without saving the file unless the user explicitly asks not to write files.

---

## Embedded Agent Prompt (Copy-Ready)

Use this verbatim prompt block when delegating to another agent or re-running generation:

```
You are a project documentation specialist. Your task is to generate a complete specifications.json file for the project described below. This file will be used to generate professional project diagrams (stakeholder maps, Gantt charts, risk matrices, etc.) using the UML-SKILLS diagram generation skills.

Read the project description carefully and extract all required information. Follow the JSON schema in prompt_skill_generator_SKILL.md exactly. If information is not explicitly provided, make reasonable inferences based on the project type and context.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [INSERT PROJECT TYPE]
**Project Description:** [INSERT PROJECT DESCRIPTION]
**Key Stakeholders:** [LIST STAKEHOLDERS OR DESCRIBE]
**Key Objectives:** [LIST OBJECTIVES]
**Timeline:** [START DATE - END DATE]
**Budget:** [TOTAL BUDGET AND CURRENCY]

## Deliverables

1. A complete, valid specifications.json following the schema in prompt_skill_generator_SKILL.md
2. Saved to projects/<project-slug>/specifications.json
3. All validation rules satisfied

## Validation Rules

1. All required fields must be populated
2. Dates must be in YYYY-MM-DD format
3. IDs must be unique
4. Stakeholder engagement strategies must match Power-Interest mapping
5. Risk scores must equal Probability × Impact
6. WBS IDs must follow proper numbering (1, 1.1, 1.2, etc.)
7. Budget totals must sum correctly
8. Phase dates must be sequential and within project timeline

Now, generate the specifications.json for the project described above.
```
