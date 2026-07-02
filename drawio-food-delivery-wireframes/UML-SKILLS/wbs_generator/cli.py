#!/usr/bin/env python3
"""CLI for the WBS Diagram Generator."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from core.validator import validate_wbs
from core.wbs_builder import build_wbs


def _load_input(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        if path.suffix in (".yaml", ".yml"):
            import yaml
            return yaml.safe_load(f)
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate WBS Diagram in Visio format")
    parser.add_argument("input", help="Path to wbs_input.json or YAML file")
    parser.add_argument("-o", "--output", help="Output VSDX path (default: ./output/wbs_diagram.vsdx)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--layout", choices=["tree", "org_chart"], default=None, help="Layout style")
    parser.add_argument("--validate-only", action="store_true", help="Validate without rendering")

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    try:
        payload = _load_input(Path(args.input))
        validate_wbs(payload)
    except Exception as exc:
        logging.error("Validation failed: %s", exc)
        return 1

    if args.validate_only:
        logging.info("Validation successful.")
        return 0

    out_path = args.output or "./output/wbs_diagram.vsdx"
    try:
        build_wbs(payload, out_path, layout_style=args.layout)
    except Exception as exc:
        logging.error("Build failed: %s", exc)
        return 1

    p = Path(out_path)
    logging.info("Generated %s (%s bytes)", out_path, p.stat().st_size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
