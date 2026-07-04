# Shape & Diagram SVG Library

A growing library of professional, consistent SVG diagram components — plus a packaged Skill so the system (not just the output) is reusable in future sessions.

## Start here

**If you're picking this up fresh:** install `svg-diagram-system.skill` (click it, "Save skill") before asking for more diagrams. It contains the full design system and a ready-to-import Python helper module, so new requests stay consistent with everything already built here instead of starting from scratch.

**If you just want the reference docs without installing anything:** read `design-tokens.md` (colors, corner radius, stroke weights, type scale) and `reusable-components.md` (the `defs`/`symbol`/`use` reuse pattern) directly — they're plain Markdown, no skill required.

## What's in this folder

```
shape-library/
├── README.md                        — this file
├── svg-diagram-system.skill         — the packaged Skill (install this)
├── design-tokens.md                 — standalone copy: color / radius / stroke / type system
├── reusable-components.md           — standalone copy: defs/symbol/use methodology
├── 01-basic-primitive-shapes/       — 32 shapes × light + dark = 64 standalone SVGs
└── diagram-examples/                — fully assembled example diagrams
    └── diagram-sequence-order-checkout-{light,dark}.svg  + its generator script
```

Two files live one level up, outside this folder, and this whole library is built from them:
- `../diagram-shapes-stencils-master-list.md` — the full shape/stencil catalogue (13 categories, ~570 shapes)
- `../diagram-types-and-use-cases.md` — the full diagram-type catalogue (74 types, purpose + when-to-use)
- `../shape_kit.py` — the same helper module bundled inside the skill, also available standalone

## The design system, in one paragraph

Everything — every shape, in every category — draws from **one two-token color system** (a `canvas` background, a `fill`, a `stroke`, and a shared `muted` tone, each with a light and dark value), **geometry-driven corner radius** (rectangles round, diamonds never do), a **fixed type scale** (six roles, from micro attribute text up to panel headings), and, going forward, **`defs`/`symbol`/`use`** instead of copy-pasted markup anywhere a shape repeats. Full detail in `design-tokens.md` and `reusable-components.md`. Nothing in this library should use a color, radius, or font size outside those two files — if a new category genuinely needs one (Gantt/Kanban status colors and BI chart colors are the two known cases), it gets added deliberately, not improvised inline.

## What's built so far

| Category | Status | Where |
|---|---|---|
| 01 — Basic & Primitive Shapes | ✅ 32 shapes, both modes | `01-basic-primitive-shapes/` |
| Sequence Diagram (comprehensive example) | ✅ | `diagram-examples/` |
| Everything else in the master lists | Queued | — |

The sequence diagram is a full worked example — one actor, five objects (one created mid-diagram), sync/async/return messages, self-messages, create/destroy, and four nested combined fragments (`opt`, `alt`+`else`, `loop`, `par`) plus a `ref` — built to exercise every element in the UML sequence-diagram notation at once, in one coherent order-checkout scenario.

## Building the next category

1. Install/read the skill (see "Start here").
2. `import` from `shape_kit.py` — don't redefine `T`/`R`/`C`/`POLY`/etc.
3. If shapes repeat within the diagram (Gantt task bars, flowchart nodes, legend entries), use the new `DEFINE`/`SYMBOL`/`USE` helpers — see `reusable-components.md` §6 for the exact pattern.
4. Build both light and dark.
5. Validate as XML, sanity-check for negative/NaN geometry, render to PNG with `cairosvg` and look at it — *then* present.

## Known gaps to resolve before certain categories

- **Project management (Gantt, Kanban, risk matrix)** and **BI/KPI dashboards** each need one additional color the base two-gray system doesn't provide (a status/priority accent, and a small data-color ramp, respectively). Decide these deliberately and add them to `design-tokens.md` before building those categories.
- Gantt charts are next in line and are also the first real test of the `defs`/`use` pattern, since task-bar rows repeat down the whole chart.
