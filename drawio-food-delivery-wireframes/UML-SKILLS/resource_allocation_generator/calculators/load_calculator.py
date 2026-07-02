from typing import Dict

LOAD_THRESHOLDS = {
    "over":    (100.01, float('inf')),
    "full":    (80,     100),
    "partial": (40,     79.99),
    "under":   (0,      39.99),
}

LOAD_LABELS = {
    "over":    "▲ OVER",
    "full":    "● FULL",
    "partial": "◐ PARTIAL",
    "under":   "○ UNDER",
}

def classify_load(allocation_pct: float) -> Dict:
    """Classify a resource's total allocation into a load category."""
    for category, (low, high) in LOAD_THRESHOLDS.items():
        if low <= allocation_pct <= high:
            return {
                "category": category,
                "label": LOAD_LABELS[category],
                "percentage": allocation_pct
            }
    return {"category": "under", "label": "○ UNDER", "percentage": allocation_pct}
