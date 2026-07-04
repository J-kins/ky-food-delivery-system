"""Deployment Architecture Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class DeploymentArchitectureConverter(BaseDiagramConverter):
    """Converts Deployment Architecture to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Deployment Architecture diagram")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        stages = template.data.get("stages", [])
        for i, stage in enumerate(stages):
            self.add_shape(doc, "rect", stage.get("x"), stage.get("y"), stage.get("width"), 
                          stage.get("height"), stage.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
            if i < len(stages) - 1:
                self.add_connector(doc, stage.get("id"), stages[i+1].get("id"))
        self.save_vsdx(doc)
        self.logger.info(f"Deployment Architecture diagram saved: {self.output_path}")
