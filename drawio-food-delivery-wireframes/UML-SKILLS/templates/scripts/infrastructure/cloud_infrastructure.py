"""Cloud Infrastructure Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class CloudInfrastructureConverter(BaseDiagramConverter):
    """Converts Cloud Infrastructure to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Cloud Infrastructure diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for provider in template.data.get("providers", []):
            self.add_shape(doc, "rect", provider.get("x"), provider.get("y"), provider.get("width"), 
                          provider.get("height"), provider.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"Cloud Infrastructure diagram saved: {self.output_path}")
