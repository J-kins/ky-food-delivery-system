from dataclasses import dataclass, field
from typing import List, Dict
from calculators.zone_calculator import ZoneCalculator


@dataclass
class RiskAnalysis:
    total_risks: int
    zone_counts: Dict[str, int]
    top_risks: List[Dict]
    mitigation_coverage: float
    risks_needing_action: List[Dict]


class RiskCalculator:
    """Calculates risk scores, zone classifications, and summary statistics."""

    def __init__(self, risks: List[Dict], zones: List[Dict]):
        self.risks = risks
        self.zones = zones
        self._enrich_risks()

    def _enrich_risks(self) -> None:
        """Compute score and zone for any risk missing them.
        
        Note: Per RX-005/RX-006 — builder always auto-computes score and zone
        from probability × impact, overriding any declared values.
        """
        for risk in self.risks:
            p = risk.get('probability', 1)
            i = risk.get('impact', 1)

            # Always override declared score for correctness
            risk['score'] = p * i

            # Always override declared zone for correctness
            risk['zone'] = ZoneCalculator.get_zone(p, i)

    def analyze(self) -> RiskAnalysis:
        """Build complete analysis summary."""
        zone_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "minimal": 0}

        for risk in self.risks:
            zone = risk.get('zone', 'minimal')
            if zone in zone_counts:
                zone_counts[zone] += 1

        top_risks = sorted(self.risks, key=lambda r: r.get('score', 0), reverse=True)[:3]

        risks_with_mitigation = sum(1 for r in self.risks if r.get('mitigation'))
        coverage = risks_with_mitigation / max(1, len(self.risks))

        needs_action = [r for r in self.risks if r.get('zone') in ('critical', 'high')]

        return RiskAnalysis(
            total_risks=len(self.risks),
            zone_counts=zone_counts,
            top_risks=top_risks,
            mitigation_coverage=round(coverage * 100, 1),
            risks_needing_action=needs_action
        )
