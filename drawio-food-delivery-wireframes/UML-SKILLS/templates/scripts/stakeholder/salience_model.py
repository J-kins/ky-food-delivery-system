"""
Salience Model Converter
Renders stakeholder analysis by power, legitimacy, and urgency (3D model)
"""

from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder


class SalienceModelConverter(BaseDiagramConverter):
    """
    Converts salience model SVG to Visio.
    Classifies stakeholders by three dimensions: Power, Legitimacy, Urgency.
    """

    diagram_type = "salience-model"
    template_name = "Salience Model"

    def __init__(self, svg_path, output_path=None):
        super().__init__(svg_path, output_path)
        self.salience_data = None

    def parse_data(self):
        """Extract salience model data from JSON"""
        try:
            data = super().parse_data()
            self.salience_data = data
            stakeholders = data.get("stakeholders", [])
            self.logger.info(f"Loaded {len(stakeholders)} stakeholders for salience analysis")
            return data
        except Exception as e:
            self.logger.error(f"Failed to parse salience model: {e}")
            raise

    def build_diagram(self, vsdx):
        """Build 3D salience model visualization"""
        if not self.salience_data:
            raise ValueError("No salience data available")

        builder = VisioBuilder(vsdx)
        data = self.salience_data
        tokens = data.get("designTokens", {}).get(self.mode, {})

        # Add title
        builder.add_title(
            data.get("projectName", "Project"),
            data.get("description", "Salience Model (Power × Legitimacy × Urgency)"),
        )

        # Stakeholder classifications
        stakeholder_types = {
            "definitive": {"color": "#F44336", "label": "Definitive (P+L+U)"},
            "dependent": {"color": "#2196F3", "label": "Dependent (L+U)"},
            "dominant": {"color": "#4CAF50", "label": "Dominant (P+L)"},
            "dangerous": {"color": "#FF9800", "label": "Dangerous (P+U)"},
            "discretionary": {"color": "#9C27B0", "label": "Discretionary (L)"},
            "dormant": {"color": "#9E9E9E", "label": "Dormant (P)"},
        }

        stakeholders = data.get("stakeholders", [])

        # Create sections for each type
        y_pos = 100
        for type_id, type_info in stakeholder_types.items():
            # Add section header
            builder.add_text(
                50,
                y_pos,
                type_info.get("label", ""),
                font_size=11,
                font_weight=600,
                fill_color=type_info.get("color", "#000000"),
            )

            # Add stakeholders of this type
            type_stakeholders = [s for s in stakeholders if s.get("type") == type_id]
            for i, stake in enumerate(type_stakeholders):
                stake_y = y_pos + 25 + (i * 30)

                # Display stakeholder with salience scores
                text = f"{stake.get('name', '')} (P:{stake.get('power', 0):.1f} L:{stake.get('legitimacy', 0):.1f} U:{stake.get('urgency', 0):.1f})"

                builder.add_shape(
                    shape_type="rectangle",
                    x=50,
                    y=stake_y,
                    width=600,
                    height=25,
                    text=text,
                    fill_color=type_info.get("color", "#E5E5E5"),
                    fill_opacity=0.2,
                    stroke_color=tokens.get("stroke", "#1A1A1A"),
                    stroke_weight=1,
                    font_size=10,
                )

            y_pos += 100

        return vsdx

    def convert(self):
        """Execute conversion pipeline"""
        self.logger.info(f"Converting {self.diagram_type} to Visio...")
        self.parse_data()
        vsdx = self.create_visio_document()
        self.build_diagram(vsdx)
        output_file = self.save_visio(vsdx)
        self.logger.info(f"Salience model saved to {output_file}")
        return output_file
