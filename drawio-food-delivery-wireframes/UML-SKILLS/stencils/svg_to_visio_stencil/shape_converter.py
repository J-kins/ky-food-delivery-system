"""Convert parsed SVG documents into Visio master shapes."""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from . import visio_builder
from .metadata_manager import add_master_metadata, add_master_connections
from .svg_parser import MarkerDef, ParsedSvg, SvgElement
from .utils import (
    estimate_text_width,
    flatten_points,
    is_none_color,
    line_angle,
    normalize_color,
    svg_dash_to_visio_pattern,
    to_visio_rect,
    to_visio_x,
    to_visio_y,
    transform_path_points,
)
from .svg_parser import _path_points

log = logging.getLogger(__name__)


class ShapeConverter:
    def __init__(self, config) -> None:
        self.config = config
        self.api = visio_builder.api()
        self._master_id = 100
        self._temp_diagram = visio_builder.new_diagram()
        self._temp_page = visio_builder.get_page(self._temp_diagram)

    def next_master_id(self) -> int:
        current = self._master_id
        self._master_id += 1
        return current

    def convert_to_master(self, parsed: ParsedSvg, metadata: Dict) -> object:
        visio_builder.clear_page_shapes(self._temp_page)
        for element in parsed.elements:
            try:
                self._draw_element(parsed, element)
            except Exception as exc:
                log.debug("Element render failed in %s: %s", parsed.path.name, exc)

        shape_count = self._temp_page.getShapes().getCount()
        if shape_count == 0:
            raise ValueError(f"No drawable elements found in {parsed.path}")

        master = self.api.Master()
        master_id = self.next_master_id()
        master.setID(master_id)
        master.setName(metadata["name"])
        master.setNameU(metadata["id"])
        master.setIconSize(1)
        master.setAlignName(2)
        master.setMatchByName(0)
        master.setIconUpdate(self.api.BOOL.TRUE)

        shapes = self._temp_page.getShapes()
        collected = [shapes.get(i) for i in range(shapes.getCount())]
        for shape in collected:
            master.getShapes().add(shape)

        root = master.getShapes().get(0)
        width_in = parsed.width / self.config.svg_dpi
        height_in = parsed.height / self.config.svg_dpi
        add_master_connections(root, metadata, width_in, height_in, self.config)
        add_master_metadata(root, metadata, self.config)
        return master

    def _style(self, element: SvgElement, *, text: bool = False) -> tuple[str, str, float, bool, bool]:
        defaults = self.config.shape_styling
        fill = normalize_color(element.style.fill, defaults.get("default_fill", "#FFFFFF"))
        stroke = normalize_color(element.style.stroke, defaults.get("default_stroke", "#334155"))
        width = element.style.stroke_width or defaults.get("default_stroke_width", 1.5)
        no_fill = is_none_color(element.style.fill)
        no_border = is_none_color(element.style.stroke) if not text else True
        return fill, stroke, width, no_fill, no_border

    def _draw_element(self, parsed: ParsedSvg, element: SvgElement) -> None:
        if element.kind == "rect":
            self._draw_rect(parsed, element)
        elif element.kind == "circle":
            self._draw_circle(parsed, element)
        elif element.kind == "ellipse":
            self._draw_ellipse(parsed, element)
        elif element.kind == "line":
            self._draw_line(parsed, element)
        elif element.kind == "polyline":
            self._draw_polyline(parsed, element)
        elif element.kind == "text":
            self._draw_text(parsed, element)

    def _draw_rect(self, parsed: ParsedSvg, element: SvgElement) -> None:
        x, y, w, h = to_visio_rect(
            element.x,
            element.y,
            element.width,
            element.height,
            parsed.height,
            self.config.svg_dpi,
        )
        shape_id = self._temp_page.drawRectangle(x, y, w, h)
        shape = visio_builder.get_shape(self._temp_page, shape_id)
        fill, stroke, width, no_fill, no_border = self._style(element)
        visio_builder.apply_fill_style(shape, fill, no_fill=no_fill)
        visio_builder.apply_line_style(
            shape,
            stroke,
            width,
            dashed=svg_dash_to_visio_pattern(element.style.stroke_dasharray) == 2,
            no_border=no_border,
        )

    def _draw_circle(self, parsed: ParsedSvg, element: SvgElement) -> None:
        diameter = element.r * 2.0
        x, y, w, h = to_visio_rect(
            element.cx - element.r,
            element.cy - element.r,
            diameter,
            diameter,
            parsed.height,
            self.config.svg_dpi,
        )
        shape_id = self._temp_page.drawOwal(x, y, w, h)
        shape = visio_builder.get_shape(self._temp_page, shape_id)
        fill, stroke, width, no_fill, no_border = self._style(element)
        visio_builder.apply_fill_style(shape, fill, no_fill=no_fill)
        visio_builder.apply_line_style(shape, stroke, width, no_border=no_border)

    def _draw_ellipse(self, parsed: ParsedSvg, element: SvgElement) -> None:
        x, y, w, h = to_visio_rect(
            element.cx - element.rx,
            element.cy - element.ry,
            element.rx * 2.0,
            element.ry * 2.0,
            parsed.height,
            self.config.svg_dpi,
        )
        shape_id = self._temp_page.drawEllipse(x, y, w, h)
        shape = visio_builder.get_shape(self._temp_page, shape_id)
        fill, stroke, width, no_fill, no_border = self._style(element)
        visio_builder.apply_fill_style(shape, fill, no_fill=no_fill)
        visio_builder.apply_line_style(shape, stroke, width, no_border=no_border)

    def _draw_line(self, parsed: ParsedSvg, element: SvgElement) -> None:
        x1 = to_visio_x(element.x1, self.config.svg_dpi)
        y1 = to_visio_y(element.y1, parsed.height, self.config.svg_dpi)
        x2 = to_visio_x(element.x2, self.config.svg_dpi)
        y2 = to_visio_y(element.y2, parsed.height, self.config.svg_dpi)
        shape_id = self._temp_page.drawLine(x1, y1, x2, y2)
        shape = visio_builder.get_shape(self._temp_page, shape_id)
        _, stroke, width, _, no_border = self._style(element)
        visio_builder.apply_fill_style(shape, "#FFFFFF", no_fill=True)
        visio_builder.apply_line_style(
            shape,
            stroke,
            width,
            dashed=svg_dash_to_visio_pattern(element.style.stroke_dasharray) == 2,
            no_border=no_border,
        )
        if element.marker_end:
            self._draw_marker(parsed, element.marker_end, element.x2, element.y2, element.x1, element.y1)
        if element.marker_start:
            self._draw_marker(parsed, element.marker_start, element.x1, element.y1, element.x2, element.y2)

    def _draw_polyline(self, parsed: ParsedSvg, element: SvgElement) -> None:
        if len(element.points) < 2:
            return
        flat = flatten_points(element.points, parsed.height, self.config.svg_dpi)
        shape_id = self._temp_page.drawPolyline(visio_builder.make_double_array(flat))
        shape = visio_builder.get_shape(self._temp_page, shape_id)
        fill, stroke, width, no_fill, no_border = self._style(element)
        if element.closed:
            visio_builder.apply_fill_style(shape, fill, no_fill=no_fill)
        else:
            visio_builder.apply_fill_style(shape, "#FFFFFF", no_fill=True)
        visio_builder.apply_line_style(
            shape,
            stroke,
            width,
            dashed=svg_dash_to_visio_pattern(element.style.stroke_dasharray) == 2,
            no_border=no_border,
        )

    def _draw_text(self, parsed: ParsedSvg, element: SvgElement) -> None:
        if not element.text:
            return
        font_size = element.style.font_size or 12.0
        text_width = estimate_text_width(element.text, font_size)
        text_height = font_size * 1.2
        anchor = (element.style.text_anchor or "start").lower()
        if anchor == "middle":
            x_svg = element.x - text_width / 2.0
        elif anchor == "end":
            x_svg = element.x - text_width
        else:
            x_svg = element.x
        y_svg = element.y - font_size
        x = to_visio_x(x_svg, self.config.svg_dpi)
        y = to_visio_y(y_svg + text_height, parsed.height, self.config.svg_dpi)
        w = text_width / self.config.svg_dpi
        h = text_height / self.config.svg_dpi
        fill, _, _, _, _ = self._style(element, text=True)
        font = (element.style.font_family or "Arial").split(",")[0].strip("'\" ")
        shape = self._temp_page.addText(
            x,
            y,
            w,
            h,
            element.text,
            font,
            fill,
            font_size / 72.0,
        )
        visio_builder.apply_fill_style(shape, "#FFFFFF", no_fill=True)
        visio_builder.apply_line_style(shape, fill, 1.0, no_border=True)

    def _draw_marker(
        self,
        parsed: ParsedSvg,
        marker_id: str,
        tip_x: float,
        tip_y: float,
        other_x: float,
        other_y: float,
    ) -> None:
        marker: Optional[MarkerDef] = parsed.markers.get(marker_id)
        if marker is None or not marker.path_d:
            return
        points, closed = _path_points(marker.path_d, samples=12)
        if not points:
            return
        angle = line_angle(other_x, other_y, tip_x, tip_y)
        transformed = transform_path_points(
            points,
            tip_x - marker.ref_x,
            tip_y - marker.ref_y,
            angle,
        )
        flat = flatten_points(transformed, parsed.height, self.config.svg_dpi)
        shape_id = self._temp_page.drawPolyline(visio_builder.make_double_array(flat))
        shape = visio_builder.get_shape(self._temp_page, shape_id)
        fill = normalize_color(marker.fill, self.config.shape_styling.get("default_stroke", "#334155"))
        stroke = normalize_color(marker.stroke, fill)
        visio_builder.apply_fill_style(shape, fill, no_fill=not closed)
        visio_builder.apply_line_style(shape, stroke, 1.0, no_border=is_none_color(marker.stroke))
