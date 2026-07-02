# Stakeholder Diagram Generator — Agent Prompt

Use this file to generate the input JSON required by the **Stakeholder Diagram Generator**. Unlike single-diagram generators, this skill produces **five artefacts** from one stakeholder dataset. You must create **six JSON files**: one **main combined file** plus **five per-diagram files**.

Any agentic AI working on any project can follow this prompt to produce valid inputs that render Stakeholder Register, Power-Interest Matrix, Influence Network, Salience Model, and Stakeholder Map as fully editable Visio files (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. Relevant diagram keys are listed in `specifications.json → diagrams_to_generate`:
   - `stakeholder_register`
   - `power_interest_matrix`
   - `influence_network`
   - `salience_model`
   - `stakeholder_map`
3. Read [stakeholder-diagram-generator-SKILL.md](../stakeholder-diagram-generator-SKILL.md) for rendering details (§2–§6 schemas, §8 complete package)

## What This Generator Produces

| # | Diagram | Output |
|---|---------|--------|
| 1 | Stakeholder Register | `register.vsdx`, `register.xlsx`, `register.csv` |
| 2 | Power-Interest Matrix | `power_interest.vsdx`, `power_interest.xlsx` |
| 3 | Influence Network | `influence.vsdx` |
| 4 | Salience Model | `salience.vsdx` |
| 5 | Stakeholder Map | `stakeholder_map.vsdx` |
| — | Combined package | `stakeholder_analysis_package.vsdx` (5 pages, `--combined`) |

> **RACI Matrix is NOT part of this generator.** Use [raci_matrix_generator/PROMPT.md](../raci_matrix_generator/PROMPT.md) separately.

---

## Output File Locations — READ THIS FIRST

You must write **six files** under `projects/<project-slug>/inputs/`:

| File | Purpose | Root key |
|------|---------|----------|
| **`stakeholder_input.json`** | **MAIN** — merged package passed to CLI | all five keys |
| `stakeholder_register_input.json` | Register only | `stakeholder_register` |
| `power_interest_input.json` | Power-Interest Matrix only | `power_interest_matrix` |
| `influence_network_input.json` | Influence Network only | `influence_network` |
| `salience_model_input.json` | Salience Model only | `salience_model` |
| `stakeholder_map_input.json` | Stakeholder Map only | `stakeholder_map` |

Example paths (Da'atSNA):

```text
projects/daatsna-community-data-platform/inputs/stakeholder_input.json          ← MAIN
projects/daatsna-community-data-platform/inputs/stakeholder_register_input.json
projects/daatsna-community-data-platform/inputs/power_interest_input.json
projects/daatsna-community-data-platform/inputs/influence_network_input.json
projects/daatsna-community-data-platform/inputs/salience_model_input.json
projects/daatsna-community-data-platform/inputs/stakeholder_map_input.json
```

### How the six files relate

```text
specifications.json
        │
        ▼
┌───────────────────────────────────────────────────────────────────┐
│  STEP 1 — Create stakeholder_register_input.json  (SOURCE OF TRUTH) │
└───────────────────────────────────────────────────────────────────┘
        │
        ├──► STEP 2 — power_interest_input.json      (derived from register)
        ├──► STEP 3 — salience_model_input.json      (derived from register)
        ├──► STEP 4 — influence_network_input.json   (register + relationships)
        └──► STEP 5 — stakeholder_map_input.json     (register + rings/sectors)
        │
        ▼
┌───────────────────────────────────────────────────────────────────┐
│  STEP 6 — MERGE all five into stakeholder_input.json  (MAIN)     │
└───────────────────────────────────────────────────────────────────┘
        │
        ▼
   CLI: python stakeholder_diagram_generator/cli.py stakeholder_input.json --combined
```

**Merge rule for the MAIN file:** shallow-merge the five per-diagram files into one object:

```json
{
  "stakeholder_register": { /* from stakeholder_register_input.json */ },
  "power_interest_matrix": { /* from power_interest_input.json */ },
  "influence_network": { /* from influence_network_input.json */ },
  "salience_model": { /* from salience_model_input.json */ },
  "stakeholder_map": { /* from stakeholder_map_input.json */ }
}
```

Only include keys for diagrams listed in `diagrams_to_generate`. If a diagram is not requested, omit both its split file and its key in the main file.

---

## Agent Instructions

You are a stakeholder management specialist. Your task is to generate **six JSON files** for the Stakeholder Diagram Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json` (especially `stakeholders[]`, `project`, `diagrams_to_generate`).
2. Check which of the five stakeholder diagrams are requested.
3. **Create `stakeholder_register_input.json` first** — map every stakeholder from specifications (minimum 5–12 stakeholders).
4. **Create `power_interest_input.json`** — assign stakeholders to quadrants from register `power` × `interest`.
5. **Create `salience_model_input.json`** — classify stakeholders using register `power`, `legitimacy`, `urgency`.
6. **Create `influence_network_input.json`** — build nodes from register + define relationships and groups.
7. **Create `stakeholder_map_input.json`** — place stakeholders on rings/sectors + map relationships.
8. **Merge all five into `stakeholder_input.json`** (the MAIN file).
9. Validate every file against the rules in the Validation section.
10. Write all six files to disk and confirm each path in your response.

If `specifications.json` is missing, gather stakeholders from the user — or infer from project type and list assumptions.

### Critical rules

- **Same stakeholder IDs everywhere** — `S-001`, `S-002`, … must match across all six files.
- **Register is authoritative** — power, interest, legitimacy, urgency, names, titles come from register; downstream files reference register IDs, never invent new people silently.
- **Six files, not one** — always write the five split files **and** the merged main file, even when only generating one diagram (register-only projects still get register split + main with register key only).
- **`engagement_strategy: "auto"`** is valid on register — validator derives strategy from power × interest before render.

---

## Mapping from specifications.json

| specifications.json | All stakeholder JSON files | Notes |
|---------------------|---------------------------|-------|
| `project.name` | `*.project_name` | On every diagram section |
| `project.version` | `*.version` | e.g. `"1.0"` |
| `project.date` | `*.date` | `YYYY-MM-DD` where section supports it |
| `stakeholders[].id` | register + all cross-refs | Keep IDs identical |
| `stakeholders[].name` | register `name` | |
| `stakeholders[].role` | register **`title`** | **Rename:** spec uses `role`, register uses `title` |
| `stakeholders[].organization` | register `organization` | |
| `stakeholders[].category` | register `category` | `Internal` or `External` |
| `stakeholders[].power` | register + salience + matrix | |
| `stakeholders[].interest` | register + matrix | |
| `stakeholders[].influence` | register + influence nodes | |
| `stakeholders[].legitimacy` | register + salience | |
| `stakeholders[].urgency` | register + salience | |
| `stakeholders[].expectations` | register `expectations` | |
| `stakeholders[].engagement_strategy` | register | Or use `"auto"` |
| `stakeholders[].contact` | register `contact` | |
| — | register `needs` | **Add** if missing in spec |
| — | register `status` | Default `"Active"` |
| — | register `type` | `"Primary"` or `"Secondary"` |

### Field name: `role` vs `title`

```json
// specifications.json
"role": "Project Sponsor"

// stakeholder_register_input.json
"title": "Project Sponsor"
```

---

## File 1 — `stakeholder_register_input.json`

**Create this file first.** Full schema in [stakeholder-diagram-generator-SKILL.md](../stakeholder-diagram-generator-SKILL.md) §2.4.

```json
{
  "stakeholder_register": {
    "title": "Stakeholder Register",
    "project_name": "string",
    "version": "1.0",
    "date": "YYYY-MM-DD",
    "stakeholders": [
      {
        "id": "S-001",
        "name": "string",
        "title": "string",
        "organization": "string",
        "category": "Internal | External",
        "type": "Primary | Secondary",
        "power": "High | Medium | Low",
        "interest": "High | Medium | Low",
        "influence": "High | Medium | Low",
        "legitimacy": "High | Medium | Low",
        "urgency": "High | Medium | Low",
        "expectations": "string",
        "needs": "string",
        "engagement_strategy": "Manage Closely | Keep Satisfied | Keep Informed | Monitor | auto",
        "communication_preference": "string (optional)",
        "contact": "string (optional)",
        "status": "Active | Inactive | Blocked",
        "notes": "string (optional)"
      }
    ]
  }
}
```

**Minimum:** 5 stakeholders, unique IDs, all required fields.

---

## File 2 — `power_interest_input.json`

Derived from register. Full schema: SKILL §3.3.

```json
{
  "power_interest_matrix": {
    "title": "Power-Interest Matrix - Stakeholder Mapping",
    "project_name": "string",
    "version": "1.0",
    "date": "YYYY-MM-DD",
    "quadrants": {
      "key_players": {
        "id": "Q1",
        "label": "Key Players",
        "power": "High",
        "interest": "High",
        "color": "#E53935",
        "text_color": "#FFFFFF",
        "strategy": "Manage Closely",
        "engagement_activities": ["Regular meetings (monthly)", "Detailed reporting"],
        "stakeholders": ["S-001", "S-002"]
      },
      "keep_satisfied": {
        "id": "Q2",
        "label": "Keep Satisfied",
        "power": "High",
        "interest": "Low",
        "color": "#FF9800",
        "text_color": "#FFFFFF",
        "strategy": "Keep Satisfied",
        "engagement_activities": ["Quarterly updates", "Annual reports"],
        "stakeholders": ["S-006"]
      },
      "keep_informed": {
        "id": "Q3",
        "label": "Keep Informed",
        "power": "Low",
        "interest": "High",
        "color": "#FFC107",
        "text_color": "#333333",
        "strategy": "Keep Informed",
        "engagement_activities": ["Newsletters", "Focus groups"],
        "stakeholders": ["S-004", "S-005"]
      },
      "monitor": {
        "id": "Q4",
        "label": "Monitor",
        "power": "Low",
        "interest": "Low",
        "color": "#4CAF50",
        "text_color": "#FFFFFF",
        "strategy": "Monitor",
        "engagement_activities": ["Public notices", "Annual reports"],
        "stakeholders": ["S-009", "S-010"]
      }
    },
    "styling": { "theme": "enterprise_blue", "font_family": "Arial", "font_size": 9 },
    "layout": { "orientation": "landscape", "page_size": "A2", "margin": 0.5 }
  }
}
```

### Quadrant assignment rules

| power | interest | Quadrant key | Strategy |
|-------|----------|--------------|----------|
| High | High | `key_players` | Manage Closely |
| High | Low/Medium | `keep_satisfied` | Keep Satisfied |
| Low/Medium | High | `keep_informed` | Keep Informed |
| Low/Medium | Low/Medium | `monitor` | Monitor |

Each register stakeholder ID appears in **exactly one** quadrant.

---

## File 3 — `influence_network_input.json`

Nodes from register + explicit relationships. Full schema: SKILL §4.3.

```json
{
  "influence_network": {
    "title": "Influence Network Diagram - Stakeholder Relationships",
    "project_name": "string",
    "version": "1.0",
    "date": "YYYY-MM-DD",
    "nodes": [
      {
        "id": "N1",
        "stakeholder_id": "S-001",
        "name": "string",
        "role": "string",
        "organization": "string",
        "influence_score": 8.5,
        "category": "Executive | PMO | Clinical | Technical | External",
        "color": "#1a237e",
        "text_color": "#FFFFFF",
        "x": 15.0,
        "y": 12.0,
        "size": 3.0
      }
    ],
    "relationships": [
      {
        "id": "R1",
        "source": "N1",
        "target": "N2",
        "type": "Formal Authority | Collaboration | Influence/Advice | Communication | Conflict/Tension | External Influence",
        "strength": "Strong | Medium | Weak",
        "label": "string",
        "color": "#1a237e",
        "bidirectional": false,
        "description": "string"
      }
    ],
    "groups": [
      {
        "id": "G1",
        "name": "Executive Leadership",
        "color": "#1a237e",
        "opacity": 0.1,
        "nodes": ["N1", "N2"]
      }
    ],
    "styling": { "theme": "enterprise_blue", "node_radius": 1.5, "arrow_style": "curved" },
    "layout": { "orientation": "landscape", "page_size": "A2", "algorithm": "force_directed" }
  }
}
```

**Influence score:** 0–10. Derive from register `power` + relationship count (see SKILL §4.8).

**Pydantic note:** `core/models.py` uses `edges[]` with `from`/`to`. The SKILL and this prompt prefer `relationships[]` with `source`/`target`. Either form works if the builder normalises them; when in doubt, include **both** or use `relationships[]` as documented in the SKILL.

---

## File 4 — `salience_model_input.json`

Classify from register P/L/U attributes. Full schema: SKILL §5.6.

```json
{
  "salience_model": {
    "title": "Salience Model - Stakeholder Prioritization",
    "project_name": "string",
    "version": "1.0",
    "date": "YYYY-MM-DD",
    "stakeholders": [
      {
        "id": "S-001",
        "name": "string",
        "role": "string",
        "organization": "string",
        "power": "High | Medium | Low",
        "legitimacy": "High | Medium | Low",
        "urgency": "High | Medium | Low",
        "category": "Definitive | Dominant | Dangerous | Dependent | Discretionary | Demanding | Dormant",
        "priority": "Critical | High | Medium | Low",
        "color": "#1a237e",
        "engagement": "string",
        "notes": "string"
      }
    ],
    "styling": { "venn_diagram_enabled": true, "show_attributes": true },
    "layout": { "orientation": "landscape", "page_size": "A2", "venn_scale": 1.0 }
  }
}
```

### Salience categories (Mitchell, Agle & Wood)

| Category | Power | Legitimacy | Urgency |
|----------|-------|------------|---------|
| Definitive | ✓ | ✓ | ✓ |
| Dominant | ✓ | ✓ | ✗ |
| Dangerous | ✓ | ✗ | ✓ |
| Dependent | ✗ | ✓ | ✓ |
| Discretionary | ✗ | ✓ | ✗ |
| Demanding | ✗ | ✗ | ✓ |
| Dormant | ✓ | ✗ | ✗ |

Only **High** counts as present (✓). Omit `category` to let the builder auto-classify from P/L/U.

---

## File 5 — `stakeholder_map_input.json`

Ecosystem radial map. Full schema: SKILL §6.3.

```json
{
  "stakeholder_map": {
    "title": "Stakeholder Map - Stakeholder Ecosystem",
    "project_name": "string",
    "version": "1.0",
    "date": "YYYY-MM-DD",
    "stakeholders": [
      {
        "id": "S-001",
        "name": "string",
        "role": "string",
        "organization": "string",
        "ring": "inner | middle | outer",
        "sector": "Executive | Management | Clinical | Technical | Regulatory | Financial | External",
        "engagement_level": "High | Medium | Low",
        "color": "#1a237e",
        "text_color": "#FFFFFF",
        "x": 18.0,
        "y": 12.0,
        "radius": 1.2
      }
    ],
    "relationships": [
      {
        "source": "S-001",
        "target": "S-003",
        "type": "Direct Reporting | Collaboration | Advisory | External Connection | Conflict/Tension",
        "label": "string",
        "strength": "Strong | Medium | Weak"
      }
    ],
    "styling": {
      "ring_color": "#E3F2FD",
      "show_relationship_lines": true,
      "show_sector_labels": true
    },
    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "center_radius": 2.0,
      "inner_radius": 6.0,
      "middle_radius": 10.0,
      "outer_radius": 15.0
    }
  }
}
```

### Ring assignment from register engagement strategy

| engagement_strategy | Default ring |
|---------------------|--------------|
| Manage Closely | inner |
| Keep Satisfied | middle |
| Keep Informed | middle |
| Monitor | outer |

---

## File 6 — `stakeholder_input.json` (MAIN)

**This is the file passed to the CLI.** It must contain all five top-level keys (or only those requested in `diagrams_to_generate`):

```json
{
  "stakeholder_register": { },
  "power_interest_matrix": { },
  "influence_network": { },
  "salience_model": { },
  "stakeholder_map": { }
}
```

Each value is the **inner object** copied from the corresponding split file (not the wrapper repeated twice).

**After writing all split files, verify the main file equals their merge.** The main file must stay in sync whenever any split file is updated.

Reference: [stakeholder_diagram_generator/examples/sample_input.json](examples/sample_input.json)

---

## Validation Rules

Apply to **all six files** before writing:

### Cross-file consistency

1. Stakeholder IDs (`S-001`, …) identical in register, matrix quadrants, salience, influence `stakeholder_id`, and map
2. Names and titles match register across all diagrams
3. Main file `stakeholder_input.json` contains exactly the merge of the five split files

### Register (`stakeholder_register_input.json`)

4. Minimum 5 stakeholders; unique IDs (`SR-001`)
5. All required fields populated (`SR-002`)
6. `category`, `power`, `interest`, etc. use valid enums (`SR-003`, `SR-004`)
7. `engagement_strategy` is valid or `"auto"` (`SR-006`)

### Power-Interest (`power_interest_input.json`)

8. Every quadrant stakeholder ID exists in register (`PI-001`)
9. Each stakeholder in exactly one quadrant (`PI-002`)

### Influence Network (`influence_network_input.json`)

10. All `relationships[].source` / `target` (or `edges[].from` / `to`) reference valid node IDs (`IN-001`)
11. `influence_score` between 0 and 10 (`IN-002`)

### Salience Model (`salience_model_input.json`)

12. `power`, `legitimacy`, `urgency` ∈ {High, Medium, Low} (`SM-001`)
13. `category` matches P/L/U lookup if provided (`SM-003`)

### Stakeholder Map (`stakeholder_map_input.json`)

14. `ring` ∈ {inner, middle, outer} (`MAP-001`)
15. `sector` from defined list (`MAP-002`)
16. Relationship source/target exist in map stakeholders[] (`MAP-004`)

Optional validation:

```bash
python stakeholder_diagram_generator/cli.py projects/<project-slug>/inputs/stakeholder_input.json --validate-only
```

---

## Quick Reference Card

| File | Root key | Minimum content | Derived from |
|------|----------|-----------------|--------------|
| `stakeholder_register_input.json` | `stakeholder_register` | 5 stakeholders | specifications.json |
| `power_interest_input.json` | `power_interest_matrix` | 4 quadrants populated | register |
| `influence_network_input.json` | `influence_network` | 3+ nodes, 2+ relationships | register |
| `salience_model_input.json` | `salience_model` | 3+ classified stakeholders | register |
| `stakeholder_map_input.json` | `stakeholder_map` | 3+ nodes on rings | register |
| **`stakeholder_input.json`** | **all five keys** | **merge of above** | **assembly step** |

---

## After Generating Input

Run the generator using the **MAIN** file only:

```bash
# Validate all sections
python stakeholder_diagram_generator/cli.py \
  projects/<project-slug>/inputs/stakeholder_input.json \
  --validate-only

# Individual diagram outputs
python stakeholder_diagram_generator/cli.py \
  projects/<project-slug>/inputs/stakeholder_input.json \
  -o projects/<project-slug>/output

# Combined 5-page Visio package
python stakeholder_diagram_generator/cli.py \
  projects/<project-slug>/inputs/stakeholder_input.json \
  -o projects/<project-slug>/output --combined
```

To regenerate a **single** diagram after editing one split file: update that split file, re-merge into `stakeholder_input.json`, then re-run CLI.

---

## Integration Notes

- Primary upstream: `specifications.json → stakeholders[]`
- RACI matrix: separate — [raci_matrix_generator/PROMPT.md](../raci_matrix_generator/PROMPT.md) uses stakeholder roles as columns
- Project charter embeds register + matrix — [project_charter_generator/PROMPT.md](../project_charter_generator/PROMPT.md)
- Full rendering specs: [stakeholder-diagram-generator-SKILL.md](../stakeholder-diagram-generator-SKILL.md) §2–§6

---

## Copy-Ready Agent Prompt

```
You are a stakeholder management specialist. Your task is to generate SIX JSON input files for the Stakeholder Diagram Generator.

Read the project data from specifications.json or the project description below. Follow the schemas in stakeholder_diagram_generator/PROMPT.md and stakeholder-diagram-generator-SKILL.md.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Healthcare Platform, Software Development]
**Stakeholders:** [LIST OR REFER TO specifications.json stakeholders[]]
**Diagrams Requested:** [stakeholder_register, power_interest_matrix, influence_network, salience_model, stakeholder_map]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables — YOU MUST CREATE ALL SIX FILES

Write each file to disk under projects/<project-slug>/inputs/:

1. stakeholder_register_input.json     ← CREATE FIRST (source of truth)
2. power_interest_input.json           ← derived from register
3. influence_network_input.json        ← nodes + relationships
4. salience_model_input.json           ← P/L/U classification
5. stakeholder_map_input.json          ← rings + sectors + relationships
6. stakeholder_input.json              ← MAIN: merge of files 1–5

## Workflow

1. Map specifications.json stakeholders[] to stakeholder_register_input.json (role → title, add needs/status)
2. Derive power_interest_input.json quadrants from register power × interest
3. Derive salience_model_input.json from register power, legitimacy, urgency
4. Build influence_network_input.json with nodes (stakeholder_id = register id) and relationships
5. Build stakeholder_map_input.json with rings from engagement strategy and sectors by function
6. Merge all five into stakeholder_input.json (main CLI input)
7. Validate cross-file ID consistency

## Validation Rules

1. Six files written to disk — not just the main file
2. Same stakeholder IDs (S-001, S-002, ...) in all files
3. Register: minimum 5 stakeholders, engagement_strategy "auto" allowed
4. Power-Interest: each stakeholder in exactly one quadrant
5. Salience: valid P/L/U and category per Mitchell-Agle-Wood
6. Influence: influence_score 0–10, valid node references
7. Map: ring inner|middle|outer, valid sector, relationship refs
8. Main file must equal merge of the five split files

## Response Format

For each of the six files:
- Confirm the file path written
- State stakeholder count / node count / relationship count

Return the complete stakeholder_input.json (MAIN) in a single JSON code block as the final artifact.

Now, generate all six stakeholder input JSON files for the project described above.
```
