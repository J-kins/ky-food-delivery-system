#!/usr/bin/env python3
"""Run the sample end-to-end and verify Communication Diagram Visio output."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.comm_builder import build_communication_diagram
from core.validator import validate


def main() -> int:
    input_path = ROOT / "examples" / "sample_input.json"
    output_path = ROOT / "examples" / "output" / "communication_diagram.vsdx"

    print("=== Communication Diagram Generator — sample run ===")
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}\n")

    payload = json.loads(input_path.read_text())
    print("1. Validating …")
    validate(payload)
    print("   ✓ schema OK")

    print("\n2. Building Visio …")
    build_communication_diagram(payload, str(output_path))

    size = output_path.stat().st_size
    print(f"\n=== Results ===")
    print(f"Visio: {output_path} ({size:,} bytes)")

    if not output_path.is_file() or size < 4000:
        print("\nFAILED: output missing or too small", file=sys.stderr)
        return 1

    print("\nSUCCESS: communication_diagram.vsdx generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
