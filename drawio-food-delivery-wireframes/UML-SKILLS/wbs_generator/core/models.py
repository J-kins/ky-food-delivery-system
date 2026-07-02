from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class LevelMeta(BaseModel):
    id: Optional[str] = None
    name: str = ""
    description: Optional[str] = ""
    color: str = "#1a237e"
    text_color: str = "#FFFFFF"
    border_color: Optional[str] = None
    shape_style: str = "rounded_rectangle"


class Levels(BaseModel):
    level_0: LevelMeta
    level_1: LevelMeta = Field(default_factory=lambda: LevelMeta(name="Phases/Deliverables", color="#1565C0"))
    level_2: LevelMeta = Field(default_factory=lambda: LevelMeta(name="Work Packages", color="#64B5F6", text_color="#333333"))
    level_3: LevelMeta = Field(
        default_factory=lambda: LevelMeta(
            name="Tasks/Activities", color="#FFFFFF", text_color="#333333", border_color="#64B5F6"
        )
    )


class WBSNodeL3(BaseModel):
    id: str
    name: str
    description: str
    level: Literal[3] = 3
    effort_hours: int


class WBSNodeL2(BaseModel):
    id: str
    name: str
    description: str
    level: Literal[2] = 2
    children: List[WBSNodeL3]


class WBSBranch(BaseModel):
    id: str
    name: str
    description: str
    level: Literal[1] = 1
    children: List[WBSNodeL2]


class Styling(BaseModel):
    theme: str = "enterprise_blue"
    font_family: str = "Arial"
    font_size: float = 10.0
    layout_style: Literal["tree", "org_chart"] = "tree"
    shadow_enabled: bool = True
    corner_radius: float = 6.0
    box_spacing: float = 0.3


class Layout(BaseModel):
    orientation: Literal["landscape", "portrait"] = "landscape"
    page_size: Literal["A1", "A2", "A3", "A4"] = "A2"
    margin: float = 0.5
    level_spacing: float = 1.5
    box_height: float = 0.8


class WBSChart(BaseModel):
    title: str = "Work Breakdown Structure"
    project_name: str = ""
    version: str = "1.0"
    date: str = ""
    description: Optional[str] = ""
    levels: Levels
    branches: List[WBSBranch]
    styling: Styling = Field(default_factory=Styling)
    layout: Layout = Field(default_factory=Layout)


class WBSSpec(BaseModel):
    wbs: WBSChart
