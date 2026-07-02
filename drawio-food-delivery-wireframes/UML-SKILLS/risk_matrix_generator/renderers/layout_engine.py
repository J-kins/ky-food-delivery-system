from typing import Dict, List, Tuple


class RiskLayoutEngine:
    """
    Handles card stacking and overflow detection.

    When more than MAX_CARDS_PER_CELL risks occupy a single cell, overflow
    cards are referenced via a footnote callout rather than drawn inside the
    cell (RX-012 warning).
    """

    MAX_CARDS_PER_CELL = 3

    @staticmethod
    def pack_cards(cell: Dict, risks: List[Dict], card_height: float = 0.55) -> Tuple[List, List]:
        """
        Pack risk cards into a cell.

        Returns:
            (visible_cards, overflow_cards)
            Overflow occurs when there are more than MAX_CARDS_PER_CELL risks
            in one cell.
        """
        max_n = RiskLayoutEngine.MAX_CARDS_PER_CELL
        visible = risks[:max_n]
        overflow = risks[max_n:]
        return visible, overflow

    @staticmethod
    def compute_card_y(cell_y: float, card_index: int,
                       card_height: float, padding: float = 0.08) -> float:
        """
        Compute the Y coordinate for a stacked card inside a cell.

        Index 0 = top of cell, index 1 = below first card, etc.
        """
        return cell_y + padding + card_index * (card_height + 0.04)
