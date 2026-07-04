"""Serverless Architecture SVG to Visio Converter"""

import logging
from typing import Any, Dict, List
from ..base import BaseDiagramConverter

logger = logging.getLogger(__name__)


class ServerlessArchitectureConverter(BaseDiagramConverter):
    """Convert serverless architecture SVG templates to Visio diagrams."""

    def render_diagram(self) -> None:
        """Render serverless architecture with API gateway, functions, and data services."""
        data = self.get_data()
        tokens = self.get_design_tokens()

        logger.info(f"Rendering Serverless Architecture: {data.get('metadata', {}).get('projectName')}")

        # Title
        title = f"Serverless Architecture - {data.get('metadata', {}).get('projectName', 'Unknown')}"
        self.builder.add_shape(
            "text",
            x=0.5,
            y=0.3,
            width=8.0,
            height=0.4,
            text=title,
            style={"font_size": 18, "font_weight": "bold", "fill": tokens.get("stroke", "#1A1A1A")},
        )

        y_pos = 1.0

        # Render architecture layers
        serverless_data = data.get("data", {})
        layers = serverless_data.get("layers", [])
        
        for layer in layers:
            y_pos = self._render_layer(layer, y_pos, tokens)

        logger.debug(f"Serverless Architecture: {len(layers)} layers rendered")

    def _render_layer(
        self,
        layer: Dict[str, Any],
        y_pos: float,
        tokens: Dict[str, str],
    ) -> float:
        """Render serverless architecture layer."""
        layer_name = layer.get("name", "Layer")
        layer_colors = {
            "API Gateway": "#FF9900",
            "Lambda Functions": "#FF9900",
            "Data Services": "#569A31",
        }
        
        color = layer_colors.get(layer_name, tokens.get("fill", "#E5E5E5"))
        
        # Layer box
        self.builder.add_shape(
            "rectangle",
            x=0.5,
            y=y_pos,
            width=7.5,
            height=0.5,
            text=layer_name,
            style={
                "fill": color,
                "stroke": tokens.get("stroke", "#1A1A1A"),
                "font_weight": "bold",
                "font_size": 12,
                "text": "#FFFFFF" if color != tokens.get("fill") else "#1A1A1A",
            },
        )

        logger.debug(f"Serverless Layer: {layer_name}")
        return y_pos + 0.7
