"""
GIS Architecture Converter

Converts GIS Architecture SVG templates to Visio diagrams showing:
- GIS Server components
- Spatial Database infrastructure
- Client application interfaces
- Data flow between components
"""

from pathlib import Path
from typing import Dict, Any
from base import BaseDiagramConverter, JSONDataParser


class GISArchitectureConverter(BaseDiagramConverter):
    """Converts GIS Architecture data to Visio format."""

    def render_diagram(self) -> None:
        """Render GIS Architecture diagram with components and connections."""
        self.logger.info("Rendering GIS Architecture diagram")

        # Parse SVG template data
        template = JSONDataParser.parse_svg_template(self.svg_path)
        metadata = template.metadata
        config = template.config
        data = template.data

        # Create document
        doc = self.create_vsdx_document(
            title=metadata.get("title", "GIS Architecture"),
            creator=metadata.get("projectName", ""),
        )

        # Get styling config
        styling = config.get("styling", {})
        fill_color = styling.get("fillColor", "#E5E5E5")
        stroke_color = styling.get("strokeColor", "#1A1A1A")

        # Render GIS components
        layers = data.get("layers", [])
        for layer in layers:
            self.add_shape(
                doc,
                shape_type="rect",
                x=layer.get("x", 0),
                y=layer.get("y", 0),
                width=layer.get("width", 200),
                height=layer.get("height", 120),
                text=layer.get("name", ""),
                fill_color=fill_color,
                line_color=stroke_color,
            )

        # Render connections
        connections = data.get("connections", [])
        for conn in connections:
            self.add_connector(doc, conn.get("from", ""), conn.get("to", ""))

        # Save document
        self.save_vsdx(doc)
        self.logger.info(f"GIS Architecture diagram saved: {self.output_path}")
