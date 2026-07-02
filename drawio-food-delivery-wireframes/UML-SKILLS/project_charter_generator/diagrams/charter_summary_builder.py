"""Single-page executive Project Charter Summary Diagram (Visio)."""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

from config.settings import PAGE_SIZES_IN, apply_aspose_diagram_license
from diagrams import aspose_renderer as asp
from schedulers.charter_layout_calculator import CharterLayoutCalculator

log = logging.getLogger(__name__)

MIN_SUMMARY_VSDX_BYTES = 4_000


def _normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Accept flat MAIN schema or wrapped project_charter schema."""
    if "project_charter" in payload:
        pc = payload["project_charter"]
        project_name = pc.get("project_name") or pc.get("project", {}).get("name", "")
        overview = pc.get("overview", {})
        return {
            "project": {
                "name": project_name,
                "sponsor": overview.get("sponsor", ""),
                "manager": overview.get("manager", ""),
                "department": overview.get("department", ""),
                "start_date": overview.get("start_date", ""),
                "end_date": overview.get("end_date", ""),
                "version": pc.get("version", "1.0"),
            },
            "vision": pc.get("vision", {}),
            "objectives": pc.get("objectives", []),
            "scope": pc.get("scope", {}),
            "stakeholders": pc.get("stakeholders", []),
            "constraints": pc.get("constraints", []),
            "assumptions": pc.get("assumptions", []),
            "milestones": pc.get("milestones", []),
            "budget": _normalize_budget(pc.get("budget", {})),
            "approvals": pc.get("approvals", []),
            "_meta": {
                "title": pc.get("title", "Project Charter"),
                "date": pc.get("date", ""),
                "confidentiality": pc.get("confidentiality", "Confidential - Internal Use Only"),
            },
        }
    meta = {
        "title": "Project Charter",
        "date": "",
        "confidentiality": "Confidential - Internal Use Only",
    }
    data = dict(payload)
    data["_meta"] = meta
    if data.get("budget"):
        b = data["budget"]
        if isinstance(b, dict):
            data["budget"] = _normalize_budget(b)
        else:
            data["budget"] = _normalize_budget(b.model_dump() if hasattr(b, "model_dump") else dict(b))
    return data


def _normalize_budget(budget: Dict[str, Any]) -> Dict[str, Any]:
    if not budget:
        return {}
    if budget.get("categories"):
        return budget
    breakdown = budget.get("breakdown", {})
    if isinstance(breakdown, dict) and not hasattr(breakdown, "personnel"):
        bd = breakdown
    elif hasattr(breakdown, "model_dump"):
        bd = breakdown.model_dump()
    elif hasattr(breakdown, "personnel"):
        bd = {
            "personnel": breakdown.personnel,
            "hardware": breakdown.hardware,
            "software": breakdown.software,
            "training": breakdown.training,
            "contingency": breakdown.contingency,
        }
    else:
        bd = {}
    total = float(budget.get("total") or 0)
    categories = []
    for key, label in [
        ("personnel", "Personnel"),
        ("hardware", "Hardware"),
        ("software", "Software"),
        ("training", "Training"),
        ("contingency", "Contingency"),
    ]:
        amt = float(bd.get(key, 0) or 0)
        if amt > 0:
            categories.append({
                "name": label,
                "total": amt,
                "percentage": (amt / total * 100) if total else 0,
            })
    return {
        "total": total,
        "currency": budget.get("currency", "USD"),
        "exchange_rate": budget.get("exchange_rate"),
        "exchange_currency": budget.get("exchange_currency", "UGX"),
        "categories": categories,
    }


def _truncate(text: str, max_len: int = 90) -> str:
    text = str(text or "").strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


class CharterSummaryBuilder:
    """Build the executive single-page charter poster."""

    def __init__(self, payload: Dict[str, Any]):
        self.data = _normalize_payload(payload)
        self.page_w, self.page_h = PAGE_SIZES_IN.get("A2", (59.4, 42.0))
        self.margin = 0.5
        self.calculator = CharterLayoutCalculator(self.page_w, self.page_h, self.margin)
        self.diagram = None
        self.page = None

    def _cx(self, section) -> float:
        return section.x

    def _left(self, section) -> float:
        return self.margin + 0.15

    def _inner_w(self, section) -> float:
        return section.width - 0.3

    def _draw_section_shell(self, section, header_h: float = 0.45) -> Tuple[float, float]:
        style = self.calculator.section_style(section.id)
        asp.add_rectangle(
            self.page,
            self._cx(section),
            section.y,
            section.width,
            section.height,
            fill_color="#FFFFFF",
            border_color=style["border"],
            border_width=1.0,
            font_size=8.0,
        )
        header_y = section.y + section.height / 2 - header_h / 2 - 0.02
        asp.add_rectangle(
            self.page,
            self._cx(section),
            header_y,
            section.width,
            header_h,
            text=section.title,
            fill_color=style["header"],
            text_color="#FFFFFF",
            border_color=style["header"],
            font_size=9.0,
            font_bold=True,
            no_border=True,
        )
        content_y = section.y - section.height / 2 + (section.height - header_h) / 2 + 0.05
        content_h = section.height - header_h - 0.12
        return content_y, content_h

    def _draw_title_block(self) -> None:
        meta = self.data.get("_meta", {})
        project = self.data.get("project", {})
        title = meta.get("title", "PROJECT CHARTER")
        lines = [title.upper(), project.get("name", "")]
        ver = project.get("version", "")
        date = meta.get("date", "")
        meta_line = " | ".join(p for p in (f"Version {ver}" if ver else "", date) if p)
        if meta_line:
            lines.append(meta_line)
        y = self.page_h - self.margin - 0.65
        asp.add_rectangle(
            self.page,
            self.page_w / 2,
            y,
            self.page_w - 2 * self.margin,
            1.3,
            text="\n".join(lines),
            fill_color="#1a237e",
            text_color="#FFFFFF",
            border_color="#1a237e",
            font_size=11.0,
            font_bold=True,
            no_border=True,
        )

    def _draw_footer(self) -> None:
        meta = self.data.get("_meta", {})
        conf = meta.get("confidentiality", "Confidential - Internal Use Only")
        asp.add_rectangle(
            self.page,
            self.page_w / 2,
            self.margin + 0.35,
            self.page_w - 2 * self.margin,
            0.55,
            text=f"Page 1 of 1          {conf}",
            fill_color="#ECEFF1",
            text_color="#546E7A",
            border_color="#90A4AE",
            font_size=7.5,
        )

    def _draw_vision(self, section) -> None:
        content_y, content_h = self._draw_section_shell(section)
        style = self.calculator.section_style("vision")
        statement = self.data.get("vision", {}).get("statement", "")
        asp.add_rectangle(
            self.page,
            self._cx(section),
            content_y,
            self._inner_w(section),
            content_h,
            text=_truncate(statement, 220),
            fill_color=style["bg"],
            text_color="#0D47A1",
            border_color=style["border"],
            font_size=9.0,
            font_bold=True,
        )

    def _draw_overview(self, section) -> None:
        content_y, content_h = self._draw_section_shell(section)
        p = self.data.get("project", {})
        left = (
            f"Project: {p.get('name', '')}\n"
            f"Sponsor: {p.get('sponsor', '')}\n"
            f"Manager: {p.get('manager', '')}"
        )
        right = (
            f"Department: {p.get('department', '')}\n"
            f"Start: {p.get('start_date', '')}\n"
            f"End: {p.get('end_date', '')}"
        )
        half_w = (self._inner_w(section) - 0.2) / 2
        asp.add_rectangle(
            self.page,
            self._left(section) + half_w / 2,
            content_y,
            half_w,
            content_h,
            text=left,
            fill_color="#FAFAFA",
            border_color="#E0E0E0",
            font_size=8.0,
        )
        asp.add_rectangle(
            self.page,
            self._left(section) + half_w + 0.2 + half_w / 2,
            content_y,
            half_w,
            content_h,
            text=right,
            fill_color="#FAFAFA",
            border_color="#E0E0E0",
            font_size=8.0,
        )

    def _draw_table_section(
        self,
        section,
        headers: List[str],
        rows: List[List[str]],
        col_widths: List[float] | None = None,
    ) -> None:
        content_y, content_h = self._draw_section_shell(section, header_h=0.42)
        inner_w = self._inner_w(section)
        n_cols = len(headers)
        if not col_widths:
            col_widths = [inner_w / n_cols] * n_cols
        row_h = min(0.36, (content_h - 0.38) / max(len(rows), 1))
        header_h = 0.36
        table_top = content_y + content_h / 2 - header_h / 2 - 0.02
        x_cursor = self._left(section)

        for i, hdr in enumerate(headers):
            asp.add_rectangle(
                self.page,
                x_cursor + col_widths[i] / 2,
                table_top,
                col_widths[i] - 0.04,
                header_h,
                text=hdr,
                fill_color="#1a237e",
                text_color="#FFFFFF",
                border_color="#1a237e",
                font_size=7.5,
                font_bold=True,
            )
            x_cursor += col_widths[i]

        for r_idx, row in enumerate(rows):
            row_y = table_top - header_h / 2 - row_h / 2 - r_idx * row_h - 0.02
            fill = "#F8F9FA" if r_idx % 2 == 0 else "#FFFFFF"
            x_cursor = self._left(section)
            for c_idx, cell in enumerate(row):
                asp.add_rectangle(
                    self.page,
                    x_cursor + col_widths[c_idx] / 2,
                    row_y,
                    col_widths[c_idx] - 0.04,
                    row_h - 0.02,
                    text=_truncate(cell, 70),
                    fill_color=fill,
                    border_color="#E0E0E0",
                    font_size=7.0,
                )
                x_cursor += col_widths[c_idx]

    def _draw_objectives(self, section) -> None:
        objectives = self.data.get("objectives", [])[:6]
        rows = [
            [
                o.get("id", ""),
                o.get("description", ""),
                o.get("measurable_criteria") or o.get("criteria", ""),
            ]
            for o in objectives
        ]
        inner_w = self._inner_w(section)
        self._draw_table_section(
            section,
            ["ID", "Objective", "Measurable Criteria"],
            rows,
            [inner_w * 0.12, inner_w * 0.48, inner_w * 0.38],
        )

    def _draw_scope(self, section) -> None:
        content_y, content_h = self._draw_section_shell(section)
        scope = self.data.get("scope", {})
        in_items = scope.get("in_scope", [])[:6]
        out_items = scope.get("out_of_scope", [])[:4]
        in_text = "IN SCOPE\n" + "\n".join(f"• {i}" for i in in_items)
        out_text = "OUT OF SCOPE\n" + "\n".join(f"• {i}" for i in out_items)
        half_w = (self._inner_w(section) - 0.2) / 2
        asp.add_rectangle(
            self.page,
            self._left(section) + half_w / 2,
            content_y,
            half_w,
            content_h,
            text=in_text,
            fill_color="#E8F5E9",
            text_color="#1B5E20",
            border_color="#2E7D32",
            font_size=7.5,
        )
        asp.add_rectangle(
            self.page,
            self._left(section) + half_w + 0.2 + half_w / 2,
            content_y,
            half_w,
            content_h,
            text=out_text,
            fill_color="#FFEBEE",
            text_color="#B71C1C",
            border_color="#E53935",
            font_size=7.5,
        )

    def _draw_stakeholders(self, section) -> None:
        stakeholders = self.data.get("stakeholders", [])[:5]
        rows = [
            [
                s.get("id", ""),
                s.get("name", ""),
                s.get("role", ""),
                s.get("organization", ""),
                _truncate(s.get("expectations", ""), 55),
            ]
            for s in stakeholders
        ]
        inner_w = self._inner_w(section)
        self._draw_table_section(
            section,
            ["ID", "Name", "Role", "Organization", "Expectations"],
            rows,
            [inner_w * 0.08, inner_w * 0.18, inner_w * 0.16, inner_w * 0.18, inner_w * 0.38],
        )

    def _draw_constraints(self, section) -> None:
        content_y, content_h = self._draw_section_shell(section)
        constraints = self.data.get("constraints", [])[:5]
        assumptions = self.data.get("assumptions", [])[:5]
        c_text = "CONSTRAINTS\n" + "\n".join(f"• {c}" for c in constraints)
        a_text = "ASSUMPTIONS\n" + "\n".join(f"• {a}" for a in assumptions)
        half_w = (self._inner_w(section) - 0.2) / 2
        asp.add_rectangle(
            self.page,
            self._left(section) + half_w / 2,
            content_y,
            half_w,
            content_h,
            text=_truncate(c_text, 350),
            fill_color="#FFEBEE",
            border_color="#C62828",
            font_size=7.5,
        )
        asp.add_rectangle(
            self.page,
            self._left(section) + half_w + 0.2 + half_w / 2,
            content_y,
            half_w,
            content_h,
            text=_truncate(a_text, 350),
            fill_color="#FFF3E0",
            border_color="#E65100",
            font_size=7.5,
        )

    def _draw_milestones(self, section) -> None:
        milestones = self.data.get("milestones", [])[:5]
        rows = [
            [
                m.get("id", ""),
                m.get("name", ""),
                m.get("date", ""),
                _truncate(m.get("description") or m.get("deliverable", ""), 60),
            ]
            for m in milestones
        ]
        inner_w = self._inner_w(section)
        self._draw_table_section(
            section,
            ["ID", "Milestone", "Date", "Description"],
            rows,
            [inner_w * 0.08, inner_w * 0.28, inner_w * 0.14, inner_w * 0.48],
        )

    def _draw_budget(self, section) -> None:
        content_y, content_h = self._draw_section_shell(section)
        budget = self.data.get("budget", {})
        categories = budget.get("categories", [])
        currency = budget.get("currency", "USD")
        total = budget.get("total", 0)

        table_w = self._inner_w(section) * 0.52
        chart_w = self._inner_w(section) * 0.42
        table_x = self._left(section) + table_w / 2
        chart_x = self._left(section) + table_w + 0.25 + chart_w / 2

        row_h = 0.34
        header_h = 0.34
        table_top = content_y + content_h / 2 - header_h / 2
        cols = [table_w * 0.45, table_w * 0.30, table_w * 0.22]
        headers = ["Category", f"Total ({currency})", "%"]
        x = self._left(section)
        for i, hdr in enumerate(headers):
            asp.add_rectangle(
                self.page, x + cols[i] / 2, table_top, cols[i] - 0.03, header_h,
                text=hdr, fill_color="#1a237e", text_color="#FFFFFF",
                font_size=7.0, font_bold=True, no_border=True,
            )
            x += cols[i]

        for r_idx, cat in enumerate(categories):
            row_y = table_top - header_h / 2 - row_h / 2 - r_idx * row_h - 0.02
            fill = "#F8F9FA" if r_idx % 2 == 0 else "#FFFFFF"
            vals = [
                cat.get("name", ""),
                f"{cat.get('total', 0):,.0f}",
                f"{cat.get('percentage', 0):.0f}%",
            ]
            x = self._left(section)
            for i, val in enumerate(vals):
                asp.add_rectangle(
                    self.page, x + cols[i] / 2, row_y, cols[i] - 0.03, row_h - 0.02,
                    text=val, fill_color=fill, border_color="#E0E0E0", font_size=7.0,
                )
                x += cols[i]

        total_y = row_y - row_h if categories else table_top - header_h
        asp.add_rectangle(
            self.page, self._left(section) + table_w / 2, total_y - 0.05, table_w, row_h,
            text=f"TOTAL: {currency} {total:,.0f}",
            fill_color="#FFF8E1", text_color="#F57F17", border_color="#FFB300",
            font_size=8.0, font_bold=True,
        )

        chart_lines = ["BUDGET DISTRIBUTION", ""]
        for cat in categories:
            pct = cat.get("percentage", 0)
            bar = "█" * max(1, int(pct / 5))
            chart_lines.append(f"{bar} {cat.get('name', '')} {pct:.0f}%")
        if budget.get("exchange_rate"):
            chart_lines.append("")
            chart_lines.append(f"1 {currency} = {budget['exchange_rate']:,} {budget.get('exchange_currency', 'UGX')}")
        asp.add_rectangle(
            self.page, chart_x, content_y, chart_w, content_h,
            text="\n".join(chart_lines),
            fill_color="#FFFDE7", border_color="#FFB300", font_size=7.5,
        )

    def _draw_approvals(self, section) -> None:
        approvals = self.data.get("approvals", [])[:4]
        rows = [
            [
                a.get("role", ""),
                a.get("name", ""),
                a.get("signature", "") or "________________________",
                a.get("date", "") or "______________",
            ]
            for a in approvals
        ]
        inner_w = self._inner_w(section)
        self._draw_table_section(
            section,
            ["Role", "Name", "Signature", "Date"],
            rows,
            [inner_w * 0.22, inner_w * 0.22, inner_w * 0.32, inner_w * 0.22],
        )

    def build(self) -> None:
        apply_aspose_diagram_license()
        asp.reset_counter()
        self.diagram = asp.new_diagram()
        self.page = self.diagram.getPages().get(0)
        self.page.setName("Charter Summary")

        props = self.page.getPageSheet().getPageProps()
        props.getPageWidth().setValue(self.page_w)
        props.getPageHeight().setValue(self.page_h)

        self._draw_title_block()
        sections = self.calculator.plan_sections(self.data)

        drawers = {
            "vision": self._draw_vision,
            "overview": self._draw_overview,
            "objectives": self._draw_objectives,
            "scope": self._draw_scope,
            "stakeholders": self._draw_stakeholders,
            "constraints": self._draw_constraints,
            "milestones": self._draw_milestones,
            "budget": self._draw_budget,
            "approvals": self._draw_approvals,
        }
        for section in sections:
            drawers[section.id](section)

        self._draw_footer()
        log.info("Charter summary diagram built (%d sections).", len(sections))

    def save(self, output_path: str) -> str:
        if self.diagram is None:
            raise RuntimeError("Call build() before save()")
        asp.save_diagram(self.diagram, output_path)
        return output_path


def build_charter_summary(payload: Dict[str, Any], output_path: str) -> str:
    """Build and save the single-page executive charter summary Visio file."""
    builder = CharterSummaryBuilder(payload)
    builder.build()
    builder.save(output_path)
    return output_path
