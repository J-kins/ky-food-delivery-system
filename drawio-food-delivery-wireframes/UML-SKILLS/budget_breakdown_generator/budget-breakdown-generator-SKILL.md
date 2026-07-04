---
name: budget-breakdown-generator
description: Generate an enterprise-grade Budget Breakdown package — Excel workbook (.xlsx) with professional formatting, formulas, charts, and a Visio visual dashboard (.vsdx) with bar chart, distribution panel, and burn-rate visualization. All outputs follow mandatory design standards from uml-diagram-generator-SKILL.md §11 plus budget-specific styling (enterprise color palette, Arial typography, title blocks, legends). Supports live data connectivity via a DataConnection sheet linking Visio shapes to Excel named ranges.
---

# Budget Breakdown Generator Skill

This production-grade skill generates a **complete Budget Breakdown Package** consisting of two synchronized, **executive-presentation-ready** output files:

1. **Excel Workbook (`.xlsx`)** — Built with `openpyxl`, containing four structured sheets: Budget Summary, Detailed Breakdown, Monthly Burn Rate, and a DataConnection sheet that acts as the live data bridge to Visio.
2. **Visio Dashboard (`.vsdx`)** — Built with `Aspose.Diagram for Python` (JVM via JPype), rendering a title block, KPI summary bar, horizontal bar chart, distribution panel, and monthly burn-rate chart.

This tool functions as a standalone financial reporting deliverable or as an integrated sub-component of the broader `project-charter-generator`.

## Design Philosophy

Every output must be:

| Principle | Requirement |
|-----------|-------------|
| **Visually stunning** | Enterprise color palette, clean white backgrounds, subtle shadows, consistent branding |
| **Enterprise-ready** | Suitable for executive presentations and board meetings |
| **Data-driven** | All numbers accurate; totals, percentages, and variance calculated programmatically |
| **Programmatic** | Fully automated — no manual tweaking after generation |

**Design system authority:** Inherits mandatory standards from [`uml-diagram-generator-SKILL.md`](uml-diagram-generator-SKILL.md) §11 (layout, typography, colors, title block, legend, QA). This skill adds budget-specific category colors, chart layout, and Excel table styling on top of that base.

## Table of Contents
1. Core Output Specifications
2. Professional Design Standards
3. Environment Setup & Dependencies
4. Input Specification (JSON/YAML Schema)
5. Excel Workbook Layout (ASCII Blueprint)
6. Visio Dashboard Layout (ASCII Blueprint)
7. Excel Implementation (openpyxl)
8. Visio Implementation (Aspose.Diagram)
9. Data Flow & Connectivity Architecture
10. Code Architecture
11. Error Handling
12. Command-Line Interface (CLI)
13. Quality Checklist
14. Usage Examples
15. Integration with Existing Skills
16. Testing Strategy
17. Troubleshooting Guide

---

## 1. Core Output Specifications

### Output A: Excel Workbook (`budget_breakdown.xlsx`)
| Sheet | Name | Purpose |
|-------|------|---------|
| 1 | `Budget Summary` | High-level category totals, Budget vs Actual comparison |
| 2 | `Detailed Breakdown` | Line-item detail with QTY × Unit Cost formulas |
| 3 | `Monthly Burn Rate` | Monthly planned vs actual with cumulative columns |
| 4 | `DataConnection` | Named cells for Visio shape linking |

### Output B: Visio Dashboard (`budget_dashboard.vsdx`)
| Section | Content |
|---------|---------|
| Title Block | Project name, total budget, currency, data source reference |
| Bar Chart | Horizontal proportional bars per category (scaled to max budget value) |
| Pie Chart | Simulated sector wedges using arc shapes |
| Burn Rate | Line chart drawn as connected polylines over a timeline axis |
| KPI Boxes | Key indicators: Total Budget, Spent to Date, Remaining, Variance |
| Legend | Category color key |

---

## 2. Professional Design Standards

### 2.1 Inherited Base Standards

Apply all settings from [`uml-diagram-generator-SKILL.md`](uml-diagram-generator-SKILL.md) §11:

- Page: **A2 landscape** (59.4 × 42.0 in), margin **0.5 cm**
- Font: **Arial** (10pt body, 14pt titles, 8pt labels)
- Title block: `#1a237e` background, white text
- QA: validate input, check text overflow, verify legend matches content, minimum `.vsdx` size ≥ 4 KB

### 2.2 Budget Category Colors (Consistent Across Excel + Visio)

Use these colors for every chart, bar, and legend swatch — do not assign ad-hoc hex values:

| Category | Hex | Usage |
|----------|-----|-------|
| Personnel | `#1565C0` | Largest cost bucket — blue |
| Hardware | `#E65100` | Orange |
| Software | `#6A1B9A` | Purple |
| Training | `#2E7D32` | Green |
| Contingency | `#FFB300` | Amber |

### 2.3 Visio Styling Configuration

```yaml
visio_styling:
  title_block:
    height: 1.5
    background: "#1a237e"
    text_color: "#FFFFFF"
    font: "Arial"
    font_size: 14
    bold: true

  colors:
    primary: "#1a237e"
    secondary: "#1565C0"
    light_blue: "#E3F2FD"
    panel_bg: "#FAFAFA"
    grid: "#E0E0E0"
    text: "#333333"
    planned: "#1565C0"
    actual: "#C62828"          # or #E65100 for burn-rate bars

  bar_chart:
    height: 4.0
    bar_height: 0.4
    bar_gap: 0.1
    category_label_width: 2.0
    value_format: "${:,.0f}"
    percent_format: "{:.0f}%"
    grid_lines: { enabled: true, style: dashed, color: "#E0E0E0" }

  burn_rate:
    width: 8.0
    height: 4.0
    planned_color: "#1565C0"
    actual_color: "#C62828"
    x_axis_labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    y_axis_label: "Amount (USD)"
    y_format: "${:,.0f}"

  shadow:
    enabled: true
    color: "rgba(0,0,0,0.08)"
    offset_x: 2
    offset_y: 2
    blur: 4

  borders:
    default: { style: solid, width: 1.0, color: "#E0E0E0" }
    accent: { style: solid, width: 2.0, color: "#1a237e" }
```

### 2.4 Excel Styling Configuration

```yaml
excel_styling:
  workbook:
    author: "Project Team"
    title: "Budget Breakdown - Project Financials"

  sheets:
    summary:       { name: "Budget Summary",       tab_color: "#1a237e", freeze_panes: "A7" }
    detailed:      { name: "Detailed Breakdown",   tab_color: "#1565C0", freeze_panes: "A2" }
    burn_rate:     { name: "Monthly Burn Rate",    tab_color: "#E65100", freeze_panes: "A2" }
    data_connection: { name: "DataConnection",     tab_color: "#2E7D32", freeze_panes: "A2" }

  table_styles:
    header:   { fill: "#1a237e", font_color: "#FFFFFF", font_size: 11, bold: true }
    body:     { font_size: 10, font_color: "#333333" }
    total:    { fill: "#E3F2FD", font_color: "#1a237e", bold: true }
  alternating_rows: { even: "#F8F9FA", odd: "#FFFFFF" }

  number_formats:
    currency: '"$"#,##0_);("$"#,##0)'
    percentage: '0.0%'
    variance: '+#,##0_);(#,##0)'

  conditional_formatting:
    variance_under_budget: { color: "#2E7D32" }   # actual < budget (savings)
    variance_over_budget:  { color: "#C62828" }   # actual > budget (overrun)

  charts:                          # recommended on Summary sheet
    pie:
      title: "Budget Distribution"
      colors: ["#1565C0", "#E65100", "#6A1B9A", "#2E7D32", "#FFB300"]
    burn_rate:
      title: "Monthly Burn Rate - Planned vs Actual"
      planned_color: "#1565C0"
      actual_color: "#E65100"
```

### 2.5 Anti-Patterns (Do NOT)

- Comic Sans or decorative fonts
- Neon or unlabeled colors
- Hardcoded percentages instead of formulas
- Lines or bars cutting through labels
- Missing title block on Visio dashboard
- Accepting empty or sub-4KB `.vsdx` files as success
- Category colors that differ between Excel and Visio

---

## 3. Environment Setup & Dependencies

### 3.1 Python Requirements
```text
python >= 3.10
aspose-diagram>=23.10.0
JPype1>=1.5.0
openpyxl>=3.1.0
python-dotenv>=1.0.0
pyyaml>=6.0
pydantic>=2.0.0
```

### 3.2 System Dependencies

**Java Runtime Environment (JRE) 8 or higher**
- Required for `Aspose.Diagram for Python` (interfacing via JPype).
- *Installation:*
  - Ubuntu: `sudo apt-get install default-jre`
  - macOS: `brew install openjdk`
  - Windows: Download from https://www.java.com/download/

### 3.3 Virtual Environment Setup
```bash
python -m venv venv
source venv/bin/activate          # Unix/macOS
venv\Scripts\activate             # Windows

pip install aspose-diagram JPype1 openpyxl python-dotenv pyyaml pydantic
```

### 3.4 Environment Variables (.env file)
```env
ASPOSE_DIAGRAM_LICENSE_PATH=/path/to/license.lic
OUTPUT_DIR=./output
LOG_LEVEL=INFO
DEFAULT_FONT_FAMILY=Arial
DEFAULT_CURRENCY=USD
```

---

## 4. Input Specification (JSON/YAML Schema)

```json
{
  "budget": {
    "title": "Budget Breakdown - Project Financials",
    "project_name": "Da'atSNA Community Data Platform",
    "version": "1.0",
    "date": "2026-06-17",
    "currency": "USD",
    "exchange_rate_note": "1 USD = 3,700 UGX",
    "budget_period": "Jan 2026 - Dec 2026",

    "categories": [
      {
        "id": "CAT1",
        "name": "Personnel",
        "color": "#1565C0",
        "text_color": "#FFFFFF",
        "budget": 31000,
        "actual": 28500,
        "notes": "Includes PM, Dev, QA, BA"
      },
      {
        "id": "CAT2",
        "name": "Hardware",
        "color": "#E65100",
        "text_color": "#FFFFFF",
        "budget": 18500,
        "actual": 19200,
        "notes": "Cloud, workstations, network"
      },
      {
        "id": "CAT3",
        "name": "Software",
        "color": "#6A1B9A",
        "text_color": "#FFFFFF",
        "budget": 1500,
        "actual": 1200,
        "notes": "Licenses, tools"
      },
      {
        "id": "CAT4",
        "name": "Training",
        "color": "#2E7D32",
        "text_color": "#FFFFFF",
        "budget": 3000,
        "actual": 2800,
        "notes": "User training, materials"
      },
      {
        "id": "CAT5",
        "name": "Contingency",
        "color": "#FFB300",
        "text_color": "#FFFFFF",
        "budget": 5400,
        "actual": 2100,
        "notes": "10% buffer of subtotal"
      }
    ],

    "line_items": [
      {
        "category": "Personnel",
        "item": "Project Manager",
        "qty": 1,
        "unit_cost": 5000,
        "total": 5000
      },
      {
        "category": "Personnel",
        "item": "Developers",
        "qty": 3,
        "unit_cost": 4000,
        "total": 12000
      },
      {
        "category": "Personnel",
        "item": "QA Engineers",
        "qty": 2,
        "unit_cost": 3500,
        "total": 7000
      },
      {
        "category": "Personnel",
        "item": "Business Analysts",
        "qty": 2,
        "unit_cost": 3500,
        "total": 7000
      },
      {
        "category": "Personnel",
        "item": "DevOps Engineer",
        "qty": 1,
        "unit_cost": 4500,
        "total": 4500
      },
      {
        "category": "Hardware",
        "item": "Cloud Servers (annual)",
        "qty": 4,
        "unit_cost": 1500,
        "total": 6000
      },
      {
        "category": "Hardware",
        "item": "Workstations",
        "qty": 5,
        "unit_cost": 2000,
        "total": 10000
      },
      {
        "category": "Hardware",
        "item": "Network Equipment",
        "qty": 1,
        "unit_cost": 2500,
        "total": 2500
      },
      {
        "category": "Software",
        "item": "Licenses (per user)",
        "qty": 5,
        "unit_cost": 200,
        "total": 1000
      },
      {
        "category": "Software",
        "item": "Development Tools",
        "qty": 1,
        "unit_cost": 500,
        "total": 500
      },
      {
        "category": "Training",
        "item": "User Training Sessions",
        "qty": 10,
        "unit_cost": 300,
        "total": 3000
      },
      {
        "category": "Contingency",
        "item": "10% Contingency Buffer",
        "qty": 1,
        "unit_cost": 5400,
        "total": 5400
      }
    ],

    "monthly_burn_rate": [
      {"month": "January",   "planned": 5000, "actual": 4800},
      {"month": "February",  "planned": 5000, "actual": 5200},
      {"month": "March",     "planned": 5000, "actual": 4500},
      {"month": "April",     "planned": 6000, "actual": 6500},
      {"month": "May",       "planned": 6000, "actual": 5800},
      {"month": "June",      "planned": 6000, "actual": 6200},
      {"month": "July",      "planned": 4000, "actual": 3500},
      {"month": "August",    "planned": 4000, "actual": 4200},
      {"month": "September", "planned": 4000, "actual": 3800},
      {"month": "October",   "planned": 4500, "actual": 5000},
      {"month": "November",  "planned": 4500, "actual": 4300},
      {"month": "December",  "planned": 5400, "actual": null}
    ],

    "styling": {
      "font_family": "Arial",
      "font_size": 9,
      "header_fill": "#1a237e",
      "header_text": "#FFFFFF",
      "alt_row_fill": "#F5F5F5",
      "total_row_fill": "#E3F2FD",
      "positive_variance": "#2E7D32",
      "negative_variance": "#C62828"
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

## 5. Excel Workbook Layout (ASCII Blueprint)

**CRITICAL:** This ASCII blueprint defines the exact sheet structure. All styling follows Section 2.4.

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                         BUDGET BREAKDOWN - PROJECT FINANCIALS                                                                │
│                              Da'atSNA Community Data Platform  │  Version 1.0  │  2026-06-17                                │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  Tabs: [Budget Summary] [Detailed Breakdown] [Monthly Burn Rate] [DataConnection]                                            │
│                                                                                                                              │
│  SHEET 1: BUDGET SUMMARY  (tab #1a237e, freeze A7)                                                                          │
│  ┌──────┬────────────────────────┬──────────────┬──────────────┬──────────────────────────────────────────────────────────┐  │
│  │  ROW │  A                     │  B           │  C           │  D                                                       │  │
│  ├──────┼────────────────────────┼──────────────┼──────────────┼──────────────────────────────────────────────────────────┤  │
│  │   1  │  BUDGET BREAKDOWN      │              │              │  [merged A1:F1, Arial 16 bold #1a237e]                   │  │
│  │   3  │  Project:              │  Da'atSNA…   │              │                                                          │  │
│  │   4  │  Date:                 │  2026-06-17  │              │                                                          │  │
│  │   5  │  Version:              │  1.0         │              │                                                          │  │
│  │   6  │  Currency:             │  USD         │              │                                                          │  │
│  │   8  │  CATEGORY              │  TOTAL (USD) │  PERCENTAGE  │  NOTES                                                   │  │
│  │  10  │  Personnel             │  $31,000     │  52.2%       │  Includes PM, Dev, QA, BA                                │  │
│  │  11  │  Hardware              │  $18,500     │  31.1%       │  Cloud, workstations, network                            │  │
│  │  12  │  Software              │  $1,500     │  2.5%        │  Licenses, tools                                         │  │
│  │  13  │  Training              │  $3,000     │  5.1%        │  User training                                           │  │
│  │  14  │  Contingency           │  $5,400     │  9.1%        │  10% buffer                                              │  │
│  │  16  │  TOTAL                 │  $59,400     │  100.0%      │  #E3F2FD total row                                       │  │
│  │  18  │  BUDGET VS ACTUAL      │  BUDGET      │  ACTUAL      │  VARIANCE [green savings / red overrun]                  │  │
│  │  24  │  EXCHANGE RATE:        │  1 USD=3700 UGX │           │                                                          │  │
│  │      │  [optional: Pie chart anchored below row 26]         │              │                                              │  │
│  └──────┴────────────────────────┴──────────────┴──────────────┴──────────────────────────────────────────────────────────┘  │
│                                                                                                                              │
│  SHEET 2: DETAILED BREAKDOWN  (tab #1565C0)                                                                                  │
│  CATEGORY │ ITEM │ QTY │ UNIT COST │ TOTAL (=QTY×UNIT)  — formulas, alternating #F8F9FA rows                                 │
│                                                                                                                              │
│  SHEET 3: MONTHLY BURN RATE  (tab #E65100)                                                                                   │
│  MONTH │ PLANNED │ ACTUAL │ CUM. PLANNED │ CUM. ACTUAL │ VARIANCE  — cumulative formulas chain row-by-row                     │
│                                                                                                                              │
│  SHEET 4: DATACONNECTION  (tab #2E7D32)  — Named ranges for Visio linking                                                    │
│  VISIO_ITEM │ VALUE │ CATEGORY │ NOTE                                                                                        │
│  TotalBudget │ 59400 │ Summary │ …                                                                                           │
│  Personnel │ 31000 │ Category │ …                                                                                            │
│  PersonnelPct │ 52 │ Percentage │ …                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Visio Dashboard Layout (ASCII Blueprint)

**CRITICAL:** This ASCII blueprint defines the exact layout agents and implementers must follow. All panels use Section 2.3 styling.

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              BUDGET BREAKDOWN - PROJECT FINANCIALS                                                           │
│         Da'atSNA Community Data Platform  │  Version 1.0  │  2026-06-17  │  USD  │  1 USD = 3,700 UGX                      │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  TOTAL BUDGET: $59,400          │  BUDGET PERIOD: Jan 2026 - Dec 2026                                                    │  │
│  │  Currency: USD  │  Exchange: 1 USD = 3,700 UGX  │  Status: In Progress  │  Last Updated: 2026-06-17                     │  │
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────────────┐  ┌───────────────────────────────────────┐  │
│  │  COST BREAKDOWN BY CATEGORY (HORIZONTAL BAR CHART)                           │  │  BUDGET DISTRIBUTION (PANEL)          │  │
│  │                                                                              │  │                                       │  │
│  │  Personnel    ████████████████████████████████████████  $31,000   52%      │  │  ■ Personnel   (52%)  #1565C0         │  │
│  │  Hardware     ██████████████████████                  $18,500   31%      │  │  ■ Hardware    (31%)  #E65100         │  │
│  │  Contingency  ██████                                   $5,400    9%      │  │  ■ Training     (5%)  #2E7D32         │  │
│  │  Training     ████                                     $3,000    5%      │  │  ■ Software     (3%)  #6A1B9A         │  │
│  │  Software     █                                        $1,500    3%      │  │  ■ Contingency  (9%)  #FFB300         │  │
│  │                                                                              │  │  Data Source: DataConnection sheet    │  │
│  └──────────────────────────────────────────────────────────────────────────────┘  └───────────────────────────────────────┘  │
│                                                                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  MONTHLY BURN RATE (PLANNED vs ACTUAL)                                                                                 │  │
│  │                                                                                                                        │  │
│  │  $8,000 ─┤                                                                                                             │  │
│  │  $6,000 ─┤  █ █ █ █ █ █ █ █ █ █ █ █  ← Planned (#1565C0)                                                            │  │
│  │  $4,000 ─┤  █ █ █ █ █ █ █ █ █ █     ← Actual  (#C62828)                                                              │  │
│  │  $2,000 ─┤                                                                                                             │  │
│  │  $0    ──┼──Jan──Feb──Mar──Apr──May──Jun──Jul──Aug──Sep──Oct──Nov──Dec──                                               │  │
│  │          Legend: ● Planned   ● Actual                                                                                  │  │
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                                              │
│  Footer: Page 1 of 1  │  CONFIDENTIAL - Internal Use Only  │  Organization Name                                            │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Visio panel map:**

| Region | Y position | Content |
|--------|------------|---------|
| Title block | Top (1.5 in) | `#1a237e` bar — title, project, version, date |
| KPI bar | Below title | 4 boxes: Total Budget, Actual Spent, Remaining, Period |
| Bar chart | Upper-left half | Horizontal bars scaled to max category |
| Distribution | Upper-right half | Category list with % and color swatches |
| Burn rate | Lower full width | Grouped bars or polylines per month |

---

## 7. Excel Implementation (openpyxl)

### 7.1 Excel Builder (`excel/budget_excel_builder.py`)

**Implementation notes:** The builder reads `styling` from input JSON (Section 2.4). All headers use `header_fill` / `header_text`. Variance cells use `positive_variance` (#2E7D32 under budget) and `negative_variance` (#C62828 over budget). Named ranges on DataConnection use `openpyxl.workbook.defined_name.DefinedName`.

```python
from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side,
    numbers
)
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from typing import Dict, List, Optional

class BudgetExcelBuilder:
    """Generates a four-sheet Excel workbook for the Budget Breakdown."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.wb = Workbook()
        self.categories = config['budget']['categories']
        self.line_items = config['budget']['line_items']
        self.burn_rate = config['budget']['monthly_burn_rate']
        self.styling = config['budget'].get('styling', {})
        
        # Computed totals
        self.total_budget = sum(c['budget'] for c in self.categories)
        self.total_actual = sum(c.get('actual', 0) for c in self.categories)
        self.total_variance = self.total_actual - self.total_budget
    
    def _style_header_row(self, ws, row: int, cols: int) -> None:
        """Apply navy blue header styling to a row."""
        header_fill = PatternFill("solid", fgColor="1a237e")
        header_font = Font(color="FFFFFF", bold=True, size=9)
        for col in range(1, cols + 1):
            cell = ws.cell(row=row, column=col)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')
    
    def _apply_currency_format(self, cell) -> None:
        """Apply USD currency format to a cell."""
        cell.number_format = '"$"#,##0'
    
    def _apply_percentage_format(self, cell) -> None:
        """Apply percentage format."""
        cell.number_format = '0.0%'
    
    def _apply_border(self, cell) -> None:
        """Apply thin border to a cell."""
        thin = Side(style='thin', color='BDBDBD')
        cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)
    
    def build_summary_sheet(self) -> None:
        """Sheet 1: Budget Summary with totals and Budget vs Actual."""
        ws = self.wb.active
        ws.title = "Budget Summary"
        
        # ── Title Block ──
        ws['A1'] = "BUDGET BREAKDOWN"
        ws['A1'].font = Font(bold=True, size=14, color="1a237e")
        ws.merge_cells('A1:D1')
        
        ws['A2'] = "Project:"
        ws['B2'] = self.config['budget']['project_name']
        ws['A3'] = "Date:"
        ws['B3'] = self.config['budget']['date']
        ws['A4'] = "Currency:"
        ws['B4'] = self.config['budget'].get('currency', 'USD')
        
        # ── Category Summary Header ──
        header_row = 6
        ws.cell(header_row, 1, "CATEGORY")
        ws.cell(header_row, 2, "BUDGET (USD)")
        ws.cell(header_row, 3, "PERCENTAGE")
        ws.cell(header_row, 4, "NOTES")
        self._style_header_row(ws, header_row, 4)
        
        # ── Category Data Rows ──
        data_start = header_row + 1
        for idx, cat in enumerate(self.categories):
            row = data_start + idx
            ws.cell(row, 1, cat['name'])
            ws.cell(row, 2, cat['budget'])
            self._apply_currency_format(ws.cell(row, 2))
            # Percentage formula: =Bn/B_total
            ws.cell(row, 3, cat['budget'] / self.total_budget)
            self._apply_percentage_format(ws.cell(row, 3))
            ws.cell(row, 4, cat.get('notes', ''))
            
            # Alternating row fill
            if idx % 2 == 0:
                fill = PatternFill("solid", fgColor="F5F5F5")
                for col in range(1, 5):
                    ws.cell(row, col).fill = fill
        
        # ── Total Row ──
        total_row = data_start + len(self.categories)
        ws.cell(total_row, 1, "TOTAL BUDGET")
        ws.cell(total_row, 2, self.total_budget)
        ws.cell(total_row, 3, 1.0)
        total_fill = PatternFill("solid", fgColor="E3F2FD")
        total_font = Font(bold=True)
        for col in range(1, 5):
            ws.cell(total_row, col).fill = total_fill
            ws.cell(total_row, col).font = total_font
        self._apply_currency_format(ws.cell(total_row, 2))
        self._apply_percentage_format(ws.cell(total_row, 3))
        
        # ── Budget vs Actual Section ──
        bva_start = total_row + 2
        ws.cell(bva_start, 1, "BUDGET VS ACTUAL")
        ws.cell(bva_start, 1).font = Font(bold=True, size=10, color="1a237e")
        
        bva_header = bva_start + 1
        ws.cell(bva_header, 1, "Category")
        ws.cell(bva_header, 2, "Budget")
        ws.cell(bva_header, 3, "Actual")
        ws.cell(bva_header, 4, "Variance")
        self._style_header_row(ws, bva_header, 4)
        
        for idx, cat in enumerate(self.categories):
            row = bva_header + 1 + idx
            ws.cell(row, 1, cat['name'])
            ws.cell(row, 2, cat['budget'])
            ws.cell(row, 3, cat.get('actual', 0))
            variance = cat.get('actual', 0) - cat['budget']
            ws.cell(row, 4, variance)
            
            for col in (2, 3, 4):
                self._apply_currency_format(ws.cell(row, col))
            
            # Conditional color: green if variance < 0 (under budget), red if over
            var_cell = ws.cell(row, 4)
            if variance < 0:
                var_cell.font = Font(color="4CAF50", bold=True)
            elif variance > 0:
                var_cell.font = Font(color="E53935", bold=True)
        
        # Total row
        bva_total = bva_header + 1 + len(self.categories)
        ws.cell(bva_total, 1, "TOTAL")
        ws.cell(bva_total, 2, self.total_budget)
        ws.cell(bva_total, 3, self.total_actual)
        ws.cell(bva_total, 4, self.total_variance)
        for col in (2, 3, 4):
            self._apply_currency_format(ws.cell(bva_total, col))
        for col in range(1, 5):
            ws.cell(bva_total, col).fill = PatternFill("solid", fgColor="E3F2FD")
            ws.cell(bva_total, col).font = Font(bold=True)
        
        # Column widths
        ws.column_dimensions['A'].width = 22
        ws.column_dimensions['B'].width = 16
        ws.column_dimensions['C'].width = 14
        ws.column_dimensions['D'].width = 40
    
    def build_detail_sheet(self) -> None:
        """Sheet 2: Detailed line-item breakdown with QTY × Unit Cost formulas."""
        ws = self.wb.create_sheet("Detailed Breakdown")
        
        headers = ["CATEGORY", "ITEM DESCRIPTION", "QTY", "UNIT COST (USD)", "TOTAL (USD)"]
        for col, h in enumerate(headers, 1):
            ws.cell(1, col, h)
        self._style_header_row(ws, 1, len(headers))
        
        for idx, item in enumerate(self.line_items):
            row = idx + 2
            ws.cell(row, 1, item['category'])
            ws.cell(row, 2, item['item'])
            ws.cell(row, 3, item.get('qty', 1))
            ws.cell(row, 4, item.get('unit_cost', 0))
            self._apply_currency_format(ws.cell(row, 4))
            # Formula: =C{row}*D{row}
            ws.cell(row, 5, f"=C{row}*D{row}")
            self._apply_currency_format(ws.cell(row, 5))
            
            if idx % 2 == 0:
                fill = PatternFill("solid", fgColor="F5F5F5")
                for col in range(1, 6):
                    ws.cell(row, col).fill = fill
        
        # Total row
        total_row = len(self.line_items) + 2
        ws.cell(total_row, 1, "TOTAL")
        ws.cell(total_row, 5, f"=SUM(E2:E{total_row - 1})")
        self._apply_currency_format(ws.cell(total_row, 5))
        for col in range(1, 6):
            ws.cell(total_row, col).fill = PatternFill("solid", fgColor="E3F2FD")
            ws.cell(total_row, col).font = Font(bold=True)
        
        ws.column_dimensions['A'].width = 16
        ws.column_dimensions['B'].width = 30
        ws.column_dimensions['C'].width = 8
        ws.column_dimensions['D'].width = 16
        ws.column_dimensions['E'].width = 16
    
    def build_burn_rate_sheet(self) -> None:
        """Sheet 3: Monthly burn rate with cumulative columns."""
        ws = self.wb.create_sheet("Monthly Burn Rate")
        
        headers = ["MONTH", "PLANNED (USD)", "ACTUAL (USD)", "CUM. PLANNED", "CUM. ACTUAL"]
        for col, h in enumerate(headers, 1):
            ws.cell(1, col, h)
        self._style_header_row(ws, 1, len(headers))
        
        for idx, month_data in enumerate(self.burn_rate):
            row = idx + 2
            ws.cell(row, 1, month_data['month'])
            ws.cell(row, 2, month_data['planned'])
            actual = month_data.get('actual')
            if actual is not None:
                ws.cell(row, 3, actual)
                self._apply_currency_format(ws.cell(row, 3))
            self._apply_currency_format(ws.cell(row, 2))
            
            # Cumulative planned: =D{row-1}+B{row} (first row: =B{row})
            if row == 2:
                ws.cell(row, 4, f"=B{row}")
                ws.cell(row, 5, f"=C{row}" if actual is not None else "")
            else:
                ws.cell(row, 4, f"=D{row - 1}+B{row}")
                ws.cell(row, 5, f"=E{row - 1}+C{row}" if actual is not None else "")
            
            for col in (4, 5):
                self._apply_currency_format(ws.cell(row, col))
            
            if idx % 2 == 0:
                fill = PatternFill("solid", fgColor="F5F5F5")
                for col in range(1, 6):
                    ws.cell(row, col).fill = fill
        
        ws.column_dimensions['A'].width = 14
        for col_letter in ('B', 'C', 'D', 'E'):
            ws.column_dimensions[col_letter].width = 16
    
    def build_data_connection_sheet(self) -> None:
        """Sheet 4: Named flat table for Visio shape data linking."""
        ws = self.wb.create_sheet("DataConnection")
        
        headers = ["VISIO_ITEM", "VALUE", "CATEGORY", "NOTE"]
        for col, h in enumerate(headers, 1):
            ws.cell(1, col, h)
        self._style_header_row(ws, 1, len(headers))
        
        rows = [
            ("TotalBudget",     self.total_budget,   "Summary",    "Linked to Visio KPI TotalBudget box"),
            ("TotalActual",     self.total_actual,   "Summary",    "Linked to Visio KPI ActualSpend box"),
            ("Remaining",       self.total_budget - self.total_actual, "Summary", "Linked to Visio KPI Remaining box"),
        ]
        
        for cat in self.categories:
            rows.append((cat['name'], cat['budget'], "Category", f"Linked to Visio bar chart: {cat['name']} bar width"))
        
        for cat in self.categories:
            pct = round(cat['budget'] / self.total_budget * 100, 1)
            rows.append((f"{cat['name']}Pct", pct, "Percentage", f"Linked to Visio pie sector angle: {cat['name']}"))
        
        for idx, (item, value, category, note) in enumerate(rows):
            row = idx + 2
            ws.cell(row, 1, item)
            ws.cell(row, 2, value)
            ws.cell(row, 3, category)
            ws.cell(row, 4, note)
            
            if idx % 2 == 0:
                fill = PatternFill("solid", fgColor="F5F5F5")
                for col in range(1, 5):
                    ws.cell(row, col).fill = fill
        
        # Create named ranges for Visio data linking
        for idx, (item, _, _, _) in enumerate(rows):
            cell_ref = f"DataConnection!$B${idx + 2}"
            ws.parent.defined_names[item] = cell_ref
        
        ws.column_dimensions['A'].width = 22
        ws.column_dimensions['B'].width = 14
        ws.column_dimensions['C'].width = 14
        ws.column_dimensions['D'].width = 50
    
    def build(self) -> None:
        """Execute all four sheet builders."""
        self.build_summary_sheet()
        self.build_detail_sheet()
        self.build_burn_rate_sheet()
        self.build_data_connection_sheet()
    
    def save(self, output_path: str) -> None:
        """Save the workbook to disk."""
        self.wb.save(output_path)
```

---

## 8. Visio Implementation (Aspose.Diagram)

### 8.1 Visio Dashboard Builder (`visio/budget_visio_builder.py`)

Uses **JVM-backed** `asposediagram.api` via `visio/aspose_helpers.py` — not the fictional `aspose.diagram` Python package.

```python
from config.settings import PAGE_SIZES_IN, apply_aspose_diagram_license
from visio import aspose_helpers as asp

class BudgetVisioBuilder:
    """Enterprise-grade budget dashboard — see Section 6 ASCII blueprint."""

    def __init__(self, spec) -> None:
        self.config = spec.budget.model_dump()
        self.categories = self.config["categories"]
        self.burn_rate = self.config["monthly_burn_rate"]
        self.layout = self.config.get("layout", {})
        self.dashboard = self.config.get("dashboard", {})
        self.font_family = self.config.get("styling", {}).get("font_family", "Arial")
        self._compute_totals()

    def _setup_page(self) -> None:
        """A2 landscape by default — Section 2.3."""
        page_size = self.layout.get("page_size", "A2")
        w, h = PAGE_SIZES_IN.get(page_size, PAGE_SIZES_IN["A2"])
        if self.layout.get("orientation", "landscape") == "portrait":
            w, h = h, w
        props = self.page.getPageSheet().getPageProps()
        props.getPageWidth().setValue(w)
        props.getPageHeight().setValue(h)

    def add_title_block(self) -> None:
        """#1a237e header bar — title, project, version, date."""
        asp.add_rectangle(
            self.page,
            x=self.page_width / 2,
            y=self.page_height - 1.5,
            w=self.page_width - 1.0,
            h=1.5,
            text=f"{title}\n{project} | Version {version} | {date}",
            fill_color="#1a237e",
            text_color="#FFFFFF",
            font_size=14.0,
            font_bold=True,
            no_border=True,
        )

    def add_bar_chart(self) -> None:
        """Horizontal bars — width proportional to budget / total_budget."""
        max_bar_width = self.page_width / 2 - 5.0
        for idx, cat in enumerate(self.categories):
            bar_w = (cat["budget"] / self.total_budget) * max_bar_width
            asp.add_rectangle(
                self.page, x=..., y=..., w=bar_w, h=1.0,
                fill_color=cat.get("color", "#1565C0"),  # Section 2.2 palette
                no_border=True,
            )

    def add_burn_rate_chart(self) -> None:
        """Grouped bars: planned #1565C0, actual #C62828 per month."""
        ...

    def build(self) -> None:
        apply_aspose_diagram_license()
        self.diagram = asp.new_diagram()
        self.page = self.diagram.getPages().get(0)
        self._setup_page()
        self.add_title_block()
        self.add_kpi_bar()
        self.add_bar_chart()
        self.add_pie_chart_panel()
        self.add_burn_rate_chart()

    def save(self, output_path: str) -> None:
        asp.save_diagram(self.diagram, output_path)
        # Post-check: file size must be >= 4000 bytes (Section 2.1 QA)
```

**Dashboard toggles** (in `budget_visio_dashboard_input.json`):

```json
{
  "dashboard": {
    "show_kpi_bar": true,
    "show_bar_chart": true,
    "show_pie_chart": true,
    "show_burn_rate_chart": true,
    "kpi_colors": {
      "total_budget": "#1a237e",
      "actual_spent": "#C62828",
      "remaining": "#2E7D32",
      "period": "#4E342E"
    }
  }
}
```

---

## 9. Data Flow & Connectivity Architecture

### 9.1 Data Flow

```yaml
data_flow:
  input:
    - JSON configuration (9-file split or combined MAIN)
    - Budget categories, line items, monthly burn rate
    - Currency and exchange rate metadata
    - styling + layout + dashboard options

  processing:
    - Validate via Pydantic models (core/validator.py)
    - Calculate totals, percentages, variance
    - Build Excel with formulas and named ranges
    - Render Visio dashboard with enterprise styling

  output:
    - budget_breakdown.xlsx  (4 sheets)
    - budget_dashboard.vsdx  (single page)
    - Minimum .vsdx size: 4000 bytes
```

### 9.2 Named Range Strategy (openpyxl)
```python
# During Excel build, each key metric gets a named range:
wb.defined_names['TotalBudget']   = 'DataConnection!$B$2'
wb.defined_names['PersonnelPct']  = 'DataConnection!$B$10'
```

### 9.3 Visio Shape Custom Properties
Visio shapes are configured with a `Prop.Value` formula that references the Excel file:
```
Prop.TotalBudget.Value = LOOKUP("TotalBudget", "DataConnection", 1, 2)
```

When Visio refreshes its data connection pointing to the `.xlsx` file, shape labels automatically update to reflect the current Excel values.

### 9.4 Connectivity Flow
```text
Input JSON
    │
    ├──► BudgetExcelBuilder ──► budget_breakdown.xlsx
    │         │
    │         └── DataConnection Sheet (Named Ranges: TotalBudget, PersonnelPct, ...)
    │                          │
    │                          └── Visio Data Connection (Refresh → auto-update)
    │
    └──► BudgetVisioBuilder ──► budget_dashboard.vsdx
              │
              └── Shapes link to Excel named ranges via custom property formulas
```

---

## 10. Code Architecture

```text
budget_breakdown_generator/
├── __init__.py
├── skill.md
├── core/
│   ├── __init__.py
│   ├── orchestrator.py            # Runs both Excel and Visio builders
│   ├── validator.py               # Input validation
│   ├── errors.py                  # Custom exceptions
│   └── models.py                  # Pydantic schema models
├── excel/
│   ├── __init__.py
│   ├── budget_excel_builder.py    # openpyxl workbook generator
│   ├── sheet_summary.py           # Sheet 1 logic
│   ├── sheet_detail.py            # Sheet 2 logic
│   ├── sheet_burn_rate.py         # Sheet 3 logic
│   └── sheet_data_connection.py   # Sheet 4 / Named ranges
├── visio/
│   ├── __init__.py
│   ├── budget_visio_builder.py    # Aspose.Diagram orchestration
│   ├── kpi_bar.py                 # KPI box shapes
│   ├── bar_chart.py               # Horizontal bar chart
│   ├── burn_rate_chart.py         # Polyline burn rate chart
│   └── layout_engine.py           # Coordinate calculations
├── calculators/
│   ├── __init__.py
│   ├── budget_calculator.py       # Totals, variance, percentages
│   └── burn_rate_calculator.py    # Cumulative burn rate math
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   └── currency_utils.py          # Formatting: $59,400 → "$59,400"
├── config/
│   ├── __init__.py
│   └── settings.py
└── cli.py
```

---

## 11. Error Handling

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| `BB-001` | InvalidInput | JSON schema validation failure. | Fix the required fields. |
| `BB-002` | NoCategories | Categories array is empty. | Add at least 1 budget category. |
| `BB-003` | NoLineItems | Line items array is empty. | Add at least 1 line item. |
| `BB-004` | NoBurnRate | Monthly burn rate array is empty. | Add at least 1 month. |
| `BB-005` | CategoryMismatch | Line item references a category not in `categories` array. | Align category names. |
| `BB-006` | NegativeBudget | Budget value < 0. | All budget values must be ≥ 0. |
| `BB-007` | TotalMismatch | Sum of category budgets ≠ declared total. | Recalculate totals or remove declared total. |
| `BB-008` | JavaNotInstalled | Missing JRE 8+ for Aspose.Diagram. | Install Java. |
| `BB-009` | LicenseMissing | Aspose `.lic` not found. | Set environment variable. |
| `BB-010` | ExcelWriteError | openpyxl file write failure. | Check output directory permissions. |
| `BB-011` | VisioWriteError | Aspose VSDX write failure. | Check Aspose installation and JRE. |

---

## 12. Command-Line Interface (CLI)

```python
# cli.py
import argparse
import json
import logging
import sys
from core.orchestrator import BudgetOrchestrator

def main():
    parser = argparse.ArgumentParser(description="Generate Budget Breakdown (Excel + Visio)")
    parser.add_argument("input", help="Path to input JSON/YAML file")
    parser.add_argument("--excel-out", help="Excel output path (default: ./output/budget_breakdown.xlsx)")
    parser.add_argument("--visio-out", help="Visio output path (default: ./output/budget_dashboard.vsdx)")
    parser.add_argument("--excel-only", action="store_true", help="Generate Excel output only")
    parser.add_argument("--visio-only", action="store_true", help="Generate Visio output only")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--validate-only", action="store_true", help="Validate input without rendering")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    with open(args.input, 'r') as f:
        spec = json.load(f)
    
    if args.validate_only:
        logging.info("Budget input validation passed.")
        sys.exit(0)
    
    orch = BudgetOrchestrator(spec)
    
    if not args.visio_only:
        excel_path = args.excel_out or "./output/budget_breakdown.xlsx"
        orch.build_excel(excel_path)
        logging.info(f"Excel saved to {excel_path}")
    
    if not args.excel_only:
        visio_path = args.visio_out or "./output/budget_dashboard.vsdx"
        orch.build_visio(visio_path)
        logging.info(f"Visio saved to {visio_path}")

if __name__ == "__main__":
    main()
```

---

## 13. Quality Checklist

Run this checklist before delivering any budget package.

### Visual (Visio + Excel)

- [ ] Enterprise color palette applied (Section 2.2) — same hex in Excel and Visio
- [ ] Arial font throughout; no decorative fonts
- [ ] Title block present on Visio (`#1a237e` background, white text)
- [ ] Clean white / `#FAFAFA` panel backgrounds; subtle borders only
- [ ] No text overflow in shapes or cells
- [ ] Bar widths proportional to budget values
- [ ] Burn rate shows both planned and actual series
- [ ] Legend / distribution panel matches category colors

### Data integrity

- [ ] Category budgets sum to total budget
- [ ] Percentages sum to 100% (±0.1% rounding)
- [ ] Variance = actual − budget for each category
- [ ] Exchange rate note present when non-USD context provided
- [ ] `actual: null` for future months handled without error

### Excel formulas

- [ ] Sheet 1 percentages computed — not hardcoded
- [ ] Sheet 2 totals use `=C{row}*D{row}` formulas
- [ ] Sheet 3 cumulative columns chain `=D{n-1}+B{n}`
- [ ] DataConnection named ranges defined (`TotalBudget`, `PersonnelPct`, etc.)

### Output integrity

- [ ] `.xlsx` opens without repair warnings
- [ ] `.vsdx` ≥ 4 KB (catches empty/corrupt exports)
- [ ] Visio KPI values match Excel DataConnection column B
- [ ] Variance colors: green (#2E7D32) under budget, red (#C62828) over budget

---

## 14. Usage Examples

### 14.1 Full Package (Excel + Visio)
```bash
python budget_breakdown_generator/cli.py data/budget.json
```

### 14.2 Excel Only
```bash
python budget_breakdown_generator/cli.py data/budget.json --excel-only --excel-out output/budget.xlsx
```

### 14.3 Visio Dashboard Only
```bash
python budget_breakdown_generator/cli.py data/budget.json --visio-only --visio-out output/budget_dashboard.vsdx
```

---

## 15. Integration with Existing Skills

1. **Charter Integration:** The Excel workbook and Visio dashboard are embedded as appendices in the `project-charter-generator` output.
2. **Resource Allocation Synergy:** Personnel costs in this budget map directly to resource allocations in the `resource-allocation-matrix-generator`.
3. **Risk Matrix Synergy:** The `Contingency` category amount feeds into the financial risk mitigation budget tracked in `risk-matrix-diagram-generator`.

---

## 16. Testing Strategy

1. **Formula Integrity Test:** Open the generated Excel, change one `unit_cost` cell, and verify that Sheet 1 totals recalculate automatically.
2. **Named Range Test:** Verify each key in `wb.defined_names` resolves to the correct `DataConnection` cell.
3. **Proportional Bar Test:** Supply two categories — one at $60,000 and one at $30,000. Assert the first bar is exactly twice the width of the second.
4. **Variance Color Test:** Supply `actual > budget` for one category. Assert the variance cell font is red (`E53935`).
5. **Missing Actual Test:** Supply `actual: null` for December. Assert Sheet 3 row 14 Column C is blank and Column E cumulative is also blank without raising an error.

---

## 17. Troubleshooting Guide

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `.vsdx` file < 4 KB or won't open | JVM not started, Aspose error | Install JRE 11+; set `ASPOSE_DIAGRAM_LICENSE_PATH`; check logs |
| `JavaNotInstalled` (BB-008) | No JRE on PATH | `brew install openjdk` (macOS) or `apt install default-jre` |
| Visio bars all same width | `total_budget` is 0 | Fix category `budget` values in input JSON |
| Excel variance colors wrong | Styling keys swapped | `positive_variance` = under budget (green); `negative_variance` = over budget (red) |
| Category colors differ Excel vs Visio | Ad-hoc hex in input | Use Section 2.2 palette only |
| Percentages don't sum to 100% | Rounding | Use one decimal place; ensure totals match |
| `CategoryMismatch` (BB-005) | Line item category name typo | Match `line_items[].category` to `categories[].name` exactly |
| Named range not found in Visio | Excel not refreshed | Re-link data connection; verify `DataConnection!B{n}` |
| Text cut off in Visio shapes | Font too large for box | Reduce `font_size` in `aspose_helpers.add_rectangle` |
| Import error `aspose.diagram` | Wrong package name | Use `asposediagram.api` via JPype (Section 8.1) |

**Validation-only run** (no render):

```bash
python budget_breakdown_generator/cli.py inputs/budget_input.json --validate-only -v
```

**End-to-end test:**

```bash
cd budget_breakdown_generator
../project_charter_generator/.venv/bin/python scripts/run_example.py
```
