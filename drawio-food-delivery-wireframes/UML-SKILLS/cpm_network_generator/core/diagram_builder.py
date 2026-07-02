from __future__ import annotations

import logging
from typing import Dict, List, Tuple

from calculators.cpm_calculator import CPMCalculator
from config.settings import PAGE_SIZES_IN, apply_aspose_diagram_license
from renderers import aspose_renderer as asp
from renderers.layout_engine import LayoutEngine

log = logging.getLogger(__name__)


class CPMNetworkBuilder:
    """Orchestrates CPM calculation and Visio AON diagram rendering."""

    def __init__(self, spec: Dict):
        self.config = spec
        self.styling = self.config.get("styling", {})
        self.page_width = 59.4
        self.page_height = 42.0
        self.diagram = None
        self.page = None
        self.positions: Dict[str, Dict[str, float]] = {}
        self._calculate_cpm()

    def _setup_page(self) -> None:
        layout = self.config.get("layout", {})
        page_size = layout.get("page_size", "A2")
        w, h = PAGE_SIZES_IN.get(page_size, PAGE_SIZES_IN["A2"])
        if layout.get("orientation", "landscape") == "portrait":
            w, h = h, w
        self.page_width = w
        self.page_height = h
        props = self.page.getPageSheet().getPageProps()
        props.getPageWidth().setValue(w)
        props.getPageHeight().setValue(h)

    def _calculate_cpm(self) -> None:
        self.cpm = CPMCalculator(self.config.get("activities", []))
        self.activities = self.cpm.activities
        self.activity_map = self.cpm.activity_map

    def _layout(self) -> None:
        engine = LayoutEngine(
            self.activities,
            self.config,
            page_width=self.page_width,
            page_height=self.page_height,
        )
        self.positions = engine.calculate()

    @staticmethod
    def _edge_points(from_pos: Dict, to_pos: Dict) -> Tuple[float, float, float, float]:
        x1 = from_pos["x"] + from_pos.get("w", 3.2) / 2
        y1 = from_pos["y"]
        x2 = to_pos["x"] - to_pos.get("w", 3.2) / 2
        y2 = to_pos["y"]
        return x1, y1, x2, y2

    def _format_node_text(self, act: Dict) -> str:
        units = act.get("duration_units", "weeks")
        unit_short = "wks" if units.startswith("week") else "days"
        text = f"[{act['id']}] {act['name']}\n"
        text += f"Duration: {act['duration']} {unit_short}\n"
        if self.styling.get("show_es_ef", True):
            text += f"ES: {act.get('es', 0)}    EF: {act.get('ef', 0)}\n"
        if self.styling.get("show_ls_lf", True):
            text += f"LS: {act.get('ls', 0)}    LF: {act.get('lf', 0)}\n"
        if self.styling.get("show_slack", True):
            slack_txt = f"Slack: {act.get('slack', 0)}"
            if act.get("is_critical"):
                slack_txt += "  [CRITICAL]"
            text += f"{slack_txt}\n"
        preds = act.get("predecessors", [])
        if self.styling.get("show_predecessors", True):
            p_str = ", ".join(
                p["id"] if isinstance(p, dict) else p for p in preds
            ) if preds else "None"
            text += f"Predecessors: {p_str}"
        return text

    def _critical_path_ids(self) -> List[str]:
        return [a["id"] for a in self.activities if a.get("is_critical")]

    def _project_duration(self) -> int:
        return max((a.get("ef", 0) for a in self.activities), default=0)

    def build(self) -> None:
        apply_aspose_diagram_license()
        asp.reset_counter()
        self.diagram = asp.new_diagram()
        self.page = self.diagram.getPages().get(0)
        self.page.setName("CPM Network")
        self._setup_page()
        self._layout()

        log.info(
            "Drawing CPM network (%d activities, %d critical)…",
            len(self.activities),
            len(self._critical_path_ids()),
        )

        title = self.config.get("title", "CPM Network Diagram")
        project = self.config.get("project_name", "")
        ver = self.config.get("version", "")
        date = self.config.get("date", "")
        header = title
        if project:
            header += f"\n{project}"
        meta = " | ".join(p for p in (f"v{ver}" if ver else "", date) if p)
        if meta:
            header += f"\n{meta}"

        margin = self.config.get("layout", {}).get("margin", 0.5)
        asp.add_text_box(
            self.page,
            self.page_width / 2,
            self.page_height - margin - 0.6,
            self.page_width - 2 * margin,
            1.2,
            header,
            font_size=12.0,
        )

        node_w = self.styling.get("node_width", 3.2)
        node_h = self.styling.get("node_height", 2.2)

        for act in self.activities:
            pos = self.positions[act["id"]]
            is_critical = act.get("is_critical", False)
            fill = "#FFEBEE" if is_critical else "#E3F2FD"
            border = (
                self.styling.get("critical_path_color", "#E53935")
                if is_critical
                else "#1565C0"
            )
            border_w = 3.0 if is_critical else 1.5
            pos_with_size = {**pos, "w": node_w, "h": node_h}
            self.positions[act["id"]] = pos_with_size

            asp.add_cpm_node(
                self.page,
                x=pos["x"],
                y=pos["y"],
                w=node_w,
                h=node_h,
                text=self._format_node_text(act),
                fill_color=fill,
                border_color=border,
                border_width=border_w,
                font_family=self.styling.get("font_family", "Arial"),
                font_size=self.styling.get("font_size", 9.0),
                is_critical=is_critical,
            )

        for act in self.activities:
            to_pos = self.positions[act["id"]]
            for pred in act.get("predecessors", []):
                pid = pred["id"] if isinstance(pred, dict) else pred
                p_type = pred.get("type", "FS") if isinstance(pred, dict) else "FS"
                p_lag = pred.get("lag", 0) if isinstance(pred, dict) else 0
                from_pos = self.positions.get(pid)
                if not from_pos:
                    continue

                both_critical = act.get("is_critical") and self.activity_map[pid].get("is_critical")
                color = (
                    self.styling.get("critical_path_color", "#E53935")
                    if both_critical
                    else "#666666"
                )
                width = 2.0 if both_critical else 1.0

                label = ""
                if p_type != "FS" or p_lag != 0:
                    label = p_type
                    if p_lag > 0:
                        label += f"+{p_lag}"
                    elif p_lag < 0:
                        label += str(p_lag)

                x1, y1, x2, y2 = self._edge_points(from_pos, to_pos)
                asp.add_connector(self.page, x1, y1, x2, y2, color, width, label)

        cp = " → ".join(self._critical_path_ids())
        summary = (
            f"CPM SUMMARY  |  Project Duration: {self._project_duration()} weeks  |  "
            f"Critical Activities: {len(self._critical_path_ids())}\n"
            f"Critical Path: {cp}"
        )
        asp.add_cpm_node(
            self.page,
            self.page_width / 2,
            margin + 0.8,
            self.page_width - 2 * margin,
            1.4,
            summary,
            fill_color="#ECEFF1",
            border_color="#90A4AE",
            border_width=1.0,
            font_family=self.styling.get("font_family", "Arial"),
            font_size=8.0,
        )

    def save(self, output_path: str) -> None:
        if self.diagram is None:
            raise RuntimeError("Call build() before save()")
        asp.save_diagram(self.diagram, output_path)
