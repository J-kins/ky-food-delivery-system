"""Business Process Analysis Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class BusinessProcessAnalysisConverter(BaseDiagramConverter):
    """Converts Business Process Analysis to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Business Process Analysis diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for step in template.data.get("steps", []):
            self.add_shape(doc, "rect", step.get("x"), step.get("y"), step.get("width"), 
                          step.get("height"), step.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"Business Process Analysis diagram saved: {self.output_path}")
