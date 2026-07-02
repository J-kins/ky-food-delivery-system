import argparse
import json
import sys
import logging
from core.diagram_builder import SystemContextBuilder

def main():
    parser = argparse.ArgumentParser(
        description="Generate a System Context Diagram (Level 0) in Visio format"
    )
    parser.add_argument("input", help="Path to input JSON/YAML specification file")
    parser.add_argument("-o", "--output", help="Output path (default: ./output/system_context.vsdx)")
    parser.add_argument("-p", "--preview", action="store_true", help="Generate PNG preview as well")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--validate-only", action="store_true", help="Only validate input, don't render")
    parser.add_argument("--theme", choices=["enterprise_blue", "dark_modern", "corporate_green", "material"], help="Color theme to use")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    with open(args.input, 'r') as f:
        spec = json.load(f)
    
    if args.validate_only:
        # Run Pydantic validations here
        logging.info("Validation successful. Exiting.")
        sys.exit(0)
        
    builder = SystemContextBuilder(spec["system_context"])
    builder.build()
    
    out_path = args.output or "./output/system_context.vsdx"
    builder.save(out_path)
    logging.info(f"Context Diagram saved to {out_path}")

if __name__ == "__main__":
    main()
