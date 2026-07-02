import logging
import networkx as nx
from typing import Dict, Any
from core.cpm_calculator import CPMCalculator
from calculators.layout_calculator import LayoutCalculator
from renderers.aspose_renderer import AsposePertRenderer

log = logging.getLogger(__name__)

class PERTChartBuilder:
    """Orchestrates mathematical calculations and node drawing."""
    
    def __init__(self, spec: Dict[str, Any]):
        self.config = spec
        self.tasks = spec.get("tasks", [])
        self.renderer = AsposePertRenderer(spec)
        self.layout_config = spec.get("layout", {})
        
        self.node_width = self.layout_config.get("node_width", 2.0)
        self.node_height = self.layout_config.get("node_height", 1.2)
        self.show_three_point = spec.get("styling", {}).get("show_three_point", False)

    def build(self) -> None:
        log.info("Calculating Critical Path Method (CPM)...")
        cpm = CPMCalculator(self.tasks)
        results = cpm.calculate()
        
        # Build DAG for layout (we strip __START__ and __END__ for the visual layout unless requested, 
        # but the spec says "Automated insertion of Start and End nodes", so we include them)
        log.info("Calculating Network Layout...")
        layout = LayoutCalculator(self.config, cpm.G)
        positions = layout.calculate_positions()
        
        log.info("Drawing Nodes and Edges...")
        self.shape_map = {}
        
        # Draw Nodes
        for node in cpm.G.nodes():
            x, y = positions[node]
            
            if node in ["__START__", "__END__"]:
                text = "START" if node == "__START__" else "END"
                sid = self.renderer.add_pert_node(node, text, x, y, 1.0, 1.0, is_critical=False)
                self.shape_map[node] = sid
                continue
                
            task_data = cpm.task_map[node]
            cpm_data = results[node]
            
            is_crit = cpm_data["is_critical"]
            
            # Formatting PERT text
            # Usually: 
            # ES | Duration | EF
            #     Name
            # LS | Slack    | LF
            name = task_data["name"]
            dur = task_data["duration"]
            es, ef = cpm_data["ES"], cpm_data["EF"]
            ls, lf = cpm_data["LS"], cpm_data["LF"]
            slack = cpm_data["Slack"]
            
            if self.show_three_point:
                o = task_data.get("optimistic", "?")
                m = task_data.get("most_likely", "?")
                p = task_data.get("pessimistic", "?")
                text = f"ES:{es} | D:{dur} (O:{o},M:{m},P:{p}) | EF:{ef}\n{name}\nLS:{ls} | Sl:{slack} | LF:{lf}"
            else:
                text = f"ES:{es} | D:{dur} | EF:{ef}\n{name}\nLS:{ls} | Sl:{slack} | LF:{lf}"
                
            sid = self.renderer.add_pert_node(node, text, x, y, self.node_width, self.node_height, is_critical=is_crit)
            self.shape_map[node] = sid
            
        # Draw Edges
        for u, v in cpm.G.edges():
            u_id = self.shape_map[u]
            v_id = self.shape_map[v]
            
            # An edge is on the critical path if BOTH nodes are critical
            # (Start and End are omitted from critical coloring unless we calculate their slack,
            # but usually the path between critical nodes is critical)
            is_crit = False
            if u not in ["__START__", "__END__"] and v not in ["__START__", "__END__"]:
                is_crit = results[u]["is_critical"] and results[v]["is_critical"]
                
            self.renderer.add_directed_edge(u_id, v_id, is_critical=is_crit)

    def save(self, output_path: str):
        self.renderer.save(output_path)
