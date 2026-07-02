"""Build the WBS tree diagram in Visio format."""
from __future__ import annotations

import logging
from typing import Any, Dict

from config.settings import PAGE_SIZES_IN, apply_aspose_diagram_license
from core.validator import index_nodes
from renderers import aspose_helpers as asp
from renderers.layout_engine import LEVEL_STYLES, LayoutEngine

log = logging.getLogger(__name__)


class WBSBuilder:
    """Orchestrates layout calculation and Aspose.Diagram rendering."""

    def __init__(self, config: Dict[str, Any]):
        if "wbs" in config:
            self.config = config["wbs"]
        else:
            self.config = config
        self.page_width = 59.4
        self.page_height = 42.0
        self.diagram = None
        self.page = None
        self.positions: Dict[str, Dict] = {}
        self.node_index: Dict[str, Dict] = index_nodes(self.config)

    def _visio_y(self, layout_y: float) -> float:
        """Convert top-down layout Y to Visio page coordinates."""
        return self.page_height - layout_y

    def _level_style(self, level: int) -> Dict[str, Any]:
        base = dict(LEVEL_STYLES.get(level, LEVEL_STYLES[3]))
        key = f"level_{level}"
        meta = self.config.get("levels", {}).get(key, {})
        if meta.get("color"):
            base["fill_color"] = meta["color"]
        if meta.get("text_color"):
            base["text_color"] = meta["text_color"]
        if meta.get("border_color"):
            base["border_color"] = meta["border_color"]
        return base

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

    def _node_label(self, node_id: str, pos: Dict) -> str:
        node = self.node_index.get(node_id, {})
        name = node.get("name") or pos.get("name", node_id)
        label = f"{node_id} {name}"
        if pos["level"] == 3 and node.get("effort_hours") is not None:
            label += f"\n({node['effort_hours']}h)"
        return label

    def _draw_title(self) -> None:
        title = self.config.get("title", "Work Breakdown Structure")
        project = self.config.get("project_name", "")
        version = self.config.get("version", "")
        date = self.config.get("date", "")
        lines = [title]
        if project:
            lines.append(project)
        meta = " | ".join(p for p in (f"v{version}" if version else "", date) if p)
        if meta:
            lines.append(meta)
        asp.add_rectangle(
            self.page,
            x=self.page_width / 2,
            y=self.page_height - 0.9,
            w=self.page_width - 1.0,
            h=1.4,
            text="\n".join(lines),
            fill_color="#1a237e",
            border_color="#1a237e",
            font_size=12.0,
            font_bold=True,
            no_border=True,
        )

    def _draw_nodes(self) -> None:
        for node_id, pos in self.positions.items():
            style = self._level_style(pos["level"])
            asp.add_rectangle(
                self.page,
                x=pos["x"],
                y=self._visio_y(pos["y"]),
                w=pos["w"],
                h=pos["h"],
                text=self._node_label(node_id, pos),
                fill_color=style["fill_color"],
                border_color=style.get("border_color", style["fill_color"]),
                border_width=style.get("line_width", 1.0),
                font_size=style.get("font_size", 9),
                font_bold=style.get("font_bold", False),
            )

    def _draw_connectors(self) -> None:
        for node_id, pos in self.positions.items():
            parent_id = pos.get("parent")
            if not parent_id or parent_id not in self.positions:
                continue
            parent = self.positions[parent_id]
            parent_bottom_layout = parent["y"] + parent["h"] / 2
            child_top_layout = pos["y"] - pos["h"] / 2
            px = parent["x"]
            cx = pos["x"]
            py = self._visio_y(parent_bottom_layout)
            cy = self._visio_y(child_top_layout)
            mid_y = (py + cy) / 2
            asp.draw_line(self.page, px, py, px, mid_y)
            asp.draw_line(self.page, px, mid_y, cx, mid_y)
            asp.draw_line(self.page, cx, mid_y, cx, cy)

    def _draw_legend(self) -> None:
        levels = self.config.get("levels", {})
        lines = ["WBS LEGEND"]
        for lvl in (1, 2, 3):
            meta = levels.get(f"level_{lvl}", {})
            name = meta.get("name", f"Level {lvl}")
            lines.append(f"L{lvl}: {name}")
        total_tasks = sum(
            1 for n in self.node_index.values() if str(n.get("id", "")).count(".") == 2
        )
        lines.append(f"Total tasks: {total_tasks}")
        asp.add_rectangle(
            self.page,
            x=self.page_width - 3.5,
            y=1.2,
            w=6.5,
            h=1.8,
            text="\n".join(lines),
            fill_color="#ECEFF1",
            border_color="#90A4AE",
            font_size=8.0,
        )

    def build(self) -> None:
        apply_aspose_diagram_license()
        asp.reset_counter()
        self.diagram = asp.new_diagram()
        self.page = self.diagram.getPages().get(0)
        self.page.setName("WBS Diagram")
        self._setup_page()

        engine = LayoutEngine(self.page_width, self.page_height, self.config)
        self.positions = engine.calculate_tree(self.config)

        log.info(
            "Drawing WBS tree (%d nodes, %d L1 branches)…",
            len(self.positions),
            len(self.config.get("branches", [])),
        )

        self._draw_title()
        self._draw_connectors()
        self._draw_nodes()
        self._draw_legend()

    def save(self, output_path: str) -> None:
        if self.diagram is None:
            raise RuntimeError("Call build() before save()")
        asp.save_diagram(self.diagram, output_path)
