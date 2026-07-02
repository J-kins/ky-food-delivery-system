#!/usr/bin/env python3
"""Run the Da'atSNA sample end-to-end and verify Word + Visio outputs open cleanly."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.charter_builder import build_charter
from core.input_merger import write_merged_outputs
from core.validator import validate_payload
from core.verify_outputs import verify_all_outputs
import json


def main() -> int:
    split_dir = ROOT / "examples" / "split"
    output_dir = ROOT / "examples" / "output"

    print("=== Project Charter Generator — sample run ===")
    print(f"Split inputs: {split_dir}")
    print(f"Output:       {output_dir}\n")

    print("1. Merging split JSON files …")
    written = write_merged_outputs(split_dir)
    for name, path in written.items():
        validate_payload(json.loads(path.read_text()))
        print(f"   ✓ {name}")

    print("\n2. Building Word + Visio deck + Charter Summary …")
    payload = json.loads((split_dir / "charter_input.json").read_text())
    outputs = build_charter(payload, str(output_dir))

    word = Path(outputs["word"])
    visio = Path(outputs["visio"])
    summary = Path(outputs["charter_summary"])
    svg_dir = Path(outputs["diagrams_svg_dir"])
    svgs = sorted(svg_dir.glob("*.svg"))

    print("\n3. Verifying outputs open without errors …")
    verify_all_outputs(outputs)
    print("   ✓ Word document readable")
    print("   ✓ Visio deck readable (Aspose reload)")
    print("   ✓ Charter summary readable (Aspose reload)")
    print(f"   ✓ {len(svgs)} SVG diagram(s) valid")

    print("\n=== Results ===")
    print(f"Word:           {word} ({word.stat().st_size:,} bytes)")
    print(f"Visio deck:     {visio} ({visio.stat().st_size:,} bytes)")
    print(f"Charter summary:{summary} ({summary.stat().st_size:,} bytes)")
    print(f"SVG diagrams:   {len(svgs)} files in {svg_dir}")
    for s in svgs:
        print(f"   • {s.name} ({s.stat().st_size:,} bytes)")

    if not word.is_file() or not visio.is_file() or not summary.is_file():
        print("\nFAILED: missing output file(s)", file=sys.stderr)
        return 1

    print("\nSUCCESS: project-charter.docx, project-charter.vsdx, and charter-summary.vsdx generated and verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
