# Shape & Diagram SVG Design Guideline (General)

This is the base visual style system for every SVG you'll build from `diagram-shapes-stencils-master-list.md` and `diagram-types-and-use-cases.md` — the UML boxes, flowchart symbols, ER entities, BPMN elements, network icons, and everything else in those two files. Palette and visual language are pulled from your reference image (light-gray-on-white / dark-gray-on-black, rounded corners, clean sans-serif, muted captions). This is the general spec — individual per-shape guidelines come after this. See `shape-style-specimen-sheet.svg` for this applied to 10 sample shapes.

## 1. Purpose & Scope

One consistent rulebook — color, radius, stroke, type — applied across hundreds of shapes so the whole library reads as one system instead of hundreds of one-off drawings, in both light and dark mode.

## 2. Color Tokens

| Token | Light value | Dark value | Used for |
|---|---|---|---|
| `canvas` | `#FFFFFF` | `#0D0D0D` | Page/artboard background |
| `shape-fill` | `#E5E5E5` | `#1E1E1E` | Fill for every shape body |
| `shape-stroke` | `#1A1A1A` | `#F2F2F2` | Shape outlines, primary text |
| `text-muted` | `#8A8A85` | `#8A8A85` | Captions, labels, secondary text (same value both modes — this is what keeps light/dark feeling like one brand) |
| `connector` | `#1A1A1A` | `#F2F2F2` | Lines, arrows, dividers |

Never introduce a new color outside this table for a standard shape. If a category genuinely needs more (see §9), extend the table — don't improvise inline.

## 3. Corner Radius Rules

Radius is decided by geometry, not by preference:

| Shape family | Radius | Reasoning |
|---|---|---|
| Rectangular process/task/module/container | `rx="8"` | Friendly without losing edges |
| Structural/data shapes (UML class, ER entity, record) | `rx="6"` | Slightly tighter — reads as "structural," not "soft" |
| Terminator / stadium shapes | `rx=height/2` (fully rounded) | Inherent to the shape, not a style choice |
| Angular shapes (diamond, triangle, parallelogram, hexagon, pentagon) | **No rounding** | Rounding a diamond softens it into a blob and kills its meaning as a decision/branch symbol |
| Circles, ovals, ellipses | N/A | Already curved; no radius property needed |

## 4. Stroke & Line Weights

| Element | Weight |
|---|---|
| Shape outline | `1.5px` |
| Connector / flow line | `2px` |
| Emphasis line (e.g. critical path, active state) | `2.5–3px` |
| Divider line inside a composite shape (UML compartments) | `1px` |

## 5. Typography Scale

One sans-serif family throughout (`Helvetica, Arial, sans-serif`, or your brand face if licensed/embedded):

| Role | Size | Weight | Color token | Notes |
|---|---|---|---|---|
| Shape label (primary content) | `12px` | 400–500 | `shape-stroke` | Centered inside most shapes |
| Small/tight label (diamonds, cylinders, cramped shapes) | `10px` | 600 | `shape-stroke` | Used where the shape geometry leaves less room |
| Micro/attribute text (UML fields, ER attributes) | `8px` | 400 | `shape-stroke` | Left-aligned, inside compartments |
| Caption / specimen label (names the shape type, sits below/outside it) | `10.5px` | 400 | `text-muted`, `+0.3px` letter-spacing | Never inside the shape itself |
| Panel heading | `18px` | 600 | `shape-stroke` | Section/sheet titles only |
| Panel subheading | `11px` | 400 | `text-muted` | One line, under the heading |

## 6. Fill & Contrast Principle

- Flat fills only — no gradients, no drop shadows, no textures.
- `shape-fill` should read as a clearly distinct, moderate step off `canvas` (light: pale gray off white; dark: dark gray off near-black) — enough to separate the shape from the page without looking like a solid block.
- Unlike the source reference (which used fill-only cards with no outline), **diagram shapes keep a visible stroke** (`shape-stroke`, 1.5px). Brand cards don't need edges; technical diagrams do — connectors need a clear boundary to terminate against, and shapes need to read correctly if printed in grayscale or low contrast. This is the one deliberate departure from the reference, and it's a functional one.

## 7. Connector & Line-Style Meaning

Keep line style tied to meaning, not decoration — this table should match the UML notation already documented in `diagram-types-and-use-cases.md`:

| Style | Meaning |
|---|---|
| Solid line, filled arrowhead | Standard flow / synchronous message |
| Solid line, open (stick) arrowhead | Async message / directed association |
| Dashed line, open arrowhead | Dependency |
| Dashed line, hollow triangle | Realization / interface implementation |
| Solid line, hollow triangle | Generalization / inheritance |
| Solid line, hollow diamond (at line end) | Aggregation |
| Solid line, filled diamond (at line end) | Composition |

## 8. Sizing & Composition

- Base unit: `8px`. Every shape's width/height should resolve to a multiple of it, so shapes drawn independently still line up when composed into a full diagram later.
- Standard shape footprint for single-concept shapes (process, terminator, entity, event, etc.): **100×50px** internal content box, with **15–20px internal padding** before text starts.
- Composite shapes (UML class, tables) may extend taller in fixed compartment increments (~23px per row) but keep the same 100–130px width band as everything else, so they sit comfortably next to simple shapes in the same diagram.

## 9. Category Notes (preview — full specs later)

The base system above applies everywhere. A few categories extend it slightly:

- **Flowchart** — pure base system, no extensions.
- **UML** — adds compartment dividers (§4) and the full relationship-line table (§7).
- **ER / DFD** — adds crow's-foot line-end markers; data stores use the cylinder construction in the specimen sheet.
- **BPMN** — event circles vary stroke weight by type (start = thin single, end = thick single, intermediate = double); gateways add an interior glyph (X, O, +) per §3's "no rounding" rule.
- **Network / Cloud / Architecture** — icons may use a slightly bolder `2px` outline to hold up at small sizes; otherwise same tokens.
- **Project Management (Gantt, Kanban, Risk Matrix)** — needs one additional accent color for status/priority (not yet specified — flag this when we get to it, since it's the one place the two-gray system needs a third color).
- **BI / KPI** — needs a small data-color ramp for charts, which the two-gray system deliberately doesn't provide — separate spec required.
- **Web/UX (wireframes, sitemaps)** — pure base system; treat every element as a rectangle or its content-appropriate primitive.

## 10. SVG File Conventions

- One SVG per shape (or small related group) as the library gets built out: `shape-[name]-[mode].svg` (e.g. `shape-decision-light.svg`), matching the naming already used for the two reference MD files.
- Every file's `viewBox` should be derived from the 8px base unit (§8) — never a hand-typed guess.
- Define the color/type classes from this guideline once in a `<style>` block at the top of each file (or a shared stylesheet if the tooling allows importing one) rather than repeating inline `fill`/`font-size` on every element — a future palette change becomes a one-line edit instead of hundreds.
- Group each shape in its own `<g>` with local, zero-based coordinates — keeps shapes copy-pasteable between files without recalculating positions.
- Both a light and a dark variant should exist for every shape before it's considered "done."

---

*Reference: `shape-style-specimen-sheet.svg` shows this guideline applied to 10 sample shapes (terminator, process, decision, data store, connector, class, actor, entity, gateway, event) spanning flowchart, UML, ER, and BPMN — in both modes.*
