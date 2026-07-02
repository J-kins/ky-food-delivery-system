from aspose.diagram import Diagram, SaveFileFormat
from typing import Dict, List
from collections import defaultdict

class ResourceAllocationBuilder:
    """Constructs the Resource Allocation Matrix Visio grid."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._calculate_positions()
        self._calculate_totals()
    
    def _setup_page(self) -> None:
        """Configure A2 landscape bounds."""
        self.page.page_sheet.page_props.page_width = 59.4
        self.page.page_sheet.page_props.page_height = 42.0
        self.page_width = 59.4
        self.page_height = 42.0
    
    def _setup_styles(self) -> None:
        """Bind global styles from config."""
        styling = self.config.get("styling", {})
        self.raci_colors = styling.get("raci_colors", {
            "R": "#E53935", "A": "#1565C0",
            "C": "#FFB300", "I": "#4CAF50", "-": "#E0E0E0"
        })
        self.load_colors = styling.get("load_colors", {
            "over": "#E53935", "full": "#FFB300",
            "partial": "#64B5F6", "under": "#4CAF50"
        })
        self.row_height = styling.get("row_height", 0.6)
        self.col_width = styling.get("column_width", 2.0)
        self.cell_padding = styling.get("cell_padding", 0.1)
    
    def _calculate_positions(self) -> None:
        """Auto-fit column widths to page boundaries."""
        layout = self.config.get("layout", {})
        margin = layout.get("margin", 0.5)
        header_height = layout.get("header_height", 0.8)
        
        resources = self.config['resource_allocation']['resources']
        phases = sorted(
            self.config['resource_allocation']['phases'],
            key=lambda p: p['order']
        )
        
        # Reserve width for the resource label column and extra columns
        resource_col_width = 2.5
        extra_cols_width = 2.5  # Total % + Status + Load bar
        
        # Available width for phase columns
        available = self.page_width - (margin * 2) - resource_col_width - extra_cols_width
        phase_col_width = available / max(1, len(phases))
        
        self.col_width = min(phase_col_width, 2.5)  # Cap at 2.5 in
        
        # Column X positions
        x = margin
        self.column_positions = {'resource': {'x': x, 'width': resource_col_width}}
        x += resource_col_width
        
        for phase in phases:
            self.column_positions[phase['id']] = {
                'x': x,
                'width': self.col_width,
                'name': phase['name'],
                'color': phase.get('color', '#1a237e')
            }
            x += self.col_width
        
        # Trailing summary columns
        self.column_positions['total_pct'] = {'x': x, 'width': 0.8}
        x += 0.8
        self.column_positions['status'] = {'x': x, 'width': 0.8}
        x += 0.8
        self.column_positions['load_bar'] = {'x': x, 'width': 1.5}
        
        # Row Y positions (below header)
        y_start = margin + 1.5 + header_height  # Title + header
        self.row_positions = {}
        
        for idx, resource in enumerate(resources):
            self.row_positions[resource['id']] = {
                'y': y_start + (idx * self.row_height),
                'height': self.row_height
            }
        
        self.footer_y = y_start + (len(resources) * self.row_height) + 0.2
        
    def _calculate_totals(self) -> None:
        """Compute per-resource and per-phase load totals."""
        allocations = self.config['resource_allocation']['allocations']
        phases = self.config['resource_allocation']['phases']
        resources = self.config['resource_allocation']['resources']
        
        self.phase_totals = {p['id']: {'count': 0, 'R': 0, 'A': 0, 'C': 0, 'I': 0} for p in phases}
        self.resource_totals = {r['id']: 0 for r in resources}
        
        # Build a lookup dictionary for fast rendering
        self.allocation_map = defaultdict(dict)
        
        for alloc in allocations:
            r_id = alloc['resource_id']
            p_id = alloc['phase_id']
            value = alloc.get('value', '-')
            pct = alloc.get('percentage', 0)
            
            # Map (resource, phase) -> allocation for fast cell lookup
            self.allocation_map[r_id][p_id] = alloc
            
            # Phase totals
            self.phase_totals[p_id]['count'] += 1
            if value in ('R', 'A', 'C', 'I'):
                self.phase_totals[p_id][value] += 1
            
            # Resource % accumulator (max per phase, not sum)
            self.resource_totals[r_id] = max(
                self.resource_totals[r_id], pct
            )
    
    def _get_load_category(self, pct: float) -> str:
        """Map utilization percentage to load label."""
        if pct > 100:
            return "over"
        elif pct >= 80:
            return "full"
        elif pct >= 40:
            return "partial"
        else:
            return "under"
    
    def build(self) -> None:
        """Execute all Visio draw calls."""
        # 1. Title Block
        # 2. Header Row (Phase Names)
        # 3. Resource Rows (RACI cells + Load bars)
        # 4. Totals Row (Phase summary counts)
        # 5. RACI Legend
        # 6. Statistics Summary Block
        pass
    
    def save(self, output_path: str) -> None:
        """Export to VSDX."""
        self.diagram.save(output_path, SaveFileFormat.VSDX)
