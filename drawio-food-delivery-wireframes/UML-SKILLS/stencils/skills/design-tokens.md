# Design Tokens — Color, Radius, Stroke, Type

The complete visual rulebook. One consistent system — color, radius, stroke, type — applied across every shape and diagram so the whole library reads as one thing instead of hundreds of one-off drawings, in both light and dark mode. Palette originates from a reference brand image; everything else derives from it.

## Table of Contents
1. [Color Tokens](#1-color-tokens)
2. [Corner Radius Rules](#2-corner-radius-rules)
3. [Stroke & Line Weights](#3-stroke--line-weights)
4. [Typography Scale](#4-typography-scale)
5. [Fill & Contrast Principle](#5-fill--contrast-principle)
6. [Connector & Line-Style Meaning](#6-connector--line-style-meaning)
7. [Sizing & Composition](#7-sizing--composition)
8. [Category Notes](#8-category-notes)

## 1. Color Tokens

| Token | Light value | Dark value | Used for |
|---|---|---|---|
| `canvas` | `#FFFFFF` | `#0D0D0D` | Page/artboard background |
| `shape-fill` | `#E5E5E5` | `#1E1E1E` | Fill for every shape body |
| `shape-stroke` | `#1A1A1A` | `#F2F2F2` | Shape outlines, primary text |
| `text-muted` | `#8A8A85` | `#8A8A85` | Captions, labels, secondary text (same value both modes — this is what keeps light/dark feeling like one system) |
| `connector` | `#1A1A1A` | `#F2F2F2` | Lines, arrows, dividers |

Never introduce a new color outside this table for a standard shape. If a category genuinely needs more (see §8), extend the table deliberately — don't improvise inline mid-diagram.

In `shape_kit.py` these are `L_CANVAS`, `L_FILL`, `L_STROKE`, `L_MUTED`, `D_CANVAS`, `D_FILL`, `D_STROKE`, `D_MUTED`.

## 2. Corner Radius Rules

Radius is decided by geometry, not by preference:

| Shape family | Radius | Reasoning |
|---|---|---|
| Rectangular process/task/module/container | `rx="8"` | Friendly without losing edges |
| Structural/data shapes (UML class, ER entity, record) | `rx="6"` | Slightly tighter — reads as "structural," not "soft" |
| Terminator / stadium shapes | `rx=height/2` (fully rounded) | Inherent to the shape, not a style choice |
| Angular shapes (diamond, triangle, parallelogram, hexagon, pentagon) | **No rounding** | Rounding a diamond softens it into a blob and kills its meaning as a decision/branch symbol |
| Circles, ovals, ellipses | N/A | Already curved; no radius property needed |

## 3. Stroke & Line Weights

| Element | Weight |
|---|---|
| Shape outline | `1.5px` |
| Connector / flow line | `2px` |
| Emphasis line (e.g. critical path, active state) | `2.5–3px` |
| Divider line inside a composite shape (UML compartments, fragment dividers) | `1–1.2px` |
| Lifeline (sequence diagrams) | `1.3px`, dashed |
| Activation bar outline | `1.3px` |

## 4. Typography Scale

One sans-serif family throughout (`Helvetica, Arial, sans-serif` in `shape_kit.FF`, or a licensed/embedded brand face):

| Role | Size | Weight | Color token | Notes |
|---|---|---|---|---|
| Shape label (primary content) | `12px` | 400–500 | `shape-stroke` | Centered inside most shapes |
| Small/tight label (diamonds, cylinders, cramped shapes) | `10px` | 600 | `shape-stroke` | Used where the shape geometry leaves less room |
| Micro/attribute text (UML fields, ER attributes) | `8px` | 400 | `shape-stroke` | Left-aligned, inside compartments |
| Caption / specimen label (names the shape type, sits below/outside it) | `10.5px` | 400 | `text-muted`, `+0.3px` letter-spacing | Never inside the shape itself |
| Message / edge label (sequence diagrams, flowchart branch labels) | `10–10.5px` | 400–600 | `shape-stroke` | Centered on or just above the line |
| Panel heading | `18–24px` | 700 | `shape-stroke` | Section/sheet titles only |
| Panel subheading | `11–11.5px` | 400 | `text-muted` | One line, under the heading |

## 5. Fill & Contrast Principle

- Flat fills only — no gradients, no drop shadows, no textures.
- `shape-fill` should read as a clearly distinct, moderate step off `canvas` (light: pale gray off white; dark: dark gray off near-black) — enough to separate the shape from the page without looking like a solid block.
- Diagram shapes keep a **visible stroke** (`shape-stroke`, 1.5px) even where a purely decorative reference wouldn't need one — connectors need a clear boundary to terminate against, and shapes need to read correctly in grayscale or low contrast. This is a deliberate, functional departure from purely decorative card/brand treatments.

## 6. Connector & Line-Style Meaning

Line style is tied to meaning, never decoration:

| Style | Meaning |
|---|---|
| Solid line, filled arrowhead | Standard flow / synchronous message |
| Solid line, open (stick) arrowhead | Async message / directed association |
| Dashed line, open arrowhead | Return message / dependency |
| Dashed line, hollow triangle | Realization / interface implementation |
| Solid line, hollow triangle | Generalization / inheritance |
| Solid line, hollow diamond (at line end) | Aggregation |
| Solid line, filled diamond (at line end) | Composition |
| Dashed line, open arrowhead → new box | Create message (sequence diagrams) |
| Small X on a lifeline | Destroy message (sequence diagrams) |

## 7. Sizing & Composition

- Base unit: `8px`. Every shape's width/height should resolve to a multiple of it, so shapes drawn independently still line up when composed into a full diagram later.
- Standard shape footprint for single-concept shapes (process, terminator, entity, event, etc.): **100×50px** internal content box, with **15–20px internal padding** before text starts.
- Composite shapes (UML class, tables) may extend taller in fixed compartment increments (~23px per row) but keep the same 100–130px width band as everything else, so they sit comfortably next to simple shapes in the same diagram.
- For multi-lifeline / multi-column diagrams (sequence diagrams, swimlanes): space columns 220–240px apart minimum — tighter than that and message labels start colliding.
- Any repeated row/column pattern (Gantt rows, table rows, legend entries) is a `<defs>`/`<use>` candidate — see `reusable-components.md`.

## 8. Category Notes

The base system above applies everywhere. A few categories extend it:

- **Flowchart** — pure base system, no extensions.
- **UML** — adds compartment dividers (§3) and the full relationship-line table (§6). The sequence diagram example additionally established: lifelines (dashed, muted), activation bars (thin filled rect, `shape-fill`/`shape-stroke`), self-message loops, and combined-fragment frames (unfilled rect + small cut-corner tab holding the operator keyword).
- **ER / DFD** — adds crow's-foot line-end markers; data stores use a cylinder construction (see `shape_kit.py`'s cylinder shape in the basic-primitives category for the reusable pattern: body rect with no stroke, two side lines, two end ellipses, top ellipse drawn last).
- **BPMN** — event circles vary stroke weight by type (start = thin single, end = thick single, intermediate = double); gateways add an interior glyph (X, O, +) per §2's "no rounding" rule.
- **Network / Cloud / Architecture** — icons may use a slightly bolder `2px` outline to hold up at small sizes; otherwise same tokens.
- **Project Management (Gantt, Kanban, Risk Matrix)** — needs one additional accent color for status/priority. **Not yet specified** — decide and add to §1's table before building this category; don't improvise a color inline. This is also the first category that needs `<defs>`/`<use>` for real (repeated task-bar rows) — see `reusable-components.md`.
- **BI / KPI** — needs a small data-color ramp for charts, which the two-gray system deliberately doesn't provide. Separate spec required before building.
- **Web/UX (wireframes, sitemaps)** — pure base system; treat every element as a rectangle or its content-appropriate primitive.

---

*Companion file: `reusable-components.md` covers `<defs>`/`<use>` architecture — read it before any diagram with 3+ repeated shapes.*
