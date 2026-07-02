import logging
from typing import Dict, Any
from dateutil import parser

log = logging.getLogger(__name__)

class TimelineCalculator:
    """Maps dates to physical X-axis coordinates for Milestone charts."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.layout = config.get("layout", {})
        
        # Dimensions
        self.page_size = self.layout.get("page_size", "A2")
        self.margin = self.layout.get("margin", 0.5)
        
        if self.page_size == "A1":
            self.total_width, self.total_height = 84.1, 59.4
        elif self.page_size == "A2":
            self.total_width, self.total_height = 59.4, 42.0
        elif self.page_size == "A3":
            self.total_width, self.total_height = 42.0, 29.7
        else: # A4
            self.total_width, self.total_height = 29.7, 21.0
            
        self.chart_width = self.total_width - (2 * self.margin)
        self.chart_start_x = self.margin
        
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

    def calculate_band(self, start_str: str, end_str: str) -> Dict[str, float]:
        """Calculates start_x and width for a continuous phase band."""
        start_x = self.date_to_x(start_str)
        end_x = self.date_to_x(end_str)
        width = max(0.1, end_x - start_x)
        
        return {
            "x": start_x + (width / 2.0),
            "start_x": start_x,
            "width": width
        }
