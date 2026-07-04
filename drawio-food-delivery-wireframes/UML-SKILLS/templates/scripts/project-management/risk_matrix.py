"""Risk matrix SVG to Visio converter."""

import logging
from typing import Any, Dict

from ..base import BaseDiagramConverter

logger = logging.getLogger(__name__)


class RiskMatrixConverter(BaseDiagramConverter):
    """Convert risk matrix SVG templates to Visio diagrams."""

    def render_diagram(self) -> None:
        """Render risk matrix grid with risks positioned."""
        data = self.get_data()
        tokens = self.get_design_tokens()

        logger.info(f"Rendering risk matrix: {data.get('projectName')}")

        # Title
        self.builder.add_shape(
            "text",
            x=0.5,
            y=0.3,
            width=5.0,
            height=0.4,
            text="Risk Matrix (Probability × Impact)",
            style={"font_size": 18, "font_weight": "bold"},
        )

        # Draw matrix grid (3x3 or 5x5)
        self._draw_matrix_grid(tokens)

        # Add risks
        risks = data.get("risks", [])
        for risk in risks:
            self._add_risk_to_matrix(risk, tokens)

        logger.debug(f"Added {len(risks)} risks to matrix")

    def _draw_matrix_grid(self, tokens: Dict[str, str]) -> None:
        """Draw the risk matrix grid."""
        grid_start_x = 1.0
        grid_start_y = 1.0
        cell_size = 1.0

        # Draw 3x3 grid
        for i in range(3):
            for j in range(3):
                x = grid_start_x + (i * cell_size)
                y = grid_start_y + (j * cell_size)

                # Determine risk level color
                if i == 2 and j == 2:  # High risk
                    fill = "#FF6B6B"
                elif i == 1 and j == 1:  # Medium risk
                    fill = "#FFD93D"
                else:  # Low risk
                    fill = "#6BCB77"

                self.builder.add_shape(
                    "rectangle",
                    x=x,
                    y=y,
                    width=cell_size - 0.05,
                    height=cell_size - 0.05,
                    style={
                        "fill": fill,
                        "stroke": tokens.get("stroke", "#1A1A1A"),
                        "opacity": "0.3",
                    },
                )

        # Add axis labels
        self.builder.add_shape(
            "text",
            x=grid_start_x - 0.5,
            y=grid_start_y + 2 * cell_size,
            width=0.4,
            height=0.8,
            text="Probability",
            style={"font_size": 10, "font_weight": "bold"},
        )

        self.builder.add_shape(
            "text",
            x=grid_start_x,
            y=grid_start_y + 3 * cell_size,
            width=3 * cell_size,
            height=0.3,
            text="Impact",
            style={"font_size": 10, "font_weight": "bold"},
        )

    def _add_risk_to_matrix(self, risk: Dict[str, Any], tokens: Dict[str, str]) -> None:
        """Add risk item to matrix."""
        description = risk.get("description", "Risk")
        probability = risk.get("probability", "Medium")
        impact = risk.get("impact", "Medium")

        # Map probability and impact to grid position
        prob_map = {"Low": 0, "Medium": 1, "High": 2}
        impact_map = {"Low": 0, "Medium": 1, "High": 2}

        prob_val = prob_map.get(probability, 1)
        impact_val = impact_map.get(impact, 1)

        x = 1.0 + (prob_val * 1.0) + 0.2
        y = 1.0 + (impact_val * 1.0) + 0.2

        logger.debug(f"Risk: {description} at grid ({prob_val}, {impact_val})")

        self.builder.add_shape(
            "circle",
            x=x,
            y=y,
            width=0.3,
            height=0.3,
            text=description[:2],  # Abbreviate
            style={
                "fill": "#E74C3C",
                "stroke": tokens.get("stroke", "#1A1A1A"),
                "font_size": 8,
            },
        )
