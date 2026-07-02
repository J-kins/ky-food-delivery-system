"""Orchestrate WBS validation and Visio generation."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

from config.settings import apply_aspose_diagram_license
from core.diagram_builder import WBSBuilder
from core.validator import validate_wbs

log = logging.getLogger(__name__)

MIN_VSDX_BYTES = 4_000


def build_wbs(spec_dict: Dict[str, Any], output_path: str, layout_style: str | None = None) -> str:
    apply_aspose_diagram_license()
    spec = validate_wbs(spec_dict)
    log.info("Payload validated successfully.")

    payload = spec.model_dump()
    if layout_style:
        payload["wbs"]["styling"]["layout_style"] = layout_style

    builder = WBSBuilder(payload)
    builder.build()
    builder.save(output_path)

    size = Path(output_path).stat().st_size
    if size < MIN_VSDX_BYTES:
        raise RuntimeError(f"WBS diagram too small ({size} bytes): {output_path}")
    log.info("WBS diagram saved to %s (%d bytes)", output_path, size)
    return output_path
