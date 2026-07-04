"""Cloud Migration Architecture SVG to Visio Converter"""

import logging
from typing import Any, Dict, List
from ..base import BaseDiagramConverter

logger = logging.getLogger(__name__)


class CloudMigrationConverter(BaseDiagramConverter):
    """Convert cloud migration architecture SVG templates to Visio diagrams."""

    def render_diagram(self) -> None:
        """Render cloud migration architecture with on-premises and cloud phases."""
        data = self.get_data()
        tokens = self.get_design_tokens()

        logger.info(f"Rendering Cloud Migration: {data.get('metadata', {}).get('projectName')}")

        # Title
        title = f"Cloud Migration Architecture - {data.get('metadata', {}).get('projectName', 'Unknown')}"
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

        # Render migration phases
        migration_data = data.get("data", {})
        phases = migration_data.get("migrationPhases", [])
        
        for phase in phases:
            y_pos = self._render_phase(phase, y_pos, tokens)

        # Render migration tools
        tools = migration_data.get("tools", [])
        if tools:
            self._render_tools(tools, y_pos, tokens)

        logger.debug(f"Cloud Migration: {len(phases)} phases and {len(tools)} tools")

    def _render_phase(
        self,
        phase: Dict[str, Any],
        y_pos: float,
        tokens: Dict[str, str],
    ) -> float:
        """Render migration phase."""
        phase_name = phase.get("name", "Phase")
        phase_colors = {
            "On-Premises": "#808080",
            "Migration Tools": "#FFC107",
            "Cloud": "#4CAF50",
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
                "text": "#FFFFFF" if color in ["#808080", "#4CAF50"] else "#1A1A1A",
            },
        )

        logger.debug(f"Migration Phase: {phase_name}")
        return y_pos + 0.7

    def _render_tools(
        self,
        tools: List[str],
        y_pos: float,
        tokens: Dict[str, str],
    ) -> None:
        """Render migration tools list."""
        logger.debug(f"Rendering {len(tools)} migration tools")
        
        tools_text = " • ".join(tools)
        self.builder.add_shape(
            "text",
            x=0.5,
            y=y_pos,
            width=7.5,
            height=0.3,
            text=f"Tools: {tools_text}",
            style={"font_size": 9},
        )
