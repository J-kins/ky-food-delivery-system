"""Cloud Cost Optimization SVG to Visio Converter"""

import logging
from typing import Any, Dict, List
from ..base import BaseDiagramConverter

logger = logging.getLogger(__name__)


class CloudCostOptimizationConverter(BaseDiagramConverter):
    """Convert cloud cost optimization SVG templates to Visio diagrams."""

    def render_diagram(self) -> None:
        """Render cost optimization phases and techniques."""
        data = self.get_data()
        tokens = self.get_design_tokens()

        logger.info(f"Rendering Cloud Cost Optimization: {data.get('metadata', {}).get('projectName')}")

        # Title
        title = f"Cloud Cost Optimization - {data.get('metadata', {}).get('projectName', 'Unknown')}"
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

        # Render optimization phases
        optimization_data = data.get("data", {})
        phases = optimization_data.get("phases", [])
        
        for phase in phases:
            y_pos = self._render_phase(phase, y_pos, tokens)

        # Render optimization techniques
        techniques = optimization_data.get("techniques", [])
        if techniques:
            self._render_techniques(techniques, y_pos, tokens)

        logger.debug(f"Cloud Cost Optimization: {len(phases)} phases and {len(techniques)} techniques")

    def _render_phase(
        self,
        phase: Dict[str, Any],
        y_pos: float,
        tokens: Dict[str, str],
    ) -> float:
        """Render optimization phase."""
        phase_name = phase.get("name", "Phase")
        phase_colors = {
            "Cost Analysis": "#E53935",
            "Optimization": "#FBC02D",
            "Monitoring": "#00897B",
        }
        
        color = phase_colors.get(phase_name, tokens.get("fill", "#E5E5E5"))
        
        # Phase box
        self.builder.add_shape(
            "rectangle",
            x=0.5,
            y=y_pos,
            width=7.5,
            height=0.5,
            text=phase_name,
            style={
                "fill": color,
                "stroke": tokens.get("stroke", "#1A1A1A"),
                "font_weight": "bold",
                "font_size": 12,
                "text": "#FFFFFF",
            },
        )

        logger.debug(f"Optimization Phase: {phase_name}")
        return y_pos + 0.7

    def _render_techniques(
        self,
        techniques: List[Dict[str, str]],
        y_pos: float,
        tokens: Dict[str, str],
    ) -> None:
        """Render optimization techniques."""
        logger.debug(f"Rendering {len(techniques)} optimization techniques")

        for technique in techniques:
            technique_name = technique.get("name", "Technique")
            
            self.builder.add_shape(
                "text",
                x=1.0,
                y=y_pos,
                width=7.0,
                height=0.25,
                text=f"• {technique_name}",
                style={"font_size": 9},
            )
            y_pos += 0.3
