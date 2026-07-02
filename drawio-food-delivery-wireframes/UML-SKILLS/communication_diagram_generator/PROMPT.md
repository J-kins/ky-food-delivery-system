# Communication Diagram Generator — Agent Prompt

Use this file to generate the input JSON required by the **Communication Diagram Generator**. Any agentic AI working on any project can follow this prompt to produce a valid `communication_diagram_input.json` that renders a UML Communication (Collaboration) Diagram as a fully editable Visio file (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`communication_diagram` is listed** in `specifications.json → diagrams_to_generate`
3. Read [SKILL.md](SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | Description |
|--------|--------|-------------|
| Communication diagram | `.vsdx` | Participant nodes, structural links, numbered messages, system boundary groups, legend |
| Preview (optional) | `.png` | Raster preview when `--preview` flag is used |

## Output File Location

Save the generated input to:

```text
projects/<project-slug>/inputs/communication_diagram_input.json
```

Example: `projects/daatsna-community-data-platform/inputs/communication_diagram_input.json`

---

## Agent Instructions

You are a UML interaction modeling specialist. Your task is to generate a complete `communication_diagram_input.json` file for the Communication Diagram Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json`, the project codebase, or the use case described by the user.
2. Identify the **interaction scenario** to model (one primary workflow per file).
3. Define participants, structural links, and numbered messages.
4. Validate against all rules in the Validation section.
5. Write the file to `projects/<project-slug>/inputs/communication_diagram_input.json`.
6. Return the complete JSON in a single code block and confirm the file path.

If `specifications.json` is missing, gather the system name, interaction scenario, actors/components, and message flow from the user — or infer from README, API routes, or service architecture and list assumptions.

---

## Mapping from specifications.json

`specifications.json` does not contain communication diagram data directly. Derive the diagram from project context:

| specifications.json | communication_diagram_input.json | Notes |
|---------------------|--------------------------------|-------|
| `project.name` | `communication_diagram.system_name` | System or product name |
| `project.description` | `communication_diagram.description` | Brief scenario context |
| `project.version` | `communication_diagram.version` | e.g. `"1.0"` |
| `project.date` | `communication_diagram.date` | `YYYY-MM-DD` |
| `wbs.branches[]` | participants / messages | Level 2 work packages suggest components |
| User-provided use case | `title`, `participants`, `messages` | Primary source for interaction flow |

### Deriving participants from a software project

| Source in codebase | Participant type | Example |
|--------------------|------------------|---------|
| End user / external actor | `actor` | Patient, Admin, Mobile User |
| API gateway / orchestrator | `control` | AppointmentSystem, AuthController |
| Database / persistence | `entity` or `database` | MedicalRecordSystem, UserRepository |
| REST/GraphQL endpoint | `boundary` | PaymentAPI, NotificationAPI |
| Microservice | `service` | AvailabilityService, EmailService |
| External system | `system` | PaymentGateway, SMSProvider |

### Deriving messages from a use case

1. Name the primary user goal (e.g., "Book Appointment").
2. List each object-to-object call in execution order.
3. Assign sequence numbers: top-level steps `1`, `2`, `3`; nested calls `1.1`, `1.1.1`, `1.2`.
4. Mark message type: most calls are `synchronous`; fire-and-forget notifications are `asynchronous`; object instantiation is `creation`.

---

## JSON Schema

Generate a complete JSON file with this structure:

```json
{
  "communication_diagram": {
    "title": "string - Diagram title (e.g., Communication Diagram - Patient Consultation)",
    "system_name": "string - System or product name",
    "version": "string - Version (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",
    "description": "string - Brief description of the interaction scenario",

    "participants": [
      {
        "id": "string - Unique ID (e.g., P1, P2)",
        "name": "string - Display name",
        "class_name": "string - UML class name (PascalCase)",
        "instance_name": "string - Instance name (camelCase)",
        "type": "string - actor | control | entity | boundary | service | database | system",
        "stereotype": "string - e.g., <<actor>>, <<control>>, <<entity>>",
        "x": "number - Optional X position in inches",
        "y": "number - Optional Y position in inches",
        "width": "number - Optional box width (default 2.5-3.0)",
        "height": "number - Optional box height (default 1.2-1.4)",
        "color": "string - Optional hex override",
        "text_color": "string - Optional hex override"
      }
    ],

    "links": [
      {
        "id": "string - Unique ID (e.g., L1)",
        "source": "string - Participant ID",
        "target": "string - Participant ID",
        "type": "string - association | dependency",
        "label": "string - Optional link label",
        "line_style": "string - solid | dashed"
      }
    ],

    "messages": [
      {
        "id": "string - Unique ID (e.g., M1)",
        "from": "string - Source participant ID",
        "to": "string - Target participant ID",
        "sequence": "string - Sequence number (1, 1.1, 1.1.1, 2, etc.)",
        "label": "string - Message name / method call",
        "type": "string - synchronous | asynchronous | creation | return",
        "return_value": "string or null - Optional return type or value",
        "guard": "string or null - Optional condition (e.g., consultation_complete)"
      }
    ],

    "groups": [
      {
        "id": "string - Unique ID (e.g., G1)",
        "name": "string - Group name",
        "label": "string - Optional display label",
        "participants": ["string - List of participant IDs inside boundary"],
        "color": "string - Fill color hex (default #E3F2FD)",
        "border_color": "string - Border color hex (default #1565C0)"
      }
    ],

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "shadow_enabled": true,
      "link_width": 1
    },

    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "participant_spacing": 3.5,
      "vertical_spacing": 3.0,
      "auto_layout": false
    }
  }
}
```

**Note:** Messages accept `"from"` / `"to"` (preferred, matches [examples/sample_input.json](examples/sample_input.json)) or `"source"` / `"target"` (also valid per Pydantic aliases).

---

## Section Guidelines

### Interaction scenario

- Model **one primary workflow** per file (e.g., "Patient Consultation Flow", "User Login Flow", "Data Sync Flow")
- Title format: `"Communication Diagram - <Scenario Name>"`
- Minimum 2 participants, recommended 3–8 for readability

### Participants

- **Minimum 2, maximum 20**
- Every participant needs a unique `id` (e.g., `P1`, `P2`, …)
- Use `ClassName:instanceName` naming convention
- Assign `stereotype` matching `type`:
  - `actor` → `<<actor>>`
  - `control` → `<<control>>`
  - `entity` → `<<entity>>`
  - `boundary` → `<<boundary>>`
  - `service` → `<<service>>`
- External actors sit outside system boundary groups; internal components go inside

### Default participant colors (by type)

| Type | Color | Hex |
|------|-------|-----|
| actor | Green | `#4CAF50` |
| control | Blue | `#1565C0` |
| entity | Dark green | `#2E7D32` |
| boundary | Orange | `#FF9800` |
| service | Purple | `#6A1B9A` |

Omit per-participant `color` unless overriding; the generator applies type defaults from styling.

### Links (structural relationships)

- Connect participants that exchange messages
- Use `association` + `solid` for permanent structural links
- Use `dependency` + `dashed` for temporary or usage relationships
- Every message path should have a corresponding link (directly or transitively)

### Messages

- **Minimum 1, recommended 4–12** for a meaningful flow
- Sequence numbering rules:
  - Top-level: `1`, `2`, `3`
  - Nested under step 1: `1.1`, `1.2`, `1.3`
  - Nested under 1.1: `1.1.1`, `1.1.2`
  - Alternative paths: `1.1a`, `1.1b`
- Every sequence number must be **unique**
- Message types:
  - `synchronous` — caller waits (most API calls, method invocations)
  - `asynchronous` — fire-and-forget (events, notifications)
  - `creation` — creates a new object
  - `return` — explicit return to caller
- Include `return_value` when the response type matters (e.g., `"List<Slot>"`, `"Booking"`)
- Include `guard` for conditional messages (e.g., `"consultation_complete"`, `"payment_approved"`)

### Groups (system boundaries)

- Optional but recommended for software systems
- Wrap internal components; leave external actors outside
- `participants` array lists IDs contained within the boundary
- Default: one group named after the system (e.g., `"Healthcare System"`)

### Layout coordinates

- If `auto_layout: false`, provide `x` and `y` for each participant
- Space participants 3–4 inches apart horizontally
- Actors typically at edges; control/orchestrator at center-top; entities below
- A2 landscape page: usable area roughly 8–50 inches wide, 2–38 inches tall

---

## Validation Rules

Fix every failure before writing the file:

1. All required fields populated — no empty `id`, `label`, or participant names
2. At least **1 participant** and **1 message**
3. All participant IDs unique
4. All link `source` and `target` reference existing participant IDs
5. All message `from` and `to` reference existing participant IDs
6. All sequence numbers **unique** (no duplicates)
7. Sequence format valid: digits separated by dots (e.g., `1`, `1.1`, `2.1.1`)
8. Group `participants[]` entries reference existing participant IDs
9. Message `type` is one of: `synchronous`, `asynchronous`, `creation`, `return`
10. Link `type` is one of: `association`, `dependency`
11. Dates in `YYYY-MM-DD` format
12. JSON is syntactically valid

Optional validation:

```bash
python communication_diagram_generator/cli.py projects/<project-slug>/inputs/communication_diagram_input.json --validate-only
```

---

## Quick Reference Card

| Section | Minimum | Maximum | Key Rule |
|---------|---------|---------|----------|
| Participants | 2 | 20 | Unique IDs; ClassName:instanceName |
| Links | 0 | — | source/target must exist |
| Messages | 1 | — | Unique sequence numbers |
| Groups | 0 | 5 | participants[] must reference valid IDs |
| Nesting depth | — | 4 levels | e.g., 1.1.1.1 |

---

## Message Numbering Example

```text
1: Book Appointment                    (P1 → P2)
  1.1: Check Availability              (P2 → P3)
    1.1.1: Return Available Slots      (P3 → P2)
  1.2: Show Available Slots            (P2 → P1)
  1.3: Select Slot and Book              (P1 → P2)
  1.4: Schedule Consultation           (P2 → P4)
  1.5: Record Booking                  (P2 → P5)
2: Record Consultation                 (P4 → P5)  [guard: consultation_complete]
```

---

## After Generating Input

Run the generator:

```bash
# Render Visio diagram
python communication_diagram_generator/cli.py projects/<project-slug>/inputs/communication_diagram_input.json \
  -o projects/<project-slug>/output/communication_diagram.vsdx

# With PNG preview
python communication_diagram_generator/cli.py projects/<project-slug>/inputs/communication_diagram_input.json \
  -o projects/<project-slug>/output/communication_diagram.vsdx --preview

# Validate only
python communication_diagram_generator/cli.py projects/<project-slug>/inputs/communication_diagram_input.json --validate-only
```

Reference implementation: [examples/sample_input.json](examples/sample_input.json)

---

## Copy-Ready Agent Prompt

```
You are a UML interaction modeling specialist. Your task is to generate a complete communication_diagram_input.json file for the Communication Diagram Generator (Visio .vsdx output).

Read the project data from specifications.json, the codebase, or the interaction scenario described below. Follow the JSON schema in communication_diagram_generator/PROMPT.md exactly. If information is not explicitly provided, infer participants and messages from the system architecture and list assumptions.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**System Name:** [INSERT SYSTEM NAME]
**Interaction Scenario:** [e.g., Patient Consultation Flow, User Registration, Data Sync]
**Scenario Description:** [DESCRIBE WHAT HAPPENS STEP BY STEP]
**Known Actors/Components:** [LIST USERS, SERVICES, DATABASES, APIs]
**External Systems:** [LIST ANY THIRD-PARTY INTEGRATIONS]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables

1. A complete, valid communication_diagram_input.json following the schema in communication_diagram_generator/PROMPT.md
2. Saved to projects/<project-slug>/inputs/communication_diagram_input.json
3. All validation rules satisfied

## Validation Rules

1. At least 2 participants with unique IDs
2. At least 1 message with a unique sequence number
3. Every message from/to references an existing participant ID
4. Every link source/target references an existing participant ID
5. Sequence numbers follow nesting (1, 1.1, 1.1.1, 2, etc.) with no duplicates
6. Actors outside system boundary; internal components grouped inside
7. Links connect all participants that exchange messages
8. Use synchronous for blocking calls, asynchronous for events

## Response Format

Return the complete communication_diagram_input.json in a single JSON code block AND write it to disk at projects/<project-slug>/inputs/communication_diagram_input.json.

Now, generate the communication_diagram_input.json for the interaction scenario described above.
```
