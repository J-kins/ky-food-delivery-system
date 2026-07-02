from typing import Dict, List

class LayoutEngine:
    """Calculates absolute (x, y, w, h) physical coordinates for all diagram elements."""
    
    def __init__(self, page_width: float, page_height: float):
        self.page_width = page_width
        self.page_height = page_height
        self.margin = 0.5  # inches
    
    def calculate_positions(self, spec: Dict) -> Dict:
        """Calculate bounds for the core system box and surrounding entities."""
        positions = {}
        
        # Absolute center alignment for System Box
        layout_cfg = spec.get("layout", {})
        system_width = layout_cfg.get("system_box_width", 8.0)
        system_height = layout_cfg.get("system_box_height", 6.0)
        system_x = (self.page_width - system_width) / 2
        system_y = (self.page_height - system_height) / 2
        
        positions["system"] = {
            "x": system_x,
            "y": system_y,
            "width": system_width,
            "height": system_height
        }
        
        entities = spec.get("external_entities", [])
        for entity in entities:
            positions[entity["id"]] = self._calculate_entity_position(entity, positions["system"])
        
        return positions
    
    def _calculate_entity_position(self, entity: Dict, sys_pos: Dict) -> Dict:
        """Determine X/Y coordinates based on compass-point directives."""
        pos = entity.get("position", "right")
        spacing = entity.get("spacing", 1.5)
        width = entity.get("width", 3.5)
        height = entity.get("height", 2.5)
        
        # Matrix grid placement
        if pos == "top-left":
            x = sys_pos["x"] - width - spacing
            y = sys_pos["y"] - height - spacing
        elif pos == "top":
            x = sys_pos["x"] + (sys_pos["width"] - width) / 2
            y = sys_pos["y"] - height - spacing
        elif pos == "top-right":
            x = sys_pos["x"] + sys_pos["width"] + spacing
            y = sys_pos["y"] - height - spacing
        elif pos == "left":
            x = sys_pos["x"] - width - spacing
            y = sys_pos["y"] + (sys_pos["height"] - height) / 2
        elif pos == "right":
            x = sys_pos["x"] + sys_pos["width"] + spacing
            y = sys_pos["y"] + (sys_pos["height"] - height) / 2
        elif pos == "bottom-left":
            x = sys_pos["x"] - width - spacing
            y = sys_pos["y"] + sys_pos["height"] + spacing
        elif pos == "bottom":
            x = sys_pos["x"] + (sys_pos["width"] - width) / 2
            y = sys_pos["y"] + sys_pos["height"] + spacing
        elif pos == "bottom-right":
            x = sys_pos["x"] + sys_pos["width"] + spacing
            y = sys_pos["y"] + sys_pos["height"] + spacing
        else:
            x = sys_pos["x"] + sys_pos["width"] + spacing
            y = sys_pos["y"] + (sys_pos["height"] - height) / 2
            
        return {"x": x, "y": y, "width": width, "height": height}
