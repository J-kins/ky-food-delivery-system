---
name: svg-diagram-system
description: Build consistent, professional SVG diagrams and shape libraries — UML, flowcharts, ER/DFD, BPMN, network and cloud architecture, Gantt and project-management charts, org charts, wireframes, sitemaps, and more — using a shared design-token palette (color, typography, corner radius, stroke weight) and proper <defs>/<use> reusable-component architecture instead of duplicated markup. Use this skill whenever the user asks to create, generate, draw, or design any diagram, chart, icon set, or shape as SVG, even if they don't say "SVG" explicitly — this includes requests to draw a flowchart, sequence diagram, class diagram, network diagram, Gantt chart, dashboard mockup, or any item from a shape/diagram library. Also use when the user wants multiple diagrams to stay visually consistent, wants a reusable icon/shape library, or wants SVG output that is dynamic, scalable, and reusable across a project rather than a one-off drawing.
---

# SVG Diagram System

A design system and build methodology for producing professional SVG diagrams of any type, that stay visually consistent across a project and reuse geometry via `<defs>`/`<use>` instead of duplicating markup per instance.

This isn't theoretical — it's what was actually used to build a real shape/diagram library (32 basic primitives, a full multi-fragment UML sequence diagram, more categories in progress). The Python helper module is bundled and ready to import.

## Before writing any SVG

1. Read `references/design-tokens.md` — the full color / typography / corner-radius / stroke-weight system. Never invent a value outside it.
2. If the diagram has **any repeated shape** (more than ~2 instances of the same geometry — task bars in a Gantt chart, nodes in a flowchart, icons in a legend), read `references/reusable-components.md` first and build it with `<defs>`/`<use>`, not copy-pasted markup. This is not optional polish — it's the difference between a one-off drawing and a maintainable component.
3. For Python-generated diagrams, `import` from `scripts/shape_kit.py` rather than re-implementing drawing primitives — it already encodes the tokens from step 1, plus `DEFINE`/`SYMBOL`/`USE` helpers for step 2.
4. Plan both a light-mode and a dark-mode version. The token system is defined for both; shipping only one is an incomplete deliverable.

## The two-token color system (summary — full table in references/design-tokens.md)

| Token | Light | Dark | Used for |
|---|---|---|---|
| canvas | `#FFFFFF` | `#0D0D0D` | page/artboard background |
| fill | `#E5E5E5` | `#1E1E1E` | every shape body |
| stroke / text | `#1A1A1A` | `#F2F2F2` | outlines, primary text |
| muted | `#8A8A85` | `#8A8A85` (same both modes) | captions, secondary text |

Corner radius, stroke weights, and the full type scale are geometry-driven, not stylistic choices — see `references/design-tokens.md` §3–5 before drawing anything angular vs. rounded.

## Reusable components (summary — full methodology in references/reusable-components.md)

Don't hand-draw the same shape twice. Define it once inside `<defs>` as a `<symbol viewBox="...">`, leave color OFF the definition, and instantiate with `<use href="#id" x=".." y="..">` — color comes from a CSS class or custom property applied at the `<use>` site (or an ancestor `<g>`), so ONE definition serves both light and dark instances. `references/reusable-components.md` has the full pattern, a worked Gantt-bar example, ID-namespacing rules, and the embedded-defs-vs-shared-sprite-sheet tradeoff.

## Build & QA workflow

1. Write the generator as a Python script (raw SVG only for something genuinely one-off and simple).
2. Run it — fix any traceback before moving on. Don't hand-debug SVG XML by eye.
3. Validate well-formedness on every output file: `python3 -c "import xml.dom.minidom; xml.dom.minidom.parse('file.svg')"`.
4. Sanity-check the geometry: grep the output for negative widths/heights or NaN — catches a layout bug before it becomes a visual one.
5. If `cairosvg` is available (`pip install cairosvg --break-system-packages`), render to PNG and actually look at it before presenting. For a multi-item library, render a throwaway contact sheet for QA only — never deliver the contact sheet itself if the user asked for separate files.
6. Only then copy to the output directory and present.

## File & naming conventions

- Individual reusable shapes: `shape-[name]-[mode].svg` — one shape, one mode, one file, transparent background, sized to a consistent viewBox (140×100 has worked well for single icons).
- Assembled diagrams (a specific scenario, not a primitive): `diagram-[type]-[scenario]-[mode].svg` (e.g. `diagram-sequence-order-checkout-light.svg`).
- Category generator scripts: `gen_NN_category-name.py`, importing `scripts/shape_kit.py` rather than redefining helpers.
- Keep light/dark as **separate files** per shape/diagram. Don't combine multiple shapes into one grid-sheet file unless the user explicitly asks for a combined reference sheet — that's a different, valid deliverable, just not the default for a shape *library*.

## Diagram categories

Applied so far: basic & primitive shapes, and a comprehensive UML sequence diagram. Queued, same token system, only the geometry changes: flowcharts, the rest of UML (class, use case, activity, state machine, component, deployment...), ER/DFD, BPMN, project management (Gantt, PERT, Kanban, timeline, risk matrix), architecture & network, org & strategy, web/UX, BI/KPI dashboards, IT methodology frameworks.

## Known open items — decide before building these categories

- **Project management & BI/KPI** need one additional accent/data color each — the base two-gray system deliberately doesn't provide one. Don't improvise a color inline; decide and record it in `references/design-tokens.md` first.
- **Gantt charts specifically** are the first planned use of the `<defs>`/`<use>` pattern for real (task bars repeat down every row) — read `references/reusable-components.md` §6 before starting one.
