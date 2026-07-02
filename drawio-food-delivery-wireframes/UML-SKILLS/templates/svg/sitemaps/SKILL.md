---
name: diagram-to-svg-replication
description: Root skill for turning a reference image of ANY diagram, chart, dashboard, wireframe, or visual layout into a faithful, production-ready, self-contained SVG. Use whenever someone uploads a screenshot/photo/export of a diagram and asks to recreate it, rebuild it, turn it into a template, make it editable, or generate "the same thing" as SVG/code. This is the PARENT skill — always read it first. If a more specific child skill exists for the image's diagram type (sitemap, gantt chart, flowchart, org chart, wireframe, dashboard, network diagram, etc.), read that too and follow it for type-specific vocabulary; it will assume everything in this file. If no child skill exists for the type in front of you, follow this file's generic process directly — do not refuse or wait for a specialized skill to appear.
---

# Diagram → SVG Replication (Root Skill)

## What this file is

This is the **trunk**. Every other skill in this family (`gantt-to-svg.md`, `sitemap-to-svg.md`,
`flowchart-to-svg.md`, `wireframe-to-svg.md`, whatever gets written next) is a **branch**: a short
file that only documents what's *different* about that diagram genre — its vocabulary, its typical
parts, its common gotchas. None of the branches re-explain the workflow, the tooling, or the quality
bar. That all lives here, once, so it stays consistent and so updates only have to happen in one
place.

If you are a child skill: assume the agent has already read this file. Don't repeat it.
If you are the agent and no child skill matches: this file alone is enough to do the job well.

## When this fires

- A reference image (upload, paste, screenshot, photo of a whiteboard) shows a diagram and the
  person wants it recreated, rebuilt, "made editable," turned into a template, or output as SVG/code.
- The phrasing varies a lot: "convert this to SVG," "make me a template based on this," "I need an
  editable version of this chart," "recreate this diagram," "this but as a vector file." Trigger on
  intent, not on the literal word "SVG."
- It does **not** require the person to attach a giant prompt document (some will paste one — like
  the over-specified generic prompts seen in earlier sessions — but treat those as *one input among
  several*, not gospel; the reference image is the source of truth, not the prose describing it).

## Phase 0 — Route before you draw anything

1. Identify the diagram's genre (sitemap, Gantt chart, org chart, flowchart, network diagram,
   wireframe/mockup, dashboard, timeline, funnel, ER diagram, etc.).
2. Check whether a child skill exists for that genre. If yes, read it — it will tell you the
   genre-specific anatomy and save you the discovery work in Phase 1–3.
3. If no child skill exists, proceed with the generic process below. Consider drafting a short child
   skill afterward (see "Writing a child skill" at the end) so the next agent that sees this genre
   doesn't start from zero.

## Phase 1 — Look at the whole image before you look at any piece of it

View the full reference image first, at full size, before cropping anything. Form a rough mental map:
title/header, legend, the main body, repeating units, anything that looks like a tooltip/popover or
an interaction-state callout. Resist the urge to start sampling pixels immediately — a wrong mental
model formed in the first ten seconds is expensive to undo later.

Then crop and zoom into each region you're unsure about. Don't trust your read of small text or thin
lines from the full image — diagrams are dense and JPEG/PNG compression blurs fine detail.

**A practical trap to expect:** your first guess at crop coordinates will often be wrong — you'll crop
whitespace next to the thing you wanted, or crop a row above/below the one you meant. When that
happens, don't re-guess blindly. Recompute: note the crop box and resize factor you used, work out
where the element actually landed in that output, divide back by the resize factor, add the crop
offset, and crop again with the corrected numbers. Treat it as arithmetic, not luck.

## Phase 2 — Get pixel-level ground truth, don't eyeball it

Use an imaging library (PIL/Pillow or equivalent) to sample actual pixel colors rather than guessing
hex codes from memory or vibes ("that looks like a Material blue"). Two things that go wrong here:

- **Sampling the wrong point.** A single `(x, y)` guess frequently lands on anti-aliased edges, text
  strokes, or gridlines and returns a misleading color (you'll get white when you meant to sample a
  filled bar, or a blended gray when you meant a solid color). Cross-check by sampling from an
  already-cropped/zoomed image where you can see exactly where the pixel grid lines up, or sample a
  few neighboring points and look for the mode/majority color rather than trusting one pixel.
- **Over-fitting to compression artifacts.** Real screenshots have noise. Round sampled colors to
  clean, plausible hex values rather than reproducing `rgb(176,175,181)` verbatim when the design
  intent is obviously a flat `#B0B0B5`-ish gray.

Build a small palette (5–12 colors is typical) before you start drawing: background, 2–4 fill tones
for the main repeating element, 1–2 accent colors, text colors by hierarchy level, line/grid color,
and any "selected/highlighted state" color if the image shows one.

## Phase 3 — Decompose the structure, name every part

Write out (mentally or literally, in comments) an inventory before coding:

- **Containers**: title/header block, legend, the primary table/canvas, footer/branding.
- **Repeating units**: what shape are the nodes/rows/cards? What varies between them (size, fill,
  border) and what's constant?
- **Hierarchy**: are there levels (phase → task → subtask; group → member; category → page)? How is
  level encoded — indentation, font weight, color, icon?
- **Connectors/relationships**: lines, arrows, dependency links. What routing style (straight,
  orthogonal/elbow, curved)? Where do arrowheads sit? Are there shared trunks/combs (one line
  branching to several targets) vs point-to-point links?
- **Special states**: tooltips, hover/selection highlighting, progress overlays, milestones — these
  carry a lot of the image's personality and are worth getting right even when they're "extra."
- **Text roles**: title, axis/header labels, body labels, inline percentage/value labels, captions.
  Note alignment (centered vs left) and whether labels sit inside or outside their shape — this is
  easy to assume wrong (see Phase 7).

## Phase 4 — Plan a coordinate system before writing draw calls

Decide, on purpose:

- A scale factor from the source image's pixel dimensions to your output canvas (2x is a comfortable
  default for crispness without becoming unwieldy).
- Column/row grid: margins, fixed-width columns (like a label column next to a timeline/canvas),
  row height, gap sizes.
- Where every repeating group sits relative to that grid (which column, which row range).

Do this **before** writing SVG. Retrofitting a grid after free-handing coordinates is how you end up
with overlapping elements you discover only on the third render.

## Phase 5 — Build with a generator script, not hand-typed SVG

For anything beyond a trivial shape count, write a small script (Python is the natural choice — it
has good string handling and you likely already have an image library loaded) that emits the SVG,
rather than typing raw `<rect>`/`<path>` tags by hand. Reasons this matters in practice, not in
theory:

- You will draw the same kind of thing — a labeled box, a badge, a row background, an arrow — dozens
  of times with only the coordinates changing. A helper function turns "dozens of chances to typo a
  coordinate" into "one function, called dozens of times."
- Anchors (top/bottom/left/right/center of a box) computed from `(x, y, w, h)` let connectors be
  derived rather than re-measured by eye each time.
- When you find a bug (wrong color, wrong spacing) you fix it in one place and regenerate, instead of
  hunting for every occurrence in a wall of markup.

A reusable starter library with exactly this kind of helper (`rect`, `rrect`, `text`, `line`,
`arrow_tri`, a `Box` anchor class, badges, tooltips, elbow/fan-out/comb connectors) ships alongside
this skill at `scripts/svg_helpers.py`. Import it rather than re-deriving the same functions from
scratch each time; extend it in place when a new diagram genre needs a new primitive (e.g. a
diamond-shaped milestone marker, a person-silhouette icon) and leave the addition there for next time.

## Phase 6 — You cannot see SVG by reading the markup. Render it.

This is the single most important habit in this whole skill. SVG markup that looks right in the
source code is frequently wrong on screen — off-by-one anchor math, a box drawn before its background
so it's invisible, text that overflows its container. Don't ship on faith.

Render the SVG to a raster image and *look at it* before considering the work done. In a typical
sandboxed environment, try renderers in this order and use whichever works:

1. A Node image library with built-in SVG rasterization (e.g. `sharp`), if it's globally installed —
   check with something like `node -e "require('sharp')"` or look at `npm list -g`.
2. `rsvg-convert` on the command line, if present.
3. `cairosvg` (Python), if it's importable.
4. A headless-browser screenshot (e.g. Playwright/Puppeteer) as a last resort — heavier, but works
   almost anywhere.

Don't assume a tool is missing — test it once, cheaply (a 3-line dummy SVG is enough), before
concluding you need a fallback. Whatever you find working, wrap it once (the bundled
`scripts/render_preview.py` does this with the same fallback chain) so you're not rediscovering it
mid-task.

## Phase 7 — The re-zoom loop: assume your first render has at least one wrong assumption

After the first full render, don't stop at "looks close." Go back to the source image and crop the
*same regions* you're least sure about, then crop the equivalent regions of your own render, and
compare side by side. Specifically interrogate:

- **Label placement** — inside the shape (and what color, for contrast) vs outside it. It's
  tempting to assume one convention applies everywhere; real designs often mix conventions between
  similar-looking elements (one bar's value sits inside in white, the next bar's sits outside in
  gray) and you will guess wrong at least once if you don't check each one.
- **Connector routing** — does the elbow go right-then-down or down-then-right? Where exactly does
  the arrowhead sit?
- **Spacing/collisions** — measure your render's actual content bounding box (e.g. scan for the
  non-white pixel extent) rather than assuming your planned canvas size has no dead space or overlap.
  Tighten the canvas to match; resize/reposition anything that collides.
- **Color** — put your rendered swatch next to the sampled source swatch; "close enough from memory"
  drifts more than you'd expect.

Fix what's wrong, regenerate, re-check. Two or three passes is normal for anything non-trivial; budget
for it rather than treating the first render as the deliverable.

## Phase 8 — Validate and ship

- Confirm the file is well-formed XML (`xml.etree.ElementTree.parse` or equivalent) before delivering.
- Keep the SVG self-contained: inline styles or a single embedded `<style>`, no external font/image
  references that won't resolve outside your sandbox.
- Save the final file to the project's output location, present it, and stop — don't re-explain the
  whole image back to the person in prose. They can see it.

---

## Fidelity doctrine: what to copy exactly vs what to approximate

Not every pixel in a reference image carries the same weight. Spend precision where it's earned:

**Copy exactly:**
- Structural hierarchy and grouping (what contains what, what's a child of what).
- Any text that's semantically meaningful: real labels, dates, percentages, named categories, axis
  values, legend entries.
- The visual *language* — color roles, shape vocabulary, connector style, typography hierarchy —
  even when you don't have the exact source font/hex, the relationships (this is darker than that,
  this is bolder than that) must hold.
- Anything the request specifically calls out as important.

**Approximate deliberately (and it's fine to say so if asked):**
- Arbitrary/decorative filler data — random-looking demo task bars, placeholder names, filler
  row counts in a demo screenshot — where the *pattern* (density, rough length distribution) matters
  more than matching each pixel. Generating plausible filler (seeded for determinism if you want
  reproducible output) is a reasonable and time-appropriate choice; chasing the exact pixel position
  of every one of forty decorative bars is not a good use of the time, and the result is usually a
  generic demo dataset anyway.
- Exact source-image compression noise, sub-pixel anti-aliasing, drop-shadow blur radii — reproduce
  the *intent* (a soft shadow exists) not the exact filter parameters.

When in doubt, ask: "if this number/label were different, would the diagram mean something different
to the person reading it?" If yes, it's in the "copy exactly" bucket.

## Brand-safety guardrail

If the reference image carries a real, named third-party product's logo or wordmark (a charting
library's watermark, a named SaaS product's UI chrome, etc.), don't reproduce that logo/wordmark
verbatim in the output. Swap in a generic, unbranded equivalent (a plain icon + neutral caption) that
preserves the layout without copying someone else's trademark. This is a default, quiet substitution —
no need to make a production out of explaining it, a one-line note in the handoff is enough.

## Tooling kit (what you're actually reaching for)

| Need | Typical tool |
|---|---|
| View full image / crops | image viewer tool available in your environment |
| Crop, resize, sample pixel colors | Python + Pillow (`PIL.Image`) |
| Generate SVG text | plain Python string-building, or `scripts/svg_helpers.py` |
| Rasterize SVG → PNG to inspect | `sharp` (node) → `rsvg-convert` → `cairosvg` → headless browser, in that order of likely availability |
| Validate SVG | `xml.etree.ElementTree.parse` |
| Measure actual content bounding box | `numpy` over the rendered PNG, find the non-background pixel extent |

## Output conventions

- One self-contained `.svg` file per diagram (or one per logical section if the source image is
  clearly multiple stacked diagrams — keep them in a single file unless asked to split them).
- Sensible descriptive filename, not `output.svg`.
- Canvas dimensions sized to the actual content, not an arbitrary preset (don't default to 1920×1080
  just because a prompt template said so — measure what you built and size to it, plus a sane margin).
- Hand off with a short, concrete note about what was matched closely and what was deliberately
  approximated (per the fidelity doctrine above) — not a re-description of the whole diagram.

---

## Quick-reference: common diagram anatomies

Useful even when no child skill exists yet for the genre in front of you:

- **Sitemap / site architecture**: title block, root node, tree hierarchy by indentation or
  vertical levels, orthogonal connectors (often a "comb" — one trunk line branching into several
  siblings), numbered callout badges, a footer link cluster.
- **Gantt / project timeline**: frozen left-hand label column (often `#` + name, with phase/task/
  subtask indentation) next to a calendar timeline; header has 2–3 stacked rows (year → quarter/month
  → day/date); bars encode duration as width and often progress as a two-tone fill; milestones are
  diamonds; dependencies are elbow arrows between bar edges; watch for a hover-state tooltip card
  showing exact dates/values.
- **Org chart**: strict top-down tree, uniform node size per level, straight or orthogonal connectors,
  sometimes photos/avatars in nodes.
- **Flowchart**: shape vocabulary carries meaning (rectangle = process, diamond = decision, rounded =
  start/end, parallelogram = I/O) — getting the shape *type* right matters more than exact sizing.
- **Wireframe/mockup**: grayscale/placeholder content blocks standing in for real UI — text lines as
  bars, images as gray rectangles with a corner-fold or mountain icon, buttons as rounded rects.
  Faithful proportions matter more than faithful "content."
- **Dashboard**: grid of cards/widgets, each with its own mini chart type (bar/line/donut/KPI number)
  — treat each widget as its own small decomposition problem.
- **Network/architecture diagram**: nodes are typically icons or labeled boxes for systems/services,
  edges show data flow direction (arrowheads matter), often grouped into bordered zones (VPC, region,
  tier).

---

## Writing a child skill

A child skill is short. It should NOT repeat the workflow, tooling, fidelity doctrine, or output
conventions above — it inherits all of that. It should ONLY contain what's specific to one diagram
genre. Use this skeleton:

```markdown
---
name: <genre>-to-svg
description: Child of diagram-to-svg-replication. Use for <genre> reference images specifically
  (e.g. "<genre> chart", typical trigger phrases). Read the root skill first for the full process;
  this file only covers what's specific to <genre>.
---

# <Genre> → SVG (child of diagram-to-svg-replication)

> Inherits the full workflow from `diagram-to-svg-replication/SKILL.md`. Read that first. This file
> only covers what's specific to this genre.

## Anatomy checklist for this genre
- [the parts this genre always or usually has]

## Vocabulary / element types
- [named shapes, bar styles, icon conventions specific to this genre]

## Common pitfalls seen in practice
- [things that were easy to get wrong last time, so the next pass doesn't repeat them]

## Worked reference (optional)
- [if you have a known-good past example, link or describe it briefly]
```

Keep it tight — a good child skill is the kind of thing you can read in under a minute and immediately
know what to look for that you wouldn't have known to look for otherwise.
