"""
Influence Network Diagram Converter
Renders stakeholder influence relationships and network topology
"""

from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder


class InfluenceNetworkConverter(BaseDiagramConverter):
    """
    Converts influence network SVG to Visio.
    Visualizes dependencies, influence flows, and relationships between stakeholders.
    """

    diagram_type = "influence-network"
    template_name = "Influence Network"

    def __init__(self, svg_path, output_path=None):
        super().__init__(svg_path, output_path)
        self.network_data = None

    def parse_data(self):
        """Extract network data from embedded JSON"""
        try:
            data = super().parse_data()
            self.network_data = data
            nodes = data.get("nodes", [])
            edges = data.get("edges", [])
            self.logger.info(
                f"Loaded influence network with {len(nodes)} nodes and {len(edges)} edges"
            )
            return data
        except Exception as e:
            self.logger.error(f"Failed to parse influence network: {e}")
            raise

    def build_diagram(self, vsdx):
        """Build network visualization"""
        if not self.network_data:
            raise ValueError("No network data available")

        builder = VisioBuilder(vsdx)
        data = self.network_data
        tokens = data.get("designTokens", {}).get(self.mode, {})

        # Add title
        builder.add_title(
            data.get("projectName", "Project"),
            data.get("description", "Influence Network"),
        )

        # Position nodes in circular layout
        nodes = data.get("nodes", [])
        num_nodes = len(nodes)
        radius = 200
        center_x, center_y = 400, 300

        import math

        node_positions = {}
        for i, node in enumerate(nodes):
            angle = (2 * math.pi * i) / num_nodes if num_nodes > 0 else 0
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            node_positions[node.get("id")] = (x, y)

            # Determine node color by type
            node_type = node.get("type", "")
            color_map = {
                "executive": "#F44336",
                "project_team": "#2196F3",
                "engineering": "#4CAF50",
                "quality": "#FF9800",
            }
            fill_color = color_map.get(node_type, tokens.get("fill", "#E5E5E5"))

            # Add node shape
            builder.add_shape(
                shape_type="circle",
                x=x - 40,
                y=y - 40,
                width=80,
                height=80,
                text=node.get("name", ""),
                fill_color=fill_color,
                stroke_color=tokens.get("stroke", "#1A1A1A"),
                stroke_weight=1.5,
                font_size=10,
                font_weight=600,
            )

        # Add edges (connections)
        edges = data.get("edges", [])
        for edge in edges:
            source_id = edge.get("source")
            target_id = edge.get("target")
            weight = edge.get("weight", "medium")

            if source_id in node_positions and target_id in node_positions:
                sx, sy = node_positions[source_id]
                tx, ty = node_positions[target_id]

                stroke_width = 2 if weight == "strong" else 1
                stroke_dasharray = None if weight == "strong" else "4,4"

                builder.add_connector(
                    x1=sx,
                    y1=sy,
                    x2=tx,
                    y2=ty,
                    stroke_color=tokens.get("stroke", "#1A1A1A"),
                    stroke_width=stroke_width,
                    stroke_dasharray=stroke_dasharray,
                    text=weight.capitalize(),
                    with_arrow=True,
                )

        return vsdx

    def convert(self):
        """Execute conversion pipeline"""
        self.logger.info(f"Converting {self.diagram_type} to Visio...")
        self.parse_data()
        vsdx = self.create_visio_document()
        self.build_diagram(vsdx)
        output_file = self.save_visio(vsdx)
        self.logger.info(f"Influence network saved to {output_file}")
        return output_file
