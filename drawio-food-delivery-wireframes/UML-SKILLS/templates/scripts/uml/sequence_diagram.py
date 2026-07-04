"""UML Sequence Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class SequenceDiagramConverter(BaseDiagramConverter):
    """Converts UML Sequence Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Sequence Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for part in template.data.get("participants", []):
            self.add_shape(doc, "rect", part.get("x"), part.get("y"), part.get("width"), 
                          part.get("height"), part.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        for msg in template.data.get("messages", []):
            self.add_connector(doc, msg.get("from"), msg.get("to"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Sequence Diagram saved: {self.output_path}")
