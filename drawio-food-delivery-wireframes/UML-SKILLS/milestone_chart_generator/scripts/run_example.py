#!/usr/bin/env python3
"""Run the sample end-to-end and verify Milestone Chart Visio output."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.milestone_builder import build_milestone_chart
from core.validator import validate_milestones
from calculators.timeline_calculator import TimelineCalculator


def main() -> int:
    input_path = ROOT / "examples" / "sample_input.json"
    output_path = ROOT / "examples" / "output" / "milestone_chart.vsdx"

    print("=== Milestone Chart Generator — sample run ===")
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}\n")

    payload = json.loads(input_path.read_text())
    print("1. Validating …")
    spec = validate_milestones(payload)
    print("   ✓ schema OK")

    calc = TimelineCalculator(spec.milestone_chart.model_dump())
    critical = sum(1 for m in spec.milestone_chart.milestones if m.is_critical)
    print(f"\n2. Timeline: {calc.total_days} days | {len(spec.milestone_chart.milestones)} milestones ({critical} critical)")

    print("\n3. Building Visio …")
    build_milestone_chart(payload, str(output_path))

    size = output_path.stat().st_size
    print(f"\n=== Results ===")
    print(f"Visio: {output_path} ({size:,} bytes)")

    if not output_path.is_file() or size < 4000:
        print("\nFAILED: output missing or too small", file=sys.stderr)
        return 1

    print("\nSUCCESS: milestone_chart.vsdx generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
