from __future__ import annotations

import logging
from typing import Any, Dict, List

from calculators.timeline_calculator import TimelineCalculator
from config.settings import PAGE_SIZES_IN, apply_aspose_diagram_license
from renderers import aspose_renderer as asp

log = logging.getLogger(__name__)


class MilestoneChartBuilder:
    """Orchestrates timeline calculation and milestone chart Visio rendering."""

    def __init__(self, spec: Dict[str, Any]):
        if "milestone_chart" in spec:
            self.config = spec["milestone_chart"]
        else:
            self.config = spec
        self.styling = self.config.get("styling", {})
        self.calculator = TimelineCalculator(self.config)
        self.diagram = None
        self.page = None
        self.timeline_y = self.calculator.total_height / 2.0
        self.band_height = self.styling.get("timeline_height", 1.0)

    def _setup_page(self) -> None:
        layout = self.config.get("layout", {})
        page_size = layout.get("page_size", "A2")
        w, h = PAGE_SIZES_IN.get(page_size, PAGE_SIZES_IN["A2"])
        if layout.get("orientation", "landscape") == "portrait":
            w, h = h, w
        self.calculator.total_width = w
        self.calculator.total_height = h
        self.calculator.chart_width = w - 2 * self.calculator.margin
        self.calculator.pixels_per_day = self.calculator.chart_width / self.calculator.total_days
        self.timeline_y = h / 2.0 + 1.0

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

    def _draw_header(self) -> None:
        title = self.config.get("title", "Milestone Chart")
        project = self.config.get("project_name", "")
        ver = self.config.get("version", "")
        date = self.config.get("date", "")
        lines = [title]
        if project:
            lines.append(project)
        meta = " | ".join(p for p in (f"v{ver}" if ver else "", date) if p)
        if meta:
            lines.append(meta)
        self._rect(
            self.calculator.total_width / 2,
            self.calculator.total_height - self.calculator.margin - 0.6,
            self.calculator.total_width - 2 * self.calculator.margin,
            1.2,
            text="\n".join(lines),
            fill="#1a237e",
            border="#1a237e",
            bold=True,
            font_size=11.0,
            no_border=True,
        )

    def _draw_phases(self) -> None:
        for phase in self.config.get("phases", []):
            band = self.calculator.calculate_band(phase["start"], phase["end"])
            self._rect(
                band["x"],
                self.timeline_y - self.band_height / 2 - 0.3,
                band["width"],
                self.band_height,
                text=phase["name"],
                fill=phase.get("color", "#E0E0E0"),
                border=phase.get("color", "#E0E0E0"),
                font_size=8.0,
                no_border=True,
            )

    def _draw_axis(self) -> None:
        left = self.calculator.margin
        right = self.calculator.total_width - self.calculator.margin
        asp.draw_line(self.page, left, self.timeline_y, right, self.timeline_y)

        self._rect(
            left + 1.0,
            self.timeline_y - 1.2,
            2.5,
            0.5,
            text=self.config["start_date"],
            fill="#ECEFF1",
            border="#90A4AE",
            font_size=7.0,
        )
        self._rect(
            right - 1.0,
            self.timeline_y - 1.2,
            2.5,
            0.5,
            text=self.config["end_date"],
            fill="#ECEFF1",
            border="#90A4AE",
            font_size=7.0,
        )

        spacing = self.config.get("layout", {}).get("grid_spacing", "months")
        days_step = 30 if spacing == "months" else (7 if spacing == "weeks" else 1)
        y1 = self.timeline_y - 0.3
        y2 = self.timeline_y + 0.3
        x = left
        while x <= right:
            asp.draw_line(self.page, x, y1, x, y2)
            x += days_step * self.calculator.pixels_per_day

    def _draw_milestones(self) -> None:
        toggle_up = True
        size = self.styling.get("milestone_size", 0.5)
        crit_color = self.styling.get("critical_color", "#E53935")
        normal_color = self.styling.get("normal_color", "#4CAF50")

        for milestone in sorted(self.config.get("milestones", []), key=lambda m: m["date"]):
            x = self.calculator.date_to_x(milestone["date"])
            is_crit = milestone.get("is_critical", False)
            color = crit_color if is_crit else normal_color
            y_offset = 2.5 if toggle_up else -2.5
            my = self.timeline_y + y_offset

            self._rect(
                x,
                my,
                size,
                size,
                text="◆",
                fill=color,
                border=color,
                font_size=12.0,
                no_border=True,
            )
            asp.draw_line(self.page, x, self.timeline_y, x, my)

            text_y = my + 0.8 if toggle_up else my - 0.8
            crit_tag = " [CRITICAL]" if is_crit else ""
            cat = milestone.get("category", "")
            cat_line = f"\n({cat})" if cat and cat != "General" else ""
            label = f"{milestone['date']}\n{milestone['name']}{crit_tag}{cat_line}"
            self._rect(
                x,
                text_y,
                3.5,
                1.2,
                text=label,
                fill="#FFFFFF",
                border="#E0E0E0",
                font_size=7.5,
                bold=is_crit,
            )
            toggle_up = not toggle_up

    def _draw_details_table(self) -> None:
        milestones: List[Dict] = sorted(
            self.config.get("milestones", []),
            key=lambda m: m["date"],
        )
        if not milestones:
            return

        lines = ["MILESTONE DETAILS", "ID | Date | Name | Category | Critical"]
        for m in milestones:
            crit = "Yes" if m.get("is_critical") else "No"
            cat = m.get("category", "General")
            desc = m.get("description", "")
            line = f"{m['id']} | {m['date']} | {m['name']} | {cat} | {crit}"
            if desc:
                line += f" — {desc[:40]}"
            lines.append(line)

        row_h = 0.35
        table_h = min(3.5, 0.8 + len(lines) * row_h)
        self._rect(
            self.calculator.total_width / 2,
            self.calculator.margin + table_h / 2,
            self.calculator.total_width - 2 * self.calculator.margin,
            table_h,
            text="\n".join(lines),
            fill="#FAFAFA",
            border="#BDBDBD",
            font_size=7.0,
        )

    def _draw_summary(self) -> None:
        critical_count = sum(1 for m in self.config.get("milestones", []) if m.get("is_critical"))
        text = (
            f"TIMELINE SUMMARY  |  {self.config['start_date']} to {self.config['end_date']}  |  "
            f"{self.calculator.total_days} days  |  "
            f"{len(self.config.get('phases', []))} phases  |  "
            f"{len(self.config.get('milestones', []))} milestones  |  "
            f"{critical_count} critical"
        )
        self._rect(
            self.calculator.total_width / 2,
            self.calculator.margin + 0.4,
            self.calculator.total_width - 2 * self.calculator.margin,
            0.7,
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
        self.page.setName("Milestone Chart")
        self._setup_page()

        log.info(
            "Drawing milestone chart (%d phases, %d milestones)…",
            len(self.config.get("phases", [])),
            len(self.config.get("milestones", [])),
        )

        self._draw_header()
        self._draw_phases()
        self._draw_axis()
        self._draw_milestones()
        self._draw_details_table()
        self._draw_summary()

    def save(self, output_path: str) -> None:
        if self.diagram is None:
            raise RuntimeError("Call build() before save()")
        asp.save_diagram(self.diagram, output_path)
