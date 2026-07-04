"""
Stakeholder Register Converter
Renders comprehensive stakeholder inventory and engagement strategy
"""

from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder


class StakeholderRegisterConverter(BaseDiagramConverter):
    """
    Converts stakeholder register SVG to Visio.
    Comprehensive inventory with contact info, engagement level, interest, impact, and strategy.
    """

    diagram_type = "stakeholder-register"
    template_name = "Stakeholder Register"

    def __init__(self, svg_path, output_path=None):
        super().__init__(svg_path, output_path)
        self.register_data = None

    def parse_data(self):
        """Extract stakeholder register data from JSON"""
        try:
            data = super().parse_data()
            self.register_data = data
            stakeholders = data.get("stakeholders", [])
            self.logger.info(f"Loaded stakeholder register with {len(stakeholders)} entries")
            return data
        except Exception as e:
            self.logger.error(f"Failed to parse stakeholder register: {e}")
            raise

    def build_diagram(self, vsdx):
        """Build stakeholder register table"""
        if not self.register_data:
            raise ValueError("No register data available")

        builder = VisioBuilder(vsdx)
        data = self.register_data
        tokens = data.get("designTokens", {}).get(self.mode, {})

        # Add title
        builder.add_title(
            data.get("projectName", "Project"),
            data.get("description", "Stakeholder Register"),
        )

        stakeholders = data.get("stakeholders", [])

        # Column headers
        headers = ["Name", "Role", "Department", "Engagement", "Interest", "Strategy"]
        col_width = 180
        row_height = 50
        start_x = 30
        start_y = 100

        # Add header row
        for i, header in enumerate(headers):
            x = start_x + i * col_width
            builder.add_shape(
                shape_type="rectangle",
                x=x,
                y=start_y,
                width=col_width,
                height=35,
                text=header,
                fill_color="#262C7C",
                stroke_color=tokens.get("stroke", "#1A1A1A"),
                stroke_weight=1.5,
                font_size=11,
                font_weight=700,
                text_color="#FFFFFF",
            )

        # Add stakeholder rows
        for idx, stakeholder in enumerate(stakeholders):
            y = start_y + 35 + idx * row_height

            row_data = [
                stakeholder.get("name", ""),
                stakeholder.get("role", ""),
                stakeholder.get("department", ""),
                stakeholder.get("engagement", ""),
                stakeholder.get("interest", ""),
                stakeholder.get("strategy", ""),
            ]

            for col_idx, cell_text in enumerate(row_data):
                x = start_x + col_idx * col_width

                builder.add_shape(
                    shape_type="rectangle",
                    x=x,
                    y=y,
                    width=col_width,
                    height=row_height,
                    text=cell_text,
                    fill_color=tokens.get("fill", "#E5E5E5"),
                    stroke_color=tokens.get("stroke", "#1A1A1A"),
                    stroke_weight=1,
                    font_size=9,
                )

        # Add engagement strategy legend
        legend_y = start_y + 35 + len(stakeholders) * row_height + 50
        builder.add_text(start_x, legend_y, "Engagement Strategies:", font_size=11, font_weight=600)

        strategies = data.get("engagementStrategies", {})
        for i, (level, description) in enumerate(strategies.items()):
            builder.add_text(
                start_x,
                legend_y + 25 + i * 20,
                f"{level}: {description}",
                font_size=9,
            )

        return vsdx

    def convert(self):
        """Execute conversion pipeline"""
        self.logger.info(f"Converting {self.diagram_type} to Visio...")
        self.parse_data()
        vsdx = self.create_visio_document()
        self.build_diagram(vsdx)
        output_file = self.save_visio(vsdx)
        self.logger.info(f"Stakeholder register saved to {output_file}")
        return output_file
