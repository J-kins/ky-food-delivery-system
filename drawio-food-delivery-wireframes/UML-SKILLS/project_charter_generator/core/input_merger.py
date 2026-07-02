"""Merge split input files into Word, Visio, or combined MAIN payloads."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from diagrams.description_schema import DIAGRAM_SPLIT_FILES

SPLIT_FILENAMES = {
    "project": "charter_project_input.json",
    "content": "charter_content_input.json",
    "people": "charter_people_input.json",
    "schedule_risk": "charter_schedule_risk_input.json",
    "word_styling": "charter_word_styling_input.json",
    "visio_diagrams": "charter_visio_diagrams_input.json",
}

EMPTY_DIAGRAMS: Dict[str, Dict[str, Any]] = {
    "problem_tree": {},
    "stakeholder_map": {},
    "system_context": {},
    "org_chart": {},
    "scope_boundary": {},
    "milestone_timeline": {},
}


def _load_json(path: Path) -> Dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _merge_shared(
    project: Dict[str, Any],
    content: Dict[str, Any],
    people: Dict[str, Any],
    schedule_risk: Dict[str, Any],
) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for part in (project, content, people, schedule_risk):
        merged.update(part)
    return merged


def load_diagram_descriptions(inputs_dir: Path) -> Dict[str, Any]:
    """Load per-diagram description JSON files into diagram_descriptions map."""
    descriptions: Dict[str, Any] = {}
    for diagram_id, filename in DIAGRAM_SPLIT_FILES.items():
        path = inputs_dir / filename
        if not path.exists():
            continue
        data = _load_json(path)
        desc = data.get("diagram_description", data)
        descriptions[diagram_id] = desc
    return descriptions


def _attach_word_extras(
    payload: Dict[str, Any],
    word_styling: Optional[Dict[str, Any]] = None,
    diagram_descriptions: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if word_styling and "word_document" in word_styling:
        payload["word_document"] = word_styling["word_document"]
    if diagram_descriptions:
        payload["diagram_descriptions"] = diagram_descriptions
    return payload


def merge_word_input(
    project: Dict[str, Any],
    content: Dict[str, Any],
    people: Dict[str, Any],
    schedule_risk: Dict[str, Any],
    word_styling: Optional[Dict[str, Any]] = None,
    diagram_descriptions: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = _merge_shared(project, content, people, schedule_risk)
    payload["diagrams"] = dict(EMPTY_DIAGRAMS)
    return _attach_word_extras(payload, word_styling, diagram_descriptions)


def merge_visio_input(
    project: Dict[str, Any],
    content: Dict[str, Any],
    people: Dict[str, Any],
    schedule_risk: Dict[str, Any],
    visio_diagrams: Optional[Dict[str, Any]] = None,
    diagram_descriptions: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = _merge_shared(project, content, people, schedule_risk)
    payload["diagrams"] = dict(EMPTY_DIAGRAMS)
    if visio_diagrams:
        payload["diagrams"].update(visio_diagrams.get("diagrams", {}))
        if "visio_deck" in visio_diagrams:
            payload["visio_deck"] = visio_diagrams["visio_deck"]
    if diagram_descriptions:
        payload["diagram_descriptions"] = diagram_descriptions
    return payload


def merge_combined_input(
    project: Dict[str, Any],
    content: Dict[str, Any],
    people: Dict[str, Any],
    schedule_risk: Dict[str, Any],
    word_styling: Optional[Dict[str, Any]] = None,
    visio_diagrams: Optional[Dict[str, Any]] = None,
    diagram_descriptions: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = merge_visio_input(
        project, content, people, schedule_risk, visio_diagrams, diagram_descriptions
    )
    if word_styling and "word_document" in word_styling:
        payload["word_document"] = word_styling["word_document"]
    return payload


def load_splits_from_directory(inputs_dir: Path) -> Dict[str, Any]:
    parts: Dict[str, Any] = {}
    for key, filename in SPLIT_FILENAMES.items():
        path = inputs_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing split file: {path}")
        parts[key] = _load_json(path)

    missing = [
        fn for fn in DIAGRAM_SPLIT_FILES.values() if not (inputs_dir / fn).exists()
    ]
    if missing:
        raise FileNotFoundError(
            f"Missing diagram description file(s): {', '.join(missing)}"
        )

    parts["diagram_descriptions"] = load_diagram_descriptions(inputs_dir)
    return parts


def merge_all_from_directory(inputs_dir: Path) -> Dict[str, Dict[str, Any]]:
    parts = load_splits_from_directory(inputs_dir)
    shared = (parts["project"], parts["content"], parts["people"], parts["schedule_risk"])
    desc = parts.get("diagram_descriptions", {})
    return {
        "charter_word_input.json": merge_word_input(
            *shared, word_styling=parts.get("word_styling"), diagram_descriptions=desc
        ),
        "charter_visio_input.json": merge_visio_input(
            *shared, visio_diagrams=parts.get("visio_diagrams"), diagram_descriptions=desc
        ),
        "charter_input.json": merge_combined_input(
            *shared,
            word_styling=parts.get("word_styling"),
            visio_diagrams=parts.get("visio_diagrams"),
            diagram_descriptions=desc,
        ),
    }


def write_merged_outputs(inputs_dir: Path) -> Dict[str, Path]:
    merged = merge_all_from_directory(inputs_dir)
    written: Dict[str, Path] = {}
    for filename, payload in merged.items():
        out = inputs_dir / filename
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
            f.write("\n")
        written[filename] = out
    return written
