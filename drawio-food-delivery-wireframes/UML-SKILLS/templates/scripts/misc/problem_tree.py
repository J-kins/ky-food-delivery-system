"""Problem Tree Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class ProblemTreeConverter(BaseDiagramConverter):
    """Converts Problem Tree Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Problem Tree Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        
        # Root problem
        root = template.data.get("root", {})
        self.add_shape(doc, "rect", root.get("x"), root.get("y"), root.get("width"), 
                      root.get("height"), root.get("label"), "#FEF3C7", "#FCD34D")
        
        # Effects (top)
        for effect in template.data.get("effects", []):
            self.add_shape(doc, "rect", effect.get("x"), effect.get("y"), effect.get("width"), 
                          effect.get("height"), effect.get("label"), "#FEE2E2", "#FCA5A5")
        
        # Root causes (bottom)
        for cause in template.data.get("causes", []):
            self.add_shape(doc, "rect", cause.get("x"), cause.get("y"), cause.get("width"), 
                          cause.get("height"), cause.get("label"), "#DBEAFE", "#93C5FD")
        
        self.save_vsdx(doc)
        self.logger.info(f"Problem Tree Diagram saved: {self.output_path}")
