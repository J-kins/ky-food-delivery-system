#!/usr/bin/env python3
"""diagram_kit — generalized layout engine for assembling complete diagrams.

Companion to shape_kit.py (shape primitives + design tokens) and the
diagram-layout-patterns skill. Provides Canvas: a cursor + nesting-stack +
two-pass-rendering base class, extracted from a working UML sequence-diagram
implementation (see gen_sequence_diagram_example.py / the Seq class). Subclass
it per diagram family (sequence, Gantt, flowchart, tree, matrix, swimlane)
rather than hand-tracking positions from scratch.

Requires shape_kit.py alongside it (color tokens + T/L primitives).
"""
from shape_kit import (
    L_CANVAS, L_FILL, L_STROKE, L_MUTED,
    D_CANVAS, D_FILL, D_STROKE, D_MUTED,
    T, L,
)


class Canvas:
    """Cursor + stack + deferred-rendering base for any diagram family.

    - self.y is a monotonically advancing cursor. Draw at self.y, then call
      self.advance() to move it. Never hand-type a y that isn't either the
      current cursor or derived from a value you stored earlier.
    - self.open_span / self.close_span tracks anything with a start that's
      only closed later (activation bars, Gantt bars, highlighted ranges).
      IMPORTANT: an open/close tracker assumes one linear timeline. If a
      diagram shows multiple alternative branches in one static picture
      (alt/if-else, one-of-these-paths), each branch needs its own local
      open/close accounting -- state does not carry cleanly across a
      divider. See references/layout-patterns.md for the concrete case
      this bit a real build.
    - self.push / self.pop / self.top track nested regions (fragments,
      swimlanes, subgraphs, grouped branches) -- push on enter with
      whatever metadata you'll need at pop-time, pop once the end position
      is known, *then* draw the enclosing frame.
    - self.defer registers a callback that runs once total height is known
      -- for anything (lifelines, a dynamic timescale header, an outer
      border) that can't be finalized until everything else has been drawn.
    """

    def __init__(self, mode="light", width=1280):
        self.mode = mode
        self.fc = L_FILL if mode == "light" else D_FILL
        self.ink = L_STROKE if mode == "light" else D_STROKE
        self.muted = L_MUTED if mode == "light" else D_MUTED
        self.canvas_color = L_CANVAS if mode == "light" else D_CANVAS
        self.w = width
        self.y = 0
        self.body = ""
        self._deferred = []
        self._spans = {}
        self._stack = []
        self._n = 0

    # ---- identifiers ----
    def uid(self, prefix="e"):
        self._n += 1
        return f"{prefix}{self._n}"

    # ---- cursor ----
    def advance(self, dy):
        self.y += dy
        return self.y

    def draw(self, svg_fragment):
        self.body += svg_fragment

    # ---- open/close span tracking ----
    def open_span(self, key, y=None):
        if self._spans.get(key) is None:
            self._spans[key] = self.y if y is None else y

    def close_span(self, key, y=None, render=None):
        start = self._spans.get(key)
        if start is None:
            return None
        end = self.y if y is None else y
        if render:
            self.draw(render(start, end))
        self._spans[key] = None
        return (start, end)

    def is_open(self, key):
        return self._spans.get(key) is not None

    # ---- nesting stack ----
    def push(self, kind, **meta):
        self._stack.append({"kind": kind, "y0": self.y, **meta})
        return self._stack[-1]

    def pop(self):
        return self._stack.pop() if self._stack else None

    def top(self):
        return self._stack[-1] if self._stack else None

    # ---- two-pass / deferred rendering ----
    def defer(self, fn):
        """fn(final_y: float) -> svg fragment (string). Runs at finalize()."""
        self._deferred.append(fn)

    # ---- output ----
    def finalize(self, title="", subtitle=""):
        final_y = self.y
        deferred_svg = "".join(fn(final_y) for fn in self._deferred)
        full_h = final_y + 120
        header = ""
        if title:
            header += T("title", 60, 42, title, 21, "700", self.ink, ls=-0.3)
        if subtitle:
            header += T("subtitle", 60, 64, subtitle, 11.5, "400", self.muted)
        if title or subtitle:
            header += L("title-rule", 60, 80, self.w - 60, 80, self.muted, 0.6)
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {full_h:.0f}" '
            f'width="{self.w}" height="{full_h:.0f}">\n'
            f'  <rect width="{self.w}" height="{full_h:.0f}" fill="{self.canvas_color}"/>\n'
            f'{header}{deferred_svg}{self.body}</svg>\n'
        )


if __name__ == "__main__":
    # Smoke test: not a real diagram -- just proves the base class round-trips
    # through push/pop, open/close span, defer, and finalize without error,
    # and that the result is valid XML.
    import xml.dom.minidom as minidom

    c = Canvas("light", width=600)
    c.advance(40)
    frag = c.push("demo-fragment")
    c.open_span("demo-actor")
    c.draw(T("t1", 40, c.y, "hello", 12, "500", c.ink))
    c.advance(30)
    c.close_span("demo-actor",
                  render=lambda s, e: T("t2", 40, e, f"span {s:.0f}-{e:.0f}", 10, "400", c.muted))
    c.pop()
    c.defer(lambda fy: T("t3", 40, fy - 10, f"fragment started at {frag['y0']:.0f}", 9, "400", c.muted))
    c.advance(20)
    svg = c.finalize(title="Canvas smoke test", subtitle="Not a real diagram -- proves the base class works")
    minidom.parseString(svg)
    print("Canvas smoke test OK -- valid XML, length", len(svg))
