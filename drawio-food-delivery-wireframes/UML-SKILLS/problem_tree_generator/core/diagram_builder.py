import logging
from typing import Dict, Any, List

from renderers.aspose_renderer import (
    Diagram, SaveFileFormat, add_rectangle, add_connector
)

log = logging.getLogger(__name__)

# ── Color palette per SKILL.md §5.1 ──────────────────────────────────────────
TIER_STYLES = {
    "root": {
        "fill":   "#EF9A9A",
        "border": "#E53935",
        "text":   "#B71C1C",
        "label":  "ROOT – Cause",
    },
    "trunk": {
        "fill":   "#FFCC80",
        "border": "#F57C00",
        "text":   "#E65100",
        "label":  "TRUNK – Core Problem",
    },
    "branch": {
        "fill":   "#90CAF9",
        "border": "#1565C0",
        "text":   "#0D47A1",
        "label":  "BRANCH – Direct Effect",
    },
    "leaf": {
        "fill":   "#A5D6A7",
        "border": "#2E7D32",
        "text":   "#1B5E20",
        "label":  "LEAF – Long-Term Effect",
    },
}

CONNECTOR_COLOR = "#666666"


class ProblemTreeBuilder:
    """
    Builds a Problem Tree Diagram in a fixed 4-tier hierarchical layout:

        LEAF   (top)       — long-term effects
        BRANCH (upper-mid) — direct effects
        TRUNK  (center)    — core problem
        ROOT   (bottom)    — root causes

    All connections flow bottom-up: ROOT → TRUNK → BRANCH → LEAF.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()

        self.styling = config.get("styling", {})
        self.font_family = self.styling.get("font_family", "Arial")
        self.font_size = float(self.styling.get("font_size", 10.0))
        self.shadow = self.styling.get("shadow_enabled", True)

        layout = config.get("layout", {})
        self.margin = float(layout.get("margin", 0.5))
        self.node_spacing = float(layout.get("node_spacing", 0.5))
        self.rank_spacing = float(layout.get("rank_spacing", 1.2))

        # Shape id registries — populated during each add_* call
        self.root_ids:   List[int] = []
        self.trunk_id:   int = -1
        self.branch_ids: List[int] = []
        self.leaf_ids:   List[int] = []

    # ─── Page setup ──────────────────────────────────────────────────────────

    def _setup_page(self) -> None:
        layout = self.config.get("layout", {})
        page_size = layout.get("page_size", "A3")
        if page_size == "A2":
            w, h = 23.39, 16.54   # landscape A2 in inches
        elif page_size == "A4":
            w, h = 11.69, 8.27
        else:                      # default A3 landscape
            w, h = 16.54, 11.69
        self.page_w = w
        self.page_h = h
        self.page.page_sheet.page_props.page_width.value = w
        self.page.page_sheet.page_props.page_height.value = h

    # ─── Geometry helpers ────────────────────────────────────────────────────

    def _node_width(self, n_nodes: int, tier: str = "") -> float:
        """Calculate per-node box width so the whole tier fills the page."""
        usable = self.page_w - (2 * self.margin)
        if n_nodes == 0:
            return usable
        total_spacing = (n_nodes - 1) * self.node_spacing
        return (usable - total_spacing) / n_nodes

    def _tier_y(self, tier: str) -> float:
        """
        Y-coordinate (centre) of each horizontal tier.
        Layout (bottom → top in Visio coordinate space where Y=0 is bottom):
          ROOT   → y = margin + h/2  (bottom row)
          TRUNK  → ROOT + rank_spacing + node_h
          BRANCH → TRUNK + rank_spacing + node_h
          LEAF   → BRANCH + rank_spacing + node_h
        """
        node_h = 1.5   # fixed node height in inches
        base = self.margin + node_h / 2.0
        step = self.rank_spacing + node_h
        tier_order = {"root": 0, "trunk": 1, "branch": 2, "leaf": 3}
        return base + tier_order[tier] * step

    def _row_xs(self, n_nodes: int) -> List[float]:
        """Return x-centre positions for n_nodes evenly spaced across the page."""
        if n_nodes == 0:
            return []
        node_w = self._node_width(n_nodes)
        start_x = self.margin + node_w / 2.0
        return [start_x + i * (node_w + self.node_spacing) for i in range(n_nodes)]

    # ─── Drawing steps ───────────────────────────────────────────────────────

    def add_title_block(self) -> None:
        title    = self.config.get("title", "Problem Tree")
        project  = self.config.get("project_name", "")
        version  = self.config.get("version", "1.0")
        date     = self.config.get("date", "")
        h = 0.7
        text = f"{title} — {project}" if project else title
        text += f"\nVersion {version}"
        if date:
            text += f"  |  {date}"
        add_rectangle(
            self.page,
            x=self.page_w / 2.0,
            y=self.page_h - self.margin - h / 2.0,
            w=self.page_w - (2 * self.margin),
            h=h,
            text=text,
            fill_color="#1a237e",
            text_color="#FFFFFF",
            border_color="#1a237e",
            font_family=self.font_family,
            font_size=self.font_size + 2.0,
            font_bold=True,
        )

    def add_roots(self, roots: List[Dict]) -> None:
        if not roots:
            return
        n = len(roots)
        node_w = self._node_width(n)
        node_h = 1.5
        y = self._tier_y("root")
        xs = self._row_xs(n)
        style = TIER_STYLES["root"]
        for i, (root, x) in enumerate(zip(roots, xs)):
            text = f"{root['id']}: {root['statement']}"
            sid = add_rectangle(
                self.page, x, y, node_w, node_h,
                text=text,
                fill_color=style["fill"],
                text_color=style["text"],
                border_color=style["border"],
                font_family=self.font_family,
                font_size=self.font_size,
                shadow=self.shadow,
            )
            self.root_ids.append(sid)
        log.debug(f"Added {n} ROOT node(s).")

    def add_trunk(self, core_problem: Dict) -> None:
        node_w = self._node_width(1)
        node_h = 1.5
        y = self._tier_y("trunk")
        x = self.page_w / 2.0
        style = TIER_STYLES["trunk"]
        text = f"CORE PROBLEM\n{core_problem['statement']}"
        self.trunk_id = add_rectangle(
            self.page, x, y, node_w * 0.6, node_h * 1.2,
            text=text,
            fill_color=style["fill"],
            text_color=style["text"],
            border_color=style["border"],
            font_family=self.font_family,
            font_size=self.font_size,
            font_bold=True,
            shadow=self.shadow,
        )
        log.debug("Added TRUNK (core problem) node.")

    def add_branches(self, branches: List[Dict]) -> None:
        if not branches:
            return
        n = len(branches)
        node_w = self._node_width(n)
        node_h = 1.5
        y = self._tier_y("branch")
        xs = self._row_xs(n)
        style = TIER_STYLES["branch"]
        for branch, x in zip(branches, xs):
            text = f"{branch['id']}: {branch['statement']}"
            sid = add_rectangle(
                self.page, x, y, node_w, node_h,
                text=text,
                fill_color=style["fill"],
                text_color=style["text"],
                border_color=style["border"],
                font_family=self.font_family,
                font_size=self.font_size,
                shadow=self.shadow,
            )
            self.branch_ids.append(sid)
        log.debug(f"Added {n} BRANCH node(s).")

    def add_leaf(self, leaf_nodes: List[Dict]) -> None:
        if not leaf_nodes:
            return
        n = len(leaf_nodes)
        node_w = self._node_width(n)
        node_h = 1.5
        y = self._tier_y("leaf")
        xs = self._row_xs(n)
        style = TIER_STYLES["leaf"]
        for leaf, x in zip(leaf_nodes, xs):
            text = f"{leaf['id']}: {leaf['statement']}"
            sid = add_rectangle(
                self.page, x, y, node_w, node_h,
                text=text,
                fill_color=style["fill"],
                text_color=style["text"],
                border_color=style["border"],
                font_family=self.font_family,
                font_size=self.font_size,
                shadow=self.shadow,
            )
            self.leaf_ids.append(sid)
        log.debug(f"Added {n} LEAF node(s).")

    def add_connectors(self) -> None:
        """
        Wire up all causal arrows:
          ROOT(s)  → TRUNK
          TRUNK    → BRANCH(es)
          BRANCH(es) → LEAF(s)
        """
        log.debug("Adding connectors...")

        # Roots → Trunk
        for rid in self.root_ids:
            add_connector(
                self.page, rid, self.trunk_id,
                line_color=CONNECTOR_COLOR,
            )

        # Trunk → Branches
        for bid in self.branch_ids:
            add_connector(
                self.page, self.trunk_id, bid,
                line_color=CONNECTOR_COLOR,
            )

        # Branches → Leaf
        for lid in self.leaf_ids:
            # Connect every branch to every leaf (fan-out)
            for bid in self.branch_ids:
                add_connector(
                    self.page, bid, lid,
                    line_color=CONNECTOR_COLOR,
                )

    def add_legend(self) -> None:
        """Draw a compact colour-coded legend at the bottom-right corner."""
        legend_text = (
            "Legend\n"
            "⬛ ROOT (Causes)  |  🟠 TRUNK (Core Problem)\n"
            "🔵 BRANCH (Direct Effects)  |  🟢 LEAF (Long-Term Effects)\n"
            "↑ Arrows show causal direction: ROOT → TRUNK → BRANCH → LEAF"
        )
        w, h = 8.0, 1.2
        x = self.page_w - self.margin - w / 2.0
        y = self.margin + h / 2.0
        add_rectangle(
            self.page, x, y, w, h,
            text=legend_text,
            fill_color="#F5F5F5",
            text_color="#444444",
            border_color="#BDBDBD",
            font_family=self.font_family,
            font_size=self.font_size - 1.5,
        )
        log.debug("Added legend.")

    def save(self, output_path: str) -> None:
        self.diagram.save(output_path, SaveFileFormat.VSDX)
        log.debug(f"[dry-run] Saved diagram to {output_path}")
