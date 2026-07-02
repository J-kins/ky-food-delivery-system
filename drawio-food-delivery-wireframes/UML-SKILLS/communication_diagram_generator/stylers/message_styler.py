"""
stylers/message_styler.py
─────────────────────────
Resolves the styling properties for a message (colour, line dash, arrow type)
based on the message type (synchronous, asynchronous, creation, return)
and the selected theme.
"""
from typing import Dict, Any
from stylers.color_themes import message_style

def get_message_style(theme: Dict, msg_type: str) -> Dict[str, Any]:
    """
    Returns a dict with resolved styling for a message.
    Format: {"color": str, "dash": bool, "open_arrow": bool}
    """
    # Normalize
    msg_type = msg_type.lower()
    return message_style(theme, msg_type)

def format_message_label(sequence: str, label: str, return_val: str = None, guard: str = None) -> str:
    """
    Constructs the message label text following UML conventions:
      [guard] sequence: label : return_val
    """
    parts = []
    
    if guard:
        parts.append(f"[{guard}]")
        
    if sequence:
        parts.append(f"{sequence}:")
        
    parts.append(label)
    
    # It's less common to put return values in the forward message label in
    # communication diagrams (usually they get a return arrow), but if specified:
    if return_val:
        parts.append(f": {return_val}")
        
    return " ".join(parts).strip()
