from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

from config.settings import PAGE_SIZES_IN, apply_aspose_diagram_license
from renderers import aspose_renderer as asp
from schedulers.timeline_calculator import TimelineCalculator

log = logging.getLogger(__name__)


class GanttChartBuilder:
    """Orchestrates timeline calculation and Gantt Visio rendering."""

    def __init__(self, spec: Dict[str, Any]):
        self.config = spec
        self.styling = spec.get("styling", {})
        self.calculator = TimelineCalculator(spec)
        self.diagram = None
        self.page = None
        self.row_height = self.styling.get("row_height", 0.6)
        self.bar_height = self.styling.get("bar_height", 0.4)
        self.current_y = self.calculator.total_height - self.calculator.margin - 2.0
        self.item_positions: Dict[str, Dict[str, float]] = {}

    def _setup_page(self) -> None:
        layout = self.config.get("layout", {})
        page_size = layout.get("page_size", "A2")
        w, h = PAGE_SIZES_IN.get(page_size, PAGE_SIZES_IN["A2"])
        if layout.get("orientation", "landscape") == "portrait":
            w, h = h, w
        self.calculator.total_width = w
        self.calculator.total_height = h
        self.calculator.chart_width = w - self.calculator.left_pane_width - (2 * self.calculator.margin)
        self.calculator.chart_start_x = self.calculator.margin + self.calculator.left_pane_width
        self.calculator.pixels_per_day = self.calculator.chart_width / self.calculator.total_days
        self.current_y = h - self.calculator.margin - 2.0

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
            no_border=no_border,
        )

    def _record_item(self, item_id: str, x: float, y: float, w: float, h: float, start_x: float, end_x: float) -> None:
        self.item_positions[item_id] = {
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "start_x": start_x,
            "end_x": end_x,
        }

    def _draw_header(self) -> None:
        title = self.config.get("title", "Gantt Chart")
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

    def _draw_timeline_axis(self) -> None:
        self._rect(
            self.calculator.chart_start_x + self.calculator.chart_width / 2,
            self.current_y,
            self.calculator.chart_width,
            0.5,
            text=f"{self.config['start_date']}  →  {self.config['end_date']}",
            fill="#ECEFF1",
            border="#90A4AE",
            font_size=8.0,
        )
        self.current_y -= 0.8
        self._draw_grid_lines()

    def _draw_grid_lines(self) -> None:
        spacing = self.config.get("layout", {}).get("grid_spacing", "weeks")
        days_step = 7 if spacing == "weeks" else (30 if spacing == "months" else 1)
        y_top = self.current_y + 0.4
        y_bottom = self.calculator.margin + 1.5
        x = self.calculator.chart_start_x
        while x <= self.calculator.chart_start_x + self.calculator.chart_width:
            asp.draw_line(self.page, x, y_bottom, x, y_top)
            x += days_step * self.calculator.pixels_per_day

    def _draw_phase(self, phase: Dict) -> None:
        tasks = self._flatten_tasks(phase.get("tasks", []))
        bar_data = self.calculator.calculate_phase_rollup(tasks)

        self._rect(
            self.calculator.margin + 2.0,
            self.current_y,
            4.0,
            self.row_height,
            text=phase["name"],
            fill="#FAFAFA",
            border="#BDBDBD",
            bold=True,
        )
        self._rect(
            bar_data["x"],
            self.current_y,
            bar_data["width"],
            self.bar_height,
            text="",
            fill=phase.get("color", "#1565C0"),
            border=phase.get("color", "#1565C0"),
            no_border=True,
        )
        self._record_item(
            phase["id"],
            bar_data["x"],
            self.current_y,
            bar_data["width"],
            self.bar_height,
            bar_data["start_x"],
            bar_data["start_x"] + bar_data["width"],
        )
        self.current_y -= self.row_height

    def _flatten_tasks(self, tasks: List[Dict]) -> List[Dict]:
        flat: List[Dict] = []
        for task in tasks:
            flat.append(task)
            flat.extend(self._flatten_tasks(task.get("children", [])))
        return flat

    def _draw_task(self, task: Dict, color: str) -> None:
        indent = task.get("level", 1) * 0.5
        bar_data = self.calculator.calculate_bar(task["start"], task["end"])

        label = task["name"]
        if self.styling.get("show_percent_complete"):
            label += f" ({task.get('completion', 0)}%)"

        self._rect(
            self.calculator.margin + 2.0 + indent,
            self.current_y,
            4.0,
            self.row_height,
            text=label,
            fill="#FFFFFF",
            border="#E0E0E0",
            font_size=8.0,
        )

        bar_text = f"{task.get('completion', 0)}%" if self.styling.get("show_percent_complete") else ""
        self._rect(
            bar_data["x"],
            self.current_y,
            bar_data["width"],
            self.bar_height,
            text=bar_text,
            fill=color,
            border=color,
            no_border=True,
        )

        completion = task.get("completion", 0)
        if completion and 0 < completion < 100:
            prog_w = bar_data["width"] * (completion / 100.0)
            self._rect(
                bar_data["start_x"] + prog_w / 2,
                self.current_y,
                prog_w,
                self.bar_height * 0.6,
                text="",
                fill="#2E7D32",
                border="#2E7D32",
                no_border=True,
            )

        self._record_item(
            task["id"],
            bar_data["x"],
            self.current_y,
            bar_data["width"],
            self.bar_height,
            bar_data["start_x"],
            bar_data["start_x"] + bar_data["width"],
        )
        self.current_y -= self.row_height

        for child in task.get("children", []):
            self._draw_task(child, color)

    def _draw_milestones(self) -> None:
        for m in self.config.get("milestones", []):
            mx = self.calculator.date_to_x(m["date"])
            self._rect(
                self.calculator.margin + 2.0,
                self.current_y,
                4.0,
                self.row_height,
                text=f"◆ {m['name']}",
                fill="#FFF8E1",
                border="#FFC107",
                font_size=8.0,
            )
            self._rect(
                mx,
                self.current_y,
                0.45,
                0.45,
                text="◆",
                fill="#FFC107",
                border="#F57F17",
                font_size=10.0,
                no_border=True,
            )
            self._record_item(
                m["id"],
                mx,
                self.current_y,
                0.45,
                0.45,
                mx - 0.2,
                mx + 0.2,
            )
            self.current_y -= self.row_height

    def _connector_points(self, from_id: str, to_id: str) -> Optional[Tuple[float, float, float, float]]:
        src = self.item_positions.get(from_id)
        dst = self.item_positions.get(to_id)
        if not src or not dst:
            return None
        x1 = src["end_x"]
        y1 = src["y"]
        x2 = dst["start_x"]
        y2 = dst["y"]
        return x1, y1, x2, y2

    def _draw_dependencies(self) -> None:
        for phase in self.config.get("phases", []):
            for task in self._flatten_tasks(phase.get("tasks", [])):
                for dep in task.get("dependencies", []):
                    pts = self._connector_points(dep, task["id"])
                    if pts:
                        x1, y1, x2, y2 = pts
                        mid_x = (x1 + x2) / 2
                        asp.draw_line(self.page, x1, y1, mid_x, y1)
                        asp.draw_line(self.page, mid_x, y1, mid_x, y2)
                        asp.draw_line(self.page, mid_x, y2, x2, y2)

        for m in self.config.get("milestones", []):
            for dep in m.get("dependencies", []):
                pts = self._connector_points(dep, m["id"])
                if pts:
                    x1, y1, x2, y2 = pts
                    mid_x = (x1 + x2) / 2
                    asp.draw_line(self.page, x1, y1, mid_x, y1)
                    asp.draw_line(self.page, mid_x, y1, mid_x, y2)
                    asp.draw_line(self.page, mid_x, y2, x2, y2)

    def _draw_summary(self) -> None:
        task_count = sum(len(self._flatten_tasks(p.get("tasks", []))) for p in self.config.get("phases", []))
        ms_count = len(self.config.get("milestones", []))
        text = (
            f"SCHEDULE SUMMARY  |  {self.config['start_date']} to {self.config['end_date']}  |  "
            f"{self.calculator.total_days} days  |  "
            f"{len(self.config.get('phases', []))} phases  |  {task_count} tasks  |  {ms_count} milestones"
        )
        self._rect(
            self.calculator.total_width / 2,
            self.calculator.margin + 0.6,
            self.calculator.total_width - 2 * self.calculator.margin,
            0.9,
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
        self.page.setName("Gantt Chart")
        self._setup_page()

        task_count = sum(len(self._flatten_tasks(p.get("tasks", []))) for p in self.config.get("phases", []))
        log.info(
            "Drawing Gantt chart (%d phases, %d tasks, %d milestones)…",
            len(self.config.get("phases", [])),
            task_count,
            len(self.config.get("milestones", [])),
        )

        self._draw_header()
        self._draw_timeline_axis()

        for phase in self.config.get("phases", []):
            self._draw_phase(phase)
            for task in phase.get("tasks", []):
                self._draw_task(task, phase.get("color", "#1565C0"))

        self._draw_milestones()
        self._draw_dependencies()
        self._draw_summary()

    def save(self, output_path: str) -> None:
        if self.diagram is None:
            raise RuntimeError("Call build() before save()")
        asp.save_diagram(self.diagram, output_path)
