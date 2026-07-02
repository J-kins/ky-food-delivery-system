from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class PertTask(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    duration: float
    duration_units: Optional[str] = "weeks"
    optimistic: Optional[float] = None
    most_likely: Optional[float] = None
    pessimistic: Optional[float] = None
    dependencies: List[str] = Field(default_factory=list)
    is_start: bool = False

class Styling(BaseModel):
    theme: str = "enterprise_blue"
    font_family: str = "Arial"
    font_size: float = 9.0
    show_three_point: bool = False

class Layout(BaseModel):
    orientation: str = "landscape"
    page_size: str = "A2"
    margin: float = 0.5
    node_width: float = 2.0
    node_height: float = 1.2
    horizontal_spacing: float = 1.0
    vertical_spacing: float = 1.0

class PertChart(BaseModel):
    title: str = "PERT Chart"
    project_name: str = ""
    version: str = "1.0"
    date: str = ""
    description: Optional[str] = ""
    tasks: List[PertTask]
    styling: Styling = Field(default_factory=Styling)
    layout: Layout = Field(default_factory=Layout)

class PertSpec(BaseModel):
    pert_chart: PertChart
