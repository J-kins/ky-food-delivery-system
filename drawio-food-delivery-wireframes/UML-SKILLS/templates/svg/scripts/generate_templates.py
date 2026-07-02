#!/usr/bin/env python3
"""
Generate blank diagram template SVGs (86 templates).

Usage:
  python scripts/generate_templates.py
  python scripts/generate_templates.py --only uml
  python scripts/generate_templates.py --id uml-class-diagram
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from template_builder import SvgBuilder  # noqa: E402
from template_catalog import all_templates, CATEGORIES  # noqa: E402
from template_layouts import render_layout  # noqa: E402

OUTPUT_ROOT = ROOT
MANIFEST_PATH = ROOT / "TEMPLATE_LIBRARY.json"


def build_svg(template) -> str:
    builder = SvgBuilder(template)
    builder._open()
    builder._chrome()
    render_layout(builder, template)
    builder._legend()
    builder._footer()
    builder.parts.append("</svg>\n")
    return "".join(builder.parts)


def write_manifest(entries: list) -> None:
    payload = {
        "version": "1.0",
        "title": "UML-SKILLS Diagram Template Library",
        "canvas": {"width": 1920, "height": 1080, "viewbox": "0 0 1920 1080"},
        "style_reference": "../stencils/briefs/PRIMEREACT_DESIGN_DIRECTION.md",
        "summary": {
            "total_templates": len(entries),
            "categories": len(CATEGORIES),
        },
        "templates": entries,
    }
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate diagram template SVGs")
    parser.add_argument("--only", help="Generate only templates in this category folder")
    parser.add_argument("--id", help="Generate a single template by slug id")
    args = parser.parse_args()

    templates = all_templates()
    if args.only:
        templates = [t for t in templates if t.category == args.only]
    if args.id:
        templates = [t for t in templates if t.id == args.id]

    if not templates:
        print("No templates matched.", file=sys.stderr)
        return 1

    manifest_entries = []
    for template in templates:
        out_path = OUTPUT_ROOT / template.output_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        svg = build_svg(template)
        out_path.write_text(svg, encoding="utf-8")
        manifest_entries.append(
            {
                "num": template.num,
                "id": template.id,
                "title": template.title,
                "category": template.category,
                "layout": template.layout,
                "description": template.description,
                "path": template.output_path,
            }
        )
        print(f"  wrote {template.output_path}")

    if args.id or args.only:
        write_manifest(manifest_entries)
    else:
        write_manifest(
            [
                {
                    "num": t.num,
                    "id": t.id,
                    "title": t.title,
                    "category": t.category,
                    "layout": t.layout,
                    "description": t.description,
                    "path": t.output_path,
                }
                for t in all_templates()
            ]
        )

    print(f"\nGenerated {len(templates)} template(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
