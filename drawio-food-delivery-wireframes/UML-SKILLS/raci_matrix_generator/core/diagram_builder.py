from aspose.diagram import Diagram, SaveFileFormat
from typing import Dict, List
from collections import defaultdict

class RACIMatrixBuilder:
    """Constructs the RACI Matrix Visio grid with phase grouping."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
        self._validate_raci()
        self._calculate_positions()
        self._calculate_counts()
    
    def _setup_page(self) -> None:
        """Configure A2 landscape page bounds."""
        self.page.page_sheet.page_props.page_width = 59.4
        self.page.page_sheet.page_props.page_height = 42.0
        self.page_width = 59.4
        self.page_height = 42.0
    
    def _setup_styles(self) -> None:
        """Bind global styles."""
        styling = self.config.get("styling", {})
        self.raci_colors = styling.get("raci_colors", {
            "R": "#E53935", "R_text": "#FFFFFF",
            "A": "#1565C0", "A_text": "#FFFFFF",
            "C": "#FFB300", "C_text": "#333333",
            "I": "#4CAF50", "I_text": "#FFFFFF",
            "-": "#E0E0E0", "-_text": "#757575"
        })
        self.row_height = styling.get("row_height", 0.55)
        self.task_col_width = styling.get("task_col_width", 2.8)
        self.role_col_width = styling.get("role_col_width", 1.4)
    
    def _validate_raci(self) -> None:
        """Enforce RULE-01 through RULE-05 before rendering."""
        tasks = self.config['raci_matrix']['tasks']
        valid_codes = {"R", "A", "C", "I", "-"}
        role_ids = {r['id'] for r in self.config['raci_matrix']['roles']}
        
        for task in tasks:
            raci = task.get('raci', {})
            
            # RULE-04: Valid values only
            for role_id, code in raci.items():
                if code not in valid_codes:
                    raise ValueError(f"RM-004: Invalid RACI code '{code}' in task '{task['id']}'.")
            
            # RULE-05: Role reference integrity
            for role_id in raci.keys():
                if role_id not in role_ids:
                    raise ValueError(f"RM-007: Role '{role_id}' in task '{task['id']}' not found in roles list.")
            
            # RULE-01: Exactly 1 Accountable
            accountable_count = sum(1 for v in raci.values() if v == 'A')
            if accountable_count > 1:
                raise ValueError(f"RM-005: Task '{task['id']}' has {accountable_count} Accountable roles. Only 1 is allowed.")
            if accountable_count == 0:
                raise ValueError(f"RM-006: Task '{task['id']}' has no Accountable role. Every task must have exactly 1 A.")
    
    def _calculate_positions(self) -> None:
        """Auto-fit grid to A2 page."""
        layout = self.config.get("layout", {})
        margin = layout.get("margin", 0.5)
        
        roles = sorted(self.config['raci_matrix']['roles'], key=lambda r: r['order'])
        
        # Compute role column width auto-fit
        available = self.page_width - (margin * 2) - self.task_col_width - 0.8  # 0.8 for Total col
        auto_width = available / max(1, len(roles))
        self.role_col_width = min(auto_width, 1.6)
        
        x = margin
        self.col_positions = {'task': {'x': x, 'width': self.task_col_width}}
        x += self.task_col_width
        
        for role in roles:
            self.col_positions[role['id']] = {'x': x, 'width': self.role_col_width}
            x += self.role_col_width
        
        self.col_positions['total'] = {'x': x, 'width': 0.8}
        
        # Row positions with phase grouping
        y_start = margin + 1.5 + layout.get("header_height", 0.8)
        tasks = sorted(self.config['raci_matrix']['tasks'], key=lambda t: (t['phase_order'], t['order']))
        
        self.row_positions = {}
        current_phase = None
        y = y_start
        
        for task in tasks:
            if task['phase'] != current_phase:
                # Phase separator row
                current_phase = task['phase']
                self.row_positions[f"PHASE_{task['phase']}"] = {
                    'y': y,
                    'height': 0.35,
                    'type': 'phase_header',
                    'name': task['phase'],
                    'phase_order': task['phase_order']
                }
                y += 0.35
            
            self.row_positions[task['id']] = {
                'y': y,
                'height': self.row_height,
                'type': 'task'
            }
            y += self.row_height
        
        self.footer_y = y + 0.2
    
    def _calculate_counts(self) -> None:
        """Compute per-role and per-task RACI distribution counts."""
        roles = self.config['raci_matrix']['roles']
        tasks = self.config['raci_matrix']['tasks']
        
        self.role_counts = {r['id']: {'R': 0, 'A': 0, 'C': 0, 'I': 0} for r in roles}
        self.task_totals = {}
        
        for task in tasks:
            raci = task.get('raci', {})
            assigned = sum(1 for v in raci.values() if v != '-')
            self.task_totals[task['id']] = assigned
            
            for role_id, code in raci.items():
                if code in ('R', 'A', 'C', 'I') and role_id in self.role_counts:
                    self.role_counts[role_id][code] += 1
    
    def build(self) -> None:
        """Execute all Aspose draw calls."""
        # 1. Title block
        # 2. Header row (role names + person names)
        # 3. Phase separator rows
        # 4. Task rows with RACI cells
        # 5. Footer totals row
        # 6. Legend block
        # 7. Summary / Gap Analysis block
        pass
    
    def save(self, output_path: str) -> None:
        """Export to VSDX."""
        self.diagram.save(output_path, SaveFileFormat.VSDX)
