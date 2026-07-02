import argparse
import json
import sys
import logging
import os
from core.diagram_builder import PERTChartBuilder
from core.validator import validate_pert

def main():
    parser = argparse.ArgumentParser(
        description="Generate a PERT Chart / Project Network Diagram in Visio format"
    )
    parser.add_argument("input", help="Path to input JSON/YAML specification file")
    parser.add_argument("-o", "--output", help="Output path (default: ./output/pert_chart.vsdx)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--show-three-point", action="store_true", help="Show (O, M, P) estimates in nodes")
    parser.add_argument("--validate-only", action="store_true", help="Only validate graph logic, don't render")
    
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s | %(message)s"
    )
    
    with open(args.input, 'r') as f:
        spec_dict = json.load(f)
        
    if args.show_three_point:
        spec_dict["pert_chart"].setdefault("styling", {})["show_three_point"] = True
        
    try:
        spec = validate_pert(spec_dict)
    except Exception as e:
        logging.error(f"Validation Error: {e}")
        sys.exit(1)
        
    if args.validate_only:
        logging.info("Graph validation successful. Exiting.")
        sys.exit(0)
        
    builder = PERTChartBuilder(spec.model_dump()["pert_chart"])
    builder.build()
    
    out_path = args.output or "./output/pert_chart.vsdx"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    builder.save(out_path)
    logging.info(f"PERT Chart saved to {out_path}")

if __name__ == "__main__":
    main()
