from typing import List, Dict

# Mitchell, Agle & Wood (1997) Salience Model
# Category determined by combination of Power, Legitimacy, Urgency
SALIENCE_CATEGORY_MAP = {
    # All three attributes High
    ("High", "High", "High"): "Definitive",
    # Two attributes High
    ("High", "High", "Low"):  "Dominant",
    ("High", "High", "Medium"): "Dominant",
    ("High", "Low",  "High"): "Dangerous",
    ("Low",  "High", "High"): "Dependent",
    ("Medium", "High", "High"): "Dependent",
    # One attribute High
    ("High", "Low",  "Low"):  "Dormant",
    ("Low",  "High", "Low"):  "Discretionary",
    ("Low",  "Low",  "High"): "Demanding",
    # Medium cases
    ("High", "Medium", "High"): "Dangerous",
    ("Medium", "Medium", "High"): "Dependent",
    ("High", "Low", "Medium"): "Dormant",
}

CATEGORY_META = {
    "Definitive":    {"color": "#2E7D32", "text_color": "#FFFFFF", "symbol": "★", "priority": "Critical"},
    "Dominant":      {"color": "#1a237e", "text_color": "#FFFFFF", "symbol": "◆", "priority": "High"},
    "Dangerous":     {"color": "#E53935", "text_color": "#FFFFFF", "symbol": "⚠",  "priority": "High"},
    "Dependent":     {"color": "#FF8A65", "text_color": "#333333", "symbol": "●", "priority": "Medium"},
    "Discretionary": {"color": "#64B5F6", "text_color": "#333333", "symbol": "○", "priority": "Medium"},
    "Demanding":     {"color": "#FFB74D", "text_color": "#333333", "symbol": "△", "priority": "Low"},
    "Dormant":       {"color": "#9E9E9E", "text_color": "#333333", "symbol": "◇", "priority": "Low"},
}


class SalienceCalculator:
    """
    Classifies stakeholders using the Mitchell, Agle & Wood (1997)
    Salience Model based on Power, Legitimacy, and Urgency attributes.
    """

    def __init__(self, stakeholders: List[Dict]):
        self.stakeholders = stakeholders
        self._classify()

    def _classify(self) -> None:
        """Assign salience category to each stakeholder."""
        for sh in self.stakeholders:
            power       = sh.get("power",       "Low")
            legitimacy  = sh.get("legitimacy",  "Low")
            urgency     = sh.get("urgency",     "Low")
            category = SALIENCE_CATEGORY_MAP.get(
                (power, legitimacy, urgency), "Dormant"
            )
            sh["salience_category"] = category
            sh["salience_meta"] = CATEGORY_META[category]

    def get_by_category(self, category: str) -> List[Dict]:
        """Return all stakeholders in a given salience category."""
        return [s for s in self.stakeholders
                if s.get("salience_category") == category]

    def category_counts(self) -> Dict[str, int]:
        """Return count per salience category."""
        counts = {cat: 0 for cat in CATEGORY_META}
        for sh in self.stakeholders:
            cat = sh.get("salience_category", "Dormant")
            counts[cat] = counts.get(cat, 0) + 1
        return counts
