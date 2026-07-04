#!/usr/bin/env python3
"""Main orchestrator for SVG template to Visio template conversion.

This module coordinates the conversion of data-driven SVG templates to Visio template files (.vstx).
Each diagram type has its own converter, and this orchestrator manages the pipeline.

Usage:
    python main.py --input <svg_file> --output <vstx_file> --diagram <type>
    python main.py --batch <svg_folder> --output-dir <vstx_folder>
    
Output Format: .vstx (Visio Template Format)
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from project_management import (
    GanttChartConverter,
    ProjectCharterConverter,
    WBSConverter,
    RiskMatrixConverter,
)
from sitemaps import SitemapConverter
from stakeholder import (
    StakeholderMapConverter,
    PowerInterestMatrixConverter,
    InfluenceNetworkConverter,
    SalienceModelConverter,
    RACIMatrixConverter,
    StakeholderRegisterConverter,
)
from data import (
    ERDDiagramConverter,
    ConceptualDataModelConverter,
    LogicalDataModelConverter,
    PhysicalDataModelConverter,
    DataPipelineConverter,
    DataLakehouseConverter,
)

logger = logging.getLogger(__name__)

# Converter registry mapping diagram types to converter classes
CONVERTER_REGISTRY = {
    # Project Management
    "gantt-chart": GanttChartConverter,
    "gantt-resource": GanttChartConverter,
    "gantt-project": GanttChartConverter,
    "project-charter": ProjectCharterConverter,
    "wbs": WBSConverter,
    "work-breakdown-structure": WBSConverter,
    "risk-matrix": RiskMatrixConverter,
    # Sitemaps
    "sitemap": SitemapConverter,
    # Stakeholder Analysis
    "stakeholder-map": StakeholderMapConverter,
    "power-interest-matrix": PowerInterestMatrixConverter,
    "influence-network": InfluenceNetworkConverter,
    "salience-model": SalienceModelConverter,
    "raci-matrix": RACIMatrixConverter,
    "stakeholder-register": StakeholderRegisterConverter,
    # Data Models & Architecture
    "erd": ERDDiagramConverter,
    "erd-diagram": ERDDiagramConverter,
    "entity-relationship": ERDDiagramConverter,
    "conceptual-model": ConceptualDataModelConverter,
    "data-model-conceptual": ConceptualDataModelConverter,
    "logical-model": LogicalDataModelConverter,
    "data-model-logical": LogicalDataModelConverter,
    "physical-model": PhysicalDataModelConverter,
    "data-model-physical": PhysicalDataModelConverter,
    "data-pipeline": DataPipelineConverter,
    "pipeline": DataPipelineConverter,
    "data-lakehouse": DataLakehouseConverter,
    "lakehouse": DataLakehouseConverter,
}


class TemplateConverterOrchestrator:
    """Orchestrates SVG template to Visio conversion."""

    def __init__(self, verbose: bool = False):
        """Initialize orchestrator.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self._setup_logging()
        self.conversion_stats = {"success": 0, "failed": 0, "skipped": 0}

    def _setup_logging(self) -> None:
        """Configure logging."""
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def convert_file(
        self,
        svg_path: Path,
        output_path: Path,
        diagram_type: Optional[str] = None,
    ) -> bool:
        """Convert single SVG file to Visio.
        
        Args:
            svg_path: Path to SVG template
            output_path: Path for output .vsdx file
            diagram_type: Optional diagram type (auto-detected if not provided)
            
        Returns:
            True if successful, False otherwise
        """
        if not svg_path.exists():
            logger.error(f"SVG file not found: {svg_path}")
            self.conversion_stats["failed"] += 1
            return False

        # Auto-detect diagram type if not provided
        if not diagram_type:
            diagram_type = self._detect_diagram_type(svg_path)

        if not diagram_type:
            logger.warning(f"Could not detect diagram type: {svg_path}")
            self.conversion_stats["skipped"] += 1
            return False

        converter_class = CONVERTER_REGISTRY.get(diagram_type)
        if not converter_class:
            logger.error(f"Unknown diagram type: {diagram_type}")
            self.conversion_stats["failed"] += 1
            return False

        try:
            logger.info(f"Converting {svg_path.name} ({diagram_type})")
            converter = converter_class(svg_path, output_path)
            result_path = converter.convert()
            
            summary = converter.get_summary()
            logger.info(f"Conversion successful: {summary['shapes']} shapes, {summary['connectors']} connectors")
            
            self.conversion_stats["success"] += 1
            return True

        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            self.conversion_stats["failed"] += 1
            return False

    def convert_batch(
        self,
        input_dir: Path,
        output_dir: Path,
        pattern: str = "*.svg",
    ) -> Dict[str, int]:
        """Convert all SVG files in directory.
        
        Args:
            input_dir: Directory containing SVG files
            output_dir: Directory for output .vsdx files
            pattern: File pattern to match (default: *.svg)
            
        Returns:
            Conversion statistics
        """
        if not input_dir.is_dir():
            logger.error(f"Input directory not found: {input_dir}")
            return self.conversion_stats

        output_dir.mkdir(parents=True, exist_ok=True)

        svg_files = list(input_dir.glob(pattern))
        logger.info(f"Found {len(svg_files)} SVG files in {input_dir}")

        for svg_path in svg_files:
            output_path = output_dir / svg_path.stem / ".vsdx"
            self.convert_file(svg_path, output_path)

        return self.conversion_stats

    def _detect_diagram_type(self, svg_path: Path) -> Optional[str]:
        """Auto-detect diagram type from filename or content.
        
        Args:
            svg_path: Path to SVG file
            
        Returns:
            Detected diagram type or None
        """
        filename = svg_path.stem.lower()

        # Match by filename patterns
        if "gantt" in filename:
            if "resource" in filename:
                return "gantt-resource"
            elif "project" in filename:
                return "gantt-project"
            return "gantt-chart"
        elif "charter" in filename:
            return "project-charter"
        elif "wbs" in filename or "breakdown" in filename:
            return "wbs"
        elif "risk" in filename and "matrix" in filename:
            return "risk-matrix"
        elif "sitemap" in filename:
            return "sitemap"

        # Could parse SVG content to detect data type
        try:
            from base import JSONDataParser
            template = JSONDataParser.parse_svg_template(svg_path)
            chart_type = template.data.get("chartType", "").lower()
            
            if chart_type:
                # Normalize chart type to diagram type
                for diagram_type in CONVERTER_REGISTRY:
                    if diagram_type.replace("-", " ") in chart_type:
                        return diagram_type
        except Exception as e:
            logger.debug(f"Could not detect from content: {e}")

        return None

    def get_stats(self) -> Dict[str, int]:
        """Get conversion statistics.
        
        Returns:
            Dictionary with success/failed/skipped counts
        """
        total = sum(self.conversion_stats.values())
        return {
            **self.conversion_stats,
            "total": total,
        }


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert SVG templates to Visio diagrams",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert single file
  python main.py -i template.svg -o diagram.vsdx

  # Convert with type auto-detection
  python main.py -i gantt-chart.svg -o gantt.vsdx

  # Batch conversion
  python main.py --batch ./templates/svg/project-management --output-dir ./output/vsdx

  # Verbose output
  python main.py -i template.svg -o diagram.vsdx -v
        """,
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        help="Input SVG template file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output .vsdx file path",
    )
    parser.add_argument(
        "-d",
        "--diagram",
        choices=list(CONVERTER_REGISTRY.keys()),
        help="Diagram type (auto-detected if not provided)",
    )
    parser.add_argument(
        "--batch",
        type=Path,
        help="Batch convert directory of SVG files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory for batch conversion",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        default="*.svg",
        help="File pattern for batch conversion (default: *.svg)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose logging",
    )
    parser.add_argument(
        "--list-types",
        action="store_true",
        help="List supported diagram types and exit",
    )

    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point."""
    args = parse_args(argv)

    if args.list_types:
        print("Supported diagram types:")
        for dtype in sorted(CONVERTER_REGISTRY.keys()):
            print(f"  - {dtype}")
        return 0

    orchestrator = TemplateConverterOrchestrator(verbose=args.verbose)

    # Single file conversion
    if args.input and args.output:
        success = orchestrator.convert_file(args.input, args.output, args.diagram)
        return 0 if success else 1

    # Batch conversion
    if args.batch and args.output_dir:
        orchestrator.convert_batch(args.batch, args.output_dir, args.pattern)
        stats = orchestrator.get_stats()
        print(f"\nConversion complete: {stats['success']} successful, {stats['failed']} failed, {stats['skipped']} skipped")
        return 0 if stats["failed"] == 0 else 1

    print("Error: Provide either -i/-o (single file) or --batch/--output-dir (batch conversion)")
    parser = argparse.ArgumentParser()
    parse_args(["--help"])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
