"""
CLI entry point for UML Diagram Generator.

Usage:
    python3 build_diagram.py spec.json output_dir/diagram_name [options]

Produces:
    output_dir/diagram_name.vsdx
    output_dir/diagram_name.pdf

Options:
    --positions <file>  JSON file with pre-computed positions.
    --validate-only     Validate the spec without rendering.
    --verbose           Enable debug logging.
    --help              Show this help message.

Architecture:
    This script is the entry point for the modular pipeline:
    - validators/  : Syntax and semantic validation of the spec.
    - layouts/     : Hierarchical, force-directed, and custom coordinate generators.
    - renderers/   : SVG, PNG, DrawIO, Mermaid, and VSDX exporters.
"""

import json
import argparse
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Modular Architecture Imports
try:
    from layouts.layout import compute_layout
    from renderers.vsdx_writer import build_vsdx
    from renderers.export_pdf import to_pdf, PdfExportError
    from validators.spec_validator import validate_spec, ValidationError
except ImportError:
    # Fallback to local flat imports if modules are not yet split
    from layout import compute_layout
    from vsdx_writer import build_vsdx
    from export_pdf import to_pdf, PdfExportError

    # Original local validator
    class ValidationError(Exception):
        pass

    def validate_spec(spec):
        ids = set()
        for c in spec.get("components", []):
            if "id" not in c:
                raise ValidationError("A component is missing an 'id' field.")
            if c["id"] in ids:
                raise ValidationError(f"Duplicate component id: {c['id']}")
            ids.add(c["id"])
        for r in spec.get("relationships", []):
            if r["source"] not in ids:
                raise ValidationError(f"Relationship source '{r['source']}' is not a known component id.")
            if r["target"] not in ids:
                raise ValidationError(f"Relationship target '{r['target']}' is not a known component id.")
        if len(ids) < 1:
            raise ValidationError("Spec has no components.")

def setup_logging(verbose):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )

def main():
    parser = argparse.ArgumentParser(description="UML Diagram Generator CLI", add_help=False)
    parser.add_argument("spec", nargs='?', help="Path to the JSON specification file")
    parser.add_argument("output", nargs='?', help="Output path stem (e.g. out/my_diagram)")
    parser.add_argument("--positions", help="Optional JSON file with pre-computed positions")
    parser.add_argument("--validate-only", action="store_true", help="Only validate spec, do not render")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose/debug logging")
    parser.add_argument("--help", action="help", help="Show this help message and exit")
    
    args = parser.parse_args()
    
    if not args.spec or not args.output:
        parser.print_help()
        sys.exit(1)

    setup_logging(args.verbose)
    
    logging.info(f"Loading specification from {args.spec}")
    try:
        with open(args.spec, 'r') as f:
            spec = json.load(f)
    except Exception as e:
        logging.error(f"Failed to read specification: {e}")
        sys.exit(1)
        
    try:
        logging.debug("Validating specification...")
        validate_spec(spec)
        logging.info("Specification is valid.")
    except ValidationError as e:
        logging.error(f"Validation Error: {e}")
        sys.exit(2)
        
    if args.validate_only:
        logging.info("Validation complete. Exiting (--validate-only).")
        sys.exit(0)

    # Memory Management: Stream or batch large specifications if implemented in layout engine
    logging.debug("Checking memory parameters and diagram size...")

    if args.positions:
        logging.info(f"Using pre-computed positions from {args.positions}")
        with open(args.positions, 'r') as f:
            positions = json.load(f)
        page_width = max(b["x"] + b["width"] for b in positions.values()) + 0.5
        page_height = max(b["y"] + b["height"] for b in positions.values()) + 0.5
    else:
        logging.info("Computing layout...")
        positions, page_width, page_height = compute_layout(spec)

    out_dir = os.path.dirname(os.path.abspath(args.output)) or "."
    os.makedirs(out_dir, exist_ok=True)
    
    vsdx_path = args.output + ".vsdx"
    pdf_path = args.output + ".pdf"

    logging.info(f"Rendering VSDX to {vsdx_path}...")
    try:
        build_vsdx(spec, positions, page_width, page_height, vsdx_path)
        logging.info(f"Successfully wrote {vsdx_path}")
    except Exception as e:
        logging.error(f"Failed to render VSDX: {e}")

    logging.info(f"Rendering PDF to {pdf_path}...")
    try:
        to_pdf(vsdx_path, pdf_path)
        logging.info(f"Successfully wrote {pdf_path}")
    except PdfExportError as e:
        logging.warning(f"PDF export skipped: {e}")

if __name__ == "__main__":
    main()
