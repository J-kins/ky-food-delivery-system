"""
Entity Relationship Diagram (ERD) Converter

Converts ERD SVG templates to Visio template format (.vstx).
Renders entity boxes with attributes and relationship connectors.
"""

from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder
import logging

logger = logging.getLogger(__name__)


class ERDDiagramConverter(BaseDiagramConverter):
    """Converter for Entity Relationship Diagrams"""

    def __init__(self, svg_path, json_data):
        super().__init__(svg_path, json_data)
        self.diagram_type = "erd"

    def convert_to_visio(self, output_path):
        """Convert ERD data to Visio template format"""
        logger.info(f"Converting ERD to Visio template: {output_path}")
        
        builder = VisioBuilder()
        data = self.data

        # Create page
        page = builder.create_page(
            name=f"{data.get('projectName', 'ERD')} - Entity Diagram",
            width=1920,
            height=1000
        )

        # Add title
        builder.add_text_shape(
            page,
            x=960, y=50,
            width=800, height=40,
            text=f"Entity Relationship Diagram - {data.get('projectName', '')}",
            font_size=16,
            font_bold=True
        )

        # Render entities
        entities = data.get("entities", [])
        entity_shapes = {}

        for entity in entities:
            entity_id = entity.get("id")
            position = entity.get("position", {})
            x = position.get("x", 0)
            y = position.get("y", 0)
            
            # Create entity box
            shape = builder.add_rectangle_shape(
                page,
                x=x, y=y,
                width=140, height=80,
                text=entity.get("name", ""),
                stroke_width=1.5,
                stroke_color="#1A1A1A",
                fill_color="#E5E5E5"
            )
            entity_shapes[entity_id] = shape

            # Add attributes
            attrs = entity.get("attributes", [])
            attr_text = "\n".join(attrs[:3])  # Show first 3 attributes
            if len(attrs) > 3:
                attr_text += "\n..."
            
            builder.add_text_shape(
                page,
                x=x+5, y=y+35,
                width=130, height=40,
                text=attr_text,
                font_size=9
            )

        # Render relationships
        relationships = data.get("relationships", [])
        for rel in relationships:
            from_id = rel.get("from")
            to_id = rel.get("to")
            
            if from_id in entity_shapes and to_id in entity_shapes:
                from_shape = entity_shapes[from_id]
                to_shape = entity_shapes[to_id]
                
                # Create connector with relationship label
                builder.add_connector(
                    page,
                    from_shape=from_shape,
                    to_shape=to_shape,
                    label=rel.get("name", ""),
                    stroke_width=1.5,
                    stroke_color="#1A1A1A"
                )

        # Save as template
        builder.save_as_template(output_path)
        logger.info(f"ERD template saved: {output_path}")
        return output_path
