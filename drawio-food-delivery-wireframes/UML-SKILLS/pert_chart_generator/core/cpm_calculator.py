import networkx as nx
from typing import Dict, Any, List, Tuple

class CPMCalculator:
    """Calculates Critical Path Method metrics: ES, EF, LS, LF, and Slack."""
    
    def __init__(self, tasks: List[Dict[str, Any]]):
        self.tasks = tasks
        self.task_map = {t["id"]: t for t in tasks}
        self.G = nx.DiGraph()
        
        # Build the graph
        for t in tasks:
            self.G.add_node(t["id"], duration=t.get("duration", 0))
            
        for t in tasks:
            for dep in t.get("dependencies", []):
                self.G.add_edge(dep, t["id"])
                
        # To handle multiple start/end nodes seamlessly, add virtual start/end
        self.G.add_node("__START__", duration=0)
        self.G.add_node("__END__", duration=0)
        
        start_nodes = [n for n, d in self.G.in_degree() if d == 0 and n not in ["__START__", "__END__"]]
        for n in start_nodes:
            self.G.add_edge("__START__", n)
            
        end_nodes = [n for n, d in self.G.out_degree() if d == 0 and n not in ["__START__", "__END__"]]
        for n in end_nodes:
            self.G.add_edge(n, "__END__")

    def calculate(self) -> Dict[str, Dict[str, float]]:
        # 1. Forward Pass (Calculate Early Start and Early Finish)
        es = {"__START__": 0.0}
        ef = {"__START__": 0.0}
        
        for node in nx.topological_sort(self.G):
            if node == "__START__": continue
            
            # ES is the max EF of all predecessors
            predecessors = list(self.G.predecessors(node))
            max_ef = max([ef[p] for p in predecessors]) if predecessors else 0.0
            
            es[node] = max_ef
            dur = self.G.nodes[node]["duration"]
            ef[node] = max_ef + dur
            
        # 2. Backward Pass (Calculate Late Start and Late Finish)
        project_duration = ef["__END__"]
        lf = {"__END__": project_duration}
        ls = {"__END__": project_duration}
        
        for node in reversed(list(nx.topological_sort(self.G))):
            if node == "__END__": continue
            
            # LF is the min LS of all successors
            successors = list(self.G.successors(node))
            min_ls = min([ls[s] for s in successors]) if successors else project_duration
            
            lf[node] = min_ls
            dur = self.G.nodes[node]["duration"]
            ls[node] = min_ls - dur
            
        # 3. Calculate Slack and Critical Path
        results = {}
        for node in self.G.nodes():
            if node in ["__START__", "__END__"]: continue
            
            slack = lf[node] - ef[node]
            is_critical = abs(slack) < 0.0001
            
            results[node] = {
                "ES": es[node],
                "EF": ef[node],
                "LS": ls[node],
                "LF": lf[node],
                "Slack": slack,
                "is_critical": is_critical
            }
            
        return results
