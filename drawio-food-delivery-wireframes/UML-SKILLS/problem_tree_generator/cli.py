import argparse
import json
import sys
import logging
import os
from core.diagram_builder import ProblemTreeBuilder
from core.validator import validate_schema


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Problem Tree Diagram in Visio format"
    )
    parser.add_argument("input", help="Path to input JSON/YAML specification file")
    parser.add_argument("-o", "--output", help="Output path (default: ./output/problem_tree.vsdx)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--validate-only", action="store_true", help="Only validate input, don't render")
    parser.add_argument(
        "--theme",
        choices=["enterprise_blue", "dark_modern", "corporate_green", "material"],
        help="Color theme override"
    )

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s | %(message)s"
    )

    # Load input
    with open(args.input, 'r') as f:
        spec_dict = json.load(f)

    # Apply theme override
    if args.theme:
        spec_dict.setdefault("problem_tree", {}).setdefault("styling", {})["theme"] = args.theme

    # Validate
    try:
        spec = validate_schema(spec_dict)
    except Exception as e:
        logging.error(f"Validation Error: {e}")
        sys.exit(1)

    if args.validate_only:
        logging.info("Validation successful. Exiting.")
        sys.exit(0)

    # Build
    pt = spec.model_dump()["problem_tree"]
    builder = ProblemTreeBuilder(pt)

    builder.add_title_block()
    builder.add_roots(pt.get("roots", []))
    builder.add_trunk(pt["core_problem"])
    builder.add_branches(pt.get("branches", []))
    builder.add_leaf(pt.get("leaf", []))
    builder.add_connectors()
    builder.add_legend()

    out_path = args.output or "./output/problem_tree.vsdx"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    builder.save(out_path)
    logging.info(f"Successfully saved Visio diagram to {out_path}")


if __name__ == "__main__":
    main()
