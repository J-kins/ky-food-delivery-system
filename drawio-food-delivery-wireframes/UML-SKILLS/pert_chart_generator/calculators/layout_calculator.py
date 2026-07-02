import networkx as nx
from typing import Dict, Any

class LayoutCalculator:
    """Calculates X/Y physical positions for DAG nodes using networkx multipartite layout."""
    
    def __init__(self, config: Dict[str, Any], G: nx.DiGraph):
        self.config = config
        self.layout_config = config.get("layout", {})
        self.G = G
        
        self.margin = self.layout_config.get("margin", 0.5)
        self.h_spacing = self.layout_config.get("horizontal_spacing", 2.5)
        self.v_spacing = self.layout_config.get("vertical_spacing", 2.0)
        
    def calculate_positions(self) -> Dict[str, tuple]:
        """Returns Dict mapping Node ID to (X, Y) layout."""
        
        # Calculate longest path from root for grouping into layers (multipartite)
        layers = {}
        for node in nx.topological_sort(self.G):
            if self.G.in_degree(node) == 0:
                layers[node] = 0
            else:
                max_pred_layer = max(layers[p] for p in self.G.predecessors(node))
                layers[node] = max_pred_layer + 1
                
        for node, layer in layers.items():
            self.G.nodes[node]["subset"] = layer
            
        # Use multipartite_layout from NetworkX
        # NetworkX returns coordinates in roughly [-1, 1] range, we'll map them 
        # to absolute Visio dimensions manually based on spacing
        
        # Determine max depth and max width
        max_layer = max(layers.values()) if layers else 0
        layer_counts = {}
        for l in layers.values():
            layer_counts[l] = layer_counts.get(l, 0) + 1
            
        positions = {}
        
        for node, layer in layers.items():
            # X position is simple: layer * horizontal_spacing
            x = self.margin + (layer * self.h_spacing)
            
            # Y position: center the nodes in the layer
            count_in_layer = layer_counts[layer]
            
            # Find index of this node in the layer
            nodes_in_layer = [n for n, l in layers.items() if l == layer]
            idx = nodes_in_layer.index(node)
            
            # Center vertically
            total_height = (count_in_layer - 1) * self.v_spacing
            start_y = self.margin + (total_height / 2.0)
            
            y = start_y - (idx * self.v_spacing) + 10.0 # Shift up by 10 for visibility in default A2 space
            
            positions[node] = (x, y)
            
        return positions
