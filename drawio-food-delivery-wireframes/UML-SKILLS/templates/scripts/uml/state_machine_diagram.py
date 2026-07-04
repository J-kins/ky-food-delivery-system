"""UML State Machine Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class StateMachineDiagramConverter(BaseDiagramConverter):
    """Converts UML State Machine Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML State Machine Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for state in template.data.get("states", []):
            self.add_shape(doc, "circle", state.get("x"), state.get("y"), state.get("rx"), 
                          state.get("ry"), state.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        for trans in template.data.get("transitions", []):
            self.add_connector(doc, trans.get("from"), trans.get("to"))
        self.save_vsdx(doc)
        self.logger.info(f"UML State Machine Diagram saved: {self.output_path}")
