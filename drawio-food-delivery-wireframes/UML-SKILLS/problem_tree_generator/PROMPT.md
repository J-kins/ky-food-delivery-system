# Problem Tree Generator — Agent Prompt

Use this file to generate the input JSON required by the **Problem Tree Generator**. Any agentic AI working on any project can follow this prompt to produce a valid `problem_tree_input.json` that renders a hierarchical Problem Tree diagram as a fully editable Visio file (`.vsdx`).

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`problem_tree` is listed** in `specifications.json → diagrams_to_generate`
3. Read [problem-tree-generator-SKILL.md](../problem-tree-generator-SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | Description |
|--------|--------|-------------|
| Problem tree diagram | `.vsdx` | Four-tier causal tree: Roots → Trunk → Branches → Leaf with directional arrows |

## Output File Location

Save the generated input to:

```text
projects/<project-slug>/inputs/problem_tree_input.json
```

Example: `projects/daatsna-community-data-platform/inputs/problem_tree_input.json`

---

## Agent Instructions

You are a problem analysis specialist. Your task is to generate a complete `problem_tree_input.json` file for the Problem Tree Generator.

### Your workflow

1. Read `projects/<project-slug>/specifications.json` and understand the project's central challenge.
2. Articulate the **core problem** (trunk), **root causes** (bottom), **direct effects** (middle), and **long-term effects** (top).
3. Validate against tier limits and all rules in the Validation section.
4. Write the file to `projects/<project-slug>/inputs/problem_tree_input.json`.
5. Return the complete JSON in a single code block and confirm the file path.

If `specifications.json` is missing, gather the problem statement, causes, and effects from the user — or infer from project description and list assumptions.

---

## Problem Tree Structure

Causal flow is always **bottom-up**:

```text
ROOTS (causes)  →  TRUNK (core problem)  →  BRANCHES (direct effects)  →  LEAF (long-term effects)
```

| Tier | Role | Question to answer |
|------|------|-------------------|
| **Roots** | Underlying causes | *Why does this problem exist?* |
| **Trunk** | Core problem | *What is the central problem?* (exactly 1) |
| **Branches** | Direct effects | *What happens because of this problem?* |
| **Leaf** | Long-term effects | *What are the ultimate consequences if unsolved?* |

---

## Mapping from specifications.json

`specifications.json` has no dedicated problem tree section. Derive content from project context:

| specifications.json | problem_tree_input.json | Notes |
|---------------------|-------------------------|-------|
| `project.name` | `problem_tree.project_name` | Full project name |
| `project.version` | `problem_tree.version` | e.g. `"1.0"` |
| `project.date` | `problem_tree.date` | `YYYY-MM-DD` |
| `project.description` | `core_problem.statement` | Reframe as the gap/problem being solved |
| `vision.statement` | `leaf[]` statements | Invert — what persists without the project |
| `objectives[]` | `branches[]` | What the project directly enables/fixes |
| `risks[]` | `roots[]` | Underlying systemic causes and barriers |
| Stakeholder pain points | `roots[]`, `branches[]` | Community/user impact |

### Deriving the core problem (trunk)

Transform the project description into a **problem statement** (not a solution):

- Bad (solution): *"Build an offline SNA platform"*
- Good (problem): *"No integrated, offline-first platform exists that lets communities collect, analyze, and visualize social network data"*

Formula: **"[Gap] — [who is affected] cannot [desired capability] because [context]"**

### Deriving roots from risks and context

Ask "Why?" repeatedly about the core problem:

- Infrastructure gaps → roots
- Policy/regulatory barriers → roots
- Skills, funding, cultural barriers → roots
- Market/business model failures → roots

### Deriving branches from objectives

Each objective's inverse (what fails without the project) becomes a direct effect:

- Objective: *"Empower communities with data skills"* → Branch: *"Communities lack tools to analyze their own network data"*

### Deriving leaf from vision

Long-term societal/systemic consequences if the problem persists for years:

- Exclusion from decision-making
- Policy failures
- Economic invisibility
- Interventions under-performing

---

## JSON Schema

Generate a complete JSON file with this structure:

```json
{
  "problem_tree": {
    "title": "string - Diagram title (e.g., Da'atSNA Problem Tree)",
    "project_name": "string - Full project name",
    "version": "string - Version (e.g., 1.0)",
    "date": "string - Today's date (YYYY-MM-DD)",

    "core_problem": {
      "id": "string - Always TRUNK",
      "statement": "string - Central problem statement (1-3 sentences)",
      "description": "string - Optional elaboration"
    },

    "roots": [
      {
        "id": "string - R1, R2, ... (max 5)",
        "statement": "string - Root cause statement",
        "description": "string - Optional elaboration"
      }
    ],

    "branches": [
      {
        "id": "string - B1, B2, ... (max 4)",
        "statement": "string - Direct effect statement",
        "description": "string - Optional elaboration"
      }
    ],

    "leaf": [
      {
        "id": "string - L1, L2, ... (max 3)",
        "statement": "string - Long-term effect statement",
        "description": "string - Optional elaboration"
      }
    ],

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 10,
      "arrow_style": "curved",
      "shadow_enabled": true,
      "corner_radius": 8
    },

    "layout": {
      "orientation": "top_to_bottom",
      "page_size": "A3",
      "margin": 0.5,
      "node_spacing": 0.4,
      "rank_spacing": 1.2
    }
  }
}
```

---

## Section Guidelines

### Core problem (trunk)

- **Exactly 1** — required
- `id` should be `"TRUNK"`
- State the problem, not the solution
- 1–3 sentences; clear and specific to the project domain
- Should align with `project.description` reframed as a gap

### Roots (causes)

- **Minimum 3, maximum 5**
- IDs: `R1`, `R2`, `R3`, `R4`, `R5`
- Each statement describes an underlying cause (not a symptom)
- Cover diverse cause types: technical, economic, political, social, organizational
- No empty statements

### Branches (direct effects)

- **Minimum 2, maximum 4**
- IDs: `B1`, `B2`, `B3`, `B4`
- Immediate consequences of the core problem
- Who is directly harmed or what directly fails?
- Map to stakeholder groups where relevant

### Leaf (long-term effects)

- **Minimum 2, maximum 3**
- IDs: `L1`, `L2`, `L3`
- Ultimate systemic consequences if the problem persists
- Think 5–10 year horizon
- Often policy, equity, economic, or institutional outcomes

### Statement writing rules

- Each `statement` is a complete sentence or concise phrase
- Be specific to the project domain (avoid generic platitudes)
- Avoid duplicating the same idea across tiers
- Causes ≠ effects — roots explain *why*; branches/leaf explain *so what*

---

## Tier Limits (enforced)

| Tier | Min (recommended) | Max (hard limit) | IDs |
|------|-------------------|------------------|-----|
| Core problem | 1 | 1 | `TRUNK` |
| Roots | 3 | **5** | `R1`–`R5` |
| Branches | 2 | **4** | `B1`–`B4` |
| Leaf | 2 | **3** | `L1`–`L3` |

Exceeding maximum counts raises `TooManyNodesError` (PT-003/004/005).

---

## Validation Rules

Fix every failure before writing the file:

1. `core_problem.statement` populated — not empty
2. `core_problem.id` = `"TRUNK"` (recommended)
3. Roots: **≤ 5** items; Branches: **≤ 4**; Leaf: **≤ 3**
4. All node IDs unique within the diagram
5. Every `statement` non-empty
6. Recommended minimums: ≥ 3 roots, ≥ 2 branches, ≥ 2 leaf nodes
7. Dates in `YYYY-MM-DD` format
8. JSON is syntactically valid

Optional validation:

```bash
python problem_tree_generator/cli.py projects/<project-slug>/inputs/problem_tree_input.json --validate-only
```

---

## Quick Reference Card

| Tier | Color (auto) | Role |
|------|--------------|------|
| Roots | Red `#EF9A9A` | Causes |
| Trunk | Orange `#FFCC80` | Core problem |
| Branches | Blue `#90CAF9` | Direct effects |
| Leaf | Green `#A5D6A7` | Long-term effects |

Arrow direction: **Roots → Trunk → Branches → Leaf**

---

## After Generating Input

Run the generator:

```bash
# Render Visio problem tree
python problem_tree_generator/cli.py projects/<project-slug>/inputs/problem_tree_input.json \
  -o projects/<project-slug>/output/problem_tree.vsdx

# With theme override
python problem_tree_generator/cli.py projects/<project-slug>/inputs/problem_tree_input.json \
  -o projects/<project-slug>/output/problem_tree.vsdx --theme corporate_green

# Validate only
python problem_tree_generator/cli.py projects/<project-slug>/inputs/problem_tree_input.json --validate-only
```

Reference implementation: [examples/sample_input.json](examples/sample_input.json)

---

## Integration Notes

- Embedded in [project-charter-generator-SKILL.md](../project-charter-generator-SKILL.md) as the problem analysis diagram.
- Complements [objective tree](../prompt_skill_generator_SKILL.md) / logical framework approaches — problem tree focuses on causality, not objectives.
- Pair with [stakeholder-diagram-generator-SKILL.md](../stakeholder-diagram-generator-SKILL.md) — stakeholders affected appear in branches and leaf.

---

## Copy-Ready Agent Prompt

```
You are a problem analysis specialist. Your task is to generate a complete problem_tree_input.json file for the Problem Tree Generator (Visio .vsdx output).

Read the project data from specifications.json or the project description below. Follow the JSON schema in problem_tree_generator/PROMPT.md exactly. If information is not explicitly provided, derive causes and effects from the project context and list assumptions.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Project Type:** [e.g., Software Development, Healthcare, Social Enterprise]
**Project Description:** [WHAT THE PROJECT ADDRESSES]
**Central Problem:** [THE GAP OR PROBLEM BEING SOLVED — NOT THE SOLUTION]
**Known Causes:** [LIST UNDERLYING CAUSES OR BARRIERS]
**Direct Effects:** [LIST IMMEDIATE CONSEQUENCES OF THE PROBLEM]
**Long-Term Effects:** [LIST SYSTEMIC CONSEQUENCES IF UNSOLVED]

## Source File (if available)

Path: projects/<project-slug>/specifications.json

## Deliverables

1. A complete, valid problem_tree_input.json following the schema in problem_tree_generator/PROMPT.md
2. Saved to projects/<project-slug>/inputs/problem_tree_input.json
3. All validation rules satisfied

## Validation Rules

1. Exactly 1 core_problem with non-empty statement (id: TRUNK)
2. Roots: 3–5 items (max 5 enforced); IDs R1–R5
3. Branches: 2–4 items (max 4 enforced); IDs B1–B4
4. Leaf: 2–3 items (max 3 enforced); IDs L1–L3
5. State the problem in trunk, not the solution
6. Roots = causes (why); Branches/Leaf = effects (so what)
7. All statements non-empty and domain-specific
8. Causal flow: Roots → Trunk → Branches → Leaf

## Response Format

Return the complete problem_tree_input.json in a single JSON code block AND write it to disk at projects/<project-slug>/inputs/problem_tree_input.json.

Now, generate the problem_tree_input.json for the project described above.
```
