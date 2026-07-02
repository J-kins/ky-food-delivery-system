"""
core/models.py
───────────────
Pydantic v2 schemas for robust JSON/YAML input validation.
These models enforce the schema defined in SKILL.md and provide
default values where permissible.
"""
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field


class Participant(BaseModel):
    id: str
    name: str = ""
    class_name: str = ""
    instance_name: str = ""
    type: Literal["actor", "control", "entity", "boundary", "service", "database", "system"] = "control"
    stereotype: str = ""

    # Optional explicit styling / layout overrides
    color: Optional[str] = None
    text_color: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None


class Link(BaseModel):
    id: str
    source: str
    target: str
    type: Literal["association", "dependency"] = "association"
    label: str = ""
    line_style: Literal["solid", "dashed"] = "solid"


class Message(BaseModel):
    id: str
    source: str = Field(alias="from")
    target: str = Field(alias="to")
    sequence: str = ""
    label: str
    type: Literal["synchronous", "asynchronous", "creation", "return"] = "synchronous"
    return_value: Optional[str] = None
    guard: Optional[str] = None

    class Config:
        populate_by_name = True


class Group(BaseModel):
    id: str
    name: str = "System Boundary"
    label: str = ""
    participants: List[str]
    color: str = "#E3F2FD"
    border_color: str = "#1565C0"


class Styling(BaseModel):
    theme: str = "enterprise_blue"
    font_family: str = "Arial"
    font_size: float = 9.0
    shadow_enabled: bool = True
    link_width: float = 1.0
    participant_types: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    message_colors: Dict[str, str] = Field(default_factory=dict)


class Layout(BaseModel):
    orientation: Literal["landscape", "portrait"] = "landscape"
    page_size: Literal["A2", "A3", "A4"] = "A2"
    margin: float = 0.5
    participant_spacing: float = 3.5
    vertical_spacing: float = 3.0
    auto_layout: bool = False


class CommunicationDiagram(BaseModel):
    title: str = "Communication Diagram"
    system_name: str = ""
    version: str = "1.0"
    date: str = ""
    description: str = ""
    
    participants: List[Participant]
    links: List[Link]
    messages: List[Message]
    groups: List[Group] = Field(default_factory=list)
    
    styling: Styling = Field(default_factory=Styling)
    layout: Layout = Field(default_factory=Layout)


class CommunicationDiagramSpec(BaseModel):
    communication_diagram: CommunicationDiagram
