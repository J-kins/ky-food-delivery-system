"""Parse embedded JSON data from SVG template files."""

import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class ParsedTemplate:
    """Parsed SVG template with embedded JSON data."""
    svg_path: Path
    data: Dict[str, Any]
    design_tokens: Dict[str, Any]
    metadata: Dict[str, Any]


class JSONDataParser:
    """Extract and validate JSON data from SVG templates."""

    @staticmethod
    def parse_svg_template(svg_path: Path) -> ParsedTemplate:
        """Parse SVG file and extract embedded JSON data.
        
        Args:
            svg_path: Path to SVG template file
            
        Returns:
            ParsedTemplate with extracted data and metadata
            
        Raises:
            ValueError: If JSON data not found or invalid
        """
        tree = ET.parse(svg_path)
        root = tree.getroot()

        # Find script element with JSON data
        ns = {"svg": "http://www.w3.org/2000/svg"}
        json_element = None
        
        for script in root.findall(".//svg:script", ns):
            script_type = script.get("type", "")
            if "json" in script_type.lower():
                json_element = script
                break

        if json_element is None or json_element.text is None:
            raise ValueError(f"No JSON data found in SVG: {svg_path}")

        try:
            data = json.loads(json_element.text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in SVG {svg_path}: {e}")

        design_tokens = data.get("designTokens", {})
        metadata = data.get("metadata", {})

        return ParsedTemplate(
            svg_path=svg_path,
            data=data,
            design_tokens=design_tokens,
            metadata=metadata,
        )

    @staticmethod
    def validate_data(data: Dict[str, Any]) -> list[str]:
        """Validate parsed data against expected structure.
        
        Args:
            data: Parsed JSON data
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        required_fields = ["projectName", "metadata"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        if "designTokens" not in data:
            errors.append("Missing designTokens (required for dual rendering)")
        
        return errors
