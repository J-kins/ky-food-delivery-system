#!/usr/bin/env python3
"""Run the Da'atSNA sample end-to-end and verify Kanban Visio output."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.kanban_builder import build_kanban
from core.validator import validate_kanban
import json


def main() -> int:
    input_path = ROOT / "examples" / "sample_input.json"
    output_path = ROOT / "examples" / "output" / "kanban_chart.vsdx"

    print("=== Kanban Chart Generator — sample run ===")
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}\n")

    payload = json.loads(input_path.read_text())
    print("1. Validating …")
    validate_kanban(payload)
    print("   ✓ schema OK")

    print("\n2. Building Visio …")
    build_kanban(payload, str(output_path))

    size = output_path.stat().st_size
    print(f"\n=== Results ===")
    print(f"Visio: {output_path} ({size:,} bytes)")

    if not output_path.is_file() or size < 4000:
        print("\nFAILED: output missing or too small", file=sys.stderr)
        return 1

    print("\nSUCCESS: kanban_chart.vsdx generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
