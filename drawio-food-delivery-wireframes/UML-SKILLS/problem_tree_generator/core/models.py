from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class CoreProblem(BaseModel):
    id: str = "TRUNK"
    statement: str
    description: Optional[str] = ""


class ProblemNode(BaseModel):
    id: str
    statement: str
    description: Optional[str] = ""


class Styling(BaseModel):
    theme: str = "enterprise_blue"
    font_family: str = "Arial"
    font_size: float = 10.0
    arrow_style: Literal["curved", "straight", "orthogonal"] = "curved"
    shadow_enabled: bool = True
    corner_radius: float = 8.0


class Layout(BaseModel):
    orientation: str = "top_to_bottom"
    page_size: Literal["A2", "A3", "A4"] = "A3"
    margin: float = 0.5
    node_spacing: float = 0.5   # inches between sibling nodes
    rank_spacing: float = 1.2   # inches between tier rows


class ProblemTree(BaseModel):
    title: str = "Problem Tree"
    project_name: str = ""
    version: str = "1.0"
    date: str = ""
    core_problem: CoreProblem
    roots: List[ProblemNode] = Field(default_factory=list)
    branches: List[ProblemNode] = Field(default_factory=list)
    leaf: List[ProblemNode] = Field(default_factory=list)
    styling: Styling = Field(default_factory=Styling)
    layout: Layout = Field(default_factory=Layout)


class ProblemTreeSpec(BaseModel):
    problem_tree: ProblemTree
