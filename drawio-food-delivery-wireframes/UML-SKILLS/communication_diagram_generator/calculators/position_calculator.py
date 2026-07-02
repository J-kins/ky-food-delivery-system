import math
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# Participant type shapes and default sizes
# ---------------------------------------------------------------------------
PARTICIPANT_TYPE_META = {
    "boundary":  {"shape": "rectangle",         "width": 2.2, "height": 0.8, "color": "#1565C0", "text_color": "#FFFFFF"},
    "control":   {"shape": "rounded_rectangle",  "width": 2.0, "height": 0.8, "color": "#2E7D32", "text_color": "#FFFFFF"},
    "entity":    {"shape": "rectangle",          "width": 2.0, "height": 0.8, "color": "#1a237e", "text_color": "#FFFFFF"},
    "actor":     {"shape": "stick_figure",       "width": 1.0, "height": 1.4, "color": "#333333", "text_color": "#333333"},
    "database":  {"shape": "cylinder",           "width": 1.8, "height": 1.0, "color": "#6A1B9A", "text_color": "#FFFFFF"},
    "component": {"shape": "component",          "width": 2.4, "height": 1.0, "color": "#E65100", "text_color": "#FFFFFF"},
    "system":    {"shape": "rectangle",          "width": 2.6, "height": 0.9, "color": "#37474F", "text_color": "#FFFFFF"},
}

DEFAULT_PARTICIPANT_META = PARTICIPANT_TYPE_META["control"]


class PositionCalculator:
    """
    Computes (x, y) positions for participants either from explicit
    coordinates in the JSON spec or via automatic grid/force layout.

    Auto-layout strategy
    ────────────────────
    Participants are distributed on a grid. The algorithm attempts to
    fill columns first, then rows, keeping the diagram reasonably compact.
    """

    def __init__(self, page_width: float, page_height: float, layout_cfg: Dict):
        self.page_width   = page_width
        self.page_height  = page_height
        self.margin       = layout_cfg.get("margin", 0.5)
        self.h_spacing    = layout_cfg.get("participant_spacing", 3.5)
        self.v_spacing    = layout_cfg.get("vertical_spacing", 3.0)
        self.title_h      = 1.5   # Space reserved at top for the title block
        self.auto_layout  = layout_cfg.get("auto_layout", False)

    def calculate(self, participants: List[Dict]) -> Dict[str, Dict]:
        """
        Return a mapping of participant_id → {"x": float, "y": float, "w": float, "h": float}.
        Honours explicit x/y coords if present, otherwise auto-distributes.
        """
        positions: Dict[str, Dict] = {}

        # Separate explicit vs auto participants
        explicit = [p for p in participants if "x" in p and "y" in p]
        auto_pts = [p for p in participants if "x" not in p or "y" not in p]

        # Place explicitly positioned participants
        for p in explicit:
            meta = PARTICIPANT_TYPE_META.get(p.get("type", "control"), DEFAULT_PARTICIPANT_META)
            positions[p["id"]] = {
                "x": p["x"], "y": p["y"],
                "w": p.get("width",  meta["width"]),
                "h": p.get("height", meta["height"]),
                "type": p.get("type", "control"),
            }

        # Auto-distribute remaining participants in a grid
        if auto_pts:
            cols      = max(1, math.ceil(math.sqrt(len(auto_pts))))
            usable_w  = self.page_width  - 2 * self.margin
            usable_h  = self.page_height - 2 * self.margin - self.title_h
            col_w     = min(self.h_spacing, usable_w / cols)
            row_h     = self.v_spacing

            for idx, p in enumerate(auto_pts):
                col = idx % cols
                row = idx // cols
                meta = PARTICIPANT_TYPE_META.get(p.get("type", "control"), DEFAULT_PARTICIPANT_META)
                x = self.margin + col * col_w + col_w / 2.0
                y = self.margin + self.title_h + row * row_h + meta["height"] / 2.0
                positions[p["id"]] = {
                    "x": x, "y": y,
                    "w": p.get("width",  meta["width"]),
                    "h": p.get("height", meta["height"]),
                    "type": p.get("type", "control"),
                }

        return positions

    def midpoint(self, pos_a: Dict, pos_b: Dict) -> Tuple[float, float]:
        """Return the midpoint between two participant centres (for label placement)."""
        return (
            (pos_a["x"] + pos_b["x"]) / 2.0,
            (pos_a["y"] + pos_b["y"]) / 2.0,
        )
