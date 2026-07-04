"""Project charter SVG to Visio converter."""

import logging
from pathlib import Path
from typing import Any, Dict

from ..base import BaseDiagramConverter

logger = logging.getLogger(__name__)


class ProjectCharterConverter(BaseDiagramConverter):
    """Convert project charter SVG templates to Visio diagrams."""

    def render_diagram(self) -> None:
        """Render project charter with sections."""
        data = self.get_data()
        tokens = self.get_design_tokens()

        logger.info(f"Rendering project charter: {data.get('projectName')}")

        # Title section
        self._add_section_title(
            data.get("projectName", "Project Charter"),
            y=0.3,
            tokens=tokens,
        )

        # Project info section
        y_pos = 1.0
        project_info = {
            "Project Code": data.get("projectCode", ""),
            "Version": data.get("version", "1.0"),
            "Last Updated": data.get("lastUpdated", ""),
        }
        y_pos = self._add_section(
            "Project Information",
            project_info,
            y_pos,
            tokens,
        )

        # Business case
        business_case = data.get("businessCase", {})
        y_pos = self._add_section(
            "Business Case",
            {
                "Business Need": business_case.get("businessNeed", ""),
                "Benefits": business_case.get("expectedBenefits", ""),
            },
            y_pos,
            tokens,
        )

        # Stakeholders
        stakeholders = data.get("stakeholders", [])
        y_pos = self._add_stakeholder_section(stakeholders, y_pos, tokens)

        # Budget
        budget = data.get("budget", {})
        y_pos = self._add_section(
            "Budget",
            {"Total": budget.get("total", "$0")},
            y_pos,
            tokens,
        )

        logger.debug(f"Charter layout complete at y={y_pos}")

    def _add_section_title(self, title: str, y: float, tokens: Dict[str, str]) -> None:
        """Add section title."""
        self.builder.add_shape(
            "text",
            x=0.5,
            y=y,
            width=5.0,
            height=0.4,
            text=title,
            style={
                "font_size": 20,
                "font_weight": "bold",
                "fill": tokens.get("text", "#1A1A1A"),
            },
        )

    def _add_section(
        self,
        section_name: str,
        fields: Dict[str, str],
        y_pos: float,
        tokens: Dict[str, str],
    ) -> float:
        """Add a section with fields."""
        # Section header
        self.builder.add_shape(
            "rectangle",
            x=0.5,
            y=y_pos,
            width=5.0,
            height=0.3,
            text=section_name,
            style={
                "fill": tokens.get("fill", "#E5E5E5"),
                "stroke": tokens.get("stroke", "#1A1A1A"),
                "font_weight": "bold",
                "font_size": 12,
            },
        )
        y_pos += 0.4

        # Fields
        for label, value in fields.items():
            self.builder.add_shape(
                "rectangle",
                x=0.5,
                y=y_pos,
                width=2.2,
                height=0.25,
                text=f"{label}: {value}",
                style={
                    "fill": tokens.get("fill", "#E5E5E5"),
                    "font_size": 10,
                },
            )
            y_pos += 0.3

        return y_pos + 0.3

    def _add_stakeholder_section(
        self,
        stakeholders: list[Dict[str, str]],
        y_pos: float,
        tokens: Dict[str, str],
    ) -> float:
        """Add stakeholder section."""
        # Header
        self.builder.add_shape(
            "rectangle",
            x=0.5,
            y=y_pos,
            width=5.0,
            height=0.3,
            text="Key Stakeholders",
            style={
                "fill": tokens.get("fill", "#E5E5E5"),
                "font_weight": "bold",
                "font_size": 12,
            },
        )
        y_pos += 0.4

        # Stakeholder rows
        for stakeholder in stakeholders:
            name = stakeholder.get("name", "")
            role = stakeholder.get("role", "")
            self.builder.add_shape(
                "rectangle",
                x=0.5,
                y=y_pos,
                width=5.0,
                height=0.25,
                text=f"{name} ({role})",
                style={"font_size": 10},
            )
            y_pos += 0.3

        return y_pos + 0.2
