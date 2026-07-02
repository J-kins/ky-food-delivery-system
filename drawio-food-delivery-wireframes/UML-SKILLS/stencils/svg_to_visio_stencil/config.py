"""Configuration loading and validation for the SVG-to-Visio converter."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ConverterConfig:
    stencil_name: str
    stencil_description: str
    stencil_version: str
    stencil_author: str
    input_directory: Path
    shape_library_path: Path
    manifest_path: Path
    output_file: Path
    template_output: Optional[Path]
    logs_directory: Path
    svg_dpi: float
    categories: Dict[str, Dict[str, str]]
    shape_styling: Dict[str, Any]
    connection_points: Dict[str, Any]
    output_options: Dict[str, Any]
    config_dir: Path = field(repr=False)
    shape_index: Dict[str, Dict[str, Any]] = field(default_factory=dict, repr=False)

    @classmethod
    def load(cls, config_path: str | Path) -> "ConverterConfig":
        config_path = Path(config_path).resolve()
        with open(config_path, encoding="utf-8") as handle:
            raw = json.load(handle)

        config_dir = config_path.parent

        def resolve(value: str) -> Path:
            path = Path(value)
            if not path.is_absolute():
                path = (config_dir / path).resolve()
            return path

        manifest_path = resolve(raw["manifest"])
        shape_library_path = resolve(raw["shape_library"])
        shape_index = _build_shape_index(manifest_path, shape_library_path)

        return cls(
            stencil_name=raw.get("stencil_name", "Custom Shape Stencil"),
            stencil_description=raw.get("stencil_description", ""),
            stencil_version=raw.get("stencil_version", "1.0.0"),
            stencil_author=raw.get("stencil_author", "SVG to Visio Converter"),
            input_directory=resolve(raw["input_directory"]),
            shape_library_path=shape_library_path,
            manifest_path=manifest_path,
            output_file=resolve(raw["output_file"]),
            template_output=resolve(raw["template_output"]) if raw.get("template_output") else None,
            logs_directory=resolve(raw.get("logs_directory", "logs")),
            svg_dpi=float(raw.get("svg_dpi", 96.0)),
            categories=raw.get("categories", {}),
            shape_styling=raw.get("shape_styling", {}),
            connection_points=raw.get("connection_points", {}),
            output_options=raw.get("output_options", {}),
            config_dir=config_dir,
            shape_index=shape_index,
        )

    def category_display_name(self, category_id: str) -> str:
        entry = self.categories.get(category_id, {})
        return entry.get("name", category_id.replace("-", " ").title())

    def category_description(self, category_id: str) -> str:
        entry = self.categories.get(category_id, {})
        return entry.get("description", "")

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.input_directory.is_dir():
            errors.append(f"Input directory not found: {self.input_directory}")
        if not self.manifest_path.is_file():
            errors.append(f"Manifest not found: {self.manifest_path}")
        if not self.shape_library_path.is_file():
            errors.append(f"Shape library not found: {self.shape_library_path}")
        return errors


def _build_shape_index(
    manifest_path: Path,
    shape_library_path: Path,
) -> Dict[str, Dict[str, Any]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    library = json.loads(shape_library_path.read_text(encoding="utf-8"))

    library_by_id: Dict[str, Dict[str, Any]] = {}
    for category in library.get("categories", []):
        for shape in category.get("shapes", []):
            library_by_id[shape["id"]] = {
                **shape,
                "category_id": category["id"],
                "category_name": category["name"],
            }

    index: Dict[str, Dict[str, Any]] = {}
    for entry in manifest.get("shapes", []):
        shape_id = entry["id"]
        merged = {
            "id": shape_id,
            "name": entry.get("name", shape_id),
            "category": entry.get("category", ""),
            "delivery": entry.get("delivery", "generate"),
            "status": entry.get("status", ""),
            "path": entry.get("path", ""),
            "asset_type": "shape",
            "description": "",
            "purpose": "",
        }
        if shape_id in library_by_id:
            lib = library_by_id[shape_id]
            merged.update(
                {
                    "name": lib.get("name", merged["name"]),
                    "description": lib.get("description", ""),
                    "purpose": lib.get("purpose", ""),
                    "asset_type": lib.get("asset_type", "shape"),
                    "category": lib.get("category_id", merged["category"]),
                    "category_name": lib.get("category_name", ""),
                }
            )
        index[shape_id] = merged
    return index
