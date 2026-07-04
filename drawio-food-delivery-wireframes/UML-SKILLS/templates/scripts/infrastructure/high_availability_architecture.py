"""High Availability Architecture Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class HighAvailabilityArchitectureConverter(BaseDiagramConverter):
    """Converts High Availability Architecture to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering High Availability Architecture diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for region in template.data.get("regions", []):
            self.add_shape(doc, "rect", region.get("x"), region.get("y"), region.get("width"), 
                          region.get("height"), region.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"High Availability Architecture diagram saved: {self.output_path}")
