from __future__ import annotations

from typing import Any, Dict, List, Set

from pydantic import ValidationError

from core.errors import (
    EmptyProjectNameError,
    InvalidInputError,
    InvalidLevelIdError,
    MissingDescriptionError,
    NoProjectRootError,
    TooManyLevelsError,
)
from core.models import WBSSpec


def _check_node(node: Dict[str, Any], depth: int, parent_id: str, seen_ids: Set[str]) -> None:
    node_id = node["id"]
    if depth > 3:
        raise TooManyLevelsError(node_id, depth)
    if node_id in seen_ids:
        raise InvalidLevelIdError(node_id, "duplicate")
    seen_ids.add(node_id)

    if parent_id and parent_id != "0":
        if not node_id.startswith(parent_id + "."):
            raise InvalidLevelIdError(node_id, parent_id)
    elif depth == 1 and "." in node_id:
        raise InvalidLevelIdError(node_id, "root")

    if not str(node.get("description", "")).strip():
        raise MissingDescriptionError(node_id)

    if depth == 3:
        if node.get("effort_hours") is None or int(node["effort_hours"]) <= 0:
            raise InvalidInputError(f"Level 3 node '{node_id}' requires positive effort_hours")
        return

    for child in node.get("children", []):
        _check_node(child, depth + 1, node_id, seen_ids)


def validate_wbs(spec_dict: Dict[str, Any]) -> WBSSpec:
    try:
        spec = WBSSpec(**spec_dict)
    except ValidationError as exc:
        raise InvalidInputError(f"Schema validation failed:\n{exc}") from exc

    wbs = spec.wbs
    if wbs.levels.level_0 is None:
        raise NoProjectRootError()
    if not wbs.levels.level_0.name.strip() and not wbs.project_name.strip():
        raise EmptyProjectNameError()
    if not wbs.branches:
        raise InvalidInputError("At least one Level 1 branch is required")

    seen: Set[str] = {"0"}
    for branch in wbs.branches:
        _check_node(branch.model_dump(), 1, "0", seen)

    return spec


def index_nodes(wbs_dict: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Build id → node lookup from the WBS tree."""
    index: Dict[str, Dict[str, Any]] = {}

    def walk(node: Dict[str, Any]) -> None:
        index[node["id"]] = node
        for child in node.get("children", []):
            walk(child)

    for branch in wbs_dict.get("branches", []):
        walk(branch)
    l0 = wbs_dict.get("levels", {}).get("level_0", {})
    if l0:
        index["0"] = l0
    return index
