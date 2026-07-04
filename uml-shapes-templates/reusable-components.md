# Reusable SVG Components — `<defs>` / `<use>` Methodology

SVG's native reuse mechanism, adapted for this project's two-mode (light/dark) design-token system. This is what makes output *dynamic* — one definition, many parameterized instances — instead of a static one-off drawing.

## Table of Contents
1. [Why this matters here specifically](#1-why-this-matters-here-specifically)
2. [The core pattern: symbol + use](#2-the-core-pattern-symbol--use)
3. [Making one definition serve both light and dark](#3-making-one-definition-serve-both-light-and-dark)
4. [ID namespacing](#4-id-namespacing)
5. [Embedded defs vs. a shared sprite sheet](#5-embedded-defs-vs-a-shared-sprite-sheet)
6. [Worked example: a Gantt task bar, three ways](#6-worked-example-a-gantt-task-bar-three-ways)
7. [Best-practices checklist](#7-best-practices-checklist)

## 1. Why this matters here specifically

Every generator built so far draws by emitting fresh SVG markup text on every call — `C(...)`, `R(...)`, `POLY(...)` in `shape_kit.py` each return a brand-new string. That's the right call for a library of 32 *distinct* shapes (each one only appears once), but it breaks down the moment a single diagram repeats the same shape many times: a Gantt chart with 40 task-bar rows, a flowchart with a dozen identical process boxes, a legend with the same swatch shown five times. Re-emitting full markup for every repeat means a larger file and — more importantly — no single place to edit if the shape's geometry needs to change. `<defs>`/`<use>` fixes both, and is the difference between a "dynamic, comprehensive" component and a static drawing.

## 2. The core pattern: symbol + use

Prefer `<symbol>` over a bare `<g>` inside `<defs>`. A `<symbol>` carries its own `viewBox`, so each `<use>` can independently set `width`/`height` and the content scales correctly — the way an `<img>` would. A reused `<g>` can only be repositioned and CSS-styled, not independently resized without a manual `transform="scale(...)"` per instance.

```html
<defs>
  <symbol id="gantt-task-bar" viewBox="0 0 100 20">
    <rect x="0" y="0" width="100" height="20" rx="4" class="fill-token stroke-token"/>
  </symbol>
</defs>

<use href="#gantt-task-bar" x="120" y="80"  width="180" height="20"/>
<use href="#gantt-task-bar" x="120" y="106" width="90"  height="20"/>
```

Two rows, one definition. Resizing, repositioning, and recoloring all happen at the `<use>` site — the geometry is written once. Use modern `href` (not `xlink:href`) — this project doesn't target legacy SVG 1.1 renderers, so there's no need to carry both.

## 3. Making one definition serve both light and dark

Leave `fill`/`stroke` **off** the shape inside `<defs>`. Hardcoding a color there makes it a permanent default that every `<use>` then has to fight. Two ways to parameterize, both compatible with the token system in `design-tokens.md`:

**A — CSS classes** (simplest, universal support):
```css
.fill-token   { fill:   var(--shape-fill); }
.stroke-token { stroke: var(--shape-stroke); stroke-width: 1.5; }
```
```html
<g style="--shape-fill:#E5E5E5; --shape-stroke:#1A1A1A;">   <!-- light block -->
  <use href="#gantt-task-bar" x="120" y="80" width="180" height="20"/>
</g>
<g style="--shape-fill:#1E1E1E; --shape-stroke:#F2F2F2;">   <!-- dark block -->
  <use href="#gantt-task-bar" x="120" y="80" width="180" height="20"/>
</g>
```
One `<defs>` block, wrapped once per mode. Best when a single file needs to contain (or toggle between) both modes.

**B — `currentColor`** (simpler, for single-color icon-style symbols):
```html
<symbol id="milestone-diamond" viewBox="0 0 20 20">
  <polygon points="10,0 20,10 10,20 0,10" fill="currentColor"/>
</symbol>
<use href="#milestone-diamond" x="40" y="40" color="#1A1A1A"/>
```
`currentColor` inherits from the `color` property set on the `<use>` (or an ancestor).

Since this project ships light and dark as **separate files** (see the naming convention in SKILL.md), most files only need one mode's values baked in — but keep pattern A in mind for any single-file, mode-switching artifact (an interactive HTML page embedding the SVG with a light/dark toggle, for instance).

## 4. ID namespacing

`id` values must be unique within a document — and eventually within a *combined* sprite sheet, if files ever get merged. Prefix every defined symbol with its category:

- `shape-rectangle`, `shape-diamond` — basic primitives
- `uml-class-box`, `uml-activation-bar` — UML-specific
- `gantt-task-bar`, `gantt-milestone` — project-management-specific

Never just `rect1` or `symbol-a` — those collide the moment two files share a page.

## 5. Embedded defs vs. a shared sprite sheet

Two valid patterns, different tradeoffs:

| | Embedded `<defs>` (top of each file) | Shared sprite sheet (`sprites.svg`) |
|---|---|---|
| Portability | Fully standalone — matches the "separate files" convention already in use | Requires the sprite file to be present/loaded |
| File size | Slightly larger per file if a shape repeats across many diagrams | Smaller per-diagram file |
| Editing | Change propagates only within that one file | Change propagates everywhere at once |
| Best for | Shape-library deliverables (each file must work alone) | A live web page or app assembling many diagrams together |

**Default for this project: embed `<defs>` at the top of each diagram file.** That matches the standalone-file requirement already established for the shape library. Reach for a shared sprite (`<use href="sprites.svg#gantt-task-bar"/>`) only for a genuinely multi-diagram, single-context deliverable — an internal dashboard rendering many diagrams from one page, for example — and say so explicitly when that's the actual target, since it changes the portability contract.

## 6. Worked example: a Gantt task bar, three ways

**Without reuse** — what a naive generator does. Fine for a one-off, wasteful for 40 rows:
```html
<rect x="120" y="80"  width="180" height="20" rx="4" fill="#E5E5E5" stroke="#1A1A1A" stroke-width="1.5"/>
<rect x="120" y="106" width="90"  height="20" rx="4" fill="#E5E5E5" stroke="#1A1A1A" stroke-width="1.5"/>
<!-- ...38 more rows, each fully re-specifying fill/stroke/radius... -->
```

**With `<defs>`/`<use>`** — one definition, N lightweight instances:
```html
<defs>
  <symbol id="gantt-task-bar" viewBox="0 0 100 20">
    <rect width="100" height="20" rx="4" class="fill-token stroke-token"/>
  </symbol>
</defs>
<use href="#gantt-task-bar" x="120" y="80"  width="180" height="20"/>
<use href="#gantt-task-bar" x="120" y="106" width="90"  height="20"/>
```

**In the Python generator** — `shape_kit.py` now has the helpers for this:
```python
from shape_kit import DEFS, SYMBOL, USE, R

# once, at the top of the file:
task_bar_symbol = SYMBOL("gantt-task-bar", "0 0 100 20",
                          R("bar", 0, 0, 100, 20, fc, 4, col, 1.5))
defs_block = DEFS(task_bar_symbol)

# once per row, instead of calling R() again:
row1 = USE("gantt-task-bar", 120, 80, w=180, h=20)
row2 = USE("gantt-task-bar", 120, 106, w=90, h=20)
```
This is the change to make before building the Gantt chart — the next diagram in the queue, and the first one where repeated rows make `<defs>`/`<use>` matter for real rather than just being good practice in the abstract.

## 7. Best-practices checklist

- [ ] Anything appearing 3+ times in one diagram is a `<symbol>`, not repeated markup
- [ ] Color lives on the `<use>`/class, never hardcoded inside `<defs>`
- [ ] Every `id` is category-prefixed
- [ ] `href` used, not `xlink:href`
- [ ] `<defs>` embedded per-file unless the deliverable is explicitly a shared multi-diagram context
- [ ] A symbol's `viewBox` matches its natural drawing coordinates, so `<use width/height>` scales predictably
- [ ] Text labels that vary per instance (task names, node labels) stay as separate `<text>` elements positioned alongside the `<use>` — don't try to bake variable text into the symbol itself

## Also covered by the source reference (not yet needed here, kept for completeness)

- **Gradients & patterns**: `<linearGradient>`/`<pattern>` inside `<defs>`, referenced as `fill="url(#id)"`. Not used in this system — flat fills only, per `design-tokens.md` §5 — but the mechanism is identical to symbol reuse if a future category needs it.
- **External sprite files**: `<use href="sprites.svg#id"/>` to reference symbols defined in a completely separate file. Relevant if/when this library gets consumed by a live web page rather than shipped as standalone files.
