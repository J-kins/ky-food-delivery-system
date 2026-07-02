"""
core/models.py
──────────────
Pydantic v2 schemas for the entire Project Charter input specification.
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class Project(BaseModel):
    name: str
    sponsor: str = ""
    manager: str = ""
    start_date: str = ""
    end_date: str = ""
    department: str = ""
    version: str = "1.0"


class Vision(BaseModel):
    statement: str
    mission: str = ""


class Objective(BaseModel):
    id: str
    description: str
    measurable_criteria: str = ""


class Scope(BaseModel):
    in_scope: List[str] = Field(default_factory=list)
    out_of_scope: List[str] = Field(default_factory=list)
    boundaries: str = ""


class Stakeholder(BaseModel):
    id: str
    name: str
    role: str = ""
    organization: str = ""
    power: Literal["High", "Low"] = "Low"
    interest: Literal["High", "Low"] = "Low"
    expectations: str = ""


class Risk(BaseModel):
    id: str
    description: str
    likelihood: int = 1   # 1-5
    impact: int = 1       # 1-5
    mitigation: str = ""


class Milestone(BaseModel):
    id: str
    name: str
    date: str
    deliverable: str = ""
    is_critical: bool = False


class BudgetBreakdown(BaseModel):
    personnel: float = 0
    hardware: float = 0
    software: float = 0
    training: float = 0
    contingency: float = 0


class Budget(BaseModel):
    total: float
    currency: str = "USD"
    breakdown: Optional[BudgetBreakdown] = None


class Approval(BaseModel):
    role: str
    name: str
    date: str = ""


class TeamMember(BaseModel):
    id: str
    name: str
    role: str
    reports_to: Optional[str] = None


class DiagramsConfig(BaseModel):
    problem_tree: Dict[str, Any] = Field(default_factory=dict)
    stakeholder_map: Dict[str, Any] = Field(default_factory=dict)
    system_context: Dict[str, Any] = Field(default_factory=dict)
    org_chart: Dict[str, Any] = Field(default_factory=dict)
    scope_boundary: Dict[str, Any] = Field(default_factory=dict)
    milestone_timeline: Dict[str, Any] = Field(default_factory=dict)


class CharterSpec(BaseModel):
    project: Project
    vision: Vision
    objectives: List[Objective] = Field(default_factory=list)
    scope: Scope = Field(default_factory=Scope)
    stakeholders: List[Stakeholder] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    risks: List[Risk] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)
    budget: Optional[Budget] = None
    success_criteria: List[str] = Field(default_factory=list)
    approvals: List[Approval] = Field(default_factory=list)
    team: List[TeamMember] = Field(default_factory=list)
    diagrams: DiagramsConfig = Field(default_factory=DiagramsConfig)
