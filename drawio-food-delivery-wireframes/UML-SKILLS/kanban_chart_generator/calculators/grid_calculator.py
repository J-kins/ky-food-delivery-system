import logging
from typing import Dict, Any, List

log = logging.getLogger(__name__)

class GridCalculator:
    """Calculates Kanban Grid Intersections and Card Geometry."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.layout = config.get("layout", {})
        
        # Dimensions
        self.page_size = self.layout.get("page_size", "A2")
        self.margin = self.layout.get("margin", 0.5)
        self.cell_padding = self.layout.get("cell_padding", 0.2)
        
        # Approximate dimensions
        if self.page_size == "A1":
            self.total_width, self.total_height = 84.1, 59.4
        elif self.page_size == "A2":
            self.total_width, self.total_height = 59.4, 42.0
        elif self.page_size == "A3":
            self.total_width, self.total_height = 42.0, 29.7
        else: # A4
            self.total_width, self.total_height = 29.7, 21.0
            
        self.swimlane_label_width = 4.0
        self.header_height = 2.5
        self.metrics_height = 2.5
        
        # Available drawing area (reserve metrics footer)
        self.grid_width = self.total_width - self.swimlane_label_width - (2 * self.margin)
        self.grid_height = (
            self.total_height - self.header_height - self.metrics_height - (2 * self.margin)
        )
        
        self.columns = sorted(config.get("columns", []), key=lambda x: x.get("order", 0))
        self.swimlanes = config.get("swimlanes", [])
        
        self.col_count = max(1, len(self.columns))
        self.swim_count = max(1, len(self.swimlanes))
        
        self.col_width = self.grid_width / self.col_count
        self.swim_height = self.grid_height / self.swim_count
        
        # Build mapping dictionaries
        self.col_map = {c["id"]: i for i, c in enumerate(self.columns)}
        self.swim_map = {s["id"]: i for i, s in enumerate(self.swimlanes)}
        
        self.card_width = self.config.get("styling", {}).get("card_width", 2.0)
        self.card_height = self.config.get("styling", {}).get("card_height", 1.0)
        
        # Keep track of card stacking per cell to avoid overlap
        self.cell_occupancy = {} # (col_idx, swim_idx) -> list of cards

    def get_column_x(self, col_id: str) -> float:
        idx = self.col_map.get(col_id, 0)
        return self.margin + self.swimlane_label_width + (idx * self.col_width)

    def get_swimlane_y(self, swim_id: str) -> float:
        # Drawing top-down
        idx = self.swim_map.get(swim_id, 0)
        return self.total_height - self.margin - self.header_height - (idx * self.swim_height)

    def calculate_card_pos(self, item: Dict) -> Dict[str, float]:
        col_idx = self.col_map.get(item["status"], 0)
        swim_idx = self.swim_map.get(item["swimlane_id"], 0)
        cell_key = (col_idx, swim_idx)
        
        # Calculate offset based on occupancy
        count = len(self.cell_occupancy.get(cell_key, []))
        
        # We can fit a few cards per row inside a cell
        cards_per_row = max(1, int((self.col_width - 2*self.cell_padding) / (self.card_width + 0.1)))
        
        row = count // cards_per_row
        col = count % cards_per_row
        
        base_x = self.get_column_x(item["status"])
        base_y = self.get_swimlane_y(item["swimlane_id"])
        
        x = base_x + self.cell_padding + (col * (self.card_width + 0.1)) + (self.card_width/2)
        y = base_y - self.cell_padding - (row * (self.card_height + 0.1)) - (self.card_height/2)
        
        if cell_key not in self.cell_occupancy:
            self.cell_occupancy[cell_key] = []
        self.cell_occupancy[cell_key].append(item["id"])
        
        return {"x": x, "y": y, "w": self.card_width, "h": self.card_height}
