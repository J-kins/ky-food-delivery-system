"""Work Breakdown Structure SVG to Visio converter."""

import logging
from typing import Any, Dict, List

from ..base import BaseDiagramConverter

logger = logging.getLogger(__name__)


class WBSConverter(BaseDiagramConverter):
    """Convert WBS SVG templates to Visio diagrams."""

    def render_diagram(self) -> None:
        """Render WBS tree structure."""
        data = self.get_data()
        tokens = self.get_design_tokens()

        logger.info(f"Rendering WBS: {data.get('projectName')}")

        # Title
        self.builder.add_shape(
            "text",
            x=0.5,
            y=0.3,
            width=5.0,
            height=0.4,
            text=data.get("projectName", "WBS"),
            style={"font_size": 18, "font_weight": "bold"},
        )

        # Root element
        wbs_structure = data.get("wbsStructure", {})
        self._add_wbs_node(wbs_structure, x=2.5, y=1.0, tokens=tokens)

    def _add_wbs_node(
        self,
        node: Dict[str, Any],
        x: float,
        y: float,
        level: int = 0,
        tokens: Dict[str, str] = None,
    ) -> float:
        """Recursively add WBS nodes."""
        if tokens is None:
            tokens = {}

        node_name = node.get("name", "Node")
        node_code = node.get("code", "")
        children = node.get("children", [])

        # Add node box
        box_width = 2.0 - (level * 0.2)
        box_height = 0.35
        
        text_label = f"{node_code}: {node_name}" if node_code else node_name
        
        self.builder.add_shape(
            "rectangle",
            x=x,
            y=y,
            width=box_width,
            height=box_height,
            text=text_label,
            style={
                "fill": tokens.get("fill", "#E5E5E5"),
                "stroke": tokens.get("stroke", "#1A1A1A"),
                "font_size": 11 - level,
            },
        )

        logger.debug(f"WBS Node: {node_code} at ({x}, {y})")

        # Add children
        current_y = y + box_height + 0.3
        x_offset = 0.5 + (level * 0.3)

        for child in children:
            # Add connector
            self.builder.add_connector(
                len(self.builder.shapes) - 1,
                len(self.builder.shapes),  # Will be next shape
                connector_type="straight",
            )

            # Recursively add child
            current_y = self._add_wbs_node(
                child,
                x=x + x_offset,
                y=current_y,
                level=level + 1,
                tokens=tokens,
            )

        return current_y + 0.2
