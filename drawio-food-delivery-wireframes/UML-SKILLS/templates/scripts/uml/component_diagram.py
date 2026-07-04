"""UML Component Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class ComponentDiagramConverter(BaseDiagramConverter):
    """Converts UML Component Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Component Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for comp in template.data.get("components", []):
            self.add_shape(doc, "rect", comp.get("x"), comp.get("y"), comp.get("width"), 
                          comp.get("height"), comp.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        for dep in template.data.get("dependencies", []):
            self.add_connector(doc, dep.get("from"), dep.get("to"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Component Diagram saved: {self.output_path}")
