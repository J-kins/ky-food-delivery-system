import logging
from typing import Dict, Any, List
from dateutil import parser
from datetime import timedelta

log = logging.getLogger(__name__)

class TimelineCalculator:
    """Maps dates to physical X-axis coordinates based on layout dimensions."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.layout = config.get("layout", {})
        
        # Dimensions
        self.page_size = self.layout.get("page_size", "A2")
        self.margin = self.layout.get("margin", 0.5)
        
        if self.page_size == "A2":
            self.total_width = 59.4
            self.total_height = 42.0
        elif self.page_size == "A3":
            self.total_width = 42.0
            self.total_height = 29.7
        else: # A4
            self.total_width = 29.7
            self.total_height = 21.0
            
        # Chart specific axes
        self.left_pane_width = 12.0 # Fixed width for the task hierarchy list
        self.chart_width = self.total_width - self.left_pane_width - (2 * self.margin)
        self.chart_start_x = self.margin + self.left_pane_width
        
        # Dates
        self.start_date = parser.parse(config["start_date"])
        self.end_date = parser.parse(config["end_date"])
        self.total_days = max(1, (self.end_date - self.start_date).days)
        self.pixels_per_day = self.chart_width / self.total_days

    def date_to_x(self, date_str: str) -> float:
        """Convert a date string to absolute X coordinate on the page."""
        dt = parser.parse(date_str)
        delta_days = (dt - self.start_date).days
        # Clamp between 0 and total_days
        delta_days = max(0, min(delta_days, self.total_days))
        return self.chart_start_x + (delta_days * self.pixels_per_day)

    def calculate_bar(self, start_str: str, end_str: str) -> Dict[str, float]:
        """Calculates X, and Width for a task bar."""
        start_x = self.date_to_x(start_str)
        end_x = self.date_to_x(end_str)
        width = max(0.1, end_x - start_x) # Minimum width for visibility
        
        return {
            "x": start_x + (width / 2.0), # Visio pins are often centered
            "start_x": start_x,
            "width": width
        }
        
    def calculate_phase_rollup(self, tasks: List[Dict]) -> Dict[str, float]:
        """Calculate the min start and max end of a list of tasks for the phase roll-up bar."""
        if not tasks:
            return self.calculate_bar(self.config["start_date"], self.config["start_date"])
            
        min_start = min(parser.parse(t["start"]) for t in tasks)
        max_end = max(parser.parse(t["end"]) for t in tasks)
        
        return self.calculate_bar(min_start.isoformat(), max_end.isoformat())
