"""Auto-build diagram descriptions from charter narrative when split files are absent."""
from __future__ import annotations

from typing import Any, Dict, List

from diagrams.description_schema import DiagramDescription, DiagramEdge, DiagramNode


def build_descriptions_from_payload(payload: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Derive all required diagram descriptions from charter shared data."""
    return {
        "problem_tree": _problem_tree(payload).model_dump(by_alias=True),
        "stakeholder_matrix": _stakeholder_matrix(payload).model_dump(by_alias=True),
        "scope_boundary": _scope_boundary(payload).model_dump(by_alias=True),
        "org_chart": _org_chart(payload).model_dump(by_alias=True),
        "milestone_timeline": _milestone_timeline(payload).model_dump(by_alias=True),
        "risk_matrix": _risk_matrix(payload).model_dump(by_alias=True),
        "system_context": _system_context(payload).model_dump(by_alias=True),
    }


def _problem_tree(payload: Dict[str, Any]) -> DiagramDescription:
    nodes: List[DiagramNode] = []
    edges: List[DiagramEdge] = []
    trunk = payload.get("vision", {}).get("statement", "Core Problem")
    nodes.append(DiagramNode(id="TRUNK", label=trunk, fill="#FFCC80", border="#F57C00"))

    for risk in payload.get("risks", [])[:5]:
        nodes.append(
            DiagramNode(
                id=risk["id"],
                label=f'{risk["id"]}: {risk["description"][:60]}',
                fill="#EF9A9A",
                border="#E53935",
                group="roots",
            )
        )
        edges.append(DiagramEdge(**{"from": risk["id"], "to": "TRUNK"}))

    for obj in payload.get("objectives", [])[:4]:
        nodes.append(
            DiagramNode(
                id=obj["id"],
                label=f'{obj["id"]}: {obj["description"][:60]}',
                fill="#90CAF9",
                border="#1565C0",
                group="branches",
            )
        )
        edges.append(DiagramEdge(**{"from": "TRUNK", "to": obj["id"]}))

    for i, crit in enumerate(payload.get("success_criteria", [])[:3]):
        nid = f"L{i+1}"
        nodes.append(DiagramNode(id=nid, label=crit[:70], fill="#A5D6A7", border="#2E7D32", group="leaves"))
        for obj in payload.get("objectives", [])[:4]:
            edges.append(DiagramEdge(**{"from": obj["id"], "to": nid}))

    return DiagramDescription(
        id="problem_tree",
        title="Problem Tree",
        format="graphviz",
        rankdir="TB",
        nodes=nodes,
        edges=edges,
        caption="Figure 4: Problem Tree",
    )


def _stakeholder_matrix(payload: Dict[str, Any]) -> DiagramDescription:
    nodes = [
        DiagramNode(id="Q_HH", label="KEY PLAYERS", fill="#FFCDD2", group="grid"),
        DiagramNode(id="Q_HL", label="KEEP SATISFIED", fill="#FFE0B2", group="grid"),
        DiagramNode(id="Q_LH", label="KEEP INFORMED", fill="#FFF9C4", group="grid"),
        DiagramNode(id="Q_LL", label="MONITOR", fill="#C8E6C9", group="grid"),
    ]
    edges: List[DiagramEdge] = []
    for sh in payload.get("stakeholders", []):
        nodes.append(
            DiagramNode(
                id=sh["id"],
                label=f'{sh["name"]}\\n{sh.get("role", "")}',
                fill="#FFFFFF",
                border="#1565C0",
            )
        )
    return DiagramDescription(
        id="stakeholder_matrix",
        title="Stakeholder Power-Interest Matrix",
        format="graphviz",
        rankdir="TB",
        nodes=nodes,
        edges=edges,
        caption="Figure 2: Power-Interest Matrix",
    )


def _scope_boundary(payload: Dict[str, Any]) -> DiagramDescription:
    scope = payload.get("scope", {})
    nodes = [
        DiagramNode(id="OUTER", label="OUT OF SCOPE", fill="#FFEBEE", border="#E53935", shape="box"),
        DiagramNode(id="INNER", label="IN SCOPE", fill="#E8F5E9", border="#2E7D32", shape="box"),
    ]
    edges: List[DiagramEdge] = []
    for i, item in enumerate(scope.get("in_scope", [])):
        nid = f"IN_{i}"
        nodes.append(DiagramNode(id=nid, label=item[:50], fill="#C8E6C9", border="#2E7D32"))
    for i, item in enumerate(scope.get("out_of_scope", [])[:4]):
        nid = f"OUT_{i}"
        nodes.append(DiagramNode(id=nid, label=item[:50], fill="#FFCDD2", border="#E53935"))
    return DiagramDescription(
        id="scope_boundary",
        title="Scope Boundary",
        format="graphviz",
        rankdir="LR",
        nodes=nodes,
        edges=edges,
        caption="Figure 1: Scope Boundaries",
    )


def _org_chart(payload: Dict[str, Any]) -> DiagramDescription:
    team = payload.get("team") or []
    if not team:
        project = payload.get("project", {})
        team = [
            {"id": "SPONSOR", "name": project.get("sponsor", "Sponsor"), "role": "Project Sponsor", "reports_to": None},
            {"id": "PM", "name": project.get("manager", "Manager"), "role": "Project Manager", "reports_to": "SPONSOR"},
        ]
    nodes = [
        DiagramNode(id=m["id"], label=f'{m["name"]}\\n{m.get("role", "")}', fill="#64B5F6", border="#1565C0")
        for m in team
    ]
    edges = [
        DiagramEdge(**{"from": m["reports_to"], "to": m["id"]})
        for m in team
        if m.get("reports_to")
    ]
    return DiagramDescription(
        id="org_chart",
        title="Project Org Chart",
        format="graphviz",
        rankdir="TB",
        nodes=nodes,
        edges=edges,
        caption="Figure 3: Project Organization",
    )


def _milestone_timeline(payload: Dict[str, Any]) -> DiagramDescription:
    nodes: List[DiagramNode] = []
    edges: List[DiagramEdge] = []
    prev = None
    for m in payload.get("milestones", []):
        color = "#E53935" if m.get("is_critical") else "#1565C0"
        nodes.append(
            DiagramNode(
                id=m["id"],
                label=f'{m["date"]}\\n{m["name"]}',
                fill=color,
                border=color,
                shape="diamond",
            )
        )
        if prev:
            edges.append(DiagramEdge(**{"from": prev, "to": m["id"]}))
        prev = m["id"]
    return DiagramDescription(
        id="milestone_timeline",
        title="Milestone Timeline",
        format="graphviz",
        rankdir="LR",
        nodes=nodes,
        edges=edges,
        caption="Figure 6: Milestone Timeline",
    )


def _risk_matrix(payload: Dict[str, Any]) -> DiagramDescription:
    nodes: List[DiagramNode] = []
    edges: List[DiagramEdge] = []
    for r in payload.get("risks", []):
        score = int(r.get("likelihood", 1)) * int(r.get("impact", 1))
        color = "#E53935" if score >= 15 else "#FF7043" if score >= 9 else "#FFC107" if score >= 4 else "#66BB6A"
        nodes.append(DiagramNode(id=r["id"], label=r["id"], fill=color, border="#333333", shape="circle"))
    return DiagramDescription(
        id="risk_matrix",
        title="Risk Matrix",
        format="graphviz",
        rankdir="TB",
        nodes=nodes,
        edges=edges,
        caption="Figure 5: Risk Matrix",
    )


def _system_context(payload: Dict[str, Any]) -> DiagramDescription:
    ctx = payload.get("diagrams", {}).get("system_context") or {}
    desc_text = ctx.get("description", "System under development")
    nodes = [
        DiagramNode(id="SYSTEM", label=payload.get("project", {}).get("name", "System"), fill="#1565C0", border="#0D47A1"),
        DiagramNode(id="EXT1", label="External Stakeholders", fill="#E3F2FD", border="#1565C0"),
        DiagramNode(id="EXT2", label="NHIS / Billing", fill="#E3F2FD", border="#1565C0"),
        DiagramNode(id="EXT3", label="Clinic Systems", fill="#E3F2FD", border="#1565C0"),
    ]
    edges = [
        DiagramEdge(**{"from": "EXT1", "to": "SYSTEM", "label": "policy"}),
        DiagramEdge(**{"from": "EXT2", "to": "SYSTEM", "label": "billing"}),
        DiagramEdge(**{"from": "SYSTEM", "to": "EXT3", "label": "patient data"}),
    ]
    return DiagramDescription(
        id="system_context",
        title="System Context",
        format="graphviz",
        rankdir="LR",
        nodes=nodes,
        edges=edges,
        caption=f"Figure: System Context — {desc_text[:40]}",
    )
