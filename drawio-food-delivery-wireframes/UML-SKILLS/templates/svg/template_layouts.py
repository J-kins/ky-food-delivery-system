"""Per-template layout renderers."""
from __future__ import annotations

from typing import Callable, Dict, List

from template_builder import CONTENT_BOTTOM, CONTENT_TOP, M, SvgBuilder, W
from template_catalog import Template

LayoutFn = Callable[[SvgBuilder, Template], None]


def render_layout(builder: SvgBuilder, template: Template) -> None:
    fn = LAYOUTS.get(template.layout)
    if fn is None:
        builder.placeholder(300, 300, 600, 300, "Layout placeholder")
        return
    fn(builder, template)
    builder.add_markers()


# --- UML -------------------------------------------------------------------

def _class_diagram(b: SvgBuilder, t: Template) -> None:
    b.class_box(180, 220, 220, 110, "ClassA")
    b.class_box(760, 180, 220, 110, "ClassB")
    b.class_box(1340, 240, 220, 110, "ClassC")
    b.add_markers()
    b.connector(400, 275, 760, 235, "1")
    b.connector(980, 235, 1340, 295, "*")
    b.guide_line(400, 330, 760, 290)
    b.label(580, 310, "&lt;multiplicity&gt;", muted=True, anchor="middle")


def _object_diagram(b: SvgBuilder, t: Template) -> None:
    for i, name in enumerate((":objA", ":objB", ":objC")):
        x = 220 + i * 520
        b.placeholder(x, 280, 200, 120, name)
        b.label(x + 100, 420, "________", anchor="middle", muted=True)
    b.guide_line(420, 340, 740, 340)
    b.label(580, 325, "&lt;link&gt;", anchor="middle", muted=True)


def _component_diagram(b: SvgBuilder, t: Template) -> None:
    boxes = [(160, 260), (560, 200), (960, 280), (1360, 220)]
    for i, (x, y) in enumerate(boxes):
        b.placeholder(x, y, 200, 140, f"Component {i + 1}")
        b.label(x + 200, y + 70, "◯", size=16)
    b.guide_line(360, 330, 560, 270)
    b.guide_line(760, 270, 960, 350)


def _deployment_diagram(b: SvgBuilder, t: Template) -> None:
    for i, x in enumerate((200, 720, 1240)):
        b.placeholder(x, 240, 280, 200, f"Node {i + 1}")
        b.placeholder(x + 40, 480, 200, 80, "artifact", rx=4)


def _package_diagram(b: SvgBuilder, t: Template) -> None:
    for i, x in enumerate((200, 720, 1240)):
        b.placeholder(x, 280, 260, 180, f"<<package>> Pkg{i + 1}", rx=4)
    b.connector(460, 370, 720, 370, "<<import>>")


def _composite_structure(b: SvgBuilder, t: Template) -> None:
    b.placeholder(480, 220, 520, 420, "Composite Part")
    b.placeholder(540, 300, 160, 100, "Part A")
    b.placeholder(780, 300, 160, 100, "Part B")
    b.placeholder(660, 460, 160, 100, "Port")


def _use_case_diagram(b: SvgBuilder, t: Template) -> None:
    b.placeholder(420, 200, 880, 520, "System Boundary", rx=8)
    b.use_case_oval(700, 360, 100, 44, "Use Case A")
    b.use_case_oval(900, 480, 100, 44, "Use Case B")
    b.use_case_oval(620, 520, 100, 44, "Use Case C")
    b.placeholder(180, 320, 80, 160, "Actor", rx=40)
    b.placeholder(1480, 380, 80, 160, "Actor", rx=40)
    b.guide_line(260, 400, 420, 400)


def _sequence_diagram(b: SvgBuilder, t: Template) -> None:
    xs = [320, 640, 960, 1280]
    for i, x in enumerate(xs):
        b.lifeline(x, 160, CONTENT_BOTTOM - 80, f"Object{i + 1}")
        if i == 1:
            b.activation(x, 380, 120)
    for y, lbl in ((300, "sync()"), (420, "async()"), (560, "return")):
        b.guide_line(xs[0], y, xs[-1], y)
        b.label(160, y - 4, lbl, muted=True)


def _activity_diagram(b: SvgBuilder, t: Template) -> None:
    b.swimlane(100, 180, 760, CONTENT_BOTTOM - 220, "Lane 1")
    b.swimlane(900, 180, 760, CONTENT_BOTTOM - 220, "Lane 2")
    b.placeholder(200, 280, 140, 56, "Action", rx=6)
    b.placeholder(420, 400, 56, 56, "?", rx=28)
    b.placeholder(620, 520, 140, 56, "Merge", rx=6)


def _state_machine(b: SvgBuilder, t: Template) -> None:
    b.label(200, 260, "●", size=18)
    b.state_rounded(280, 240, 160, 72, "State A")
    b.state_rounded(620, 320, 160, 72, "State B")
    b.state_rounded(980, 260, 160, 72, "State C")
    b.state_rounded(1320, 380, 160, 72, "State D")
    b.guide_line(440, 276, 620, 356)
    b.guide_line(780, 356, 980, 296)
    b.label(700, 340, "event / guard", muted=True, anchor="middle")


def _communication_diagram(b: SvgBuilder, t: Template) -> None:
    pts = [(300, 300), (700, 220), (1100, 340), (1500, 280)]
    for i, (x, y) in enumerate(pts):
        b.placeholder(x, y, 120, 80, f":obj{i + 1}")
    b.guide_line(360, 340, 760, 260)
    b.label(560, 285, "1: msg()", anchor="middle", muted=True)
    b.guide_line(820, 260, 1160, 380)
    b.label(990, 305, "2: reply()", anchor="middle", muted=True)


def _interaction_overview(b: SvgBuilder, t: Template) -> None:
    b.placeholder(200, 240, 200, 80, "alt [guard]", rx=6)
    b.placeholder(480, 300, 200, 80, "loop", rx=6)
    b.placeholder(760, 260, 200, 80, "ref", rx=6)
    b.label(800, 305, "sd ref", muted=True, anchor="middle")


def _timing_diagram(b: SvgBuilder, t: Template) -> None:
    for i, x in enumerate((280, 640, 1000, 1360)):
        b.label(x, 180, f"Lifeline {i + 1}", anchor="middle")
        b.parts.append(
            f'  <line x1="{x}" y1="200" x2="{x}" y2="{CONTENT_BOTTOM - 100}" '
            f'stroke="#334155" stroke-width="1.25"/>\n'
        )
        for j, state in enumerate(("idle", "active", "idle")):
            y = 280 + j * 120
            b.placeholder(x - 60, y, 120, 48, state, rx=4)


def _profile_diagram(b: SvgBuilder, t: Template) -> None:
    b.placeholder(300, 280, 200, 100, "<<stereotype>>")
    b.placeholder(760, 240, 220, 120, "Metaclass")
    b.placeholder(1200, 300, 200, 100, "<<profile>>")
    b.connector(500, 330, 760, 300)


# --- Architecture ----------------------------------------------------------

def _layered_stack(b: SvgBuilder, t: Template) -> None:
    labels = t.layout_config or ("Layer 1", "Layer 2", "Layer 3", "Layer 4")
    y = 180
    h = (CONTENT_BOTTOM - 220) // len(labels)
    for lbl in labels:
        b.layer_band(120, y, W - 240, h - 16, lbl)
        y += h


def _tier_columns(b: SvgBuilder, t: Template) -> None:
    labels = t.layout_config or ("Tier 1", "Tier 2", "Tier 3")
    w = (W - 280) // len(labels)
    for i, lbl in enumerate(labels):
        b.placeholder(120 + i * w, 200, w - 24, CONTENT_BOTTOM - 280, lbl)


def _grid_blocks(b: SvgBuilder, t: Template) -> None:
    labels = t.layout_config or tuple(f"Block {i + 1}" for i in range(6))
    cols, rows = 3, 2
    cw, ch = 280, 160
    for i, lbl in enumerate(labels):
        c, r = i % cols, i // cols
        b.placeholder(200 + c * (cw + 40), 220 + r * (ch + 40), cw, ch, lbl)


def _service_blocks(b: SvgBuilder, t: Template) -> None:
    b.solid_box(760, 180, 280, 80, "Core System")
    for i, (x, y) in enumerate([(240, 360), (560, 500), (960, 500), (1320, 360)]):
        b.placeholder(x, y, 200, 100, f"Service {i + 1}")
        b.guide_line(900, 260, x + 100, y)


def _microservices(b: SvgBuilder, t: Template) -> None:
    b.solid_box(760, 200, 240, 72, "API Gateway")
    for i, x in enumerate(range(240, 1420, 240)):
        b.placeholder(x, 420, 180, 100, f"µService {i + 1}")
        b.guide_line(880, 272, x + 90, 420)


def _event_driven(b: SvgBuilder, t: Template) -> None:
    b.placeholder(220, 380, 200, 120, "Producer")
    b.solid_box(760, 360, 240, 100, "Message Broker")
    b.placeholder(1340, 380, 200, 120, "Consumer")
    b.connector(420, 440, 760, 410)
    b.connector(1000, 410, 1340, 440)


def _hexagonal(b: SvgBuilder, t: Template) -> None:
    cx, cy = W // 2, 480
    b.parts.append(
        f'  <polygon points="{cx},{cy - 120} {cx + 140},{cy - 60} {cx + 140},{cy + 60} '
        f'{cx},{cy + 120} {cx - 140},{cy + 60} {cx - 140},{cy - 60}" fill="#EFF6FF" '
        f'stroke="#334155" stroke-width="1.5"/>\n'
    )
    b.label(cx, cy + 5, "Domain Core", anchor="middle")
    for i, (x, y, lbl) in enumerate(
        [(200, 300, "Adapter"), (1480, 300, "Adapter"), (200, 660, "Port"), (1480, 660, "Port")]
    ):
        b.placeholder(x, y, 180, 90, lbl)
        b.guide_line(x + 90, y + 45, cx, cy)


def _concentric(b: SvgBuilder, t: Template) -> None:
    labels = list(t.layout_config or ("Entities", "Use Cases", "Controllers", "Frameworks"))
    cx, cy = W // 2, 500
    radii = [280, 220, 160, 100]
    for r, lbl in zip(radii, labels):
        b.parts.append(
            f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e2e8f0" stroke-width="1.5"/>\n'
        )
        b.label(cx, cy - r + 20, lbl, anchor="middle", muted=True)


def _c4_context(b: SvgBuilder, t: Template) -> None:
    b.solid_box(760, 400, 280, 120, "System")
    for lbl, x, y in (("User", 280, 400), ("External System A", 1320, 280), ("External System B", 1320, 520)):
        b.placeholder(x, y, 200, 90, lbl)
        b.guide_line(x + 200, y + 45, 760, 460)


def _c4_container(b: SvgBuilder, t: Template) -> None:
    b.placeholder(320, 200, 1120, 560, "System Boundary")
    for i, (x, y, lbl) in enumerate([(400, 300, "Web App"), (760, 300, "API"), (1120, 300, "Database"), (760, 520, "Cache")]):
        b.placeholder(x, y, 200, 100, lbl)


def _c4_component(b: SvgBuilder, t: Template) -> None:
    b.placeholder(400, 240, 880, 440, "Container Boundary")
    for i, x in enumerate((480, 720, 960, 1200)):
        b.placeholder(x, 360, 160, 90, f"Component {i + 1}")


def _solution_blocks(b: SvgBuilder, t: Template) -> None:
    _grid_blocks(b, t)


def _hub_spoke(b: SvgBuilder, t: Template) -> None:
    hub = t.layout_config[0] if t.layout_config else "Integration Hub"
    b.solid_box(760, 380, 260, 100, hub)
    for i, (x, y) in enumerate([(220, 260), (1320, 260), (220, 600), (1320, 600)]):
        b.placeholder(x, y, 180, 90, f"System {i + 1}")
        b.guide_line(x + 90, y + 45, 760, 430)


def _layered_flow(b: SvgBuilder, t: Template) -> None:
    labels = t.layout_config or ("Source", "Process", "Store", "Sink")
    x = 140
    w = (W - 280) // len(labels) - 20
    for i, lbl in enumerate(labels):
        b.placeholder(x, 360, w, 140, lbl)
        if i < len(labels) - 1:
            b.guide_line(x + w, 430, x + w + 40, 430)
        x += w + 40


def _security_zones(b: SvgBuilder, t: Template) -> None:
    zones = ("Internet", "DMZ", "Internal", "Restricted")
    for i, z in enumerate(zones):
        b.placeholder(120 + i * 420, 220, 380, CONTENT_BOTTOM - 300, z)


# --- Infrastructure --------------------------------------------------------

def _infra_blocks(b: SvgBuilder, t: Template) -> None:
    b.placeholder(200, 300, 240, 140, "Compute")
    b.placeholder(560, 300, 240, 140, "Storage")
    b.placeholder(920, 300, 240, 140, "Network")
    b.placeholder(1280, 300, 240, 140, "Security")


def _network_topology(b: SvgBuilder, t: Template) -> None:
    b.solid_box(860, 220, 160, 80, "Router")
    for lbl, x, y in (("Switch A", 400, 400), ("Switch B", 1320, 400), ("Firewall", 860, 520)):
        b.placeholder(x, y, 160, 80, lbl)
        b.guide_line(x + 80, y, 940, 300 if y < 500 else 520)


def _cloud_vpc(b: SvgBuilder, t: Template) -> None:
    b.placeholder(280, 220, 1200, CONTENT_BOTTOM - 280, "VPC / Region")
    b.placeholder(400, 320, 320, 200, "Availability Zone A")
    b.placeholder(1040, 320, 320, 200, "Availability Zone B")


def _deployment_envs(b: SvgBuilder, t: Template) -> None:
    for i, env in enumerate(("Development", "Staging", "Production")):
        b.placeholder(180 + i * 520, 280, 440, CONTENT_BOTTOM - 360, env)


def _container_cluster(b: SvgBuilder, t: Template) -> None:
    b.placeholder(360, 240, 960, CONTENT_BOTTOM - 320, "Cluster")
    for i, x in enumerate((440, 720, 1000)):
        b.placeholder(x, 360, 180, 120, f"Pod {i + 1}")


def _kubernetes(b: SvgBuilder, t: Template) -> None:
    b.placeholder(360, 200, 960, 180, "Control Plane")
    b.placeholder(360, 440, 960, CONTENT_BOTTOM - 500, "Worker Nodes")
    for x in (440, 720, 1000):
        b.placeholder(x, 520, 160, 100, "Node")


def _ha_active_standby(b: SvgBuilder, t: Template) -> None:
    b.placeholder(320, 340, 280, 160, "Active")
    b.placeholder(1080, 340, 280, 160, "Standby")
    b.solid_box(760, 360, 160, 80, "Load Balancer")
    b.guide_line(600, 420, 760, 400)
    b.guide_line(920, 400, 1080, 420)


def _dr_sites(b: SvgBuilder, t: Template) -> None:
    b.placeholder(240, 280, 520, CONTENT_BOTTOM - 340, "Production Site")
    b.placeholder(1000, 280, 520, CONTENT_BOTTOM - 340, "DR Site")
    b.guide_line(760, 480, 1000, 480)
    b.label(880, 465, "replication", anchor="middle", muted=True)


# --- Project management ----------------------------------------------------

def _charter_sections(b: SvgBuilder, t: Template) -> None:
    sections = (
        "Vision", "Overview", "Objectives", "Scope", "Stakeholders",
        "Constraints", "Milestones", "Budget", "Approvals",
    )
    cols = 3
    cw, ch = 520, 120
    for i, sec in enumerate(sections):
        c, r = i % cols, i // cols
        b.placeholder(120 + c * (cw + 24), 180 + r * (ch + 20), cw, ch, sec)


def _wbs_tree(b: SvgBuilder, t: Template) -> None:
    b.placeholder(760, 180, 200, 60, "1.0 Project")
    for i, x in enumerate((360, 760, 1160)):
        b.placeholder(x, 300, 180, 50, f"1.{i + 1}")
        b.guide_line(860, 240, x + 90, 300)
    for i in range(3):
        b.placeholder(280 + i * 200, 420, 140, 44, f"1.{i + 1}.1")


def _gantt(b: SvgBuilder, t: Template) -> None:
    b.placeholder(100, 180, 420, CONTENT_BOTTOM - 240, "Task List")
    b.placeholder(540, 180, W - 580, CONTENT_BOTTOM - 240, "Timeline / Task Bars")
    for i in range(6):
        y = 240 + i * 80
        b.guide_line(560, y, W - 100, y)
        b.placeholder(580, y + 20, 120 + i * 80, 28, f"Task {i + 1}", rx=4)


def _milestone_timeline(b: SvgBuilder, t: Template) -> None:
    b.guide_line(160, 500, W - 160, 500)
    for i, x in enumerate(range(280, 1500, 240)):
        b.parts.append(f'  <polygon points="{x},{500 - 14} {x + 14},{500} {x},{500 + 14} {x - 14},{500}" fill="#3B82F6"/>\n')
        b.label(x, 540, f"M{i + 1}", anchor="middle", muted=True)


def _roadmap(b: SvgBuilder, t: Template) -> None:
    for i, lbl in enumerate(("Phase 1", "Phase 2", "Phase 3", "Phase 4")):
        b.placeholder(160 + i * 420, 360, 360, 200, lbl)


def _pert_network(b: SvgBuilder, t: Template) -> None:
    nodes = [(320, 280), (640, 200), (640, 420), (960, 280), (1280, 360)]
    for i, (x, y) in enumerate(nodes):
        b.placeholder(x, y, 120, 72, f"A{i + 1}", rx=36)
    b.guide_line(440, 316, 640, 236)
    b.guide_line(440, 316, 640, 456)


def _cpm_network(b: SvgBuilder, t: Template) -> None:
    _pert_network(b, t)
    b.label(640, 180, "critical path →", muted=True, anchor="middle")


def _risk_matrix(b: SvgBuilder, t: Template) -> None:
    b.matrix(560, 280, 5, 5, 96, 72, col_labels=("1", "2", "3", "4", "5"), row_labels=("5", "4", "3", "2", "1"))
    b.label(520, 600, "Impact →", muted=True)
    b.label(400, 320, "↑ Probability", muted=True)


def _heat_map(b: SvgBuilder, t: Template) -> None:
    colors = ("#EFF6FF", "#BFDBFE", "#93C5FD", "#60A5FA", "#3B82F6")
    x0, y0, cw, ch = 480, 300, 80, 60
    for r in range(5):
        for c in range(8):
            b.parts.append(
                f'  <rect x="{x0 + c * cw}" y="{y0 + r * ch}" width="{cw}" height="{ch}" '
                f'fill="{colors[(r + c) % len(colors)]}" stroke="#e2e8f0" stroke-width="1"/>\n'
            )


def _threat_tree(b: SvgBuilder, t: Template) -> None:
    b.placeholder(760, 200, 200, 60, "Threat Goal")
    for i, x in enumerate((360, 760, 1160)):
        b.placeholder(x, 360, 160, 50, f"Vector {i + 1}")
        b.guide_line(860, 260, x + 80, 360)
    for x in (300, 420, 700, 820, 1100, 1220):
        b.placeholder(x, 500, 100, 40, "Leaf", rx=4)


def _allocation_matrix(b: SvgBuilder, t: Template) -> None:
    b.matrix(400, 240, 6, 8, 140, 56, col_labels=("R1", "R2", "R3", "R4", "R5", "R6"))
    b.label(400, 220, "Resources →", muted=True)


def _org_chart(b: SvgBuilder, t: Template) -> None:
    b.solid_box(760, 200, 200, 60, "Program Lead")
    for i, x in enumerate((360, 760, 1160)):
        b.placeholder(x, 340, 180, 56, f"Team {i + 1}")
        b.guide_line(860, 260, x + 90, 340)


# --- Stakeholder -----------------------------------------------------------

def _stakeholder_map(b: SvgBuilder, t: Template) -> None:
    b.solid_box(760, 400, 240, 100, "System")
    for i, (x, y) in enumerate([(300, 300), (1320, 300), (300, 560), (1320, 560), (760, 220)]):
        b.placeholder(x, y, 160, 72, f"Stakeholder {i + 1}")
        b.guide_line(x + 80, y + 36, 880, 450)


def _quadrant_matrix(b: SvgBuilder, t: Template) -> None:
    b.matrix(480, 280, 2, 2, 360, 200)
    b.label(660, 250, "Keep Satisfied", anchor="middle", muted=True)
    b.label(1020, 250, "Manage Closely", anchor="middle", muted=True)
    b.label(660, 650, "Monitor", anchor="middle", muted=True)
    b.label(1020, 650, "Keep Informed", anchor="middle", muted=True)
    b.label(840, 240, "High Power", anchor="middle", muted=True)
    b.label(450, 480, "High Interest", muted=True)


def _influence_network(b: SvgBuilder, t: Template) -> None:
    _stakeholder_map(b, t)


def _venn_three(b: SvgBuilder, t: Template) -> None:
    for cx, lbl in ((640, "Power"), (960, "Legitimacy"), (800, "Urgency")):
        b.parts.append(
            f'  <circle cx="{cx}" cy="480" r="140" fill="#EFF6FF" fill-opacity="0.5" '
            f'stroke="#334155" stroke-width="1.5"/>\n'
        )
        b.label(cx, 360, lbl, anchor="middle")


def _raci_matrix(b: SvgBuilder, t: Template) -> None:
    b.matrix(360, 240, 5, 8, 200, 56, col_labels=("PM", "BA", "Dev", "QA", "Ops"))
    b.label(360, 220, "Roles →", muted=True)


def _register_table(b: SvgBuilder, t: Template) -> None:
    headers = ("ID", "Name", "Role", "Org", "Power", "Interest", "Strategy")
    x, y, cw = 100, 200, 200
    for i, h in enumerate(headers):
        w = 160 if i > 0 else 60
        ox = x + sum(160 if j > 0 else 60 for j in range(i))
        b.solid_box(ox, y, w, 40, h, rx=0)
    for r in range(8):
        for c in range(len(headers)):
            w = 160 if c > 0 else 60
            ox = x + sum(160 if j > 0 else 60 for j in range(c))
            b.placeholder(ox, y + 40 + r * 48, w, 44, "", rx=0)


# --- Process & flow --------------------------------------------------------

def _bpmn_swimlanes(b: SvgBuilder, t: Template) -> None:
    _activity_diagram(b, t)


def _dfd(b: SvgBuilder, t: Template) -> None:
    b.placeholder(160, 400, 140, 80, "External Entity")
    b.placeholder(480, 360, 160, 100, "Process")
    b.placeholder(860, 400, 160, 80, "Data Store", rx=4)
    b.placeholder(1240, 400, 140, 80, "External Entity")
    b.guide_line(300, 440, 480, 410)
    b.label(390, 425, "data flow", muted=True, anchor="middle")


def _side_by_side(b: SvgBuilder, t: Template) -> None:
    b.label(480, 200, "As-Is", anchor="middle", size=16)
    b.label(1320, 200, "To-Be", anchor="middle", size=16)
    b.placeholder(120, 240, 720, CONTENT_BOTTOM - 300, "Current Process")
    b.placeholder(960, 240, 720, CONTENT_BOTTOM - 300, "Future Process")


def _process_flow(b: SvgBuilder, t: Template) -> None:
    b.label(200, 400, "●", size=16)
    b.placeholder(280, 380, 140, 56, "Step 1", rx=6)
    b.placeholder(500, 392, 56, 56, "?", rx=28)
    b.placeholder(620, 380, 140, 56, "Step 2", rx=6)
    b.label(900, 400, "◎", size=16)


def _workflow_swimlanes(b: SvgBuilder, t: Template) -> None:
    _bpmn_swimlanes(b, t)


def _value_stream(b: SvgBuilder, t: Template) -> None:
    for i, x in enumerate(range(200, 1400, 200)):
        b.placeholder(x, 320, 140, 80, f"Step {i + 1}")
    b.guide_line(160, 520, W - 160, 520)
    b.label(200, 510, "timeline →", muted=True)


# --- Data ------------------------------------------------------------------

def _erd(b: SvgBuilder, t: Template) -> None:
    b.placeholder(240, 320, 200, 140, "Entity A")
    b.placeholder(760, 280, 200, 140, "Entity B")
    b.placeholder(1280, 340, 200, 140, "Entity C")
    b.guide_line(440, 390, 760, 350)
    b.label(600, 360, "1 — *", anchor="middle", muted=True)


def _conceptual_entities(b: SvgBuilder, t: Template) -> None:
    for i, x in enumerate((300, 760, 1220)):
        b.placeholder(x, 360, 220, 120, f"Entity {i + 1}")


def _logical_entities(b: SvgBuilder, t: Template) -> None:
    for i, x in enumerate((240, 720, 1200)):
        b.class_box(x, 300, 220, 110, f"Entity{i + 1}")


def _physical_tables(b: SvgBuilder, t: Template) -> None:
    _logical_entities(b, t)


def _pipeline_layers(b: SvgBuilder, t: Template) -> None:
    labels = ("Ingest", "Transform", "Serve")
    x = 140
    w = (W - 280) // len(labels) - 20
    for i, lbl in enumerate(labels):
        b.placeholder(x, 360, w, 140, lbl)
        if i < len(labels) - 1:
            b.guide_line(x + w, 430, x + w + 40, 430)
        x += w + 40


def _spatial_flow(b: SvgBuilder, t: Template) -> None:
    labels = ("Source", "ETL", "Service", "Client")
    x = 140
    w = (W - 280) // len(labels) - 20
    for i, lbl in enumerate(labels):
        b.placeholder(x, 360, w, 140, lbl)
        if i < len(labels) - 1:
            b.guide_line(x + w, 430, x + w + 40, 430)
        x += w + 40


def _lakehouse_layers(b: SvgBuilder, t: Template) -> None:
    for i, layer in enumerate(("Bronze", "Silver", "Gold")):
        b.layer_band(160 + i * 520, 300, 480, CONTENT_BOTTOM - 380, layer)


# --- GIS -------------------------------------------------------------------

def _gis_stack(b: SvgBuilder, t: Template) -> None:
    b.placeholder(280, 360, 200, 120, "GIS Server")
    b.placeholder(760, 360, 200, 120, "Spatial DB")
    b.placeholder(1240, 360, 200, 120, "Client App")


def _geospatial_model(b: SvgBuilder, t: Template) -> None:
    b.placeholder(360, 280, 960, CONTENT_BOTTOM - 340, "Feature Dataset")
    for x in (440, 720, 1000):
        b.placeholder(x, 380, 180, 100, "Feature Class")


def _map_layout(b: SvgBuilder, t: Template) -> None:
    b.placeholder(280, 200, 1000, CONTENT_BOTTOM - 320, "Map Frame")
    b.placeholder(1320, CONTENT_BOTTOM - 200, 240, 120, "Legend", muted=True)
    b.placeholder(320, CONTENT_BOTTOM - 120, 200, 32, "Scale Bar", rx=4)
    b.label(1240, CONTENT_BOTTOM - 100, "N ▲", anchor="middle")


def _tool_chain(b: SvgBuilder, t: Template) -> None:
    for i, x in enumerate(range(200, 1400, 280)):
        b.placeholder(x, 400, 200, 80, f"Tool {i + 1}")
        if x < 1200:
            b.guide_line(x + 200, 440, x + 280, 440)


# --- Cloud -----------------------------------------------------------------

def _cloud_provider(b: SvgBuilder, t: Template) -> None:
    provider = t.layout_config[0] if t.layout_config else "Cloud"
    b.placeholder(300, 220, 1200, CONTENT_BOTTOM - 280, f"{provider} VPC")
    for lbl, x in (("Compute", 420), ("Storage", 760), ("Database", 1100)):
        b.placeholder(x, 360, 220, 120, lbl)


def _multi_cloud(b: SvgBuilder, t: Template) -> None:
    for i, cloud in enumerate(("AWS", "Azure", "GCP")):
        b.placeholder(200 + i * 520, 300, 440, CONTENT_BOTTOM - 380, cloud)
    b.solid_box(760, 220, 280, 60, "Integration Layer")


def _serverless(b: SvgBuilder, t: Template) -> None:
    b.solid_box(360, 360, 200, 80, "API Gateway")
    b.placeholder(760, 360, 200, 80, "Function")
    b.placeholder(1160, 360, 200, 80, "Datastore")
    b.guide_line(560, 400, 760, 400)
    b.guide_line(960, 400, 1160, 400)


def _migration(b: SvgBuilder, t: Template) -> None:
    b.placeholder(240, 300, 480, CONTENT_BOTTOM - 360, "On-Premises")
    b.placeholder(1080, 300, 480, CONTENT_BOTTOM - 360, "Cloud")
    b.label(860, 460, "migration →", anchor="middle", size=18, muted=True)


def _cost_optimization(b: SvgBuilder, t: Template) -> None:
    for lbl, x in (("Spend", 280), ("Resources", 760), ("Optimizations", 1240)):
        b.placeholder(x, 340, 320, CONTENT_BOTTOM - 400, lbl)


# --- DevOps ----------------------------------------------------------------

def _pipeline_stages(b: SvgBuilder, t: Template) -> None:
    stages = ("Source", "Build", "Test", "Deploy")
    for i, stage in enumerate(stages):
        b.placeholder(180 + i * 420, 380, 340, 120, stage)
        if i < len(stages) - 1:
            b.guide_line(520 + i * 420, 440, 600 + i * 420, 440)


def _devops_toolchain(b: SvgBuilder, t: Template) -> None:
    tools = ("Plan", "Code", "Build", "Test", "Release", "Operate")
    for i, tool in enumerate(tools):
        b.placeholder(120 + i * 280, 360, 220, 100, tool)


def _gitops(b: SvgBuilder, t: Template) -> None:
    b.placeholder(280, 380, 200, 100, "Git Repo")
    b.placeholder(760, 380, 200, 100, "Operator")
    b.placeholder(1240, 380, 200, 100, "Cluster")
    b.guide_line(480, 430, 760, 430)
    b.guide_line(960, 430, 1240, 430)
    b.guide_line(1340, 480, 380, 520)


def _observability(b: SvgBuilder, t: Template) -> None:
    for i, sig in enumerate(("Logs", "Metrics", "Traces", "Dashboards")):
        b.placeholder(200 + i * 400, 360, 300, 140, sig)


def _iac(b: SvgBuilder, t: Template) -> None:
    b.placeholder(320, 360, 280, 120, "IaC Definitions")
    b.placeholder(1080, 360, 280, 120, "Cloud Resources")
    b.guide_line(600, 420, 1080, 420)


def _service_mesh(b: SvgBuilder, t: Template) -> None:
    b.solid_box(760, 240, 280, 72, "Control Plane")
    b.placeholder(360, 420, 960, CONTENT_BOTTOM - 500, "Data Plane / Services")
    for x in (440, 720, 1000):
        b.placeholder(x, 500, 140, 80, "Sidecar")


LAYOUTS: Dict[str, LayoutFn] = {
    "class_diagram": _class_diagram,
    "object_diagram": _object_diagram,
    "component_diagram": _component_diagram,
    "deployment_diagram": _deployment_diagram,
    "package_diagram": _package_diagram,
    "composite_structure": _composite_structure,
    "use_case_diagram": _use_case_diagram,
    "sequence_diagram": _sequence_diagram,
    "activity_diagram": _activity_diagram,
    "state_machine": _state_machine,
    "communication_diagram": _communication_diagram,
    "interaction_overview": _interaction_overview,
    "timing_diagram": _timing_diagram,
    "profile_diagram": _profile_diagram,
    "layered_stack": _layered_stack,
    "tier_columns": _tier_columns,
    "grid_blocks": _grid_blocks,
    "service_blocks": _service_blocks,
    "microservices": _microservices,
    "event_driven": _event_driven,
    "hexagonal": _hexagonal,
    "concentric": _concentric,
    "c4_context": _c4_context,
    "c4_container": _c4_container,
    "c4_component": _c4_component,
    "solution_blocks": _solution_blocks,
    "hub_spoke": _hub_spoke,
    "layered_flow": _layered_flow,
    "security_zones": _security_zones,
    "infra_blocks": _infra_blocks,
    "network_topology": _network_topology,
    "cloud_vpc": _cloud_vpc,
    "deployment_envs": _deployment_envs,
    "container_cluster": _container_cluster,
    "kubernetes": _kubernetes,
    "ha_active_standby": _ha_active_standby,
    "dr_sites": _dr_sites,
    "charter_sections": _charter_sections,
    "wbs_tree": _wbs_tree,
    "gantt": _gantt,
    "milestone_timeline": _milestone_timeline,
    "roadmap": _roadmap,
    "pert_network": _pert_network,
    "cpm_network": _cpm_network,
    "risk_matrix": _risk_matrix,
    "heat_map": _heat_map,
    "threat_tree": _threat_tree,
    "allocation_matrix": _allocation_matrix,
    "org_chart": _org_chart,
    "stakeholder_map": _stakeholder_map,
    "quadrant_matrix": _quadrant_matrix,
    "influence_network": _influence_network,
    "venn_three": _venn_three,
    "raci_matrix": _raci_matrix,
    "register_table": _register_table,
    "bpmn_swimlanes": _bpmn_swimlanes,
    "dfd": _dfd,
    "side_by_side": _side_by_side,
    "process_flow": _process_flow,
    "workflow_swimlanes": _workflow_swimlanes,
    "value_stream": _value_stream,
    "erd": _erd,
    "conceptual_entities": _conceptual_entities,
    "logical_entities": _logical_entities,
    "physical_tables": _physical_tables,
    "pipeline_layers": _pipeline_layers,
    "lakehouse_layers": _lakehouse_layers,
    "gis_stack": _gis_stack,
    "geospatial_model": _geospatial_model,
    "map_layout": _map_layout,
    "tool_chain": _tool_chain,
    "spatial_flow": _spatial_flow,
    "cloud_provider": _cloud_provider,
    "multi_cloud": _multi_cloud,
    "serverless": _serverless,
    "migration": _migration,
    "cost_optimization": _cost_optimization,
    "pipeline_stages": _pipeline_stages,
    "devops_toolchain": _devops_toolchain,
    "gitops": _gitops,
    "observability": _observability,
    "iac": _iac,
    "service_mesh": _service_mesh,
}
