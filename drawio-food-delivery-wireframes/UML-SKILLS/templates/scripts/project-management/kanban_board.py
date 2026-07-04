"""Kanban Board Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class KanbanBoardConverter(BaseDiagramConverter):
    """Converts Kanban Board to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Kanban Board")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        
        for col in template.data.get("columns", []):
            self.add_shape(doc, "rect", col.get("x"), col.get("y"), col.get("width"), 
                          col.get("height"), col.get("name"), "#f1f5f9", "#334155")
        
        for card in template.data.get("cards", []):
            self.add_shape(doc, "rect", card.get("x", 0), card.get("y", 0), 100, 60, 
                          card.get("title"), "#FFFFFF", "#334155")
        
        self.save_vsdx(doc)
        self.logger.info(f"Kanban Board saved: {self.output_path}")
