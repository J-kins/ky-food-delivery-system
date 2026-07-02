"""Construct the Budget Dashboard Visio page via Aspose.Diagram."""
from __future__ import annotations

import logging
from typing import Any, Dict, List

from config.settings import PAGE_SIZES_IN, apply_aspose_diagram_license
from visio import aspose_helpers as asp

log = logging.getLogger(__name__)

_DEFAULT_DASHBOARD = {
    "show_kpi_bar": True,
    "show_bar_chart": True,
    "show_pie_chart": True,
    "show_burn_rate_chart": True,
    "kpi_colors": {
        "total_budget": "#1a237e",
        "actual_spent": "#C62828",
        "remaining": "#2E7D32",
        "period": "#4E342E",
    },
}


class BudgetVisioBuilder:
    """Builds a single-page budget dashboard .vsdx file."""

    def __init__(self, spec) -> None:
        self.config: Dict[str, Any] = spec.budget.model_dump()
        self.categories: List[dict] = self.config["categories"]
        self.burn_rate: List[dict] = self.config["monthly_burn_rate"]
        self.layout = self.config.get("layout", {})
        self.dashboard = {**_DEFAULT_DASHBOARD, **self.config.get("dashboard", {})}
        self.font_family = self.config.get("styling", {}).get("font_family", "Arial")
        self._compute_totals()
        self.diagram = None
        self.page = None
        self.page_width = 59.4
        self.page_height = 42.0

    def _compute_totals(self) -> None:
        self.total_budget = sum(c["budget"] for c in self.categories)
        self.total_actual = sum(
            c.get("actual", 0) for c in self.categories if c.get("actual") is not None
        )
        self.remaining = self.total_budget - self.total_actual

    def _setup_page(self) -> None:
        page_size = self.layout.get("page_size", "A2")
        w, h = PAGE_SIZES_IN.get(page_size, PAGE_SIZES_IN["A2"])
        if self.layout.get("orientation", "landscape") == "portrait":
            w, h = h, w
        self.page_width = w
        self.page_height = h
        props = self.page.getPageSheet().getPageProps()
        props.getPageWidth().setValue(w)
        props.getPageHeight().setValue(h)

    def _add_rectangle(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        text: str = "",
        fill_color: str = "#FFFFFF",
        text_color: str = "#000000",
        border_color: str = "#E0E0E0",
        bold: bool = False,
        font_size: float = 12.0,
        no_fill: bool = False,
        no_border: bool = False,
    ) -> None:
        asp.add_rectangle(
            self.page,
            x=x,
            y=y,
            w=w,
            h=h,
            text=text,
            fill_color=fill_color,
            text_color=text_color,
            border_color=border_color,
            font_size=font_size,
            font_bold=bold,
            no_fill=no_fill,
            no_border=no_border,
        )

    def add_title_block(self) -> None:
        title = self.config.get("title", "Budget Breakdown - Visual Dashboard")
        project = self.config.get("project_name", "")
        version = self.config.get("version", "1.0")
        date = self.config.get("date", "")
        text = f"{title}\n{project} | Version {version} | {date}"
        self._add_rectangle(
            x=self.page_width / 2,
            y=self.page_height - 1.5,
            w=self.page_width - 1.0,
            h=1.5,
            text=text,
            fill_color="#1a237e",
            text_color="#FFFFFF",
            border_color="#1a237e",
            bold=True,
            font_size=14.0,
            no_border=True,
        )

    def add_kpi_bar(self) -> None:
        if not self.dashboard.get("show_kpi_bar", True):
            return
        colors = self.dashboard.get("kpi_colors", {})
        margin = self.layout.get("margin", 0.5)
        box_width = (self.page_width - margin * 2) / 4
        y = self.page_height - 3.5
        kpi_items = [
            (f"TOTAL BUDGET: ${self.total_budget:,.0f}", colors.get("total_budget", "#1a237e")),
            (f"ACTUAL SPENT: ${self.total_actual:,.0f}", colors.get("actual_spent", "#C62828")),
            (f"REMAINING: ${self.remaining:,.0f}", colors.get("remaining", "#2E7D32")),
            (f"PERIOD: {self.config.get('budget_period', '')}", colors.get("period", "#4E342E")),
        ]
        for idx, (label, color) in enumerate(kpi_items):
            x = margin + (box_width / 2) + (idx * box_width)
            self._add_rectangle(
                x=x,
                y=y,
                w=box_width - 0.2,
                h=1.0,
                text=label,
                fill_color=color,
                text_color="#FFFFFF",
                border_color=color,
                bold=True,
                font_size=11.0,
                no_border=True,
            )

    def add_bar_chart(self) -> None:
        if not self.dashboard.get("show_bar_chart", True):
            return
        margin = self.layout.get("margin", 0.5)
        x_label_width = 4.0
        max_bar_width = self.page_width / 2 - x_label_width - margin - 1.0
        bar_height = 1.0
        bar_gap = 0.5
        container_x = margin + (self.page_width / 2 - margin) / 2
        container_y = self.page_height / 2 + 1.0
        container_h = len(self.categories) * (bar_height + bar_gap) + 2.0
        self._add_rectangle(
            x=container_x,
            y=container_y,
            w=(self.page_width / 2 - margin) - 0.5,
            h=container_h,
            text="",
            fill_color="#FAFAFA",
            border_color="#E0E0E0",
        )
        self._add_rectangle(
            x=container_x,
            y=container_y + container_h / 2 - 0.5,
            w=(self.page_width / 2 - margin) - 0.5,
            h=1.0,
            text="COST BREAKDOWN BY CATEGORY",
            bold=True,
            no_fill=True,
            no_border=True,
        )
        y_start = container_y + container_h / 2 - 2.0
        for idx, cat in enumerate(self.categories):
            y = y_start - idx * (bar_height + bar_gap)
            bar_w = (cat["budget"] / self.total_budget) * max_bar_width if self.total_budget else 0
            self._add_rectangle(
                x=margin + x_label_width / 2 + 0.2,
                y=y,
                w=x_label_width,
                h=bar_height,
                text=cat["name"],
                no_fill=True,
                no_border=True,
                bold=True,
            )
            self._add_rectangle(
                x=margin + x_label_width + bar_w / 2 + 0.5,
                y=y,
                w=max(bar_w, 0.05),
                h=bar_height,
                text="",
                fill_color=cat.get("color", "#1565C0"),
                no_border=True,
            )
            pct = round((cat["budget"] / self.total_budget) * 100) if self.total_budget else 0
            self._add_rectangle(
                x=margin + x_label_width + bar_w + 1.5,
                y=y,
                w=2.0,
                h=bar_height,
                text=f"${cat['budget']:,.0f}\n{pct}%",
                font_size=8.0,
                no_fill=True,
                no_border=True,
            )

    def add_pie_chart_panel(self) -> None:
        if not self.dashboard.get("show_pie_chart", True):
            return
        margin = self.layout.get("margin", 0.5)
        container_w = self.page_width / 2 - margin - 0.5
        container_x = self.page_width - margin - container_w / 2
        bar_height = 1.0
        bar_gap = 0.5
        container_h = len(self.categories) * (bar_height + bar_gap) + 2.0
        container_y = self.page_height / 2 + 1.0
        lines = [
            f"• {c['name']}: {round((c['budget'] / self.total_budget) * 100)}%"
            for c in self.categories
        ] if self.total_budget else []
        body = "DISTRIBUTION BY CATEGORY\n\n" + "\n".join(lines)
        self._add_rectangle(
            x=container_x,
            y=container_y,
            w=container_w,
            h=container_h,
            text=body,
            fill_color="#FAFAFA",
            border_color="#E0E0E0",
            bold=True,
            font_size=10.0,
        )

    def add_burn_rate_chart(self) -> None:
        if not self.dashboard.get("show_burn_rate_chart", True) or not self.burn_rate:
            return
        margin = self.layout.get("margin", 0.5)
        chart_w = self.page_width - margin * 2
        chart_h = 8.0
        chart_x = self.page_width / 2
        chart_y = chart_h / 2 + margin
        self._add_rectangle(
            x=chart_x,
            y=chart_y,
            w=chart_w,
            h=chart_h,
            text="MONTHLY BURN RATE (Planned vs Actual)",
            fill_color="#FAFAFA",
            border_color="#E0E0E0",
            bold=True,
            font_size=11.0,
        )
        max_val = max(
            max(m.get("planned", 0) for m in self.burn_rate),
            max((m.get("actual") or 0) for m in self.burn_rate),
            1,
        )
        inner_w = chart_w - 2.0
        inner_left = margin + 1.0
        inner_bottom = chart_y - chart_h / 2 + 1.5
        inner_height = chart_h - 2.5
        n = len(self.burn_rate)
        group_w = inner_w / max(n, 1)
        bar_w = group_w * 0.35
        for idx, month_data in enumerate(self.burn_rate):
            cx = inner_left + (idx + 0.5) * group_w
            planned_h = (month_data.get("planned", 0) / max_val) * inner_height
            actual = month_data.get("actual")
            actual_h = ((actual or 0) / max_val) * inner_height if actual is not None else 0
            if planned_h > 0:
                self._add_rectangle(
                    x=cx - bar_w / 2,
                    y=inner_bottom + planned_h / 2,
                    w=bar_w,
                    h=planned_h,
                    text="",
                    fill_color="#1565C0",
                    no_border=True,
                )
            if actual_h > 0:
                self._add_rectangle(
                    x=cx + bar_w / 2,
                    y=inner_bottom + actual_h / 2,
                    w=bar_w,
                    h=actual_h,
                    text="",
                    fill_color="#C62828",
                    no_border=True,
                )
            label = month_data.get("month", "")[:3]
            self._add_rectangle(
                x=cx,
                y=inner_bottom - 0.4,
                w=group_w,
                h=0.6,
                text=label,
                font_size=7.0,
                no_fill=True,
                no_border=True,
            )

    def build(self) -> None:
        apply_aspose_diagram_license()
        asp.reset_counter()
        self.diagram = asp.new_diagram()
        self.page = self.diagram.getPages().get(0)
        self.page.setName("Budget Dashboard")
        self._setup_page()
        self.add_title_block()
        self.add_kpi_bar()
        self.add_bar_chart()
        self.add_pie_chart_panel()
        self.add_burn_rate_chart()

    def save(self, output_path: str) -> None:
        if self.diagram is None:
            raise RuntimeError("Call build() before save()")
        asp.save_diagram(self.diagram, output_path)
