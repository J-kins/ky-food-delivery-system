"""
Stakeholder Map Converter
Renders stakeholder relationships and positioning diagrams in Visio
"""

from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder
import json


class StakeholderMapConverter(BaseDiagramConverter):
    """
    Converts data-driven stakeholder map SVG templates to Visio diagrams.
    Maps stakeholder positions, relationships, influence levels, and interactions.
    """

    diagram_type = "stakeholder-map"
    template_name = "Stakeholder Map"

    def __init__(self, svg_path, output_path=None):
        super().__init__(svg_path, output_path)
        self.stakeholder_map_data = None

    def parse_data(self):
        """Extract stakeholder data from embedded JSON"""
        try:
            data = super().parse_data()
            self.stakeholder_map_data = data
            self.logger.info(
                f"Loaded {len(data.get('stakeholders', []))} stakeholders for map"
            )
            return data
        except Exception as e:
            self.logger.error(f"Failed to parse stakeholder map data: {e}")
            raise

    def build_diagram(self, vsdx):
        """Build Visio diagram from stakeholder data"""
        if not self.stakeholder_map_data:
            raise ValueError("No stakeholder data available. Run parse_data() first.")

        builder = VisioBuilder(vsdx)
        data = self.stakeholder_map_data

        # Add title
        builder.add_title(
            data.get("projectName", "Project"),
            data.get("description", "Stakeholder Map"),
        )

        # Get design tokens
        tokens = data.get("designTokens", {}).get(self.mode, {})

        # Add center entity
        center = data.get("centerEntity", {})
        center_x = center.get("x", 400)
        center_y = center.get("y", 300)
        center_width = center.get("width", 140)
        center_height = center.get("height", 80)

        builder.add_shape(
            shape_type="rectangle",
            x=center_x - center_width / 2,
            y=center_y - center_height / 2,
            width=center_width,
            height=center_height,
            text=center.get("name", "System"),
            fill_color=tokens.get("fill", "#E5E5E5"),
            stroke_color=tokens.get("stroke", "#1A1A1A"),
            stroke_weight=1.5,
            corner_radius=8,
        )

        # Add stakeholders
        stakeholders = data.get("stakeholders", [])
        for stakeholder in stakeholders:
            pos = stakeholder.get("position", {})
            x = pos.get("x", 100)
            y = pos.get("y", 100)
            width = 120
            height = 70

            # Determine if indirect (dashed border)
            relationship = stakeholder.get("relationship", "Direct")
            is_indirect = relationship == "Indirect"

            builder.add_shape(
                shape_type="rectangle",
                x=x,
                y=y,
                width=width,
                height=height,
                text=f"{stakeholder.get('name', '')}\n({stakeholder.get('role', '')})",
                fill_color=tokens.get("fill", "#E5E5E5"),
                stroke_color=tokens.get("stroke", "#1A1A1A"),
                stroke_weight=1.5,
                stroke_dasharray="5,5" if is_indirect else None,
                corner_radius=6,
            )

            # Add connector line from stakeholder to center
            connector_dasharray = "4,4" if is_indirect else None
            builder.add_connector(
                x1=x + width / 2,
                y1=y + height / 2,
                x2=center_x,
                y2=center_y,
                stroke_color=tokens.get("stroke", "#1A1A1A"),
                stroke_width=1.5,
                stroke_dasharray=connector_dasharray,
                text=stakeholder.get("relationship", ""),
            )

        # Add connections between stakeholders
        connections = data.get("connections", [])
        for conn in connections:
            from_id = conn.get("from")
            to_id = conn.get("to")
            strength = conn.get("strength", "medium")

            from_stake = next(
                (s for s in stakeholders if s.get("id") == from_id), None
            )
            to_stake = next((s for s in stakeholders if s.get("id") == to_id), None)

            if from_stake and to_stake:
                from_pos = from_stake.get("position", {})
                to_pos = to_stake.get("position", {})

                stroke_weight = 2 if strength == "strong" else 1.5

                builder.add_connector(
                    x1=from_pos.get("x", 0),
                    y1=from_pos.get("y", 0),
                    x2=to_pos.get("x", 0),
                    y2=to_pos.get("y", 0),
                    stroke_color=tokens.get("stroke", "#1A1A1A"),
                    stroke_width=stroke_weight,
                    text=strength.capitalize(),
                )

        return vsdx

    def convert(self):
        """Execute full conversion pipeline"""
        self.logger.info(f"Converting {self.diagram_type} to Visio...")

        self.parse_data()

        vsdx = self.create_visio_document()
        self.build_diagram(vsdx)

        output_file = self.save_visio(vsdx)
        self.logger.info(f"Stakeholder map saved to {output_file}")

        return output_file
