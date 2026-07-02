"""Generate charter diagram PNGs from payload using layout engine + Pillow."""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Tuple

from diagrams.layouts import (
    layout_milestone_timeline,
    layout_org_chart,
    layout_problem_tree,
    layout_risk_matrix,
    layout_scope_boundary,
    layout_stakeholder_matrix,
)
from diagrams.png_renderer import render_layout_to_png

log = logging.getLogger(__name__)

DIAGRAM_SPECS: List[Tuple[str, Any, str]] = [
    ("problem_tree", layout_problem_tree, "problem-tree.png"),
    ("stakeholder_matrix", layout_stakeholder_matrix, "stakeholder-matrix.png"),
    ("scope_boundary", layout_scope_boundary, "scope-boundary.png"),
    ("org_chart", layout_org_chart, "org-chart.png"),
    ("milestone_timeline", layout_milestone_timeline, "milestone-timeline.png"),
    ("risk_matrix", layout_risk_matrix, "risk-matrix.png"),
]


def generate_all_diagrams(payload: Dict[str, Any], output_dir: str) -> Dict[str, str]:
    diagrams_dir = os.path.join(output_dir, "diagrams")
    os.makedirs(diagrams_dir, exist_ok=True)
    paths: Dict[str, str] = {}

    for key, layout_fn, filename in DIAGRAM_SPECS:
        try:
            layout = layout_fn(payload)
            path = os.path.join(diagrams_dir, filename)
            render_layout_to_png(layout, path)
            paths[key] = path
            log.info("Rendered diagram %s → %s", key, path)
        except Exception as exc:
            log.warning("Failed to render %s: %s", key, exc)

    return paths
