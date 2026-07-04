"""UML Activity Diagram Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class ActivityDiagramConverter(BaseDiagramConverter):
    """Converts UML Activity Diagram to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering UML Activity Diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for activity in template.data.get("activities", []):
            shape_type = activity.get("type", "rect")
            self.add_shape(doc, shape_type, activity.get("x"), activity.get("y"), 
                          activity.get("width", activity.get("r")), activity.get("height", activity.get("r")), 
                          activity.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"UML Activity Diagram saved: {self.output_path}")
