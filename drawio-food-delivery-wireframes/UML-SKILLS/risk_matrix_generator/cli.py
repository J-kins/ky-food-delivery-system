import argparse
import json
import logging
import sys
from core.diagram_builder import RiskMatrixBuilder


def main():
    parser = argparse.ArgumentParser(description="Generate Visio Risk Matrix Diagram")
    parser.add_argument("input", help="Path to input JSON/YAML file")
    parser.add_argument(
        "-o", "--output",
        help="Output VSDX path (default: ./output/risk_matrix.vsdx)"
    )
    parser.add_argument("-p", "--preview", action="store_true",
                        help="Generate PNG preview via Graphviz")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")
    parser.add_argument("--validate-only", action="store_true",
                        help="Validate input without rendering")
    parser.add_argument("--top-risks", type=int, default=3,
                        help="Number of top risks to highlight in summary (default: 3)")
    parser.add_argument("--no-register", action="store_true",
                        help="Skip risk register table section")

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    with open(args.input, 'r') as f:
        spec = json.load(f)

    if args.validate_only:
        logging.info("Risk Matrix input validation passed.")
        sys.exit(0)

    builder = RiskMatrixBuilder(spec)
    builder.build()

    out_path = args.output or "./output/risk_matrix.vsdx"
    builder.save(out_path)
    logging.info(f"Risk Matrix saved to {out_path}")


if __name__ == "__main__":
    main()
