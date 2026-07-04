# SVG Templates - Data-Driven Diagram System

## Overview

This directory contains reusable, data-driven SVG templates designed for both **web-based rendering** and **Visio diagram conversion**. Every template follows a strict separation of concerns: **data lives in JSON**, **presentation lives in SVG**, and **rendering adapters** bridge the two worlds.

## Design Philosophy

### Single Source of Truth
All diagram data is stored in a structured JSON block embedded in each SVG file. This enables:
- **Web rendering**: JavaScript reads JSON, populates SVG dynamically
- **Visio export**: Python reads same JSON, generates `.vsdx`, `.vstx`, or `.vssx` files
- **No duplication**: Changes to data automatically update both outputs

### Data-Driven Architecture
Every element (task, shape, connector, label, style) is derived from data, never hardcoded:
- Task bars position and size based on date calculations
- Colors determined by status/priority from data
- Connectors drawn from dependency relationships
- Text content populated from data properties
- Layout spacing and typography scale from design tokens

### Design Token Compliance
All templates follow the **Design Guidelines** (`skills/design-tokens.md`):
- **Colors**: Light (`#FFFFFF` canvas, `#E5E5E5` fill, `#1A1A1A` stroke) and Dark (`#0D0D0D` canvas, `#1E1E1E` fill, `#F2F2F2` stroke)
- **Stroke Weights**: Shape outlines (1.5px), connectors/flow lines (2px)
- **Corner Radius**: Rectangles (`rx="8"`), stadiums (fully rounded), diamonds (no rounding)
- **Typography**: 12px labels (400–500 weight), 10px secondary (600 weight), 8px micro (400 weight)
- **Spacing**: All dimensions in 8px multiples

## Template Structure

### SVG File Anatomy

```xml
<svg viewBox="0 0 1400 800" xmlns="http://www.w3.org/2000/svg">
  <!-- 1. DESIGN TOKENS (CSS Variables) -->
  <defs>
    <style>
      :root {
        --canvas-light: #FFFFFF;
        --fill-light: #E5E5E5;
        --stroke-light: #1A1A1A;
        --status-completed: #10B981;
        --status-in-progress: #3B82F6;
        /* ... more tokens ... */
      }
    </style>
  </defs>

  <!-- 2. DATA BLOCK (JSON - Single Source of Truth) -->
  <script type="application/json" id="diagram-data">
  {
    "metadata": {
      "title": "Project Name",
      "version": "1.0",
      "created": "2024-01-01T00:00:00Z",
      "mode": "light" // or "dark"
    },
    "config": {
      "timeline": {
        "start": "2024-01-01",
        "end": "2024-03-31",
        "granularity": "day" // day, week, month
      },
      "layout": {
        "taskColumnWidth": 200,
        "rowHeight": 40,
        "pixelsPerDay": 15
      }
    },
    "data": {
      "tasks": [
        {
          "id": "t1",
          "name": "Task 1",
          "start": "2024-01-01",
          "duration": 10,
          "status": "completed", // completed, in-progress, pending, blocked
          "priority": "high", // high, medium, low
          "progress": 100,
          "assignee": "Team A",
          "dependencies": [],
          "customData": {} // Extensible for future needs
        }
      ],
      "milestones": [
        {
          "id": "m1",
          "name": "Phase 1 Complete",
          "date": "2024-01-15",
          "type": "phase" // phase, deadline, review, release
        }
      ],
      "resources": [
        {
          "id": "r1",
          "name": "Team A",
          "capacity": 100,
          "allocation": {} // task allocation percentages
        }
      ]
    }
  }
  </script>

  <!-- 3. REUSABLE COMPONENTS (defs) -->
  <defs>
    <!-- Task Bar Template -->
    <g id="task-bar-template">
      <rect class="task-bar-bg" x="0" y="0" width="100" height="32" rx="4" />
      <rect class="task-bar-progress" x="0" y="0" width="50" height="32" rx="4" />
      <text class="task-label" x="5" y="20">Task Label</text>
    </g>

    <!-- Task Row Template -->
    <g id="task-row-template">
      <rect class="row-bg" x="0" y="0" width="1400" height="40" />
      <text class="task-name" x="10" y="25">Task Name</text>
      <use href="#task-bar-template" x="210" y="4" />
    </g>

    <!-- Dependency Connector Template -->
    <g id="dependency-line">
      <path class="connector" d="M 0 0 Q 10 10 20 20" stroke-dasharray="5,5" />
    </g>

    <!-- Milestone Marker Template -->
    <g id="milestone-marker">
      <circle class="milestone-dot" r="6" />
      <text class="milestone-label" y="-12">Milestone</text>
    </g>
  </defs>

  <!-- 4. STATIC STRUCTURE (Container for rendered content) -->
  <g id="header-section">
    <!-- Populated by script: date columns, gridlines -->
  </g>

  <g id="content-section">
    <!-- Populated by script: task rows, task bars, milestones, connectors -->
  </g>

  <!-- 5. INTERACTIVE ELEMENTS (Script Hooks) -->
  <g id="interactive-layer" class="interactive">
    <!-- Populated by script: hover regions, click handlers, tooltips -->
  </g>

  <!-- 6. RENDERING ENGINE (Web Adapter) -->
  <script type="text/javascript">
  (function() {
    const svgElement = document.currentScript.closest('svg');
    const dataElement = svgElement.querySelector('#diagram-data');
    const data = JSON.parse(dataElement.textContent);

    // Rendering functions
    function renderGanttChart() {
      const config = data.config;
      const tasks = data.data.tasks;
      
      // Calculate positions from data
      tasks.forEach((task, index) => {
        const startDate = new Date(task.start);
        const x = calculatePixelPosition(startDate, config);
        const width = task.duration * config.layout.pixelsPerDay;
        const y = index * config.layout.rowHeight;
        
        // Render task bar using data
        renderTaskBar(task, x, y, width);
      });

      // Render milestones, connectors, and dependencies
      renderMilestones();
      renderDependencies();
      renderGridlines();
    }

    function renderTaskBar(task, x, y, width) {
      const taskBarGroup = document.createElementNS('http://www.w3.org/2000/svg', 'use');
      taskBarGroup.setAttribute('href', '#task-bar-template');
      taskBarGroup.setAttribute('x', x);
      taskBarGroup.setAttribute('y', y);
      taskBarGroup.setAttribute('data-task-id', task.id);
      taskBarGroup.setAttribute('class', `task-bar status-${task.status} priority-${task.priority}`);
      // ... render based on data properties
    }

    // Initialize on load
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', renderGanttChart);
    } else {
      renderGanttChart();
    }
  })();
  </script>
</svg>
```

## How It Works: Web Rendering

1. **Browser loads SVG**
2. **Script extracts JSON** from `#diagram-data`
3. **Calculates positions** using date ranges and pixel conversion
4. **Renders dynamically** by:
   - Cloning `<defs>` templates
   - Setting data attributes (id, status, priority)
   - Applying CSS classes for styling
   - Adding event listeners for interactivity
5. **Result**: Fully functional, interactive Gantt chart

## How It Works: Visio Export

1. **Python script reads SVG** file
2. **Extracts JSON** from embedded `<script type="application/json">`
3. **Parses structure** (tasks, milestones, dependencies)
4. **Generates Visio shapes** using `python-vsdx` library:
   - Creates task bars as rectangles
   - Draws connectors for dependencies
   - Applies styles from design tokens
   - Positions using same layout calculations as web
5. **Outputs** `.vsdx`, `.vstx`, or `.vssx` files

### Example Python Adapter (Pseudocode)
```python
import json
import svgwrite
from vsdx import Document

def svg_to_visio(svg_path, output_path):
    # Parse SVG and extract JSON
    tree = ET.parse(svg_path)
    data_element = tree.find(".//script[@type='application/json']")
    data = json.loads(data_element.text)
    
    # Create Visio document
    doc = Document()
    page = doc.add_page()
    
    # Render tasks
    for task in data['data']['tasks']:
        x = calculate_position(task['start'], data['config'])
        y = task_index * data['config']['layout']['rowHeight']
        
        # Add shape to Visio
        shape = page.add_shape(
            name=task['name'],
            shape_type='rectangle',
            x=x, y=y, width=width, height=height
        )
        shape.style = get_style_from_token(task['status'])
    
    # Render dependencies
    for task in data['data']['tasks']:
        for dep_id in task.get('dependencies', []):
            add_connector(page, dep_id, task['id'])
    
    doc.save(output_path)
```

## Template Categories

### Current Templates

#### `gantt-chart-dynamic.svg`
- **Purpose**: Project timeline visualization with tasks, dependencies, milestones, resource allocation
- **Data Sections**: Tasks, Milestones, Resources, Timeline config, Layout config
- **Interactive Elements**: Hover for tooltips, click for task details, drag to reschedule
- **Rendering**: Date-to-pixel conversion, progress fill calculation, dependency path drawing
- **Visio Output**: Taskbars as shapes, connectors for dependencies, swimlanes for teams

## Data Schema Reference

### Gantt Chart Data Structure

```json
{
  "metadata": {
    "title": "String - Project name",
    "description": "String - Project description",
    "owner": "String - Project owner",
    "version": "String - Schema version",
    "created": "ISO8601 - Creation timestamp",
    "updated": "ISO8601 - Last update timestamp",
    "mode": "light | dark"
  },
  "config": {
    "timeline": {
      "start": "YYYY-MM-DD",
      "end": "YYYY-MM-DD",
      "granularity": "day | week | month"
    },
    "layout": {
      "taskColumnWidth": "Number - pixels",
      "rowHeight": "Number - pixels",
      "pixelsPerDay": "Number - scale factor",
      "headerHeight": "Number - pixels"
    },
    "styling": {
      "mode": "light | dark",
      "theme": "default | custom",
      "showWeekends": "Boolean",
      "showMilestones": "Boolean",
      "showDependencies": "Boolean"
    }
  },
  "data": {
    "tasks": [
      {
        "id": "Unique identifier",
        "name": "Task name",
        "description": "Optional description",
        "start": "YYYY-MM-DD",
        "duration": "Number of days",
        "status": "completed | in-progress | pending | blocked",
        "priority": "high | medium | low",
        "progress": "0–100 percentage",
        "assignee": "Resource name or ID",
        "dependencies": ["t1", "t2"], // Task IDs this depends on
        "effort": "Number - estimated hours",
        "actual": "Number - actual hours spent",
        "customData": {} // Any additional properties
      }
    ],
    "milestones": [
      {
        "id": "Unique identifier",
        "name": "Milestone name",
        "date": "YYYY-MM-DD",
        "type": "phase | deadline | review | release | checkpoint"
      }
    ],
    "resources": [
      {
        "id": "Unique identifier",
        "name": "Resource/Team name",
        "role": "Designer, Developer, etc.",
        "capacity": "100 - maximum percentage",
        "allocation": {
          "t1": 50, // Task ID → percentage allocation
          "t2": 30
        }
      }
    ]
  }
}
```

## Design Tokens in Templates

All templates use consistent design tokens:

```css
/* Light Mode (Default) */
--canvas-light: #FFFFFF;
--fill-light: #E5E5E5;
--stroke-light: #1A1A1A;
--text-light: #1A1A1A;
--muted-light: #8A8A85;

/* Dark Mode */
--canvas-dark: #0D0D0D;
--fill-dark: #1E1E1E;
--stroke-dark: #F2F2F2;
--text-dark: #F2F2F2;
--muted-dark: #8A8A85;

/* Status Colors (Consistent Across Modes) */
--status-completed: #10B981;
--status-in-progress: #3B82F6;
--status-pending: #F59E0B;
--status-blocked: #EF4444;

/* Priority Colors */
--priority-high: #DC2626;
--priority-medium: #F59E0B;
--priority-low: #6B7280;

/* Grid & Layout */
--grid-line: rgba(26, 26, 26, 0.1); /* light mode */
--grid-line-dark: rgba(242, 242, 242, 0.1); /* dark mode */
--today-indicator: #06B6D4;

/* Typography */
--font-label: 12px;
--font-secondary: 10px;
--font-micro: 8px;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
```

## Usage Examples

### Web Implementation

```html
<div id="diagram-container">
  <iframe src="gantt-chart-dynamic.svg" style="width: 100%; height: 600px;"></iframe>
</div>

<!-- Or embedded -->
<object data="gantt-chart-dynamic.svg" type="image/svg+xml" style="width: 100%;"></object>
```

### Python Visio Conversion

```python
from template_converter import SVGToVisioConverter

converter = SVGToVisioConverter()
converter.convert(
    svg_path='gantt-chart-dynamic.svg',
    output_format='vsdx',
    output_path='gantt-chart.vsdx'
)
```

### JavaScript Enhancement (Web-Based)

```javascript
// Load SVG dynamically with custom data
fetch('gantt-chart-dynamic.svg')
  .then(r => r.text())
  .then(svg => {
    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(svg, 'image/svg+xml');
    
    // Inject custom data
    const dataElement = svgDoc.querySelector('#gantt-data');
    const customData = {
      // ... your project data
    };
    dataElement.textContent = JSON.stringify(customData);
    
    // Append to DOM
    document.getElementById('container').appendChild(
      svgDoc.documentElement
    );
  });
```

## Best Practices

1. **Keep Data Clean**: Ensure all dates are ISO8601 format, IDs are unique, dependencies exist in task list
2. **Design Token Usage**: Always reference CSS variables, never hardcode colors
3. **Reusable Components**: Add new shape types to `<defs>` before rendering
4. **Responsive Layout**: Use viewport calculations, not fixed pixel coordinates
5. **Accessibility**: Add `aria-label` and `role` attributes to interactive elements
6. **Mode Support**: Test both light and dark modes before deployment
7. **Performance**: Limit to ~200 tasks before implementing virtualization

## Extending Templates

### Adding a New Field to Task Data

1. Add to data schema (`config.data.tasks[]`)
2. Update rendering logic to calculate new positions/sizes
3. Add CSS class or attribute binding
4. Update Python adapter to handle new field
5. Test both web and Visio output

### Creating a New Template

1. Copy `gantt-chart-dynamic.svg` as starting point
2. Define data schema in JSON comment
3. Create reusable components in `<defs>`
4. Implement rendering logic in `<script>`
5. Add Python adapter for Visio export
6. Document schema and usage in this README

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Tasks not rendering | JSON invalid | Validate JSON in `#diagram-data` |
| Colors wrong | Mode mismatch | Check `metadata.mode` matches CSS |
| Dates off by one | Timezone issue | Use UTC dates in data |
| Visio export fails | Missing Python deps | Install `python-vsdx`, `lxml` |
| Text overflowing | Column width too narrow | Increase `layout.taskColumnWidth` |

## Related Documentation

- `skills/design-tokens.md` - Design system tokens
- `skills/reusable-components.md` - SVG reusable component patterns
- `skills/SKILL.md` - General template authoring guidelines
- `skills/README.md` - Skills directory overview
