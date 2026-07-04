"""Sitemap SVG to Visio converter."""

import logging
from typing import Any, Dict, List, Optional

from ..base import BaseDiagramConverter

logger = logging.getLogger(__name__)


class SitemapConverter(BaseDiagramConverter):
    """Convert sitemap SVG templates to Visio diagrams."""

    def render_diagram(self) -> None:
        """Render sitemap hierarchy with pages and connections."""
        data = self.get_data()
        tokens = self.get_design_tokens()

        logger.info(f"Rendering sitemap: {data.get('projectName')}")

        # Title
        self.builder.add_shape(
            "text",
            x=0.5,
            y=0.3,
            width=5.0,
            height=0.4,
            text=f"Sitemap - {data.get('projectName')}",
            style={"font_size": 18, "font_weight": "bold"},
        )

        # Render hierarchy
        hierarchy = data.get("hierarchyStructure", [])
        y_pos = 1.2

        for level in hierarchy:
            y_pos = self._add_hierarchy_level(level, y_pos, tokens)

        # Add user flows section
        user_flows = data.get("userFlows", [])
        y_pos = self._add_user_flows(user_flows, y_pos, tokens)

        logger.debug(f"Sitemap layout complete with {len(hierarchy)} levels")

    def _add_hierarchy_level(
        self,
        level: Dict[str, Any],
        y_pos: float,
        tokens: Dict[str, str],
    ) -> float:
        """Add a hierarchy level with pages."""
        level_name = level.get("name", "Level")
        level_type = level.get("type", "primary")
        pages = level.get("pages", [])

        logger.debug(f"Level: {level_name} with {len(pages)} pages")

        # Level header
        fill_color = self._get_level_color(level_type, tokens)
        self.builder.add_shape(
            "rectangle",
            x=0.5,
            y=y_pos,
            width=5.0,
            height=0.3,
            text=level_name,
            style={
                "fill": fill_color,
                "stroke": tokens.get("stroke", "#1A1A1A"),
                "font_weight": "bold",
                "font_size": 12,
            },
        )
        y_pos += 0.4

        # Add page boxes
        x_pos = 0.5
        max_y = y_pos
        
        for i, page in enumerate(pages):
            # New row if needed
            if x_pos + 1.5 > 5.5:
                x_pos = 0.5
                y_pos += 0.5

            self._add_page_box(page, x_pos, y_pos, tokens)
            x_pos += 1.6
            max_y = max(max_y, y_pos + 0.4)

        return max_y + 0.3

    def _add_page_box(
        self,
        page: Dict[str, Any],
        x: float,
        y: float,
        tokens: Dict[str, str],
    ) -> None:
        """Add individual page box."""
        title = page.get("title", "Page")
        category = page.get("category", "")
        interactions = page.get("interactions", [])

        # Main box
        self.builder.add_shape(
            "rectangle",
            x=x,
            y=y,
            width=1.5,
            height=0.4,
            text=title,
            style={
                "fill": tokens.get("fill", "#E5E5E5"),
                "stroke": tokens.get("stroke", "#1A1A1A"),
                "font_weight": "bold",
                "font_size": 10,
            },
        )

        # Category label
        if category:
            self.builder.add_shape(
                "text",
                x=x,
                y=y + 0.42,
                width=1.5,
                height=0.15,
                text=category,
                style={"font_size": 8},
            )

        logger.debug(f"Page: {title} ({category}) with {len(interactions)} interactions")

    def _add_user_flows(
        self,
        flows: List[Dict[str, Any]],
        y_pos: float,
        tokens: Dict[str, str],
    ) -> float:
        """Add user flow documentation."""
        self.builder.add_shape(
            "rectangle",
            x=0.5,
            y=y_pos,
            width=5.0,
            height=0.3,
            text="Primary User Journeys",
            style={
                "fill": tokens.get("fill", "#E5E5E5"),
                "font_weight": "bold",
                "font_size": 12,
            },
        )
        y_pos += 0.4

        for i, flow in enumerate(flows, 1):
            flow_name = flow.get("flowName", f"Flow {i}")
            steps = flow.get("steps", [])
            step_text = " → ".join(steps[:4])  # Show first 4 steps
            if len(steps) > 4:
                step_text += "..."

            self.builder.add_shape(
                "rectangle",
                x=0.5,
                y=y_pos,
                width=5.0,
                height=0.35,
                text=f"{i}. {flow_name}: {step_text}",
                style={
                    "fill": tokens.get("fill", "#E5E5E5"),
                    "font_size": 9,
                },
            )
            y_pos += 0.4

        return y_pos + 0.2

    def _get_level_color(self, level_type: str, tokens: Dict[str, str]) -> str:
        """Get color for hierarchy level type."""
        colors = {
            "entry-point": "#262C7C",
            "primary": "#2196F3",
            "secondary": "#4CAF50",
            "tertiary": "#FFC107",
        }
        return colors.get(level_type, tokens.get("fill", "#E5E5E5"))
