"""Process Flow Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class ProcessFlowDiagramConverter(BaseDiagramConverter):
    """Converts Process Flow Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Process Flow Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        steps = template.data.get("steps", [])
        for i, step in enumerate(steps):
            self.add_shape(doc, "rect", step.get("x"), step.get("y"), step.get("width"), 
                          step.get("height"), step.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
            if i < len(steps) - 1:
                self.add_connector(doc, step.get("id"), steps[i+1].get("id"))
        self.save_vsdx(doc)
        self.logger.info(f"Process Flow Diagram saved: {self.output_path}")
