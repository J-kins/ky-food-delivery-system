"""Compile diagram descriptions to SVG XML for Word document embedding."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

from diagrams.auto_descriptions import build_descriptions_from_payload
from diagrams.description_schema import (
    REQUIRED_WORD_DIAGRAMS,
    DiagramDescription,
    parse_description_file,
)
from diagrams.source_builder import description_to_dot
from diagrams.xml_pipeline import (
    compile_description_to_svg,
    description_to_svg_xml,
    layout_to_svg_xml,
)
from word.png_renderer import layout_to_png

log = logging.getLogger(__name__)

LAYOUT_FALLBACK = {}  # populated lazily to avoid circular imports


def _layout_fallback_fn(diagram_id: str):
    from diagrams import layouts
    return {
        "problem_tree": layouts.layout_problem_tree,
        "stakeholder_matrix": layouts.layout_stakeholder_matrix,
        "scope_boundary": layouts.layout_scope_boundary,
        "org_chart": layouts.layout_org_chart,
        "milestone_timeline": layouts.layout_milestone_timeline,
        "risk_matrix": layouts.layout_risk_matrix,
        "system_context": layouts.layout_system_context,
    }.get(diagram_id)


def _get_descriptions(payload: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    if payload.get("diagram_descriptions"):
        return payload["diagram_descriptions"]
    log.info("No diagram_descriptions in payload — auto-generating from narrative data.")
    return build_descriptions_from_payload(payload)


def _attach_layout(
    artifact: Dict[str, str],
    layout: dict,
) -> Dict[str, str]:
    """Store layout dict for native Word DrawingML shape embedding."""
    artifact["layout"] = layout
    return artifact


def _attach_png(
    artifact: Dict[str, str],
    layout: dict,
    png_dir: Path,
    diagram_id: str,
) -> Dict[str, str]:
    """Generate PNG from layout for Word embedding (Word cannot display SVG reliably)."""
    png_path = png_dir / f"{diagram_id}.png"
    layout_to_png(layout, png_path)
    artifact["png"] = str(png_path)
    return artifact


def _compile_one(
    desc: DiagramDescription,
    source_dir: Path,
    svg_dir: Path,
    payload: Dict[str, Any],
) -> Dict[str, str]:
    diagram_id = desc.id
    source_path = source_dir / f"{diagram_id}.dot"
    svg_path = svg_dir / f"{diagram_id}.svg"
    png_dir = svg_dir.parent / "png"
    png_dir.mkdir(parents=True, exist_ok=True)
    layout_fn = _layout_fallback_fn(diagram_id)

    # Always persist DOT source for traceability
    if desc.format == "graphviz":
        source_path.write_text(description_to_dot(desc), encoding="utf-8")

    # 1) Prefer Graphviz / D2 CLI when available
    try:
        artifact = compile_description_to_svg(desc, source_dir, svg_dir)
        if layout_fn:
            layout = layout_fn(payload)
            artifact = _attach_layout(artifact, layout)
            artifact = _attach_png(artifact, layout, png_dir, diagram_id)
        return artifact
    except Exception as exc:
        log.warning("%s: external compiler unavailable (%s) — using built-in SVG XML", diagram_id, exc)

    # 2) Pure-Python SVG from description nodes/edges
    if desc.nodes:
        svg_xml = description_to_svg_xml(desc, svg_path)
        artifact = {
            "id": diagram_id,
            "title": desc.title,
            "format": "svg_xml",
            "source": str(source_path) if source_path.exists() else "",
            "svg": str(svg_path),
            "svg_xml": svg_xml,
            "caption": desc.caption or desc.title,
        }
        if layout_fn:
            layout = layout_fn(payload)
            artifact = _attach_layout(artifact, layout)
            artifact = _attach_png(artifact, layout, png_dir, diagram_id)
        else:
            # Build minimal layout from description for PNG
            layout = {
                "title": desc.title,
                "nodes": [
                    {
                        "id": n.id,
                        "text": n.label,
                        "x": 3 + (i % 4) * 5.5,
                        "y": 3 + (i // 4) * 2.5,
                        "w": 4.5,
                        "h": 1.2,
                        "fill": n.fill or "#FFFFFF",
                        "border": n.border or "#666666",
                        "text_color": n.text_color or "#000000",
                    }
                    for i, n in enumerate(desc.nodes)
                ],
                "edges": [{"from": e.from_id, "to": e.to_id, "color": e.color or "#666666"} for e in desc.edges],
            }
            artifact = _attach_layout(artifact, layout)
            artifact = _attach_png(artifact, layout, png_dir, diagram_id)
        return artifact

    # 3) Layout-engine fallback
    if layout_fn:
        layout = layout_fn(payload)
        svg_xml = layout_to_svg_xml(layout, svg_path)
        artifact = {
            "id": diagram_id,
            "title": desc.title,
            "format": "svg_xml",
            "source": str(source_path) if source_path.exists() else "",
            "svg": str(svg_path),
            "svg_xml": svg_xml,
            "caption": desc.caption or desc.title,
        }
        artifact = _attach_layout(artifact, layout)
        return _attach_png(artifact, layout, png_dir, diagram_id)

    raise RuntimeError(f"Cannot compile diagram: {diagram_id}")


def compile_word_diagrams(payload: Dict[str, Any], output_dir: str) -> Dict[str, Dict[str, str]]:
    """Compile all required diagram descriptions to SVG XML for Word embedding."""
    descriptions = _get_descriptions(payload)
    source_dir = Path(output_dir) / "diagrams" / "source"
    svg_dir = Path(output_dir) / "diagrams" / "svg"
    source_dir.mkdir(parents=True, exist_ok=True)
    svg_dir.mkdir(parents=True, exist_ok=True)

    compiled: Dict[str, Dict[str, str]] = {}
    for diagram_id in REQUIRED_WORD_DIAGRAMS:
        raw = descriptions.get(diagram_id)
        if not raw:
            raise RuntimeError(f"Missing required diagram description: {diagram_id}")

        desc = DiagramDescription.model_validate(raw)
        artifact = _compile_one(desc, source_dir, svg_dir, payload)
        compiled[diagram_id] = artifact
        log.info("Compiled %s → %s", diagram_id, artifact["svg"])

    if len(compiled) < len(REQUIRED_WORD_DIAGRAMS):
        missing = set(REQUIRED_WORD_DIAGRAMS) - set(compiled)
        raise RuntimeError(f"Failed to compile diagrams: {missing}")

    return compiled


def load_description_split_file(path: Path) -> Dict[str, Any]:
    import json
    data = json.loads(path.read_text(encoding="utf-8"))
    desc = parse_description_file(data)
    return desc.model_dump(by_alias=True)
