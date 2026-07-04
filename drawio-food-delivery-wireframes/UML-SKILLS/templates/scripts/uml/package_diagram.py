"""UML Package Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class PackageDiagramConverter(BaseDiagramConverter):
    """Converts UML Package Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Package Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for pkg in template.data.get("packages", []):
            self.add_shape(doc, "rect", pkg.get("x"), pkg.get("y"), pkg.get("width"), 
                          pkg.get("height"), pkg.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Package Diagram saved: {self.output_path}")
