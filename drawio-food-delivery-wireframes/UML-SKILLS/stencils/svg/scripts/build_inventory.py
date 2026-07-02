#!/usr/bin/env python3
"""Build SHAPE_LIBRARY.json and SHAPE_LIBRARY.md from shape_catalog.py."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shape_catalog import CATEGORIES, library_dict  # noqa: E402


def build_markdown(data: dict) -> str:
    lines = [
        "# UML & Architecture Shape Library",
        "",
        f"**Version:** {data['version']}",
        f"**Total shapes:** {data['summary']['total_shapes']}",
        f"**Categories:** {data['summary']['categories']}",
        "",
        "## Summary by delivery",
        "",
        "| Delivery | Count |",
        "|----------|-------|",
    ]
    for k, v in sorted(data["summary"]["by_delivery"].items()):
        lines.append(f"| `{k}` | {v} |")

    lines += [
        "",
        "## Summary by asset type",
        "",
        "| Asset type | Count |",
        "|------------|-------|",
    ]
    for k, v in sorted(data["summary"]["by_asset_type"].items()):
        lines.append(f"| `{k}` | {v} |")

    lines += [
        "",
        "See [STYLE_GUIDE.md](./STYLE_GUIDE.md) for rendering consistency.",
        "",
        "Regenerate: `python scripts/build_inventory.py`",
        "",
    ]

    for cat in data["categories"]:
        lines.append(f"## {cat['name']} (`{cat['id']}`) — {cat['count']} shapes")
        lines.append("")
        lines.append("| ID | Name | Visual | Purpose | Delivery | Output |")
        lines.append("|----|------|--------|---------|----------|--------|")
        for s in cat["shapes"]:
            out = s.get("output_path") or "—"
            visual = s["visual"].replace("|", "\\|")
            purpose = s["purpose"].replace("|", "\\|")
            lines.append(
                f"| `{s['id']}` | {s['name']} | {visual} | {purpose} | `{s['delivery']}` | `{out}` |"
            )
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    data = library_dict()
    json_path = ROOT / "SHAPE_LIBRARY.json"
    md_path = ROOT / "SHAPE_LIBRARY.md"

    json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    md_path.write_text(build_markdown(data), encoding="utf-8")

    print(f"Wrote {data['summary']['total_shapes']} shapes")
    print(f"  JSON: {json_path}")
    print(f"  MD:   {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
