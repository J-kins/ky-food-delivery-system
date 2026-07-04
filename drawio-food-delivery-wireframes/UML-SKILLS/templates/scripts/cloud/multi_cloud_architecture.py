"""Multi-Cloud Architecture SVG to Visio Converter"""

import logging
from typing import Any, Dict, List
from ..base import BaseDiagramConverter

logger = logging.getLogger(__name__)


class MultiCloudArchitectureConverter(BaseDiagramConverter):
    """Convert multi-cloud architecture SVG templates to Visio diagrams."""

    def render_diagram(self) -> None:
        """Render multi-cloud architecture with multiple cloud providers."""
        data = self.get_data()
        tokens = self.get_design_tokens()

        logger.info(f"Rendering Multi-Cloud Architecture: {data.get('metadata', {}).get('projectName')}")

        # Title
        title = f"Multi-Cloud Architecture - {data.get('metadata', {}).get('projectName', 'Unknown')}"
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

        # Render cloud providers
        multi_cloud_data = data.get("data", {})
        providers = multi_cloud_data.get("cloudProviders", [])
        
        for provider in providers:
            y_pos = self._render_provider(provider, y_pos, tokens)

        # Render integrations
        integrations = multi_cloud_data.get("integrations", [])
        if integrations:
            self._render_integrations(integrations, tokens)

        logger.debug(f"Multi-Cloud Architecture: {len(providers)} cloud providers")

    def _render_provider(
        self,
        provider: Dict[str, Any],
        y_pos: float,
        tokens: Dict[str, str],
    ) -> float:
        """Render cloud provider section."""
        provider_name = provider.get("name", "Cloud Provider")
        provider_colors = {
            "AWS": "#FF9900",
            "Azure": "#0078D4",
            "Google Cloud": "#4285F4",
        }
        
        color = provider_colors.get(provider_name, tokens.get("fill", "#E5E5E5"))
        
        # Provider header
        self.builder.add_shape(
            "rectangle",
            x=0.5,
            y=y_pos,
            width=7.5,
            height=0.35,
            text=provider_name,
            style={
                "fill": color,
                "stroke": tokens.get("stroke", "#1A1A1A"),
                "font_weight": "bold",
                "font_size": 12,
                "text": "#FFFFFF" if color != tokens.get("fill") else "#1A1A1A",
            },
        )

        logger.debug(f"Cloud Provider: {provider_name}")
        return y_pos + 0.5

    def _render_integrations(
        self,
        integrations: List[Dict[str, str]],
        tokens: Dict[str, str],
    ) -> None:
        """Render integration connections between cloud providers."""
        logger.debug(f"Rendering {len(integrations)} cloud integrations")
        
        for integration in integrations:
            from_provider = integration.get("from", "")
            to_provider = integration.get("to", "")
            integration_type = integration.get("type", "data-sync")
            
            logger.debug(f"Integration: {from_provider} <-> {to_provider} ({integration_type})")
