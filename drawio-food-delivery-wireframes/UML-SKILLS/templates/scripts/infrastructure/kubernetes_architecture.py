"""Kubernetes Architecture Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class KubernetesArchitectureConverter(BaseDiagramConverter):
    """Converts Kubernetes Architecture to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Kubernetes Architecture diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for component in template.data.get("components", []):
            self.add_shape(doc, "rect", component.get("x"), component.get("y"), component.get("width"), 
                          component.get("height"), component.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"Kubernetes Architecture diagram saved: {self.output_path}")
