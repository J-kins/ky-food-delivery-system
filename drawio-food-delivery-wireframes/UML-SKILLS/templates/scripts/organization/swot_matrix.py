"""SWOT Matrix Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class SWOTMatrixConverter(BaseDiagramConverter):
    """Converts SWOT Matrix to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering SWOT Matrix")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        
        colors = {
            "s": "#86EFAC",  # Green for Strengths
            "w": "#FCA5A5",  # Red for Weaknesses
            "o": "#93C5FD",  # Blue for Opportunities
            "t": "#FBBF24"   # Orange for Threats
        }
        
        for quad in template.data.get("quadrants", []):
            self.add_shape(doc, "rect", 150, 150, 600, 400, 
                          quad.get("label"), colors.get(quad.get("id")), "#334155")
        
        self.save_vsdx(doc)
        self.logger.info(f"SWOT Matrix saved: {self.output_path}")
