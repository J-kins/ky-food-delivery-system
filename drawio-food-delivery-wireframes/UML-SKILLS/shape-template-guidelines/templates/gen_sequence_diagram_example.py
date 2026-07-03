#!/usr/bin/env python3
"""Example: UML Sequence Diagram — comprehensive reference.

One coherent scenario (order checkout) built to exercise every core
sequence-diagram element: actor + object lifelines, activation bars,
sync / async / return messages, self-messages, create / destroy, and
nested alt / opt / loop / par / ref combined fragments.
"""
import os
from shape_kit import (
    L_CANVAS, L_FILL, L_STROKE, L_MUTED,
    D_CANVAS, D_FILL, D_STROKE, D_MUTED,
    T, R, L, C, POLY, PATH, ARROW, OPEN_ARROW,
)

OUT = "/mnt/user-data/outputs/shape-library/diagram-examples"
os.makedirs(OUT, exist_ok=True)

W = 1450

CUSTOMER, WEBAPP, ORDER, INV, PAY, NOTIFY = "customer", "webapp", "order", "inv", "pay", "notify"
PX = {CUSTOMER: 100, WEBAPP: 340, ORDER: 580, INV: 820, PAY: 1060, NOTIFY: 1300}


class Seq:
    def __init__(self, mode):
        self.mode = mode
        self.fc = L_FILL if mode == "light" else D_FILL
        self.ink = L_STROKE if mode == "light" else D_STROKE
        self.muted = L_MUTED if mode == "light" else D_MUTED
        self.canvas = L_CANVAS if mode == "light" else D_CANVAS
        self.body = ""
        self.y = 0
        self.px = dict(PX)
        self.active = {}
        self.top = {}
        self.bottom = {}
        self.stack = []
        self.n = 0

    def uid(self, pre):
        self.n += 1
        return f"{pre}{self.n}"

    # ---- participant headers ----
    def actor_header(self, pid, label):
        x = self.px[pid]
        cy = 108
        self.body += C(self.uid("h"), x, cy, 9, self.fc, self.ink, 1.6)
        self.body += L(self.uid("h"), x, cy + 9, x, cy + 34, self.ink, 1.6)
        self.body += L(self.uid("h"), x - 13, cy + 17, x + 13, cy + 17, self.ink, 1.6)
        self.body += L(self.uid("h"), x, cy + 34, x - 11, cy + 50, self.ink, 1.6)
        self.body += L(self.uid("h"), x, cy + 34, x + 11, cy + 50, self.ink, 1.6)
        self.body += T(self.uid("h"), x, 166, label, 11, "600", self.ink, "middle")
        self.top[pid] = 172

    def object_header(self, pid, label, w=190, h=46):
        x = self.px[pid]
        y0 = 172 - h
        self.body += R(self.uid("h"), x - w / 2, y0, w, h, self.fc, 6, self.ink, 1.6)
        self.body += T(self.uid("h"), x, 172 - h / 2 + 4, label, 11.5, "500", self.ink, "middle")
        self.top[pid] = 172

    def start(self, y):
        self.y = y

    # ---- activation ----
    def _edge(self, pid, other_x):
        cx = self.px[pid]
        if self.active.get(pid) is not None:
            return cx + (5 if other_x > cx else -5)
        return cx

    def activate(self, pid, y=None):
        if self.active.get(pid) is None:
            self.active[pid] = self.y if y is None else y

    def deactivate(self, pid, y=None):
        start = self.active.get(pid)
        if start is not None:
            end = self.y if y is None else y
            x = self.px[pid]
            self.body += R(self.uid("a"), x - 5, start, 10, max(end - start, 4), self.fc, 0, self.ink, 1.3)
            self.active[pid] = None

    # ---- messages ----
    def msg(self, fr, to, label, style="sync"):
        y = self.y
        x1r, x2r = self.px[fr], self.px[to]
        x1 = self._edge(fr, x2r)
        pre_active = self.active.get(to) is not None
        x2 = x2r + ((5 if x1r < x2r else -5) if pre_active else 0)
        dash = "6,4" if style == "return" else None
        hollow = style in ("async", "return")
        direction = "right" if x2r > x1r else "left"
        self.body += T(self.uid("m"), (x1r + x2r) / 2, y - 7, label,
                        10.3, "600" if style == "sync" else "400", self.ink, "middle")
        self.body += L(self.uid("m"), x1, y, x2, y, self.ink, 1.6 if style != "return" else 1.3, dash=dash)
        self.body += ARROW(self.uid("m"), x2, y, direction, 8.5, self.ink, hollow=hollow)
        if style == "sync":
            self.activate(to, y)
        if style == "return":
            self.deactivate(fr, y)
        self.y += 50

    def self_msg(self, pid, label):
        y0 = self.y
        edge = self._edge(pid, self.px[pid] + 100)
        w = 48
        d = (f"M {edge:.1f},{y0:.1f} L {edge+w:.1f},{y0:.1f} "
             f"L {edge+w:.1f},{y0+26:.1f} L {edge+4:.1f},{y0+26:.1f}")
        self.body += PATH(self.uid("s"), d, "none", self.ink, 1.5)
        self.body += ARROW(self.uid("s"), edge + 4, y0 + 26, "left", 7, self.ink)
        self.body += T(self.uid("s"), edge + w + 8, y0 + 16, label, 10, "500", self.ink, "start")
        self.y += 65

    def create(self, fr, to, arrow_label, box_label, w=190, h=46):
        y = self.y
        x1 = self._edge(fr, self.px[to])
        x2 = self.px[to]
        self.body += T(self.uid("c"), (x1 + x2) / 2, y - 7, arrow_label, 10, "500", self.ink, "middle")
        self.body += L(self.uid("c"), x1, y, x2 - w / 2, y, self.ink, 1.4, dash="6,4")
        self.body += OPEN_ARROW(self.uid("c"), x2 - w / 2, y, "right", 8, self.ink)
        self.body += R(self.uid("c"), x2 - w / 2, y - h / 2, w, h, self.fc, 6, self.ink, 1.6)
        self.body += T(self.uid("c"), x2, y + 4, box_label, 11.5, "500", self.ink, "middle")
        self.top[to] = y
        self.y += 55

    def destroy(self, pid):
        y = self.y
        self.deactivate(pid, y)
        x = self.px[pid]
        s = 9
        self.body += L(self.uid("d"), x - s, y - s, x + s, y + s, self.ink, 2.2)
        self.body += L(self.uid("d"), x - s, y + s, x + s, y - s, self.ink, 2.2)
        self.bottom[pid] = y
        self.y += 40

    def note(self, pids, lines):
        xs = [self.px[p] for p in pids]
        cx = sum(xs) / len(xs)
        w = max(200, 40 + 7.2 * max(len(ln) for ln in lines))
        h = 22 + 16 * len(lines)
        y = self.y
        fold = 12
        x0 = cx - w / 2
        pts = [(x0, y), (x0 + w - fold, y), (x0 + w, y + fold), (x0 + w, y + h), (x0, y + h)]
        self.body += POLY(self.uid("n"), pts, self.fc, self.ink, 1.3)
        self.body += PATH(self.uid("n"),
                           f"M {x0+w-fold:.1f},{y:.1f} L {x0+w-fold:.1f},{y+fold:.1f} L {x0+w:.1f},{y+fold:.1f}",
                           "none", self.ink, 1.0)
        for i, ln in enumerate(lines):
            self.body += T(self.uid("n"), x0 + 14, y + 22 + i * 16, ln, 9.5, "400", self.ink, "start")
        self.y += h + 16

    def ref(self, pids, label):
        xs = [self.px[p] for p in pids]
        x0, x1 = min(xs) - 50, max(xs) + 50
        y = self.y
        h = 44
        self.body += R(self.uid("r"), x0, y, x1 - x0, h, "none", 0, self.ink, 1.4)
        self._tab(x0, y, "ref")
        self.body += T(self.uid("r"), (x0 + x1) / 2, y + h / 2 + 4, label, 11, "600", self.ink, "middle")
        self.y += h + 16

    # ---- fragments ----
    def _tab(self, x, y, keyword):
        w, hgt, cut = 42, 22, 9
        pts = [(x, y), (x + w, y), (x + w, y + hgt - cut), (x + w - cut, y + hgt), (x, y + hgt)]
        self.body += POLY(self.uid("t"), pts, self.fc, self.ink, 1.3)
        self.body += T(self.uid("t"), x + 7, y + 15, keyword, 9.5, "700", self.ink, "start")
        return w, hgt

    def frag_start(self, kind, guard, x0, x1):
        y0 = self.y
        tw, th = self._tab(x0, y0, kind)
        if guard:
            self.body += T(self.uid("g"), x0 + tw + 8, y0 + 15, guard, 10, "400", self.muted, "start")
        self.stack.append({"kind": kind, "y0": y0, "x0": x0, "x1": x1})
        self.y += th + 14

    def frag_div(self, guard):
        f = self.stack[-1]
        y = self.y
        self.body += L(self.uid("fd"), f["x0"], y, f["x1"], y, self.ink, 1.2, dash="4,4")
        if guard:
            self.body += T(self.uid("fd"), f["x0"] + 8, y + 15, guard, 10, "400", self.muted, "start")
        self.y += 28

    def frag_end(self):
        f = self.stack.pop()
        y1 = self.y + 14
        self.body += R(self.uid("f"), f["x0"], f["y0"], f["x1"] - f["x0"], y1 - f["y0"],
                        "none", 0, self.ink, 1.4)
        self.y = y1

    # ---- finalize ----
    def render(self, title, subtitle):
        final_y = self.y
        lifelines = ""
        for pid, x in self.px.items():
            if pid not in self.top:
                continue
            y0 = self.top[pid]
            y1 = self.bottom.get(pid, final_y)
            lifelines += L(self.uid("ll"), x, y0, x, y1, self.muted, 1.3, dash="4,4")
        header = (
            T("title", 60, 42, title, 21, "700", self.ink, ls=-0.3)
            + T("subtitle", 60, 64, subtitle, 11.5, "400", self.muted)
            + L("title-rule", 60, 80, W - 60, 80, self.muted, 0.6)
        )
        legend = self._legend(final_y + 30)
        full_h = final_y + 120
        full_body = header + lifelines + self.body + legend
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {full_h:.0f}" '
            f'width="{W}" height="{full_h:.0f}">\n'
            f'  <rect width="{W}" height="{full_h:.0f}" fill="{self.canvas}"/>\n'
            f'{full_body}</svg>\n'
        )

    def _legend(self, y):
        items = [("sync", "Sync call"), ("async", "Async call"),
                 ("return", "Return"), ("create", "Create"), ("destroy", "Destroy")]
        out = T("lg-hdr", 60, y, "NOTATION", 8.5, "700", self.muted, ls=1.5)
        x = 60
        y2 = y + 22
        for kind, label in items:
            if kind == "sync":
                out += L(self.uid("lg"), x, y2, x + 50, y2, self.ink, 1.6)
                out += ARROW(self.uid("lg"), x + 58, y2, "right", 7, self.ink)
            elif kind == "async":
                out += L(self.uid("lg"), x, y2, x + 50, y2, self.ink, 1.6)
                out += OPEN_ARROW(self.uid("lg"), x + 58, y2, "right", 7, self.ink)
            elif kind in ("return", "create"):
                out += L(self.uid("lg"), x, y2, x + 50, y2, self.ink, 1.3, dash="6,4")
                out += OPEN_ARROW(self.uid("lg"), x + 58, y2, "right", 7, self.ink)
            elif kind == "destroy":
                s = 6
                out += L(self.uid("lg"), x + 25 - s, y2 - s, x + 25 + s, y2 + s, self.ink, 2)
                out += L(self.uid("lg"), x + 25 - s, y2 + s, x + 25 + s, y2 - s, self.ink, 2)
            out += T(self.uid("lg"), x + 70, y2 + 4, label, 9.5, "400", self.muted, "start")
            x += 200
        return out


def scenario(mode):
    s = Seq(mode)
    s.actor_header(CUSTOMER, "Customer")
    s.object_header(WEBAPP, "web : WebApp")
    s.object_header(ORDER, "order : OrderService")
    s.object_header(INV, "inventory : InventoryService")
    s.object_header(PAY, "payment : PaymentGateway")
    s.start(210)

    s.msg(CUSTOMER, WEBAPP, "submitOrder(cart)", "sync")
    s.msg(WEBAPP, ORDER, "createOrder(cart)", "sync")
    s.self_msg(ORDER, "validateItems()")

    s.frag_start("opt", "[loyaltyMember]", s.px[ORDER] - 95, s.px[ORDER] + 300)
    s.self_msg(ORDER, "applyLoyaltyDiscount()")
    s.frag_end()

    s.frag_start("alt", "[stock available]", s.px[WEBAPP] - 40, s.px[NOTIFY] + 110)

    s.msg(ORDER, INV, "reserveStock(items)", "sync")
    s.msg(INV, ORDER, "reserved", "return")
    s.msg(ORDER, PAY, "authorize(amount)", "sync")

    s.frag_start("loop", "[retry up to 3\u00d7]", s.px[PAY] - 90, s.px[PAY] + 210)
    s.self_msg(PAY, "attemptAuthorization()")
    s.frag_end()

    s.msg(PAY, ORDER, "authorized", "return")

    s.frag_start("par", "[finalize concurrently]", s.px[ORDER] - 40, s.px[PAY] + 40)
    s.msg(ORDER, INV, "commitStock()", "async")
    s.frag_div("")
    s.msg(ORDER, PAY, "captureFunds()", "async")
    s.frag_end()

    s.ref([INV, PAY], "Payment Reconciliation")

    s.create(ORDER, NOTIFY, "\u00abcreate\u00bb", "notify : NotificationService")
    s.msg(ORDER, NOTIFY, "send(order)", "sync")
    s.note([NOTIFY], ["Composes and dispatches", "the confirmation email"])
    s.msg(NOTIFY, ORDER, "queued", "return")

    s.msg(ORDER, WEBAPP, "orderConfirmed(orderId)", "return")

    s.frag_div("[else: out of stock]")
    s.activate(ORDER)
    s.msg(ORDER, WEBAPP, "orderRejected(reason)", "return")

    s.frag_end()

    s.msg(WEBAPP, CUSTOMER, "showConfirmation()", "return")
    s.destroy(NOTIFY)

    title = "Sequence Diagram \u2014 Order Checkout (Comprehensive Example)"
    subtitle = ("Every core element in one scenario: lifelines, activation bars, sync / async / return "
                "messages, self-messages, create / destroy, and alt / opt / loop / par / ref fragments.")
    return s.render(title, subtitle)


if __name__ == "__main__":
    for mode in ("light", "dark"):
        svg = scenario(mode)
        path = os.path.join(OUT, f"diagram-sequence-order-checkout-{mode}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  ok  {path}  ({len(svg)} bytes)")
