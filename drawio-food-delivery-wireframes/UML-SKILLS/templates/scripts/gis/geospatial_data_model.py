"""
Geospatial Data Model Converter

Converts Geospatial Data Model SVG templates to Visio diagrams representing:
- Point geometries (delivery locations)
- Line geometries (route networks)
- Polygon geometries (service areas)
- Spatial relationships and attributes
"""

from pathlib import Path
from typing import Dict, Any
from base import BaseDiagramConverter, JSONDataParser


class GeospatialDataModelConverter(BaseDiagramConverter):
    """Converts Geospatial Data Model data to Visio format."""

    def render_diagram(self) -> None:
        """Render Geospatial Data Model diagram with geometry types."""
        self.logger.info("Rendering Geospatial Data Model diagram")

        # Parse SVG template data
        template = JSONDataParser.parse_svg_template(self.svg_path)
        metadata = template.metadata
        config = template.config
        data = template.data

        # Create document
        doc = self.create_vsdx_document(
            title=metadata.get("title", "Geospatial Data Model"),
            creator=metadata.get("projectName", ""),
        )

        # Get styling config
        styling = config.get("styling", {})
        fill_color = styling.get("fillColor", "#E5E5E5")
        stroke_color = styling.get("strokeColor", "#1A1A1A")

        # Render geometry type entities
        entities = data.get("entities", [])
        for entity in entities:
            self.add_shape(
                doc,
                shape_type="rect",
                x=entity.get("x", 0),
                y=entity.get("y", 0),
                width=entity.get("width", 200),
                height=entity.get("height", 120),
                text=entity.get("name", ""),
                fill_color=fill_color,
                line_color=stroke_color,
            )

        # Save document
        self.save_vsdx(doc)
        self.logger.info(f"Geospatial Data Model diagram saved: {self.output_path}")
