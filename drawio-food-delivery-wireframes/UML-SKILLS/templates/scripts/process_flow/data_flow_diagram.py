"""Data Flow Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class DataFlowDiagramConverter(BaseDiagramConverter):
    """Converts Data Flow Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Data Flow Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for entity in template.data.get("entities", []):
            self.add_shape(doc, "rect", entity.get("x"), entity.get("y"), entity.get("width"), 
                          entity.get("height"), entity.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        for flow in template.data.get("dataflows", []):
            self.add_connector(doc, flow.get("from"), flow.get("to"))
        self.save_vsdx(doc)
        self.logger.info(f"Data Flow Diagram saved: {self.output_path}")
