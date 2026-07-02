#!/usr/bin/env python3
"""Convert SVG stencil shapes into a Visio stencil (.vssx) file."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import ConverterConfig
from .stencil_builder import StencilBuilder
from .template_builder import build_template
from .utils import setup_logging


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    package_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Convert SVG shapes to a Visio stencil (.vssx) using Aspose.Diagram.",
    )
    parser.add_argument(
        "-c",
        "--config",
        default=str(package_dir / "config.json"),
        help="Path to configuration file (JSON)",
    )
    parser.add_argument("-i", "--input", help="Override input directory containing SVG files")
    parser.add_argument("-o", "--output", help="Override output .vssx file path")
    parser.add_argument("--category", help="Convert only a single category id")
    parser.add_argument("--per-category", action="store_true", help="Write one .vssx per category")
    parser.add_argument("--create-template", action="store_true", help="Also generate a .vstx template")
    parser.add_argument("--validate-only", action="store_true", help="Validate configuration and exit")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = ConverterConfig.load(args.config)

    if args.input:
        config.input_directory = Path(args.input).resolve()
    if args.output:
        config.output_file = Path(args.output).resolve()
    if args.per_category:
        config.output_options["per_category_stencils"] = True

    errors = config.validate()
    if errors:
        for err in errors:
            print(f"Configuration error: {err}", file=sys.stderr)
        return 1

    if args.validate_only:
        print("Configuration validated successfully.")
        print(f"  Input:  {config.input_directory}")
        print(f"  Output: {config.output_file}")
        print(f"  Shapes indexed: {len(config.shape_index)}")
        return 0

    logger = setup_logging(config.logs_directory, verbose=args.verbose)
    logger.info("Starting SVG to Visio stencil conversion")
    logger.info("Input directory: %s", config.input_directory)
    logger.info("Output file: %s", config.output_file)

    builder = StencilBuilder(config)
    stencil_path = builder.build(category_filter=args.category)
    builder.log_summary()

    if args.create_template or config.output_options.get("create_template"):
        try:
            build_template(config, stencil_path)
        except Exception as exc:
            logger.error("Template generation failed: %s", exc)

    return 0 if builder.stats.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
