from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# Level style constants — matches the exact hex colours from the skill spec.
# ---------------------------------------------------------------------------
LEVEL_STYLES = {
    0: {
        "fill_color":   "#1a237e",
        "text_color":   "#FFFFFF",
        "border_color": "#1a237e",
        "font_size":    14,
        "font_bold":    True,
        "box_height":   1.0,
        "corner_radius": 0,
        "line_width":   2.0,
        "shadow":       True,
    },
    1: {
        "fill_color":   "#1565C0",
        "text_color":   "#FFFFFF",
        "border_color": "#1565C0",
        "font_size":    12,
        "font_bold":    True,
        "box_height":   0.9,
        "corner_radius": 6,
        "line_width":   1.5,
        "shadow":       True,
    },
    2: {
        "fill_color":   "#64B5F6",
        "text_color":   "#333333",
        "border_color": "#64B5F6",
        "font_size":    10,
        "font_bold":    False,
        "box_height":   0.8,
        "corner_radius": 6,
        "line_width":   1.0,
        "shadow":       True,
    },
    3: {
        "fill_color":   "#FFFFFF",
        "text_color":   "#333333",
        "border_color": "#64B5F6",
        "font_size":    9,
        "font_bold":    False,
        "box_height":   0.7,
        "corner_radius": 6,
        "line_width":   1.0,
        "shadow":       True,
    },
}


class LayoutEngine:
    """
    Solves N-ary tree layout coordinates using a simplified Reingold-Tilford
    approach to prevent child-node collisions across asymmetric branches.

    Coordinate convention
    ─────────────────────
    • Level 0 (Project Root) is drawn at the TOP of the page.
    • Children branch downward with increasing Y-offset.
    • All boxes are centred horizontally over their subtree extent.
    • Connector routing is orthogonal (right-angle), no arrowheads.
    """

    def __init__(self, page_width: float, page_height: float, config: Dict = None):
        layout_cfg       = (config or {}).get("layout", {})
        self.page_width  = page_width
        self.page_height = page_height
        self.margin      = layout_cfg.get("margin", 0.5)
        self.title_h     = 1.5           # Height reserved for the title block
        self.v_spacing   = layout_cfg.get("level_spacing", 1.5)
        self.box_spacing = (config or {}).get("styling", {}).get("box_spacing", 0.3)

        # Map level → box height from LEVEL_STYLES
        self.level_heights = {lvl: meta["box_height"] for lvl, meta in LEVEL_STYLES.items()}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def calculate_tree(self, wbs_spec: Dict) -> Dict:
        """
        Entry point.  Returns a positions dict keyed by node id.

        Coordinate convention: Y increases downward from the top of the drawable area
        (diagram_builder converts to Visio bottom-origin coordinates).
        """
        positions: Dict[str, Dict] = {}
        layout_style = wbs_spec.get("styling", {}).get("layout_style", "tree")
        if layout_style == "org_chart":
            self.box_spacing = max(0.15, self.box_spacing * 0.5)
            self.v_spacing = max(1.0, self.v_spacing * 0.85)

        root_w = self._estimate_subtree_width(wbs_spec.get("branches", []), level=1)
        root_w = max(root_w, 3.5)
        root_x = self.page_width / 2.0
        root_y = self.margin + self.title_h + self.level_heights[0] / 2.0

        root_node = wbs_spec.get("levels", {}).get("level_0", {})
        positions["0"] = {
            "id": "0",
            "x": root_x,
            "y": root_y,
            "w": root_w,
            "h": self.level_heights[0],
            "level": 0,
            "name": root_node.get("name", "Project"),
            "parent": None,
        }

        self._layout_children(
            children=wbs_spec.get("branches", []),
            level=1,
            parent_x=root_x,
            parent_y=root_y,
            avail_w=self.page_width - 2 * self.margin,
            x_origin=self.margin,
            positions=positions,
            parent_id="0",
        )

        self._verify_no_overlap(positions)
        return positions

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _layout_children(
        self,
        children: List[Dict],
        level: int,
        parent_x: float,
        parent_y: float,
        avail_w: float,
        x_origin: float,
        positions: Dict,
        parent_id: str = "0",
    ) -> None:
        """Recursively lay out a list of sibling nodes at `level`."""
        if not children or level > 3:
            return

        box_h = self.level_heights[level]
        node_y = parent_y + self.level_heights[level - 1] / 2.0 + self.v_spacing + box_h / 2.0

        leaf_counts = [self._count_leaves(n) for n in children]
        total_leaves = max(sum(leaf_counts), len(children))
        total_spacing = self.box_spacing * (len(children) - 1)
        drawable_w = avail_w - total_spacing

        x_cursor = x_origin
        for i, node in enumerate(children):
            proportion = leaf_counts[i] / total_leaves
            node_w = max(drawable_w * proportion, 1.5)
            node_cx = x_cursor + node_w / 2.0

            positions[node["id"]] = {
                "id": node["id"],
                "x": node_cx,
                "y": node_y,
                "w": node_w,
                "h": box_h,
                "level": level,
                "name": node.get("name", node["id"]),
                "parent": parent_id,
            }

            if "children" in node:
                self._layout_children(
                    children=node["children"],
                    level=level + 1,
                    parent_x=node_cx,
                    parent_y=node_y,
                    avail_w=node_w,
                    x_origin=x_cursor,
                    positions=positions,
                    parent_id=node["id"],
                )

            x_cursor += node_w + self.box_spacing

    def _verify_no_overlap(self, positions: Dict) -> None:
        from core.errors import LayoutError

        by_level: Dict[int, List[Dict]] = {}
        for pos in positions.values():
            by_level.setdefault(pos["level"], []).append(pos)
        for level, nodes in by_level.items():
            nodes.sort(key=lambda n: n["x"])
            for i in range(len(nodes) - 1):
                a, b = nodes[i], nodes[i + 1]
                gap = (b["x"] - a["x"]) - (a["w"] + b["w"]) / 2.0
                if gap < -0.05:
                    raise LayoutError(
                        f"Nodes '{a['id']}' and '{b['id']}' overlap at level {level}. "
                        "Increase page_size or level_spacing."
                    )

    def _count_leaves(self, node: Dict) -> int:
        """Count leaf nodes under a node (returns 1 if no children)."""
        if "children" not in node or not node["children"]:
            return 1
        return sum(self._count_leaves(c) for c in node["children"])

    def _estimate_subtree_width(self, nodes: List[Dict], level: int) -> float:
        """Estimate total horizontal space required by a list of nodes."""
        if not nodes:
            return 2.0
        total_leaves = sum(self._count_leaves(n) for n in nodes)
        return total_leaves * 2.0 + self.box_spacing * (len(nodes) - 1)
