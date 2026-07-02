"""Build Visio stencil documents from converted masters."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from tqdm import tqdm

from .config import ConverterConfig
from .shape_converter import ShapeConverter
from .svg_parser import parse_svg_file
from .utils import ensure_parent

log = logging.getLogger("svg_to_visio")


@dataclass
class ConversionStats:
    total: int = 0
    success: int = 0
    failed: int = 0
    skipped: int = 0
    errors: List[str] = field(default_factory=list)


class StencilBuilder:
    def __init__(self, config: ConverterConfig) -> None:
        self.config = config
        self.converter = ShapeConverter(config)
        self.stats = ConversionStats()

    def build(self, category_filter: Optional[str] = None) -> Path:
        entries = self._collect_entries(category_filter)
        self.stats.total = len(entries)

        if self.config.output_options.get("per_category_stencils") and category_filter is None:
            return self._build_per_category(entries)

        return self._build_single(entries, self.config.output_file, category_filter)

    def _collect_entries(self, category_filter: Optional[str]) -> List[Dict]:
        manifest = json.loads(self.config.manifest_path.read_text(encoding="utf-8"))
        skip_files = set(self.config.output_options.get("skip_files", ["sprite.svg"]))
        entries: List[Dict] = []

        for entry in manifest.get("shapes", []):
            if category_filter and entry.get("category") != category_filter:
                continue
            if entry.get("delivery") == "annotation":
                self.stats.skipped += 1
                continue

            rel_path = entry.get("path")
            if not rel_path:
                self.stats.skipped += 1
                continue
            rel = Path(rel_path)
            if rel.name in skip_files:
                self.stats.skipped += 1
                continue

            if rel.parts and rel.parts[0] == "shapes":
                svg_path = (self.config.input_directory / Path(*rel.parts[1:])).resolve()
            else:
                svg_path = (self.config.input_directory / rel).resolve()
            if not svg_path.is_file():
                self.stats.skipped += 1
                log.warning("SVG not found for %s (%s)", entry.get("id"), rel_path)
                continue

            metadata = dict(self.config.shape_index.get(entry["id"], {}))
            metadata.update(
                {
                    "id": entry["id"],
                    "name": metadata.get("name", entry.get("name", entry["id"])),
                    "category": entry.get("category", metadata.get("category", "")),
                    "source_file": str(svg_path),
                }
            )
            if not metadata.get("category_name"):
                metadata["category_name"] = self.config.category_display_name(metadata["category"])
            entries.append({"svg_path": svg_path, "metadata": metadata})

        return entries

    def _build_single(
        self,
        entries: List[Dict],
        output_file: Path,
        category_filter: Optional[str],
    ) -> Path:
        from . import visio_builder

        diagram = visio_builder.new_diagram()
        diagram.getDocumentSettings().setTopPage(0)
        diagram.getDocumentSettings().setDefaultFillStyle(0)
        diagram.getDocumentProps().setTitle(self.config.stencil_name)
        diagram.getDocumentProps().setSubject(self.config.stencil_description)
        diagram.getDocumentProps().setCreator(self.config.stencil_author)

        category_masters: Dict[str, List[object]] = {}
        iterator = tqdm(entries, desc="Converting shapes", unit="shape")
        for entry in iterator:
            svg_path = entry["svg_path"]
            metadata = entry["metadata"]
            iterator.set_postfix_str(metadata["name"][:24])
            try:
                parsed = parse_svg_file(svg_path)
                master = self.converter.convert_to_master(parsed, metadata)
                diagram.getMasters().add(master)
                category_masters.setdefault(metadata["category"], []).append(master)
                self.stats.success += 1
                log.debug("Converted %s", metadata["id"])
            except Exception as exc:
                self.stats.failed += 1
                message = f"{metadata.get('id', svg_path.name)}: {exc}"
                self.stats.errors.append(message)
                log.error("Failed to convert %s: %s", svg_path.name, exc)

        ensure_parent(output_file)
        visio_builder.save_diagram(diagram, str(output_file), visio_builder.api().SaveFileFormat.VSSX)
        log.info("Stencil saved to %s (%d masters)", output_file, diagram.getMasters().getCount())
        return output_file

    def _build_per_category(self, entries: List[Dict]) -> Path:
        categories = sorted({entry["metadata"]["category"] for entry in entries})
        last_output = self.config.output_file
        for category_id in categories:
            category_entries = [e for e in entries if e["metadata"]["category"] == category_id]
            slug = category_id.replace("_", "-")
            output_file = self.config.output_file.parent / f"{slug}.vssx"
            last_output = self._build_single(category_entries, output_file, category_id)
        return last_output

    def log_summary(self) -> None:
        log.info("=" * 50)
        log.info("CONVERSION SUMMARY")
        log.info("Total files:  %d", self.stats.total)
        log.info("Successful:   %d", self.stats.success)
        log.info("Failed:       %d", self.stats.failed)
        log.info("Skipped:      %d", self.stats.skipped)
        if self.stats.errors:
            log.info("Errors:")
            for err in self.stats.errors[:20]:
                log.info("  - %s", err)
            if len(self.stats.errors) > 20:
                log.info("  ... and %d more", len(self.stats.errors) - 20)
        log.info("=" * 50)
