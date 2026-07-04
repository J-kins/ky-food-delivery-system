"""Data Pipeline Architecture Converter"""
from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder
import logging

logger = logging.getLogger(__name__)

class DataPipelineConverter(BaseDiagramConverter):
    def __init__(self, svg_path, json_data):
        super().__init__(svg_path, json_data)
        self.diagram_type = "pipeline"

    def convert_to_visio(self, output_path):
        logger.info(f"Converting Data Pipeline to Visio: {output_path}")
        builder = VisioBuilder()
        data = self.data
        page = builder.create_page(name="Data Pipeline Architecture", width=1920, height=1000)
        builder.add_text_shape(page, x=960, y=50, width=800, height=40, text="Data Pipeline Architecture (ETL)", font_size=16, font_bold=True)
        
        layers = data.get("layers", [])
        component_shapes = {}
        
        for layer in layers:
            components = layer.get("components", [])
            for comp in components:
                position = comp.get("position", {})
                comp_id = comp.get("id")
                x = position.get("x", 0)
                y = position.get("y", 0)
                
                # Color by component type
                colors = {"source": "#FF6B6B", "ingestion": "#4ECDC4", "processing": "#45B7D1", "storage": "#96CEB4", "analytics": "#FFEAA7"}
                color = colors.get(comp.get("type", "source"), "#E5E5E5")
                
                shape = builder.add_rectangle_shape(page, x=x, y=y, width=120, height=60, text=comp.get("name", ""), fill_color=color, stroke_width=1.5)
                tech = comp.get("technology", "")
                builder.add_text_shape(page, x=x+5, y=y+45, width=110, height=15, text=tech, font_size=8)
                component_shapes[comp_id] = shape
        
        flows = data.get("flows", [])
        for flow in flows:
            from_id, to_id = flow.get("from"), flow.get("to")
            if from_id in component_shapes and to_id in component_shapes:
                builder.add_connector(page, from_shape=component_shapes[from_id], to_shape=component_shapes[to_id], stroke_width=2)
        
        builder.save_as_template(output_path)
        logger.info(f"Pipeline template saved: {output_path}")
        return output_path
