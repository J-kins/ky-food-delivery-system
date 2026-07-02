"""Merge nine split budget JSON files into Excel, Visio, or combined MAIN payloads."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

SPLIT_FILENAMES = {
    "metadata": "budget_metadata_input.json",
    "categories": "budget_categories_input.json",
    "line_items": "budget_line_items_input.json",
    "burn_rate": "budget_monthly_burn_rate_input.json",
    "excel_styling": "budget_excel_styling_input.json",
    "visio_dashboard": "budget_visio_dashboard_input.json",
}


def _load_json(path: Path) -> Dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _budget_section(data: Dict[str, Any]) -> Dict[str, Any]:
    return dict(data.get("budget", data))


def merge_excel_input(
    metadata: Dict[str, Any],
    categories: Dict[str, Any],
    line_items: Dict[str, Any],
    burn_rate: Dict[str, Any],
    excel_styling: Dict[str, Any],
) -> Dict[str, Any]:
    budget: Dict[str, Any] = {}
    for part in (metadata, categories, line_items, burn_rate, excel_styling):
        budget.update(_budget_section(part))
    return {"budget": budget}


def merge_visio_input(
    metadata: Dict[str, Any],
    categories: Dict[str, Any],
    burn_rate: Dict[str, Any],
    visio_dashboard: Dict[str, Any],
) -> Dict[str, Any]:
    budget: Dict[str, Any] = {}
    for part in (metadata, categories, burn_rate):
        budget.update(_budget_section(part))
    dash = _budget_section(visio_dashboard)
    if "layout" in dash:
        budget["layout"] = dash["layout"]
    if "dashboard" in dash:
        budget["dashboard"] = dash["dashboard"]
    budget["line_items"] = []
    budget.setdefault("styling", {"font_family": "Arial"})
    return {"budget": budget}


def merge_combined_input(
    metadata: Dict[str, Any],
    categories: Dict[str, Any],
    line_items: Dict[str, Any],
    burn_rate: Dict[str, Any],
    excel_styling: Dict[str, Any],
    visio_dashboard: Dict[str, Any],
) -> Dict[str, Any]:
    budget: Dict[str, Any] = {}
    for part in (metadata, categories, line_items, burn_rate, excel_styling):
        budget.update(_budget_section(part))
    dash = _budget_section(visio_dashboard)
    if "layout" in dash:
        budget["layout"] = dash["layout"]
    if "dashboard" in dash:
        budget["dashboard"] = dash["dashboard"]
    return {"budget": budget}


def load_splits_from_directory(inputs_dir: Path) -> Dict[str, Dict[str, Any]]:
    parts: Dict[str, Dict[str, Any]] = {}
    for key, filename in SPLIT_FILENAMES.items():
        path = inputs_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing split file: {path}")
        parts[key] = _load_json(path)
    return parts


def merge_all_from_directory(inputs_dir: Path) -> Dict[str, Dict[str, Any]]:
    p = load_splits_from_directory(inputs_dir)
    shared = (p["metadata"], p["categories"], p["line_items"], p["burn_rate"])
    return {
        "budget_excel_input.json": merge_excel_input(
            p["metadata"], p["categories"], p["line_items"], p["burn_rate"], p["excel_styling"]
        ),
        "budget_visio_input.json": merge_visio_input(
            p["metadata"], p["categories"], p["burn_rate"], p["visio_dashboard"]
        ),
        "budget_input.json": merge_combined_input(
            p["metadata"],
            p["categories"],
            p["line_items"],
            p["burn_rate"],
            p["excel_styling"],
            p["visio_dashboard"],
        ),
    }


def write_merged_outputs(inputs_dir: Path) -> Dict[str, Path]:
    merged = merge_all_from_directory(inputs_dir)
    written: Dict[str, Path] = {}
    for filename, payload in merged.items():
        out = inputs_dir / filename
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
            f.write("\n")
        written[filename] = out
    return written
