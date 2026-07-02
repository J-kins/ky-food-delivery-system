"""
stylers/participant_styler.py
─────────────────────────────
Handles text layout and label formatting for participant boxes.
UML Communication Diagrams standardise a 3-line format:
  <<stereotype>>
  ClassName:instanceName
  (Participant Name)
"""

def build_participant_label(participant: dict) -> str:
    """
    Constructs the standard 3-line participant label.

    Example:
        <<control>>
        AppointmentSystem:scheduler
        (Appointment System)
    """
    stereotype = participant.get("stereotype", f"<<{participant.get('type', 'participant')}>>")
    cls_name   = participant.get("class_name", "")
    inst_name  = participant.get("instance_name", "")
    part_name  = participant.get("name", "")

    # Line 1: Stereotype
    lines = [stereotype]

    # Line 2: Class:instance
    if cls_name and inst_name:
        lines.append(f"{cls_name}:{inst_name}")
    elif cls_name:
        lines.append(f"{cls_name}")
    elif inst_name:
        lines.append(f":{inst_name}")

    # Line 3: Name
    if part_name:
        lines.append(f"({part_name})")

    return "\n".join(lines)
