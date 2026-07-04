"""Business Process Model Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class BusinessProcessModelConverter(BaseDiagramConverter):
    """Converts Business Process Model to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Business Process Model diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for swimlane in template.data.get("swimlanes", []):
            self.add_shape(doc, "rect", swimlane.get("x"), swimlane.get("y"), swimlane.get("width"), 
                          swimlane.get("height"), swimlane.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        for activity in template.data.get("activities", []):
            self.add_shape(doc, "rect", activity.get("x"), activity.get("y"), activity.get("width"), 
                          activity.get("height"), activity.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"Business Process Model diagram saved: {self.output_path}")
