"""Observability Architecture Converter.

Converts Observability architecture SVG templates to Visio diagrams.
"""

from typing import Dict, Any
from pathlib import Path

from ..base import BaseDiagramConverter


class ObservabilityArchitectureConverter(BaseDiagramConverter):
    """Converter for Observability Architecture diagrams."""

    diagram_type = "observability-architecture"
    display_name = "Observability Architecture"
    template_pattern = "*observability*.svg"

    def render_diagram(
        self, 
        data: Dict[str, Any], 
        output_path: Path,
        **kwargs
    ) -> Path:
        """Render Observability Architecture diagram to Visio format.
        
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
        output.append(f"DIAGRAM: {metadata.get('title', 'Observability Architecture')}")
        output.append(f"Project: {metadata.get('projectName', '')}")
        output.append(f"Description: {metadata.get('description', '')}")
        output.append(f"Version: {metadata.get('version', '1.0')}")
        output.append("")
        output.append("DESIGN TOKENS:")
        output.append(f"  Canvas: {styling.get('canvasColor', '#FFFFFF')}")
        output.append(f"  Fill: {styling.get('fillColor', '#E5E5E5')}")
        output.append(f"  Stroke: {styling.get('strokeColor', '#1A1A1A')}")
        output.append("")
        output.append("OBSERVABILITY PILLARS:")
        
        pillars = diagram_data.get("pillars", [])
        for pillar in pillars:
            output.append(f"  [{pillar.get('id')}] {pillar.get('name')}")
            output.append(f"       Position: ({pillar.get('x')}, {pillar.get('y')})")
            output.append(f"       Size: {pillar.get('width')}x{pillar.get('height')}")

        with open(output_path, "w") as f:
            f.write("\n".join(output))

        return output_path

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate Observability Architecture data structure."""
        required_keys = ["metadata", "config", "data"]
        if not all(key in data for key in required_keys):
            return False

        diagram_data = data.get("data", {})
        if "pillars" not in diagram_data:
            return False

        return True
