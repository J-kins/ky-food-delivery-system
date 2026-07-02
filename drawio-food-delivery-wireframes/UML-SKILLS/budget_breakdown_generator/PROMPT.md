# Budget Breakdown Generator — Agent Prompt

Use this file to generate the input JSON required by the **Budget Breakdown Generator**. This generator produces an **Excel workbook** (`.xlsx`) and a **Visio dashboard** (`.vsdx`) from one budget dataset. You must create **nine JSON files**:

- **Four shared data files** (source of truth for numbers)
- **Two Excel-specific files** (styling + Excel MAIN)
- **Two Visio-specific files** (dashboard layout + Visio MAIN)
- **One combined MAIN** (full package for both outputs)

Any agentic AI working on any project can follow this prompt to produce valid inputs.

## Prerequisites

1. **`specifications.json` exists** — generated using [prompt_skill_generator_SKILL.md](../prompt_skill_generator_SKILL.md)
2. **`budget_breakdown` is listed** in `specifications.json → diagrams_to_generate`
3. Read [budget-breakdown-generator-SKILL.md](../budget-breakdown-generator-SKILL.md) for rendering details after input is ready

## What This Generator Produces

| Output | Format | CLI flag | Input MAIN file |
|--------|--------|----------|-----------------|
| Excel workbook | `.xlsx` | `--excel-only` | `budget_excel_input.json` |
| Visio dashboard | `.vsdx` | `--visio-only` | `budget_visio_input.json` |
| Both | `.xlsx` + `.vsdx` | (default) | `budget_input.json` |

| Excel sheet | Shared data file |
|-------------|------------------|
| Budget Summary | `budget_categories_input.json` + header |
| Detailed Breakdown | `budget_line_items_input.json` |
| Monthly Burn Rate | `budget_monthly_burn_rate_input.json` |
| DataConnection | Auto-generated from above |

| Visio element | Shared / Visio data |
|---------------|-------------------|
| KPI bar | categories + header |
| Bar / pie charts | categories (colors) |
| Burn rate chart | `budget_monthly_burn_rate_input.json` |
| Page layout | `budget_visio_dashboard_input.json` |

---

## Output File Locations — READ THIS FIRST

All files live under `projects/<project-slug>/inputs/`:

### Shared data (used by Excel, Visio, and combined MAIN)

| File | Purpose |
|------|---------|
| `budget_metadata_input.json` | Project header only — **no styling, no layout** |
| `budget_categories_input.json` | Category summary rows |
| `budget_line_items_input.json` | Detailed line items (**Excel only**, but defines totals) |
| `budget_monthly_burn_rate_input.json` | Monthly planned/actual burn |

### Excel bundle

| File | Purpose |
|------|---------|
| `budget_excel_styling_input.json` | Excel sheet styling (headers, variance colors) |
| **`budget_excel_input.json`** | **Excel MAIN** — merge for `--excel-only` |

### Visio bundle

| File | Purpose |
|------|---------|
| `budget_visio_dashboard_input.json` | Visio page layout + dashboard/chart options |
| **`budget_visio_input.json`** | **Visio MAIN** — merge for `--visio-only` |

### Combined

| File | Purpose |
|------|---------|
| **`budget_input.json`** | **Full MAIN** — merge for Excel + Visio together |

Example paths (Da'atSNA):

```text
projects/daatsna-community-data-platform/inputs/
├── budget_metadata_input.json              ← shared header
├── budget_categories_input.json            ← shared
├── budget_line_items_input.json            ← Excel data
├── budget_monthly_burn_rate_input.json     ← shared
├── budget_excel_styling_input.json         ← Excel only
├── budget_excel_input.json                 ← Excel MAIN
├── budget_visio_dashboard_input.json       ← Visio only
├── budget_visio_input.json                 ← Visio MAIN
└── budget_input.json                       ← Combined MAIN
```

### How the nine files relate

```text
specifications.json → budget
        │
        ├─► STEP 1  budget_metadata_input.json        (shared header)
        ├─► STEP 2  budget_categories_input.json      (shared)
        ├─► STEP 3  budget_line_items_input.json      (Excel breakdown)
        ├─► STEP 4  budget_monthly_burn_rate_input.json (shared)
        │
        ├─► STEP 5  budget_excel_styling_input.json   (Excel styling)
        └─► STEP 6  budget_visio_dashboard_input.json (Visio layout)
        │
        ├─► STEP 7  MERGE → budget_excel_input.json   (Excel MAIN)
        ├─► STEP 8  MERGE → budget_visio_input.json   (Visio MAIN)
        └─► STEP 9  MERGE → budget_input.json         (Combined MAIN)
```

**Shared data rule:** `categories[]` and `monthly_burn_rate[]` must be **identical** in `budget_excel_input.json`, `budget_visio_input.json`, and `budget_input.json`. Author them once in the split files, then copy into each merge.

---

## Merge rules

### Excel MAIN — `budget_excel_input.json`

```json
{
  "budget": {
    "title": "...",
    "project_name": "...",
    "version": "...",
    "date": "...",
    "currency": "...",
    "exchange_rate_note": "...",
    "budget_period": "...",
    "categories": [ /* budget_categories_input.json */ ],
    "line_items": [ /* budget_line_items_input.json */ ],
    "monthly_burn_rate": [ /* budget_monthly_burn_rate_input.json */ ],
    "styling": { /* budget_excel_styling_input.json */ }
  }
}
```

No `layout` key required for Excel-only runs.

### Visio MAIN — `budget_visio_input.json`

```json
{
  "budget": {
    "title": "...",
    "project_name": "...",
    "version": "...",
    "date": "...",
    "currency": "...",
    "budget_period": "...",
    "categories": [ /* budget_categories_input.json — same as Excel */ ],
    "monthly_burn_rate": [ /* budget_monthly_burn_rate_input.json — same as Excel */ ],
    "line_items": [],
    "layout": { /* budget_visio_dashboard_input.json → budget.layout */ },
    "dashboard": { /* budget_visio_dashboard_input.json → budget.dashboard (optional) */ },
    "styling": {
      "font_family": "Arial"
    }
  }
}
```

Visio builder does **not** read `line_items[]` — only `categories[]` and `monthly_burn_rate[]`. Set `"line_items": []` because the current CLI schema requires the key.

### Combined MAIN — `budget_input.json`

```json
{
  "budget": {
    "...header fields...",
    "categories": [ ... ],
    "line_items": [ ... ],
    "monthly_burn_rate": [ ... ],
    "styling": { /* from budget_excel_styling_input.json */ },
    "layout": { /* from budget_visio_dashboard_input.json */ },
    "dashboard": { /* optional, from budget_visio_dashboard_input.json */ }
  }
}
```

---

## Agent Instructions

You are a project financial documentation specialist. Your task is to generate **nine JSON files**.

### Your workflow

1. Read `projects/<project-slug>/specifications.json` (especially `budget`, `project`, `phases`).
2. **Create shared files** (steps 1–4): metadata → categories → line items → burn rate.
3. **Create `budget_excel_styling_input.json`** — Excel presentation config.
4. **Create `budget_visio_dashboard_input.json`** — Visio page layout and chart options.
5. **Merge `budget_excel_input.json`** — Excel MAIN.
6. **Merge `budget_visio_input.json`** — Visio MAIN (`line_items: []`).
7. **Merge `budget_input.json`** — combined MAIN (superset).
8. Validate cross-file consistency.
9. Write all nine files to disk and confirm each path.

### Critical rules

- **Nine files, not one** — always write all split files and all three MAIN merges.
- **Shared data stays in sync** — categories and burn rate identical across Excel, Visio, and combined MAIN files.
- **Excel owns line items** — author `line_items[]` only in `budget_line_items_input.json`; copy into `budget_excel_input.json` and `budget_input.json`. Use `"line_items": []` in `budget_visio_input.json`.
- **Styling vs layout** — Excel styling in `budget_excel_styling_input.json`; Visio layout in `budget_visio_dashboard_input.json`. Do not mix them in `budget_metadata_input.json`.

---

## Mapping from specifications.json

| specifications.json | Target file | Notes |
|---------------------|-------------|-------|
| `project.name` | `budget_metadata_input.json` | `budget.project_name` |
| `project.version` | metadata | `budget.version` |
| `project.date` | metadata | `YYYY-MM-DD` |
| `project.start_date` + `project.end_date` | metadata | `budget.budget_period` |
| `budget.currency` | metadata | USD, UGX, EUR |
| `budget.categories[]` | `budget_categories_input.json` | Add colors, actual, notes |
| `budget.categories[].items[]` | `budget_line_items_input.json` | Flatten |
| — | `budget_monthly_burn_rate_input.json` | Derive from timeline |
| — | `budget.title` | `"Budget Breakdown - <project.name>"` |
| — | `budget_excel_styling_input.json` | Excel defaults |
| — | `budget_visio_dashboard_input.json` | Visio layout defaults |

### Line item mapping

```json
{
  "category": "<must match categories[].name>",
  "item": "<item.name>",
  "qty": "<item.qty>",
  "unit_cost": "<item.unit_cost>",
  "total": "<item.qty × item.unit_cost>"
}
```

### Default category color palette

`#1a237e`, `#1565C0`, `#2E7D32`, `#E65100`, `#6A1B9A`, `#00695C`, `#C62828`, `#4E342E`

---

## Shared file schemas

### `budget_metadata_input.json` (header only)

```json
{
  "budget": {
    "title": "Budget Breakdown - Project Name",
    "project_name": "string",
    "version": "1.0",
    "date": "YYYY-MM-DD",
    "currency": "USD",
    "exchange_rate_note": "string (optional)",
    "budget_period": "Jan 2026 - Dec 2026"
  }
}
```

### `budget_categories_input.json`

```json
{
  "budget": {
    "categories": [
      {
        "id": "CAT1",
        "name": "Personnel",
        "color": "#1a237e",
        "text_color": "#FFFFFF",
        "budget": 31000,
        "actual": 28500,
        "notes": "Project team salaries and contractors"
      }
    ]
  }
}
```

Minimum **3**, maximum **8** categories.

### `budget_line_items_input.json` (Excel)

```json
{
  "budget": {
    "line_items": [
      {
        "category": "Personnel",
        "item": "Project Manager (6 months)",
        "qty": 6,
        "unit_cost": 5000,
        "total": 30000
      }
    ]
  }
}
```

Minimum **1 line item per category**. `total` = `qty × unit_cost`.

### `budget_monthly_burn_rate_input.json` (Excel + Visio)

```json
{
  "budget": {
    "monthly_burn_rate": [
      { "month": "January", "planned": 4500, "actual": 4200 },
      { "month": "February", "planned": 4500, "actual": null }
    ]
  }
}
```

`planned` sums to total budget (± $100). Full month names. `actual`: `null` for future months.

---

## Excel file schemas

### `budget_excel_styling_input.json`

```json
{
  "budget": {
    "styling": {
      "font_family": "Arial",
      "font_size": 9,
      "header_fill": "#1a237e",
      "header_text": "#FFFFFF",
      "alt_row_fill": "#F5F5F5",
      "total_row_fill": "#E3F2FD",
      "positive_variance": "#4CAF50",
      "negative_variance": "#E53935"
    }
  }
}
```

Used by `BudgetExcelBuilder` for sheet headers, alternating rows, and variance conditional colors.

### `budget_excel_input.json` (Excel MAIN)

Merge: metadata + categories + line_items + monthly_burn_rate + excel styling.

```bash
python budget_breakdown_generator/cli.py budget_excel_input.json --excel-only
```

---

## Visio file schemas

### `budget_visio_dashboard_input.json`

```json
{
  "budget": {
    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5
    },
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
}
```

- `layout` — used by `BudgetVisioBuilder` for page dimensions (`A2` landscape default).
- `dashboard` — optional; controls which chart panels render. Builder uses sensible defaults if omitted.

### `budget_visio_input.json` (Visio MAIN)

Merge: metadata + categories + monthly_burn_rate + visio dashboard (layout + dashboard). Set `"line_items": []`.

```bash
python budget_breakdown_generator/cli.py budget_visio_input.json --visio-only
```

---

## Combined MAIN — `budget_input.json`

Full merge of all sections. Use for generating **both** Excel and Visio in one run:

```bash
python budget_breakdown_generator/cli.py budget_input.json
```

Reference: [examples/sample_input.json](examples/sample_input.json)

---

## Validation Rules

### Cross-file consistency

1. `categories[]` identical in `budget_excel_input.json`, `budget_visio_input.json`, and `budget_input.json`
2. `monthly_burn_rate[]` identical across all three MAIN files
3. Header fields identical across all three MAIN files
4. `budget_visio_input.json` has `"line_items": []` (empty — Visio does not use line items; key required by current validator)
5. `budget_excel_input.json` has **no** `layout` (optional) but **must** have `styling`
6. `budget_input.json` includes both `styling` and `layout`
7. Category names in `line_items[].category` match `categories[].name`
8. Sum of category budgets = sum of line item totals = sum of planned burn (± $100)

### Per-section rules

9. At least 3 categories, 1 line item per category, 1 burn-rate month
10. Every line item: `total` = `qty × unit_cost`
11. Category `budget` = sum of its line items
12. Dates in `YYYY-MM-DD` format; JSON valid

Optional validation:

```bash
python budget_breakdown_generator/cli.py projects/<slug>/inputs/budget_input.json --validate-only
python budget_breakdown_generator/cli.py projects/<slug>/inputs/budget_excel_input.json --validate-only
python budget_breakdown_generator/cli.py projects/<slug>/inputs/budget_visio_input.json --validate-only
```

---

## Quick Reference Card

| File | Bundle | Used by |
|------|--------|---------|
| `budget_metadata_input.json` | Shared | All merges |
| `budget_categories_input.json` | Shared | Excel + Visio |
| `budget_line_items_input.json` | Shared (Excel data) | Excel only |
| `budget_monthly_burn_rate_input.json` | Shared | Excel + Visio |
| `budget_excel_styling_input.json` | Excel | Excel merge |
| `budget_excel_input.json` | **Excel MAIN** | `--excel-only` |
| `budget_visio_dashboard_input.json` | Visio | Visio merge |
| `budget_visio_input.json` | **Visio MAIN** | `--visio-only` |
| `budget_input.json` | **Combined MAIN** | Full package |

---

## After Generating Input

```bash
# Full package (Excel + Visio) — use combined MAIN
python budget_breakdown_generator/cli.py \
  projects/<project-slug>/inputs/budget_input.json \
  -o projects/<project-slug>/output

# Excel only — use Excel MAIN
python budget_breakdown_generator/cli.py \
  projects/<project-slug>/inputs/budget_excel_input.json \
  --excel-only -o projects/<project-slug>/output

# Visio only — use Visio MAIN
python budget_breakdown_generator/cli.py \
  projects/<project-slug>/inputs/budget_visio_input.json \
  --visio-only -o projects/<project-slug>/output
```

When editing: update the relevant split file(s), re-merge the affected MAIN file(s), then re-run CLI.

---

## Integration Notes

- Primary upstream: `specifications.json → budget`
- [project_charter_generator/PROMPT.md](../project_charter_generator/PROMPT.md) — embeds budget summary
- [resource_allocation_generator/PROMPT.md](../resource_allocation_generator/PROMPT.md) — personnel line items align with staffing
- [gantt_chart_generator/PROMPT.md](../gantt_chart_generator/PROMPT.md) — burn rate follows phase timeline

---

## Copy-Ready Agent Prompt

```
You are a project financial documentation specialist. Your task is to generate NINE JSON input files for the Budget Breakdown Generator (Excel workbook + Visio dashboard).

Read specifications.json or the project description below. Follow budget_breakdown_generator/PROMPT.md exactly.

## The Project

**Project Name:** [INSERT PROJECT NAME]
**Total Budget:** [AMOUNT AND CURRENCY]
**Budget Period:** [START - END]
**Categories / Line Items:** [DESCRIBE OR REFER TO SPEC]

## Deliverables — YOU MUST CREATE ALL NINE FILES

### Shared data (author first)
1. budget_metadata_input.json           ← header only (no styling/layout)
2. budget_categories_input.json
3. budget_line_items_input.json         ← Excel Detailed Breakdown
4. budget_monthly_burn_rate_input.json  ← Excel + Visio charts

### Excel bundle
5. budget_excel_styling_input.json      ← Excel sheet styling only
6. budget_excel_input.json              ← Excel MAIN (merge 1+2+3+4+5)

### Visio bundle
7. budget_visio_dashboard_input.json    ← Visio layout + dashboard options
8. budget_visio_input.json              ← Visio MAIN (merge 1+2+4+7; line_items: [])

### Combined
9. budget_input.json                    ← Full MAIN (merge all; both outputs)

## Workflow

1. Write shared split files 1–4 from specifications.json
2. Write Excel styling (5) and Visio dashboard config (7)
3. Merge budget_excel_input.json (includes line_items + styling)
4. Merge budget_visio_input.json (categories + burn rate + layout; line_items: [])
5. Merge budget_input.json (superset: everything)
6. Verify categories[] and monthly_burn_rate[] match across all three MAIN files

## Validation Rules

1. Nine files on disk — not just the combined file
2. budget_visio_input.json must use `"line_items": []` (not populated line items)
3. budget_excel_input.json must contain styling; budget_visio_input.json must contain layout
4. categories and monthly_burn_rate identical across excel, visio, and combined MAIN files
5. Category names match between categories and line_items
6. Totals reconcile: category budgets = line item sums = planned burn sum

## Response Format

Confirm all nine file paths. Report category count, line item count, month count.

Return budget_input.json (combined MAIN) in a final JSON code block.

Now, generate all nine budget input JSON files.
```
