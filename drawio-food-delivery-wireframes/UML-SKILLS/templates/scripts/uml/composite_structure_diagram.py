"""UML Composite Structure Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class CompositeStructureDiagramConverter(BaseDiagramConverter):
    """Converts UML Composite Structure Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Composite Structure Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for clf in template.data.get("classifiers", []):
            self.add_shape(doc, "rect", clf.get("x"), clf.get("y"), clf.get("width"), 
                          clf.get("height"), clf.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Composite Structure Diagram saved: {self.output_path}")
