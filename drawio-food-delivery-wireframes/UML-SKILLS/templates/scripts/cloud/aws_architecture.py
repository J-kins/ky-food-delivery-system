"""AWS Architecture SVG to Visio Converter"""

import logging
from typing import Any, Dict, List
from ..base import BaseDiagramConverter

logger = logging.getLogger(__name__)


class AWSArchitectureConverter(BaseDiagramConverter):
    """Convert AWS architecture SVG templates to Visio diagrams."""

    def render_diagram(self) -> None:
        """Render AWS architecture with VPC, services, and relationships."""
        data = self.get_data()
        tokens = self.get_design_tokens()

        logger.info(f"Rendering AWS Architecture: {data.get('metadata', {}).get('projectName')}")

        # Title
        title = f"AWS Architecture - {data.get('metadata', {}).get('projectName', 'Unknown')}"
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

        # Render VPC Container
        vpc_data = data.get("data", {})
        resource_groups = vpc_data.get("resourceGroups", [])
        
        for rg in resource_groups:
            y_pos = self._render_vpc(rg, y_pos, tokens)

        # Render services
        services = vpc_data.get("services", [])
        y_pos = self._render_services(services, y_pos, tokens)

        # Render relationships
        relationships = vpc_data.get("relationships", [])
        if relationships:
            self._render_relationships(relationships, tokens)

        logger.debug(f"AWS Architecture: {len(services)} services rendered")

    def _render_vpc(
        self,
        vpc: Dict[str, Any],
        y_pos: float,
        tokens: Dict[str, str],
    ) -> float:
        """Render VPC container."""
        vpc_name = vpc.get("name", "AWS VPC")
        
        # VPC box
        self.builder.add_shape(
            "rectangle",
            x=0.5,
            y=y_pos,
            width=7.5,
            height=0.35,
            text=vpc_name,
            style={
                "fill": tokens.get("fill", "#E5E5E5"),
                "stroke": tokens.get("stroke", "#1A1A1A"),
                "font_weight": "bold",
                "font_size": 12,
            },
        )

        logger.debug(f"VPC Container: {vpc_name}")
        return y_pos + 0.5

    def _render_services(
        self,
        services: List[Dict[str, Any]],
        y_pos: float,
        tokens: Dict[str, str],
    ) -> float:
        """Render AWS services."""
        service_colors = {
            "compute": "#FF9900",
            "storage": "#569A31",
            "database": "#527FFF",
            "networking": "#FF9900",
        }

        x_pos = 0.5
        max_y = y_pos

        for service in services:
            service_name = service.get("name", "Service")
            service_type = service.get("id", "compute").lower()
            description = service.get("description", "")

            # Service box
            color = service_colors.get(service_type, tokens.get("fill", "#E5E5E5"))
            
            self.builder.add_shape(
                "rectangle",
                x=x_pos,
                y=y_pos,
                width=2.0,
                height=0.5,
                text=service_name,
                style={
                    "fill": color,
                    "stroke": tokens.get("stroke", "#1A1A1A"),
                    "font_weight": "bold",
                    "font_size": 11,
                },
            )

            # Description
            if description:
                self.builder.add_shape(
                    "text",
                    x=x_pos,
                    y=y_pos + 0.52,
                    width=2.0,
                    height=0.25,
                    text=description,
                    style={"font_size": 8},
                )
                max_y = max(max_y, y_pos + 0.8)
            else:
                max_y = max(max_y, y_pos + 0.5)

            x_pos += 2.2
            if x_pos > 7.5:
                x_pos = 0.5
                y_pos = max_y + 0.2

        return max_y + 0.3

    def _render_relationships(
        self,
        relationships: List[Dict[str, str]],
        tokens: Dict[str, str],
    ) -> None:
        """Render service relationships/connectors."""
        logger.debug(f"Rendering {len(relationships)} relationships")
        
        for rel in relationships:
            relationship_label = rel.get("label", "")
            logger.debug(f"Relationship: {rel.get('from')} -> {rel.get('to')} ({relationship_label})")
