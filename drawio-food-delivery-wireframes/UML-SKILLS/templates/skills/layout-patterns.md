# Diagram Layout Patterns — Cursor, Stack, Two-Pass

The methodology behind `scripts/diagram_kit.py`'s `Canvas` class, plus a sketch for each diagram family it's meant to be subclassed for.

## Table of Contents
1. [The three techniques](#1-the-three-techniques)
2. [Why an open/close span tracker needs care](#2-why-an-openclose-span-tracker-needs-care)
3. [Sequence / time-axis](#3-sequence--time-axis-proven)
4. [Timeline / Gantt](#4-timeline--gantt)
5. [Graph / node-edge](#5-graph--node-edge)
6. [Tree / hierarchy](#6-tree--hierarchy)
7. [Matrix / grid](#7-matrix--grid)
8. [Swimlane](#8-swimlane)

## 1. The three techniques

**Cursor.** `Canvas.y` only ever moves forward. Every drawing method reads `self.y`, draws at it, then calls `self.advance(dy)`. No method anywhere computes an absolute y by adding up a chain of constants by hand — that arithmetic is exactly where off-by-one and copy-paste errors live once a diagram has more than a handful of elements.

**Stack.** `Canvas.push(kind, **meta)` records the current cursor as a region's start, plus whatever you'll need later (an x-range, a guard label). `Canvas.pop()` returns that saved state once the region's content is done — at which point `self.y` IS the end position, so the enclosing frame can finally be drawn. Nesting falls out for free: push `alt`, push `loop` inside it, pop `loop` (draws the inner frame), keep going, pop `alt` (draws the outer frame around everything, including the now-already-drawn inner one). Order of drawing doesn't matter for correctness as long as frames use `fill="none"` — an unfilled rectangle never obscures what's already there regardless of when it's drawn.

**Two-pass / defer.** `Canvas.defer(fn)` queues a callback that receives the *final* cursor position and returns SVG. Call it for anything that structurally can't be finalized while content is still streaming in — most commonly a lifeline (top is known the moment a participant is declared, bottom is only known once the whole diagram is done) or an outer canvas border.

## 2. Why an open/close span tracker needs care

This is a real bug that showed up building the reference sequence diagram, not a hypothetical:

The `alt` fragment needed `OrderService` to send a return message in **each** of its two branches (`[stock available]` vs. `[else: out of stock]`). The naive activation-tracking logic — open a span when a sync message arrives, close it when that participant sends a return — closed `OrderService`'s span in the *first* branch. By the time the second branch's return fired, there was no open span left to close, so that branch's activation bar would have silently failed to render.

**Fix:** explicitly re-open the span right after the branch divider (`frag_div`/`close of the previous operand`), before drawing that branch's content.

**General lesson:** an open/close tracker assumes one linear timeline. The moment a diagram shows multiple *alternative* branches in one static picture — any `alt`, `if/else`, "one of these paths" construct — each branch needs its own local open/close accounting. Don't assume state (open spans, running totals, "currently active" flags) carries cleanly across a divider. Check explicitly.

## 3. Sequence / time-axis (proven)

Fixed x per participant, y advances with time, spans track "who's currently active."

```python
class SequenceCanvas(Canvas):
    def __init__(self, mode, participants):       # participants: {id: x}
        super().__init__(mode)
        self.px = dict(participants)

    def msg(self, fr, to, label, style="sync"):
        y = self.y
        # ...draw the arrow between self.px[fr] and self.px[to] at y...
        if style == "sync":
            self.open_span(to, y)
        if style == "return":
            self.close_span(fr, y, render=lambda s, e: activation_bar(self.px[fr], s, e))
        self.advance(50)
```

This is exactly what `Seq` in `gen_sequence_diagram_example.py` does (with more message styles, self-messages, create/destroy, and fragment handling) — read that file for the complete, working, QA'd version rather than rederiving it. Timing and Communication diagrams are close enough variants to start from the same base.

## 4. Timeline / Gantt

Fixed y per row, x is time/date, dependencies are edges between bar endpoints.

```python
class GanttCanvas(Canvas):
    def __init__(self, mode, day_width=20, label_col_width=200, row_height=32):
        super().__init__(mode)
        self.day_width, self.label_w, self.row_h = day_width, label_col_width, row_height
        self.bar_end = {}          # task_id -> (x_end, y_center), for drawing dependency arrows
        self.date_span = [None, None]   # tracked as rows are added, resolved at defer-time

    def row(self, task_id, label, start_day, duration_days, color=None):
        y = self.y
        x = self.label_w + start_day * self.day_width
        w = duration_days * self.day_width
        # ...draw label text at (10, y+18), bar rect at (x, y+4, w, row_h-8)...
        self.bar_end[task_id] = (x + w, y + self.row_h / 2)
        d0, d1 = self.date_span
        self.date_span = [start_day if d0 is None else min(d0, start_day),
                           start_day + duration_days if d1 is None else max(d1, start_day + duration_days)]
        self.advance(self.row_h)

    def dependency(self, from_task, to_task):
        fx, fy = self.bar_end[from_task]
        self.defer(lambda _fy: _elbow_arrow(fx, fy, to_task))   # to_task's start is known by now too
```

**Gotcha:** the timescale header (which day/week columns to draw, and how wide the canvas needs to be) depends on the earliest and latest dates across *every* row — that's a `defer()` candidate almost by definition, not something you can draw as the first row streams in. Track the running min/max as rows are added (as above), resolve the header in the deferred callback.

## 5. Graph / node-edge

Nodes placed on a grid or by rank; edges routed between node **boundaries**, never centers.

```python
class GraphCanvas(Canvas):
    def __init__(self, mode):
        super().__init__(mode)
        self.node_box = {}   # id -> (x, y, w, h), filled in as each node is placed

    def node(self, nid, x, y, w, h, label, shape="rect"):
        self.node_box[nid] = (x, y, w, h)
        # ...draw the shape via shape_kit primitives, centered label...

    def edge(self, from_id, to_id, label=""):
        self.defer(lambda _: self._draw_edge(from_id, to_id, label))

    def _draw_edge(self, from_id, to_id, label):
        fx, fy, fw, fh = self.node_box[from_id]
        tx, ty, tw, th = self.node_box[to_id]
        # find the nearest edge-midpoint on each box's boundary, not (fx+fw/2, fy+fh/2)
        # ...route + arrowhead...
```

**Gotcha:** routing from box centers means the line visibly cuts through both shapes' fills before the visual "trim" — even when the underlying math is correct, it reads as a bug. Always resolve to the boundary point nearest the other node, and defer edges until every node they touch has been placed (in case layout order doesn't match connection order).

## 6. Tree / hierarchy

Levels top-down (or left-right); parent-child connectors; sibling spacing is *the* two-pass case — width has to propagate bottom-up before position propagates top-down.

```python
class TreeCanvas(Canvas):
    def __init__(self, mode):
        super().__init__(mode)
        self.nodes = {}   # id -> {"label":, "parent":, "children": [...], "width": None, "x": None}

    def add(self, nid, label, parent=None):
        self.nodes[nid] = {"label": label, "parent": parent, "children": [], "width": None, "x": None}
        if parent:
            self.nodes[parent]["children"].append(nid)

    def layout(self, root, level_height=90, min_gap=20):
        def measure(nid):                      # pass 1: bottom-up
            n = self.nodes[nid]
            if not n["children"]:
                n["width"] = 140
            else:
                n["width"] = sum(measure(c) for c in n["children"]) + min_gap * (len(n["children"]) - 1)
            return n["width"]

        def place(nid, x_left, depth):         # pass 2: top-down
            n = self.nodes[nid]
            n["x"] = x_left + n["width"] / 2
            self.draw_node_at(nid, n["x"], depth * level_height)   # your box+label drawing
            cx = x_left
            for c in n["children"]:
                place(c, cx, depth + 1)
                cx += self.nodes[c]["width"] + min_gap

        measure(root)
        place(root, 0, 0)
        self.defer(lambda _: self._draw_connectors())   # every node's x is known only after place()
```

**Gotcha:** don't try to assign an x position while still adding children — a node's width depends on its *entire* subtree, which isn't known until every descendant has been added. This is why `layout()` is a separate, explicit two-pass step rather than something that happens incrementally inside `add()`.

## 7. Matrix / grid

Rows × columns of cells. This is already-proven math, not a sketch — it's the exact grid arithmetic used for the Basic & Primitive Shapes contact sheet (`gen_01_basic_primitive_shapes.py`) and the four foundation guideline pages (`gen_shape_guideline_svgs.py`): fixed column width + gutter, fixed row height + gutter, a cell's top-left is `(LM + col*(colW+gutter), top + row*(rowH+gutter))`. Reuse that directly rather than re-deriving it — the only thing that changes per diagram (SWOT, RACI, a Kanban board, an ER entity's attribute compartments) is what gets drawn *inside* each cell.

## 8. Swimlane

The sequence pattern rotated: lanes instead of lifelines, and flow is the *primary* advancing axis (often horizontal) with lane membership as the secondary dimension.

```python
class SwimlaneCanvas(Canvas):
    def __init__(self, mode, lanes):     # lanes: {id: y_top}
        super().__init__(mode)
        self.lane_y = dict(lanes)

    def step(self, lane_id, x, label, shape="rect"):
        y = self.lane_y[lane_id]
        # ...draw the shape at (x, y)...

    def flow(self, from_lane, from_x, to_lane, to_x, label=""):
        # can cross lanes (a handoff) -- draw as an elbow, not a straight
        # diagonal, so the "which lane owns this step" reading stays clear
        ...
```

If a BPMN or cross-functional flowchart is genuinely needed, start from `SequenceCanvas` above and swap which axis is the advancing one — the open/close span and stack mechanics transfer directly, only the axis and the "participant" concept (now "lane") change.

---

*A complete mapping from every diagram type in the master catalogue to one of these six families (plus honest notes on the few that don't fit cleanly) is in `diagram-catalogue.md`.*
