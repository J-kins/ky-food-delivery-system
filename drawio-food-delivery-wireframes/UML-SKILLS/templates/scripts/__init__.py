"""SVG Template to Visio Diagram Converter.

A modular system for converting data-driven SVG templates to Visio diagrams (.vsdx).

Architecture:
- base/: Core converter classes and utilities
- project-management/: Converters for PM diagrams (Gantt, Charter, WBS, Risk Matrix)
- sitemaps/: Converters for sitemap diagrams
- main.py: Orchestrator for coordinating conversions

Each SVG template contains embedded JSON data that drives the conversion,
ensuring the same data can be rendered both in web browsers and Visio.
"""

__version__ = "1.0.0"
__author__ = "SVG Template Converter"

from base import BaseDiagramConverter, JSONDataParser, VisioBuilder

__all__ = [
    "BaseDiagramConverter",
    "JSONDataParser",
    "VisioBuilder",
]
