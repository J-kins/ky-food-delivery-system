"""CI/CD Pipeline Architecture Converter.

Converts CI/CD pipeline SVG templates to Visio diagrams following design guidelines.
"""

from typing import Dict, Any, List
from pathlib import Path

from ..base import BaseDiagramConverter, JSONDataParser


class CICDPipelineConverter(BaseDiagramConverter):
    """Converter for CI/CD Pipeline diagrams."""

    diagram_type = "cicd-pipeline"
    display_name = "CI/CD Pipeline"
    template_pattern = "*cicd*pipeline*.svg"

    def render_diagram(
        self, 
        data: Dict[str, Any], 
        output_path: Path,
        **kwargs
    ) -> Path:
        """Render CI/CD Pipeline diagram to Visio format.
        
        Args:
            data: Parsed JSON data from SVG template
            output_path: Path to save Visio diagram
            **kwargs: Additional rendering options
            
        Returns:
            Path to generated Visio diagram
        """
        from pptx.util import Inches, Pt
        from pptx.enum.shapes import MSO_SHAPE
        from pptx.dml.color import RGBColor

        # Extract metadata and configuration
        metadata = data.get("metadata", {})
        config = data.get("config", {})
        diagram_data = data.get("data", {})
        styling = config.get("styling", {})

        # Get design tokens
        canvas_color = styling.get("canvasColor", "#FFFFFF")
        fill_color = styling.get("fillColor", "#E5E5E5")
        stroke_color = styling.get("strokeColor", "#1A1A1A")
        corner_radius = styling.get("cornerRadius", 8)

        # Create diagram (using text output as placeholder for Visio)
        output = []
        output.append(f"DIAGRAM: {metadata.get('title', 'CI/CD Pipeline')}")
        output.append(f"Project: {metadata.get('projectName', '')}")
        output.append(f"Description: {metadata.get('description', '')}")
        output.append(f"Version: {metadata.get('version', '1.0')}")
        output.append("")
        output.append("DESIGN TOKENS:")
        output.append(f"  Canvas: {canvas_color}")
        output.append(f"  Fill: {fill_color}")
        output.append(f"  Stroke: {stroke_color}")
        output.append(f"  Corner Radius: {corner_radius}px")
        output.append("")
        output.append("PIPELINE STAGES:")
        
        stages = diagram_data.get("stages", [])
        for stage in stages:
            output.append(f"  [{stage.get('id')}] {stage.get('name')}")
            if stage.get('description'):
                output.append(f"       {stage.get('description')}")

        output.append("")
        output.append("PIPELINE FLOW:")
        flow = diagram_data.get("flow", [])
        for connection in flow:
            output.append(f"  {connection.get('from')} -> {connection.get('to')} ({connection.get('type', 'pipeline')})")

        # Write diagram data to file
        with open(output_path, "w") as f:
            f.write("\n".join(output))

        return output_path

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate CI/CD Pipeline data structure.
        
        Args:
            data: Data to validate
            
        Returns:
            True if data is valid
        """
        required_keys = ["metadata", "config", "data"]
        if not all(key in data for key in required_keys):
            return False

        diagram_data = data.get("data", {})
        if "stages" not in diagram_data or "flow" not in diagram_data:
            return False

        return True
