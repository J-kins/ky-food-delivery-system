import logging
from typing import Dict, Any, Tuple

from calculators.sequence_calculator import SequenceNumberGenerator
from calculators.position_calculator import PositionCalculator
from config.settings import PAGE_SIZES_IN, apply_aspose_diagram_license
from stylers.color_themes import get_theme, participant_fill, participant_text_color
from stylers.participant_styler import build_participant_label
from stylers.message_styler import get_message_style, format_message_label
from renderers import aspose_renderer as asp

log = logging.getLogger(__name__)


class CommunicationDiagramBuilder:
    """
    Main orchestration class for building Communication Diagrams in Visio format.

    Rendering pipeline:
      1. Title block
      2. System boundary groups (behind participants)
      3. Participant nodes
      4. Structural links (no arrowheads)
      5. Numbered message connectors
      6. Legend
    """

    def __init__(self, spec: Dict[str, Any]):
        self.config = spec["communication_diagram"]
        self.diagram = None
        self.page = None
        self.page_width = 59.4
        self.page_height = 42.0
        self.pos_calc = PositionCalculator(
            self.page_width, self.page_height, self.config.get("layout", {})
        )
        participants = self.config.get("participants", [])
        self.positions = self.pos_calc.calculate(participants)
        self._setup_styles()

    def _setup_page(self) -> None:
        layout = self.config.get("layout", {})
        page_size = layout.get("page_size", "A2")
        w, h = PAGE_SIZES_IN.get(page_size, PAGE_SIZES_IN["A2"])
        if layout.get("orientation", "landscape") == "portrait":
            w, h = h, w
        self.page_width = w
        self.page_height = h
        self.pos_calc.page_width = w
        self.pos_calc.page_height = h
        props = self.page.getPageSheet().getPageProps()
        props.getPageWidth().setValue(w)
        props.getPageHeight().setValue(h)

    def _setup_styles(self) -> None:
        styling = self.config.get("styling", {})
        theme_name = styling.get("theme", "enterprise_blue")
        self.theme = get_theme(theme_name)
        self.font_family = styling.get("font_family", "Arial")
        self.font_size = float(styling.get("font_size", 9.0))
        self.shadow = styling.get("shadow_enabled", True)
        self.link_width = float(styling.get("link_width", 1.0))

    @staticmethod
    def _edge_points(from_pos: Dict, to_pos: Dict) -> Tuple[float, float, float, float]:
        dx = to_pos["x"] - from_pos["x"]
        dy = to_pos["y"] - from_pos["y"]
        if abs(dx) >= abs(dy):
            if dx >= 0:
                x1 = from_pos["x"] + from_pos["w"] / 2
                x2 = to_pos["x"] - to_pos["w"] / 2
            else:
                x1 = from_pos["x"] - from_pos["w"] / 2
                x2 = to_pos["x"] + to_pos["w"] / 2
            y1 = from_pos["y"]
            y2 = to_pos["y"]
        else:
            if dy >= 0:
                y1 = from_pos["y"] + from_pos["h"] / 2
                y2 = to_pos["y"] - to_pos["h"] / 2
            else:
                y1 = from_pos["y"] - from_pos["h"] / 2
                y2 = to_pos["y"] + to_pos["h"] / 2
            x1 = from_pos["x"]
            x2 = to_pos["x"]
        return x1, y1, x2, y2

    def add_title_block(self) -> None:
        title = self.config.get("title", "Communication Diagram")
        system = self.config.get("system_name", "")
        ver = self.config.get("version", "1.0")
        date = self.config.get("date", "")
        text = f"{title}\n"
        if system:
            text += f"{system} | "
        text += f"Version {ver} | {date}"

        margin = self.config.get("layout", {}).get("margin", 0.5)
        h = 1.2
        w = self.page_width - (2 * margin)
        x = self.page_width / 2.0
        y = self.page_height - margin - (h / 2.0)

        asp.add_rectangle(
            self.page,
            x,
            y,
            w,
            h,
            text=text,
            fill_color=self.theme["title_bg"],
            text_color=self.theme["title_text"],
            border_color=self.theme["title_bg"],
            font_family=self.font_family,
            font_size=self.font_size + 2.0,
            font_bold=True,
            no_border=True,
        )

    def add_groups(self) -> None:
        for group in self.config.get("groups", []):
            member_ids = group.get("participants", [])
            valid_ids = [pid for pid in member_ids if pid in self.positions]
            if not valid_ids:
                continue

            xs = [self.positions[pid]["x"] for pid in valid_ids]
            ys = [self.positions[pid]["y"] for pid in valid_ids]
            ws = [self.positions[pid]["w"] for pid in valid_ids]
            hs = [self.positions[pid]["h"] for pid in valid_ids]

            padding = 1.0
            x1 = min(x - w / 2 for x, w in zip(xs, ws)) - padding
            y1 = min(y - h / 2 for y, h in zip(ys, hs)) - padding
            x2 = max(x + w / 2 for x, w in zip(xs, ws)) + padding
            y2 = max(y + h / 2 for y, h in zip(ys, hs)) + padding

            gw = x2 - x1
            gh = y2 - y1
            gx = x1 + gw / 2.0
            gy = y1 + gh / 2.0

            asp.add_rectangle(
                self.page,
                gx,
                gy,
                gw,
                gh,
                text=group.get("label", group.get("name", "")),
                fill_color=group.get("color", self.theme["group_bg"]),
                text_color=self.theme["group_border"],
                border_color=group.get("border_color", self.theme["group_border"]),
                border_width=2.0,
                line_pattern=2,
                font_family=self.font_family,
                font_size=self.font_size + 1.0,
                font_bold=True,
            )

    def add_participants(self) -> None:
        for p in self.config.get("participants", []):
            pid = p["id"]
            pos = self.positions.get(pid)
            if not pos:
                continue

            p_type = p.get("type", "control")
            fill_c = participant_fill(self.theme, p_type, p.get("color", ""))
            text_c = participant_text_color(self.theme, p_type, p.get("text_color", ""))
            label = build_participant_label(p)

            asp.add_rectangle(
                self.page,
                pos["x"],
                pos["y"],
                pos["w"],
                pos["h"],
                text=label,
                fill_color=fill_c,
                text_color=text_c,
                border_color=fill_c,
                font_family=self.font_family,
                font_size=self.font_size,
                font_bold=True,
            )

    def add_links(self) -> None:
        for link in self.config.get("links", []):
            src_id = link.get("source")
            tgt_id = link.get("target")
            from_pos = self.positions.get(src_id)
            to_pos = self.positions.get(tgt_id)
            if not from_pos or not to_pos:
                log.warning("Skipping link %s→%s: missing participant position", src_id, tgt_id)
                continue

            dashed = link.get("line_style") == "dashed" or link.get("type") == "dependency"
            x1, y1, x2, y2 = self._edge_points(from_pos, to_pos)
            asp.add_connector(
                self.page,
                x1,
                y1,
                x2,
                y2,
                label=link.get("label", ""),
                line_color=self.theme["link_color"],
                line_width=self.link_width,
                dashed=dashed,
                font_family=self.font_family,
                font_size=self.font_size - 1.0,
            )

    def add_messages(self) -> None:
        messages = self.config.get("messages", [])
        sorted_msgs = sorted(
            messages,
            key=lambda m: SequenceNumberGenerator.parse_for_sort(m.get("sequence", "0")),
        )

        for msg in sorted_msgs:
            src_id = msg.get("from")
            tgt_id = msg.get("to")
            from_pos = self.positions.get(src_id)
            to_pos = self.positions.get(tgt_id)
            if not from_pos or not to_pos:
                log.warning("Skipping message %s: missing participant position", msg.get("sequence"))
                continue

            msg_style = get_message_style(self.theme, msg.get("type", "synchronous"))
            label_text = format_message_label(
                msg.get("sequence", ""),
                msg.get("label", ""),
                msg.get("return_value"),
                msg.get("guard"),
            )
            x1, y1, x2, y2 = self._edge_points(from_pos, to_pos)
            asp.add_connector(
                self.page,
                x1,
                y1,
                x2,
                y2,
                label=label_text,
                line_color=msg_style["color"],
                line_width=self.link_width + 0.5,
                dashed=msg_style["dash"],
                font_family=self.font_family,
                font_size=self.font_size,
            )

    def add_legend(self) -> None:
        margin = self.config.get("layout", {}).get("margin", 0.5)
        w = min(self.page_width - 2 * margin, 18.0)
        h = 2.2
        x = self.page_width / 2.0
        y = margin + (h / 2.0)

        text = (
            "LEGEND\n"
            "Participants: <<stereotype>> Class:instance (Name)\n"
            "Links: solid = association  |  dashed = dependency\n"
            "Messages: [guard] sequence: label : return_value"
        )

        asp.add_rectangle(
            self.page,
            x,
            y,
            w,
            h,
            text=text,
            fill_color=self.theme["legend_bg"],
            text_color="#333333",
            border_color=self.theme["legend_border"],
            font_family=self.font_family,
            font_size=self.font_size - 1.0,
        )

    def build(self, include_legend: bool = True) -> None:
        apply_aspose_diagram_license()
        asp.reset_counter()
        self.diagram = asp.new_diagram()
        self.page = self.diagram.getPages().get(0)
        self.page.setName("Communication Diagram")
        self._setup_page()

        n_part = len(self.config.get("participants", []))
        n_msg = len(self.config.get("messages", []))
        log.info("Drawing communication diagram (%d participants, %d messages)…", n_part, n_msg)

        self.add_title_block()
        self.add_groups()
        self.add_participants()
        self.add_links()
        self.add_messages()
        if include_legend:
            self.add_legend()

    def save(self, output_path: str) -> None:
        if self.diagram is None:
            raise RuntimeError("Call build() before save()")
        asp.save_diagram(self.diagram, output_path)
