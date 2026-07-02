from typing import List, Dict

class RACICalculator:
    """Aggregates RACI statistics for summary sections."""
    
    def __init__(self, tasks: List[Dict], roles: List[Dict]):
        self.tasks = tasks
        self.roles = roles
    
    def total_assignments(self) -> int:
        """Count all non-empty RACI cell assignments."""
        return sum(
            sum(1 for v in t.get('raci', {}).values() if v != '-')
            for t in self.tasks
        )
    
    def average_per_task(self) -> float:
        """Average number of assignments per task."""
        n = len(self.tasks)
        return round(self.total_assignments() / max(1, n), 1)
    
    def role_summary(self) -> Dict:
        """Per-role distribution counts."""
        summary = {r['id']: {'R': 0, 'A': 0, 'C': 0, 'I': 0, 'total': 0} for r in self.roles}
        for task in self.tasks:
            for role_id, code in task.get('raci', {}).items():
                if code in ('R', 'A', 'C', 'I') and role_id in summary:
                    summary[role_id][code] += 1
                    summary[role_id]['total'] += 1
        return summary
