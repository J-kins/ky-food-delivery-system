"""UML Use Case Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class UseCaseDiagramConverter(BaseDiagramConverter):
    """Converts UML Use Case Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Use Case Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for actor in template.data.get("actors", []):
            self.add_shape(doc, "circle", actor.get("x"), actor.get("y"), actor.get("width"), 
                          actor.get("height"), actor.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        for uc in template.data.get("usecases", []):
            self.add_shape(doc, "ellipse", uc.get("x"), uc.get("y"), uc.get("width"), 
                          uc.get("height"), uc.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Use Case Diagram saved: {self.output_path}")
