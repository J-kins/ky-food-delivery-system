"""
Conceptual Data Model Converter

Converts conceptual data model SVG to Visio template format.
High-level business concepts without implementation details.
"""

from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder
import logging

logger = logging.getLogger(__name__)


class ConceptualDataModelConverter(BaseDiagramConverter):
    """Converter for Conceptual Data Models"""

    def __init__(self, svg_path, json_data):
        super().__init__(svg_path, json_data)
        self.diagram_type = "conceptual"

    def convert_to_visio(self, output_path):
        """Convert conceptual model to Visio template"""
        logger.info(f"Converting Conceptual Data Model to Visio: {output_path}")
        
        builder = VisioBuilder()
        data = self.data

        # Create page
        page = builder.create_page(
            name=f"{data.get('projectName', 'Conceptual Model')}",
            width=1920,
            height=1000
        )

        # Add title
        builder.add_text_shape(
            page,
            x=960, y=50,
            width=800, height=40,
            text="Conceptual Data Model",
            font_size=16,
            font_bold=True
        )

        # Render concepts as rounded rectangles
        concepts = data.get("concepts", [])
        concept_shapes = {}

        for concept in concepts:
            position = concept.get("position", {})
            x = position.get("x", 0)
            y = position.get("y", 0)
            concept_id = concept.get("id")
            
            shape = builder.add_rounded_rectangle(
                page,
                x=x, y=y,
                width=140, height=80,
                text=concept.get("name", ""),
                stroke_width=2,
                stroke_color="#262C7C",
                fill_color="#E8F0FF"
            )
            concept_shapes[concept_id] = shape

        # Add relationships with labels
        relationships = data.get("relationships", [])
        for rel in relationships:
            from_id = rel.get("from")
            to_id = rel.get("to")
            
            if from_id in concept_shapes and to_id in concept_shapes:
                builder.add_connector(
                    page,
                    from_shape=concept_shapes[from_id],
                    to_shape=concept_shapes[to_id],
                    label=rel.get("label", ""),
                    stroke_width=1.5,
                    stroke_color="#262C7C"
                )

        builder.save_as_template(output_path)
        logger.info(f"Conceptual model template saved: {output_path}")
        return output_path
