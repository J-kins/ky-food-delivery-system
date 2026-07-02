from typing import List, Dict

class GapAnalyzer:
    """Identifies RACI completeness gaps and role utilization anomalies."""
    
    def __init__(self, tasks: List[Dict], roles: List[Dict]):
        self.tasks = tasks
        self.roles = roles
    
    def tasks_missing_r(self) -> List[str]:
        """Tasks with no Responsible assigned."""
        return [
            t['name'] for t in self.tasks
            if 'R' not in t.get('raci', {}).values()
        ]
    
    def tasks_missing_a(self) -> List[str]:
        """Tasks with no Accountable assigned."""
        return [
            t['name'] for t in self.tasks
            if 'A' not in t.get('raci', {}).values()
        ]
    
    def overloaded_roles(self, role_summary: Dict, threshold: int = 10) -> List[str]:
        """Roles with more than `threshold` assignments."""
        return [
            role_id for role_id, counts in role_summary.items()
            if counts['total'] > threshold
        ]
    
    def underutilized_roles(self, role_summary: Dict) -> List[str]:
        """Roles with zero R and zero A assignments."""
        return [
            role_id for role_id, counts in role_summary.items()
            if counts['R'] == 0 and counts['A'] == 0
        ]
    
    def generate_report(self, role_summary: Dict) -> Dict:
        """Generate a comprehensive gap analysis report."""
        missing_r = self.tasks_missing_r()
        missing_a = self.tasks_missing_a()
        overloaded = self.overloaded_roles(role_summary)
        underutilized = self.underutilized_roles(role_summary)
        
        return {
            "raci_complete": len(missing_a) == 0,
            "tasks_missing_r": missing_r,
            "tasks_missing_a": missing_a,
            "overloaded_roles": overloaded,
            "underutilized_roles": underutilized,
            "gaps_detected": len(missing_r) + len(missing_a) + len(underutilized)
        }
