#!/usr/bin/env python3
"""CLI for the CPM Network Diagram Generator."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from core.cpm_builder import build_cpm_network
from core.validator import validate


def _load_input(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        if path.suffix in (".yaml", ".yml"):
            import yaml
            return yaml.safe_load(f)
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description="CPM Network Diagram Generator")
    parser.add_argument("input", help="Path to cpm_network_input.json or YAML file")
    parser.add_argument("-o", "--output-dir", default="./output", help="Output directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--validate-only", action="store_true", help="Validate only")

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

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "cpm_diagram.vsdx"

    try:
        build_cpm_network(payload, str(output_path))
    except Exception as exc:
        logging.error("Build failed: %s", exc)
        return 1

    logging.info("Generated %s (%s bytes)", output_path, output_path.stat().st_size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
