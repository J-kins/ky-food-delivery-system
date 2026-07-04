"""UML Interaction Overview Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class InteractionOverviewDiagramConverter(BaseDiagramConverter):
    """Converts UML Interaction Overview Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Interaction Overview Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for frag in template.data.get("fragments", []):
            self.add_shape(doc, "rect", frag.get("x"), frag.get("y"), frag.get("width"), 
                          frag.get("height"), frag.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Interaction Overview Diagram saved: {self.output_path}")
