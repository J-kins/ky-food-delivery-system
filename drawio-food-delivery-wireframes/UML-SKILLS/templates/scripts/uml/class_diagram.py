"""UML Class Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class ClassDiagramConverter(BaseDiagramConverter):
    """Converts UML Class Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Class Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for cls in template.data.get("classes", []):
            self.add_shape(doc, "rect", cls.get("x"), cls.get("y"), cls.get("width"), 
                          cls.get("height"), cls.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        for rel in template.data.get("relationships", []):
            self.add_connector(doc, rel.get("from"), rel.get("to"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Class Diagram saved: {self.output_path}")
