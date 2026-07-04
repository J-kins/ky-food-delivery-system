"""Container Architecture Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class ContainerArchitectureConverter(BaseDiagramConverter):
    """Converts Container Architecture to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Container Architecture diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for layer in template.data.get("layers", []):
            self.add_shape(doc, "rect", layer.get("x"), layer.get("y"), layer.get("width"), 
                          layer.get("height"), layer.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"Container Architecture diagram saved: {self.output_path}")
