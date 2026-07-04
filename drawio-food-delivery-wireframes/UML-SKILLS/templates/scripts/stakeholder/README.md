# Stakeholder Analysis Module

Comprehensive module for converting stakeholder analysis diagrams from data-driven SVG templates to Visio format.

## Overview

This module provides six specialized converters for different stakeholder analysis methodologies:

1. **Stakeholder Map** - Visual positioning of stakeholders and their relationships
2. **Power-Interest Matrix** - Classification by power and interest level (Mendelow Matrix)
3. **Influence Network** - Network topology showing influence and dependencies
4. **Salience Model** - Analysis by power, legitimacy, and urgency (Mitchell Model)
5. **RACI Matrix** - Responsibility assignment (Responsible, Accountable, Consulted, Informed)
6. **Stakeholder Register** - Comprehensive inventory with contact and engagement details

## Data-Driven Architecture

Each template contains embedded JSON defining:
- **Stakeholder Data** - Names, roles, departments, contact info
- **Relationships** - Direct/indirect connections, influence levels
- **Engagement Strategy** - Communication frequency and methods
- **Design Tokens** - Light/dark mode support, colors, typography

Example JSON structure:
```json
{
  "diagramType": "Stakeholder Map",
  "projectName": "Project Name",
  "stakeholders": [
    {
      "id": "s1",
      "name": "John Doe",
      "role": "Executive Sponsor",
      "group": "Executive",
      "influence": "High",
      "position": {"x": 150, "y": 200},
      "interest": "Strategic Alignment",
      "relationship": "Direct"
    }
  ],
  "connections": [
    {"from": "s1", "to": "system", "strength": "strong"}
  ]
}
```

## Converter Details

### StakeholderMapConverter
Renders spatial positioning of stakeholders around a central system.
- **Input:** stakeholder-map-dynamic.svg
- **Output:** Stakeholder positions with relationship connectors
- **Key Features:**
  - Circular/spatial layout
  - Direct vs. indirect relationships
  - Connection strength indicators
  - Influence level visualization

### PowerInterestMatrixConverter
Creates 2×2 classification matrix (Manage Closely, Keep Satisfied, Keep Informed, Monitor).
- **Input:** power-interest-matrix-dynamic.svg
- **Output:** Quadrant-based stakeholder positioning
- **Quadrants:**
  - High Power, High Interest: Manage Closely (Red)
  - High Power, Low Interest: Keep Satisfied (Orange)
  - Low Power, High Interest: Keep Informed (Blue)
  - Low Power, Low Interest: Monitor (Gray)

### InfluenceNetworkConverter
Network diagram showing influence flows and dependencies.
- **Input:** influence-network-dynamic.svg
- **Output:** Circular network topology with edges
- **Features:**
  - Circular node layout
  - Edge weight indicators (strong/medium)
  - Type-based coloring (executive, project_team, engineering, quality)
  - Directional arrows

### SalienceModelConverter
Three-dimensional stakeholder classification.
- **Input:** salience-model-dynamic.svg
- **Output:** Stakeholder grouping by salience type
- **Salience Types:**
  - Definitive (Power + Legitimacy + Urgency)
  - Dependent (Legitimacy + Urgency)
  - Dominant (Power + Legitimacy)
  - Dangerous (Power + Urgency)
  - Discretionary (Legitimacy)
  - Dormant (Power)

### RACIMatrixConverter
Responsibility assignment matrix table.
- **Input:** raci-matrix-dynamic.svg
- **Output:** Tabular format with activities and roles
- **Responsibility Types:**
  - R (Responsible) - Does the work
  - A (Accountable) - Final authority
  - C (Consulted) - Provides input
  - I (Informed) - Kept in the loop

### StakeholderRegisterConverter
Comprehensive stakeholder inventory table.
- **Input:** stakeholder-register-dynamic.svg
- **Output:** Detailed stakeholder records
- **Columns:**
  - Name, Role, Department
  - Engagement Level, Interest, Strategy
  - Contact Information
  - Issues and Concerns

## Usage

### Single Conversion
```bash
python main.py -i stakeholder-map-dynamic.svg -o stakeholder_map.vsdx -d stakeholder-map
```

### Batch Conversion
```bash
python main.py --batch templates/svg/stakeholder --output-dir diagrams
```

### Type Auto-Detection
```bash
python main.py -i power-interest-matrix-dynamic.svg -o matrix.vsdx
# Automatically detects diagram type from filename
```

## Design Token Support

All converters support light and dark modes via design tokens:

**Light Mode:**
- Canvas: #FFFFFF
- Fill: #E5E5E5
- Stroke: #1A1A1A
- Text: #1A1A1A

**Dark Mode:**
- Canvas: #0D0D0D
- Fill: #1E1E1E
- Stroke: #F2F2F2
- Text: #F2F2F2

## Integration with Main Orchestrator

All converters are registered in the main orchestrator:

```python
CONVERTER_REGISTRY = {
    "stakeholder-map": StakeholderMapConverter,
    "power-interest-matrix": PowerInterestMatrixConverter,
    "influence-network": InfluenceNetworkConverter,
    "salience-model": SalienceModelConverter,
    "raci-matrix": RACIMatrixConverter,
    "stakeholder-register": StakeholderRegisterConverter,
}
```

## File Structure

```
stakeholder/
├── __init__.py                    # Module exports
├── README.md                      # This file
├── stakeholder_map.py             # Stakeholder Map converter
├── power_interest_matrix.py       # Power-Interest Matrix converter
├── influence_network.py           # Influence Network converter
├── salience_model.py              # Salience Model converter
├── raci_matrix.py                 # RACI Matrix converter
└── stakeholder_register.py        # Stakeholder Register converter
```

## SVG Template Filenames

Each converter expects specific SVG template filenames:
- `stakeholder-map-dynamic.svg`
- `power-interest-matrix-dynamic.svg`
- `influence-network-dynamic.svg`
- `salience-model-dynamic.svg`
- `raci-matrix-dynamic.svg`
- `stakeholder-register-dynamic.svg`

## Logging

All converters use the standard logging configuration from the base module:
- INFO: Conversion steps and completion
- WARNING: Data validation issues
- ERROR: Critical conversion failures

Example output:
```
INFO: Converting stakeholder-map to Visio...
INFO: Loaded 6 stakeholders for map
INFO: Stakeholder map saved to diagrams/stakeholder_map.vsdx
```

## Extending the Module

To add a new stakeholder diagram type:

1. **Create a new converter class** in a new `.py` file:
```python
from base.diagram_converter import BaseDiagramConverter

class NewStakeholderConverter(BaseDiagramConverter):
    diagram_type = "new-diagram-type"
    template_name = "New Diagram Type"
    
    def parse_data(self):
        return super().parse_data()
    
    def build_diagram(self, vsdx):
        # Implementation
        return vsdx
    
    def convert(self):
        self.parse_data()
        vsdx = self.create_visio_document()
        self.build_diagram(vsdx)
        return self.save_visio(vsdx)
```

2. **Export from `__init__.py`**:
```python
from .new_converter import NewStakeholderConverter

__all__ = [..., "NewStakeholderConverter"]
```

3. **Register in `main.py`**:
```python
from stakeholder import NewStakeholderConverter

CONVERTER_REGISTRY = {
    ...,
    "new-diagram-type": NewStakeholderConverter,
}
```

## Best Practices

1. **Keep JSON structure flat** - Avoid deep nesting for better parsing
2. **Include metadata** - Always include projectName and description
3. **Use consistent naming** - Follow snake_case for IDs and camelCase for display names
4. **Validate data** - Check for required fields before building diagrams
5. **Test auto-detection** - Ensure filenames match converter expectations

## Dependencies

- `python-pptx` or `python-docx` - For Visio generation
- `lxml` - For SVG parsing
- Standard library: `json`, `logging`, `pathlib`

## Error Handling

Each converter includes comprehensive error handling:
- Missing SVG file detection
- Invalid JSON parsing
- Missing required data fields
- Visio document generation errors

All errors are logged with detailed context for debugging.

---

**Version:** 1.0  
**Created:** 2024-01-15  
**Last Updated:** 2024-01-15
