"""
Catalog of blank diagram template SVGs (86 templates).

Run: python scripts/generate_templates.py
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

# PrimeReact Lara tokens — aligned with stencils/svg/shape_catalog.py
STYLE = {
    "primary": "#3B82F6",
    "primary_tint": "#EFF6FF",
    "surface_0": "#ffffff",
    "surface_50": "#f8fafc",
    "surface_100": "#f1f5f9",
    "surface_200": "#e2e8f0",
    "surface_700": "#334155",
    "text_muted": "#64748b",
    "placeholder_stroke": "#94a3b8",
    "guide_stroke": "#cbd5e1",
    "border_radius": 6,
    "font_family": "Inter, system-ui, -apple-system, Segoe UI, sans-serif",
}

CANVAS = {"width": 1920, "height": 1080, "viewbox": "0 0 1920 1080"}


@dataclass(frozen=True)
class Template:
    num: int
    id: str
    title: str
    category: str
    layout: str
    description: str = ""
    layout_config: Tuple[str, ...] = ()

    @property
    def filename(self) -> str:
        return f"{self.num:02d}-{self.id}-template.svg"

    @property
    def output_path(self) -> str:
        return f"{self.category}/{self.filename}"


def _t(
    num: int,
    slug: str,
    title: str,
    category: str,
    layout: str,
    description: str = "",
    layout_config: Tuple[str, ...] = (),
) -> Template:
    return Template(num, slug, title, category, layout, description, layout_config)


def all_templates() -> List[Template]:
    return [
        # UML (14)
        _t(1, "uml-class-diagram", "UML Class Diagram", "uml", "class_diagram",
           "3-class layout with relationship guides and multiplicity placeholders"),
        _t(2, "uml-object-diagram", "UML Object Diagram", "uml", "object_diagram",
           "3-object layout with link placeholders"),
        _t(3, "uml-component-diagram", "UML Component Diagram", "uml", "component_diagram",
           "4-component layout with interface ports"),
        _t(4, "uml-deployment-diagram", "UML Deployment Diagram", "uml", "deployment_diagram",
           "Node layout with artifact placeholders"),
        _t(5, "uml-package-diagram", "UML Package Diagram", "uml", "package_diagram",
           "Package folders with dependency spaces"),
        _t(6, "uml-composite-structure", "UML Composite Structure Diagram", "uml", "composite_structure",
           "Outer part with internal sub-parts"),
        _t(7, "uml-use-case-diagram", "UML Use Case Diagram", "uml", "use_case_diagram",
           "System boundary, actors, and use case ovals"),
        _t(8, "uml-sequence-diagram", "UML Sequence Diagram", "uml", "sequence_diagram",
           "Lifelines, activation bars, message spaces"),
        _t(9, "uml-activity-diagram", "UML Activity Diagram", "uml", "activity_diagram",
           "Swimlanes with action and decision placeholders"),
        _t(10, "uml-state-machine", "UML State Machine Diagram", "uml", "state_machine",
            "States and transition layout"),
        _t(11, "uml-communication-diagram", "UML Communication Diagram", "uml", "communication_diagram",
            "Objects with numbered message links"),
        _t(12, "uml-interaction-overview", "UML Interaction Overview Diagram", "uml", "interaction_overview",
            "Activity nodes referencing interaction fragments"),
        _t(13, "uml-timing-diagram", "UML Timing Diagram", "uml", "timing_diagram",
            "Lifelines with state timeline tracks"),
        _t(14, "uml-profile-diagram", "UML Profile Diagram", "uml", "profile_diagram",
            "Stereotypes and metaclass layout"),
        # Architecture (16)
        _t(15, "enterprise-architecture", "Enterprise Architecture", "architecture", "layered_stack",
           "4-layer enterprise stack", ("Business", "Data", "Application", "Technology")),
        _t(16, "business-capability-map", "Business Capability Map", "architecture", "tier_columns",
           "Tiered capability columns", ("Strategic", "Core", "Supporting")),
        _t(17, "application-landscape", "Application Landscape", "architecture", "grid_blocks",
           "Application system grid", ("App A", "App B", "App C", "App D", "App E", "App F")),
        _t(18, "system-architecture", "System Architecture", "architecture", "service_blocks",
           "Component and service layout"),
        _t(19, "layered-architecture", "Layered Architecture", "architecture", "layered_stack",
           "4-layer stack", ("Presentation", "Business", "Data", "Integration")),
        _t(20, "microservices-architecture", "Microservices Architecture", "architecture", "microservices",
           "API gateway and service mesh"),
        _t(21, "event-driven-architecture", "Event-Driven Architecture", "architecture", "event_driven",
           "Producer, broker, consumer flow"),
        _t(22, "hexagonal-architecture", "Hexagonal Architecture", "architecture", "hexagonal",
           "Domain core with ports and adapters"),
        _t(23, "clean-architecture", "Clean Architecture", "architecture", "concentric",
           "Concentric rings", ("Entities", "Use Cases", "Controllers", "Frameworks")),
        _t(24, "c4-system-context", "C4 System Context", "architecture", "c4_context",
           "System centre with users and external systems"),
        _t(25, "c4-container-diagram", "C4 Container Diagram", "architecture", "c4_container",
           "Containers inside system boundary"),
        _t(26, "c4-component-diagram", "C4 Component Diagram", "architecture", "c4_component",
           "Components inside a container"),
        _t(27, "solution-architecture", "Solution Architecture", "architecture", "solution_blocks",
           "End-to-end solution layout"),
        _t(28, "integration-architecture", "Integration Architecture", "architecture", "hub_spoke",
           "ESB / API hub with integrations", ("Integration Hub",)),
        _t(29, "data-architecture", "Data Architecture", "architecture", "layered_flow",
           "Data flow layers", ("Ingest", "Process", "Store", "Consume")),
        _t(30, "security-architecture", "Security Architecture", "architecture", "security_zones",
           "Security zones and controls"),
        # Infrastructure (8)
        _t(31, "infrastructure-architecture", "Infrastructure Architecture", "infrastructure", "infra_blocks",
           "Servers, storage, and network"),
        _t(32, "network-architecture", "Network Architecture", "infrastructure", "network_topology",
           "Router, switch, firewall topology"),
        _t(33, "cloud-architecture", "Cloud Architecture", "infrastructure", "cloud_vpc",
           "VPC, region, and availability zones"),
        _t(34, "deployment-architecture", "Deployment Architecture", "infrastructure", "deployment_envs",
           "Dev, staging, production environments"),
        _t(35, "container-architecture", "Container Architecture", "infrastructure", "container_cluster",
           "Cluster, pods, and services"),
        _t(36, "kubernetes-architecture", "Kubernetes Architecture", "infrastructure", "kubernetes",
           "Control plane and worker nodes"),
        _t(37, "high-availability-architecture", "High Availability Architecture", "infrastructure", "ha_active_standby",
           "Active, standby, and failover paths"),
        _t(38, "disaster-recovery-architecture", "Disaster Recovery Architecture", "infrastructure", "dr_sites",
           "Production and DR site layout"),
        # Project management (12)
        _t(39, "project-charter", "Project Charter", "project-management", "charter_sections",
           "Charter document sections"),
        _t(40, "work-breakdown-structure", "Work Breakdown Structure", "project-management", "wbs_tree",
           "4-level hierarchical WBS"),
        _t(41, "gantt-chart", "Gantt Chart", "project-management", "gantt",
           "Task list and timeline grid"),
        _t(42, "milestone-chart", "Milestone Chart", "project-management", "milestone_timeline",
           "Timeline with milestone markers"),
        _t(43, "roadmap-diagram", "Roadmap Diagram", "project-management", "roadmap",
           "Phases, timeline, and milestones"),
        _t(44, "pert-chart", "PERT Chart", "project-management", "pert_network",
           "Activity node network"),
        _t(45, "critical-path-diagram", "Critical Path Diagram", "project-management", "cpm_network",
           "CPM nodes with critical path highlight"),
        _t(46, "risk-matrix", "Risk Matrix", "project-management", "risk_matrix",
           "5×5 probability × impact matrix"),
        _t(47, "risk-heat-map", "Risk Heat Map", "project-management", "heat_map",
           "Colour-coded risk cells"),
        _t(48, "threat-tree", "Threat Tree", "project-management", "threat_tree",
           "Root, branches, and leaf threats"),
        _t(49, "resource-allocation-matrix", "Resource Allocation Matrix", "project-management", "allocation_matrix",
           "Resource × task grid"),
        _t(50, "team-structure-diagram", "Team Structure Diagram", "project-management", "org_chart",
           "Org chart with reporting lines"),
        # Stakeholder (6)
        _t(51, "stakeholder-map", "Stakeholder Map", "stakeholder", "stakeholder_map",
           "Central system with surrounding stakeholders"),
        _t(52, "power-interest-matrix", "Power–Interest Matrix", "stakeholder", "quadrant_matrix",
           "2×2 power vs interest grid"),
        _t(53, "influence-network-diagram", "Influence Network Diagram", "stakeholder", "influence_network",
           "Stakeholder nodes and influence arrows"),
        _t(54, "salience-model", "Salience Model", "stakeholder", "venn_three",
           "Power, legitimacy, urgency Venn"),
        _t(55, "raci-matrix", "RACI Matrix", "stakeholder", "raci_matrix",
           "Tasks × roles RACI grid"),
        _t(56, "stakeholder-register", "Stakeholder Register", "stakeholder", "register_table",
           "Stakeholder register columns"),
        # Process & flow (6)
        _t(57, "business-process-model", "Business Process Model", "process-flow", "bpmn_swimlanes",
           "BPMN swimlanes, tasks, gateways"),
        _t(58, "data-flow-diagram", "Data Flow Diagram", "process-flow", "dfd",
           "External entities, processes, data stores"),
        _t(59, "business-process-analysis", "Business Process Analysis", "process-flow", "side_by_side",
           "As-Is / To-Be process columns"),
        _t(60, "process-flow-diagram", "Process Flow Diagram", "process-flow", "process_flow",
           "Steps, decisions, start/end"),
        _t(61, "workflow-diagram", "Workflow Diagram", "process-flow", "workflow_swimlanes",
           "Workflow activities in swimlanes"),
        _t(62, "value-stream-map", "Value Stream Map", "process-flow", "value_stream",
           "Process steps, inventory, timeline"),
        # Data (6)
        _t(63, "erd-diagram", "ERD Diagram", "data", "erd",
           "Entities, relationships, cardinalities"),
        _t(64, "data-model-conceptual", "Conceptual Data Model", "data", "conceptual_entities",
           "High-level entity layout"),
        _t(65, "data-model-logical", "Logical Data Model", "data", "logical_entities",
           "Detailed entities with attributes"),
        _t(66, "data-model-physical", "Physical Data Model", "data", "physical_tables",
           "Tables, columns, constraints"),
        _t(67, "data-pipeline-architecture", "Data Pipeline Architecture", "data", "pipeline_layers",
           "Ingestion, processing, storage"),
        _t(68, "data-lakehouse-architecture", "Data Lakehouse Architecture", "data", "lakehouse_layers",
           "Bronze, Silver, Gold medallion layers"),
        # GIS (5)
        _t(69, "gis-architecture", "GIS Architecture", "gis", "gis_stack",
           "Server, database, client layout"),
        _t(70, "geospatial-data-model", "Geospatial Data Model", "gis", "geospatial_model",
           "Feature classes and attributes"),
        _t(71, "map-design", "Map Design", "gis", "map_layout",
           "Map frame, legend, scale, compass"),
        _t(72, "geoprocessing-workflow", "Geoprocessing Workflow", "gis", "tool_chain",
           "Sequential geoprocessing tools"),
        _t(73, "spatial-data-flow", "Spatial Data Flow", "gis", "spatial_flow",
           "Source to client spatial pipeline"),
        # Cloud (7)
        _t(74, "aws-architecture", "AWS Architecture", "cloud", "cloud_provider",
           "AWS VPC, EC2, S3, RDS layout", ("AWS",)),
        _t(75, "azure-architecture", "Azure Architecture", "cloud", "cloud_provider",
           "Azure VNet, VM, Blob, SQL layout", ("Azure",)),
        _t(76, "gcp-architecture", "GCP Architecture", "cloud", "cloud_provider",
           "GCP VPC, Compute, Storage, BigQuery", ("GCP",)),
        _t(77, "multi-cloud-architecture", "Multi-Cloud Architecture", "cloud", "multi_cloud",
           "AWS, Azure, GCP integration"),
        _t(78, "serverless-architecture", "Serverless Architecture", "cloud", "serverless",
           "API Gateway, functions, datastore"),
        _t(79, "cloud-migration-architecture", "Cloud Migration Architecture", "cloud", "migration",
           "On-premises to cloud transition"),
        _t(80, "cloud-cost-optimization", "Cloud Cost Optimization", "cloud", "cost_optimization",
           "Cost, resource, and optimization areas"),
        # DevOps (6)
        _t(81, "cicd-pipeline", "CI/CD Pipeline", "devops", "pipeline_stages",
           "Source, build, test, deploy stages"),
        _t(82, "devops-architecture", "DevOps Architecture", "devops", "devops_toolchain",
           "Plan, code, build, test, release toolchain"),
        _t(83, "gitops-architecture", "GitOps Architecture", "devops", "gitops",
           "Git repo, operator, cluster loop"),
        _t(84, "observability-architecture", "Observability Architecture", "devops", "observability",
           "Logs, metrics, traces, dashboards"),
        _t(85, "infrastructure-as-code", "Infrastructure as Code", "devops", "iac",
           "IaC definitions to cloud resources"),
        _t(86, "service-mesh-architecture", "Service Mesh Architecture", "devops", "service_mesh",
           "Control plane, data plane, sidecars"),
    ]


CATEGORIES = sorted({t.category for t in all_templates()})
