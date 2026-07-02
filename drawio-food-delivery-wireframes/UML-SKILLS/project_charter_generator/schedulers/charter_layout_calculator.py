"""Vertical section layout for the single-page Project Charter Summary Diagram."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CharterSection:
    id: str
    title: str
    height: float
    x: float
    y: float
    width: float


SECTION_COLORS: Dict[str, Dict[str, str]] = {
    "vision": {"bg": "#E3F2FD", "border": "#1565C0", "header": "#1565C0"},
    "overview": {"bg": "#F5F5F5", "border": "#78909C", "header": "#78909C"},
    "objectives": {"bg": "#E8F5E9", "border": "#2E7D32", "header": "#2E7D32"},
    "scope": {"bg": "#FFF3E0", "border": "#E65100", "header": "#E65100"},
    "stakeholders": {"bg": "#F3E5F5", "border": "#6A1B9A", "header": "#6A1B9A"},
    "constraints": {"bg": "#FFEBEE", "border": "#C62828", "header": "#C62828"},
    "milestones": {"bg": "#E0F7FA", "border": "#00838F", "header": "#00838F"},
    "budget": {"bg": "#FFF8E1", "border": "#FFB300", "header": "#FFB300"},
    "approvals": {"bg": "#F5F5F5", "border": "#78909C", "header": "#78909C"},
}


class CharterLayoutCalculator:
    """Compute Y positions for stacked charter sections on A2 landscape."""

    def __init__(
        self,
        page_width: float = 59.4,
        page_height: float = 42.0,
        margin: float = 0.5,
        section_gap: float = 0.25,
        title_block_height: float = 1.4,
        footer_height: float = 0.6,
    ):
        self.page_width = page_width
        self.page_height = page_height
        self.margin = margin
        self.section_gap = section_gap
        self.title_block_height = title_block_height
        self.footer_height = footer_height
        self.available_width = page_width - (margin * 2)
        self.sections: List[CharterSection] = []
        self.current_y = page_height - margin - (title_block_height / 2) - 0.3

    def calculate_section_heights(self, data: Dict[str, Any]) -> Dict[str, float]:
        objectives = data.get("objectives", [])
        stakeholders = data.get("stakeholders", [])
        milestones = data.get("milestones", [])
        approvals = data.get("approvals", [])

        return {
            "vision": 1.1,
            "overview": 1.3,
            "objectives": 0.55 + min(len(objectives), 6) * 0.38 + 0.15,
            "scope": 1.7,
            "stakeholders": 0.55 + min(len(stakeholders), 5) * 0.38 + 0.15,
            "constraints": 1.5,
            "milestones": 0.55 + min(len(milestones), 5) * 0.38 + 0.15,
            "budget": 2.2,
            "approvals": 0.55 + min(len(approvals), 4) * 0.42 + 0.15,
        }

    def plan_sections(self, data: Dict[str, Any]) -> List[CharterSection]:
        """Place all sections top-to-bottom; scale down uniformly if overflow."""
        heights = self.calculate_section_heights(data)
        order = [
            ("vision", "VISION"),
            ("overview", "PROJECT OVERVIEW"),
            ("objectives", "OBJECTIVES"),
            ("scope", "SCOPE"),
            ("stakeholders", "STAKEHOLDERS"),
            ("constraints", "CONSTRAINTS & ASSUMPTIONS"),
            ("milestones", "MILESTONES & TIMELINE"),
            ("budget", "BUDGET SUMMARY"),
            ("approvals", "APPROVALS"),
        ]

        raw_total = sum(heights[k] for k, _ in order) + self.section_gap * (len(order) - 1)
        bottom_limit = self.margin + self.footer_height + 0.4
        top_limit = self.page_height - self.margin - self.title_block_height - 0.5
        available = top_limit - bottom_limit
        scale = min(1.0, available / raw_total) if raw_total > 0 else 1.0

        self.sections = []
        self.current_y = top_limit
        for section_id, title in order:
            h = heights[section_id] * scale
            section = CharterSection(
                id=section_id,
                title=title,
                height=h,
                x=self.margin + self.available_width / 2,
                y=self.current_y - h / 2,
                width=self.available_width,
            )
            self.sections.append(section)
            self.current_y -= h + (self.section_gap * scale)

        return self.sections

    def get_section_positions(self) -> Dict[str, Dict[str, float]]:
        return {
            s.id: {"x": s.x, "y": s.y, "width": s.width, "height": s.height}
            for s in self.sections
        }

    @staticmethod
    def section_style(section_id: str) -> Dict[str, str]:
        return SECTION_COLORS.get(
            section_id,
            {"bg": "#FFFFFF", "border": "#BDBDBD", "header": "#1a237e"},
        )
