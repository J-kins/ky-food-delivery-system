"""
Power-Interest Matrix Converter
Renders stakeholder classification by power and interest level
"""

from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder


class PowerInterestMatrixConverter(BaseDiagramConverter):
    """
    Converts power-interest matrix SVG templates to Visio.
    Classifies stakeholders into: Manage Closely, Keep Satisfied, Keep Informed, Monitor
    """

    diagram_type = "power-interest-matrix"
    template_name = "Power-Interest Matrix"

    def __init__(self, svg_path, output_path=None):
        super().__init__(svg_path, output_path)
        self.matrix_data = None

    def parse_data(self):
        """Extract matrix data from embedded JSON"""
        try:
            data = super().parse_data()
            self.matrix_data = data
            quadrants = data.get("quadrants", {})
            self.logger.info(f"Loaded power-interest matrix with {len(quadrants)} quadrants")
            return data
        except Exception as e:
            self.logger.error(f"Failed to parse power-interest matrix: {e}")
            raise

    def build_diagram(self, vsdx):
        """Build Visio matrix diagram"""
        if not self.matrix_data:
            raise ValueError("No matrix data available")

        builder = VisioBuilder(vsdx)
        data = self.matrix_data
        tokens = data.get("designTokens", {}).get(self.mode, {})

        # Add title
        builder.add_title(
            data.get("projectName", "Project"),
            data.get("description", "Power-Interest Matrix"),
        )

        # Matrix dimensions
        quadrants = data.get("quadrants", {})
        
        # Create 2x2 grid
        # Y-axis: Power (Low to High)
        # X-axis: Interest (Low to High)
        
        quad_configs = {
            "manage_closely": (600, 100, "#F44336"),  # High Power, High Interest - Red
            "keep_satisfied": (200, 100, "#FF9800"),  # High Power, Low Interest - Orange
            "keep_informed": (600, 400, "#2196F3"),  # Low Power, High Interest - Blue
            "monitor": (200, 400, "#9E9E9E"),  # Low Power, Low Interest - Gray
        }

        for quad_id, (x, y, color) in quad_configs.items():
            quad = quadrants.get(quad_id, {})
            label = quad.get("label", quad_id)

            # Add quadrant background
            builder.add_shape(
                shape_type="rectangle",
                x=x,
                y=y,
                width=180,
                height=180,
                text="",
                fill_color=color,
                fill_opacity=0.1,
                stroke_color=tokens.get("stroke", "#1A1A1A"),
                stroke_weight=1,
            )

            # Add quadrant label
            builder.add_text(x + 90, y + 10, label, font_size=12, font_weight=700)

            # Add stakeholders in quadrant
            stakeholders = quad.get("stakeholders", [])
            for i, stakeholder in enumerate(stakeholders):
                stake_y = y + 40 + (i * 35)
                builder.add_shape(
                    shape_type="rectangle",
                    x=x + 10,
                    y=stake_y,
                    width=160,
                    height=28,
                    text=stakeholder.get("name", ""),
                    fill_color=color,
                    fill_opacity=0.3,
                    stroke_color=tokens.get("stroke", "#1A1A1A"),
                    stroke_weight=1,
                    font_size=10,
                )

        # Add axis labels
        builder.add_text(100, 250, "POWER", font_size=11, font_weight=600, rotation=90)
        builder.add_text(400, 550, "INTEREST", font_size=11, font_weight=600)

        return vsdx

    def convert(self):
        """Execute conversion pipeline"""
        self.logger.info(f"Converting {self.diagram_type} to Visio...")
        self.parse_data()
        vsdx = self.create_visio_document()
        self.build_diagram(vsdx)
        output_file = self.save_visio(vsdx)
        self.logger.info(f"Power-interest matrix saved to {output_file}")
        return output_file
