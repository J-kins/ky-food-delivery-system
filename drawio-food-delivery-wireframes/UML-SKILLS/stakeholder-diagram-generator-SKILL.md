---
name: stakeholder-diagram-generator
description: Generate professional Stakeholder artefacts — Stakeholder Register (Visio table + Excel export), Power-Interest Matrix, Influence Network Diagram, Salience Model mapping, and Stakeholder Map — in fully editable Visio format (.vsdx) using Aspose.Diagram for Python. The Stakeholder Register is the foundational source of truth that feeds all downstream stakeholder diagrams.
---

# Stakeholder Diagram Generator

This production-grade skill is engineered to generate a suite of **Stakeholder Management Artifacts** in Microsoft Visio (`.vsdx`) and Excel (`.xlsx`) formats. Leveraging `Aspose.Diagram for Python` and `openpyxl`, it provides an automated pipeline for turning structured JSON specifications into accurate governance maps, registers, matrices, influence networks, and salience models.

## Table of Contents
1. **Overview**
   - 1.1 Purpose of this Skill
   - 1.2 Core Output Specifications
   - 1.3 Environment Setup & Dependencies
   - 1.4 Project Folder Structure
   - 1.5 Component Relationship Diagram
2. **Stakeholder Register** (Source of Truth)
   - 2.1 Definition and Purpose
   - 2.2 Field Descriptions
   - 2.3 ASCII Blueprint
   - 2.4 Input Specification (JSON Schema)
   - 2.5 Implementation Code (Visio + Excel + CSV)
   - 2.6 Engagement Strategy Auto-Classification
   - 2.7 Validation Rules
   - 2.8 Output Formats
3. **Power-Interest Matrix**
   - 3.1 Definition and Purpose
   - 3.2 ASCII Blueprint
   - 3.3 Input Specification
   - 3.4 Data Integration (from Stakeholder Register)
   - 3.5 Implementation Code
   - 3.6 Styling Details
   - 3.7 Validation Rules
4. **Influence Network Diagram**
   - 4.1 Definition and Purpose
   - 4.2 ASCII Blueprint
   - 4.3 Input Specification
   - 4.4 Relationship Types
   - 4.5 Node Categories
   - 4.6 Implementation Code
   - 4.7 Layout Algorithm
   - 4.8 Influence Score Calculation
   - 4.9 Validation Rules
5. **Salience Model**
   - 5.1 Definition and Purpose
   - 5.2 The 7 Stakeholder Categories
   - 5.3 ASCII Blueprint
   - 5.4 The Salience Venn Diagram
   - 5.5 Category Mapping Logic
   - 5.6 Input Specification
   - 5.7 Category Color Palette
   - 5.8 Implementation Code
   - 5.9 Validation Rules
6. **Stakeholder Map**
   - 6.1 Definition and Purpose
   - 6.2 ASCII Blueprint
   - 6.3 Input Specification
   - 6.4 Proximity Rings
   - 6.5 Stakeholder Sectors
   - 6.6 Relationship Types
   - 6.7 Implementation Code
   - 6.8 Visual Styling
   - 6.9 Validation Rules
7. **Integration** (with Project Charter and sibling skills)
8. **Complete Input Package** (`example_complete.json`)
9. **Output Directory Structure**
10. **Error Handling**
11. **CLI Interface**
12. **Usage Examples**
13. **Quality Checklist**
14. **Testing Strategy**
15. **Summary: All Stakeholder Components**

> **Note:** The **RACI Matrix** is a separate skill — see [raci-matrix-diagram-generator-SKILL.md](raci-matrix-diagram-generator-SKILL.md). It consumes stakeholder roles from the Register but is not part of this generator.

---

## 1. Overview

Stakeholder management is a critical pillar of project management. It involves identifying all individuals, groups, or organizations that may affect or be affected by a project, analyzing their expectations and impact, and developing appropriate management strategies for effectively engaging them in project decisions and execution.

### 1.1 Purpose of this Skill
This generator automates the creation of visual and tabular stakeholder management tools. Manual creation of these artifacts in Visio or PowerPoint is time-consuming, prone to alignment errors, and difficult to keep in sync as stakeholder dynamics evolve over the project lifecycle.

By using a JSON-based specification, the generator guarantees:
- **Mathematical Precision**: Layout algorithms ensure zero overlap and perfect alignment.
- **Single Source of Truth**: The Stakeholder Register feeds data to all downstream artifacts.
- **Automated Analysis**: Automatic classification using models like Mitchell, Agle & Wood (1997).
- **CI/CD Integration**: Project documentation can be version-controlled alongside code.

The approach implemented here strictly follows the PMBOK® Guide (Project Management Institute) standards for stakeholder analysis. It integrates qualitative classification techniques (Power/Interest grids) with multi-dimensional models (Salience model: Power, Legitimacy, Urgency) to provide a holistic view of the stakeholder landscape.

### 1.2 Core Output Specifications

This skill generates **five stakeholder artefacts** (RACI is excluded — separate skill):

| # | Artefact | Primary Output | Secondary Output |
|---|----------|----------------|------------------|
| 1 | Stakeholder Register | `register.vsdx` | `register.xlsx`, `register.csv` |
| 2 | Power-Interest Matrix | `power_interest.vsdx` | `power_interest.xlsx`, `power_interest.png` |
| 3 | Influence Network Diagram | `influence.vsdx` | `influence.png` |
| 4 | Salience Model | `salience.vsdx` | `salience.png` |
| 5 | Stakeholder Map | `stakeholder_map.vsdx` | `stakeholder_map.png` |
| — | **Combined package** | `stakeholder_analysis_package.vsdx` | All five as Visio pages |

Each output guarantees:
1. **Precise layout** — auto-fitted to A2 landscape page dimensions.
2. **Single source of truth** — Register data feeds all downstream diagrams.
3. **Auto-classification** — engagement strategy, salience category, quadrant placement.
4. **Fully editable** — corporate-themed Microsoft Visio shapes (`.vsdx`).

### 1.3 Environment Setup & Dependencies

#### Python Requirements
```text
python >= 3.10
aspose-diagram-python >= 24.0.0
python-dotenv >= 1.0.0
pyyaml >= 6.0
pillow >= 10.0.0
typing-extensions >= 4.0.0
pydantic >= 2.0.0
openpyxl >= 3.1.0
pandas >= 2.0.0
```

#### System Dependencies
**Java Runtime Environment (JRE) 8+** — required for Aspose.Diagram (JPype).

#### Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Unix/macOS
pip install -r stakeholder_diagram_generator/requirements.txt
```

#### Environment Variables (`.env`)
```env
ASPOSE_DIAGRAM_LICENSE_PATH=/path/to/license.lic
OUTPUT_DIR=./output
LOG_LEVEL=INFO
DEFAULT_COLOR_THEME=enterprise_blue
DEFAULT_FONT_FAMILY=Arial
DEFAULT_FONT_SIZE=9
```

### 1.4 Project Folder Structure

```text
stakeholder_diagram_generator/
├── README.md
├── skill.md                          # Copy of this SKILL file
├── requirements.txt
├── .env.example
├── .gitignore
├── cli.py
│
├── core/
│   ├── __init__.py
│   ├── diagram_builder.py            # Main orchestration (StakeholderDiagramBuilder)
│   ├── validator.py                  # validate_and_enrich()
│   ├── errors.py                     # Custom exceptions (SH-001 … SH-020)
│   └── models.py                     # Pydantic StakeholderSpec models
│
├── diagrams/
│   ├── __init__.py
│   ├── register_builder.py           # Stakeholder Register
│   ├── power_interest_builder.py     # Power-Interest Matrix
│   ├── influence_network_builder.py  # Influence Network Diagram
│   ├── salience_builder.py           # Salience Model
│   └── stakeholder_map_builder.py    # Stakeholder Map
│
├── renderers/
│   ├── __init__.py
│   ├── aspose_renderer.py            # Aspose.Diagram rendering
│   ├── dot_generator.py              # Graphviz DOT (PNG previews)
│   ├── excel_exporter.py             # Excel export
│   └── layout_engine.py              # Layout calculations
│
├── calculators/
│   ├── __init__.py
│   ├── stakeholder_calculator.py     # Register summary stats
│   ├── power_interest_calculator.py  # Quadrant assignment
│   ├── influence_calculator.py       # Influence score calculation
│   └── salience_calculator.py        # Mitchell, Agle & Wood classification
│
├── stylers/                          # (planned) Theme and diagram-specific styling
├── utils/                            # (planned) File, logging, geometry, data utilities
├── templates/                        # (optional) .vstx templates per diagram type
├── config/                           # (planned) settings.py, color_palettes.py
│
├── examples/
│   ├── sample_input.json
│   ├── example_register.json
│   ├── example_power_interest.json
│   ├── example_influence.json
│   ├── example_salience.json
│   ├── example_stakeholder_map.json
│   └── example_complete.json         # All five diagrams in one payload
│
├── tests/
│   ├── test_validator.py
│   ├── test_calculators.py
│   ├── test_renderers.py
│   └── test_integration.py
│
├── output/                           # Generated output (gitignored)
│   ├── register/
│   ├── power_interest/
│   ├── influence/
│   ├── salience/
│   ├── stakeholder_map/
│   ├── complete/
│   └── logs/
│
└── docs/
    ├── user_guide.md
    ├── developer_guide.md
    └── images/                       # Preview screenshots
```

### 1.5 Component Relationship Diagram

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                           STAKEHOLDER DIAGRAM GENERATOR                                       │
│                                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                         INPUT (JSON — single or split files)                            │ │
│  │  stakeholder_register │ power_interest_matrix │ influence_network │ salience_model     │ │
│  │  stakeholder_map │ styling │ layout                                                  │ │
│  └────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                         │                                                    │
│                                         ▼                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                    CORE ORCHESTRATION (core/diagram_builder.py)                         │ │
│  │   Validator → Calculators → Stylers → Layout Engine → Aspose Renderer                │ │
│  └────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                         │                                                    │
│         ┌───────────────┬───────────────┼───────────────┬───────────────┐                   │
│         ▼               ▼               ▼               ▼               ▼                   │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐              │
│  │  Register  │ │Power-Int.  │ │ Influence  │ │  Salience  │ │    Map     │              │
│  │  Builder   │ │  Builder   │ │  Builder   │ │  Builder   │ │  Builder   │              │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘ └────────────┘              │
│         │               │               │               │               │                   │
│         ▼               ▼               ▼               ▼               ▼                   │
│  register.vsdx   power_interest   influence.vsdx  salience.vsdx  stakeholder_map.vsdx    │
│  register.xlsx   .vsdx + .xlsx    + .png          + .png         + .png                   │
│                                                                                              │
│  Combined: output/complete/stakeholder_analysis_package.vsdx (5 pages)                        │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Data flow (within this skill):**
```text
stakeholder_register.stakeholders[]
    ├──► power_interest_matrix.quadrants (auto from power × interest)
    ├──► influence_network.nodes (from register + relationships[])
    ├──► salience_model.stakeholders (from power, legitimacy, urgency)
    └──► stakeholder_map.stakeholders (from ring + sector + relationships)
```

**Sibling skills (separate generators):**
- [raci-matrix-diagram-generator-SKILL.md](raci-matrix-diagram-generator-SKILL.md) — task × role accountability (uses stakeholder roles, not generated here)
- [project-charter-generator-SKILL.md](project-charter-generator-SKILL.md) — embeds stakeholder section from Register

---

## 2. Stakeholder Register

The **Stakeholder Register** is the foundational project management artefact that identifies, characterises, and classifies all individuals, groups, and organisations that may affect or be affected by the project. It is the **single source of truth** from which the Power-Interest Matrix, Influence Network Diagram, Salience Model, and Stakeholder Map are all derived.

> **Data Flow:** `stakeholder_input.json` → Stakeholder Register (Visio + Excel) → Power-Interest Matrix → Influence Network → Salience Model → Stakeholder Map

### 2.1 Definition and Purpose
| Purpose | Description |
|---------|-------------|
| Identification | Catalogues every stakeholder (internal + external) with full contact details |
| Classification | Assigns Power, Interest, Influence, Legitimacy, and Urgency ratings |
| Strategy | Prescribes the correct engagement strategy per stakeholder |
| Data Source | Feeds all downstream diagrams automatically — change one record, update all diagrams |
| Communication | Documents preferred communication channels and frequencies |

### 2.2 Field Descriptions
| Field | Type | Required | Valid Values | Description |
|-------|------|----------|--------------|-------------|
| `id` | string | Yes | `S-001`, `S-002`, … | Unique stakeholder identifier |
| `name` | string | Yes | Any | Full name |
| `title` | string | Yes | Any | Job title or role |
| `organization` | string | Yes | Any | Department or organisation |
| `category` | enum | Yes | `Internal`, `External` | Organisational relationship |
| `type` | enum | No | `Primary`, `Secondary` | Level of direct involvement |
| `power` | enum | Yes | `High`, `Medium`, `Low` | Decision-making authority |
| `interest` | enum | Yes | `High`, `Medium`, `Low` | Degree of concern in project outcomes |
| `influence` | enum | Yes | `High`, `Medium`, `Low` | Informal ability to affect decisions |
| `legitimacy` | enum | Yes | `High`, `Medium`, `Low` | Appropriateness of their involvement (Salience Model) |
| `urgency` | enum | Yes | `High`, `Medium`, `Low` | Time-sensitivity of their claim (Salience Model) |
| `expectations` | string | Yes | Any | What they expect from the project |
| `needs` | string | Yes | Any | What they need to work effectively |
| `engagement_strategy` | enum | Yes | `Manage Closely`, `Keep Satisfied`, `Keep Informed`, `Monitor` | PMI quadrant strategy |
| `communication_preference` | string | No | Any | Preferred channel and frequency |
| `contact` | string | No | Any | Email, phone, or address |
| `status` | enum | Yes | `Active`, `Inactive`, `Blocked` | Current engagement status |
| `notes` | string | No | Any | Additional context |

Note: The data validation layer guarantees that all enum fields strictly conform to the acceptable vocabulary before rendering begins. This avoids structural corruptions in downstream systems.

### 2.3 ASCII Blueprint — Stakeholder Register Table
```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                  STAKEHOLDER REGISTER                                                                                        │
│                                             Da'atSNA Community Data Platform                                                                                 │
│                                             Version 1.0  |  2026-06-17                                                                                      │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                                              │
│  ┌──────┬───────────────────┬──────────────────┬───────────────┬──────────┬───────┬──────────┬───────────┬────────────┬─────────┬──────────────────────────────────┬────────────────────┐  │
│  │  ID  │  NAME             │  TITLE/ROLE       │  ORGANIZATION │ CATEGORY │ POWER │ INTEREST │ INFLUENCE │ LEGITIMACY │ URGENCY │  EXPECTATIONS / NEEDS             │  ENGAGEMENT        │  │
│  ├──────┼───────────────────┼──────────────────┼───────────────┼──────────┼───────┼──────────┼───────────┼────────────┼─────────┼──────────────────────────────────┼────────────────────┤  │
│  │      │                   │                  │               │          │       │          │           │            │         │                                  │                    │  │
│  │S-001 │ Dr. James Okello  │ Project Sponsor   │ Min. of Health│ Internal │ High  │ High     │ High      │ High       │ High    │ Project success, policy alignment │ ● Manage Closely   │  │
│  │      │                   │                  │               │          │       │          │           │            │         │ Regular status, risk visibility   │                    │  │
│  ├──────┼───────────────────┼──────────────────┼───────────────┼──────────┼───────┼──────────┼───────────┼────────────┼─────────┼──────────────────────────────────┼────────────────────┤  │
│  │S-002 │ Dr. Sarah Nambi   │ Policy Maker      │ Min. of Health│ Internal │ High  │ High     │ High      │ High       │ Medium  │ Regulatory compliance, policy    │ ● Manage Closely   │  │
│  │      │                   │                  │               │          │       │          │           │            │         │ implementation, briefs            │                    │  │
│  ├──────┼───────────────────┼──────────────────┼───────────────┼──────────┼───────┼──────────┼───────────┼────────────┼─────────┼──────────────────────────────────┼────────────────────┤  │
│  │S-006 │ NHIS              │ Insurance Company │ NHIS          │ External │ High  │ Low      │ Medium    │ Medium     │ Low     │ Cost control, claims processing  │ ◐ Keep Satisfied   │  │
│  │      │                   │                  │               │          │       │          │           │            │         │ Compliance reports, SLA docs      │                    │  │
│  ├──────┴───────────────────┴──────────────────┴───────────────┴──────────┴───────┴──────────┴───────────┴────────────┴─────────┴──────────────────────────────────┴────────────────────┤  │
│  │  SUMMARY  │  Total: 3  │  Internal: 2  │  External: 1  │  Manage Closely: 2  │  Keep Satisfied: 1  │  Keep Informed: 0  │  Monitor: 0                                                  │  │
│  └───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                                                                              │
│  Engagement Strategies:                                                                                                                                      │
│  ● Manage Closely  = High Power + High Interest  (Q1 Key Players)                                                                                            │
│  ◐ Keep Satisfied  = High Power + Low Interest   (Q2 Keep Satisfied)                                                                                         │
│  ● Keep Informed   = Low Power + High Interest   (Q3 Keep Informed)                                                                                          │
│  ○ Monitor         = Low Power + Low Interest    (Q4 Monitor)                                                                                                │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.4 Input Specification (JSON Schema)
```json
{
  "stakeholder_register": {
    "title": "Stakeholder Register",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    "stakeholders": [
      {
        "id": "S-001",
        "name": "Dr. James Okello",
        "title": "Project Sponsor",
        "organization": "Ministry of Health",
        "category": "Internal",
        "type": "Primary",
        "power": "High",
        "interest": "High",
        "influence": "High",
        "legitimacy": "High",
        "urgency": "High",
        "expectations": "Project success, policy alignment, national impact",
        "needs": "Regular status updates, risk visibility",
        "engagement_strategy": "Manage Closely",
        "communication_preference": "Monthly steering committee meetings",
        "contact": "james.okello@health.go.ug",
        "status": "Active",
        "notes": "Key decision maker for funding"
      },
      {
        "id": "S-002",
        "name": "Dr. Sarah Nambi",
        "title": "Policy Maker",
        "organization": "Ministry of Health",
        "category": "Internal",
        "type": "Primary",
        "power": "High",
        "interest": "High",
        "influence": "High",
        "legitimacy": "High",
        "urgency": "Medium",
        "expectations": "Regulatory compliance, policy implementation",
        "needs": "Compliance reports, policy briefs",
        "engagement_strategy": "Manage Closely",
        "communication_preference": "Quarterly briefings",
        "contact": "sarah.nambi@health.go.ug",
        "status": "Active",
        "notes": "Approves all regulatory documents"
      },
      {
        "id": "S-003",
        "name": "John Smith",
        "title": "Project Manager",
        "organization": "PMO",
        "category": "Internal",
        "type": "Primary",
        "power": "Medium",
        "interest": "High",
        "influence": "Medium",
        "legitimacy": "High",
        "urgency": "High",
        "expectations": "On-time delivery, budget management",
        "needs": "Clear requirements, executive support",
        "engagement_strategy": "Keep Informed",
        "communication_preference": "Weekly stand-ups",
        "contact": "john.smith@health.go.ug",
        "status": "Active",
        "notes": "Day-to-day project execution"
      },
      {
        "id": "S-004",
        "name": "Dr. Alice Nambi",
        "title": "Clinical Lead",
        "organization": "Mulago Hospital",
        "category": "Internal",
        "type": "Primary",
        "power": "Low",
        "interest": "High",
        "influence": "Medium",
        "legitimacy": "High",
        "urgency": "High",
        "expectations": "Usability, patient care improvement",
        "needs": "Clinical workflow input sessions",
        "engagement_strategy": "Keep Informed",
        "communication_preference": "Bi-weekly focus groups",
        "contact": "alice.nambi@mulago.ug",
        "status": "Active",
        "notes": "Represents end-user clinical staff"
      },
      {
        "id": "S-005",
        "name": "Emily Davis",
        "title": "Lead Developer",
        "organization": "Development Team",
        "category": "Internal",
        "type": "Primary",
        "power": "Low",
        "interest": "Medium",
        "influence": "Low",
        "legitimacy": "Medium",
        "urgency": "Medium",
        "expectations": "Technical clarity, stable requirements",
        "needs": "Architecture decisions, sprint priorities",
        "engagement_strategy": "Monitor",
        "communication_preference": "Daily scrum",
        "contact": "emily.davis@dev.health.ug",
        "status": "Active",
        "notes": "Technical delivery lead"
      },
      {
        "id": "S-006",
        "name": "NHIS",
        "title": "Insurance Company",
        "organization": "NHIS",
        "category": "External",
        "type": "Secondary",
        "power": "High",
        "interest": "Low",
        "influence": "Medium",
        "legitimacy": "Medium",
        "urgency": "Low",
        "expectations": "Cost control, claims processing integration",
        "needs": "Compliance reports, SLA documentation",
        "engagement_strategy": "Keep Satisfied",
        "communication_preference": "Quarterly updates",
        "contact": "partnerships@nhis.ug",
        "status": "Active",
        "notes": "Billing integration stakeholder"
      }
    ]
  }
}
```

> **Validator note:** `engagement_strategy` may be set to `"auto"` — the validator in `core/validator.py` derives the correct strategy from `power` × `interest` before rendering. Medium power is treated as Low for quadrant placement when interest is High (→ Keep Informed) or Low (→ Monitor).

### 2.5 Implementation Code (Visio + Excel + CSV)

Implementation lives in `diagrams/register_builder.py` with Excel export via `renderers/excel_exporter.py`.

```python
# diagrams/register_builder.py
from aspose.diagram import Diagram, SaveFileFormat
from typing import Dict, List
import pandas as pd

class StakeholderRegisterBuilder:
    """Builds Stakeholder Register in Visio table + Excel/CSV formats."""

    HEADER_FILL = "#1a237e"
    HEADER_TEXT = "#FFFFFF"
    ROW_EVEN = "#F5F5F5"
    ROW_ODD = "#FFFFFF"

    def __init__(self, config: Dict):
        self.config = config
        self.data = config["stakeholder_register"]
        self.stakeholders = self.data["stakeholders"]
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()

    def _setup_page(self) -> None:
        self.page.page_sheet.page_props.page_width = 59.4   # A2 landscape
        self.page.page_sheet.page_props.page_height = 42.0

    def build_visio_table(self) -> None:
        """Render tabular register with header row, alternating fills, summary footer."""
        # 1. Title block (project_name, version, date)
        # 2. Column headers: ID, Name, Title, Org, Category, Power, Interest, ...
        # 3. One row per stakeholder with engagement strategy badge
        # 4. Summary footer: counts by category and engagement strategy
        pass

    def export_excel(self, output_path: str) -> None:
        """Export register to .xlsx for further analysis."""
        rows = [{
            "ID": s["id"], "Name": s["name"], "Title": s["title"],
            "Organization": s["organization"], "Category": s["category"],
            "Power": s["power"], "Interest": s["interest"],
            "Influence": s["influence"], "Legitimacy": s["legitimacy"],
            "Urgency": s["urgency"], "Expectations": s["expectations"],
            "Needs": s["needs"], "Engagement": s["engagement_strategy"],
            "Communication": s.get("communication_preference", ""),
            "Contact": s.get("contact", ""), "Status": s.get("status", "Active"),
            "Notes": s.get("notes", "")
        } for s in self.stakeholders]
        df = pd.DataFrame(rows)
        df.to_excel(output_path, sheet_name="Stakeholder Register", index=False)

    def export_csv(self, output_path: str) -> None:
        """Export register to CSV for data integration."""
        self.export_excel(output_path.replace(".csv", ".xlsx"))  # or direct CSV via df.to_csv

    def save(self, output_path: str) -> None:
        self.build_visio_table()
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

### 2.6 Engagement Strategy Auto-Classification
When `engagement_strategy` is set to `"auto"` or is missing, `core/validator.py` derives the correct strategy:

```text
                        HIGH INTEREST    LOW/MEDIUM INTEREST
  HIGH POWER    →       Manage Closely   Keep Satisfied
  LOW/MEDIUM    →       Keep Informed    Monitor
```

This matches PMBOK quadrant mapping used by the Power-Interest Matrix builder.

### 2.7 Validation Rules

| Rule | Code | Description | Severity |
|------|------|-------------|----------|
| Unique ID | `SR-001` | Each stakeholder `id` must be unique | Error |
| Required fields | `SR-002` | All required fields populated | Error |
| Valid category | `SR-003` | `category` ∈ {Internal, External} | Error |
| Valid enums | `SR-004` | power/interest/influence/legitimacy/urgency ∈ {High, Medium, Low} | Error |
| Valid status | `SR-005` | status ∈ {Active, Inactive, Blocked} | Error |
| Engagement match | `SR-006` | engagement_strategy matches power×interest (unless auto) | Warning |
| Minimum count | `SR-007` | At least 1 stakeholder required | Error |

### 2.8 Output Formats

| Format | Path | Description |
|--------|------|-------------|
| Visio table | `output/register/register.vsdx` | Editable register with summary footer |
| Excel | `output/register/register.xlsx` | Full data export for analysis |
| CSV | `output/register/register.csv` | Integration with PM tools |
| PNG preview | `output/register/register.png` | Optional via `--preview` |

---
## 3. Power-Interest Matrix

The Power-Interest Matrix is a foundational stakeholder management tool that maps stakeholders based on their level of power (ability to influence the project) and interest (level of concern or involvement). It helps determine appropriate engagement strategies for each stakeholder group. This matrix is dynamically generated from data in the Stakeholder Register.

### 3.1 Definition and Purpose
The Power-Interest Matrix is rendered as a 2x2 grid with the following quadrants:

| Quadrant | Power | Interest | Color | Engagement Strategy |
|----------|-------|----------|-------|---------------------|
| Q1: Key Players | High | High | #E53935 (Red) | Manage Closely |
| Q2: Keep Satisfied | High | Low | #FF9800 (Orange) | Keep Satisfied |
| Q3: Keep Informed | Low | High | #FFC107 (Amber) | Keep Informed |
| Q4: Monitor | Low | Low | #4CAF50 (Green) | Monitor |

These quadrant mappings directly correlate to the engagement protocols established in the PMI project management framework, ensuring alignment with global standards.

### 3.2 ASCII Blueprint
```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                      POWER-INTEREST MATRIX - STAKEHOLDER MAPPING                                                              │
│                                                 Da'atSNA Community Data Platform                                                                             │
│                                                 Version 1.0  |  2026-06-17                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                                                 │
│                                                     POWER (High → Low)                                                                                        │
│                                                   ▲                                                                                                            │
│                                                   │                                                                                                            │
│                              ┌────────────────────┼────────────────────────────────────────────────────────────────────────────┐                               │
│                              │                    │                                                                            │                               │
│                              │                    │                                                                            │                               │
│                              │  HIGH POWER /      │  HIGH POWER /                                                             │                               │
│                              │  HIGH INTEREST     │  LOW INTEREST                                                              │                               │
│                              │  (KEY PLAYERS)     │  (KEEP SATISFIED)                                                         │                               │
│                              │                    │                                                                            │                               │
│                              │  ┌───────────────┐ │  ┌────────────────────────────────────────────────────────────────────┐   │                               │
│                              │  │ S-001 Sponsor │ │  │ S-006 NHIS (Insurance Company)                                  │   │                               │
│                              │  │ S-002 Policy  │ │  │ S-007 Board of Directors                                        │   │                               │
│                              │  │   Maker       │ │  │ S-008 Government Agencies                                      │   │                               │
│                              │  │ S-003 PMO     │ │  │                                                                  │   │                               │
│                              │  └───────────────┘ │  └────────────────────────────────────────────────────────────────────┘   │                               │
│                              │                    │                                                                            │                               │
│                              │  STRATEGY:         │  STRATEGY:                                                                 │                               │
│                              │  • Regular         │  • Regular updates                                                        │                               │
│                              │    meetings        │  • Annual reports                                                         │                               │
│                              │  • Detailed        │  • High-level briefings                                                   │                               │
│                              │    reporting       │  • Issue-based engagement                                                 │                               │
│                              │                    │                                                                            │                               │
│                              ├────────────────────┼────────────────────────────────────────────────────────────────────────────┤                               │
│                              │                    │                                                                            │                               │
│                              │  LOW POWER /       │  LOW POWER /                                                              │                               │
│                              │  HIGH INTEREST     │  LOW INTEREST                                                             │                               │
│                              │  (KEEP INFORMED)   │  (MONITOR)                                                               │                               │
│                              │                    │                                                                            │                               │
│                              │  ┌───────────────┐ │  ┌────────────────────────────────────────────────────────────────────┐   │                               │
│                              │  │ S-004 Clinical│ │  │ S-009 General Public                                             │   │                               │
│                              │  │   Lead        │ │  │ S-010 Media (Health Journalists)                                 │   │                               │
│                              │  │ S-005 Dev     │ │  │ S-011 Medical Suppliers                                           │   │                               │
│                              │  │   Lead        │ │  │ S-012 Local Community Leaders                                    │   │                               │
│                              │  └───────────────┘ │  └────────────────────────────────────────────────────────────────────┘   │                               │
│                              │                    │                                                                            │                               │
│                              │  STRATEGY:         │  STRATEGY:                                                                 │                               │
│                              │  • Newsletters     │  • Public notices                                                         │                               │
│                              │  • Focus groups    │  • Annual reports                                                         │                               │
│                              │  • Surveys         │  • Press releases                                                         │                               │
│                              │  • User groups     │  • Social media                                                           │                               │
│                              │                    │                                                                            │                               │
│                              └────────────────────┼────────────────────────────────────────────────────────────────────────────┘                               │
│                                                   │                                                                                                            │
│                                                   ▼                                                                                                            │
│                                              LOW POWER                                                                                                        │
│                                                                                                                                                                 │
│  ◄─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────► │
│      LOW INTEREST                                                                                          HIGH INTEREST                                       │
│                                                                                                                                                                 │
│  Legend:  Engagement Strategies:  ● Manage Closely (High Power/High Interest)  ● Keep Satisfied (High Power/Low Interest)                                     │
│  ● Keep Informed (Low Power/High Interest)  ● Monitor (Low Power/Low Interest)                                                                                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Note on layout algorithm: The geometry calculations ensure that bounding boxes for stakeholder items strictly wrap text without breaching quadrant perimeters.

### 3.3 Input Specification
```json
{
  "power_interest_matrix": {
    "title": "Power-Interest Matrix - Stakeholder Mapping",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    
    "quadrants": {
      "key_players": {
        "id": "Q1",
        "label": "Key Players",
        "power": "High",
        "interest": "High",
        "color": "#E53935",
        "text_color": "#FFFFFF",
        "strategy": "Manage Closely",
        "engagement_activities": [
          "Regular meetings (monthly)",
          "Detailed reporting",
          "Executive briefings",
          "Steering committee participation"
        ],
        "stakeholders": ["S-001", "S-002", "S-003"]
      },
      "keep_satisfied": {
        "id": "Q2",
        "label": "Keep Satisfied",
        "power": "High",
        "interest": "Low",
        "color": "#FF9800",
        "text_color": "#FFFFFF",
        "strategy": "Keep Satisfied",
        "engagement_activities": [
          "Regular updates (quarterly)",
          "Annual reports",
          "High-level briefings",
          "Issue-based engagement"
        ],
        "stakeholders": ["S-006", "S-007", "S-008"]
      },
      "keep_informed": {
        "id": "Q3",
        "label": "Keep Informed",
        "power": "Low",
        "interest": "High",
        "color": "#FFC107",
        "text_color": "#333333",
        "strategy": "Keep Informed",
        "engagement_activities": [
          "Newsletters (monthly)",
          "Focus groups",
          "Surveys",
          "User group meetings"
        ],
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
        "engagement_activities": [
          "Public notices",
          "Annual reports",
          "Press releases",
          "Social media updates"
        ],
        "stakeholders": ["S-009", "S-010", "S-011", "S-012"]
      }
    },
    
    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "grid_line_width": 2,
      "quadrant_padding": 0.3,
      "stakeholder_box_height": 0.6,
      "shadow_enabled": true
    },
    
    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5
    }
  }
}
```

### 3.4 Data Integration (from Stakeholder Register)
```python
def generate_matrix_from_register(stakeholders: List[Dict]) -> Dict:
    """Generate Power-Interest Matrix from stakeholder data."""
    matrix = {
        'key_players': [],
        'keep_satisfied': [],
        'keep_informed': [],
        'monitor': []
    }
    
    for stakeholder in stakeholders:
        power = stakeholder.get('power', 'Low')
        interest = stakeholder.get('interest', 'Low')
        
        if power == 'High' and interest == 'High':
            matrix['key_players'].append(stakeholder['id'])
        elif power == 'High' and interest == 'Low':
            matrix['keep_satisfied'].append(stakeholder['id'])
        elif power == 'Low' and interest == 'High':
            matrix['keep_informed'].append(stakeholder['id'])
        else:
            matrix['monitor'].append(stakeholder['id'])
    
    return matrix
```

### 3.5 Implementation Code
```python
from aspose.diagram import Diagram, Page, Shape, SaveFileFormat
from aspose.diagram.shapes import Rectangle, Connector
from aspose.diagram.styling import Fill, Line, TextStyle
from typing import List, Dict, Optional

class PowerInterestMatrixBuilder:
    """Builds Power-Interest Matrix in Visio format."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._calculate_positions()
    
    def _setup_page(self) -> None:
        """Configure page size and orientation."""
        pass
    
    def save(self, output_path: str) -> None:
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

### 3.6 Styling Details

| Property | Value | Description |
|----------|-------|-------------|
| Quadrant corner radius | 2pt | Slightly rounded |
| Grid line width | 2pt | `#333333` |
| Quadrant padding | 0.3in | Internal margin |
| Stakeholder box height | 0.6in | Per-stakeholder label |
| Header fill | `#1a237e` | Dark navy |
| Shadow | enabled | Drop shadow on stakeholder boxes |

### 3.7 Validation Rules

| Rule | Code | Description | Severity |
|------|------|-------------|----------|
| Stakeholder mapping | `PI-001` | Each stakeholder ID must exist in Register | Error |
| Single quadrant | `PI-002` | Each stakeholder in exactly one quadrant | Error |
| Strategy match | `PI-003` | Quadrant strategy matches power×interest | Warning |
| Empty quadrant | `PI-004` | Quadrant has zero stakeholders | Warning |
| Valid colors | `PI-005` | Hex color codes on all quadrants | Error |

---
## 4. Influence Network Diagram

The Influence Network Diagram (also known as a Stakeholder Network Map or Influence Diagram) visually represents the relationships, influence flows, and communication channels between stakeholders. Unlike the Power-Interest Matrix (which shows individual stakeholder positions), the Influence Network Diagram shows how stakeholders relate to and influence each other. This is critical for understanding power dynamics, communication planning, conflict resolution, and change management.

### 4.1 Definition and Purpose

| Element | Description | Visual Representation |
|---------|-------------|----------------------|
| Stakeholder Nodes | Individual stakeholders or groups | Rounded rectangles with names/roles |
| Influence Arrows | Direction of influence or communication | Arrows with varying thickness |
| Relationship Strength | Strength of influence | Line thickness (1-3pt) |
| Relationship Type | Type of relationship | Color-coded lines |
| Stakeholder Groups | Coalitions or alliances | Grouped with dashed boundaries |
| Influence Score | Quantitative influence level | Numbers or heat indicators |

### 4.2 ASCII Blueprint

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                     INFLUENCE NETWORK DIAGRAM - STAKEHOLDER RELATIONSHIPS                                                           │
│                                                Da'atSNA Community Data Platform                                                                                  │
│                                                Version 1.0  |  2026-06-17                                                                                       │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                                                  │
│                                                    ┌──────────────────────────────────┐                                                                         │
│                                                    │    Ministry of Health (MoH)     │                                                                         │
│                                                    │    Dr. Sarah Nambi              │                                                                         │
│                                                    │    High Influence (9.5)         │                                                                         │
│                                                    └────────────────┬─────────────────┘                                                                         │
│                                                                     │                                                                                            │
│                                                                     │  STRONG (3pt)                                                                              │
│                                                                     │  "Policy Direction"                                                                        │
│                                                                     ▼                                                                                            │
│                    ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐                │
│                    │                                                                                                                             │                │
│                    │                                                                                                                             │                │
│                    │                                 ┌──────────────────────────────────┐                                                     │                │
│                    │                                 │    Project Sponsor              │                                                     │                │
│                    │                                 │    Dr. James Okello             │                                                     │                │
│                    │                                 │    High Influence (8.5)         │                                                     │                │
│                    │                                 └────────────────┬─────────────────┘                                                     │                │
│                    │                                                  │                                                                         │                │
│                    │                     ┌────────────────────────────┼────────────────────────────┐                                            │                │
│                    │                     │                            │                            │                                            │                │
│                    │                     │                            │                            │                                            │                │
│                    │                     ▼                            ▼                            ▼                                            │                │
│                    │   ┌──────────────────────────────────┐  ┌──────────────────────────────────┐  ┌──────────────────────────────────┐        │                │
│                    │   │    PMO / Project Manager        │  │    Board of Directors           │  │    Steering Committee            │        │                │
│                    │   │    John Smith                   │  │    (Health Board)                │  │    (Cross-functional)            │        │                │
│                    │   │    Medium Influence (6.5)       │  │    High Influence (8.0)          │  │    Medium Influence (6.0)        │        │                │
│                    │   └────────────────┬─────────────────┘  └──────────────────────────────────┘  └──────────────────────────────────┘        │                │
│                    │                    │                                                                                                      │                │
│                    │   ┌────────────────┼────────────────┐                                                                                     │                │
│                    │   │                │                │                                                                                     │                │
│                    │   │    STRONG      │    MEDIUM     │                                                                                     │                │
│                    │   ▼                ▼               ▼                                                                                     │                │
│                    │  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐                 │                │
│                    │  │                                   DEVELOPMENT TEAM                                                   │                 │                │
│                    │  │  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐                              │                 │                │
│                    │  │  │  Dev Lead         │  │  QA Lead          │  │  UX Lead          │                              │                 │                │
│                    │  │  │  Emily Davis      │  │  David Wilson     │  │  Tom Adams        │                              │                 │                │
│                    │  │  │  Med Influence    │  │  Med Influence    │  │  Low Influence    │                              │                 │                │
│                    │  │  │  (5.5)            │  │  (5.0)            │  │  (3.5)            │                              │                 │                │
│                    │  │  └────────────────────┘  └────────────────────┘  └────────────────────┘                              │                 │                │
│                    │  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘                 │                │
│                    │                                                    │                                                                         │                │
│                    │                                                    │  MEDIUM (2pt)                                                           │                │
│                    │                                                    │  "Reporting"                                                             │                │
│                    │                                                    ▼                                                                         │                │
│                    │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐                    │                │
│                    │   │  ┌────────────────────────────┐  ┌────────────────────────────────┐  ┌────────────────────────────┐                    │                │
│                    │   │  │  Clinical Lead             │  │  Lead BA                    │  │  Patient Reps              │                    │                │
│                    │   │  │  Dr. Alice Nambi           │  │  Sarah Johnson              │  │  (Community Voices)        │                    │                │
│                    │   │  │  Med Influence (5.0)       │  │  Med Influence (5.5)        │  │  Low Influence (3.0)       │                    │                │
│                    │   │  └────────────────────────────┘  └────────────────────────────────┘  └────────────────────────────┘                    │                │
│                    │   └──────────────────────────────────────────────────────────────────────────────────────────────────┘                    │                │
│                    │                                                                                                                             │                │
│                    └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘                │
│                                                                                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  LEGEND                                                                                                                                                     │ │
│  │  ═══════                                                                                                                                                     │ │
│  │  Node Types:    ● High Influence (7-10)  ● Medium Influence (4-6)  ● Low Influence (1-3)                                                                     │ │
│  │  Relationships: ─── STRONG (3pt)  ─── MEDIUM (2pt)  ─── WEAK (1pt)                                                                                          │ │
│  │  Colors:        ■ Executive/Leadership  ■ PMO/Management  ■ Clinical  ■ Technical  ■ External                                                               │ │
│  │                                                                                                                                                              │ │
│  │  INFLUENCE SCORE KEY:                                                                                                                                        │ │
│  │  10 = Highest Influence  │  7-10 = High  │  4-6 = Medium  │  1-3 = Low  │  0 = No Influence                                                                 │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Input Specification

```json
{
  "influence_network": {
    "title": "Influence Network Diagram - Stakeholder Relationships",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",

    "nodes": [
      {
        "id": "N1",
        "stakeholder_id": "S-001",
        "name": "Dr. James Okello",
        "role": "Project Sponsor",
        "organization": "Ministry of Health",
        "influence_score": 8.5,
        "category": "Executive",
        "color": "#1a237e",
        "text_color": "#FFFFFF",
        "x": 15.0,
        "y": 12.0,
        "size": 3.0
      },
      {
        "id": "N2",
        "stakeholder_id": "S-002",
        "name": "Dr. Sarah Nambi",
        "role": "Policy Maker",
        "organization": "Ministry of Health",
        "influence_score": 9.5,
        "category": "Executive",
        "color": "#1a237e",
        "text_color": "#FFFFFF",
        "x": 15.0,
        "y": 4.0,
        "size": 3.5
      },
      {
        "id": "N3",
        "stakeholder_id": "S-003",
        "name": "John Smith",
        "role": "Project Manager",
        "organization": "PMO",
        "influence_score": 6.5,
        "category": "PMO",
        "color": "#1565C0",
        "text_color": "#FFFFFF",
        "x": 8.0,
        "y": 20.0,
        "size": 2.5
      }
    ],

    "relationships": [
      {
        "id": "R1",
        "source": "N2",
        "target": "N1",
        "type": "Formal Authority",
        "strength": "Strong",
        "label": "Policy Direction",
        "color": "#1a237e",
        "bidirectional": false,
        "description": "Sets policy framework for project"
      },
      {
        "id": "R2",
        "source": "N1",
        "target": "N3",
        "type": "Formal Authority",
        "strength": "Strong",
        "label": "Directs",
        "color": "#1a237e",
        "bidirectional": false,
        "description": "Provides project oversight"
      },
      {
        "id": "R3",
        "source": "N3",
        "target": "N4",
        "type": "Collaboration",
        "strength": "Medium",
        "label": "Collaborates",
        "color": "#2E7D32",
        "bidirectional": true,
        "description": "Regular coordination meetings"
      }
    ],

    "groups": [
      {
        "id": "G1",
        "name": "Executive Leadership",
        "color": "#1a237e",
        "opacity": 0.1,
        "nodes": ["N1", "N2"]
      },
      {
        "id": "G2",
        "name": "Project Management",
        "color": "#1565C0",
        "opacity": 0.1,
        "nodes": ["N3"]
      }
    ],

    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "node_radius": 1.5,
      "arrow_style": "curved",
      "shadow_enabled": true
    },

    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "algorithm": "force_directed",
      "node_spacing": 2.0
    }
  }
}
```

> **Note:** The Pydantic model in `core/models.py` uses `edges` as an alias — input may use `relationships[]` (preferred) or `edges[]` with `from`/`to` keys. The builder normalises both forms.

### 4.4 Relationship Types

| Relationship Type | Color | Line Style | Line Width | Symbol | Description |
|-------------------|-------|------------|------------|--------|-------------|
| Formal Authority | #1a237e (Dark Blue) | Solid | 3pt | → | Hierarchical/Reporting |
| Influence/Advice | #E65100 (Orange) | Solid | 2pt | → | Advisory/Influential |
| Collaboration | #2E7D32 (Green) | Dashed | 2pt | ↔ | Collaborative/Shared |
| Communication | #6A1B9A (Purple) | Dotted | 1pt | → | Information flow |
| Conflict/Tension | #C62828 (Red) | Solid | 2pt | ⚡ | Tension/Conflict |
| External Influence | #00838F (Teal) | Solid | 2pt | → | External pressure |

### 4.5 Node Categories

| Category | Color | Shape | Description |
|----------|-------|-------|-------------|
| Executive | #1a237e | Circle | C-suite, high-level decision makers |
| PMO/Management | #1565C0 | Rounded Rectangle | Project management team |
| Clinical | #2E7D32 | Rounded Rectangle | Healthcare providers |
| Technical | #6A1B9A | Rounded Rectangle | Development team |
| External | #00838F | Hexagon | External stakeholders |

### 4.6 Implementation Code

```python
# diagrams/influence_network_builder.py
from aspose.diagram import Diagram, SaveFileFormat
from typing import Dict, List

class InfluenceNetworkBuilder:
    """Builds Influence Network Diagram in Visio format."""

    STRENGTH_WIDTH = {"Strong": 3.0, "Medium": 2.0, "Weak": 1.0}

    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._calculate_positions()

    def _calculate_positions(self) -> None:
        nodes = self.config["influence_network"]["nodes"]
        if any("x" in n for n in nodes):
            self.positions = {n["id"]: (n["x"], n["y"]) for n in nodes}
        else:
            self._force_directed_layout()

    def _force_directed_layout(self) -> None:
        """Spring-repulsion layout when x/y not provided."""
        pass

    def build(self) -> None:
        self.add_title_block()
        self.add_groups()
        for node in self.config["influence_network"]["nodes"]:
            self.add_node(node)
        for rel in self.config["influence_network"].get("relationships", []):
            self.add_relationship(rel)
        self.add_legend()

    def save(self, output_path: str) -> None:
        self.build()
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

### 4.7 Layout Algorithm

When explicit `x`/`y` coordinates are omitted, `renderers/layout_engine.py` applies a **force-directed** algorithm:
- **Repulsion** — Coulomb's law between all node pairs (prevents overlap).
- **Attraction** — Hooke's law along relationship edges (pulls connected nodes together).
- **Iterations** — 100–300 cycles until positions stabilise.
- **Constraints** — nodes clamped within page margins.

### 4.8 Influence Score Calculation

```python
# calculators/influence_calculator.py
def calculate_influence_score(stakeholder: Dict, relationships: List[Dict]) -> float:
    """Calculate influence score (0–10) from role power and relationship graph."""
    power_score = {"High": 8.0, "Medium": 5.0, "Low": 2.0}.get(
        stakeholder.get("power", "Low"), 3.0
    )
    node_id = stakeholder.get("id")
    boost = 0.0
    for rel in relationships:
        if rel.get("source") == node_id:
            boost += 1.0   # outgoing influence
        if rel.get("target") == node_id:
            boost += 1.5   # incoming influence (being influenced by others)
    return min(round(power_score + boost * 0.5, 1), 10.0)
```

| Score Range | Label | Node Size |
|-------------|-------|-----------|
| 7–10 | High Influence | Large (3.0–3.5 in) |
| 4–6 | Medium Influence | Medium (2.5 in) |
| 1–3 | Low Influence | Small (1.5–2.0 in) |

### 4.9 Validation Rules

| Rule | Code | Description | Severity |
|------|------|-------------|----------|
| Valid node IDs | `IN-001` | All relationship source/target IDs exist in nodes[] | Error |
| Influence range | `IN-002` | influence_score between 0 and 10 | Error |
| No orphan nodes | `IN-003` | Warning if node has zero relationships | Warning |
| Circular refs | `IN-004` | One-way cycle detection | Warning |
| Group refs | `IN-005` | Group node IDs must exist | Error |

---
## 5. Salience Model

The Salience Model (developed by Mitchell, Agle, and Wood) is a stakeholder identification and prioritization framework that categorizes stakeholders based on three key attributes: Power (ability to influence), Legitimacy (perceived validity of their claim), and Urgency (time-sensitivity of their claim). Stakeholders are classified into seven categories based on combinations of these attributes, helping project managers understand who truly matters and when.

### 5.1 Definition and Purpose

| Attribute | Definition | Assessment | Visual Indicator |
|-----------|------------|------------|------------------|
| Power | Ability to influence project outcomes | High/Medium/Low | Circle size or position |
| Legitimacy | Perceived validity of stakeholder's claim | High/Medium/Low | Color intensity |
| Urgency | Time-sensitivity of their claim | High/Medium/Low | Border thickness or pattern |

### 5.2 The 7 Stakeholder Categories

| Category | Power | Legitimacy | Urgency | Color | Description | Engagement |
|----------|-------|------------|---------|-------|-------------|------------|
| **Dormant** | ✓ | ✗ | ✗ | #9E9E9E (Grey) | Has power but no legitimacy or urgency | Monitor |
| **Discretionary** | ✗ | ✓ | ✗ | #64B5F6 (Light Blue) | Has legitimacy but no power or urgency | Keep informed |
| **Demanding** | ✗ | ✗ | ✓ | #FFB74D (Amber) | Has urgency but no power or legitimacy | Acknowledge |
| **Dominant** | ✓ | ✓ | ✗ | #1a237e (Dark Blue) | Has power and legitimacy | Manage closely |
| **Dangerous** | ✓ | ✗ | ✓ | #E53935 (Red) | Has power and urgency, no legitimacy | High attention |
| **Dependent** | ✗ | ✓ | ✓ | #FF8A65 (Coral) | Has legitimacy and urgency, no power | Keep informed |
| **Definitive** | ✓ | ✓ | ✓ | #2E7D32 (Green) | Has all three attributes | Top priority |

### 5.3 ASCII Blueprint

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                         SALIENCE MODEL - STAKEHOLDER PRIORITIZATION                                                                     │
│                                                    Da'atSNA Community Data Platform                                                                                    │
│                                                    Version 1.0  |  2026-06-17                                                                                         │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                                                          │
│                                            ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│                                            │                              LEGITIMACY                                                                                │ │
│                                            │                                 ▲                                                                                       │ │
│                                            │                                 │                                                                                       │ │
│                                            │                    ┌────────────┼────────────────────────────────┐                                                      │ │
│                                            │                    │            │                                │                                                      │ │
│                                            │                    │            │  DISCRETIONARY               │                                                      │ │
│                                            │                    │            │  (Legitimate, No Power, No   │                                                      │ │
│                                            │                    │            │   Urgency)                    │                                                      │ │
│                                            │                    │            │  ┌─────────────────────────┐ │                                                      │ │
│                                            │                    │            │  │ Clinical Staff         │ │                                                      │ │
│                                            │                    │            │  │ Patients (General)     │ │                                                      │ │
│                                            │                    │            │  └─────────────────────────┘ │                                                      │ │
│                                            │                    │            │                                │                                                      │ │
│                                            │                    │            │                    DEPENDENT  │                                                      │ │
│                                            │                    │            │                    (Legitimate,│                                                      │ │
│                                            │                    │            │                     Urgent,   │                                                      │ │
│                                            │                    │            │                     No Power) │                                                      │ │
│                                            │                    │            │  ┌─────────────────────────┐ │                                                      │ │
│                                            │                    │            │  │ Patient Reps           │ │                                                      │ │
│                                            │                    │            │  │ Community Leaders      │ │                                                      │ │
│                                            │                    │            │  └─────────────────────────┘ │                                                      │ │
│                                            │                    │            │                                │                                                      │ │
│                                            │                    │            │                    DOMINANT   │                                                      │ │
│                                            │                    │            │                    (Power &   │                                                      │ │
│                                            │                    │            │                     Legitimate│                                                      │ │
│                                            │                    │            │                     No Urgency)│                                                      │ │
│                                            │                    │            │  ┌─────────────────────────┐ │                                                      │ │
│                                            │                    │            │  │ Project Sponsor        │ │                                                      │ │
│                                            │                    │            │  │ MoH Policy Maker       │ │                                                      │ │
│                                            │                    │            │  └─────────────────────────┘ │                                                      │ │
│                                            │                    │            │                                │                                                      │ │
│                                            │                    │            │                    DEFINITIVE │                                                      │ │
│                                            │                    │            │                    (Power,    │                                                      │ │
│                                            │                    │            │                     Legitimate│                                                      │ │
│                                            │                    │            │                     Urgent)   │                                                      │ │
│                                            │                    │            │  ┌─────────────────────────┐ │                                                      │ │
│                                            │                    │            │  │ Project Manager        │ │                                                      │ │
│                                            │                    │            │  │ Steering Committee     │ │                                                      │ │
│                                            │                    │            │  └─────────────────────────┘ │                                                      │ │
│                                            │                    │            │                                │                                                      │ │
│                              DORMANT  ────┼────────────────────┼────────────────────────────────┼──────────────┼───────────┐                              │ │
│                              (Power, No    │                    │            │                                │           │                              │ │
│                              Legitimacy,   │                    │            │                                │           │                              │ │
│                              No Urgency)   │                    │            │                                │           │                              │ │
│                              ┌────────────────────────────────┘            │                                │           │                              │ │
│                              │                                             │                                │           │                              │ │
│                              │                                             │                                │           │                              │ │
│                              │                                             │                                │           │                              │ │
│                              │                                             │                                │           │                              │ │
│                              │                                             │                                │           │                              │ │
│                              │                                             │                                │           │                              │ │
│                              ▼                                             ▼                                ▼           ▼                              │ │
│              ┌─────────────────────────────┐               ┌─────────────────────────────┐   ┌─────────────────────────────────────────────────────┐ │
│              │  DORMANT                    │               │  DEMANDING                  │   │  DANGEROUS                                          │ │
│              │  (Power only)               │               │  (Urgency only)             │   │  (Power + Urgency, No Legitimacy)                  │ │
│              │  ┌─────────────────────────┐│               │  ┌─────────────────────────┐│   │  ┌───────────────────────────────────────────────┐ │ │
│              │  │ Board of Directors      ││               │  │ Media (Breaking News)   ││   │  │ Competitor / Rival Organization               │ │ │
│              │  │ Insurance Companies     ││               │  │ Disgruntled Employee    ││   │  │ Whistleblower                               │ │ │
│              │  └─────────────────────────┘│               │  └─────────────────────────┘│   │  └───────────────────────────────────────────────┘ │ │
│              └─────────────────────────────┘               └─────────────────────────────┘   └─────────────────────────────────────────────────────┘ │
│                                                                                                                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  LEGEND                                                                                                                                                         │ │
│  │  ═══════                                                                                                                                                         │ │
│  │  ● Power (Ability to Influence)    ● Legitimacy (Perceived Validity)    ● Urgency (Time-Sensitivity)                                                             │ │
│  │                                                                                                                                                                  │ │
│  │  STAKEHOLDER CATEGORIES:                                                                                                                                         │ │
│  │  ████████  DEFINITIVE (P+L+U)  Top Priority  │  ████████  DOMINANT (P+L)  Manage Closely          │  ████████  DISCRETIONARY (L)  Keep Informed           │ │
│  │  ████████  DANGEROUS (P+U)    High Attention  │  ████████  DEPENDENT (L+U)  Keep Informed        │  ████████  DORMANT (P)  Monitor                        │ │
│  │  ████████  DEMANDING (U)      Acknowledge                                                                                                                       │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.4 The Salience Venn Diagram (Alternative View)

```text
                    ┌─────────────────────────────────────────────────────────────────────────────┐
                    │                                                                             │
                    │                        POWER                                                │
                    │                        ▲                                                    │
                    │                        │                                                    │
                    │              ┌─────────┼─────────────────────┐                             │
                    │              │         │                     │                             │
                    │              │         │    DORMANT          │                             │
                    │              │         │   (Power only)      │                             │
                    │              │         │   ┌──────────────┐  │                             │
                    │              │         │   │ Board       │  │                             │
                    │              │         │   │ Insurance   │  │                             │
                    │              │         │   └──────────────┘  │                             │
                    │              │         │                     │                             │
                    │              │         │       DOMINANT      │                             │
                    │              │         │      (P + L)        │                             │
                    │              │         │   ┌──────────────┐  │                             │
                    │              │         │   │ Sponsor     │  │                             │
                    │              │         │   │ MoH Policy  │  │                             │
                    │              │         │   └──────────────┘  │                             │
                    │              │         │                     │                             │
                    │              │         │     DEFINITIVE      │                             │
                    │              │         │    (P + L + U)      │                             │
                    │              │         │   ┌──────────────┐  │                             │
                    │              │         │   │ Project Mgr │  │                             │
                    │              │         │   │ Steering    │  │                             │
                    │              │         │   └──────────────┘  │                             │
                    │              │         │                     │                             │
                    │              │         │       DANGEROUS     │                             │
                    │              │         │      (P + U)        │                             │
                    │              │         │   ┌──────────────┐  │                             │
                    │              │         │   │ Competitor   │  │                             │
                    │              │         │   │ Whistleblower│  │                             │
                    │              │         │   └──────────────┘  │                             │
                    │              │         │                     │                             │
                    │   ┌──────────┼─────────┼─────────────────────┼──────────┐                  │
                    │   │          │         │                     │          │                  │
                    │   │  DISCRETIONARY    │                     │  DEMANDING                  │
                    │   │  (L only)        │                     │  (U only)                   │
                    │   │  ┌──────────────┐│                     │  ┌──────────────┐           │
                    │   │  │ Clinical    ││                     │  │ Media       │           │
                    │   │  │ Staff       ││                     │  │ Disgruntled │           │
                    │   │  └──────────────┘│                     │  └──────────────┘           │
                    │   │          │         │                     │          │                  │
                    │   │          │    DEPENDENT                  │          │                  │
                    │   │          │   (L + U)                     │          │                  │
                    │   │          │  ┌──────────────┐            │          │                  │
                    │   │          │  │ Patient Reps │            │          │                  │
                    │   │          │  │ Community    │            │          │                  │
                    │   │          │  └──────────────┘            │          │                  │
                    │   │          │         LEGITIMACY           │          │                  │
                    │   │          │         ◄────────────────────┼──────────┘                  │
                    │   └──────────┼──────────────────────────────┼──────────┘                  │
                    │              │                              │                              │
                    │              │         URGENCY              │                              │
                    │              └──────────────────────────────┘                              │
                    └─────────────────────────────────────────────────────────────────────────────┘
```

### 5.5 Category Mapping Logic

Classification follows Mitchell, Agle & Wood (1997) as implemented in `calculators/salience_calculator.py`. Attributes are evaluated as **High**, **Medium**, or **Low** — only **High** counts as present (✓) for category assignment:

| Category | Power | Legitimacy | Urgency | Engagement |
|----------|-------|------------|---------|------------|
| Definitive | ✓ | ✓ | ✓ | Top Priority |
| Dominant | ✓ | ✓ | ✗ | Manage Closely |
| Dangerous | ✓ | ✗ | ✓ | High Attention |
| Dependent | ✗ | ✓ | ✓ | Keep Informed |
| Discretionary | ✗ | ✓ | ✗ | Keep Informed |
| Demanding | ✗ | ✗ | ✓ | Acknowledge |
| Dormant | ✓ | ✗ | ✗ | Monitor |

```python
# calculators/salience_calculator.py — key lookup
SALIENCE_CATEGORY_MAP = {
    ("High", "High", "High"):   "Definitive",
    ("High", "High", "Low"):    "Dominant",
    ("High", "High", "Medium"): "Dominant",
    ("High", "Low",  "High"):   "Dangerous",
    ("Low",  "High", "High"):   "Dependent",
    ("High", "Low",  "Low"):    "Dormant",
    ("Low",  "High", "Low"):    "Discretionary",
    ("Low",  "Low",  "High"):   "Demanding",
    # ... additional Medium combinations
}
```

When `category` is omitted from input, the builder auto-classifies from register `power`, `legitimacy`, `urgency` fields.

### 5.6 Input Specification

```json
{
  "salience_model": {
    "title": "Salience Model - Stakeholder Prioritization",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    
    "stakeholders": [
      {
        "id": "S-001",
        "name": "Dr. James Okello",
        "role": "Project Sponsor",
        "organization": "Ministry of Health",
        "power": "High",
        "legitimacy": "High",
        "urgency": "Low",
        "category": "Dominant",
        "priority": "High",
        "color": "#1a237e",
        "engagement": "Manage Closely",
        "notes": "Key decision maker for funding"
      },
      {
        "id": "S-003",
        "name": "John Smith",
        "role": "Project Manager",
        "organization": "PMO",
        "power": "High",
        "legitimacy": "High",
        "urgency": "High",
        "category": "Definitive",
        "priority": "Critical",
        "color": "#2E7D32",
        "engagement": "Top Priority",
        "notes": "Day-to-day project execution"
      },
      {
        "id": "S-007",
        "name": "Competitor",
        "role": "Market Rival",
        "organization": "Private Sector",
        "power": "High",
        "legitimacy": "Low",
        "urgency": "High",
        "category": "Dangerous",
        "priority": "High",
        "color": "#E53935",
        "engagement": "High Attention",
        "notes": "Could disrupt market position"
      }
    ],
    
    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "venn_diagram_enabled": true,
      "show_attributes": true,
      "shadow_enabled": true
    },
    
    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "venn_scale": 1.0
    }
  }
}
```

### 5.7 Category Color Palette

| Category | Color Name | Hex Code | Text Color | Symbol | Priority |
|----------|------------|----------|------------|--------|----------|
| Definitive | Green | #2E7D32 | #FFFFFF | ★ | Critical |
| Dominant | Dark Blue | #1a237e | #FFFFFF | ◆ | High |
| Dangerous | Red | #E53935 | #FFFFFF | ⚠️ | High |
| Dependent | Coral | #FF8A65 | #333333 | ● | Medium |
| Discretionary | Light Blue | #64B5F6 | #333333 | ○ | Medium |
| Demanding | Amber | #FFB74D | #333333 | △ | Low |
| Dormant | Grey | #9E9E9E | #333333 | ◇ | Low |

### 5.8 Implementation Code

```python
from aspose.diagram import Diagram, Page, Shape, SaveFileFormat
from aspose.diagram.shapes import Rectangle, Oval, Connector
from aspose.diagram.styling import Fill, Line, TextStyle
from typing import List, Dict, Optional

class SalienceModelBuilder:
    """Builds Salience Model in Visio format."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._categorize_stakeholders()
        self._calculate_positions()
    
    def _setup_page(self) -> None:
        pass
    
    def _setup_styles(self) -> None:
        pass
    
    def _categorize_stakeholders(self) -> None:
        pass
    
    def _calculate_positions(self) -> None:
        pass
    
    def _calculate_venn_positions(self) -> None:
        pass
    
    def save(self, output_path: str) -> None:
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

### 5.9 Validation Rules

| Rule | Code | Description | Severity |
|------|------|-------------|----------|
| Valid attributes | `SM-001` | power/legitimacy/urgency ∈ {High, Medium, Low} | Error |
| Category assignment | `SM-002` | Each stakeholder maps to exactly one category | Error |
| Priority consistency | `SM-003` | Declared category matches computed category | Warning |
| Register linkage | `SM-004` | Stakeholder IDs exist in Register | Error |
| Venn overflow | `SM-005` | >5 names per category region triggers compact mode | Warning |

---
## 6. Stakeholder Map

The Stakeholder Map (also known as a Stakeholder Landscape or Stakeholder Ecosystem Map) is a visual representation that shows ALL stakeholders in relation to the project/organization, their categories, and their interconnections. Unlike the Power-Interest Matrix (which focuses on power/interest), the Influence Network (which focuses on relationships), or the Salience Model (which focuses on attributes), the Stakeholder Map provides a holistic, "big picture" view of the entire stakeholder ecosystem. It answers the question: "Who are all the people and organizations connected to this project, and how do they relate to each other and to us?"

### Key Differences from Other Stakeholder Diagrams:

| Feature | Power-Interest Matrix | Influence Network | Salience Model | **Stakeholder Map** |
|---------|----------------------|-------------------|----------------|---------------------|
| **Primary Focus** | Power + Interest | Relationships & Influence | Power + Legitimacy + Urgency | **Ecosystem Overview** |
| **Structure** | 2x2 Grid | Network/Graph | Venn Diagram/Table | **Radial/Concentric** |
| **Key Elements** | Quadrants | Nodes + Arrows | Attribute Circles | **Rings + Sectors** |
| **Best For** | Engagement Strategy | Communication Planning | Priority Setting | **Strategic Overview** |

### 6.1 Definition and Purpose

| Element | Description | Visual Representation |
|---------|-------------|----------------------|
| Project/System Center | The project at the center | Large circle/box in center |
| Proximity Rings | Distance from project indicates engagement level | Concentric circles (Inner, Middle, Outer) |
| Stakeholder Sectors | Categories of stakeholders | Colored sectors/segments |
| Stakeholder Nodes | Individual stakeholders or groups | Circles/boxes with names |
| Relationships | Connections between stakeholders | Lines/arrows between nodes |
| Group Boundaries | Clusters of related stakeholders | Dashed boundaries |

### 6.2 ASCII Blueprint for Stakeholder Map

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                         STAKEHOLDER MAP - STAKEHOLDER ECOSYSTEM                                                                           │
│                                                    Da'atSNA Community Data Platform                                                                                    │
│                                                    Version 1.0  |  2026-06-17                                                                                         │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                                                          │
│                                                        ┌─────────────────────────────────────┐                                                                         │
│                                                        │          OUTER RING                 │                                                                         │
│                                                        │    (External / Low Engagement)      │                                                                         │
│                                                        │                                     │                                                                         │
│                                                        │          ┌────────────────────┐      │                                                                         │
│                                                        │          │    MIDDLE RING     │      │                                                                         │
│                                                        │          │ (Supporting /     │      │                                                                         │
│                                                        │          │  Medium Engagement)│      │                                                                         │
│                                                        │          │                    │      │                                                                         │
│                       ┌──────────────────────────────┐ │          │  ┌──────────────┐  │      │                                                                         │
│                       │                              │ │          │  │  INNER RING  │  │      │                                                                         │
│                       │  Media / Public              │ │          │  │   (Core /    │  │      │                                                                         │
│                       │  (Journalists, Social Media) │ │          │  │   High       │  │      │                                                                         │
│                       │                              │ │          │  │  Engagement) │  │      │                                                                         │
│                       │                              │ │          │  │              │  │      │                                                                         │
│                       │                              │ │          │  │  ┌──────────┐ │  │      │                                                                         │
│                       │                              │ │          │  │  │ PROJECT  │ │  │      │                                                                         │
│                       │                              │ │          │  │  │ CENTER   │ │  │      │                                                                         │
│   ┌─────────────────────────────────────────────────┼─┼──────────┼──┼──┼──────────┼─┼──┼──────┼────────────────────────────────────────────────────────────────────┐ │
│   │  Suppliers /                                    │ │          │  │  └──────────┘ │  │      │     Competitors / Market                                     │ │
│   │  Vendors                                        │ │          │  │              │  │      │     (Other Health Tech)                                          │ │
│   │  (Equipment,                                    │ │          │  │   ┌────────┐   │  │      │                                                                     │ │
│   │   Software)                                     │ │          │  │   │ Clinical│   │  │      │     ┌────────────────────────────────────────────────────┐       │ │
│   │                                                 │ │          │  │   │  Staff  │   │  │      │     │                                                    │       │ │
│   └─────────────────────────────────────────────────┼─┼──────────┼──┼──┼─────────┼───┼──┼──────┼─────┼────────────────────────────────────────────────────┘       │ │
│                                                     │ │          │  │   └────────┘   │  │      │     │                                                    │       │ │
│                                                     │ │          │  │   ┌────────┐   │  │      │     │  Regulatory Bodies                                 │       │ │
│                                                     │ │          │  │   │Project │   │  │      │     │  (MoH, Uganda FDA, etc.)                           │       │ │
│                                                     │ │          │  │   │Manager │   │  │      │     │                                                    │       │ │
│                                                     │ │          │  │   └────────┘   │  │      │     │                                                    │       │ │
│                                                     │ │          │  │   ┌────────┐   │  │      │     │  ┌────────────────────────────────────────────┐   │       │ │
│                                                     │ │          │  │   │Sponsor │   │  │      │     │  │                                            │   │       │ │
│                                                     │ │          │  │   │        │   │  │      │     │  │  Insurance Companies                       │   │       │ │
│                                                     │ │          │  │   └────────┘   │  │      │     │  │  (NHIS, Private Insurers)                  │   │       │ │
│                                                     │ │          │  │               │  │      │     │  │                                            │   │       │ │
│                                                     │ │          │  │   ┌────────┐   │  │      │     │  └────────────────────────────────────────────┘   │       │ │
│                                                     │ │          │  │   │  BA /  │   │  │      │     │                                                    │       │ │
│   ┌─────────────────────────────────────────────────┼─┼──────────┼──┼──┼─────────┼───┼──┼──────┼─────┼────────────────────────────────────────────────────┐       │ │
│   │  Technology                                    │ │          │  │   │  Dev   │   │  │      │     │  Community /                                       │       │ │
│   │  Partners                                       │ │          │  │   │  Team  │   │  │      │     │  Civil Society                                      │       │ │
│   │  (Cloud, Integration)                           │ │          │  │   └────────┘   │  │      │     │  (Patient Groups, NGOs)                            │       │ │
│   └─────────────────────────────────────────────────┼─┼──────────┼──┼─────────────────┼──┼──────┼─────┼────────────────────────────────────────────────────┘       │ │
│                                                     │ │          │                    │  │      │     │                                                    │       │ │
│                                                     │ │          └────────────────────┘  │      │     │                                                    │       │ │
│                                                     │ │                                 │      │     │                                                    │       │ │
│                                                     │ └─────────────────────────────────┘      │     │                                                    │       │ │
│                                                     │                                          │     │                                                    │       │ │
│                                                     └──────────────────────────────────────────┘     │                                                    │       │ │
│                                                                                                          │                                                  │       │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  LEGEND                                                                                                                                                         │ │
│  │  ═══════                                                                                                                                                         │ │
│  │  Rings:  ● INNER (Core Team, High Engagement)  ● MIDDLE (Supporting, Medium Engagement)  ● OUTER (External, Low Engagement)                                     │ │
│  │  Sectors:  ■ Executive  ■ Management  ■ Clinical  ■ Technical  ■ Regulatory  ■ Financial  ■ External/Community                                                  │ │
│  │  Relationships: ─── Strong  ─── Medium  ─── Weak  ─ - - - - - External Connection                                                                              │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Input Specification

```json
{
  "stakeholder_map": {
    "title": "Stakeholder Map - Stakeholder Ecosystem",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    
    "stakeholders": [
      {
        "id": "S-001",
        "name": "Dr. James Okello",
        "role": "Project Sponsor",
        "organization": "Ministry of Health",
        "ring": "inner",
        "sector": "Executive",
        "engagement_level": "High",
        "color": "#1a237e",
        "text_color": "#FFFFFF",
        "x": 18.0,
        "y": 12.0,
        "radius": 1.2
      },
      {
        "id": "S-002",
        "name": "Dr. Sarah Nambi",
        "role": "Policy Maker",
        "organization": "Ministry of Health",
        "ring": "inner",
        "sector": "Regulatory",
        "engagement_level": "High",
        "color": "#C62828",
        "text_color": "#FFFFFF",
        "x": 14.0,
        "y": 8.0,
        "radius": 1.2
      },
      {
        "id": "S-003",
        "name": "John Smith",
        "role": "Project Manager",
        "organization": "PMO",
        "ring": "inner",
        "sector": "Management",
        "engagement_level": "High",
        "color": "#1565C0",
        "text_color": "#FFFFFF",
        "x": 18.0,
        "y": 18.0,
        "radius": 1.0
      }
    ],
    
    "relationships": [
      {
        "source": "S-001",
        "target": "S-002",
        "type": "Direct Reporting",
        "label": "Reports to",
        "strength": "Strong"
      },
      {
        "source": "S-001",
        "target": "S-003",
        "type": "Direct Reporting",
        "label": "Directs",
        "strength": "Strong"
      }
    ],
    
    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 9,
      "ring_color": "#E3F2FD",
      "ring_stroke": "#1565C0",
      "show_relationship_lines": true,
      "show_sector_labels": true,
      "shadow_enabled": true
    },
    
    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "center_radius": 2.0,
      "inner_radius": 6.0,
      "middle_radius": 10.0,
      "outer_radius": 15.0
    }
  }
}
```

### 6.4 Proximity Rings (Engagement Levels)

| Ring | Distance | Stakeholder Type | Engagement Level | Color |
|------|----------|------------------|------------------|-------|
| Inner | Closest | Core Team, Direct Stakeholders | High | #1a237e |
| Middle | Medium | Supporting, Indirect Stakeholders | Medium | #1565C0 |
| Outer | Furthest | External, Peripheral Stakeholders | Low | #64B5F6 |

### 6.5 Stakeholder Sectors (Categories)

| Sector | Description | Color | Examples |
|--------|-------------|-------|----------|
| Executive | Leadership/Decision Makers | #1a237e | Sponsor, Board |
| Management | Project Management | #1565C0 | PMO, Program Managers |
| Clinical | Healthcare Providers | #2E7D32 | Doctors, Nurses, Clinical Leads |
| Technical | Technology/Development | #6A1B9A | Dev Team, QA, Architects |
| Regulatory | Government/Compliance | #C62828 | MoH, Uganda FDA, Regulators |
| Financial | Funding/Insurance | #FFB300 | Donors, Insurance Companies |
| External/Community | Public/Community | #00838F | Patients, Media, NGOs |

### 6.6 Relationship Types

| Type | Line Style | Color | Line Width | Symbol | Description |
|------|------------|-------|------------|--------|-------------|
| Direct Reporting | Solid | #1a237e | 3pt | → | Hierarchical reporting |
| Collaboration | Dashed | #2E7D32 | 2pt | ↔ | Working together |
| Advisory | Dotted | #FFB300 | 1pt | → | Advisory/consultative |
| External Connection | Dot-Dash | #00838F | 1pt | → | External relationship |
| Conflict/Tension | Solid (Red) | #C62828 | 2pt | ⚡ | Tension or conflict |

| Strength | Line Width | Description |
|----------|------------|-------------|
| Strong | 3pt | Primary relationship |
| Medium | 2pt | Regular coordination |
| Weak | 1pt | Occasional contact |

### 6.7 Implementation Code

```python
from aspose.diagram import Diagram, Page, Shape, SaveFileFormat
from aspose.diagram.shapes import Rectangle, Oval, Connector, Arc
from aspose.diagram.styling import Fill, Line, TextStyle
from typing import List, Dict, Optional
import math

class StakeholderMapBuilder:
    """Builds Stakeholder Map in Visio format."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._calculate_positions()
    
    def _setup_page(self) -> None:
        """Configure page size and orientation."""
        orientation = self.config.get("layout", {}).get("orientation", "landscape")
        page_size = self.config.get("layout", {}).get("page_size", "A2")
        
        if page_size == "A2":
            if orientation == "landscape":
                self.page.page_sheet.page_props.page_width = 59.4
                self.page.page_sheet.page_props.page_height = 42.0
            else:
                self.page.page_sheet.page_props.page_width = 42.0
                self.page.page_sheet.page_props.page_height = 59.4
        else:
            self.page.page_sheet.page_props.page_width = 42.0
            self.page.page_sheet.page_props.page_height = 29.7
        
        self.page_width = self.page.page_sheet.page_props.page_width
        self.page_height = self.page.page_sheet.page_props.page_height
        self.center_x = self.page_width / 2
        self.center_y = (self.page_height / 2) + 0.5
    
    def _setup_styles(self) -> None:
        """Set up global styling defaults."""
        self.font_family = self.config.get("styling", {}).get("font_family", "Arial")
        self.font_size = self.config.get("styling", {}).get("font_size", 9)
        self.shadow_enabled = self.config.get("styling", {}).get("shadow_enabled", True)
        self.show_relationship_lines = self.config.get("styling", {}).get("show_relationship_lines", True)
    
    def _calculate_positions(self) -> None:
        """Calculate positions for stakeholders in the map."""
        # Get layout parameters
        center_radius = self.config.get("layout", {}).get("center_radius", 2.0)
        inner_radius = self.config.get("layout", {}).get("inner_radius", 6.0)
        middle_radius = self.config.get("layout", {}).get("middle_radius", 10.0)
        outer_radius = self.config.get("layout", {}).get("outer_radius", 15.0)
        
        # Store ring radii for reference
        self.ring_radii = {
            "inner": inner_radius,
            "middle": middle_radius,
            "outer": outer_radius
        }
        
        # Get stakeholders
        stakeholders = self.config['stakeholder_map']['stakeholders']
        
        # Group stakeholders by ring
        rings = {"inner": [], "middle": [], "outer": []}
        for stakeholder in stakeholders:
            ring = stakeholder.get('ring', 'outer')
            rings[ring].append(stakeholder)
        
        # Calculate positions within each ring
        self.stakeholder_positions = {}
        
        for ring, ring_stakeholders in rings.items():
            if not ring_stakeholders:
                continue
            
            radius = self.ring_radii[ring]
            n = len(ring_stakeholders)
            
            # Distribute stakeholders evenly around the circle
            for i, stakeholder in enumerate(ring_stakeholders):
                # Use specified position if provided
                if 'x' in stakeholder and 'y' in stakeholder:
                    self.stakeholder_positions[stakeholder['id']] = {
                        'x': stakeholder['x'],
                        'y': stakeholder['y']
                    }
                    continue
                
                # Calculate position on ring
                angle = (i / n) * 2 * math.pi - math.pi / 2
                x = self.center_x + radius * math.cos(angle)
                y = self.center_y + radius * math.sin(angle)
                
                self.stakeholder_positions[stakeholder['id']] = {
                    'x': x,
                    'y': y
                }
    
    def add_title_block(self) -> None:
        """Add title block at top of diagram."""
        pass
    
    def add_rings(self) -> None:
        """Add concentric rings for proximity levels."""
        pass
    
    def add_sectors(self) -> None:
        """Add sector wedges for stakeholder categories."""
        pass
    
    def add_center(self) -> None:
        """Add the project center node."""
        pass
    
    def add_stakeholders(self) -> None:
        """Add stakeholder nodes in appropriate positions."""
        pass
    
    def add_relationships(self) -> None:
        """Add relationship lines between stakeholders."""
        pass
    
    def add_legend(self) -> None:
        """Add legend explaining rings, sectors, and relationship types."""
        pass
    
    def save(self, output_path: str) -> None:
        """Save diagram to .vsdx file."""
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

### 6.8 Visual Styling

| Element | Property | Value |
|---------|----------|-------|
| Project center | Shape | Circle, radius 2.0in, fill `#1a237e`, text white |
| Inner ring | Stroke | `#1565C0`, fill `#E3F2FD` at 30% opacity |
| Middle ring | Stroke | `#1565C0`, fill `#BBDEFB` at 20% opacity |
| Outer ring | Stroke | `#64B5F6`, fill `#E3F2FD` at 10% opacity |
| Stakeholder node | Shape | Circle, radius from input (0.8–1.2in) |
| Sector labels | Font | 9pt bold, sector color |
| Legend | Position | Bottom of page, full width |

Ring assignment from Register engagement strategy:

| engagement_strategy | Default ring |
|---------------------|--------------|
| Manage Closely | inner |
| Keep Satisfied | middle |
| Keep Informed | middle |
| Monitor | outer |

### 6.9 Validation Rules

| Rule | Code | Description | Severity |
|------|------|-------------|----------|
| Valid ring | `MAP-001` | ring ∈ {inner, middle, outer} | Error |
| Valid sector | `MAP-002` | sector ∈ defined sector list (§6.5) | Error |
| Position bounds | `MAP-003` | x/y within page margins | Warning |
| Relationship refs | `MAP-004` | source/target exist in stakeholders[] | Error |
| Register linkage | `MAP-005` | stakeholder IDs match Register | Error |
| Duplicate IDs | `MAP-006` | Unique stakeholder IDs | Error |

---
## 7. Integration

### 7.1 Within This Skill

All five diagrams share a single JSON payload (`example_complete.json`) or split input files. The recommended generation order:

```text
1. Stakeholder Register     ← author first (source of truth)
2. Power-Interest Matrix     ← auto from power × interest
3. Salience Model            ← auto from power, legitimacy, urgency
4. Influence Network         ← nodes from register + manual relationships
5. Stakeholder Map           ← rings/sectors from register + relationships
```

### 7.2 Project Charter Integration

This module is a sub-component of [project-charter-generator-SKILL.md](project-charter-generator-SKILL.md). The charter embeds:
- Stakeholder Register table (from `stakeholders[]`)
- Power-Interest Matrix page
- Optional influence/salience/map pages via `diagrams.stakeholder_*` keys

Map `specifications.json → stakeholders[]` directly into `stakeholder_register.stakeholders[]`.

### 7.3 Sibling Skills (Not Generated Here)

| Skill | Relationship |
|-------|--------------|
| [raci-matrix-diagram-generator-SKILL.md](raci-matrix-diagram-generator-SKILL.md) | Uses stakeholder **roles** as RACI columns — separate generator |
| [risk-matrix-diagram-generator-SKILL.md](risk-matrix-diagram-generator-SKILL.md) | Risk owners reference stakeholder names |
| [resource-allocation-matrix-generator-SKILL.md](resource-allocation-matrix-generator-SKILL.md) | Resources align with internal stakeholders |

### 7.4 Cross-Diagram Consistency Rules

1. Stakeholder IDs (`S-001`, …) must be identical across all five diagrams.
2. Power/Interest in Register must match Power-Interest quadrant placement.
3. Salience `category` must match computed value from P/L/U attributes.
4. Influence `stakeholder_id` on nodes must reference Register IDs.
5. Stakeholder Map `ring` should align with Register `engagement_strategy`.

---

## 8. Complete Input Package

A single JSON file containing all five diagram sections:

```json
{
  "stakeholder_register": { "...": "see §2.4" },
  "power_interest_matrix": { "...": "see §3.3 — quadrants optional (auto-generated)" },
  "influence_network": { "...": "see §4.3" },
  "salience_model": { "...": "see §5.6" },
  "stakeholder_map": { "...": "see §6.3" }
}
```

Save to: `projects/<project-slug>/inputs/stakeholder_input.json`

Reference implementation: `stakeholder_diagram_generator/examples/sample_input.json`

Minimum viable payload — Register only (other diagrams auto-generated if omitted):

```json
{
  "stakeholder_register": {
    "title": "Stakeholder Register",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "stakeholders": [ "... at least 3 stakeholders ..." ]
  }
}
```

---

## 9. Output Directory Structure

```text
output/
├── stakeholder_analysis_package.vsdx    # ALL diagrams — 5 Visio pages (with --combined)
│                                         # Pages: Register → Power-Interest → Influence → Salience → Map
│
├── register/
│   ├── register.vsdx
│   ├── register.xlsx
│   ├── register.csv
│   └── register.png
│
├── power_interest/
│   ├── power_interest.vsdx
│   ├── power_interest.xlsx
│   └── power_interest.png
│
├── influence/
│   ├── influence.vsdx
│   └── influence.png
│
├── salience/
│   ├── salience.vsdx
│   └── salience.png
│
├── stakeholder_map/
│   ├── stakeholder_map.vsdx
│   └── stakeholder_map.png
│
├── complete/
│   └── stakeholder_analysis_package.vsdx
│
└── logs/
    └── generation.log
```

Alternative flat layout (individual numbered files):

```text
output/individual/
├── 01_stakeholder_register.vsdx
├── 01_stakeholder_register.xlsx
├── 02_power_interest_matrix.vsdx
├── 02_power_interest_matrix.xlsx
├── 03_influence_network.vsdx
├── 04_salience_model.vsdx
└── 05_stakeholder_map.vsdx
```

---

## 10. Error Handling

| Code | Name | Component | Description | Resolution |
|------|------|-----------|-------------|------------|
| `SH-001` | InvalidInput | Core | JSON fails Pydantic schema | Validate against §2–§6 schemas |
| `SH-002` | NoRegister | Register | stakeholders[] empty | Add at least 1 stakeholder |
| `SR-001` | DuplicateID | Register | Duplicate stakeholder id | Assign unique S-00N IDs |
| `SR-002` | MissingRequiredField | Register | Required field empty | Populate all required fields |
| `SR-003` | InvalidCategory | Register | category not Internal/External | Fix category value |
| `SR-004` | InvalidEnum | Register | Invalid power/interest/etc. | Use High/Medium/Low |
| `SR-006` | EngagementMismatch | Register | Strategy ≠ power×interest | Set auto or fix strategy |
| `PI-001` | UnknownStakeholder | Matrix | ID not in Register | Sync IDs |
| `PI-002` | DuplicateQuadrant | Matrix | Stakeholder in two quadrants | One quadrant only |
| `PI-004` | EmptyQuadrant | Matrix | Quadrant has zero entries | Warning — add stakeholders |
| `IN-001` | InvalidNodeRef | Network | Relationship references missing node | Fix source/target |
| `IN-002` | InvalidScore | Network | influence_score outside 0–10 | Correct score |
| `SM-001` | InvalidAttribute | Salience | Invalid P/L/U value | Use High/Medium/Low |
| `SM-002` | NoCategory | Salience | Cannot classify stakeholder | Check attribute combination |
| `MAP-001` | InvalidRing | Map | ring not inner/middle/outer | Fix ring value |
| `MAP-002` | InvalidSector | Map | Unknown sector name | Use §6.5 sector list |
| `MAP-004` | MissingReference | Map | Relationship target missing | Fix source/target IDs |
| `SH-010` | JavaNotInstalled | Render | Missing JRE 8+ | Install Java for JPype |
| `SH-011` | LicenseMissing | Render | Aspose .lic not found | Set ASPOSE_DIAGRAM_LICENSE_PATH |
| `SH-012` | RenderError | Render | File write failure | Check path permissions |

---

## 11. CLI Interface

Implemented in `stakeholder_diagram_generator/cli.py`:

```bash
# Generate all individual diagrams
python stakeholder_diagram_generator/cli.py \
  projects/daatsna-community-data-platform/inputs/stakeholder_input.json \
  -o projects/daatsna-community-data-platform/output

# Combined single Visio file (5 pages)
python stakeholder_diagram_generator/cli.py \
  projects/daatsna-community-data-platform/inputs/stakeholder_input.json \
  -o ./output --combined

# Validate input only (no rendering)
python stakeholder_diagram_generator/cli.py \
  projects/daatsna-community-data-platform/inputs/stakeholder_input.json \
  --validate-only

# Custom theme
python stakeholder_diagram_generator/cli.py spec.json -o ./output --theme corporate
```

| Flag | Description |
|------|-------------|
| `config` | Path to input JSON (required) |
| `-o`, `--output` | Output directory (default: `./output`) |
| `--combined` | Single `stakeholder_analysis_package.vsdx` with all pages |
| `--theme` | Color theme (default: `enterprise_blue`) |
| `-v`, `--verbose` | Debug logging |
| `--validate-only` | Validate and exit without rendering |

---

## 12. Usage Examples

### 12.1 Register Only (Minimum)
```bash
python stakeholder_diagram_generator/cli.py examples/example_register.json -o ./output
```

### 12.2 Full Stakeholder Analysis Package
```bash
python stakeholder_diagram_generator/cli.py examples/example_complete.json \
  -o ./output --combined
```

### 12.3 Validate Before CI Render
```bash
python stakeholder_diagram_generator/cli.py spec.json --validate-only && \
python stakeholder_diagram_generator/cli.py spec.json -o ./dist --combined
```

### 12.4 From specifications.json
```bash
# After prompt_skill_generator produces specifications.json,
# agent generates stakeholder_input.json per stakeholder_diagram_generator/PROMPT.md
python stakeholder_diagram_generator/cli.py \
  projects/daatsna-community-data-platform/inputs/stakeholder_input.json \
  -o projects/daatsna-community-data-platform/output --combined
```

---

## 13. Quality Checklist

- [ ] **Register completeness:** All stakeholders have unique IDs and required fields.
- [ ] **Quadrant accuracy:** Every stakeholder appears in exactly one Power-Interest quadrant.
- [ ] **Salience consistency:** Auto-computed categories match declared categories (or declarations omitted).
- [ ] **Network integrity:** All relationship source/target IDs resolve to nodes.
- [ ] **Map ring alignment:** Inner ring = Manage Closely stakeholders; outer = Monitor.
- [ ] **Cross-reference:** Same stakeholder names/IDs across all five outputs.
- [ ] **Excel export:** Register xlsx row count matches Visio table row count.
- [ ] **Combined package:** 5 pages in correct order when using `--combined`.
- [ ] **No RACI content:** RACI matrix is not embedded (separate skill).
- [ ] **Legend present:** Every diagram includes a legend explaining colors/symbols.

---

## 14. Testing Strategy

| Test | Input | Assert |
|------|-------|--------|
| Register validation | Duplicate S-001 | `SR-001` raised |
| Auto engagement | power=High, interest=Low, strategy=auto | → Keep Satisfied |
| Quadrant generation | 6 stakeholders with mixed P/I | 4 quadrants populated |
| Salience Definitive | P=H, L=H, U=H | category = Definitive, color #2E7D32 |
| Salience Dormant | P=H, L=L, U=L | category = Dormant |
| Influence score cap | 20 relationships | score ≤ 10.0 |
| Missing node ref | relationship target N99 | `IN-001` raised |
| Map invalid ring | ring="core" | `MAP-001` raised |
| Combined output | example_complete.json --combined | 5 pages in VSDX |
| Excel export | register with 6 rows | xlsx has 6 data rows + header |

Run tests:
```bash
pytest stakeholder_diagram_generator/tests/ -v
```

---

## 15. Summary: All Stakeholder Components

| Component | Focus | Structure | Use When |
|-----------|-------|-----------|----------|
| Stakeholder Register | Data source | Table | Foundation — identify and classify all stakeholders |
| Power-Interest Matrix | Engagement strategy | 2×2 grid | Decide how to engage each stakeholder |
| Influence Network | Relationships | Network graph | Understand who influences whom |
| Salience Model | Prioritization | Venn / category map | Prioritize attention using P+L+U |
| Stakeholder Map | Big picture | Radial / concentric | Strategic ecosystem overview |

**Not included (separate skills):**
- RACI Matrix → [raci-matrix-diagram-generator-SKILL.md](raci-matrix-diagram-generator-SKILL.md)
- Resource Allocation → [resource-allocation-matrix-generator-SKILL.md](resource-allocation-matrix-generator-SKILL.md)
