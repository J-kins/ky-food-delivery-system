from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field


class Category(BaseModel):
    id: str
    name: str
    budget: float
    actual: Optional[float] = None
    color: Optional[str] = None
    text_color: Optional[str] = None
    notes: Optional[str] = None


class LineItem(BaseModel):
    category: str
    item: str
    qty: int = 1
    unit_cost: float
    total: float


class MonthlyBurn(BaseModel):
    month: str
    planned: float
    actual: Optional[float] = None


class Styling(BaseModel):
    font_family: str = "Arial"
    font_size: float = 9.0
    header_fill: str = "#1a237e"
    header_text: str = "#FFFFFF"
    alt_row_fill: str = "#F5F5F5"
    total_row_fill: str = "#E3F2FD"
    positive_variance: str = "#4CAF50"
    negative_variance: str = "#E53935"


class Layout(BaseModel):
    orientation: Literal["landscape", "portrait"] = "landscape"
    page_size: Literal["A2", "A3", "A4"] = "A2"
    margin: float = 0.5


class DashboardOptions(BaseModel):
    show_kpi_bar: bool = True
    show_bar_chart: bool = True
    show_pie_chart: bool = True
    show_burn_rate_chart: bool = True
    kpi_colors: Dict[str, str] = Field(default_factory=dict)


class Budget(BaseModel):
    title: str = "Budget Breakdown"
    project_name: str = ""
    version: str = "1.0"
    date: str = ""
    currency: str = "USD"
    exchange_rate_note: Optional[str] = None
    budget_period: Optional[str] = None

    categories: List[Category]
    line_items: List[LineItem]
    monthly_burn_rate: List[MonthlyBurn]

    styling: Styling = Field(default_factory=Styling)
    layout: Layout = Field(default_factory=Layout)
    dashboard: Optional[DashboardOptions] = None


class BudgetSpec(BaseModel):
    budget: Budget
