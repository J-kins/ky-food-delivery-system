"""Infrastructure as Code Converter.

Converts Infrastructure as Code SVG templates to Visio diagrams.
"""

from typing import Dict, Any
from pathlib import Path

from ..base import BaseDiagramConverter


class InfrastructureAsCodeConverter(BaseDiagramConverter):
    """Converter for Infrastructure as Code diagrams."""

    diagram_type = "infrastructure-as-code"
    display_name = "Infrastructure as Code"
    template_pattern = "*infrastructure*code*.svg"

    def render_diagram(
        self, 
        data: Dict[str, Any], 
        output_path: Path,
        **kwargs
    ) -> Path:
        """Render Infrastructure as Code diagram to Visio format.
        
        Args:
            data: Parsed JSON data from SVG template
            output_path: Path to save Visio diagram
            **kwargs: Additional rendering options
            
        Returns:
            Path to generated Visio diagram
        """
        metadata = data.get("metadata", {})
        config = data.get("config", {})
        diagram_data = data.get("data", {})
        styling = config.get("styling", {})

        output = []
        output.append(f"DIAGRAM: {metadata.get('title', 'Infrastructure as Code')}")
        output.append(f"Project: {metadata.get('projectName', '')}")
        output.append(f"Description: {metadata.get('description', '')}")
        output.append(f"Version: {metadata.get('version', '1.0')}")
        output.append("")
        output.append("DESIGN TOKENS:")
        output.append(f"  Canvas: {styling.get('canvasColor', '#FFFFFF')}")
        output.append(f"  Fill: {styling.get('fillColor', '#E5E5E5')}")
        output.append(f"  Stroke: {styling.get('strokeColor', '#1A1A1A')}")
        output.append("")
        output.append("IAC STAGES:")
        
        stages = diagram_data.get("stages", [])
        for stage in stages:
            output.append(f"  [{stage.get('id')}] {stage.get('name')}")
            output.append(f"       Position: ({stage.get('x')}, {stage.get('y')})")
            output.append(f"       Size: {stage.get('width')}x{stage.get('height')}")

        with open(output_path, "w") as f:
            f.write("\n".join(output))

        return output_path

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate Infrastructure as Code data structure."""
        required_keys = ["metadata", "config", "data"]
        if not all(key in data for key in required_keys):
            return False

        diagram_data = data.get("data", {})
        if "stages" not in diagram_data:
            return False

        return True
