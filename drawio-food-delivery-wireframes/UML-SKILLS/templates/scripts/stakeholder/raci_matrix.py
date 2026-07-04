"""
RACI Matrix Converter
Renders responsibility assignment matrix (Responsible, Accountable, Consulted, Informed)
"""

from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder


class RACIMatrixConverter(BaseDiagramConverter):
    """
    Converts RACI matrix SVG to Visio.
    Maps activities to roles with responsibility levels: R, A, C, I.
    """

    diagram_type = "raci-matrix"
    template_name = "RACI Matrix"

    def __init__(self, svg_path, output_path=None):
        super().__init__(svg_path, output_path)
        self.raci_data = None

    def parse_data(self):
        """Extract RACI matrix data from JSON"""
        try:
            data = super().parse_data()
            self.raci_data = data
            activities = data.get("activities", [])
            roles = data.get("roles", [])
            self.logger.info(f"Loaded RACI matrix: {len(activities)} activities × roles")
            return data
        except Exception as e:
            self.logger.error(f"Failed to parse RACI matrix: {e}")
            raise

    def build_diagram(self, vsdx):
        """Build RACI matrix table"""
        if not self.raci_data:
            raise ValueError("No RACI data available")

        builder = VisioBuilder(vsdx)
        data = self.raci_data
        tokens = data.get("designTokens", {}).get(self.mode, {})

        # Add title
        builder.add_title(
            data.get("projectName", "Project"),
            data.get("description", "RACI Matrix"),
        )

        roles = data.get("roles", ["Responsible", "Accountable", "Consulted", "Informed"])
        activities = data.get("activities", [])

        # Table dimensions
        col_width = 120
        row_height = 40
        start_x = 50
        start_y = 100

        # Add role headers
        for i, role in enumerate(roles):
            x = start_x + (i + 1) * col_width
            builder.add_text(
                x + col_width / 2,
                start_y - 30,
                role[0].upper(),  # Use first letter (R, A, C, I)
                font_size=12,
                font_weight=600,
                text_anchor="middle",
            )

        # Add activity rows
        for activity_idx, activity in enumerate(activities):
            y = start_y + activity_idx * row_height

            # Activity name
            builder.add_shape(
                shape_type="rectangle",
                x=start_x,
                y=y,
                width=col_width,
                height=row_height,
                text=activity.get("name", ""),
                fill_color=tokens.get("fill", "#E5E5E5"),
                stroke_color=tokens.get("stroke", "#1A1A1A"),
                stroke_weight=1,
                font_size=9,
            )

            # Responsible
            resp = activity.get("responsible", "")
            builder.add_shape(
                shape_type="rectangle",
                x=start_x + col_width,
                y=y,
                width=col_width,
                height=row_height,
                text="R\n" + (resp[:10] if resp else ""),
                fill_color="#FFE0B2",
                stroke_color=tokens.get("stroke", "#1A1A1A"),
                stroke_weight=1,
                font_size=8,
            )

            # Accountable
            acct = activity.get("accountable", "")
            builder.add_shape(
                shape_type="rectangle",
                x=start_x + 2 * col_width,
                y=y,
                width=col_width,
                height=row_height,
                text="A\n" + (acct[:10] if acct else ""),
                fill_color="#C8E6C9",
                stroke_color=tokens.get("stroke", "#1A1A1A"),
                stroke_weight=1,
                font_size=8,
            )

            # Consulted
            consulted = activity.get("consulted", [])
            consulted_str = ", ".join(consulted)[:15] if consulted else ""
            builder.add_shape(
                shape_type="rectangle",
                x=start_x + 3 * col_width,
                y=y,
                width=col_width,
                height=row_height,
                text="C\n" + consulted_str,
                fill_color="#BBDEFB",
                stroke_color=tokens.get("stroke", "#1A1A1A"),
                stroke_weight=1,
                font_size=8,
            )

            # Informed
            informed = activity.get("informed", [])
            informed_str = ", ".join(informed)[:15] if informed else ""
            builder.add_shape(
                shape_type="rectangle",
                x=start_x + 4 * col_width,
                y=y,
                width=col_width,
                height=row_height,
                text="I\n" + informed_str,
                fill_color="#E1BEE7",
                stroke_color=tokens.get("stroke", "#1A1A1A"),
                stroke_weight=1,
                font_size=8,
            )

        return vsdx

    def convert(self):
        """Execute conversion pipeline"""
        self.logger.info(f"Converting {self.diagram_type} to Visio...")
        self.parse_data()
        vsdx = self.create_visio_document()
        self.build_diagram(vsdx)
        output_file = self.save_visio(vsdx)
        self.logger.info(f"RACI matrix saved to {output_file}")
        return output_file
