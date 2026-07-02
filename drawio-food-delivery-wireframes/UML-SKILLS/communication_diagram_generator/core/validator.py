"""
core/validator.py
─────────────────
Parses a raw dictionary using the Pydantic models. Raises our custom
CD-00X exceptions if validation fails, keeping the CLI and Builders
clean from dealing with raw Pydantic errors.
"""
from typing import Dict, Any
from pydantic import ValidationError
from core.models import CommunicationDiagramSpec
from core.errors import (
    InvalidInputError,
    NoParticipantsError,
    NoMessagesError,
    InvalidParticipantRefError,
    DuplicateSequenceError,
)

def validate(spec_dict: Dict[str, Any]) -> CommunicationDiagramSpec:
    """
    Validates a raw dictionary against the Communication Diagram schema.
    Raises domain-specific exceptions (CD-001, etc.) on failure.
    """
    try:
        spec = CommunicationDiagramSpec(**spec_dict)
    except ValidationError as e:
        raise InvalidInputError(f"Schema validation failed:\n{e}")

    diagram = spec.communication_diagram

    # CD-002: No Participants
    if not diagram.participants:
        raise NoParticipantsError()

    # CD-003: No Messages
    if not diagram.messages:
        raise NoMessagesError()

    participant_ids = {p.id for p in diagram.participants}

    # Validate Links
    for link in diagram.links:
        if link.source not in participant_ids:
            raise InvalidParticipantRefError(link.source, f"[Link {link.id}]")
        if link.target not in participant_ids:
            raise InvalidParticipantRefError(link.target, f"[Link {link.id}]")

    # Validate Messages (CD-004, CD-005)
    seen_seqs = set()
    for msg in diagram.messages:
        # Check references
        if msg.source not in participant_ids:
            raise InvalidParticipantRefError(msg.source, msg.sequence)
        if msg.target not in participant_ids:
            raise InvalidParticipantRefError(msg.target, msg.sequence)
        
        # Check duplicate sequences (only if they actually provided one)
        if msg.sequence:
            if msg.sequence in seen_seqs:
                raise DuplicateSequenceError(msg.sequence)
            seen_seqs.add(msg.sequence)

    # Note: Circular dependency (CD-007) is mostly a conceptual warning
    # since communication diagrams explicitly model cycles. We skip it
    # here unless there's a strict structural tree requirement.

    return spec
