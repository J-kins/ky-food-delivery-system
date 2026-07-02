from typing import List, Dict

# Power × Interest → Engagement Strategy lookup
POWER_INTEREST_STRATEGY = {
    ("High", "High"): "Manage Closely",
    ("High", "Low"):  "Keep Satisfied",
    ("Low",  "High"): "Keep Informed",
    ("Low",  "Low"):  "Monitor",
    # Medium fallbacks
    ("High", "Medium"): "Manage Closely",
    ("Medium", "High"): "Keep Informed",
    ("Medium", "Medium"): "Keep Informed",
    ("Medium", "Low"):  "Monitor",
    ("Low",  "Medium"): "Monitor",
}

# Power × Interest → Matrix quadrant key
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


class StakeholderCalculator:
    """Core processing and enrichment of raw stakeholder records."""

    VALID_LEVELS = {"High", "Medium", "Low"}
    VALID_STRATEGIES = {"Manage Closely", "Keep Satisfied", "Keep Informed", "Monitor", "auto"}
    VALID_STATUSES = {"Active", "Inactive", "Blocked"}
    VALID_CATEGORIES = {"Internal", "External"}

    def __init__(self, stakeholders: List[Dict]):
        self.stakeholders = stakeholders
        self._enrich_strategies()

    def _enrich_strategies(self) -> None:
        """Auto-classify engagement_strategy when missing or set to 'auto'."""
        for sh in self.stakeholders:
            if sh.get("engagement_strategy") in (None, "auto", ""):
                power    = sh.get("power", "Low")
                interest = sh.get("interest", "Low")
                sh["engagement_strategy"] = POWER_INTEREST_STRATEGY.get(
                    (power, interest), "Monitor"
                )

    def summary(self) -> Dict:
        """Return aggregate counts for the register footer."""
        counts = {"total": 0, "internal": 0, "external": 0,
                  "manage_closely": 0, "keep_satisfied": 0,
                  "keep_informed": 0, "monitor": 0}
        for sh in self.stakeholders:
            counts["total"] += 1
            if sh.get("category") == "Internal":
                counts["internal"] += 1
            else:
                counts["external"] += 1
            strategy = sh.get("engagement_strategy", "")
            key = strategy.lower().replace(" ", "_")
            if key in counts:
                counts[key] += 1
        return counts

    def get_by_strategy(self, strategy: str) -> List[Dict]:
        """Filter stakeholders by engagement strategy."""
        return [s for s in self.stakeholders
                if s.get("engagement_strategy") == strategy]

    def get_by_category(self, category: str) -> List[Dict]:
        """Filter stakeholders by Internal / External category."""
        return [s for s in self.stakeholders
                if s.get("category") == category]
