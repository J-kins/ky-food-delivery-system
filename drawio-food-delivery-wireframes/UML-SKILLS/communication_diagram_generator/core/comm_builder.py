"""Orchestrate validation and Communication Diagram Visio generation."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

from config.settings import apply_aspose_diagram_license
from core.diagram_builder import CommunicationDiagramBuilder
from core.validator import validate

log = logging.getLogger(__name__)

MIN_VSDX_BYTES = 4_000


def build_communication_diagram(spec_dict: Dict[str, Any], output_path: str) -> str:
    apply_aspose_diagram_license()
    validate(spec_dict)
    log.info("Payload validated successfully.")

    builder = CommunicationDiagramBuilder(spec_dict)
    builder.build(include_legend=True)
    builder.save(output_path)

    size = Path(output_path).stat().st_size
    if size < MIN_VSDX_BYTES:
        raise RuntimeError(f"Communication diagram too small ({size} bytes): {output_path}")
    log.info("Communication diagram saved to %s (%d bytes)", output_path, size)
    return output_path
