"""Physical Data Model Converter"""
from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder
import logging

logger = logging.getLogger(__name__)

class PhysicalDataModelConverter(BaseDiagramConverter):
    def __init__(self, svg_path, json_data):
        super().__init__(svg_path, json_data)
        self.diagram_type = "physical"

    def convert_to_visio(self, output_path):
        logger.info(f"Converting Physical Data Model to Visio: {output_path}")
        builder = VisioBuilder()
        data = self.data
        page = builder.create_page(name=f"{data.get('projectName')} - Physical ({data.get('schema')})", width=1920, height=1000)
        builder.add_text_shape(page, x=960, y=50, width=800, height=40, text=f"Physical Data Model - {data.get('schema', 'Database')}", font_size=16, font_bold=True)
        
        tables = data.get("tables", [])
        for table in tables:
            position = table.get("position", {})
            x = position.get("x", 0)
            y = position.get("y", 0)
            
            # Create table with schema info
            shape = builder.add_rectangle_shape(page, x=x, y=y, width=220, height=160, text=table.get("name", ""), stroke_width=1.5, fill_color="#F0F0F0")
            
            # Add metadata
            metadata = f"Engine: {table.get('engine', 'InnoDB')}\nCharset: {table.get('charset', 'utf8mb4')}"
            builder.add_text_shape(page, x=x+5, y=y+125, width=210, height=30, text=metadata, font_size=8)
            
            # Add indexed columns
            columns = table.get("columns", [])
            indexed = [c.get("name") for c in columns if c.get("indexed")]
            if indexed:
                indexes = f"Indexes: {', '.join(indexed[:3])}"
                builder.add_text_shape(page, x=x+5, y=y+155, width=210, height=20, text=indexes, font_size=8)
        
        builder.save_as_template(output_path)
        logger.info(f"Physical model template saved: {output_path}")
        return output_path
