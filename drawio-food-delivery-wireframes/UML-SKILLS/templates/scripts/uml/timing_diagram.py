"""UML Timing Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class TimingDiagramConverter(BaseDiagramConverter):
    """Converts UML Timing Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Timing Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for lifeline in template.data.get("lifelines", []):
            self.add_shape(doc, "rect", lifeline.get("x"), lifeline.get("y"), 100, 60, 
                          lifeline.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        time_axis = template.data.get("timeAxis", {})
        self.add_shape(doc, "rect", time_axis.get("x"), time_axis.get("y"), 
                      time_axis.get("width"), time_axis.get("height"), "Time Axis", 
                      styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Timing Diagram saved: {self.output_path}")
