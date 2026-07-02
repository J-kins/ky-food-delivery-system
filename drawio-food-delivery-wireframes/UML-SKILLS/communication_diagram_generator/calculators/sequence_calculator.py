class SequenceNumberGenerator:
    """
    Generates and manages hierarchical message sequence numbers for
    Communication Diagrams (e.g. 1, 1.1, 1.1.1, 2, 2.1 …).

    Sequence format follows UML Communication Diagram conventions:
      - Top-level messages:  1, 2, 3 …
      - Nested sub-messages: 1.1, 1.2, 1.1.1 …
    """

    def __init__(self):
        self.sequence_stack: list = []
        self.message_counters: dict = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def next_top_level(self) -> str:
        """Advance and return the next top-level sequence number."""
        if not self.sequence_stack:
            self.sequence_stack = [1]
        else:
            # Pop back to the top level and increment
            self.sequence_stack = [self.sequence_stack[0] + 1]
        self.message_counters[self._current()] = 0
        return self._current()

    def add_nested_message(self, parent_sequence: str) -> str:
        """
        Add a nested sub-message under *parent_sequence*.

        Example:
            parent_sequence = "1.1"  →  returns "1.1.1"
        """
        parts = [int(p) for p in parent_sequence.split(".")]
        # Increment the last counter at this depth, or start a new sub-level
        key = parent_sequence
        sub_count = self.message_counters.get(key, 0) + 1
        self.message_counters[key] = sub_count
        nested = parts + [sub_count]
        return ".".join(map(str, nested))

    def reset(self) -> None:
        """Reset the generator for a fresh diagram."""
        self.sequence_stack = []
        self.message_counters = {}

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _current(self) -> str:
        return ".".join(map(str, self.sequence_stack))

    @staticmethod
    def parse_for_sort(sequence: str) -> tuple:
        """
        Convert a dotted sequence string to a sortable tuple of ints.

        Example:  "1.2.3"  →  (1, 2, 3)
        """
        if not sequence:
            return (0,)
        try:
            return tuple(int(p) for p in sequence.split("."))
        except ValueError:
            return (0,)
