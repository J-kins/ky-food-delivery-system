from typing import List, Optional, Literal, Dict, Any, Union
from pydantic import BaseModel, Field


class PredecessorObj(BaseModel):
    id: str
    type: Literal["FS", "SS", "FF", "SF"] = "FS"
    lag: int = 0


class Activity(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    duration: int
    duration_units: str = "weeks"
    predecessors: List[Union[str, PredecessorObj]] = Field(default_factory=list)
    is_start: bool = False
    is_end: bool = False
    lag: int = 0  # Support legacy lag parameter


class Styling(BaseModel):
    theme: str = "enterprise_blue"
    font_family: str = "Arial"
    font_size: float = 9.0
    critical_path_color: str = "#E53935"
    critical_path_text_color: str = "#FFFFFF"
    node_width: float = 3.2
    node_height: float = 2.2
    show_es_ef: bool = True
    show_ls_lf: bool = True
    show_slack: bool = True
    show_predecessors: bool = True
    shadow_enabled: bool = True


class Layout(BaseModel):
    orientation: Literal["landscape", "portrait"] = "landscape"
    page_size: Literal["A2", "A3", "A4"] = "A2"
    margin: float = 0.5
    level_spacing: float = 3.0
    node_spacing: float = 1.5


class CpmNetwork(BaseModel):
    title: str = "CPM Network Diagram"
    project_name: str = ""
    version: str = "1.0"
    date: str = ""
    description: Optional[str] = ""

    activities: List[Activity]
    
    styling: Styling = Field(default_factory=Styling)
    layout: Layout = Field(default_factory=Layout)


class CpmSpec(BaseModel):
    cpm_network: CpmNetwork
