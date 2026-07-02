from typing import Dict

# Pre-computed lookup for 5x5 grid (probability x impact)
ZONE_LOOKUP = {
    (5, 5): "critical", (5, 4): "high",    (5, 3): "high",    (5, 2): "medium", (5, 1): "low",
    (4, 5): "critical", (4, 4): "high",    (4, 3): "medium",  (4, 2): "low",    (4, 1): "minimal",
    (3, 5): "high",     (3, 4): "medium",  (3, 3): "low",     (3, 2): "low",    (3, 1): "minimal",
    (2, 5): "medium",   (2, 4): "low",     (2, 3): "low",     (2, 2): "minimal",(2, 1): "minimal",
    (1, 5): "low",      (1, 4): "minimal", (1, 3): "minimal", (1, 2): "minimal",(1, 1): "minimal",
}

ZONE_COLORS = {
    "critical": {"fill": "#E53935", "text": "#FFFFFF"},
    "high":     {"fill": "#FF9800", "text": "#FFFFFF"},
    "medium":   {"fill": "#FFC107", "text": "#333333"},
    "low":      {"fill": "#4CAF50", "text": "#FFFFFF"},
    "minimal":  {"fill": "#E0E0E0", "text": "#333333"},
}


class ZoneCalculator:
    """Classifies risks and grid cells into color zones."""

    @staticmethod
    def get_zone(probability: int, impact: int) -> str:
        """Return zone ID for a given probability/impact pair."""
        key = (int(probability), int(impact))
        return ZONE_LOOKUP.get(key, "minimal")

    @staticmethod
    def get_zone_from_score(score: int) -> str:
        """Classify a numeric score into a zone."""
        if score >= 20:
            return "critical"
        if score >= 15:
            return "high"
        if score >= 10:
            return "medium"
        if score >= 5:
            return "low"
        return "minimal"

    @staticmethod
    def get_colors(zone_id: str) -> Dict:
        """Return fill and text color for a zone."""
        return ZONE_COLORS.get(zone_id, ZONE_COLORS["minimal"])
