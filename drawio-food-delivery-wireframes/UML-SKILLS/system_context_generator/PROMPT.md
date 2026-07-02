# System Context Diagram Generator — Agent Prompt

Use this file to generate the input JSON required by the **System Context Diagram Generator** (Level 0 / C4-style context). Any agentic AI working on any project can follow this prompt to produce a valid `system_context_input.json` that renders a central system with external entities and labeled data flows as a fully editable Visio file (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`system_context` is listed** in `specifications.json → diagrams_to_generate`
3. Read [system-context-diagram-generator-SKILL.md](../system-context-diagram-generator-SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | Description |
|--------|--------|-------------|
| System context diagram | `.vsdx` | Level 0 diagram: central system, external entities, data flows, boundary, legend |

## Output File Location

Save the generated input to:

```text
projects/<project-slug>/inputs/system_context_input.json
```

Example: `projects/daatsna-community-data-platform/inputs/system_context_input.json`

---

## Agent Instructions

You are a solution architect. Your task is to generate a complete `system_context_input.json` file for the System Context Diagram Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json` (especially `project`, `stakeholders`, `vision`, `objectives`).
2. Define the **central system** block (`system`) — name, description, boundary style.
3. Identify **external entities** — users, systems, organizations, regulators (minimum 4, recommended 6–10).
4. Assign each entity a **compass position** around the system box.
5. Define **data flows** per entity — direction, label, data type/format.
6. Set `system_boundary`, `styling`, and `layout`.
7. Validate against all rules in the Validation section.
8. Write the file to `projects/<project-slug>/inputs/system_context_input.json`.
9. Return the complete JSON in a single code block and confirm the file path.

If `specifications.json` is missing, gather system scope and external actors from the user — or infer from project type and list assumptions.

---

## Mapping from specifications.json

There is no dedicated `system_context` section in `specifications.json`. Derive the diagram from project metadata and stakeholders:

| specifications.json | system_context_input.json | Notes |
|-----------------------|----------------------------|-------|
| `project.name` | `system_context.system_name` | Full project/product name |
| `project.name` or short label | `system.name` | Central box title (e.g. "Healthcare Ecosystem") |
| `project.description` | `system_context.description` | Diagram subtitle |
| `project.description` | `system.description` | Central box description |
| `project.version` | `system_context.version` | e.g. `"1.0"` |
| `project.date` | `system_context.date` | `YYYY-MM-DD` |
| `vision.statement` | `system.description` (fallback) | If project description is thin |
| `stakeholders[]` (External) | `external_entities[]` | Organizations, regulators, partners |
| `stakeholders[]` (Internal users) | `external_entities[]` type `user` | Clinical staff, patients as actors |
| — | `external_entities[].data_flows` | **Infer** from domain (see patterns below) |

### Stakeholder → external entity transform

Map stakeholders to context entities when they interact with the system from **outside** the system boundary:

```json
{
  "id": "E1",
  "name": "<stakeholders[].name or organization>",
  "type": "user | system | organization",
  "description": "<stakeholders[].role>: <stakeholders[].expectations>",
  "position": "top-left",
  "data_flows": [
    {
      "direction": "bidirectional",
      "label": "<what data crosses the boundary>",
      "data_type": "JSON"
    }
  ]
}
```

| Stakeholder signal | Entity `type` | Typical `position` |
|--------------------|---------------|-------------------|
| Patient, citizen, end user | `user` | `top`, `top-left` |
| Doctor, nurse, clinical staff | `user` | `left` |
| Ministry, regulator, FDA | `organization` | `bottom-right`, `bottom` |
| Insurance, NHIS, donor | `organization` | `right`, `bottom-right` |
| External HIS, lab, pharmacy system | `system` | `right`, `bottom-left`, `bottom` |
| Payment gateway, API partner | `system` | `bottom` |

Use entity IDs `E1`, `E2`, … `E10`. Central system ID is always `SYSTEM`.

### Da'atSNA healthcare pattern (reference)

| ID | Entity | type | position |
|----|--------|------|----------|
| E1 | Patients | user | top-left |
| E2 | Doctors | user | left |
| E3 | Pharmacies | system | bottom-left |
| E4 | Laboratories | system | right |
| E5 | Ministry of Health | organization | bottom-right |
| E6 | Insurance Companies | organization | right |
| E7 | External Systems (HIS) | system | bottom |
| E8 | Payment Gateways | system | bottom |

---

## JSON Schema

Generate a complete JSON file with this structure:

```json
{
  "system_context": {
    "title": "string - Diagram title",
    "system_name": "string - Full project/product name",
    "version": "string - Version (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",
    "description": "string - One-line system purpose",

    "system": {
      "id": "SYSTEM",
      "name": "string - Central box label",
      "description": "string - What the system does",
      "boundary_style": "double_line | single_line"
    },

    "external_entities": [
      {
        "id": "string - E1, E2, ...",
        "name": "string - Entity name",
        "type": "string - user | system | organization",
        "description": "string - Role or purpose",
        "position": "string - compass position (see below)",
        "data_flows": [
          {
            "direction": "string - bidirectional | inbound | outbound",
            "label": "string - Data exchanged (human-readable)",
            "data_type": "string - JSON | XML | HL7 | FHIR | CSV | PDF | EDI | JSON/XML"
          }
        ]
      }
    ],

    "system_boundary": {
      "type": "rectangle",
      "line_style": "dashed",
      "line_width": 2,
      "color": "#1a237e",
      "label": "System Boundary"
    },

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 10,
      "arrow_style": "orthogonal",
      "shadow_enabled": true,
      "corner_radius": 8
    },

    "layout": {
      "orientation": "landscape",
      "page_size": "A3",
      "margin": 0.5,
      "system_box_width": 8.0,
      "system_box_height": 6.0,
      "entity_spacing": 1.5
    }
  }
}
```

---

## Section Guidelines

### Central system (`system`)

- **Required** — missing block raises `SC-002`
- `id` must be `"SYSTEM"`
- `name` is the label inside the central box (can differ from `system_name`)
- `boundary_style`: `"double_line"` (default) or `"single_line"`

### External entities

- **Minimum 1, recommended 6–8** (`SC-003` if empty)
- Unique IDs: `E1`, `E2`, …
- **At least one `data_flows[]` entry per entity** (`SC-005`)
- Spread positions around the compass — avoid stacking more than 2 entities on the same position when possible

### Valid `position` values (`SC-004`)

| Position | Placement |
|----------|-----------|
| `top-left` | Above-left of system box |
| `top` | Above center |
| `top-right` | Above-right |
| `left` | Left center |
| `right` | Right center |
| `bottom-left` | Below-left |
| `bottom` | Below center |
| `bottom-right` | Below-right |

Implemented in `renderers/layout_engine.py` — invalid values default to `right` with a warning.

### Entity types and colors (auto-styled)

| type | Color | Shape cue |
|------|-------|-----------|
| `user` | `#4CAF50` | Person / user |
| `system` | `#2196F3` | External system |
| `organization` | `#FF9800` | Organization / building |

Regulatory bodies use `type: "organization"` with regulatory description (e.g. Ministry of Health).

### Data flows

| direction | Arrow rendering |
|-----------|-----------------|
| `bidirectional` | Arrowheads both ends |
| `inbound` | Entity → System |
| `outbound` | System → Entity |

| data_type | Use when |
|-----------|----------|
| `JSON` | REST APIs, mobile/web payloads |
| `XML` / `JSON/XML` | Legacy or mixed APIs |
| `HL7` / `FHIR` | Healthcare interoperability |
| `CSV` / `PDF` | Reports, exports |
| `EDI` | Insurance / billing |

### Layout defaults

- **A3 landscape** — system box centered at `(page_width - 8) / 2`
- Increase `entity_spacing` (e.g. 2.0) if entities overlap (`SC-009`)
- Optional per-entity overrides: `width`, `height`, `spacing` on entity object

---

## Validation Rules

Fix every failure before writing the file:

1. Root key must be `system_context` (CLI reads `spec["system_context"]`)
2. `system` block present with `id`, `name`, `description`
3. At least **1 external entity**; recommend 6–8
4. All entity IDs unique
5. Each entity has at least one `data_flows[]` entry with `label` and `data_type`
6. `position` is one of the eight compass values
7. `direction` is `bidirectional`, `inbound`, or `outbound`
8. Dates in `YYYY-MM-DD` format
9. JSON is syntactically valid

Optional validation:

```bash
python system_context_generator/cli.py projects/<project-slug>/inputs/system_context_input.json --validate-only
```

> **Note:** `--validate-only` currently exits successfully without deep Pydantic checks until `core/validator.py` is implemented. Apply the rules above manually.

---

## Quick Reference Card

| Section | Minimum | Maximum | Key Rule |
|---------|---------|---------|----------|
| system | 1 block | 1 | id = SYSTEM |
| external_entities | 1 | 12 | Unique E IDs; ≥1 data flow each |
| data_flows per entity | 1 | 3 | label + data_type required |
| position | 8 values | — | Compass placement |
| Page | A3 landscape | — | System centered |

---

## After Generating Input

Run the generator:

```bash
# Render Visio context diagram
python system_context_generator/cli.py \
  projects/<project-slug>/inputs/system_context_input.json \
  -o projects/<project-slug>/output/system_context.vsdx

# With theme override
python system_context_generator/cli.py \
  projects/<project-slug>/inputs/system_context_input.json \
  -o projects/<project-slug>/output/system_context.vsdx \
  --theme corporate_green

# PNG preview (requires Graphviz)
python system_context_generator/cli.py \
  projects/<project-slug>/inputs/system_context_input.json \
  -o projects/<project-slug>/output/system_context.vsdx --preview

# Validate only
python system_context_generator/cli.py \
  projects/<project-slug>/inputs/system_context_input.json --validate-only
```

Reference schema: [system-context-diagram-generator-SKILL.md](../system-context-diagram-generator-SKILL.md) Section 3 (full Da'atSNA healthcare example with 8 entities).

---

## Integration Notes

- **C4 Level 0** — this diagram is the context map; detailed containers/components use [uml-diagram-generator-SKILL.md](../uml-diagram-generator-SKILL.md).
- **Stakeholders** — external actors overlap with [stakeholder_diagram_generator/PROMPT.md](../stakeholder_diagram_generator/PROMPT.md) but serve a different purpose (data flows vs engagement analysis).
- **Communication diagram** — sequence-style interactions in [communication_diagram_generator/PROMPT.md](../communication_diagram_generator/PROMPT.md) complement this static context view.
- **Project charter** — context diagram embedded via [project-charter-generator-SKILL.md](../project-charter-generator-SKILL.md).

---

## Copy-Ready Agent Prompt

```
You are a solution architect. Your task is to generate a complete system_context_input.json file for the System Context Diagram Generator (Level 0, Visio .vsdx output).

Read the project data from specifications.json or the project description below. Follow the JSON schema in system_context_generator/PROMPT.md exactly. If information is not explicitly provided, derive external entities and data flows from project type, stakeholders, and domain conventions.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Healthcare Platform, E-Commerce, Internal Tool]
**System Purpose:** [WHAT THE CENTRAL SYSTEM DOES]
**External Actors:** [USERS, SYSTEMS, ORGANIZATIONS THAT INTERACT WITH IT]
**Key Integrations:** [APIs, DATA FORMATS, THIRD-PARTY SYSTEMS]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables

1. A complete, valid system_context_input.json following the schema in system_context_generator/PROMPT.md
2. Saved to projects/<project-slug>/inputs/system_context_input.json
3. All validation rules satisfied

## Validation Rules

1. Root key: system_context
2. system block with id SYSTEM, name, description
3. At least 4 external entities (recommend 6-8); unique E1, E2, ... IDs
4. Each entity: valid compass position, at least one data_flow with label and data_type
5. data_flow direction: bidirectional, inbound, or outbound
6. Spread entities around the diagram (top, left, right, bottom positions)
7. system_name and dates from project metadata

## Response Format

Return the complete system_context_input.json in a single JSON code block AND write it to disk at projects/<project-slug>/inputs/system_context_input.json.

Now, generate the system_context_input.json for the project described above.
```
