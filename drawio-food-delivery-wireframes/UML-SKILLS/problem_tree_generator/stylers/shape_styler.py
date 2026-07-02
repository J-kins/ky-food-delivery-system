class ShapeBuilder:
    """Creates styled shapes for the diagram via Aspose."""
    
    @staticmethod
    def create_rounded_rectangle(diagram, x: float, y: float, width: float, height: float,
                                  fill_color: str, border_color: str, 
                                  text: str, font_size: int = 10,
                                  corner_radius: int = 8,
                                  shadow: bool = True) -> int:
        """Create a styled rounded rectangle shape and return its internal ID."""
        # Implementation using Aspose.Diagram API
        # e.g. shape_id = diagram.add_shape(x, y, width, height, "Rectangle", 0)
        # shape = diagram.pages[0].shapes.get_shape(shape_id)
        # shape.fill.fill_foregnd.value = fill_color
        # shape.line.line_color.value = border_color
        pass
    
    @staticmethod
    def create_connector(diagram, source_id: int, target_id: int,
                         color: str = "#666666",
                         label: str = "") -> None:
        """Create a styled dynamic connector with arrowhead."""
        # shape = diagram.add_shape(...) 
        # diagram.pages[0].connect_shapes_via_connector(...)
        pass
