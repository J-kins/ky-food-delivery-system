from typing import List, Dict

QUADRANT_MAP = {
    ("High", "High"): "key_players",
    ("High", "Low"):  "keep_satisfied",
    ("Low",  "High"): "keep_informed",
    ("Low",  "Low"):  "monitor",
    ("High", "Medium"): "key_players",
    ("Medium", "High"): "keep_informed",
    ("Medium", "Medium"): "keep_informed",
    ("Medium", "Low"):  "monitor",
    ("Low",  "Medium"): "monitor",
}

QUADRANT_META = {
    "key_players":    {"label": "Key Players",    "color": "#E53935", "text_color": "#FFFFFF", "strategy": "Manage Closely"},
    "keep_satisfied": {"label": "Keep Satisfied", "color": "#FF9800", "text_color": "#FFFFFF", "strategy": "Keep Satisfied"},
    "keep_informed":  {"label": "Keep Informed",  "color": "#FFC107", "text_color": "#333333", "strategy": "Keep Informed"},
    "monitor":        {"label": "Monitor",         "color": "#4CAF50", "text_color": "#FFFFFF", "strategy": "Monitor"},
}


class PowerInterestCalculator:
    """Places stakeholders into Power-Interest quadrants from register data."""

    def __init__(self, stakeholders: List[Dict]):
        self.stakeholders = stakeholders
        self.quadrants: Dict[str, List[Dict]] = {
            "key_players": [], "keep_satisfied": [],
            "keep_informed": [], "monitor": []
        }
        self._classify()

    def _classify(self) -> None:
        """Classify each stakeholder into a quadrant."""
        for sh in self.stakeholders:
            power    = sh.get("power",    "Low")
            interest = sh.get("interest", "Low")
            key = QUADRANT_MAP.get((power, interest), "monitor")
            self.quadrants[key].append(sh)

    def get_quadrant_meta(self, quadrant_id: str) -> Dict:
        """Return styling metadata for a quadrant."""
        return QUADRANT_META.get(quadrant_id, QUADRANT_META["monitor"])

    def summary(self) -> Dict:
        """Return counts per quadrant."""
        return {k: len(v) for k, v in self.quadrants.items()}
