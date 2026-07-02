"""Construct the Kanban board Visio page."""
from __future__ import annotations

import logging
from typing import Any, Dict

from calculators.grid_calculator import GridCalculator
from calculators.metrics_calculator import compute_metrics, format_metrics_text
from config.settings import PAGE_SIZES_IN, apply_aspose_diagram_license
from renderers import aspose_helpers as asp

log = logging.getLogger(__name__)

_PRIORITY_COLORS = {
    "High": "#FFCDD2",
    "Medium": "#FFF9C4",
    "Low": "#C8E6C9",
}


class KanbanChartBuilder:
    """Orchestrates grid calculation and Aspose.Diagram drawing."""

    def __init__(self, spec: Dict[str, Any]):
        if "kanban_chart" in spec:
            self.config = spec["kanban_chart"]
        else:
            self.config = spec
        self.calculator = GridCalculator(self.config)
        self.diagram = None
        self.page = None
        self.font = self.config.get("styling", {}).get("font_family", "Arial")
        self.show_wip = self.config.get("styling", {}).get("show_wip_limits", True)
        self.metrics = compute_metrics(self.config)

    def _setup_page(self) -> None:
        layout = self.config.get("layout", {})
        page_size = layout.get("page_size", "A2")
        w, h = PAGE_SIZES_IN.get(page_size, PAGE_SIZES_IN["A2"])
        if layout.get("orientation", "landscape") == "portrait":
            w, h = h, w
        self.calculator.total_width = w
        self.calculator.total_height = h
        props = self.page.getPageSheet().getPageProps()
        props.getPageWidth().setValue(w)
        props.getPageHeight().setValue(h)

    def _rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        text: str = "",
        fill: str = "#FFFFFF",
        border: str = "#CCCCCC",
        bold: bool = False,
        font_size: float = 9.0,
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
            fill_color=fill,
            border_color=border,
            font_size=font_size,
            font_bold=bold,
            no_fill=no_fill,
            no_border=no_border,
        )

    def _draw_title(self) -> None:
        title = self.config.get("title", "Kanban Chart")
        project = self.config.get("project_name", "")
        sprint = self.config.get("sprint", "")
        date = self.config.get("date", "")
        lines = [title]
        if project:
            lines.append(project)
        meta = " | ".join(p for p in (sprint, date) if p)
        if meta:
            lines.append(meta)
        self._rect(
            x=self.calculator.total_width / 2,
            y=self.calculator.total_height - 1.2,
            w=self.calculator.total_width - 1.0,
            h=2.0,
            text="\n".join(lines),
            fill="#1a237e",
            border="#1a237e",
            bold=True,
            font_size=12.0,
            no_border=True,
        )

    def _draw_column_headers(self) -> None:
        col_counts = {c["id"]: 0 for c in self.calculator.columns}
        for item in self.config.get("work_items", []):
            if item["status"] in col_counts:
                col_counts[item["status"]] += 1

        y = self.calculator.total_height - self.calculator.header_height - 1.5
        for col in self.calculator.columns:
            x = self.calculator.get_column_x(col["id"]) + self.calculator.col_width / 2
            count = col_counts.get(col["id"], 0)
            wip = col.get("wip_limit")
            if self.show_wip and wip is not None:
                sub = f"WIP: {count}/{wip}"
            elif wip is None:
                sub = f"Items: {count}"
            else:
                sub = f"Items: {count}"
            text = f"{col['name']}\n{sub}"
            over_wip = wip is not None and count > wip
            fill = col.get("color", "#E3F2FD")
            if over_wip:
                fill = "#FFEBEE"
            self._rect(
                x=x,
                y=y,
                w=self.calculator.col_width - 0.1,
                h=1.2,
                text=text,
                fill=fill,
                border=col.get("text_color", "#0D47A1"),
                bold=True,
                font_size=8.0,
            )

    def _draw_swimlane_labels(self) -> None:
        for swimlane in self.calculator.swimlanes:
            y = self.calculator.get_swimlane_y(swimlane["id"]) - self.calculator.swim_height / 2
            icon = swimlane.get("icon", "")
            label = f"{icon} {swimlane['name']}".strip()
            self._rect(
                x=self.calculator.margin + self.calculator.swimlane_label_width / 2,
                y=y,
                w=self.calculator.swimlane_label_width - 0.1,
                h=self.calculator.swim_height - 0.1,
                text=label,
                fill=swimlane.get("color", "#1a237e"),
                border=swimlane.get("color", "#1a237e"),
                bold=True,
                font_size=9.0,
                no_border=True,
            )

    def _draw_grid_lines(self) -> None:
        left = self.calculator.margin + self.calculator.swimlane_label_width
        right = self.calculator.total_width - self.calculator.margin
        top = self.calculator.total_height - self.calculator.header_height - 2.0
        bottom = self.calculator.metrics_height + self.calculator.margin

        for col in self.calculator.columns:
            x = self.calculator.get_column_x(col["id"])
            asp.draw_line(self.page, x, bottom, x, top)
        asp.draw_line(self.page, right, bottom, right, top)

        for swimlane in self.calculator.swimlanes:
            y = self.calculator.get_swimlane_y(swimlane["id"]) - self.calculator.swim_height
            asp.draw_line(self.page, left, y, right, y)
        asp.draw_line(self.page, left, bottom, right, bottom)

    def _draw_column_backgrounds(self) -> None:
        left = self.calculator.margin + self.calculator.swimlane_label_width
        top = self.calculator.total_height - self.calculator.header_height - 2.0
        bottom = self.calculator.metrics_height + self.calculator.margin
        for col in self.calculator.columns:
            x = self.calculator.get_column_x(col["id"]) + self.calculator.col_width / 2
            self._rect(
                x=x,
                y=(top + bottom) / 2,
                w=self.calculator.col_width - 0.05,
                h=top - bottom,
                fill=col.get("color", "#FAFAFA"),
                no_border=True,
            )

    def _draw_cards(self) -> None:
        styling = self.config.get("styling", {})
        pri_colors = styling.get("priority_colors", _PRIORITY_COLORS)
        for item in self.config.get("work_items", []):
            geom = self.calculator.calculate_card_pos(item)
            color = pri_colors.get(item.get("priority", "Medium"), "#FFFFFF")
            pri_tag = item.get("priority", "")[0] if item.get("priority") else ""
            text = (
                f"[{item['id']}] {item['title']}\n"
                f"{item.get('type', '')} | {pri_tag} | {item.get('assignee', '')}"
            )
            self._rect(
                x=geom["x"],
                y=geom["y"],
                w=geom["w"],
                h=geom["h"],
                text=text,
                fill=color,
                border="#BDBDBD",
                font_size=7.5,
            )

    def _draw_metrics_bar(self) -> None:
        text = "METRICS\n" + format_metrics_text(self.metrics)
        self._rect(
            x=self.calculator.total_width / 2,
            y=self.calculator.metrics_height / 2 + self.calculator.margin / 2,
            w=self.calculator.total_width - 1.0,
            h=self.calculator.metrics_height,
            text=text,
            fill="#ECEFF1",
            border="#90A4AE",
            font_size=8.0,
        )

    def build(self) -> None:
        apply_aspose_diagram_license()
        asp.reset_counter()
        self.diagram = asp.new_diagram()
        self.page = self.diagram.getPages().get(0)
        self.page.setName("Kanban Board")
        self._setup_page()

        log.info("Drawing Kanban grid (%d columns, %d swimlanes, %d cards)…",
                 len(self.calculator.columns),
                 len(self.calculator.swimlanes),
                 len(self.config.get("work_items", [])))

        self._draw_title()
        self._draw_column_backgrounds()
        self._draw_grid_lines()
        self._draw_swimlane_labels()
        self._draw_column_headers()
        self._draw_cards()
        self._draw_metrics_bar()

    def save(self, output_path: str) -> None:
        if self.diagram is None:
            raise RuntimeError("Call build() before save()")
        asp.save_diagram(self.diagram, output_path)
