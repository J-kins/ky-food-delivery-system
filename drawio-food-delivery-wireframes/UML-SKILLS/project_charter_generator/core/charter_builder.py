"""Orchestrate charter validation, diagram rendering, Word, and Visio output."""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict

from config.settings import apply_aspose_diagram_license
from core.errors import WordGenerationError
from core.validator import validate_payload
from diagrams.aspose_renderer import build_visio_deck
from diagrams.charter_summary_builder import MIN_SUMMARY_VSDX_BYTES, build_charter_summary
from diagrams.description_schema import REQUIRED_WORD_DIAGRAMS
from diagrams.word_diagram_pipeline import compile_word_diagrams
from word.document_builder import build_word_document
from core.verify_outputs import verify_all_outputs

log = logging.getLogger(__name__)

MIN_DOCX_BYTES = 8_000
MIN_VSDX_BYTES = 5_000


def _verify_file(path: str, min_bytes: int, label: str) -> None:
    p = Path(path)
    if not p.is_file():
        raise WordGenerationError(f"{label} not created: {path}")
    size = p.stat().st_size
    if size < min_bytes:
        raise WordGenerationError(f"{label} too small ({size} bytes): {path}")


def build_charter(
    json_payload: Dict[str, Any],
    output_dir: str,
    *,
    word_only: bool = False,
    visio_only: bool = False,
) -> Dict[str, str]:
    """Run the full or partial charter generation pipeline."""
    os.makedirs(output_dir, exist_ok=True)
    apply_aspose_diagram_license()

    validate_payload(json_payload)
    log.info("Payload validated successfully.")

    word_diagrams: Dict[str, Dict[str, str]] = {}
    if not visio_only:
        word_diagrams = compile_word_diagrams(json_payload, output_dir)
        log.info("Word diagrams compiled to SVG XML (%d/%d).", len(word_diagrams), len(REQUIRED_WORD_DIAGRAMS))

    outputs: Dict[str, str] = {
        "diagrams_svg_dir": os.path.join(output_dir, "diagrams", "svg"),
        "diagrams_source_dir": os.path.join(output_dir, "diagrams", "source"),
    }

    if not visio_only:
        doc_path = os.path.join(output_dir, "project-charter.docx")
        build_word_document(json_payload, word_diagrams, doc_path)
        _verify_file(doc_path, MIN_DOCX_BYTES, "Word document")
        outputs["word"] = doc_path
        log.info("Word document saved to %s (%d bytes)", doc_path, Path(doc_path).stat().st_size)

    if not word_only:
        vsdx_path = os.path.join(output_dir, "visio", "project-charter.vsdx")
        build_visio_deck(json_payload, {}, vsdx_path)
        _verify_file(vsdx_path, MIN_VSDX_BYTES, "Visio deck")
        outputs["visio"] = vsdx_path
        log.info("Visio deck saved to %s (%d bytes)", vsdx_path, Path(vsdx_path).stat().st_size)

        summary_path = os.path.join(output_dir, "visio", "charter-summary.vsdx")
        build_charter_summary(json_payload, summary_path)
        _verify_file(summary_path, MIN_SUMMARY_VSDX_BYTES, "Charter summary diagram")
        outputs["charter_summary"] = summary_path
        log.info("Charter summary saved to %s (%d bytes)", summary_path, Path(summary_path).stat().st_size)

    verify_all_outputs(outputs)
    return outputs
