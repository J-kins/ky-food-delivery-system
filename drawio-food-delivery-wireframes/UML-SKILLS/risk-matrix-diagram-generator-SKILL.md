---
name: risk-matrix-diagram-generator
description: Generate professional Risk Matrix (Probability-Impact Heat Map) diagrams in fully editable Visio format (.vsdx) using Aspose.Diagram for Python. Plots project risks onto a 5x5 color-coded grid and generates a full risk register summary with mitigation strategies.
---

# Risk Matrix Diagram Generator Skill

This production-grade skill generates **Risk Matrix Diagrams** (also called Probability-Impact Matrices or Risk Heat Maps) in Microsoft Visio (`.vsdx`) format. Unlike tabular diagrams, the Risk Matrix is fundamentally a **coordinate-based diagram** — each risk is plotted as a point on a 2D plane where the X-axis represents Impact severity and the Y-axis represents Probability of occurrence. The intersection cell is color-coded by risk zone, and a risk item card is placed inside the appropriate cell.

Utilizing `Aspose.Diagram for Python`, this tool mathematically computes cell coordinates for each `(probability, impact)` pair, fills grid cells with zone-specific colors, overlays risk item cards, and appends a full risk register table with mitigation strategies.

This tool functions as a standalone risk assessment deliverable or as an integrated sub-component of the broader `project-charter-generator`.

## Table of Contents
1. Core Output Specifications
2. Environment Setup & Dependencies
3. Input Specification (JSON/YAML Schema)
4. Risk Matrix Visual Layout (ASCII Blueprint)
5. Risk Zones, Probability & Impact Scales
6. Detailed Styling Specifications
7. Code Architecture
8. Core Implementation Code
9. Error Handling
10. Command-Line Interface (CLI)
11. Quality Checklist
12. Usage Examples
13. Integration with Existing Skills
14. Testing Strategy

---

## 1. Core Output Specifications

The primary purpose of this skill is to generate a complete Risk Matrix that guarantees:
1. **5×5 Coordinate Grid:** A Probability (Y-axis, 1–5) × Impact (X-axis, 1–5) grid with 25 cells, each auto-filled with a zone color derived from the mathematical product `score = probability × impact`.
2. **Risk Zone Coloring:** Five color bands — Critical (Red), High (Orange), Medium (Amber), Low (Green), Minimal (Grey) — applied as cell backgrounds.
3. **Risk Item Cards:** Each risk in the input is placed as a floating rounded-rectangle card in the cell at `(probability, impact)`, displaying the Risk ID, short name, and score.
4. **Axis Labels:** Y-axis labeled with probability levels (Rare → Almost Certain); X-axis labeled with impact levels (Minor → Catastrophic).
5. **Risk Register Table:** A tabular section below the grid listing every risk with ID, Name, Probability, Impact, Score, Zone, and Mitigation Strategy.
6. **Summary Block:** A statistics box showing total counts by zone, top 3 risks by score, and mitigation completion status.
7. **Professional Formatting:** Fully editable, corporate-themed Microsoft Visio shapes (`.vsdx`).

---

## 2. Environment Setup & Dependencies

### 2.1 Python Requirements
```text
python >= 3.10
aspose-diagram-python >= 24.0.0
python-dotenv >= 1.0.0
pyyaml >= 6.0
pillow >= 10.0.0
typing-extensions >= 4.0.0
pydantic >= 2.0.0
```

### 2.2 System Dependencies

**Java Runtime Environment (JRE) 8 or higher**
- Required for `Aspose.Diagram for Python` (interfacing via JPype).
- *Installation guide:*
  - Ubuntu: `sudo apt-get install default-jre`
  - macOS: `brew install openjdk`
  - Windows: Download from https://www.java.com/download/

### 2.3 Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate on Unix/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Install dependencies
pip install aspose-diagram-python python-dotenv pyyaml pillow pydantic
```

### 2.4 Environment Variables (.env file)
```env
ASPOSE_DIAGRAM_LICENSE_PATH=/path/to/license.lic
OUTPUT_DIR=./output
LOG_LEVEL=INFO
DEFAULT_COLOR_THEME=enterprise_blue
DEFAULT_FONT_FAMILY=Arial
DEFAULT_FONT_SIZE=9
```

---

## 3. Input Specification (JSON/YAML Schema)

```json
{
  "risk_matrix": {
    "title": "Risk Matrix - Risk Assessment Dashboard",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    "sprint": "Sprint 5",
    "description": "Probability-Impact matrix for project risk assessment",

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
        "id": "R-001",
        "name": "Data Breach / Cyber Attack",
        "description": "Unauthorized access to patient data or system breach",
        "probability": 5,
        "impact": 5,
        "score": 25,
        "zone": "critical",
        "category": "Security",
        "mitigation": "Implement encryption, MFA, regular penetration testing, and security training",
        "owner": "Security Officer",
        "status": "Open",
        "trigger": "Failed security audit or suspicious activity detected"
      },
      {
        "id": "R-002",
        "name": "Regulatory Non-compliance",
        "description": "Failure to meet HIPAA, GDPR, or Uganda Data Protection Act requirements",
        "probability": 4,
        "impact": 5,
        "score": 20,
        "zone": "critical",
        "category": "Compliance",
        "mitigation": "Engage compliance team, regular audits, policy updates",
        "owner": "Compliance Officer",
        "status": "In Progress",
        "trigger": "Regulatory audit findings"
      },
      {
        "id": "R-003",
        "name": "Technology Failure",
        "description": "Critical system failure or downtime affecting operations",
        "probability": 4,
        "impact": 4,
        "score": 16,
        "zone": "high",
        "category": "Technical",
        "mitigation": "Implement redundancy, backup systems, disaster recovery plan",
        "owner": "DevOps Lead",
        "status": "Open",
        "trigger": "System performance degradation"
      },
      {
        "id": "R-004",
        "name": "Staff Turnover",
        "description": "Loss of key project personnel or critical skills",
        "probability": 3,
        "impact": 4,
        "score": 12,
        "zone": "medium",
        "category": "Resource",
        "mitigation": "Cross-training, knowledge management, succession planning",
        "owner": "Project Manager",
        "status": "Monitoring",
        "trigger": "Job market activity or employee dissatisfaction"
      },
      {
        "id": "R-005",
        "name": "Budget Overrun",
        "description": "Project costs exceed allocated budget",
        "probability": 3,
        "impact": 3,
        "score": 9,
        "zone": "low",
        "category": "Financial",
        "mitigation": "Regular budget monitoring, contingency reserves, cost control",
        "owner": "Project Manager",
        "status": "Monitoring",
        "trigger": "Cost variance > 10%"
      },
      {
        "id": "R-006",
        "name": "Schedule Delay",
        "description": "Project timeline slips beyond planned completion date",
        "probability": 2,
        "impact": 3,
        "score": 6,
        "zone": "low",
        "category": "Schedule",
        "mitigation": "Buffer management, agile sprints, regular progress tracking",
        "owner": "Project Manager",
        "status": "Open",
        "trigger": "Missed milestones or task delays"
      },
      {
        "id": "R-007",
        "name": "Stakeholder Resistance",
        "description": "Key stakeholders resistant to system adoption",
        "probability": 2,
        "impact": 2,
        "score": 4,
        "zone": "minimal",
        "category": "Stakeholder",
        "mitigation": "Regular communication, change management, stakeholder engagement",
        "owner": "Project Manager",
        "status": "Monitoring",
        "trigger": "Negative stakeholder feedback"
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

## 4. Risk Matrix Visual Layout (ASCII Blueprint)

**CRITICAL REQUIREMENT:** The grid must be rendered as a 5×5 coordinate plane. Cell `(probability=5, impact=5)` is the top-right corner (highest risk), and `(probability=1, impact=1)` is the bottom-left corner (lowest risk). Risk item cards are placed inside cells — multiple risks in the same cell are stacked vertically.

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                  RISK MATRIX - RISK ASSESSMENT DASHBOARD                                                      │
│                                             Da'atSNA Community Data Platform                                                                  │
│                                             Version 1.0  |  Sprint 5  |  2026-06-17                                                          │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                              │
│                                                ◄──────────── IMPACT (Severity) ──────────────►                                               │
│                                                                                                                                              │
│                                         │    1-MINOR   │  2-MODERATE  │   3-MAJOR    │   4-SEVERE   │ 5-CATASTROPHIC│                       │
│                                         ├──────────────┼──────────────┼──────────────┼──────────────┼───────────────┤                       │
│                ▲  5 - Almost Certain    │   LOW  (5)   │  MED  (10)   │  HIGH  (15)  │  HIGH  (20)  │  CRIT  (25)   │                       │
│                │                        │              │              │              │  ┌──────────┐ │  ┌──────────┐  │                       │
│                │                        │              │              │              │  │  R-004   │ │  │  R-001   │  │                       │
│                │                        │              │              │              │  │Staff Turn│ │  │DataBrch  │  │                       │
│                │                        │              │              │              │  │Score: 12 │ │  │Score: 25 │  │                       │
│                │                        │              │              │              │  └──────────┘ │  └──────────┘  │                       │
│  P             │                        ├──────────────┼──────────────┼──────────────┼──────────────┼───────────────┤                       │
│  R             │  4 - Likely            │  MIN   (4)   │   LOW  (8)   │  MED  (12)   │  HIGH  (16)  │  CRIT  (20)   │                       │
│  O             │                        │              │              │              │  ┌──────────┐ │  ┌──────────┐  │                       │
│  B             │                        │              │              │              │  │  R-003   │ │  │  R-002   │  │                       │
│  A             │                        │              │              │              │  │Tech Fail │ │  │Reg Compl │  │                       │
│  B             │                        │              │              │              │  │Score: 16 │ │  │Score: 20 │  │                       │
│  I             │                        │              │              │              │  └──────────┘ │  └──────────┘  │                       │
│  L             │                        ├──────────────┼──────────────┼──────────────┼──────────────┼───────────────┤                       │
│  I             │  3 - Possible          │  MIN   (3)   │   LOW  (6)   │   LOW  (9)   │  MED  (12)   │  HIGH  (15)   │                       │
│  T             │                        │              │              │  ┌──────────┐ │              │               │                       │
│  Y             │                        │              │              │  │  R-005   │ │              │               │                       │
│                │                        │              │              │  │Budget Ov │ │              │               │                       │
│                │                        │              │              │  │Score:  9 │ │              │               │                       │
│                │                        │              │              │  └──────────┘ │              │               │                       │
│                │                        ├──────────────┼──────────────┼──────────────┼──────────────┼───────────────┤                       │
│                │  2 - Unlikely          │  MIN   (2)   │  MIN   (4)   │   LOW  (6)   │   LOW  (8)   │  MED  (10)    │                       │
│                │                        │              │              │  ┌──────────┐ │              │               │                       │
│                │                        │              │              │  │  R-006   │ │              │               │                       │
│                │                        │              │              │  │Sched Dly │ │              │               │                       │
│                │                        │              │              │  │Score:  6 │ │              │               │                       │
│                │                        │              │              │  └──────────┘ │              │               │                       │
│                │                        ├──────────────┼──────────────┼──────────────┼──────────────┼───────────────┤                       │
│                │  1 - Rare              │  MIN   (1)   │  MIN   (2)   │  MIN   (3)   │  MIN   (4)   │   LOW  (5)    │                       │
│                │                        │  ┌──────────┐│              │              │              │               │                       │
│                │                        │  │  R-007   ││              │              │              │               │                       │
│                │                        │  │Stk Resist││              │              │              │               │                       │
│                ▼                        │  │Score:  4 ││              │              │              │               │                       │
│                                         │  └──────────┘│              │              │              │               │                       │
│                                         └──────────────┴──────────────┴──────────────┴──────────────┴───────────────┘                       │
│                                                                                                                                              │
│  Legend:                                                                                                                                     │
│  ══════                                                                                                                                      │
│  [CRIT] CRITICAL  Score 20-25  #E53935 (Red)    — Immediate executive action required                                                        │
│  [HIGH] HIGH      Score 15-19  #FF9800 (Orange) — Senior management attention required                                                       │
│  [MED]  MEDIUM    Score 10-14  #FFC107 (Amber)  — Management attention required                                                              │
│  [LOW]  LOW       Score  5-9   #4CAF50 (Green)  — Monitor and review periodically                                                            │
│  [MIN]  MINIMAL   Score  1-4   #E0E0E0 (Grey)   — Acceptable, monitor only                                                                   │
│                                                                                                                                              │
│  RISK REGISTER SUMMARY                                                                                                                       │
│  ═══════════════════                                                                                                                          │
│  ┌────────┬──────────────────────────┬─────┬──────┬───────┬──────────┬───────────────────────────────────────────────────────────────────┐  │
│  │   ID   │ RISK NAME                │ P   │  I   │ SCORE │  ZONE    │ MITIGATION STRATEGY                                               │  │
│  ├────────┼──────────────────────────┼─────┼──────┼───────┼──────────┼───────────────────────────────────────────────────────────────────┤  │
│  │ R-001  │ Data Breach / Cyber Att. │  5  │  5   │  25   │ CRITICAL │ Implement encryption, MFA, penetration testing, security training │  │
│  │ R-002  │ Regulatory Non-complianc │  4  │  5   │  20   │ CRITICAL │ Engage compliance team, regular audits, policy updates            │  │
│  │ R-003  │ Technology Failure       │  4  │  4   │  16   │ HIGH     │ Implement redundancy, backup systems, disaster recovery plan      │  │
│  │ R-004  │ Staff Turnover           │  3  │  4   │  12   │ MEDIUM   │ Cross-training, knowledge management, succession planning         │  │
│  │ R-005  │ Budget Overrun           │  3  │  3   │   9   │ LOW      │ Regular budget monitoring, contingency reserves                   │  │
│  │ R-006  │ Schedule Delay           │  2  │  3   │   6   │ LOW      │ Buffer management, agile sprints, regular progress tracking       │  │
│  │ R-007  │ Stakeholder Resistance   │  2  │  2   │   4   │ MINIMAL  │ Regular communication, change management, engagement              │  │
│  ├────────┼──────────────────────────┼─────┼──────┼───────┼──────────┼───────────────────────────────────────────────────────────────────┤  │
│  │ TOTALS │ 7 Risks                  │     │      │  Avg  │          │ Critical:2  High:1  Medium:1  Low:2  Minimal:1                     │  │
│  └────────┴──────────────────────────┴─────┴──────┴───────┴──────────┴───────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Risk Zones, Probability & Impact Scales

### 5.1 Zone Scoring Logic
Risk Score = `probability × impact`. The product determines the cell color band.

| Zone | Score Range | Fill Color | Text Color | Required Action |
|------|-------------|------------|------------|-----------------|
| Critical | 20–25 | `#E53935` | `#FFFFFF` | Immediate executive action |
| High | 15–19 | `#FF9800` | `#FFFFFF` | Senior management attention |
| Medium | 10–14 | `#FFC107` | `#333333` | Management attention required |
| Low | 5–9 | `#4CAF50` | `#FFFFFF` | Monitor and review periodically |
| Minimal | 1–4 | `#E0E0E0` | `#333333` | Acceptable, monitor only |

### 5.2 Probability Scale
| Score | Label | Description | Approx. Frequency |
|-------|-------|-------------|-------------------|
| 5 | Almost Certain | ≥ 75% chance | More than once per year |
| 4 | Likely | 50–74% chance | Once per year |
| 3 | Possible | 25–49% chance | Once every 2–3 years |
| 2 | Unlikely | 10–24% chance | Once every 5 years |
| 1 | Rare | < 10% chance | Once every 10+ years |

### 5.3 Impact Scale
| Score | Label | Description | Example Financial Loss |
|-------|-------|-------------|------------------------|
| 5 | Catastrophic | Business failure, loss of life | > $1M |
| 4 | Severe | Major reputation damage, operations suspended | $500K–$1M |
| 3 | Major | Significant operational impact | $100K–$500K |
| 2 | Moderate | Manageable impact, recoverable | $10K–$100K |
| 1 | Minor | Negligible impact | < $10K |

### 5.4 Pre-computed Zone Map (5×5)
The following table shows the zone for every cell in the 5×5 grid, computed as `P × I`:

```text
                 IMPACT
                  1        2        3        4        5
                  ─────────────────────────────────────
Prob 5 │         LOW(5)  MED(10)  HI(15)   HI(20)  CR(25)
Prob 4 │         MIN(4)  LOW(8)   MED(12)  HI(16)  CR(20)
Prob 3 │         MIN(3)  LOW(6)   LOW(9)   MED(12) HI(15)
Prob 2 │         MIN(2)  MIN(4)   LOW(6)   LOW(8)  MED(10)
Prob 1 │         MIN(1)  MIN(2)   MIN(3)   MIN(4)  LOW(5)
```

---

## 6. Detailed Styling Specifications

### 6.1 Grid Cell Styling
| Property | Value | Description |
|----------|-------|-------------|
| Cell Size | `1.5in × 1.5in` | Square cells, exact |
| Grid Line Color | `#333333` | Dark grey borders |
| Grid Line Width | 1pt | |
| Fill Color | Zone color | Background per zone |
| Fill Opacity | 80% | Slight transparency |
| Corner Radius | 0pt | Hard edges for grid feel |

### 6.2 Risk Item Card Styling
| Property | Value | Description |
|----------|-------|-------------|
| Shape | Rounded Rectangle | Standard card |
| Corner Radius | 4pt | |
| Fill Color | `#FFFFFF` | White card on colored background |
| Border Color | `#666666` | Subtle grey outline |
| Border Width | 1pt | |
| Shadow | Enabled | Drop shadow `rgba(0,0,0,0.2)` |
| Max Width | `cell_size - 0.2in` | Leaves a margin within the cell |
| Max Height | `0.6in` per card | For stacking multiple cards |

### 6.3 Risk Item Text
| Element | Font Size | Weight | Color |
|---------|-----------|--------|-------|
| Risk ID | 8pt | Bold | `#1a237e` |
| Risk Name | 7pt | Regular | `#333333` |
| Score Badge | 7pt | Bold | Zone text color |

### 6.4 Axis Label Styling
| Property | Value |
|----------|-------|
| Font Size | 9pt Bold |
| Probability label | Rotated 90° on the left |
| Impact label | Horizontal across the top |
| Scale labels | 8pt Regular, centred above/left of each column/row |

---

## 7. Code Architecture

```text
risk_matrix_generator/
├── __init__.py
├── skill.md
├── core/
│   ├── __init__.py
│   ├── diagram_builder.py         # Main orchestration
│   ├── validator.py               # Input validation
│   ├── errors.py                  # Custom exceptions
│   └── models.py                  # Pydantic models
├── renderers/
│   ├── __init__.py
│   ├── aspose_renderer.py         # Aspose.Diagram API layer
│   ├── dot_generator.py           # PNG preview generation
│   └── layout_engine.py           # Cell/card stacking calculations
├── calculators/
│   ├── __init__.py
│   ├── risk_calculator.py         # Score computation & analysis
│   └── zone_calculator.py         # Zone classification
├── stylers/
│   ├── __init__.py
│   ├── color_themes.py
│   ├── cell_styler.py             # Grid cell zone colors
│   └── risk_styler.py             # Risk card overlays
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   └── geometry_utils.py
├── templates/
│   └── risk_matrix_template.vstx
├── config/
│   ├── __init__.py
│   └── settings.py
└── cli.py
```

---

## 8. Core Implementation Code

### 8.1 Zone Calculator (`calculators/zone_calculator.py`)

```python
from typing import List, Dict

# Pre-computed lookup for 5x5 grid (probability x impact)
ZONE_LOOKUP = {
    (5, 5): "critical", (5, 4): "high",    (5, 3): "high",   (5, 2): "medium", (5, 1): "low",
    (4, 5): "critical", (4, 4): "high",    (4, 3): "medium", (4, 2): "low",    (4, 1): "minimal",
    (3, 5): "high",     (3, 4): "medium",  (3, 3): "low",    (3, 2): "low",    (3, 1): "minimal",
    (2, 5): "medium",   (2, 4): "low",     (2, 3): "low",    (2, 2): "minimal",(2, 1): "minimal",
    (1, 5): "low",      (1, 4): "minimal", (1, 3): "minimal",(1, 2): "minimal",(1, 1): "minimal",
}

ZONE_COLORS = {
    "critical": {"fill": "#E53935", "text": "#FFFFFF"},
    "high":     {"fill": "#FF9800", "text": "#FFFFFF"},
    "medium":   {"fill": "#FFC107", "text": "#333333"},
    "low":      {"fill": "#4CAF50", "text": "#FFFFFF"},
    "minimal":  {"fill": "#E0E0E0", "text": "#333333"},
}

class ZoneCalculator:
    """Classifies risks and grid cells into color zones."""
    
    @staticmethod
    def get_zone(probability: int, impact: int) -> str:
        """Return zone ID for a given probability/impact pair."""
        key = (int(probability), int(impact))
        return ZONE_LOOKUP.get(key, "minimal")
    
    @staticmethod
    def get_zone_from_score(score: int) -> str:
        """Classify a numeric score into a zone."""
        if score >= 20: return "critical"
        if score >= 15: return "high"
        if score >= 10: return "medium"
        if score >= 5:  return "low"
        return "minimal"
    
    @staticmethod
    def get_colors(zone_id: str) -> Dict:
        """Return fill and text color for a zone."""
        return ZONE_COLORS.get(zone_id, ZONE_COLORS["minimal"])
```

### 8.2 Risk Calculator (`calculators/risk_calculator.py`)

```python
from dataclasses import dataclass, field
from typing import List, Dict
from calculators.zone_calculator import ZoneCalculator

@dataclass
class RiskAnalysis:
    total_risks: int
    zone_counts: Dict[str, int]
    top_risks: List[Dict]
    mitigation_coverage: float
    risks_needing_action: List[Dict]

class RiskCalculator:
    """Calculates risk scores, zone classifications, and summary statistics."""
    
    def __init__(self, risks: List[Dict], zones: List[Dict]):
        self.risks = risks
        self.zones = zones
        self._enrich_risks()
    
    def _enrich_risks(self) -> None:
        """Compute score and zone for any risk missing them."""
        for risk in self.risks:
            p = risk.get('probability', 1)
            i = risk.get('impact', 1)
            
            # Compute score if missing
            if 'score' not in risk:
                risk['score'] = p * i
            
            # Classify zone if missing or override
            risk['zone'] = ZoneCalculator.get_zone(p, i)
    
    def analyze(self) -> RiskAnalysis:
        """Build complete analysis summary."""
        zone_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "minimal": 0}
        
        for risk in self.risks:
            zone = risk.get('zone', 'minimal')
            if zone in zone_counts:
                zone_counts[zone] += 1
        
        top_risks = sorted(self.risks, key=lambda r: r.get('score', 0), reverse=True)[:3]
        
        risks_with_mitigation = sum(1 for r in self.risks if r.get('mitigation'))
        coverage = risks_with_mitigation / max(1, len(self.risks))
        
        needs_action = [r for r in self.risks if r.get('zone') in ('critical', 'high')]
        
        return RiskAnalysis(
            total_risks=len(self.risks),
            zone_counts=zone_counts,
            top_risks=top_risks,
            mitigation_coverage=round(coverage * 100, 1),
            risks_needing_action=needs_action
        )
```

### 8.3 Diagram Builder (`core/diagram_builder.py`)

```python
from aspose.diagram import Diagram, SaveFileFormat
from typing import Dict, List
from collections import defaultdict
from calculators.risk_calculator import RiskCalculator
from calculators.zone_calculator import ZoneCalculator

class RiskMatrixBuilder:
    """Constructs the 5x5 Risk Matrix Visio diagram."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._calculate_grid()
        self._analyze_risks()
    
    def _setup_page(self) -> None:
        """Configure A2 landscape bounds."""
        self.page.page_sheet.page_props.page_width = 59.4
        self.page.page_sheet.page_props.page_height = 42.0
        self.page_width = 59.4
        self.page_height = 42.0
    
    def _setup_styles(self) -> None:
        """Bind global styles from config."""
        styling = self.config.get("styling", {})
        self.cell_size = styling.get("cell_size", 1.5)
        self.font_family = styling.get("font_family", "Arial")
        self.font_size = styling.get("font_size", 9)
        self.shadow_enabled = styling.get("shadow_enabled", True)
        self.risk_zones = self.config['risk_matrix']['risk_zones']
    
    def _calculate_grid(self) -> None:
        """Compute (x, y) for all 25 grid cells."""
        layout = self.config.get("layout", {})
        margin = layout.get("margin", 0.5)
        header_height = layout.get("header_height", 1.2)
        
        # Offset for axis labels
        axis_label_width = 2.0  # Width reserved for probability labels on the left
        axis_label_height = 1.2 # Height reserved for impact labels on top
        
        x_origin = margin + axis_label_width
        y_origin = margin + header_height + axis_label_height
        
        self.cell_positions = {}
        
        # Visio Y: Lower number = higher on page.
        # Prob=5 (Almost Certain) maps to the TOP row → smallest Y
        # Prob=1 (Rare) maps to the BOTTOM row → largest Y
        for prob in range(1, 6):
            for impact in range(1, 6):
                # X increases left to right (impact 1→5)
                cell_x = x_origin + (impact - 1) * self.cell_size
                # Y increases downward in Visio — prob 5 is at row 0
                cell_y = y_origin + (5 - prob) * self.cell_size
                
                score = prob * impact
                zone = ZoneCalculator.get_zone(prob, impact)
                colors = ZoneCalculator.get_colors(zone)
                
                self.cell_positions[(prob, impact)] = {
                    'x': cell_x,
                    'y': cell_y,
                    'width': self.cell_size,
                    'height': self.cell_size,
                    'score': score,
                    'zone': zone,
                    'fill_color': colors['fill'],
                    'text_color': colors['text']
                }
        
        # Store grid bounds for reference
        self.grid_x_start = x_origin
        self.grid_y_start = y_origin
        self.grid_total_width = self.cell_size * 5
        self.grid_total_height = self.cell_size * 5
    
    def _analyze_risks(self) -> None:
        """Run risk analysis."""
        risks = self.config['risk_matrix']['risks']
        zones = self.config['risk_matrix']['risk_zones']
        calculator = RiskCalculator(risks, zones)
        self.analysis = calculator.analyze()
        
        # Group risks by (probability, impact) for card stacking
        self.risk_cell_map = defaultdict(list)
        for risk in risks:
            key = (risk['probability'], risk['impact'])
            self.risk_cell_map[key].append(risk)
    
    def _get_card_positions(self, cell: Dict, risks_in_cell: List[Dict]) -> List[Dict]:
        """
        Compute stacked card positions within a cell.
        Multiple risks in the same cell are stacked vertically.
        """
        card_height = 0.55  # Inches per card
        card_width = self.cell_size - 0.15
        padding = 0.08
        
        positions = []
        for idx, risk in enumerate(risks_in_cell):
            card_x = cell['x'] + padding
            card_y = cell['y'] + padding + (idx * (card_height + 0.05))
            positions.append({
                'x': card_x,
                'y': card_y,
                'width': card_width,
                'height': card_height,
                'risk': risk
            })
        return positions
    
    def build(self) -> None:
        """Execute all Aspose.Diagram draw calls."""
        # 1. Title block
        # 2. Impact axis labels (top, horizontal)
        # 3. Probability axis labels (left, vertical with arrow)
        # 4. 25 grid cells with zone colors
        # 5. Risk item cards overlaid on cells
        # 6. Score label in corner of each cell (small, muted)
        # 7. Legend block (zone definitions)
        # 8. Risk register table (below the grid)
        # 9. Summary statistics block
        pass
    
    def save(self, output_path: str) -> None:
        """Export to VSDX."""
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

### 8.4 Layout Engine (`renderers/layout_engine.py`)

```python
from typing import Dict, List, Tuple

class RiskLayoutEngine:
    """
    Handles card stacking and overflow detection.
    When more than N risks occupy a single cell, overflow cards
    are referenced via a footnote callout rather than drawn inside.
    """
    
    MAX_CARDS_PER_CELL = 3
    
    @staticmethod
    def pack_cards(cell: Dict, risks: List[Dict], card_height: float = 0.55) -> Tuple[List, List]:
        """
        Pack risk cards into a cell.
        Returns (visible_cards, overflow_cards).
        Overflow occurs when there are more than MAX_CARDS_PER_CELL risks in one cell.
        """
        max_n = RiskLayoutEngine.MAX_CARDS_PER_CELL
        visible = risks[:max_n]
        overflow = risks[max_n:]
        return visible, overflow
    
    @staticmethod
    def compute_card_y(cell_y: float, card_index: int, card_height: float, padding: float = 0.08) -> float:
        """
        Compute the Y coordinate for a stacked card inside a cell.
        Index 0 = top of cell, index 1 = below first card, etc.
        """
        return cell_y + padding + card_index * (card_height + 0.04)
```

---

## 9. Error Handling

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| `RX-001` | InvalidInput | JSON fails Pydantic schema. | Validate all fields. |
| `RX-002` | NoRisks | Risks array is empty. | Add at least 1 risk. |
| `RX-003` | InvalidProbability | Probability not in `[1,2,3,4,5]`. | Set to integer 1–5. |
| `RX-004` | InvalidImpact | Impact not in `[1,2,3,4,5]`. | Set to integer 1–5. |
| `RX-005` | InvalidScore | Declared score ≠ `probability × impact`. | Remove `score` field and let it auto-compute. |
| `RX-006` | InvalidZone | Declared zone does not match computed zone. | Remove `zone` field and let it auto-classify. |
| `RX-007` | DuplicateRiskID | Two risks share the same `id`. | Assign unique IDs. |
| `RX-008` | NoZonesDefined | `risk_zones` array is empty. | Provide zone definitions. |
| `RX-009` | JavaNotInstalled | Missing JRE 8+. | Install Java for JPype. |
| `RX-010` | LicenseMissing | Aspose `.lic` not found. | Set environment variable. |
| `RX-011` | RenderError | File write failure. | Check path permissions. |
| `RX-012` | CellOverflow | More than 3 risks in a single cell. | Warning only — overflow risks shown as footnotes. |

> **Note on `RX-005` and `RX-006`:** These are not hard errors but consistency warnings. The builder always overrides declared `score` and `zone` with auto-computed values to ensure correctness.

---

## 10. Command-Line Interface (CLI)

```python
# cli.py
import argparse
import json
import logging
import sys
from core.diagram_builder import RiskMatrixBuilder

def main():
    parser = argparse.ArgumentParser(description="Generate Visio Risk Matrix Diagram")
    parser.add_argument("input", help="Path to input JSON/YAML file")
    parser.add_argument("-o", "--output", help="Output VSDX path (default: ./output/risk_matrix.vsdx)")
    parser.add_argument("-p", "--preview", action="store_true", help="Generate PNG preview")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--validate-only", action="store_true", help="Validate without rendering")
    parser.add_argument("--top-risks", type=int, default=3, help="Number of top risks to highlight in summary")
    parser.add_argument("--no-register", action="store_true", help="Skip risk register table")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    with open(args.input, 'r') as f:
        spec = json.load(f)
    
    if args.validate_only:
        logging.info("Risk Matrix input validation passed.")
        sys.exit(0)
    
    builder = RiskMatrixBuilder(spec)
    builder.build()
    
    out_path = args.output or "./output/risk_matrix.vsdx"
    builder.save(out_path)
    logging.info(f"Risk Matrix saved to {out_path}")

if __name__ == "__main__":
    main()
```

---

## 11. Quality Checklist

- [ ] **Zone Colors:** Every cell is filled with its correct zone color based on the pre-computed lookup table.
- [ ] **Coordinate Accuracy:** Cell `(prob=5, impact=5)` renders in the top-right corner of the grid; `(prob=1, impact=1)` in the bottom-left.
- [ ] **Card Placement:** Risk cards appear within the bounds of the correct cell with padding.
- [ ] **Card Stacking:** Multiple risks in the same cell stack vertically without overflowing cell boundaries.
- [ ] **Overflow Handling:** More than 3 risks in a cell triggers `RX-012` warning and shows `+N more` footnote.
- [ ] **Score Override:** Builder always auto-computes score from `probability × impact`, ignoring any declared value.
- [ ] **Register Table:** All risks appear in the risk register section below the grid in score-descending order.
- [ ] **Summary Block:** Zone counts, top 3 risks, and mitigation coverage percentage are accurate.

---

## 12. Usage Examples

### 12.1 Standard Generation
```bash
python risk_matrix_generator/cli.py data/risks.json -o output/risk_matrix.vsdx
```

### 12.2 Highlight Top 5 Risks in Summary
```bash
python risk_matrix_generator/cli.py data/risks.json -o output/risk_matrix.vsdx --top-risks 5
```

### 12.3 Grid Only (No Register Table)
```bash
python risk_matrix_generator/cli.py data/risks.json -o output/risk_matrix.vsdx --no-register
```

### 12.4 With PNG Preview
```bash
python risk_matrix_generator/cli.py data/risks.json -o output/risk_matrix.vsdx --preview
```

---

## 13. Integration with Existing Skills

1. **Charter Integration:** The Risk Matrix is a mandatory section of the `project-charter-generator`. It is embedded after the Stakeholder Matrix and before the Milestone Chart.
2. **RACI Synergy:** The `owner` field in each risk maps directly to a Role ID in the `raci-matrix-diagram-generator`, enabling cross-linking between the two documents.
3. **WBS Synergy:** Risk categories (`Technical`, `Schedule`, `Resource`) correspond to WBS Level-1 nodes, enabling phase-level risk filtering.

---

## 14. Testing Strategy

1. **Zone Boundary Test:** Supply a risk with `probability=4, impact=5` (`score=20`). Assert zone = `critical` and cell fill = `#E53935`.
2. **Zone Boundary Test 2:** Supply a risk with `probability=3, impact=5` (`score=15`). Assert zone = `high` and cell fill = `#FF9800`.
3. **Score Override Test:** Supply a risk with `score: 5` but `probability=5, impact=5`. Assert the builder overrides to `score=25` and zone = `critical`.
4. **Cell Overflow Test:** Place 5 risks in cell `(3,3)`. Assert `RX-012` warning fires and only the top 3 (by ID order) are drawn in-cell.
5. **Empty Risks Test:** Supply an empty `risks` array. Assert `RX-002` is raised.
6. **Invalid Probability Test:** Supply `probability: 6`. Assert `RX-003` is raised.
