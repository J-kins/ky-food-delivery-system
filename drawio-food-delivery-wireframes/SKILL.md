---
name: drawio-food-delivery-wireframes
description: Use this skill whenever asked to create, extend, or revise drawio (.drawio / diagrams.net) wireframes for the "food delivery system" student project described in this file — a multi-role food delivery app/platform covering Customer, Kitchen Staff, Delivery Rider, Restaurant Manager, Administrator, and Customer Support. Trigger on any mention of wireframes, drawio, diagrams.net, low-fidelity mockups, screen flows, or "the system diagram" for this project, even if the user doesn't restate the full screen list. Also trigger if the user only asks for the 5 required screens (Login, food menu with prices, select food, make payment, order status notifications) — build those first but be aware the full system goes further; see references/screen-inventory.md.
---

# Drawio Wireframes — Food Delivery System

You're producing a single `.drawio` file (or updating one) containing
low-fidelity, grayscale wireframes for every screen in a food delivery
platform, organized into pages by user role, with labeled flow arrows showing
how screens connect. This is for a university-level software engineering
assignment — it needs to look deliberate and complete, not just be a pile of
boxes.

If you have your own drawio-generation tool or skill already available
(an MCP tool, a different skill, direct API access to diagrams.net, etc.),
**use it for the actual file mechanics.** Treat the three reference files
below as the content/spec it should follow — what screens to build, what
each one contains, and what style to use — rather than redoing that thinking
yourself. If you don't have a separate drawio tool, `references/drawio-xml-guide.md`
plus `assets/pattern-templates.drawio` are a complete enough fallback to
hand-write or script the file directly.

## Read these in order

1. **`references/screen-inventory.md`** — the full list of ~95 screens,
   organized by role, each tagged with a priority (🔴 required / 🟠 core /
   🟡 recommended / ⚪ stretch) and mapped to one of the 13 layout patterns.
   Start here to know *what* to build and in what order.
2. **`references/layout-patterns.md`** — the 13 reusable layout patterns
   (ASCII-diagrammed) that basically every screen in the inventory is a
   variant of. Read this to know *how* each screen should actually be laid
   out — region by region, what goes where.
3. **`references/drawio-xml-guide.md`** — file/page organization, canvas
   sizes, the exact style strings to use for every element (so the whole
   system looks like one consistent design, not 95 different ones), and the
   one coordinate-system rule that breaks diagrams if you get it wrong.
4. **`assets/pattern-templates.drawio`** — open this directly in
   diagrams.net (or read its raw XML) before building anything. It contains
   three fully working example frames: a mobile Login screen (Pattern A), a
   mobile Home screen (Pattern C), and a desktop Admin Dashboard (Patterns
   H+I). Copy its structure for every new screen rather than reinventing the
   XML conventions from scratch.

## Background — why these screens, specifically

This is a food delivery app project where the lecturer required exactly 5
screens: Login, a food menu screen showing prices, a screen to select/customize
food, a payment screen, and a way to receive order status notifications. The
human has already expanded that into a fuller system covering every role that
realistically touches such a platform (kitchen staff prepping orders, riders
delivering them, restaurant managers running the kitchen-side business, an
admin overseeing the whole platform, and a support team handling issues).
`screen-inventory.md` is that expansion, with some additional screens layered
in (marked **(NEW)**) to make the system feel complete rather than having
obvious gaps — e.g. there was no screen for entering a promo code, no
onboarding flow, no empty states, no way for a rider to actually see/accept a
new delivery request, etc. These are flagged so the human can cut anything
that's out of scope for their specific assignment.

## Workflow

1. Skim `screen-inventory.md` fully once before building anything, so the
   page/flow structure in your head matches the one in
   `drawio-xml-guide.md` §1.
2. Set up the 8 pages described in `drawio-xml-guide.md` §1.
3. Build screens in priority order (🔴 → 🟠 → 🟡 → ⚪), not role-by-role —
   if you run out of time, every role should at least have its core screens
   rather than some roles being complete and others missing entirely.
4. For each screen: look up its Pattern letter in `screen-inventory.md`,
   read that pattern's full layout in `layout-patterns.md`, copy the closest
   matching frame from `pattern-templates.drawio`, then relabel/adjust per
   the screen's specific "Layout notes" column.
5. Once a page's screens exist, add labeled flow arrows between them showing
   the primary user journey for that role.
6. Do the final consistency pass described in `drawio-xml-guide.md` §7.
7. Hand back the finished `.drawio` file, and call out: (a) which 🔴/🟠
   screens you completed, (b) which 🟡/⚪ screens you skipped for time, and
   (c) which **(NEW)** screens you included so the human can confirm they're
   not out of scope for what was actually assigned.

## Things to get right

- Stay grayscale + the single `#4A6FA5` accent (see the style cheat-sheet) —
  don't let drawio's default blue/orange/green shape colors leak in when you
  duplicate shapes.
- Keep mobile frames at 360×780 and desktop frames at 1440×900 throughout —
  inconsistent frame sizes are the fastest way to make a wireframe set look
  unplanned.
- Don't skip the flow arrows in step 5. A folder of disconnected screens is a
  *screen gallery*; the arrows are what make it a wireframe **of a system**,
  which is what was actually asked for.
- The "Food Details" and "Food Menu" screens (#18–19) are two of the five
  required screens — give them real attention: visible prices on every menu
  row, and actual size/add-on/quantity controls on the detail screen, not
  just placeholder text.
