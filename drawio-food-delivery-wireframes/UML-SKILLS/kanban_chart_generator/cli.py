#!/usr/bin/env python3
"""CLI for the Kanban Chart Generator."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from core.kanban_builder import build_kanban
from core.validator import validate_kanban


def _load_input(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        if path.suffix in (".yaml", ".yml"):
            import yaml
            return yaml.safe_load(f)
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Visio Kanban Dashboard")
    parser.add_argument("input", help="Path to kanban_input.json or YAML file")
    parser.add_argument(
        "-o", "--output",
        help="Output VSDX path (default: ./output/kanban_chart.vsdx)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--validate-only", action="store_true", help="Validate without rendering")

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    try:
        payload = _load_input(Path(args.input))
        validate_kanban(payload)
    except Exception as exc:
        logging.error("Validation failed: %s", exc)
        return 1

    if args.validate_only:
        logging.info("Kanban schema validation successful.")
        return 0

    out_path = args.output or "./output/kanban_chart.vsdx"
    try:
        build_kanban(payload, out_path)
    except Exception as exc:
        logging.error("Build failed: %s", exc)
        return 1

    p = Path(out_path)
    logging.info("Generated %s (%s bytes)", out_path, p.stat().st_size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
