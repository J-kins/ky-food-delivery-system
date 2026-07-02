from typing import List, Dict
from collections import deque
from core.errors import CycleDetectedError

class CPMCalculator:
    """Calculates CPM values accommodating advanced dependencies and lag."""
    
    def __init__(self, activities: List[Dict]):
        self.activities = activities
        self.activity_map = {a['id']: a for a in activities}
        self.dependencies = self._build_dependency_graph()
        
        self._topological_sort()
        self.forward_pass()
        self.backward_pass()
        self.identify_critical_path()
        self.calculate_free_float()
    
    def _build_dependency_graph(self) -> Dict:
        """Construct the DAG of predecessors/successors."""
        graph = {}
        for activity in self.activities:
            graph[activity['id']] = {'predecessors': [], 'successors': []}
        
        for activity in self.activities:
            for pred in activity.get('predecessors', []):
                # handle both legacy str and new obj
                if isinstance(pred, dict):
                    pred_id = pred['id']
                    rel_type = pred.get('type', 'FS')
                    lag = pred.get('lag', 0)
                    graph[activity['id']]['predecessors'].append(pred)
                else:
                    pred_id = pred
                    rel_type = 'FS'
                    lag = 0
                    graph[activity['id']]['predecessors'].append({'id': pred_id, 'type': 'FS', 'lag': 0})
                    
                graph[pred_id]['successors'].append({
                    'id': activity['id'],
                    'type': rel_type,
                    'lag': lag
                })
        return graph
        
    def _topological_sort(self) -> None:
        """Kahn's Algorithm to sort nodes."""
        in_degree = {a['id']: 0 for a in self.activities}
        for act_id, edges in self.dependencies.items():
            for succ in edges['successors']:
                in_degree[succ['id']] += 1
                
        queue = deque([k for k, v in in_degree.items() if v == 0])
        sorted_ids = []
        
        while queue:
            u = queue.popleft()
            sorted_ids.append(u)
            for succ in self.dependencies[u]['successors']:
                in_degree[succ['id']] -= 1
                if in_degree[succ['id']] == 0:
                    queue.append(succ['id'])
                    
        if len(sorted_ids) != len(self.activities):
            raise CycleDetectedError()
            
        self.sorted_activities = [self.activity_map[aid] for aid in sorted_ids]
    
    def forward_pass(self) -> None:
        """Compute ES and EF considering FS, SS, FF, SF relationships."""
        for act in self.sorted_activities:
            act['es'] = 0
            act['ef'] = act['duration']
            
            for pred_obj in self.dependencies[act['id']]['predecessors']:
                pred_id = pred_obj['id']
                rel_type = pred_obj['type']
                lag = pred_obj['lag']
                
                p_act = self.activity_map[pred_id]
                
                # Apply lag constraints
                if rel_type == 'FS':
                    act['es'] = max(act['es'], p_act.get('ef', 0) + lag)
                    act['ef'] = act['es'] + act['duration']
                elif rel_type == 'SS':
                    act['es'] = max(act['es'], p_act.get('es', 0) + lag)
                    act['ef'] = act['es'] + act['duration']
                elif rel_type == 'FF':
                    act['ef'] = max(act['ef'], p_act.get('ef', 0) + lag)
                    act['es'] = act['ef'] - act['duration']
                elif rel_type == 'SF':
                    act['ef'] = max(act['ef'], p_act.get('es', 0) + lag)
                    act['es'] = act['ef'] - act['duration']
    
    def backward_pass(self) -> None:
        """Compute LS and LF."""
        total_dur = max([a.get('ef', 0) for a in self.activities]) if self.activities else 0
        
        for act in reversed(self.sorted_activities):
            act['lf'] = total_dur
            act['ls'] = act['lf'] - act['duration']
            
            for succ_obj in self.dependencies[act['id']]['successors']:
                succ_id = succ_obj['id']
                rel_type = succ_obj['type']
                lag = succ_obj['lag']
                s_act = self.activity_map[succ_id]
                
                if rel_type == 'FS':
                    act['lf'] = min(act['lf'], s_act['ls'] - lag)
                    act['ls'] = act['lf'] - act['duration']
                elif rel_type == 'SS':
                    act['ls'] = min(act['ls'], s_act['ls'] - lag)
                    act['lf'] = act['ls'] + act['duration']
                elif rel_type == 'FF':
                    act['lf'] = min(act['lf'], s_act['lf'] - lag)
                    act['ls'] = act['lf'] - act['duration']
                elif rel_type == 'SF':
                    act['ls'] = min(act['ls'], s_act['lf'] - lag)
                    act['lf'] = act['ls'] + act['duration']
                    
            act['slack'] = act['ls'] - act.get('es', 0)
    
    def identify_critical_path(self) -> None:
        """Flag Total Float == 0."""
        for act in self.activities:
            act['is_critical'] = abs(act.get('slack', 1)) < 0.01

    def calculate_free_float(self) -> None:
        """Free Float = Min(ES of successors) - EF."""
        for act in self.activities:
            successors = self.dependencies[act['id']]['successors']
            if not successors:
                act['free_float'] = 0
            else:
                min_es = min([self.activity_map[s['id']]['es'] for s in successors])
                act['free_float'] = max(0, min_es - act['ef'])
