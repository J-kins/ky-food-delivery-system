"""UML Profile Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class ProfileDiagramConverter(BaseDiagramConverter):
    """Converts UML Profile Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Profile Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for stereotype in template.data.get("stereotypes", []):
            self.add_shape(doc, "rect", stereotype.get("x"), stereotype.get("y"), stereotype.get("width"), 
                          stereotype.get("height"), stereotype.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Profile Diagram saved: {self.output_path}")
