"""Stakeholder Power/Interest Matrix Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class PowerInterestMatrixConverter(BaseDiagramConverter):
    """Converts Power/Interest Matrix to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Power/Interest Matrix")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        
        colors = {"q1": "#FEE2E2", "q2": "#FEF3C7", "q3": "#DBEAFE", "q4": "#ECFDF5"}
        for quad in template.data.get("quadrants", []):
            self.add_shape(doc, "rect", quad.get("x"), quad.get("y"), 300, 300, 
                          quad.get("name"), colors.get(quad.get("id")), "#334155")
        
        self.save_vsdx(doc)
        self.logger.info(f"Power/Interest Matrix saved: {self.output_path}")
