"""
renderers/layout_engine.py
───────────────────────────
Computes (x, y) positions for participants.

Strategy:
  • If ALL participants have explicit x/y in the JSON → use them as-is.
  • Mixed / none → auto-grid:  distribute in a smart grid that avoids
    overlap, respecting the page dimensions and participant sizes.

All coordinates are in centimetres (Aspose's internal unit).
"""
import math
import logging
from typing import Dict, List, Any, Tuple

log = logging.getLogger(__name__)

# Default participant box sizes (cm) per type
DEFAULT_SIZES: Dict[str, Tuple[float, float]] = {
    "actor":    (2.5, 1.2),
    "control":  (3.0, 1.4),
    "entity":   (3.0, 1.4),
    "boundary": (3.0, 1.4),
    "service":  (3.0, 1.4),
    "database": (2.8, 1.6),
    "system":   (3.2, 1.4),
}
DEFAULT_SIZE = (3.0, 1.4)


class LayoutEngine:
    """
    Resolves final positions for all participants.

    Args:
        page_width:  usable page width in cm
        page_height: usable page height in cm
        layout_cfg:  the `layout` section from the JSON spec
    """

    TITLE_H   = 1.8   # cm reserved at top for title block
    LEGEND_H  = 2.0   # cm reserved at bottom for legend

    def __init__(self, page_width: float, page_height: float, layout_cfg: Dict):
        self.page_width   = page_width
        self.page_height  = page_height
        self.margin       = layout_cfg.get("margin", 0.5)
        self.h_spacing    = layout_cfg.get("participant_spacing", 3.0)   # gap between cols
        self.v_spacing    = 2.5                                           # gap between rows
        self.auto_layout  = layout_cfg.get("auto_layout", False)

    def calculate(self, participants: List[Dict]) -> Dict[str, Dict[str, Any]]:
        """
        Return {participant_id: {x, y, w, h}} for every participant.
        Coordinates point to the **centre** of each box (Aspose PinX/PinY).
        """
        positions: Dict[str, Dict] = {}

        # Separate explicit vs auto participants
        explicit = [p for p in participants if "x" in p and "y" in p]
        auto_pts = [p for p in participants if "x" not in p or "y" not in p]

        # Place explicitly-positioned participants
        for p in explicit:
            w, h = self._size(p)
            positions[p["id"]] = {"x": float(p["x"]), "y": float(p["y"]), "w": w, "h": h}

        # Auto-layout remaining participants in a balanced grid
        if auto_pts:
            self._grid_layout(auto_pts, positions)

        return positions

    # ── Private ──────────────────────────────────────────────────────────────

    def _size(self, participant: Dict) -> Tuple[float, float]:
        """Return (width, height) in cm — honours JSON overrides."""
        defaults = DEFAULT_SIZES.get(participant.get("type", "control"), DEFAULT_SIZE)
        w = participant.get("width",  defaults[0])
        h = participant.get("height", defaults[1])
        return float(w), float(h)

    def _grid_layout(self, participants: List[Dict], positions: Dict) -> None:
        """
        Distribute participants in a rectangular grid.

        The grid is calculated to be as square as possible while fitting
        within the usable page area (excluding title and legend bands).
        """
        n    = len(participants)
        cols = max(1, math.ceil(math.sqrt(n)))
        rows = math.ceil(n / cols)

        usable_w = self.page_width  - 2 * self.margin
        usable_h = (self.page_height - 2 * self.margin
                    - self.TITLE_H - self.LEGEND_H)

        # Cell size = max participant size + spacing
        max_w = max((self._size(p)[0] for p in participants), default=3.0)
        max_h = max((self._size(p)[1] for p in participants), default=1.4)
        cell_w = max_w + self.h_spacing
        cell_h = max_h + self.v_spacing

        # If participants would overflow the page, squeeze spacing
        if cell_w * cols > usable_w:
            cell_w = usable_w / cols
        if cell_h * rows > usable_h:
            cell_h = usable_h / rows

        x_start = self.margin + cell_w / 2.0
        y_start  = self.margin + self.TITLE_H + max_h / 2.0

        for idx, p in enumerate(participants):
            col = idx % cols
            row = idx // cols
            w, h = self._size(p)
            positions[p["id"]] = {
                "x": x_start + col * cell_w,
                "y": y_start  + row * cell_h,
                "w": w,
                "h": h,
            }
            log.debug(f"  auto-layout {p['id']} → ({positions[p['id']]['x']:.2f}, {positions[p['id']]['y']:.2f})")
