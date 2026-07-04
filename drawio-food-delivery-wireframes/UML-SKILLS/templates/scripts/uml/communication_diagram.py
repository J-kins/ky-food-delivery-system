"""UML Communication Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class CommunicationDiagramConverter(BaseDiagramConverter):
    """Converts UML Communication Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Communication Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for obj in template.data.get("objects", []):
            self.add_shape(doc, "rect", obj.get("x"), obj.get("y"), obj.get("width"), 
                          obj.get("height"), obj.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Communication Diagram saved: {self.output_path}")
