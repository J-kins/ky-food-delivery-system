"""
Geoprocessing Workflow Converter

Converts Geoprocessing Workflow SVG templates to Visio diagrams showing:
- Input data sources
- Spatial processing operations
- Analysis transformations
- Output results and products
"""

from pathlib import Path
from typing import Dict, Any
from base import BaseDiagramConverter, JSONDataParser


class GeoprocessingWorkflowConverter(BaseDiagramConverter):
    """Converts Geoprocessing Workflow data to Visio format."""

    def render_diagram(self) -> None:
        """Render Geoprocessing Workflow diagram with processing pipeline."""
        self.logger.info("Rendering Geoprocessing Workflow diagram")

        # Parse SVG template data
        template = JSONDataParser.parse_svg_template(self.svg_path)
        metadata = template.metadata
        config = template.config
        data = template.data

        # Create document
        doc = self.create_vsdx_document(
            title=metadata.get("title", "Geoprocessing Workflow"),
            creator=metadata.get("projectName", ""),
        )

        # Get styling config
        styling = config.get("styling", {})
        fill_color = styling.get("fillColor", "#E5E5E5")
        stroke_color = styling.get("strokeColor", "#1A1A1A")

        # Render workflow stages
        stages = data.get("stages", [])
        for i, stage in enumerate(stages):
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

            # Add connectors between stages
            if i < len(stages) - 1:
                self.add_connector(doc, stage.get("id", ""), stages[i + 1].get("id", ""))

        # Save document
        self.save_vsdx(doc)
        self.logger.info(f"Geoprocessing Workflow diagram saved: {self.output_path}")
