#!/usr/bin/env python3
"""CLI for the Project Charter Generator."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from core.charter_builder import build_charter
from core.input_merger import merge_all_from_directory, write_merged_outputs
from core.validator import validate_payload


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
            validate_payload(_load_input(path))
    logging.info("Merge complete (%d MAIN files).", len(written))
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    payload = _load_input(Path(args.input))
    try:
        validate_payload(payload)
    except Exception as exc:
        logging.error("Validation failed: %s", exc)
        return 1

    if args.validate_only:
        logging.info("Validation successful.")
        return 0

    try:
        outputs = build_charter(
            payload,
            args.output_dir,
            word_only=args.word_only,
            visio_only=args.visio_only,
        )
    except Exception as exc:
        logging.error("Build failed: %s", exc)
        return 1

    for key, path in outputs.items():
        if key.endswith("_dir"):
            continue
        p = Path(path)
        if p.is_file():
            logging.info("Generated %s (%s bytes)", path, p.stat().st_size)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Project Charter Generator")
    sub = parser.add_subparsers(dest="command")

    merge_p = sub.add_parser("merge", help="Merge nine split JSON files into MAIN files")
    merge_p.add_argument(
        "inputs_dir",
        help="Directory containing charter_*_input.json split files",
    )
    merge_p.add_argument("--validate", action="store_true", help="Validate merged MAIN files")
    merge_p.set_defaults(func=cmd_merge)

    build_p = sub.add_parser("build", help="Build charter from a MAIN JSON file")
    build_p.add_argument("input", help="Path to charter_input.json (or word/visio MAIN)")
    build_p.add_argument("-o", "--output-dir", default="./output", help="Output directory")
    build_p.add_argument("--validate-only", action="store_true")
    build_p.add_argument("--word-only", action="store_true")
    build_p.add_argument("--visio-only", action="store_true")
    build_p.add_argument("-v", "--verbose", action="store_true")
    build_p.set_defaults(func=cmd_build)

    # Default: treat first positional arg as build input (backward compatible)
    parser.add_argument(
        "input_legacy",
        nargs="?",
        help=argparse.SUPPRESS,
    )
    parser.add_argument("-o", "--output-dir", default="./output", dest="output_dir_legacy")
    parser.add_argument("--validate-only", action="store_true", dest="validate_only_legacy")
    parser.add_argument("--word-only", action="store_true", dest="word_only_legacy")
    parser.add_argument("--visio-only", action="store_true", dest="visio_only_legacy")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    if args.command:
        return args.func(args)

    if args.input_legacy:
        ns = argparse.Namespace(
            input=args.input_legacy,
            output_dir=args.output_dir_legacy,
            validate_only=args.validate_only_legacy,
            word_only=args.word_only_legacy,
            visio_only=args.visio_only_legacy,
        )
        return cmd_build(ns)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
