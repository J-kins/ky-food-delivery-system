"""Gantt chart SVG to Visio converter."""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from ..base import BaseDiagramConverter

logger = logging.getLogger(__name__)


class GanttChartConverter(BaseDiagramConverter):
    """Convert Gantt chart SVG templates to Visio diagrams."""

    def render_diagram(self) -> None:
        """Render Gantt chart with timeline and task bars."""
        data = self.get_data()
        tokens = self.get_design_tokens()

        # Extract timeline info
        timeline = data.get("timeRange", {})
        start_date = timeline.get("startDate", "2024-01-01")
        end_date = timeline.get("endDate", "2024-12-31")
        granularity = timeline.get("granularity", "weekly")

        logger.info(f"Rendering Gantt: {start_date} to {end_date} ({granularity})")

        # Add title
        self.builder.add_shape(
            "text",
            x=0.5,
            y=0.3,
            width=5.0,
            height=0.4,
            text=data.get("projectName", "Gantt Chart"),
            style={"font_size": 20, "font_weight": "bold", "fill": tokens.get("text", "#1A1A1A")},
        )

        # Add timeline header
        self._add_timeline_header(start_date, end_date, granularity, tokens)

        # Add tasks/phases
        phases = data.get("phases", [])
        task_rows = data.get("tasks", [])
        y_pos = 1.0

        for phase in phases:
            self._add_phase_bar(phase, start_date, y_pos, tokens)
            y_pos += 0.5

        for task in task_rows:
            self._add_task_bar(task, start_date, y_pos, tokens)
            y_pos += 0.35

        logger.debug(f"Added {len(phases)} phases and {len(task_rows)} tasks")

    def _add_timeline_header(self, start: str, end: str, granularity: str, tokens: Dict[str, str]) -> None:
        """Add timeline header with date markers."""
        # Parse dates
        try:
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
        except (ValueError, TypeError):
            logger.warning(f"Invalid date format: {start}, {end}")
            return

        logger.debug(f"Timeline: {start_dt} to {end_dt} ({granularity})")

        # Add month/week headers based on granularity
        if granularity == "weekly":
            current = start_dt
            x_pos = 0.5
            while current <= end_dt:
                week_end = current + timedelta(days=7)
                week_label = f"{current.strftime('%m/%d')} - {week_end.strftime('%m/%d')}"
                self.builder.add_shape(
                    "rectangle",
                    x=x_pos,
                    y=0.7,
                    width=1.0,
                    height=0.25,
                    text=week_label,
                    style={"font_size": 9, "fill": tokens.get("headerBg", "#FAFAFB")},
                )
                current = week_end
                x_pos += 1.0

    def _add_phase_bar(self, phase: Dict[str, Any], start_date: str, y_pos: float, tokens: Dict[str, str]) -> None:
        """Add phase bar to timeline."""
        phase_name = phase.get("name", "Phase")
        phase_start = phase.get("startDate", start_date)
        duration_str = phase.get("duration", "4 weeks")
        status = phase.get("status", "planned")

        # Color based on status
        status_colors = {
            "completed": "#4CAF50",
            "in-progress": "#2196F3",
            "planned": "#FFC107",
            "at-risk": "#FF9800",
            "blocked": "#F44336",
        }
        fill_color = status_colors.get(status, tokens.get("fill", "#E5E5E5"))

        logger.debug(f"Phase: {phase_name} ({status})")

        self.builder.add_shape(
            "rectangle",
            x=0.5,
            y=y_pos,
            width=2.0,
            height=0.4,
            text=f"{phase_name} - {duration_str}",
            style={
                "fill": fill_color,
                "stroke": tokens.get("stroke", "#1A1A1A"),
                "font_size": 11,
            },
        )

    def _add_task_bar(self, task: Dict[str, Any], start_date: str, y_pos: float, tokens: Dict[str, str]) -> None:
        """Add individual task bar."""
        task_name = task.get("name", "Task")
        progress = task.get("progress", 0)

        logger.debug(f"Task: {task_name} ({progress}% complete)")

        self.builder.add_shape(
            "rectangle",
            x=0.5,
            y=y_pos,
            width=1.5,
            height=0.3,
            text=f"{task_name} - {progress}%",
            style={
                "fill": tokens.get("fill", "#E5E5E5"),
                "stroke": tokens.get("stroke", "#1A1A1A"),
                "font_size": 10,
            },
        )
