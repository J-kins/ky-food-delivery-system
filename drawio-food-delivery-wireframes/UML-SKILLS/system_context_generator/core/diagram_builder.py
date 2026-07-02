from aspose.diagram import Diagram, Page, Shape, SaveFileFormat
from typing import List, Dict, Optional
import logging

class SystemContextBuilder:
    """Main class for building system context diagrams (Level 0)."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._setup_positions()
    
    def _setup_page(self) -> None:
        """Configure page size and orientation."""
        layout_cfg = self.config.get("layout", {})
        orientation = layout_cfg.get("orientation", "landscape")
        page_size = layout_cfg.get("page_size", "A3")
        
        # Aspose works in inches internally by default
        if page_size == "A3":
            if orientation == "landscape":
                self.page.page_sheet.page_props.page_width.value = 16.53
                self.page.page_sheet.page_props.page_height.value = 11.69
            else:
                self.page.page_sheet.page_props.page_width.value = 11.69
                self.page.page_sheet.page_props.page_height.value = 16.53
    
    def _setup_styles(self) -> None:
        """Set up global styling defaults."""
        style_cfg = self.config.get("styling", {})
        self.theme = style_cfg.get("theme", "enterprise_blue")
        self.font_family = style_cfg.get("font_family", "Arial")
        self.font_size = style_cfg.get("font_size", 10)
        self.corner_radius = style_cfg.get("corner_radius", 8)
    
    def _setup_positions(self) -> None:
        """Calculate exact coordinate mapping for all elements."""
        from renderers.layout_engine import LayoutEngine
        self.layout_engine = LayoutEngine(
            self.page.page_sheet.page_props.page_width.value, 
            self.page.page_sheet.page_props.page_height.value
        )
        self.positions = self.layout_engine.calculate_positions(self.config)
    
    def build(self) -> None:
        """Execute the drawing pipeline."""
        sys_cfg = self.config["system"]
        self.add_title_block(
            self.config["title"], 
            sys_cfg["description"], 
            self.config["version"], 
            self.config["date"]
        )
        self.add_system_boundary()
        self.add_system_box(sys_cfg)
        self.add_external_entities(self.config["external_entities"])
        self.add_data_flows(self.config["external_entities"])
        self.add_legend()

    def add_title_block(self, title: str, subtitle: str, version: str, date: str) -> None:
        # Implementation via Aspose geometry logic
        pass

    def add_system_boundary(self) -> None:
        # Drawing a dashed rectangle wrapping the system logic
        pass
    
    def add_system_box(self, system: Dict) -> None:
        # Drawing the solid center system box
        pass
    
    def add_external_entities(self, entities: List[Dict]) -> None:
        # Draw external entities using spatial map
        pass
    
    def add_data_flows(self, entities: List[Dict]) -> None:
        # Route connectors with Arrow types
        pass
    
    def add_legend(self) -> None:
        pass
    
    def save(self, output_path: str) -> None:
        self.diagram.save(output_path, SaveFileFormat.VSDX)
