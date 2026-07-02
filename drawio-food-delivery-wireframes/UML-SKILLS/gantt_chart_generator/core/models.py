from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field

class Task(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    start: str
    end: str
    completion: int = 0
    dependencies: List[str] = Field(default_factory=list)
    level: int = 1

class Phase(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    color: str = "#1565C0"
    text_color: str = "#FFFFFF"
    tasks: List[Task]

class Milestone(BaseModel):
    id: str
    name: str
    date: str
    dependencies: List[str] = Field(default_factory=list)

class Styling(BaseModel):
    theme: str = "enterprise_blue"
    font_family: str = "Arial"
    font_size: float = 9.0
    bar_height: float = 0.4
    row_height: float = 0.6
    show_percent_complete: bool = False
    critical_path_color: str = "#E53935"

class Layout(BaseModel):
    orientation: Literal["landscape", "portrait"] = "landscape"
    page_size: Literal["A2", "A3", "A4"] = "A2"
    margin: float = 0.5
    grid_spacing: Literal["days", "weeks", "months"] = "weeks"

class GanttChart(BaseModel):
    title: str = "Gantt Chart"
    project_name: str = ""
    version: str = "1.0"
    date: str = ""
    start_date: str
    end_date: str
    phases: List[Phase]
    milestones: Optional[List[Milestone]] = Field(default_factory=list)
    styling: Styling = Field(default_factory=Styling)
    layout: Layout = Field(default_factory=Layout)

class GanttSpec(BaseModel):
    gantt_chart: GanttChart
