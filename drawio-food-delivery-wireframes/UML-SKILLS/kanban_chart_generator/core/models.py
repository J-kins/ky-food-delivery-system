from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field

class KanbanColumn(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    wip_limit: Optional[int] = None
    color: str = "#E3F2FD"
    text_color: str = "#0D47A1"
    order: int

class Swimlane(BaseModel):
    id: str
    name: str
    color: str = "#1a237e"
    text_color: str = "#FFFFFF"
    icon: Optional[str] = ""

class WorkItem(BaseModel):
    id: str
    title: str
    type: Literal["Feature", "Bug", "Task", "Story", "Epic"]
    status: str
    priority: Literal["High", "Medium", "Low"]
    assignee: str
    swimlane_id: str
    size: Optional[int] = None
    tags: List[str] = Field(default_factory=list)

class Styling(BaseModel):
    theme: str = "enterprise_blue"
    font_family: str = "Arial"
    font_size: float = 9.0
    card_width: float = 2.0
    card_height: float = 1.0
    show_wip_limits: bool = True

class Layout(BaseModel):
    orientation: Literal["landscape", "portrait"] = "landscape"
    page_size: Literal["A1", "A2", "A3", "A4"] = "A2"
    margin: float = 0.5
    cell_padding: float = 0.2

class KanbanChart(BaseModel):
    title: str = "Kanban Chart"
    project_name: str = ""
    version: str = "1.0"
    date: str = ""
    sprint: Optional[str] = ""
    description: Optional[str] = ""
    columns: List[KanbanColumn]
    swimlanes: List[Swimlane]
    work_items: List[WorkItem]
    styling: Styling = Field(default_factory=Styling)
    layout: Layout = Field(default_factory=Layout)

class KanbanSpec(BaseModel):
    kanban_chart: KanbanChart
