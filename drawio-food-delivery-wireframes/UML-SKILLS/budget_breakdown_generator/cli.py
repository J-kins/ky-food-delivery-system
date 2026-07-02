#!/usr/bin/env python3
"""CLI for the Budget Breakdown Generator."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from core.budget_builder import build_budget
from core.input_merger import write_merged_outputs
from core.validator import validate


def _load_input(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        if path.suffix in (".yaml", ".yml"):
            import yaml
            return yaml.safe_load(f)
        return json.load(f)


def cmd_merge(args: argparse.Namespace) -> int:
    inputs_dir = Path(args.inputs_dir)
    if not inputs_dir.is_dir():
        logging.error("Inputs directory not found: %s", inputs_dir)
        return 1
    written = write_merged_outputs(inputs_dir)
    for name, path in written.items():
        logging.info("Wrote %s", path)
        if args.validate:
            validate(_load_input(path))
    logging.info("Merge complete (%d MAIN files).", len(written))
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    payload = _load_input(Path(args.input))
    try:
        validate(payload)
    except Exception as exc:
        logging.error("Validation failed: %s", exc)
        return 1

    if args.validate_only:
        logging.info("Validation successful.")
        return 0

    try:
        outputs = build_budget(
            payload,
            args.output_dir,
            excel_only=args.excel_only,
            visio_only=args.visio_only,
        )
    except Exception as exc:
        logging.error("Build failed: %s", exc)
        return 1

    for path in outputs.values():
        p = Path(path)
        if p.is_file():
            logging.info("Generated %s (%s bytes)", path, p.stat().st_size)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Budget Breakdown Generator")
    sub = parser.add_subparsers(dest="command")

    merge_p = sub.add_parser("merge", help="Merge split JSON files into MAIN files")
    merge_p.add_argument("inputs_dir", help="Directory containing budget_*_input.json split files")
    merge_p.add_argument("--validate", action="store_true", help="Validate merged MAIN files")
    merge_p.set_defaults(func=cmd_merge)

    build_p = sub.add_parser("build", help="Build Excel workbook and/or Visio dashboard")
    build_p.add_argument("input", help="Path to budget_input.json or MAIN file")
    build_p.add_argument("-o", "--output-dir", default="./output", help="Output directory")
    build_p.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    build_p.add_argument("--validate-only", action="store_true", help="Validate only")
    build_p.add_argument("--excel-only", action="store_true", help="Excel workbook only")
    build_p.add_argument("--visio-only", action="store_true", help="Visio dashboard only")
    build_p.set_defaults(func=cmd_build)

    # Back-compat: `cli.py input.json` without subcommand
    parser.add_argument("legacy_input", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("-o", "--output-dir", default="./output", dest="legacy_output_dir")
    parser.add_argument("-v", "--verbose", action="store_true", dest="legacy_verbose")
    parser.add_argument("--validate-only", action="store_true", dest="legacy_validate_only")
    parser.add_argument("--excel-only", action="store_true", dest="legacy_excel_only")
    parser.add_argument("--visio-only", action="store_true", dest="legacy_visio_only")

    args = parser.parse_args()
    if args.command:
        logging.basicConfig(level=logging.DEBUG if getattr(args, "verbose", False) else logging.INFO)
        return args.func(args)

    if not args.legacy_input:
        parser.print_help()
        return 1

    args.input = args.legacy_input
    args.output_dir = args.legacy_output_dir
    args.validate_only = args.legacy_validate_only
    args.excel_only = args.legacy_excel_only
    args.visio_only = args.legacy_visio_only
    logging.basicConfig(level=logging.DEBUG if args.legacy_verbose else logging.INFO)
    return cmd_build(args)


if __name__ == "__main__":
    sys.exit(main())
