"""Orchestrate budget validation, Excel workbook, and Visio dashboard generation."""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict

from config.settings import apply_aspose_diagram_license
from core.validator import validate
from excel.budget_excel_builder import BudgetExcelBuilder
from visio.budget_visio_builder import BudgetVisioBuilder

log = logging.getLogger(__name__)

MIN_XLSX_BYTES = 4_000
MIN_VSDX_BYTES = 5_000


def _verify_file(path: str, min_bytes: int, label: str) -> None:
    p = Path(path)
    if not p.is_file():
        raise RuntimeError(f"{label} not created: {path}")
    size = p.stat().st_size
    if size < min_bytes:
        raise RuntimeError(f"{label} too small ({size} bytes): {path}")


def build_budget(
    spec_dict: Dict[str, Any],
    output_dir: str,
    *,
    excel_only: bool = False,
    visio_only: bool = False,
) -> Dict[str, str]:
    apply_aspose_diagram_license()
    spec = validate(spec_dict)
    log.info("Payload validated successfully.")

    os.makedirs(output_dir, exist_ok=True)
    outputs: Dict[str, str] = {}

    if not visio_only:
        excel_path = os.path.join(output_dir, "budget_breakdown.xlsx")
        eb = BudgetExcelBuilder(spec)
        eb.build()
        eb.save(excel_path)
        _verify_file(excel_path, MIN_XLSX_BYTES, "Excel workbook")
        outputs["excel"] = excel_path
        log.info("Excel saved to %s (%d bytes)", excel_path, Path(excel_path).stat().st_size)

    if not excel_only:
        visio_path = os.path.join(output_dir, "budget_dashboard.vsdx")
        vb = BudgetVisioBuilder(spec)
        vb.build()
        vb.save(visio_path)
        _verify_file(visio_path, MIN_VSDX_BYTES, "Visio dashboard")
        outputs["visio"] = visio_path
        log.info("Visio saved to %s (%d bytes)", visio_path, Path(visio_path).stat().st_size)

    return outputs
