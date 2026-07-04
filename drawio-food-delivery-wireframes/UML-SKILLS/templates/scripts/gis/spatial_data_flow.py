"""
Spatial Data Flow Converter

Converts Spatial Data Flow SVG templates to Visio diagrams depicting:
- Data sources (GPS, satellite, aerial)
- Data collection processes
- Transformation and processing
- Storage and repository systems
"""

from pathlib import Path
from typing import Dict, Any
from base import BaseDiagramConverter, JSONDataParser


class SpatialDataFlowConverter(BaseDiagramConverter):
    """Converts Spatial Data Flow data to Visio format."""

    def render_diagram(self) -> None:
        """Render Spatial Data Flow diagram with multi-source data pipeline."""
        self.logger.info("Rendering Spatial Data Flow diagram")

        # Parse SVG template data
        template = JSONDataParser.parse_svg_template(self.svg_path)
        metadata = template.metadata
        config = template.config
        data = template.data

        # Create document
        doc = self.create_vsdx_document(
            title=metadata.get("title", "Spatial Data Flow"),
            creator=metadata.get("projectName", ""),
        )

        # Get styling config
        styling = config.get("styling", {})
        fill_color = styling.get("fillColor", "#E5E5E5")
        stroke_color = styling.get("strokeColor", "#1A1A1A")

        # Render data sources
        sources = data.get("sources", [])
        for source in sources:
            self.add_shape(
                doc,
                shape_type="rect",
                x=source.get("x", 0),
                y=source.get("y", 0),
                width=source.get("width", 200),
                height=source.get("height", 120),
                text=source.get("name", ""),
                fill_color=fill_color,
                line_color=stroke_color,
            )

        # Render processing stages
        processing = data.get("processing", [])
        for stage in processing:
            self.add_shape(
                doc,
                shape_type="rect",
                x=stage.get("x", 0),
                y=stage.get("y", 0),
                width=stage.get("width", 200),
                height=stage.get("height", 120),
                text=stage.get("name", ""),
                fill_color=fill_color,
                line_color=stroke_color,
            )

        # Render output
        output = data.get("output", [])
        for out in output:
            self.add_shape(
                doc,
                shape_type="rect",
                x=out.get("x", 0),
                y=out.get("y", 0),
                width=out.get("width", 200),
                height=out.get("height", 120),
                text=out.get("name", ""),
                fill_color=fill_color,
                line_color=stroke_color,
            )

        # Save document
        self.save_vsdx(doc)
        self.logger.info(f"Spatial Data Flow diagram saved: {self.output_path}")
