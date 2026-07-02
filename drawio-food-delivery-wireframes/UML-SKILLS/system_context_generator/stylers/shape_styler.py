class ShapeBuilder:
    """Wraps Aspose.Diagram primitive creation."""
    
    @staticmethod
    def create_entity_box(diagram, x: float, y: float, width: float, height: float,
                          fill_color: str, border_color: str, 
                          text: str) -> int:
        """Create a styled entity box and return its shape ID."""
        # shape_id = diagram.add_shape(x, y, width, height, "Rectangle", 0)
        # Apply hex colors, shadows, and text blocks...
        return 1
    
    @staticmethod
    def create_system_box(diagram, x: float, y: float, width: float, height: float,
                          fill_color: str, border_color: str,
                          text: str) -> int:
        """Create the central system box with a heavy border."""
        # Implementation
        return 2
    
    @staticmethod
    def create_data_flow(diagram, source_id: int, target_id: int,
                         color: str, label: str, bidirectional: bool) -> None:
        """Route dynamic connector with orthogonal rules and labeled midpoint."""
        # Configure ConLineRouteExt for orthogonal lines
        pass
