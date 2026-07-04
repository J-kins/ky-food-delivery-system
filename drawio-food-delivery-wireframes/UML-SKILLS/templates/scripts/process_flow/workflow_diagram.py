"""Workflow Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class WorkflowDiagramConverter(BaseDiagramConverter):
    """Converts Workflow Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Workflow Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for state in template.data.get("states", []):
            self.add_shape(doc, "rect", state.get("x"), state.get("y"), state.get("width"), 
                          state.get("height"), state.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        for transition in template.data.get("transitions", []):
            self.add_connector(doc, transition.get("from"), transition.get("to"))
        self.save_vsdx(doc)
        self.logger.info(f"Workflow Diagram saved: {self.output_path}")
