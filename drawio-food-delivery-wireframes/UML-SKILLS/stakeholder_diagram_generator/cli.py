import argparse
import json
import logging
import sys
import os
from core.diagram_builder import StakeholderDiagramBuilder
from core.validator import validate_and_enrich


def main():
    parser = argparse.ArgumentParser(
        description="Generate Visio Stakeholder Diagrams"
    )
    parser.add_argument("config", help="Path to input JSON specification file")
    parser.add_argument(
        "-o", "--output",
        default="./output",
        help="Output directory (default: ./output)"
    )
    parser.add_argument(
        "--combined",
        action="store_true",
        help="Output all diagrams as pages in a single Visio file"
    )
    parser.add_argument(
        "--theme",
        default="enterprise_blue",
        help="Color theme"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--validate-only", action="store_true", help="Validate input without rendering")

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s | %(message)s"
    )

    with open(args.config, "r") as f:
        spec_dict = json.load(f)

    try:
        spec = validate_and_enrich(spec_dict)
    except Exception as e:
        logging.error(f"Validation Error: {e}")
        sys.exit(1)

    if args.validate_only:
        logging.info("Validation passed. All required fields present.")
        sys.exit(0)

    os.makedirs(args.output, exist_ok=True)

    # Convert the pydantic model back to a dict for the builder to use
    builder = StakeholderDiagramBuilder(spec.model_dump())
    builder.build_all()

    if args.combined:
        out_path = os.path.join(args.output, "complete", "stakeholder_analysis_package.vsdx")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        builder.save_combined(out_path)
        logging.info(f"Combined package saved to {out_path}")
    else:
        builder.save_all(args.output)
        logging.info(f"Individual diagrams saved to {args.output}/")

if __name__ == "__main__":
    main()
