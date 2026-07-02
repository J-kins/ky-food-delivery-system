"""Shared utilities for logging, coordinates, and color parsing."""
from __future__ import annotations

import logging
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

Color = str
Point = Tuple[float, float]


def setup_logging(log_dir: Path, verbose: bool = False) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("svg_to_visio")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(
        log_dir / f"conversion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def parse_length(value: str | None, default: float = 0.0) -> float:
    if not value:
        return default
    cleaned = value.strip().replace("px", "").replace("pt", "")
    try:
        return float(cleaned)
    except ValueError:
        return default


def normalize_color(value: str | None, fallback: str) -> Color:
    if not value or value.lower() in {"none", "transparent", "inherit"}:
        return fallback
    value = value.strip()
    if value.startswith("#"):
        if len(value) == 4:
            return "#" + "".join(ch * 2 for ch in value[1:])
        return value
    named = {
        "white": "#FFFFFF",
        "black": "#000000",
    }
    return named.get(value.lower(), fallback)


def is_none_color(value: str | None) -> bool:
    return not value or value.lower() in {"none", "transparent"}


def svg_dash_to_visio_pattern(dasharray: str | None) -> int:
    if not dasharray:
        return 1
    parts = [p for p in re.split(r"[\s,]+", dasharray.strip()) if p]
    if not parts:
        return 1
    return 2


def to_visio_x(x: float, dpi: float) -> float:
    return x / dpi


def to_visio_y(y: float, viewbox_height: float, dpi: float) -> float:
    return (viewbox_height - y) / dpi


def to_visio_rect(
    x: float,
    y: float,
    width: float,
    height: float,
    viewbox_height: float,
    dpi: float,
) -> Tuple[float, float, float, float]:
    return (
        x / dpi,
        (viewbox_height - y - height) / dpi,
        width / dpi,
        height / dpi,
    )


def flatten_points(points: Sequence[Point], viewbox_height: float, dpi: float) -> List[float]:
    flat: List[float] = []
    for x, y in points:
        flat.extend([to_visio_x(x, dpi), to_visio_y(y, viewbox_height, dpi)])
    return flat


def polygon_points(attr: str) -> List[Point]:
    values = [float(v) for v in re.split(r"[\s,]+", attr.strip()) if v]
    return list(zip(values[0::2], values[1::2]))


def rounded_rect_points(
    x: float,
    y: float,
    width: float,
    height: float,
    rx: float,
    ry: float,
    segments: int = 6,
) -> List[Point]:
    rx = min(rx, width / 2.0)
    ry = min(ry or rx, height / 2.0)
    if rx <= 0 and ry <= 0:
        return [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height),
            (x, y),
        ]

    points: List[Point] = []
    corners = [
        (x + rx, y, math.pi, 1.5 * math.pi),
        (x + width - rx, y, 1.5 * math.pi, 2.0 * math.pi),
        (x + width, y + ry, 2.0 * math.pi, 2.5 * math.pi),
        (x + width - rx, y + height, 0.5 * math.pi, math.pi),
        (x + rx, y + height, 0.0, 0.5 * math.pi),
        (x, y + height - ry, 1.5 * math.pi, 2.0 * math.pi),
    ]
    # top edge start
    points.append((x + rx, y))
    for cx, cy, start, end in corners[:2]:
        for step in range(1, segments + 1):
            t = start + (end - start) * (step / segments)
            points.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    points.append((x + width, y + height - ry))
    for cx, cy, start, end in corners[2:4]:
        for step in range(1, segments + 1):
            t = start + (end - start) * (step / segments)
            points.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    points.append((x + rx, y + height))
    for cx, cy, start, end in corners[4:]:
        for step in range(1, segments + 1):
            t = start + (end - start) * (step / segments)
            points.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    points.append((x, y + ry))
    for step in range(1, segments + 1):
        t = math.pi + (0.5 * math.pi) * (step / segments)
        points.append((x + rx * math.cos(t), y + ry * math.sin(t)))
    points.append(points[0])
    return points


def line_angle(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.atan2(y2 - y1, x2 - x1)


def rotate_point(x: float, y: float, angle: float) -> Point:
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return x * cos_a - y * sin_a, x * sin_a + y * cos_a


def transform_path_points(
    points: Iterable[Point],
    tx: float,
    ty: float,
    angle: float,
    sx: float = 1.0,
    sy: float = 1.0,
) -> List[Point]:
    transformed: List[Point] = []
    for x, y in points:
        x *= sx
        y *= sy
        x, y = rotate_point(x, y, angle)
        transformed.append((x + tx, y + ty))
    return transformed


def estimate_text_width(text: str, font_size: float) -> float:
    return max(font_size * 0.55 * len(text), font_size)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
