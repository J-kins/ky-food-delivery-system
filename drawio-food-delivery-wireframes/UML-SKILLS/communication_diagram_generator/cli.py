#!/usr/bin/env python3
"""CLI for the Communication Diagram Generator."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from core.comm_builder import build_communication_diagram
from core.validator import validate


def _load_input(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        if path.suffix in (".yaml", ".yml"):
            import yaml
            return yaml.safe_load(f)
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Communication Diagram in Visio format (.vsdx)"
    )
    parser.add_argument("input", help="Path to input JSON or YAML specification file")
    parser.add_argument(
        "-o", "--output",
        default="./output/communication_diagram.vsdx",
        help="Output path (default: ./output/communication_diagram.vsdx)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    parser.add_argument("--no-legend", action="store_true", help="Skip legend generation")
    parser.add_argument("--validate-only", action="store_true", help="Validate without rendering")

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    try:
        payload = _load_input(Path(args.input))
        validate(payload)
    except Exception as exc:
        logging.error("Validation failed: %s", exc)
        return 1

    if args.validate_only:
        logging.info("Validation successful.")
        return 0

    try:
        if args.no_legend:
            from core.diagram_builder import CommunicationDiagramBuilder
            builder = CommunicationDiagramBuilder(payload)
            builder.build(include_legend=False)
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            builder.save(args.output)
        else:
            build_communication_diagram(payload, args.output)
    except Exception as exc:
        logging.error("Build failed: %s", exc)
        return 1

    p = Path(args.output)
    logging.info("Generated %s (%s bytes)", args.output, p.stat().st_size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
