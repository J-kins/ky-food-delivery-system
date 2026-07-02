from typing import List, Dict

class AllocationCalculator:
    """Computes summary statistics for the resource allocation matrix."""
    
    def __init__(self, resources: List[Dict], allocations: List[Dict]):
        self.resources = resources
        self.allocations = allocations
        self.resource_map = {r['id']: r for r in resources}
    
    def total_allocation_pct(self) -> float:
        """Sum of all resource allocations."""
        return sum(r.get('allocation', 0) for r in self.resources)
    
    def average_utilization(self) -> float:
        """Average resource utilization across all resources."""
        total = self.total_allocation_pct()
        return round(total / max(1, len(self.resources)), 1)
    
    def overloaded_resources(self) -> List[Dict]:
        """Return list of resources with > 100% allocation."""
        return [r for r in self.resources if r.get('allocation', 0) > 100]
    
    def underutilized_resources(self) -> List[Dict]:
        """Return list of resources with < 40% allocation."""
        return [r for r in self.resources if r.get('allocation', 0) < 40]
    
    def peak_phase(self, phase_totals: Dict) -> str:
        """Identify the phase(s) with the highest resource count."""
        if not phase_totals:
            return "N/A"
        max_count = max(v['count'] for v in phase_totals.values())
        peaks = [pid for pid, v in phase_totals.items() if v['count'] == max_count]
        return ", ".join(peaks)
    
    def resource_gap_summary(self) -> str:
        """Identify whether the project needs additional headcount."""
        overloaded = self.overloaded_resources()
        if overloaded:
            names = [r['name'] for r in overloaded]
            return f"Consider additional resource to relieve: {', '.join(names)}"
        return "Allocation levels are within capacity."
