"""DevOps Architecture Converter.

Converts DevOps architecture SVG templates to Visio diagrams.
"""

from typing import Dict, Any
from pathlib import Path

from ..base import BaseDiagramConverter


class DevOpsArchitectureConverter(BaseDiagramConverter):
    """Converter for DevOps Architecture diagrams."""

    diagram_type = "devops-architecture"
    display_name = "DevOps Architecture"
    template_pattern = "*devops*architecture*.svg"

    def render_diagram(
        self, 
        data: Dict[str, Any], 
        output_path: Path,
        **kwargs
    ) -> Path:
        """Render DevOps Architecture diagram to Visio format.
        
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
        output.append(f"DIAGRAM: {metadata.get('title', 'DevOps Architecture')}")
        output.append(f"Project: {metadata.get('projectName', '')}")
        output.append(f"Description: {metadata.get('description', '')}")
        output.append(f"Version: {metadata.get('version', '1.0')}")
        output.append("")
        output.append("DESIGN TOKENS:")
        output.append(f"  Canvas: {styling.get('canvasColor', '#FFFFFF')}")
        output.append(f"  Fill: {styling.get('fillColor', '#E5E5E5')}")
        output.append(f"  Stroke: {styling.get('strokeColor', '#1A1A1A')}")
        output.append(f"  Corner Radius: {styling.get('cornerRadius', 8)}px")
        output.append("")
        output.append("DEVOPS LAYERS:")
        
        layers = diagram_data.get("layers", [])
        for layer in layers:
            output.append(f"  [{layer.get('id')}] {layer.get('name')}")
            output.append(f"       Position: ({layer.get('x')}, {layer.get('y')})")
            output.append(f"       Size: {layer.get('width')}x{layer.get('height')}")

        with open(output_path, "w") as f:
            f.write("\n".join(output))

        return output_path

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate DevOps Architecture data structure."""
        required_keys = ["metadata", "config", "data"]
        if not all(key in data for key in required_keys):
            return False

        diagram_data = data.get("data", {})
        if "layers" not in diagram_data:
            return False

        return True
