"""UML Deployment Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class DeploymentDiagramConverter(BaseDiagramConverter):
    """Converts UML Deployment Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Deployment Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for node in template.data.get("nodes", []):
            self.add_shape(doc, "rect", node.get("x"), node.get("y"), node.get("width"), 
                          node.get("height"), node.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        for conn in template.data.get("connections", []):
            self.add_connector(doc, conn.get("from"), conn.get("to"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Deployment Diagram saved: {self.output_path}")
