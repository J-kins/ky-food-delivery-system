"""Orchestrate validation and Kanban Visio generation."""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict

from config.settings import apply_aspose_diagram_license
from core.diagram_builder import KanbanChartBuilder
from core.validator import validate_kanban

log = logging.getLogger(__name__)

MIN_VSDX_BYTES = 4_000


def build_kanban(spec_dict: Dict[str, Any], output_path: str) -> str:
    apply_aspose_diagram_license()
    spec = validate_kanban(spec_dict)
    log.info("Payload validated successfully.")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    builder = KanbanChartBuilder(spec.model_dump())
    builder.build()
    builder.save(output_path)

    size = Path(output_path).stat().st_size
    if size < MIN_VSDX_BYTES:
        raise RuntimeError(f"Kanban chart too small ({size} bytes): {output_path}")
    log.info("Kanban chart saved to %s (%d bytes)", output_path, size)
    return output_path
