from aspose.diagram import Diagram, SaveFileFormat
from typing import Dict, List
from collections import defaultdict
from calculators.risk_calculator import RiskCalculator
from calculators.zone_calculator import ZoneCalculator


class RiskMatrixBuilder:
    """Constructs the 5×5 Risk Matrix Visio diagram."""

    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._calculate_grid()
        self._analyze_risks()

    def _setup_page(self) -> None:
        """Configure A2 landscape bounds."""
        self.page.page_sheet.page_props.page_width = 59.4
        self.page.page_sheet.page_props.page_height = 42.0
        self.page_width = 59.4
        self.page_height = 42.0

    def _setup_styles(self) -> None:
        """Bind global styles from config."""
        styling = self.config.get("styling", {})
        self.cell_size = styling.get("cell_size", 1.5)
        self.font_family = styling.get("font_family", "Arial")
        self.font_size = styling.get("font_size", 9)
        self.shadow_enabled = styling.get("shadow_enabled", True)
        self.risk_zones = self.config['risk_matrix']['risk_zones']

    def _calculate_grid(self) -> None:
        """
        Compute (x, y) origin for all 25 grid cells.

        Coordinate convention:
          - Impact (1→5) increases left-to-right (X axis).
          - Probability (1→5) increases bottom-to-top (Y axis).
            In Visio's coordinate space (Y grows downward), prob=5 maps to the
            smallest Y value (top row) and prob=1 maps to the largest Y value
            (bottom row).
        """
        layout = self.config.get("layout", {})
        margin = layout.get("margin", 0.5)
        header_height = layout.get("header_height", 1.2)

        # Reserve space for axis labels
        axis_label_width = 2.0   # Left column for probability labels
        axis_label_height = 1.2  # Top row for impact labels

        x_origin = margin + axis_label_width
        y_origin = margin + header_height + axis_label_height

        self.cell_positions = {}

        for prob in range(1, 6):
            for impact in range(1, 6):
                # X increases left to right (impact 1→5)
                cell_x = x_origin + (impact - 1) * self.cell_size
                # Y increases downward in Visio — prob 5 is at row 0 (top)
                cell_y = y_origin + (5 - prob) * self.cell_size

                score = prob * impact
                zone = ZoneCalculator.get_zone(prob, impact)
                colors = ZoneCalculator.get_colors(zone)

                self.cell_positions[(prob, impact)] = {
                    'x': cell_x,
                    'y': cell_y,
                    'width': self.cell_size,
                    'height': self.cell_size,
                    'score': score,
                    'zone': zone,
                    'fill_color': colors['fill'],
                    'text_color': colors['text']
                }

        # Grid bounding box reference
        self.grid_x_start = x_origin
        self.grid_y_start = y_origin
        self.grid_total_width = self.cell_size * 5
        self.grid_total_height = self.cell_size * 5

    def _analyze_risks(self) -> None:
        """Run risk enrichment and analysis; group risks by cell for stacking."""
        risks = self.config['risk_matrix']['risks']
        zones = self.config['risk_matrix']['risk_zones']
        calculator = RiskCalculator(risks, zones)
        self.analysis = calculator.analyze()

        # Group risks by (probability, impact) for card stacking
        self.risk_cell_map = defaultdict(list)
        for risk in risks:
            key = (risk['probability'], risk['impact'])
            self.risk_cell_map[key].append(risk)

    def _get_card_positions(self, cell: Dict, risks_in_cell: List[Dict]) -> List[Dict]:
        """
        Compute stacked card positions within a cell.
        Multiple risks in the same cell are stacked vertically.
        """
        card_height = 0.55   # Inches per card
        card_width = self.cell_size - 0.15
        padding = 0.08

        positions = []
        for idx, risk in enumerate(risks_in_cell):
            card_x = cell['x'] + padding
            card_y = cell['y'] + padding + (idx * (card_height + 0.05))
            positions.append({
                'x': card_x,
                'y': card_y,
                'width': card_width,
                'height': card_height,
                'risk': risk
            })
        return positions

    def build(self) -> None:
        """Execute all Aspose.Diagram draw calls in order."""
        # 1. Title block (project name, version, date)
        # 2. Impact axis labels (top, horizontal: Minor → Catastrophic)
        # 3. Probability axis labels (left, vertical with arrow: Rare → Almost Certain)
        # 4. 25 grid cells with zone fill colors and score corner labels
        # 5. Risk item cards overlaid on cells (stacked vertically per cell)
        # 6. Overflow footnote callouts where > MAX_CARDS_PER_CELL
        # 7. Legend block (zone definitions, colors)
        # 8. Risk register table (below the grid, sorted by score descending)
        # 9. Summary statistics block (zone counts, top risks, mitigation coverage)
        pass

    def save(self, output_path: str) -> None:
        """Export to VSDX."""
        self.diagram.save(output_path, SaveFileFormat.VSDX)
