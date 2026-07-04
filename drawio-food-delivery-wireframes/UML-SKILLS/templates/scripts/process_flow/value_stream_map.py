"""Value Stream Map Converter"""
from pathlib import Path
from base import BaseDiagramConverter, JSONDataParser

class ValueStreamMapConverter(BaseDiagramConverter):
    """Converts Value Stream Map to Visio format."""
    def render_diagram(self) -> None:
        self.logger.info("Rendering Value Stream Map")
        template = JSONDataParser.parse_svg_template(self.svg_path)
        doc = self.create_vsdx_document(title=template.metadata.get("title"), creator=template.metadata.get("projectName"))
        styling = template.config.get("styling", {})
        for supplier in template.data.get("suppliers", []):
            self.add_shape(doc, "rect", supplier.get("x"), supplier.get("y"), supplier.get("width"), 
                          supplier.get("height"), supplier.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        for process in template.data.get("processes", []):
            self.add_shape(doc, "rect", process.get("x"), process.get("y"), process.get("width"), 
                          process.get("height"), process.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        for customer in template.data.get("customers", []):
            self.add_shape(doc, "rect", customer.get("x"), customer.get("y"), customer.get("width"), 
                          customer.get("height"), customer.get("name"), styling.get("fillColor"), styling.get("strokeColor"))
        self.save_vsdx(doc)
        self.logger.info(f"Value Stream Map saved: {self.output_path}")
