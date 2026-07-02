"""Build Graphviz DOT or D2 source from diagram description JSON."""
from __future__ import annotations

import textwrap
from typing import List

from diagrams.description_schema import DiagramDescription


def _escape_dot(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def description_to_dot(desc: DiagramDescription) -> str:
    if desc.source and desc.format == "graphviz":
        return desc.source.strip()

    lines: List[str] = [
        f'digraph "{desc.id}" {{',
        "  graph [bgcolor=white fontname=Arial];",
        f'  rankdir={desc.rankdir};',
        '  node [shape=box style="rounded,filled" fontname=Arial fontsize=10 margin="0.2,0.1"];',
        '  edge [color="#666666" fontname=Arial fontsize=9];',
    ]

    clusters: dict = {}
    for node in desc.nodes:
        if node.group:
            clusters.setdefault(node.group, []).append(node)

    rendered: set = set()
    for group, nodes in clusters.items():
        lines.append(f'  subgraph "cluster_{group}" {{')
        lines.append(f'    label="{_escape_dot(group)}";')
        for node in nodes:
            lines.append(_node_line(node))
            rendered.add(node.id)
        lines.append("  }")

    for node in desc.nodes:
        if node.id not in rendered:
            lines.append(_node_line(node))

    for edge in desc.edges:
        label = f' label="{_escape_dot(edge.label)}"' if edge.label else ""
        color = f' color="{edge.color}"'
        lines.append(f'  "{edge.from_id}" -> "{edge.to_id}"[{label}{color}];')

    lines.append("}")
    return "\n".join(lines)


def _node_line(node) -> str:
    shape = node.shape or "box"
    return (
        f'  "{node.id}" [label="{_escape_dot(node.label)}" shape={shape} '
        f'fillcolor="{node.fill}" color="{node.border}" fontcolor="{node.text_color}"];'
    )


def description_to_d2(desc: DiagramDescription) -> str:
    if desc.source and desc.format == "d2":
        return desc.source.strip()

    direction = "down" if desc.rankdir in ("TB", "BT") else "right"
    lines = [f"direction: {direction}", f'title: "{desc.title}" {{ style.font-size: 18 }}', ""]

    for node in desc.nodes:
        style = f'style.fill: "{node.fill}"; style.stroke: "{node.border}"'
        lines.append(f'{node.id}: "{node.label.replace(chr(10), " ")}" {{ {style} }}')

    lines.append("")
    for edge in desc.edges:
        arrow = "->" if edge.style != "dashed" else "-->"
        label = f': "{edge.label}"' if edge.label else ""
        lines.append(f"{edge.from_id} {arrow} {edge.to_id}{label}")

    return "\n".join(lines)
