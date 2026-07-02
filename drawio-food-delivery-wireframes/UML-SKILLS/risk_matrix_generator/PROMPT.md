# Risk Matrix Generator — Agent Prompt

Use this file to generate the input JSON required by the **Risk Matrix Generator**. Any agentic AI working on any project can follow this prompt to produce a valid `risk_matrix_input.json` that renders a Probability × Impact heat map with risk cards and a risk register as a fully editable Visio file (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`risk_matrix` is listed** in `specifications.json → diagrams_to_generate`
3. Read [risk-matrix-diagram-generator-SKILL.md](../risk-matrix-diagram-generator-SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | Description |
|--------|--------|-------------|
| Risk matrix | `.vsdx` | 5×5 Probability × Impact grid with zone colors, risk item cards, risk register table, summary block |

## Output File Location

Save the generated input to:

```text
projects/<project-slug>/inputs/risk_matrix_input.json
```

Example: `projects/daatsna-community-data-platform/inputs/risk_matrix_input.json`

---

## Agent Instructions

You are a project risk analyst. Your task is to generate a complete `risk_matrix_input.json` file for the Risk Matrix Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json` (especially `risks`, `project`, `stakeholders`).
2. Copy or define default **probability** and **impact** scales (1–5).
3. Include default **risk_zones** (Critical → Minimal).
4. Transform each `specifications.json → risks[]` entry into a plotted risk with `probability`, `impact`, mitigation, owner, and category.
5. Compute `score = probability × impact` and assign `zone` (or omit — builder auto-computes).
6. Validate against all rules in the Validation section.
7. Write the file to `projects/<project-slug>/inputs/risk_matrix_input.json`.
8. Return the complete JSON in a single code block and confirm the file path.

If `specifications.json` is missing, gather risks from the user — or infer from project type and list assumptions.

---

## Mapping from specifications.json

| specifications.json | risk_matrix_input.json | Notes |
|-----------------------|------------------------|-------|
| `project.name` | `risk_matrix.project_name` | Full project name |
| `project.version` | `risk_matrix.version` | e.g. `"1.0"` |
| `project.date` | `risk_matrix.date` | `YYYY-MM-DD` |
| `risks[].id` | `risks[].id` | Keep IDs (R-001, R-002, …) |
| `risks[].name` | `risks[].name` | Short label for card |
| `risks[].description` | `risks[].description` | Full risk description |
| `risks[].probability` | `risks[].probability` | Integer 1–5 |
| `risks[].impact` | `risks[].impact` | Integer 1–5 |
| `risks[].score` | `risks[].score` | **Compute:** `probability × impact` |
| `risks[].mitigation` | `risks[].mitigation` | Required for register |
| `risks[].owner` | `risks[].owner` | Map to stakeholder role/name |
| — | `risks[].zone` | Auto from grid lookup (see Zone Map) |
| — | `risks[].category` | Infer: Security, Technical, Schedule, etc. |
| — | `risks[].status` | Open, In Progress, Monitoring, Closed |
| — | `risks[].trigger` | Early warning indicator |

### Charter field name difference

[project_charter_generator/PROMPT.md](../project_charter_generator/PROMPT.md) uses `likelihood` instead of `probability`. When sourcing from a charter payload:

```json
"probability": "<charter.risks[].likelihood>"
```

Risk matrix input always uses **`probability`**, not `likelihood`.

### Score and zone auto-computation

The builder **always overrides** declared `score` and `zone` from `probability × impact` and the cell lookup table (`calculators/risk_calculator.py`, `calculators/zone_calculator.py`). You may omit `score` and `zone`, or include correctly computed values. Mismatched values trigger consistency warnings RX-005 / RX-006 but are corrected at render time.

### Recommended risk categories

| Category | Examples |
|----------|----------|
| Security | Data breach, unauthorized access |
| Compliance | HIPAA, GDPR, regulatory audit failure |
| Technical | System failure, integration issues |
| Resource | Staff turnover, skill gaps |
| Financial | Budget overrun, cost escalation |
| Schedule | Milestone slip, dependency delay |
| Stakeholder | Adoption resistance, sponsor disengagement |

---

## JSON Schema

Generate a complete JSON file with this structure:

```json
{
  "risk_matrix": {
    "title": "string - Diagram title",
    "project_name": "string - Full project name",
    "version": "string - Version (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",
    "sprint": "string - Optional period label",
    "description": "string - Optional description",

    "probability_scale": {
      "1": "Rare",
      "2": "Unlikely",
      "3": "Possible",
      "4": "Likely",
      "5": "Almost Certain"
    },

    "impact_scale": {
      "1": "Minor",
      "2": "Moderate",
      "3": "Major",
      "4": "Severe",
      "5": "Catastrophic"
    },

    "risk_zones": [
      {
        "id": "critical",
        "name": "Critical",
        "color": "#E53935",
        "text_color": "#FFFFFF",
        "score_range": [20, 25],
        "action": "Immediate action required",
        "symbol": "CRITICAL"
      },
      {
        "id": "high",
        "name": "High",
        "color": "#FF9800",
        "text_color": "#FFFFFF",
        "score_range": [15, 19],
        "action": "Senior management attention",
        "symbol": "HIGH"
      },
      {
        "id": "medium",
        "name": "Medium",
        "color": "#FFC107",
        "text_color": "#333333",
        "score_range": [10, 14],
        "action": "Management attention required",
        "symbol": "MEDIUM"
      },
      {
        "id": "low",
        "name": "Low",
        "color": "#4CAF50",
        "text_color": "#FFFFFF",
        "score_range": [5, 9],
        "action": "Monitor and review",
        "symbol": "LOW"
      },
      {
        "id": "minimal",
        "name": "Minimal",
        "color": "#E0E0E0",
        "text_color": "#333333",
        "score_range": [1, 4],
        "action": "Acceptable, monitor only",
        "symbol": "MINIMAL"
      }
    ],

    "risks": [
      {
        "id": "string - R-001, R-002, ...",
        "name": "string - Short risk name",
        "description": "string - Full risk description",
        "probability": "number - 1 to 5",
        "impact": "number - 1 to 5",
        "score": "number - probability × impact (optional; auto-computed)",
        "zone": "string - critical | high | medium | low | minimal (optional; auto-computed)",
        "category": "string - Risk category",
        "mitigation": "string - Mitigation strategy",
        "owner": "string - Risk owner role or name",
        "status": "string - Open | In Progress | Monitoring | Closed",
        "trigger": "string - Early warning indicator"
      }
    ],

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "grid_line_color": "#333333",
      "grid_line_width": 1,
      "cell_size": 1.5,
      "shadow_enabled": true
    },

    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "header_height": 1.2,
      "summary_height": 2.0
    }
  }
}
```

---

## Section Guidelines

### Probability scale (Y-axis, 1 = bottom, 5 = top)

| Score | Label | Approx. frequency |
|-------|-------|-------------------|
| 5 | Almost Certain | ≥ 75% — more than once per year |
| 4 | Likely | 50–74% — once per year |
| 3 | Possible | 25–49% — once every 2–3 years |
| 2 | Unlikely | 10–24% — once every 5 years |
| 1 | Rare | < 10% — once every 10+ years |

### Impact scale (X-axis, 1 = left, 5 = right)

| Score | Label | Example severity |
|-------|-------|------------------|
| 5 | Catastrophic | Business failure, loss of life |
| 4 | Severe | Major reputation damage, ops suspended |
| 3 | Major | Significant operational impact |
| 2 | Moderate | Manageable, recoverable impact |
| 1 | Minor | Negligible impact |

### Zone map (5×5 cell lookup)

Zone is determined by **(probability, impact) cell position**, not score alone. Use this table when assigning `zone`:

```text
                 IMPACT
                  1        2        3        4        5
                  ─────────────────────────────────────
Prob 5 │         LOW      MED      HIGH     HIGH     CRIT
Prob 4 │         MIN      LOW      MED      HIGH     CRIT
Prob 3 │         MIN      LOW      LOW      MED      HIGH
Prob 2 │         MIN      MIN      LOW      LOW      MED
Prob 1 │         MIN      MIN      MIN      MIN      LOW
```

Abbreviations: CRIT = critical, MED = medium, MIN = minimal.

Example: `(probability=4, impact=3)` → score 12, zone **medium** (not high — score 12 alone would be medium, but cell lookup is authoritative).

### Risks array

- **Minimum 3, recommended 5–10**
- Unique `id` per risk (RX-007)
- `probability` and `impact` must be integers **1–5** (RX-003, RX-004)
- Every risk needs a non-empty `mitigation` string
- Spread risks across the grid — avoid placing more than **3 risks in the same cell** (RX-012 overflow warning)
- Include at least one risk in Critical or High zone for realistic portfolios

### risk_zones array

- **Required** — provide all 5 zones (RX-008 if empty)
- Use default colors and score ranges from schema above
- `id` values must match zone lookup: `critical`, `high`, `medium`, `low`, `minimal`

---

## Validation Rules

Fix every failure before writing the file:

1. All required fields populated under `risk_matrix`
2. At least **1 risk** in `risks[]` (RX-002)
3. All risk IDs unique (RX-007)
4. `probability` and `impact` are integers 1–5 for every risk
5. If provided, `score` must equal `probability × impact` (otherwise builder overrides — RX-005)
6. If provided, `zone` must match cell lookup for that pair (otherwise builder overrides — RX-006)
7. `risk_zones` array has all 5 zone definitions
8. No more than 3 risks share the same `(probability, impact)` pair (RX-012 warning if exceeded)
9. Dates in `YYYY-MM-DD` format
10. JSON is syntactically valid

Optional validation:

```bash
python risk_matrix_generator/cli.py projects/<project-slug>/inputs/risk_matrix_input.json --validate-only
```

---

## Quick Reference Card

| Section | Minimum | Maximum | Key Rule |
|---------|---------|---------|----------|
| Risks | 1 | 20 | Unique IDs; P and I are 1–5 |
| risk_zones | 5 | 5 | All zone bands defined |
| Score | 1 | 25 | Always P × I |
| Risks per cell | 0 | 3 | Overflow beyond 3 triggers warning |
| Mitigation | required | — | Non-empty string per risk |

---

## After Generating Input

Run the generator:

```bash
# Render Visio risk matrix
python risk_matrix_generator/cli.py projects/<project-slug>/inputs/risk_matrix_input.json \
  -o projects/<project-slug>/output/risk_matrix.vsdx

# Highlight top 5 risks in summary
python risk_matrix_generator/cli.py projects/<project-slug>/inputs/risk_matrix_input.json \
  --top-risks 5 -o projects/<project-slug>/output/risk_matrix.vsdx

# Grid only (skip register table)
python risk_matrix_generator/cli.py projects/<project-slug>/inputs/risk_matrix_input.json \
  --no-register -o projects/<project-slug>/output/risk_matrix.vsdx

# Validate only
python risk_matrix_generator/cli.py projects/<project-slug>/inputs/risk_matrix_input.json --validate-only
```

Reference schema: [risk-matrix-diagram-generator-SKILL.md](../risk-matrix-diagram-generator-SKILL.md) Section 3 (full Da'atSNA example with 7 risks).

---

## Integration Notes

- `specifications.json → risks[]` maps nearly 1:1 — primary upstream source.
- [project_charter_generator/PROMPT.md](../project_charter_generator/PROMPT.md) embeds risk matrix from `risks[]`; charter uses `likelihood` → map to `probability` here.
- Risk `owner` aligns with roles in [raci_matrix_generator/PROMPT.md](../raci_matrix_generator/PROMPT.md).
- Risk `category` aligns with WBS Level-1 branches in [wbs_diagram_generator/PROMPT.md](../wbs_diagram_generator/PROMPT.md) (when available).
- [problem_tree_generator/PROMPT.md](../problem_tree_generator/PROMPT.md) derives causal trees from risks — complementary, not a substitute for this heat map.

### Builder implementation note

`core/diagram_builder.py` reads `styling` and `layout` from the JSON **root** as well as `risk_matrix` content. If custom styling does not apply, duplicate `styling` and `layout` at the root level mirroring the nested values.

---

## Copy-Ready Agent Prompt

```
You are a project risk analyst. Your task is to generate a complete risk_matrix_input.json file for the Risk Matrix Generator (Visio .vsdx output).

Read the project data from specifications.json or the project description below. Follow the JSON schema in risk_matrix_generator/PROMPT.md exactly. If information is not explicitly provided, derive risks from project type, domain, and stakeholders and list assumptions.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Software Development, Healthcare, Infrastructure]
**Known Risks:** [LIST RISKS WITH PROBABILITY/IMPACT IF KNOWN]
**Risk Owners:** [LIST WHO OWNS EACH RISK]
**Mitigation Strategies:** [DESCRIBE OR REQUEST INFERENCE]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables

1. A complete, valid risk_matrix_input.json following the schema in risk_matrix_generator/PROMPT.md
2. Saved to projects/<project-slug>/inputs/risk_matrix_input.json
3. All validation rules satisfied

## Validation Rules

1. At least 1 risk; recommend 5-10 with varied P/I scores
2. probability and impact: integers 1-5 for every risk
3. score = probability × impact (omit or compute correctly)
4. zone matches the 5×5 cell lookup table (omit or compute correctly)
5. All risk IDs unique (R-001, R-002, ...)
6. Every risk has mitigation, owner, category, status, and trigger
7. Include all 5 risk_zones with default colors
8. Include probability_scale and impact_scale defaults
9. No more than 3 risks in the same (probability, impact) cell

## Response Format

Return the complete risk_matrix_input.json in a single JSON code block AND write it to disk at projects/<project-slug>/inputs/risk_matrix_input.json.

Now, generate the risk_matrix_input.json for the project described above.
```
