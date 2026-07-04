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
from cloud import (
    AWSArchitectureConverter,
    AzureArchitectureConverter,
    GCPArchitectureConverter,
    MultiCloudArchitectureConverter,
    ServerlessArchitectureConverter,
    CloudMigrationConverter,
    CloudCostOptimizationConverter,
)
from devops import (
    CICDPipelineConverter,
    DevOpsArchitectureConverter,
    GitOpsArchitectureConverter,
    ObservabilityArchitectureConverter,
    InfrastructureAsCodeConverter,
    ServiceMeshArchitectureConverter,
)
from gis import (
    GISArchitectureConverter,
    GeospatialDataModelConverter,
    MapDesignConverter,
    GeoprocessingWorkflowConverter,
    SpatialDataFlowConverter,
)
from infrastructure import (
    InfrastructureArchitectureConverter,
    NetworkArchitectureConverter,
    CloudInfrastructureConverter,
    DeploymentArchitectureConverter,
    ContainerArchitectureConverter,
    KubernetesArchitectureConverter,
    HighAvailabilityArchitectureConverter,
    DisasterRecoveryArchitectureConverter,
)
from process_flow import (
    BusinessProcessModelConverter,
    DataFlowDiagramConverter,
    BusinessProcessAnalysisConverter,
    ProcessFlowDiagramConverter,
    WorkflowDiagramConverter,
    ValueStreamMapConverter,
)
from uml import (
    ClassDiagramConverter,
    ObjectDiagramConverter,
    ComponentDiagramConverter,
    DeploymentDiagramConverter,
    PackageDiagramConverter,
    CompositeStructureDiagramConverter,
    UseCaseDiagramConverter,
    SequenceDiagramConverter,
    ActivityDiagramConverter,
    StateMachineDiagramConverter,
    CommunicationDiagramConverter,
    InteractionOverviewDiagramConverter,
    TimingDiagramConverter,
    ProfileDiagramConverter,
)
from project_management import (
    KanbanBoardConverter,
    TimelineConverter,
)
from organization import (
    OrgChartConverter,
    SWOTMatrixConverter,
)
from misc import (
    ProblemTreeConverter,
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
    "kanban-board": KanbanBoardConverter,
    "kanban": KanbanBoardConverter,
    "timeline": TimelineConverter,
    "simple-timeline": TimelineConverter,
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
    # Cloud Architecture
    "aws": AWSArchitectureConverter,
    "aws-architecture": AWSArchitectureConverter,
    "azure": AzureArchitectureConverter,
    "azure-architecture": AzureArchitectureConverter,
    "gcp": GCPArchitectureConverter,
    "gcp-architecture": GCPArchitectureConverter,
    "google-cloud": GCPArchitectureConverter,
    "multi-cloud": MultiCloudArchitectureConverter,
    "multi-cloud-architecture": MultiCloudArchitectureConverter,
    "serverless": ServerlessArchitectureConverter,
    "serverless-architecture": ServerlessArchitectureConverter,
    "cloud-migration": CloudMigrationConverter,
    "migration": CloudMigrationConverter,
    "cloud-cost-optimization": CloudCostOptimizationConverter,
    "cost-optimization": CloudCostOptimizationConverter,
    # DevOps
    "cicd": CICDPipelineConverter,
    "cicd-pipeline": CICDPipelineConverter,
    "ci-cd": CICDPipelineConverter,
    "devops": DevOpsArchitectureConverter,
    "devops-architecture": DevOpsArchitectureConverter,
    "gitops": GitOpsArchitectureConverter,
    "gitops-architecture": GitOpsArchitectureConverter,
    "observability": ObservabilityArchitectureConverter,
    "observability-architecture": ObservabilityArchitectureConverter,
    "iac": InfrastructureAsCodeConverter,
    "infrastructure-as-code": InfrastructureAsCodeConverter,
    "infrastructure-code": InfrastructureAsCodeConverter,
    "service-mesh": ServiceMeshArchitectureConverter,
    "service-mesh-architecture": ServiceMeshArchitectureConverter,
    # GIS (Geographic Information Systems)
    "gis": GISArchitectureConverter,
    "gis-architecture": GISArchitectureConverter,
    "geospatial": GeospatialDataModelConverter,
    "geospatial-data-model": GeospatialDataModelConverter,
    "map-design": MapDesignConverter,
    "map": MapDesignConverter,
    "geoprocessing": GeoprocessingWorkflowConverter,
    "geoprocessing-workflow": GeoprocessingWorkflowConverter,
    "spatial-data-flow": SpatialDataFlowConverter,
    "data-flow": SpatialDataFlowConverter,
    # Infrastructure
    "infrastructure": InfrastructureArchitectureConverter,
    "infrastructure-architecture": InfrastructureArchitectureConverter,
    "network": NetworkArchitectureConverter,
    "network-architecture": NetworkArchitectureConverter,
    "cloud-infrastructure": CloudInfrastructureConverter,
    "cloud-arch": CloudInfrastructureConverter,
    "deployment": DeploymentArchitectureConverter,
    "deployment-architecture": DeploymentArchitectureConverter,
    "container": ContainerArchitectureConverter,
    "container-architecture": ContainerArchitectureConverter,
    "kubernetes": KubernetesArchitectureConverter,
    "kubernetes-architecture": KubernetesArchitectureConverter,
    "k8s": KubernetesArchitectureConverter,
    "high-availability": HighAvailabilityArchitectureConverter,
    "ha-architecture": HighAvailabilityArchitectureConverter,
    "disaster-recovery": DisasterRecoveryArchitectureConverter,
    "dr-architecture": DisasterRecoveryArchitectureConverter,
    # Process Flow & Workflow
    "business-process-model": BusinessProcessModelConverter,
    "bpm": BusinessProcessModelConverter,
    "process-model": BusinessProcessModelConverter,
    "data-flow-diagram": DataFlowDiagramConverter,
    "dfd": DataFlowDiagramConverter,
    "business-process-analysis": BusinessProcessAnalysisConverter,
    "bpa": BusinessProcessAnalysisConverter,
    "process-flow-diagram": ProcessFlowDiagramConverter,
    "pfd": ProcessFlowDiagramConverter,
    "workflow-diagram": WorkflowDiagramConverter,
    "workflow": WorkflowDiagramConverter,
    "value-stream-map": ValueStreamMapConverter,
    "vsm": ValueStreamMapConverter,
    "value-stream": ValueStreamMapConverter,
    # UML Diagrams
    "uml-class-diagram": ClassDiagramConverter,
    "class-diagram": ClassDiagramConverter,
    "uml-class": ClassDiagramConverter,
    "uml-object-diagram": ObjectDiagramConverter,
    "object-diagram": ObjectDiagramConverter,
    "uml-object": ObjectDiagramConverter,
    "uml-component-diagram": ComponentDiagramConverter,
    "component-diagram": ComponentDiagramConverter,
    "uml-component": ComponentDiagramConverter,
    "uml-deployment-diagram": DeploymentDiagramConverter,
    "deployment-diagram": DeploymentDiagramConverter,
    "uml-deployment": DeploymentDiagramConverter,
    "uml-package-diagram": PackageDiagramConverter,
    "package-diagram": PackageDiagramConverter,
    "uml-package": PackageDiagramConverter,
    "uml-composite-structure": CompositeStructureDiagramConverter,
    "composite-structure": CompositeStructureDiagramConverter,
    "uml-composite": CompositeStructureDiagramConverter,
    "uml-use-case-diagram": UseCaseDiagramConverter,
    "use-case-diagram": UseCaseDiagramConverter,
    "usecase-diagram": UseCaseDiagramConverter,
    "uml-use-case": UseCaseDiagramConverter,
    "uml-sequence-diagram": SequenceDiagramConverter,
    "sequence-diagram": SequenceDiagramConverter,
    "uml-sequence": SequenceDiagramConverter,
    "uml-activity-diagram": ActivityDiagramConverter,
    "activity-diagram": ActivityDiagramConverter,
    "uml-activity": ActivityDiagramConverter,
    "uml-state-machine": StateMachineDiagramConverter,
    "state-machine-diagram": StateMachineDiagramConverter,
    "state-machine": StateMachineDiagramConverter,
    "uml-state": StateMachineDiagramConverter,
    "uml-communication-diagram": CommunicationDiagramConverter,
    "communication-diagram": CommunicationDiagramConverter,
    "uml-communication": CommunicationDiagramConverter,
    "uml-interaction-overview": InteractionOverviewDiagramConverter,
    "interaction-overview-diagram": InteractionOverviewDiagramConverter,
    "interaction-overview": InteractionOverviewDiagramConverter,
    "uml-timing-diagram": TimingDiagramConverter,
    "timing-diagram": TimingDiagramConverter,
    "uml-timing": TimingDiagramConverter,
    "uml-profile-diagram": ProfileDiagramConverter,
    "profile-diagram": ProfileDiagramConverter,
    "uml-profile": ProfileDiagramConverter,
    # Organization
    "org-chart": OrgChartConverter,
    "organization-chart": OrgChartConverter,
    "organizational-chart": OrgChartConverter,
    "swot-matrix": SWOTMatrixConverter,
    "swot": SWOTMatrixConverter,
    # Miscellaneous
    "problem-tree": ProblemTreeConverter,
    "problem-tree-diagram": ProblemTreeConverter,
    "problem-analysis": ProblemTreeConverter,
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
        # Cloud Architecture Detection
        elif "aws" in filename:
            return "aws-architecture"
        elif "azure" in filename:
            return "azure-architecture"
        elif "gcp" in filename or "google" in filename:
            return "gcp-architecture"
        elif "multi-cloud" in filename or "multicloud" in filename:
            return "multi-cloud-architecture"
        elif "serverless" in filename:
            return "serverless-architecture"
        elif "migration" in filename:
            return "cloud-migration"
        elif "cost" in filename and "optimization" in filename:
            return "cloud-cost-optimization"
        # DevOps Detection
        elif "cicd" in filename or "ci-cd" in filename:
            return "cicd-pipeline"
        elif "devops" in filename and "architecture" in filename:
            return "devops-architecture"
        elif "gitops" in filename:
            return "gitops-architecture"
        elif "observability" in filename:
            return "observability-architecture"
        elif "infrastructure" in filename and "code" in filename:
            return "infrastructure-as-code"
        elif "service" in filename and "mesh" in filename:
            return "service-mesh-architecture"
        # GIS Detection
        elif "gis" in filename and "architecture" in filename:
            return "gis-architecture"
        elif "gis" in filename:
            return "gis-architecture"
        elif "geospatial" in filename:
            return "geospatial-data-model"
        elif "map" in filename and "design" in filename:
            return "map-design"
        elif "geoprocessing" in filename:
            return "geoprocessing-workflow"
        elif "spatial" in filename and "flow" in filename:
            return "spatial-data-flow"
        # Infrastructure Detection
        elif "infrastructure" in filename and "architecture" in filename:
            return "infrastructure-architecture"
        elif "infrastructure" in filename:
            return "infrastructure-architecture"
        elif "network" in filename and "architecture" in filename:
            return "network-architecture"
        elif "cloud" in filename and ("architecture" in filename or "infra" in filename):
            return "cloud-infrastructure"
        elif "deployment" in filename and "architecture" in filename:
            return "deployment-architecture"
        elif "container" in filename and "architecture" in filename:
            return "container-architecture"
        elif "kubernetes" in filename or "k8s" in filename:
            return "kubernetes-architecture"
        elif "high-availability" in filename or "ha-architecture" in filename:
            return "high-availability"
        elif "disaster-recovery" in filename or "dr-architecture" in filename:
            return "disaster-recovery"
        # Process Flow Detection
        elif "business-process-model" in filename or "bpm" in filename:
            return "business-process-model"
        elif "data-flow-diagram" in filename or "dfd" in filename:
            return "data-flow-diagram"
        elif "business-process-analysis" in filename or "bpa" in filename:
            return "business-process-analysis"
        elif "process-flow-diagram" in filename or "pfd" in filename:
            return "process-flow-diagram"
        elif "workflow" in filename and "diagram" in filename:
            return "workflow-diagram"
        elif "value-stream-map" in filename or "vsm" in filename:
            return "value-stream-map"
        # UML Detection
        elif "uml" in filename and "class" in filename:
            return "uml-class-diagram"
        elif "uml" in filename and "object" in filename:
            return "uml-object-diagram"
        elif "uml" in filename and "component" in filename:
            return "uml-component-diagram"
        elif "uml" in filename and "deployment" in filename:
            return "uml-deployment-diagram"
        elif "uml" in filename and "package" in filename:
            return "uml-package-diagram"
        elif "uml" in filename and "composite" in filename:
            return "uml-composite-structure"
        elif "uml" in filename and ("use-case" in filename or "usecase" in filename):
            return "uml-use-case-diagram"
        elif "uml" in filename and "sequence" in filename:
            return "uml-sequence-diagram"
        elif "uml" in filename and "activity" in filename:
            return "uml-activity-diagram"
        elif "uml" in filename and ("state-machine" in filename or "state_machine" in filename):
            return "uml-state-machine"
        elif "uml" in filename and "communication" in filename:
            return "uml-communication-diagram"
        elif "uml" in filename and "interaction-overview" in filename:
            return "uml-interaction-overview"
        elif "uml" in filename and "timing" in filename:
            return "uml-timing-diagram"
        elif "uml" in filename and "profile" in filename:
            return "uml-profile-diagram"

        # Could parse SVG content to detect data type
        try:
            from base import JSONDataParser
            template = JSONDataParser.parse_svg_template(svg_path)
            chart_type = template.data.get("chartType", "").lower()
            title = template.data.get("metadata", {}).get("title", "").lower()
            
            if chart_type:
                # Normalize chart type to diagram type
                for diagram_type in CONVERTER_REGISTRY:
                    if diagram_type.replace("-", " ") in chart_type:
                        return diagram_type
            
            # Check title for cloud architecture keywords
            if "aws" in title:
                return "aws-architecture"
            elif "azure" in title:
                return "azure-architecture"
            elif "gcp" in title or "google cloud" in title:
                return "gcp-architecture"
            elif "multi-cloud" in title:
                return "multi-cloud-architecture"
            elif "serverless" in title:
                return "serverless-architecture"
            elif "migration" in title:
                return "cloud-migration"
            elif "cost optimization" in title:
                return "cloud-cost-optimization"
            elif "ci/cd" in title or "cicd" in title:
                return "cicd-pipeline"
            elif "devops" in title and "architecture" in title:
                return "devops-architecture"
            elif "gitops" in title:
                return "gitops-architecture"
            elif "observability" in title:
                return "observability-architecture"
            elif "infrastructure as code" in title:
                return "infrastructure-as-code"
            elif "service mesh" in title:
                return "service-mesh-architecture"
            elif "gis" in title and "architecture" in title:
                return "gis-architecture"
            elif "geospatial" in title:
                return "geospatial-data-model"
            elif "map" in title and "design" in title:
                return "map-design"
            elif "geoprocessing" in title:
                return "geoprocessing-workflow"
            elif "spatial" in title and "flow" in title:
                return "spatial-data-flow"
            elif "infrastructure" in title and "architecture" in title:
                return "infrastructure-architecture"
            elif "network" in title and "architecture" in title:
                return "network-architecture"
            elif "cloud" in title and "infrastructure" in title:
                return "cloud-infrastructure"
            elif "deployment" in title and "architecture" in title:
                return "deployment-architecture"
            elif "container" in title and "architecture" in title:
                return "container-architecture"
            elif "kubernetes" in title or "k8s" in title:
                return "kubernetes-architecture"
            elif "high availability" in title:
                return "high-availability"
            elif "disaster recovery" in title:
                return "disaster-recovery"
            elif "business process model" in title:
                return "business-process-model"
            elif "data flow diagram" in title:
                return "data-flow-diagram"
            elif "business process analysis" in title:
                return "business-process-analysis"
            elif "process flow diagram" in title:
                return "process-flow-diagram"
            elif "workflow" in title and "diagram" in title:
                return "workflow-diagram"
            elif "value stream" in title:
                return "value-stream-map"
            elif "uml" in title and "class" in title:
                return "uml-class-diagram"
            elif "uml" in title and "object" in title:
                return "uml-object-diagram"
            elif "uml" in title and "component" in title:
                return "uml-component-diagram"
            elif "uml" in title and "deployment" in title:
                return "uml-deployment-diagram"
            elif "uml" in title and "package" in title:
                return "uml-package-diagram"
            elif "uml" in title and "composite" in title:
                return "uml-composite-structure"
            elif "uml" in title and "use case" in title:
                return "uml-use-case-diagram"
            elif "uml" in title and "sequence" in title:
                return "uml-sequence-diagram"
            elif "uml" in title and "activity" in title:
                return "uml-activity-diagram"
            elif "uml" in title and "state machine" in title:
                return "uml-state-machine"
            elif "uml" in title and "communication" in title:
                return "uml-communication-diagram"
            elif "uml" in title and "interaction overview" in title:
                return "uml-interaction-overview"
            elif "uml" in title and "timing" in title:
                return "uml-timing-diagram"
            elif "uml" in title and "profile" in title:
                return "uml-profile-diagram"
            elif "kanban" in title:
                return "kanban-board"
            elif "timeline" in title and "gantt" not in title:
                return "timeline"
            elif "org" in title and "chart" in title:
                return "org-chart"
            elif "organization" in title and "chart" in title:
                return "org-chart"
            elif "swot" in title:
                return "swot-matrix"
            elif "problem tree" in title or "problem-tree" in title:
                return "problem-tree"
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
