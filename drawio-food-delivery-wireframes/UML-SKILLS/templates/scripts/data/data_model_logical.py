"""Logical Data Model Converter"""
from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder
import logging

logger = logging.getLogger(__name__)

class LogicalDataModelConverter(BaseDiagramConverter):
    def __init__(self, svg_path, json_data):
        super().__init__(svg_path, json_data)
        self.diagram_type = "logical"

    def convert_to_visio(self, output_path):
        logger.info(f"Converting Logical Data Model to Visio: {output_path}")
        builder = VisioBuilder()
        data = self.data
        page = builder.create_page(name=f"{data.get('projectName')} - Logical", width=1920, height=1000)
        builder.add_text_shape(page, x=960, y=50, width=800, height=40, text="Logical Data Model", font_size=16, font_bold=True)
        
        tables = data.get("tables", [])
        table_shapes = {}
        
        for table in tables:
            position = table.get("position", {})
            table_id = table.get("id")
            x = position.get("x", 0)
            y = position.get("y", 0)
            
            # Create table container
            shape = builder.add_rectangle_shape(page, x=x, y=y, width=200, height=150, text=table.get("name", ""), stroke_width=1.5)
            table_shapes[table_id] = shape
            
            # Add columns
            columns = table.get("columns", [])
            col_text = "\n".join([f"{'PK ' if c.get('pk') else ''}{c.get('name')} ({c.get('type')})" for c in columns[:5]])
            builder.add_text_shape(page, x=x+5, y=y+30, width=190, height=110, text=col_text, font_size=9)
        
        relationships = data.get("relationships", [])
        for rel in relationships:
            from_id, to_id = rel.get("from"), rel.get("to")
            if from_id in table_shapes and to_id in table_shapes:
                builder.add_connector(page, from_shape=table_shapes[from_id], to_shape=table_shapes[to_id], label=rel.get("type", ""), stroke_width=1.5)
        
        builder.save_as_template(output_path)
        logger.info(f"Logical model template saved: {output_path}")
        return output_path
