import argparse
import json
import logging
import sys
from core.diagram_builder import RACIMatrixBuilder

def main():
    parser = argparse.ArgumentParser(description="Generate Visio RACI Matrix")
    parser.add_argument("input", help="Path to input JSON/YAML file")
    parser.add_argument("-o", "--output", help="Output VSDX path (default: ./output/raci_matrix.vsdx)")
    parser.add_argument("-p", "--preview", action="store_true", help="Generate PNG preview")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--validate-only", action="store_true", help="Validate RACI rules without rendering")
    parser.add_argument("--gap-report", action="store_true", help="Print gap analysis report to stdout")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    with open(args.input, 'r') as f:
        spec = json.load(f)
    
    if args.validate_only:
        builder = RACIMatrixBuilder(spec)  # Validation runs in __init__
        logging.info("RACI validation passed. All rules satisfied.")
        sys.exit(0)
    
    builder = RACIMatrixBuilder(spec)
    builder.build()
    
    out_path = args.output or "./output/raci_matrix.vsdx"
    builder.save(out_path)
    logging.info(f"RACI Matrix saved to {out_path}")

if __name__ == "__main__":
    main()
