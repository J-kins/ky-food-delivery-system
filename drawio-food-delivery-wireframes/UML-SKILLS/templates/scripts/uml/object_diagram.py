"""UML Object Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class ObjectDiagramConverter(BaseDiagramConverter):
    """Converts UML Object Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Object Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for obj in template.data.get("objects", []):
            self.add_shape(doc, "rect", obj.get("x"), obj.get("y"), obj.get("width"), 
                          obj.get("height"), obj.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        for link in template.data.get("links", []):
            self.add_connector(doc, link.get("from"), link.get("to"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Object Diagram saved: {self.output_path}")
