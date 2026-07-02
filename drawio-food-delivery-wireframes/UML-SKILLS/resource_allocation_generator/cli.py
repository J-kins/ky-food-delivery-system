import argparse
import json
import logging
import sys
from core.diagram_builder import ResourceAllocationBuilder

def main():
    parser = argparse.ArgumentParser(description="Generate Visio Resource Allocation Matrix")
    parser.add_argument("input", help="Path to input JSON/YAML file")
    parser.add_argument("-o", "--output", help="Output VSDX path (default: ./output/resource_allocation.vsdx)")
    parser.add_argument("-p", "--preview", action="store_true", help="Generate PNG preview")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--type",
        choices=["RACI", "PERCENTAGE", "BOTH"],
        default="RACI",
        help="Allocation display mode"
    )
    parser.add_argument("--validate-only", action="store_true", help="Validate without rendering")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    with open(args.input, 'r') as f:
        spec = json.load(f)
    
    # Override allocation_type from CLI flag
    spec['resource_allocation']['allocation_type'] = args.type
    
    if args.validate_only:
        logging.info("Validation successful.")
        sys.exit(0)
    
    builder = ResourceAllocationBuilder(spec)
    builder.build()
    
    out_path = args.output or "./output/resource_allocation.vsdx"
    builder.save(out_path)
    logging.info(f"Resource Allocation Matrix saved to {out_path}")

if __name__ == "__main__":
    main()
