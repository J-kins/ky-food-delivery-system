"""Timeline Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class TimelineConverter(BaseDiagramConverter):
    """Converts Timeline Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Timeline")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        
        for event in template.data.get("events", []):
            self.add_shape(doc, "circle", event.get("x"), event.get("y"), 20, 20, 
                          event.get("label"), "#0284C7", "#0284C7")
        
        self.save_vsdx(doc)
        self.logger.info(f"Timeline saved: {self.output_path}")
