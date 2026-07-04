"""Data Lakehouse Architecture Converter"""
from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder
import logging

logger = logging.getLogger(__name__)

class DataLakehouseConverter(BaseDiagramConverter):
    def __init__(self, svg_path, json_data):
        super().__init__(svg_path, json_data)
        self.diagram_type = "lakehouse"

    def convert_to_visio(self, output_path):
        logger.info(f"Converting Data Lakehouse to Visio: {output_path}")
        builder = VisioBuilder()
        data = self.data
        page = builder.create_page(name="Data Lakehouse Architecture", width=1920, height=1000)
        builder.add_text_shape(page, x=960, y=50, width=800, height=40, text="Data Lakehouse Architecture (Delta Lake)", font_size=16, font_bold=True)
        
        zones = data.get("zones", [])
        zone_colors = {"Raw Zone (Bronze)": "#D4A574", "Processed Zone (Silver)": "#C0C0C0", "Analytics Zone (Gold)": "#FFD700", "Serving Layer": "#87CEEB"}
        
        for zone in zones:
            location = zone.get("location", {})
            x = location.get("x", 0)
            y = location.get("y", 0)
            zone_name = zone.get("zone", "")
            color = zone_colors.get(zone_name, "#E5E5E5")
            
            # Zone container
            builder.add_rectangle_shape(page, x=x-50, y=y-50, width=450, height=200, text=zone_name, fill_color=color, stroke_width=2)
            
            # Components in zone
            components = zone.get("components", [])
            for i, comp in enumerate(components):
                comp_x = x + (i * 140)
                builder.add_rectangle_shape(page, x=comp_x, y=y, width=130, height=60, text=comp.get("name", ""), fill_color="white", stroke_width=1.5)
        
        tech = data.get("technology", {})
        tech_text = f"Storage: {tech.get('storage', '')}\nCompute: {tech.get('compute', '')}\nOrchestration: {tech.get('orchestration', '')}"
        builder.add_text_shape(page, x=100, y=850, width=800, height=80, text=tech_text, font_size=10)
        
        builder.save_as_template(output_path)
        logger.info(f"Lakehouse template saved: {output_path}")
        return output_path
