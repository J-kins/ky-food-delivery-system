"""Organization Chart Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class OrgChartConverter(BaseDiagramConverter):
    """Converts Organization Chart to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Organization Chart")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        
        for node in template.data.get("nodes", []):
            self.add_shape(doc, "rect", node.get("x"), node.get("y"), node.get("width"), 
                          node.get("height"), node.get("title"), "#3B82F6", "#334155")
        
        for edge in template.data.get("edges", []):
            self.add_connector(doc, edge.get("from"), edge.get("to"))
        
        self.save_vsdx(doc)
        self.logger.info(f"Organization Chart saved: {self.output_path}")
