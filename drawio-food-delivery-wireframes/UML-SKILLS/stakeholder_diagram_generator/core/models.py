from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field


class Stakeholder(BaseModel):
    id: str
    name: str
    title: str
    organization: str
    category: Literal["Internal", "External"]
    type: Optional[Literal["Primary", "Secondary"]] = "Primary"
    power: Literal["High", "Medium", "Low"]
    interest: Literal["High", "Medium", "Low"]
    influence: Literal["High", "Medium", "Low"]
    legitimacy: Literal["High", "Medium", "Low"]
    urgency: Literal["High", "Medium", "Low"]
    expectations: str
    needs: str
    engagement_strategy: Optional[Literal["Manage Closely", "Keep Satisfied", "Keep Informed", "Monitor", "auto"]] = "auto"
    communication_preference: Optional[str] = ""
    contact: Optional[str] = ""
    status: Literal["Active", "Inactive", "Blocked"]
    notes: Optional[str] = ""

class StakeholderRegister(BaseModel):
    title: str = "Stakeholder Register"
    project_name: str = ""
    version: str = "1.0"
    stakeholders: List[Stakeholder]

class MatrixQuadrant(BaseModel):
    id: str
    label: str
    power: str
    interest: str
    color: str
    text_color: str
    strategy: str
    engagement_activities: List[str]
    stakeholders: List[str] = Field(default_factory=list)

class Quadrants(BaseModel):
    key_players: MatrixQuadrant
    keep_satisfied: MatrixQuadrant
    keep_informed: MatrixQuadrant
    monitor: MatrixQuadrant

class PowerInterestMatrix(BaseModel):
    title: str = "Power-Interest Matrix"
    project_name: str = ""
    version: str = "1.0"
    date: str = ""
    quadrants: Optional[Quadrants] = None
    styling: Dict = Field(default_factory=dict)
    layout: Dict = Field(default_factory=dict)

# Influence Network and Salience models are similar
class InfluenceNetwork(BaseModel):
    title: str = "Influence Network"
    nodes: Optional[List[Dict]] = Field(default_factory=list)
    edges: Optional[List[Dict]] = Field(default_factory=list)

class SalienceModel(BaseModel):
    title: str = "Salience Model"
    
class StakeholderMap(BaseModel):
    title: str = "Stakeholder Map"

class StakeholderSpec(BaseModel):
    stakeholder_register: Optional[StakeholderRegister] = None
    power_interest_matrix: Optional[PowerInterestMatrix] = None
    influence_network: Optional[InfluenceNetwork] = None
    salience_model: Optional[SalienceModel] = None
    stakeholder_map: Optional[StakeholderMap] = None
