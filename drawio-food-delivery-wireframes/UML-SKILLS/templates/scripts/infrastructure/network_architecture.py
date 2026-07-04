"""Network Architecture Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class NetworkArchitectureConverter(BaseDiagramConverter):
    """Converts Network Architecture to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Network Architecture diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for zone in template.data.get("zones", []):
            self.add_shape(doc, "rect", zone.get("x"), zone.get("y"), zone.get("width"), 
                          zone.get("height"), zone.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"Network Architecture diagram saved: {self.output_path}")
