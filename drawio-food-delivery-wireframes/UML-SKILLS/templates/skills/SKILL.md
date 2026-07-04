---
name: diagram-layout-patterns
description: Assemble complete, multi-element SVG diagrams (sequence diagrams, Gantt charts, flowcharts, ER diagrams, BPMN, org charts, class diagrams, and more) using proven layout patterns -- cursor-based positioning, nested-structure stacks, and two-pass rendering -- instead of hand-computing every coordinate. Use this skill whenever the user asks to build, generate, or assemble a complete diagram (not a single primitive shape) as SVG, especially one with sequential or time-based content, nested regions (fragments, swimlanes, subgraphs), rows that repeat, or elements whose size depends on content added after them. Companion to the svg-diagram-system skill, which supplies the shape primitives and design tokens this skill assembles into full diagrams -- install both together.
---

# Diagram Layout Patterns

How to assemble a *complete* diagram — correctly position, nest, and size dozens of related elements — without hand-computing every coordinate and hoping the arithmetic holds.

Companion to **svg-diagram-system** (shape primitives, color/type/radius tokens, `defs`/`use`). This skill is one level up: the layout grammar that decides *where* those shapes go and *when* a container's size can even be known.

## The core problem this solves

Individual shapes have fixed geometry — a diamond is always the same relative points. A *diagram* is different: you don't know how tall a sequence diagram's `alt` fragment is until everything inside it is drawn; you don't know a Gantt chart's total height until you know how many rows it has; a flowchart connector has to route between two node positions decided a few lines of code ago. Hand-typing absolute Y coordinates for a 20+ element diagram is exactly how subtle bugs happen — this was learned firsthand building a comprehensive UML sequence diagram (see the cautionary example in `references/layout-patterns.md`).

## Three techniques, used together

1. **Cursor-based positioning** — maintain a running position (usually a `y` cursor that only moves forward) and advance it after each element, instead of computing `y = 172 + 50 + 65 + 36 + ...` by hand.
2. **A stack for nested structure** — anything that nests (combined fragments, swimlanes, subgraphs, grouped org-chart branches) goes on an explicit stack: push on enter with a remembered start position, pop on exit once the end position is known, *then* draw the enclosing frame. Never draw a container's boundary before you know where it ends.
3. **Two-pass rendering** — some elements can't be drawn until the whole diagram is known: lifelines (top known immediately, bottom only once every message is placed), overall canvas height, a Gantt chart's timescale header if it's driven by the latest task's end date. Emit content as you go; defer boundary/summary elements to a final pass.

Full methodology, the generalized `Canvas` base class, and a worked before/after are in `references/layout-patterns.md`. Don't reimplement this per diagram type — `scripts/diagram_kit.py` provides it once. It depends on `shape_kit.py` from **svg-diagram-system** for color tokens and text/line primitives — install both skills, or copy `shape_kit.py` alongside `diagram_kit.py`.

## Which pattern fits which diagram family

| Family | Example diagram types | Core layout idea |
|---|---|---|
| Sequence / time-axis | Sequence, Timing, Communication | Fixed x per participant; y = time, advances downward; open/close span tracking per participant |
| Timeline / Gantt | Gantt, PERT, Timeline, Milestone Chart | Fixed y per row; x = time/date; dependencies are edges between bar endpoints |
| Graph / node-edge | Flowchart, DFD, ERD, Network, most UML | Nodes placed on a grid or by rank; edges routed between node *boundaries*, not centers |
| Tree / hierarchy | Org Chart, Mind Map, Decision Tree, Sitemap | Levels top-down or left-right; parent-child connectors; sibling spacing is two-pass (width bottom-up, then position top-down) |
| Matrix / grid | ER entity internals, SWOT, RACI, Kanban, tables | Rows × columns of cells — the same grid math already used for the basic-shapes contact sheet and the foundation guideline pages |
| Swimlane | BPMN, Cross-Functional Flowchart | Sequence pattern rotated: lanes instead of lifelines, flow is the primary advancing axis |

Full per-family notes and code sketches: `references/layout-patterns.md`. A complete mapping of all diagram types in the master catalogue to their family: `references/diagram-catalogue.md`.

## Workflow

1. Identify the family from the table above (or look it up in `references/diagram-catalogue.md`).
2. Use `scripts/diagram_kit.py`'s `Canvas` (cursor + span-tracking + stack + defer) as the base — don't hand-roll a new one per diagram.
3. Draw shapes via `shape_kit.py` primitives and `DEFINE`/`SYMBOL`/`USE` for anything repeating.
4. Defer frame/boundary/summary elements to `Canvas.defer()`, resolved once total extent is known.
5. Same QA discipline as always: run it, validate as XML, sanity-check for negative/NaN geometry, render to PNG and look at it before presenting.

## What's been proven with this pattern so far

The UML sequence diagram (`diagram-sequence-order-checkout-*.svg`) is the reference implementation: 6 lifelines, nested `alt`/`opt`/`loop`/`par` fragments, activation-bar tracking across a branching `alt`/`else`, a mid-diagram `create`, and a `destroy` — built with a cursor + stack, with zero hand-typed absolute coordinates below the header. `Canvas` in `diagram_kit.py` is that implementation's pattern, generalized. The other five families in the table above are documented with code sketches but not yet built and QA'd against a real diagram — treat those as a strong starting point, not proven-in-production the way the sequence pattern is.

## Next up

Gantt chart — timeline family, and the first real test of both this skill and `defs`/`use` together (task-bar rows repeat; row count isn't known until the task list is). Decide the status/priority accent color (flagged in `svg-diagram-system`'s open items) before starting it.
