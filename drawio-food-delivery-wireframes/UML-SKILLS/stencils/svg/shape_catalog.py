"""
Single source of truth for the UML & architecture shape library.

Run:
  python scripts/build_inventory.py   # → SHAPE_LIBRARY.json + SHAPE_LIBRARY.md
  python scripts/generate_shapes.py   # → shapes/**/*.svg + sprite.svg
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Literal, Optional

Delivery = Literal["generate", "manual", "download", "annotation"]
AssetType = Literal["shape", "connector", "marker", "annotation"]


@dataclass(frozen=True)
class Shape:
    id: str
    name: str
    description: str
    visual: str
    purpose: str
    asset_type: AssetType = "shape"
    delivery: Delivery = "generate"
    generator: Optional[str] = None
    download_url: Optional[str] = None
    download_pack: Optional[str] = None
    notes: Optional[str] = None


@dataclass(frozen=True)
class Category:
    id: str
    name: str
    shapes: List[Shape]


STYLE = {
    "viewBox_node": "0 0 80 80",
    "viewBox_connector": "0 0 120 24",
    "viewBox_wide": "0 0 120 80",
    # PrimeReact Lara tokens (see STYLE_GUIDE.md)
    "primary": "#3B82F6",
    "primary_tint": "#EFF6FF",
    "surface_0": "#ffffff",
    "surface_50": "#f8fafc",
    "surface_200": "#e2e8f0",
    "surface_700": "#334155",
    "text_muted": "#64748b",
    "focus_ring": "#BFDBFE",
    "border_radius": 6,
    "border_radius_sm": 4,
    # Generator aliases
    "stroke": "#334155",
    "stroke_width": 1.5,
    "stroke_width_connector": 1.25,
    "fill": "#ffffff",
    "marker_fill": "#334155",
    "font_family": "Inter, system-ui, -apple-system, Segoe UI, sans-serif",
    "font_size_label": 12,
    "font_size_stereotype": 10,
    "font_size_caption": 9,
}


def _cat(cid: str, name: str, shapes: List[Shape]) -> Category:
    return Category(id=cid, name=name, shapes=shapes)


def _s(
    id: str,
    name: str,
    description: str,
    visual: str,
    purpose: str,
    *,
    asset_type: AssetType = "shape",
    delivery: Delivery = "generate",
    generator: Optional[str] = None,
    download_url: Optional[str] = None,
    download_pack: Optional[str] = None,
    notes: Optional[str] = None,
) -> Shape:
    return Shape(
        id=id,
        name=name,
        description=description,
        visual=visual,
        purpose=purpose,
        asset_type=asset_type,
        delivery=delivery,
        generator=generator or id,
        download_url=download_url,
        download_pack=download_pack,
        notes=notes,
    )


CATEGORIES: List[Category] = [
    _cat("basic-geometric", "Basic Geometric Shapes", [
        _s("rectangle", "Rectangle", "Four-sided shape with 90° corners", "▭", "Base for classes, components, nodes"),
        _s("rounded-rectangle", "Rounded Rectangle", "Rectangle with rounded corners", "▭ (rounded)", "Activities, actions, use cases"),
        _s("square", "Square", "Equal-sided rectangle", "◻", "Boxes, containers"),
        _s("circle", "Circle", "Perfect round shape", "◯", "Interfaces, control points"),
        _s("ellipse", "Ellipse", "Oval shape", "◯ (stretched)", "Use cases, actors (head)"),
        _s("diamond", "Diamond", "Four-sided rotated square", "◇", "Decisions, branching points"),
        _s("triangle", "Triangle", "Three-sided polygon", "▲", "Directional indicators, signals"),
        _s("hexagon", "Hexagon", "Six-sided polygon", "⬡", "Database notations, signals"),
        _s("pentagon", "Pentagon", "Five-sided polygon", "⬠", "Send/receive signals"),
        _s("cylinder", "Cylinder", "3D cylinder shape", "⬢", "Databases, storage"),
        _s("folder", "Folder", "Tabbed rectangle", "📁", "Packages, namespaces"),
        _s("line", "Line", "Straight path", "───", "Connectors, edges", asset_type="connector", generator="line-solid"),
        _s("arrow", "Arrow", "Line with arrowhead", "───▶", "Flow direction, dependencies", asset_type="connector", generator="arrow-solid"),
        _s("bracket", "Bracket", "Curved or angled brackets", "[ ]", "Constraints, stereotypes", delivery="manual"),
        _s("dashed-line", "Dashed Line", "Line with dashes", "─ ─ ─", "Dependencies, interfaces", asset_type="connector", generator="line-dashed"),
        _s("dotted-line", "Dotted Line", "Line with dots", "· · ·", "Optional relationships", asset_type="connector", generator="line-dotted"),
    ]),
    _cat("uml-class", "UML Class Diagram", [
        _s("class-box", "Class Box", "3-compartment rectangle", "┌Name├attrs├methods┘", "Core class structure", generator="class-box", delivery="generate"),
        _s("abstract-class", "Abstract Class", "Class with italic name", "┌*Class*┘", "Abstract classes", generator="abstract-class"),
        _s("interface-box", "Interface", "Class with <<interface>>", "┌<<interface>>┘", "Interface definition", generator="interface-box"),
        _s("enumeration", "Enumeration", "Class with <<enumeration>>", "┌<<enumeration>>┘", "Enumerated types", generator="enumeration"),
        _s("stereotype", "Stereotype", "Text in guillemets", "<<stereotype>>", "Marking UML elements", asset_type="annotation", delivery="annotation"),
        _s("attribute", "Attribute", "Text in class box", "+ name: Type", "Class properties", asset_type="annotation", delivery="annotation"),
        _s("method", "Method", "Text in class box", "+ method(): ReturnType", "Class operations", asset_type="annotation", delivery="annotation"),
        _s("visibility-marker", "Visibility Marker", "+ - # ~ symbols", "+ - # ~", "Access modifiers", asset_type="annotation", delivery="annotation"),
        _s("association", "Association", "Solid line", "───────────", "General relationship", asset_type="connector", generator="line-solid"),
        _s("aggregation", "Aggregation", "Hollow diamond line", "◇───────────", "Has-a relationship", asset_type="connector", generator="aggregation"),
        _s("composition", "Composition", "Filled diamond line", "◆───────────", "Part-of relationship", asset_type="connector", generator="composition"),
        _s("inheritance", "Inheritance", "Hollow triangle line", "△───────────", "Is-a relationship", asset_type="connector", generator="inheritance"),
        _s("dependency", "Dependency", "Dashed arrow", "─ ─ ─ ─ ▶", "Using relationship", asset_type="connector", generator="dependency"),
        _s("realization", "Realization", "Dashed hollow triangle", "─ ─ ─ ─ △", "Implementation", asset_type="connector", generator="realization"),
        _s("multiplicity", "Multiplicity", "Text labels 1, *, 0..1", "1, *", "Cardinality indicators", asset_type="annotation", delivery="annotation"),
        _s("constraint-brace", "Constraint", "Text in braces", "{constraint}", "Business rules", asset_type="annotation", delivery="annotation"),
    ]),
    _cat("uml-use-case", "UML Use Case Diagram", [
        _s("actor", "Actor", "Stick figure or <<actor>> box", "👤", "User/external system", generator="actor"),
        _s("use-case", "Use Case", "Oval with text", "(Use Case)", "System function", generator="use-case"),
        _s("system-boundary", "System Boundary", "Rectangle with name", "┌ System ┘", "System scope", generator="system-boundary"),
        _s("include-relationship", "Include", "Dashed arrow <<include>>", "─ ─ ▶ <<include>>", "Required functionality", asset_type="connector", generator="include"),
        _s("extend-relationship", "Extend", "Dashed arrow <<extend>>", "─ ─ ▶ <<extend>>", "Optional functionality", asset_type="connector", generator="extend"),
        _s("actor-generalization", "Generalization", "Hollow triangle line", "△───────────", "Actor inheritance", asset_type="connector", generator="inheritance"),
        _s("actor-head", "Actor Head", "Ellipse for stick figure head", "◯", "Actor icon part", generator="ellipse", notes="Sub-part of actor; use actor.svg for full figure"),
    ]),
    _cat("uml-sequence", "UML Sequence Diagram", [
        _s("lifeline", "Lifeline", "Box with vertical dashed line", "┌Obj┘ │ │ │", "Object timeline", generator="lifeline"),
        _s("actor-lifeline", "Actor Lifeline", "Actor with dashed line", "👤 │ │ │", "User timeline", generator="actor-lifeline"),
        _s("activation-bar", "Activation Bar", "Thin vertical rectangle", "┌─┐││└─┘", "Execution period", generator="activation-bar"),
        _s("sync-message", "Synchronous Message", "Solid arrow", "─────▶", "Blocking call", asset_type="connector", generator="arrow-solid"),
        _s("async-message", "Asynchronous Message", "Open arrow", "─────▷", "Non-blocking call", asset_type="connector", generator="arrow-open"),
        _s("return-message", "Return Message", "Dashed arrow", "─ ─ ─ ▶", "Returning value", asset_type="connector", generator="arrow-dashed"),
        _s("self-message", "Self Message", "Arrow looping back", "───┐◄──┘", "Self-call", asset_type="connector", generator="self-message"),
        _s("create-message", "Create Message", "Dashed arrow <<create>>", "─ ─ ▶ <<create>>", "Object creation", asset_type="connector", generator="create-message"),
        _s("destroy-message", "Destroy Message", "Arrow with X", "─────▶ X", "Object destruction", asset_type="connector", generator="destroy-message"),
        _s("combined-fragment", "Combined Fragment", "Rectangle with operator", "┌ alt ┘", "Loops, conditions", generator="combined-fragment"),
        _s("alt-fragment", "Alt Fragment", "Combined fragment alt", "┌ alt [c] ┘", "Alternative paths", generator="alt-fragment"),
        _s("loop-fragment", "Loop Fragment", "Combined fragment loop", "┌ loop ┘", "Repetition", generator="loop-fragment"),
        _s("opt-fragment", "Opt Fragment", "Combined fragment opt", "┌ opt ┘", "Optional flow", generator="opt-fragment"),
        _s("par-fragment", "Par Fragment", "Combined fragment par", "┌ par ┘", "Parallel flows", generator="par-fragment"),
        _s("guard", "Guard", "Text in brackets", "[condition]", "Conditional logic", asset_type="annotation", delivery="annotation"),
        _s("message-number", "Message Number", "Numbered labels", "1, 1.1, 2", "Message ordering", asset_type="annotation", delivery="annotation"),
        _s("interaction-occurrence", "Interaction Occurrence", "Rectangle ref", "ref", "Reusable interaction", generator="interaction-occurrence"),
        _s("continuation", "Continuation", "Rectangle with label", "┌cont.┘", "Fragment continuation", generator="continuation"),
    ]),
    _cat("uml-activity", "UML Activity Diagram", [
        _s("initial-node", "Initial Node", "Solid black circle", "●", "Start of flow", asset_type="marker", generator="initial-node"),
        _s("final-node", "Final Node", "Circle with border", "◉", "End of flow", asset_type="marker", generator="final-node"),
        _s("flow-final-node", "Flow Final Node", "Circle with X", "⊗", "End of specific flow", asset_type="marker", generator="flow-final-node"),
        _s("action", "Action", "Rounded rectangle", "┌ Action ┘", "Single step", generator="rounded-rectangle"),
        _s("activity", "Activity", "Rounded rectangle <<activity>>", "┌<<activity>>┘", "Complex step", generator="activity"),
        _s("decision-node", "Decision Node", "Diamond", "◇", "Branching point", generator="diamond"),
        _s("merge-node", "Merge Node", "Diamond", "◇", "Combining paths", generator="diamond", notes="Same geometry as decision-node"),
        _s("fork-node", "Fork Node", "Horizontal bar", "────", "Parallel splitting", asset_type="marker", generator="fork-bar"),
        _s("join-node", "Join Node", "Horizontal bar", "────", "Parallel merging", asset_type="marker", generator="join-bar"),
        _s("object-node", "Object Node", "Rectangle", "┌ Object ┘", "Data passing", generator="rectangle"),
        _s("data-store-node", "Data Store Node", "Rectangle <<datastore>>", "┌<<datastore>>┘", "Data storage", generator="data-store"),
        _s("send-signal", "Send Signal", "Pentagon", "⬠", "Sending signal", generator="pentagon"),
        _s("accept-signal", "Accept Signal", "Jagged edge shape", "┌──╲│", "Receiving signal", generator="accept-signal", delivery="manual"),
        _s("accept-time-event", "Accept Time Event", "Hourglass shape", "⏳", "Time-based trigger", delivery="manual"),
        _s("interrupting-edge", "Interrupting Edge", "Zigzag line", "╲╱╲╱╲", "Flow interruption", asset_type="connector", generator="zigzag"),
        _s("swimlane", "Swimlane", "Vertical/horizontal divider", "┌ Lane ┘", "Actor/role separation", generator="swimlane"),
        _s("activity-partition", "Activity Partition", "Swimlane with label", "┌ Role ┘", "Organization grouping", generator="swimlane"),
        _s("expansion-region", "Expansion Region", "Dashed border rectangle", "┌─ ─ ─┘", "Multi-element area", generator="expansion-region"),
        _s("exception-handler", "Exception Handler", "Lightning bolt", "⚡", "Error handling", delivery="manual"),
        _s("control-flow", "Control Flow", "Solid arrow", "─────▶", "Flow direction", asset_type="connector", generator="arrow-solid"),
        _s("object-flow", "Object Flow", "Dashed arrow", "─ ─ ─ ▶", "Object movement", asset_type="connector", generator="arrow-dashed"),
        _s("interrupting-flow", "Interrupting Flow", "Arrow with bolt", "─────▶⚡", "Flow interruption", asset_type="connector", delivery="manual"),
    ]),
    _cat("uml-state-machine", "UML State Machine Diagram", [
        _s("state", "State", "Rounded rectangle", "┌ State ┘", "Object state", generator="rounded-rectangle"),
        _s("sm-initial-state", "Initial State", "Solid black circle", "●", "Starting point", asset_type="marker", generator="initial-node"),
        _s("sm-final-state", "Final State", "Circle with border", "◉", "End point", asset_type="marker", generator="final-node"),
        _s("choice-pseudostate", "Choice Pseudo-state", "Diamond", "◇", "Conditional branching", generator="diamond"),
        _s("fork-pseudostate", "Fork Pseudo-state", "Horizontal bar", "────", "Parallel splitting", asset_type="marker", generator="fork-bar"),
        _s("join-pseudostate", "Join Pseudo-state", "Horizontal bar", "────", "Parallel merging", asset_type="marker", generator="join-bar"),
        _s("deep-history", "Deep History", "Circle with H*", "H*", "History deep", asset_type="marker", generator="deep-history"),
        _s("shallow-history", "Shallow History", "Circle with H", "H", "History shallow", asset_type="marker", generator="shallow-history"),
        _s("entry-point", "Entry Point", "Circle with arrow", "●→", "Entry into composite", asset_type="marker", delivery="manual"),
        _s("exit-point", "Exit Point", "Circle with arrow", "●", "Exit from composite", asset_type="marker", delivery="manual"),
        _s("composite-state", "Composite State", "State with internal border", "┌ State ┌─┐ ┘", "Nested states", generator="composite-state"),
        _s("submachine-state", "Submachine State", "State with ref", "┌ State ref ┘", "Reusable state", generator="submachine-state"),
        _s("transition", "Transition", "Solid arrow with label", "────▶ trigger", "State change", asset_type="connector", generator="arrow-solid"),
        _s("internal-transition", "Internal Transition", "Self-loop", "───┐◄──┘", "Self-transition", asset_type="connector", generator="self-message"),
        _s("completion-transition", "Completion Transition", "Arrow no label", "─────▶", "Automatic transition", asset_type="connector", generator="arrow-solid"),
        _s("transition-event", "Event", "Text on transition", "event()", "Triggering event", asset_type="annotation", delivery="annotation"),
        _s("transition-guard", "Transition Guard", "Text in brackets", "[condition]", "Condition for transition", asset_type="annotation", delivery="annotation"),
        _s("transition-action", "Transition Action", "Text with slash", "/ action", "Activity on transition", asset_type="annotation", delivery="annotation"),
    ]),
    _cat("uml-component-deployment", "UML Component & Deployment", [
        _s("component", "Component", "Rectangle <<component>>", "┌<<component>>┘", "System component", generator="component"),
        _s("component-lollipop", "Component with Lollipop", "Component + provided IF", "┌───○", "Provided interface", generator="component-lollipop"),
        _s("component-socket", "Component with Socket", "Component + required IF", "┌───(", "Required interface", generator="component-socket"),
        _s("interface-provided", "Interface (Provided)", "Circle with label", "○", "Provided interface", generator="lollipop"),
        _s("interface-required", "Interface (Required)", "Half-circle", "(", "Required interface", generator="socket"),
        _s("port", "Port", "Small square on component", "□", "Interaction point", asset_type="marker", generator="port"),
        _s("artifact", "Artifact", "Rectangle <<artifact>>", "┌<<artifact>>┘", "Deployment artifact", generator="artifact"),
        _s("node", "Node", "3D rectangle", "┌ Node ┘", "Physical resource", generator="node"),
        _s("device", "Device", "Node <<device>>", "┌<<device>>┘", "Hardware device", generator="device"),
        _s("execution-environment", "Execution Environment", "Node <<EE>>", "┌<<EE>>┘", "Software environment", generator="execution-environment"),
        _s("deployment-relationship", "Deployment", "Dashed arrow <<deploy>>", "─ ─ ▶ <<deploy>>", "Deployment relationship", asset_type="connector", generator="dependency"),
        _s("manifest-relationship", "Manifest", "Dashed arrow <<manifest>>", "─ ─ ▶ <<manifest>>", "Artifact manifestation", asset_type="connector", generator="dependency"),
    ]),
    _cat("uml-package", "UML Package & Organizational", [
        _s("package", "Package", "Folder shape", "┌ Package ┘", "Grouping element", generator="folder"),
        _s("package-stereotype", "Package with Stereotype", "Package <<stereotype>>", "┌<<st>> Package┘", "Typed package", generator="package-stereotype"),
        _s("model", "Model", "Package <<model>>", "┌<<model>>┘", "Model grouping", generator="model"),
        _s("subsystem", "Subsystem", "Package <<subsystem>>", "┌<<subsystem>>┘", "Subsystem grouping", generator="subsystem"),
        _s("profile", "Profile", "Package <<profile>>", "┌<<profile>>┘", "Stereotype definition", generator="profile"),
        _s("package-import", "Package Import", "Dashed arrow <<import>>", "─ ─ ▶ <<import>>", "Package dependency", asset_type="connector", generator="dependency"),
        _s("package-merge", "Package Merge", "Dashed arrow <<merge>>", "─ ─ ▶ <<merge>>", "Package combination", asset_type="connector", generator="dependency"),
    ]),
    _cat("architecture", "Architecture Diagram", [
        _s("microservice", "Microservice", "Rectangle <<ms>>", "┌<<ms>> Service┘", "Microservice", generator="microservice"),
        _s("api-gateway", "API Gateway", "Rectangle <<gateway>>", "┌<<gateway>> API┘", "API gateway", generator="api-gateway"),
        _s("database", "Database", "Cylinder shape", "⬢", "Database", generator="cylinder"),
        _s("cache", "Cache", "Rectangle with lightning", "┌ ⚡ Cache ┘", "Cache layer", generator="cache"),
        _s("message-queue", "Message Queue", "Rectangle <<queue>>", "┌<<queue>>┘", "Message queue", generator="message-queue"),
        _s("load-balancer", "Load Balancer", "Rectangle <<lb>>", "┌<<lb>> LB┘", "Load balancer", generator="load-balancer"),
        _s("firewall", "Firewall", "Rectangle <<fw>>", "┌<<fw>> FW┘", "Firewall", generator="firewall"),
        _s("storage", "Storage", "Rectangle <<storage>>", "┌<<storage>>┘", "Object storage", generator="storage"),
        _s("container", "Container", "Rectangle <<container>>", "┌<<container>>┘", "Container", generator="container-box"),
        _s("pod", "Pod", "Rectangle <<pod>>", "┌<<pod>>┘", "Kubernetes pod", generator="pod"),
        _s("k8s-service", "Service", "Rectangle <<service>>", "┌<<service>>┘", "Kubernetes service", generator="k8s-service"),
        _s("ingress", "Ingress", "Rectangle <<ingress>>", "┌<<ingress>>┘", "Kubernetes ingress", generator="ingress"),
        _s("configmap", "ConfigMap", "Rectangle <<config>>", "┌<<config>>┘", "Kubernetes config", generator="configmap"),
        _s("secret", "Secret", "Rectangle <<secret>>", "┌<<secret>>┘", "Kubernetes secret", generator="secret"),
        _s("persistent-volume", "Persistent Volume", "Rectangle <<pv>>", "┌<<pv>>┘", "Storage volume", generator="persistent-volume"),
        _s("namespace", "Namespace", "Rectangle <<ns>>", "┌<<ns>>┘", "Kubernetes namespace", generator="namespace"),
        _s("consumer", "Consumer", "Rectangle <<consumer>>", "┌<<consumer>>┘", "Event consumer", generator="consumer"),
        _s("producer", "Producer", "Rectangle <<producer>>", "┌<<producer>>┘", "Event producer", generator="producer"),
        _s("broker", "Broker", "Rectangle <<broker>>", "┌<<broker>>┘", "Message broker", generator="broker"),
        _s("topic", "Topic", "Rectangle <<topic>>", "┌<<topic>>┘", "Kafka topic", generator="topic"),
    ]),
    _cat("data-database", "Data & Database", [
        _s("table", "Table", "Grid with columns", "┌ Table ┘", "Database table", generator="table"),
        _s("view-db", "View", "Rectangle <<view>>", "┌<<view>>┘", "Database view", generator="view-db"),
        _s("stored-procedure", "Stored Procedure", "Rectangle <<sp>>", "┌<<sp>>┘", "Stored procedure", generator="stored-procedure"),
        _s("index-db", "Index", "Rectangle <<index>>", "┌<<index>>┘", "Database index", generator="index-db"),
        _s("primary-key", "Primary Key", "Column with PK", "id PK", "Primary key", asset_type="annotation", delivery="annotation"),
        _s("foreign-key", "Foreign Key", "Column with FK", "id FK", "Foreign key", asset_type="annotation", delivery="annotation"),
        _s("table-relationship", "Relationship", "Line with cardinalities", "1 ─── *", "Table relationship", asset_type="connector", generator="association"),
        _s("er-entity", "Entity", "Rectangle for ER", "┌ Entity ┘", "ER entity", generator="rectangle"),
    ]),
    _cat("cloud-architecture", "Cloud Architecture", [
        _s("aws-ec2", "AWS EC2", "AWS EC2 icon", "EC2", "AWS compute", generator="aws-ec2",
           notes="Official icons: https://aws.amazon.com/architecture/icons/"),
        _s("aws-s3", "AWS S3", "AWS S3 icon", "S3", "AWS storage", generator="aws-s3",
           notes="Official icons: https://aws.amazon.com/architecture/icons/"),
        _s("aws-rds", "AWS RDS", "AWS RDS icon", "RDS", "AWS database", generator="aws-rds",
           notes="Official icons: https://aws.amazon.com/architecture/icons/"),
        _s("aws-lambda", "AWS Lambda", "AWS Lambda icon", "λ", "AWS serverless", generator="aws-lambda",
           notes="Official icons: https://aws.amazon.com/architecture/icons/"),
        _s("aws-api-gateway", "AWS API Gateway", "AWS APIG icon", "APIG", "AWS API gateway", generator="aws-api-gateway",
           notes="Official icons: https://aws.amazon.com/architecture/icons/"),
        _s("aws-vpc", "AWS VPC", "AWS VPC border", "VPC", "AWS network", generator="aws-vpc",
           notes="Official icons: https://aws.amazon.com/architecture/icons/"),
        _s("azure-vm", "Azure VM", "Azure VM icon", "VM", "Azure compute", delivery="manual",
           download_pack="azure-architecture-icons", notes="Download from Microsoft Learn icon set"),
        _s("azure-blob", "Azure Blob", "Azure Blob icon", "Blob", "Azure storage", delivery="manual",
           download_pack="azure-architecture-icons"),
        _s("azure-sql", "Azure SQL", "Azure SQL icon", "SQL", "Azure database", delivery="manual",
           download_pack="azure-architecture-icons"),
        _s("azure-functions", "Azure Functions", "Azure Functions", "⚡", "Azure serverless", delivery="manual",
           download_pack="azure-architecture-icons"),
        _s("gcp-compute", "GCP Compute Engine", "GCE icon", "GCE", "GCP compute", delivery="manual",
           download_pack="gcp-architecture-icons"),
        _s("gcp-storage", "GCP Cloud Storage", "GCS icon", "GCS", "GCP storage", delivery="manual",
           download_pack="gcp-architecture-icons"),
        _s("gcp-bigquery", "GCP BigQuery", "BQ icon", "BQ", "GCP data warehouse", delivery="manual",
           download_pack="gcp-architecture-icons"),
        _s("cloud-region", "Cloud Region", "Box with region name", "us-east-1", "Cloud region", generator="cloud-region"),
        _s("cloud-az", "Cloud Availability Zone", "Box with AZ label", "AZ-A", "Availability zone", generator="cloud-az"),
        _s("cloud-generic", "Cloud Generic", "Generic cloud service box", "Cloud", "Fallback cloud node", generator="cloud-generic"),
    ]),
    _cat("infrastructure-network", "Infrastructure & Network", [
        _s("server", "Server", "3D rectangle rack", "Server", "Physical server", generator="server"),
        _s("switch", "Switch", "Rectangle with ports", "Switch", "Network switch", generator="switch"),
        _s("router", "Router", "Rectangle with antennas", "Router", "Network router", generator="router"),
        _s("firewall-network", "Firewall", "Rectangle with shield", "FW", "Network firewall", generator="firewall"),
        _s("load-balancer-network", "Load Balancer", "Rectangle LB", "LB", "Network load balancer", generator="load-balancer"),
        _s("vpn", "VPN", "Rectangle VPN", "VPN", "VPN gateway", generator="vpn"),
        _s("internet", "Internet", "Cloud shape", "☁", "External network", generator="internet-cloud"),
        _s("dmz", "DMZ", "Rectangle DMZ", "DMZ", "Network DMZ", generator="dmz"),
        _s("subnet", "Subnet", "Rectangle CIDR", "10.0.1.0/24", "Network subnet", generator="subnet"),
    ]),
    _cat("process-flow", "Process & Flow", [
        _s("process", "Process", "Rectangle", "Process", "Standard process", generator="rectangle"),
        _s("flow-start", "Start", "Solid circle", "●", "Process start", asset_type="marker", generator="initial-node"),
        _s("flow-end", "End", "Circle with border", "◉", "Process end", asset_type="marker", generator="final-node"),
        _s("flow-decision", "Decision", "Diamond", "◇", "Decision point", generator="diamond"),
        _s("document", "Document", "Wavy bottom rectangle", "Document", "Document output", generator="document", delivery="manual"),
        _s("data-parallelogram", "Data", "Parallelogram", "Data", "Data input", generator="data-parallelogram", delivery="manual"),
        _s("predefined-process", "Predefined Process", "Double border rectangle", "Process", "Subroutine", generator="predefined-process"),
        _s("manual-input", "Manual Input", "Angled top rectangle", "Manual", "Manual entry", delivery="manual"),
        _s("display", "Display", "Screen rectangle", "Display", "Screen output", generator="display", delivery="manual"),
        _s("manual-operation", "Manual Operation", "Trapezoid", "Manual", "Manual task", delivery="manual"),
        _s("off-page-connector", "Off-page Connector", "Pentagon", "⬠", "Connector to another page", generator="pentagon"),
    ]),
    _cat("connector-line", "Connector & Line Types", [
        _s("line-solid", "Solid Line", "Standard line", "───────────", "Association, flow", asset_type="connector", generator="line-solid"),
        _s("line-dashed", "Dashed Line", "Dashed connector", "─ ─ ─ ─ ─", "Dependency, optional", asset_type="connector", generator="line-dashed"),
        _s("line-dotted", "Dotted Line", "Dotted connector", "· · · · ·", "Weak relationship", asset_type="connector", generator="line-dotted"),
        _s("arrow-solid", "Solid Arrow", "Filled arrowhead", "───────────▶", "Synchronous flow", asset_type="connector", generator="arrow-solid"),
        _s("arrow-open", "Open Arrow", "Open arrowhead", "───────────▷", "Asynchronous flow", asset_type="connector", generator="arrow-open"),
        _s("arrow-dashed", "Dashed Arrow", "Dashed with arrowhead", "─ ─ ─ ─ ▶", "Dependency", asset_type="connector", generator="arrow-dashed"),
        _s("arrow-double", "Double-headed Arrow", "Arrow both ends", "◀──────────▶", "Bi-directional", asset_type="connector", generator="arrow-double"),
        _s("arrow-hollow-triangle", "Solid Triangle Arrow", "Hollow triangle", "───────────△", "Inheritance", asset_type="connector", generator="inheritance"),
        _s("arrow-dashed-triangle", "Dashed Triangle Arrow", "Dashed hollow triangle", "─ ─ ─ ─ △", "Realization", asset_type="connector", generator="realization"),
        _s("diamond-hollow-end", "Hollow Diamond", "Diamond at end", "◇───────────", "Aggregation", asset_type="connector", generator="aggregation"),
        _s("diamond-filled-end", "Filled Diamond", "Filled diamond", "◆───────────", "Composition", asset_type="connector", generator="composition"),
        _s("self-loop", "Self-loop", "Arrow looping back", "───┐◄──┘", "Self-reference", asset_type="connector", generator="self-message"),
        _s("zigzag-line", "Zigzag Line", "Zigzag connector", "╲╱╲╱╲", "Interrupting flow", asset_type="connector", generator="zigzag"),
        _s("bend-point", "Bend Point", "Small circle at bend", "●", "Connector control point", asset_type="marker", generator="initial-node"),
    ]),
    _cat("miscellaneous", "Miscellaneous", [
        _s("note", "Note", "Folded rectangle", "Note", "Comments", generator="note", delivery="manual"),
        _s("constraint-text", "Constraint", "Text in braces", "{constraint}", "Limitation", asset_type="annotation", delivery="annotation"),
        _s("tag", "Tag", "Rectangle <<tag>>", "Tag", "Metadata", generator="tag"),
        _s("legend", "Legend", "Rectangle with symbols", "Legend", "Diagram legend", generator="legend"),
        _s("title-block", "Title Block", "Project info block", "Project", "Document header", generator="title-block"),
        _s("timeline", "Timeline", "Horizontal line", "────────", "Timeline", asset_type="connector", generator="line-solid"),
        _s("milestone", "Milestone", "Diamond marker", "◆", "Milestone", asset_type="marker", generator="diamond-filled-marker"),
        _s("phase", "Phase", "Rectangle phase name", "Phase 1", "Project phase", generator="phase"),
        _s("sequence-number", "Number", "Text label", "1, 2, 3", "Sequence numbers", asset_type="annotation", delivery="annotation"),
        _s("condition-text", "Condition", "Text in brackets", "[condition]", "Guard condition", asset_type="annotation", delivery="annotation"),
    ]),
]


def all_shapes() -> List[Shape]:
    out: List[Shape] = []
    for cat in CATEGORIES:
        out.extend(cat.shapes)
    return out


def library_dict() -> dict:
    shapes = all_shapes()
    by_delivery: Dict[str, int] = {}
    by_asset: Dict[str, int] = {}
    for s in shapes:
        by_delivery[s.delivery] = by_delivery.get(s.delivery, 0) + 1
        by_asset[s.asset_type] = by_asset.get(s.asset_type, 0) + 1
    return {
        "version": "1.0",
        "title": "UML & Architecture Shape Library",
        "style": STYLE,
        "summary": {
            "total_shapes": len(shapes),
            "categories": len(CATEGORIES),
            "by_delivery": by_delivery,
            "by_asset_type": by_asset,
        },
        "categories": [
            {
                "id": c.id,
                "name": c.name,
                "count": len(c.shapes),
                "shapes": [
                    {
                        **asdict(s),
                        "output_path": f"shapes/{c.id}/{s.id}.svg" if s.delivery != "annotation" else None,
                    }
                    for s in c.shapes
                ],
            }
            for c in CATEGORIES
        ],
    }
