"""Compute Kanban board metrics from work items and columns."""
from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List


def _done_column_ids(columns: List[dict]) -> set:
    return {c["id"] for c in columns if c["id"].upper() == "DONE" or c["name"].lower() == "done"}


def _blocked_column_ids(columns: List[dict]) -> set:
    return {c["id"] for c in columns if "BLOCK" in c["id"].upper()}


def compute_metrics(config: Dict[str, Any]) -> Dict[str, Any]:
    items = config.get("work_items", [])
    columns = config.get("columns", [])
    done_ids = _done_column_ids(columns)
    blocked_ids = _blocked_column_ids(columns)

    total = len(items)
    completed = sum(1 for i in items if i["status"] in done_ids)
    blocked = sum(1 for i in items if i["status"] in blocked_ids)
    in_progress = total - completed - blocked

    priority_dist = dict(Counter(i.get("priority", "Medium") for i in items))
    type_dist = dict(Counter(i.get("type", "Task") for i in items))
    high_priority = priority_dist.get("High", 0)

    wip_limit_total = sum(c.get("wip_limit") or 0 for c in columns)

    return {
        "total_cards": total,
        "in_progress": in_progress,
        "completed": completed,
        "blocked_items": blocked,
        "high_priority_count": high_priority,
        "wip_limit_total": wip_limit_total,
        "priority_distribution": priority_dist,
        "type_distribution": type_dist,
    }


def format_metrics_text(metrics: Dict[str, Any]) -> str:
    pri = metrics.get("priority_distribution", {})
    types = metrics.get("type_distribution", {})
    pri_line = "  ".join(f"{k} ({v})" for k, v in sorted(pri.items()))
    type_line = "  ".join(f"{k} ({v})" for k, v in sorted(types.items()))
    return (
        f"Total Cards: {metrics['total_cards']}   |   "
        f"In Progress: {metrics['in_progress']}   |   "
        f"Completed: {metrics['completed']}   |   "
        f"Blocked: {metrics['blocked_items']}   |   "
        f"High Priority: {metrics['high_priority_count']}   |   "
        f"WIP Limit Total: {metrics['wip_limit_total']}\n"
        f"Priority Distribution: {pri_line}\n"
        f"Work Item Types: {type_line}"
    )
