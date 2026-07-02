from typing import Dict, List
from collections import defaultdict


class LayoutEngine:
    """Assigns AON nodes to depth levels (left→right) with vertical stacking."""

    def __init__(
        self,
        activities: List[Dict],
        config: Dict,
        page_width: float = 59.4,
        page_height: float = 42.0,
    ):
        self.activities = activities
        self.config = config
        self.page_width = page_width
        self.page_height = page_height
        layout = config.get("layout", {})
        self.level_spacing = layout.get("level_spacing", 3.0)
        self.node_spacing = layout.get("node_spacing", 1.5)
        self.margin = layout.get("margin", 0.5)
        self.title_h = 2.0
        self.summary_h = 2.0
        self.node_w = config.get("styling", {}).get("node_width", 3.2)
        self.node_h = config.get("styling", {}).get("node_height", 2.2)

    def calculate(self) -> Dict[str, Dict[str, float]]:
        levels = self._assign_levels()
        positions: Dict[str, Dict[str, float]] = {}
        max_level = max(levels.keys()) if levels else 0

        drawable_w = self.page_width - 2 * self.margin - self.node_w
        if max_level > 0:
            x_step = drawable_w / max_level
        else:
            x_step = self.level_spacing

        for level, nodes in levels.items():
            x = self.margin + self.node_w / 2 + level * x_step
            count = len(nodes)
            total_h = count * self.node_h + max(0, count - 1) * self.node_spacing
            usable_h = self.page_height - self.margin * 2 - self.title_h - self.summary_h
            start_y = self.margin + self.summary_h + (usable_h - total_h) / 2 + self.node_h / 2

            for idx, nid in enumerate(nodes):
                y = start_y + idx * (self.node_h + self.node_spacing)
                positions[nid] = {"x": x, "y": y}

        return positions

    def _assign_levels(self) -> Dict[int, List[str]]:
        levels: Dict[int, List[str]] = defaultdict(list)
        depths: Dict[str, int] = {}

        for act in self.activities:
            preds = act.get("predecessors", [])
            if not preds:
                d = 0
            else:
                max_d = 0
                for p in preds:
                    pid = p["id"] if isinstance(p, dict) else p
                    if pid in depths:
                        max_d = max(max_d, depths[pid])
                d = max_d + 1
            depths[act["id"]] = d
            levels[d].append(act["id"])

        return dict(levels)
