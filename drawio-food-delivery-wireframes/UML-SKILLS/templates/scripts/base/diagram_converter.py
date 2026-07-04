"""Base diagram converter from SVG templates to Visio."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

from .json_parser import JSONDataParser, ParsedTemplate
from .visio_builder import VisioBuilder

logger = logging.getLogger(__name__)


class BaseDiagramConverter(ABC):
    """Abstract base class for SVG template to Visio conversion."""

    def __init__(self, svg_path: Path, output_path: Path):
        """Initialize converter.
        
        Args:
            svg_path: Path to SVG template
            output_path: Path for output .vsdx file
        """
        self.svg_path = svg_path
        self.output_path = output_path
        self.template: Optional[ParsedTemplate] = None
        self.builder: Optional[VisioBuilder] = None

    def convert(self) -> Path:
        """Execute complete conversion pipeline.
        
        Returns:
            Path to generated Visio file
        """
        logger.info(f"Converting {self.svg_path.name} to Visio")

        # Parse template
        self.template = JSONDataParser.parse_svg_template(self.svg_path)

        # Validate
        errors = JSONDataParser.validate_data(self.template.data)
        if errors:
            raise ValueError(f"Data validation failed: {', '.join(errors)}")

        logger.debug(f"Parsed template: {self.template.data.get('projectName', 'Unknown')}")

        # Build diagram
        self.builder = VisioBuilder(
            self.output_path,
            diagram_name=self.template.data.get("projectName", "Diagram"),
        )

        # Render-specific conversion
        self.render_diagram()

        # Generate output
        result_path = self.builder.build()
        logger.info(f"Conversion complete: {result_path}")
        return result_path

    @abstractmethod
    def render_diagram(self) -> None:
        """Render diagram-specific content.
        
        Subclasses must implement diagram-specific rendering logic.
        Template and builder are available as instance variables.
        """
        pass

    def get_design_tokens(self, mode: str = "lightMode") -> Dict[str, str]:
        """Get design tokens for rendering mode.
        
        Args:
            mode: 'lightMode' or 'darkMode'
            
        Returns:
            Dictionary of design tokens
        """
        if not self.template:
            return {}
        return self.template.design_tokens.get(mode, {})

    def get_data(self) -> Dict[str, Any]:
        """Get parsed template data.
        
        Returns:
            Parsed JSON data from template
        """
        if not self.template:
            return {}
        return self.template.data

    def get_summary(self) -> Dict[str, Any]:
        """Get conversion summary.
        
        Returns:
            Dictionary with conversion statistics
        """
        if not self.builder:
            return {"status": "not_built"}
        return {
            "diagram": self.template.data.get("projectName") if self.template else "Unknown",
            "output_path": str(self.output_path),
            **self.builder.get_summary(),
        }
