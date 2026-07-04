"""
Map Design Converter

Converts Map Design SVG templates to Visio diagrams showing:
- Base map layers
- Thematic data layers
- Map annotations and symbolization
- Legend and cartographic elements
"""

from pathlib import Path
from typing import Dict, Any
from base import BaseDiagramConverter, JSONDataParser


class MapDesignConverter(BaseDiagramConverter):
    """Converts Map Design data to Visio format."""

    def render_diagram(self) -> None:
        """Render Map Design diagram with layered map components."""
        self.logger.info("Rendering Map Design diagram")

        # Parse SVG template data
        template = JSONDataParser.parse_svg_template(self.svg_path)
        metadata = template.metadata
        config = template.config
        data = template.data

        # Create document
        doc = self.create_vsdx_document(
            title=metadata.get("title", "Map Design"),
            creator=metadata.get("projectName", ""),
        )

        # Get styling config
        styling = config.get("styling", {})
        fill_color = styling.get("fillColor", "#E5E5E5")
        stroke_color = styling.get("strokeColor", "#1A1A1A")

        # Render map layers
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

        # Save document
        self.save_vsdx(doc)
        self.logger.info(f"Map Design diagram saved: {self.output_path}")
