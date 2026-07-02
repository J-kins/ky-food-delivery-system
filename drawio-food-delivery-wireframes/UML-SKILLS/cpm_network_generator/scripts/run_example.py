#!/usr/bin/env python3
"""Run the sample end-to-end and verify CPM Visio output."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.cpm_builder import build_cpm_network
from core.validator import validate
from calculators.cpm_calculator import CPMCalculator


def main() -> int:
    input_path = ROOT / "examples" / "sample_input.json"
    output_path = ROOT / "examples" / "output" / "cpm_diagram.vsdx"

    print("=== CPM Network Generator — sample run ===")
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}\n")

    payload = json.loads(input_path.read_text())
    print("1. Validating …")
    spec = validate(payload)
    print("   ✓ schema OK")

    print("\n2. CPM calculations …")
    calc = CPMCalculator(spec.cpm_network.model_dump()["activities"])
    critical = [a["id"] for a in calc.activities if a.get("is_critical")]
    duration = max(a.get("ef", 0) for a in calc.activities)
    print(f"   Project duration: {duration} weeks")
    print(f"   Critical path: {' → '.join(critical)}")

    print("\n3. Building Visio …")
    build_cpm_network(payload, str(output_path))

    size = output_path.stat().st_size
    print(f"\n=== Results ===")
    print(f"Visio: {output_path} ({size:,} bytes)")

    if not output_path.is_file() or size < 4000:
        print("\nFAILED: output missing or too small", file=sys.stderr)
        return 1

    print("\nSUCCESS: cpm_diagram.vsdx generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
