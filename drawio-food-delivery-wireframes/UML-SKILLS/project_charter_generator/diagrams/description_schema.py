"""Diagram description schema and required charter diagram IDs."""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

DiagramFormat = Literal["graphviz", "d2"]

REQUIRED_WORD_DIAGRAMS: List[str] = [
    "problem_tree",
    "stakeholder_matrix",
    "scope_boundary",
    "org_chart",
    "milestone_timeline",
    "risk_matrix",
    "system_context",
]

DIAGRAM_SPLIT_FILES: Dict[str, str] = {
    "problem_tree": "charter_diagram_problem_tree_input.json",
    "stakeholder_matrix": "charter_diagram_stakeholder_matrix_input.json",
    "scope_boundary": "charter_diagram_scope_boundary_input.json",
    "org_chart": "charter_diagram_org_chart_input.json",
    "milestone_timeline": "charter_diagram_milestone_timeline_input.json",
    "risk_matrix": "charter_diagram_risk_matrix_input.json",
    "system_context": "charter_diagram_system_context_input.json",
}


class DiagramNode(BaseModel):
    id: str
    label: str
    shape: str = "box"
    fill: str = "#FFFFFF"
    border: str = "#666666"
    text_color: str = "#000000"
    group: Optional[str] = None


class DiagramEdge(BaseModel):
    from_id: str = Field(alias="from")
    to_id: str = Field(alias="to")
    label: str = ""
    style: str = "solid"
    color: str = "#666666"

    model_config = {"populate_by_name": True}


class DiagramDescription(BaseModel):
    """Structured diagram spec consumed by Graphviz or D2 compilers."""

    id: str
    title: str
    format: DiagramFormat = "graphviz"
    engine: str = "dot"
    rankdir: str = "TB"
    nodes: List[DiagramNode] = Field(default_factory=list)
    edges: List[DiagramEdge] = Field(default_factory=list)
    source: Optional[str] = None
    caption: Optional[str] = None

    model_config = {"populate_by_name": True}


class DiagramDescriptionFile(BaseModel):
    diagram_description: DiagramDescription


def parse_description_file(data: Dict[str, Any]) -> DiagramDescription:
    return DiagramDescriptionFile.model_validate(data).diagram_description
