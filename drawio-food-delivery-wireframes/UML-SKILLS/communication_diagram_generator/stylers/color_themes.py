"""
stylers/color_themes.py
───────────────────────
Defines colour palettes for participant types and message types across
all supported themes. Returns dicts that override per-participant colours
when the JSON spec doesn't supply an explicit colour.
"""
from typing import Dict, Any

# ── Theme definitions ─────────────────────────────────────────────────────────

THEMES: Dict[str, Dict[str, Any]] = {
    "enterprise_blue": {
        "participant_types": {
            "actor":    {"fill": "#4CAF50", "text": "#FFFFFF"},
            "control":  {"fill": "#1565C0", "text": "#FFFFFF"},
            "entity":   {"fill": "#2E7D32", "text": "#FFFFFF"},
            "boundary": {"fill": "#FF9800", "text": "#FFFFFF"},
            "service":  {"fill": "#6A1B9A", "text": "#FFFFFF"},
            "database": {"fill": "#37474F", "text": "#FFFFFF"},
            "system":   {"fill": "#1a237e", "text": "#FFFFFF"},
        },
        "message_types": {
            "synchronous":  {"color": "#1a237e", "dash": False, "open_arrow": False},
            "asynchronous": {"color": "#6A1B9A", "dash": True,  "open_arrow": False},
            "creation":     {"color": "#E65100", "dash": True,  "open_arrow": False},
            "return":       {"color": "#2E7D32", "dash": True,  "open_arrow": True},
        },
        "title_bg":   "#1a237e",
        "title_text": "#FFFFFF",
        "group_bg":   "#E3F2FD",
        "group_border": "#1565C0",
        "link_color": "#666666",
        "legend_bg":  "#F5F5F5",
        "legend_border": "#BDBDBD",
    },
    "corporate_grey": {
        "participant_types": {
            "actor":    {"fill": "#546E7A", "text": "#FFFFFF"},
            "control":  {"fill": "#37474F", "text": "#FFFFFF"},
            "entity":   {"fill": "#455A64", "text": "#FFFFFF"},
            "boundary": {"fill": "#607D8B", "text": "#FFFFFF"},
            "service":  {"fill": "#78909C", "text": "#FFFFFF"},
            "database": {"fill": "#263238", "text": "#FFFFFF"},
            "system":   {"fill": "#212121", "text": "#FFFFFF"},
        },
        "message_types": {
            "synchronous":  {"color": "#263238", "dash": False, "open_arrow": False},
            "asynchronous": {"color": "#546E7A", "dash": True,  "open_arrow": False},
            "creation":     {"color": "#BF360C", "dash": True,  "open_arrow": False},
            "return":       {"color": "#33691E", "dash": True,  "open_arrow": True},
        },
        "title_bg":   "#37474F",
        "title_text": "#FFFFFF",
        "group_bg":   "#ECEFF1",
        "group_border": "#546E7A",
        "link_color": "#9E9E9E",
        "legend_bg":  "#F5F5F5",
        "legend_border": "#BDBDBD",
    },
    "minimal": {
        "participant_types": {
            "actor":    {"fill": "#FFFFFF", "text": "#333333"},
            "control":  {"fill": "#FFFFFF", "text": "#333333"},
            "entity":   {"fill": "#FFFFFF", "text": "#333333"},
            "boundary": {"fill": "#FFFFFF", "text": "#333333"},
            "service":  {"fill": "#FFFFFF", "text": "#333333"},
            "database": {"fill": "#FFFFFF", "text": "#333333"},
            "system":   {"fill": "#FFFFFF", "text": "#333333"},
        },
        "message_types": {
            "synchronous":  {"color": "#333333", "dash": False, "open_arrow": False},
            "asynchronous": {"color": "#333333", "dash": True,  "open_arrow": False},
            "creation":     {"color": "#333333", "dash": True,  "open_arrow": False},
            "return":       {"color": "#333333", "dash": True,  "open_arrow": True},
        },
        "title_bg":   "#333333",
        "title_text": "#FFFFFF",
        "group_bg":   "#FAFAFA",
        "group_border": "#333333",
        "link_color": "#AAAAAA",
        "legend_bg":  "#FAFAFA",
        "legend_border": "#CCCCCC",
    },
}


def get_theme(name: str) -> Dict[str, Any]:
    """Return the theme dict, falling back to enterprise_blue if unknown."""
    return THEMES.get(name, THEMES["enterprise_blue"])


def participant_fill(theme: Dict, p_type: str, override: str = "") -> str:
    """Return fill colour for a participant type, honouring per-node override."""
    if override:
        return override
    return theme["participant_types"].get(p_type, {"fill": "#1565C0"})["fill"]


def participant_text_color(theme: Dict, p_type: str, override: str = "") -> str:
    if override:
        return override
    return theme["participant_types"].get(p_type, {"text": "#FFFFFF"})["text"]


def message_style(theme: Dict, msg_type: str) -> Dict[str, Any]:
    """Return line-style dict for a message type."""
    return theme["message_types"].get(msg_type, theme["message_types"]["synchronous"])
