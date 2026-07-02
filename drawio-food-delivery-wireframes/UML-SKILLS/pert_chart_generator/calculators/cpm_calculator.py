from typing import List, Dict, Optional
import logging

class CPMCalculator:
    """Calculates Critical Path Method values for PERT charts."""
    
    def __init__(self, tasks: List[Dict]):
        self.tasks = tasks
        self.task_map = {t['id']: t for t in tasks}
        self.dependencies = {t['id']: t.get('dependencies', []) for t in tasks}
        self.forward_pass()
        self.backward_pass()
        self.identify_critical_path()
    
    def forward_pass(self) -> None:
        """Calculate Earliest Start (ES) and Earliest Finish (EF)."""
        # Execute in topological order to ensure predecessors are calculated first
        for task in self.tasks:
            if not task.get('dependencies', []):
                task['es'] = 0
            else:
                task['es'] = max([
                    self.task_map[dep]['ef'] 
                    for dep in task['dependencies']
                ])
            task['ef'] = task['es'] + task['duration']
    
    def backward_pass(self) -> None:
        """Calculate Latest Start (LS) and Latest Finish (LF)."""
        all_ids = set(self.task_map.keys())
        successor_ids = set()
        for deps in self.dependencies.values():
            successor_ids.update(deps)
            
        end_tasks = list(all_ids - successor_ids)
        max_ef = max([self.task_map[t]['ef'] for t in end_tasks]) if end_tasks else 0
        
        # Initialize LF for end tasks
        for task in self.tasks:
            if task['id'] in end_tasks:
                task['lf'] = max_ef
            else:
                task['lf'] = float('inf')
        
        # Calculate in reverse topological order
        for task in reversed(self.tasks):
            if task['lf'] == float('inf'):
                successors = [
                    t for t in self.tasks 
                    if task['id'] in t.get('dependencies', [])
                ]
                if successors:
                    task['lf'] = min([t['ls'] for t in successors])
                else:
                    task['lf'] = task['ef']
                    
            task['ls'] = task['lf'] - task['duration']
            task['slack'] = task['ls'] - task['es']
    
    def identify_critical_path(self) -> List[str]:
        """Flag tasks where Slack == 0 as Critical."""
        critical_tasks = []
        for task in self.tasks:
            is_critical = abs(task.get('slack', 1)) < 0.01
            task['is_critical'] = is_critical
            if is_critical:
                critical_tasks.append(task['id'])
        return critical_tasks
    
    def get_total_duration(self) -> float:
        """Get total project duration."""
        return max([t.get('ef', 0) for t in self.tasks]) if self.tasks else 0
