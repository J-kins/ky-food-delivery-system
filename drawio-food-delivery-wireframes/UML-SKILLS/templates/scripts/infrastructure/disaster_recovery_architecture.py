"""Disaster Recovery Architecture Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class DisasterRecoveryArchitectureConverter(BaseDiagramConverter):
    """Converts Disaster Recovery Architecture to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Disaster Recovery Architecture diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for site in template.data.get("sites", []):
            self.add_shape(doc, "rect", site.get("x"), site.get("y"), site.get("width"), 
                          site.get("height"), site.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"Disaster Recovery Architecture diagram saved: {self.output_path}")
