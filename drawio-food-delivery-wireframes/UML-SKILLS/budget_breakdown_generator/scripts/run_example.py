#!/usr/bin/env python3
"""Run the Da'atSNA sample end-to-end and verify Excel + Visio outputs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.budget_builder import build_budget
from core.input_merger import write_merged_outputs
from core.validator import validate


def main() -> int:
    split_dir = ROOT / "examples" / "split"
    output_dir = ROOT / "examples" / "output"

    print("=== Budget Breakdown Generator — sample run ===")
    print(f"Split inputs: {split_dir}")
    print(f"Output:       {output_dir}\n")

    print("1. Merging split JSON files …")
    written = write_merged_outputs(split_dir)
    for name, path in written.items():
        validate(json.loads(path.read_text()))
        print(f"   ✓ {name}")

    print("\n2. Building Excel + Visio …")
    payload = json.loads((split_dir / "budget_input.json").read_text())
    outputs = build_budget(payload, str(output_dir))

    excel = Path(outputs["excel"])
    visio = Path(outputs["visio"])

    print("\n=== Results ===")
    print(f"Excel: {excel} ({excel.stat().st_size:,} bytes)")
    print(f"Visio: {visio} ({visio.stat().st_size:,} bytes)")

    if not excel.is_file() or not visio.is_file():
        print("\nFAILED: missing output file(s)", file=sys.stderr)
        return 1

    print("\nSUCCESS: both budget_breakdown.xlsx and budget_dashboard.vsdx generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
