from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field

class Phase(BaseModel):
    id: str
    name: str
    start: str
    end: str
    color: str = "#E0E0E0"
    text_color: str = "#000000"

class Milestone(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    date: str
    phase: Optional[str] = None
    is_critical: bool = False
    category: Optional[str] = "General"

class Styling(BaseModel):
    theme: str = "enterprise_blue"
    font_family: str = "Arial"
    font_size: float = 9.0
    timeline_height: float = 1.0
    milestone_size: float = 0.5
    critical_color: str = "#E53935"
    normal_color: str = "#4CAF50"


class Layout(BaseModel):
    orientation: Literal["landscape", "portrait"] = "landscape"
    page_size: Literal["A1", "A2", "A3", "A4"] = "A2"
    margin: float = 0.5
    grid_spacing: Literal["days", "weeks", "months"] = "months"

class MilestoneChart(BaseModel):
    title: str = "Milestone Chart"
    project_name: str = ""
    version: str = "1.0"
    date: str = ""
    start_date: str
    end_date: str
    description: Optional[str] = ""
    phases: List[Phase] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)
    styling: Styling = Field(default_factory=Styling)
    layout: Layout = Field(default_factory=Layout)

class MilestoneSpec(BaseModel):
    milestone_chart: MilestoneChart
