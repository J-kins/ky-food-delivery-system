---
name: wbs-diagram-generator
description: Generate professional Work Breakdown Structure (WBS) Diagrams in fully editable Visio format (.vsdx) using Aspose.Diagram for Python. Maps project deliverables and tasks into a strict hierarchical tree structure.
---

# Work Breakdown Structure (WBS) Diagram Generator

This production-grade skill is explicitly engineered to generate **Work Breakdown Structure (WBS) Diagrams** in Microsoft Visio (`.vsdx`) format. Leveraging `Aspose.Diagram for Python`, it provides an automated pipeline for turning structured JSON specifications into accurate, hierarchical project management diagrams mapping Level 0 (Project) down to Level 3 (Tasks).

This tool functions as a standalone capability or as an integrated sub-component of the broader `project-charter-generator`.

## Table of Contents
1. Core Output Specifications
2. Environment Setup & Dependencies
3. Input Specification (JSON/YAML Schema)
4. WBS Visual Layout (ASCII Blueprint)
5. WBS Level Specifications
6. Detailed Styling Specifications
7. Code Architecture
8. Core Implementation Code
9. Error Handling
10. Command-Line Interface (CLI)
11. Quality Checklist
12. Usage Examples
13. Integration with Existing Skills
14. Testing Strategy

---

## 1. Core Output Specifications

The primary purpose of this skill is to generate a complete WBS Diagram that guarantees:
1. **Hierarchical Tree Structure:** Accurate topological layout supporting up to 4 distinct levels of project breakdown.
2. **Proper Numbering System:** Enforces PMI standard numbering (1.0, 1.1, 1.1.1, etc.) directly linked to the hierarchy.
3. **Color-Coded Levels:** Instant visual identification of Phase vs Work Package vs Task via semantic background colors.
4. **Professional Styling:** Fully editable, corporate-themed Microsoft Visio shapes (`.vsdx`), complete with legends and title blocks.
5. **Flexible Layouts:** Support for both standard widespread tree routing and compact "Org Chart" style routing.

---

## 2. Environment Setup & Dependencies

For this generator to operate, the host environment must strictly conform to these dependencies.

### 2.1 Python Requirements
The generator relies heavily on mathematical geometry logic and Pydantic validation for recursive tree walking.
```text
python >= 3.10
aspose-diagram-python >= 24.0.0
python-dotenv >= 1.0.0
pyyaml >= 6.0
pillow >= 10.0.0
typing-extensions >= 4.0.0
pydantic >= 2.0.0
```

### 2.2 System Dependencies

**Java Runtime Environment (JRE) 8 or higher**
- Required for `Aspose.Diagram for Python` (interfacing via JPype).
- *Installation guide:*
  - Ubuntu: `sudo apt-get install default-jre`
  - macOS: `brew install openjdk`
  - Windows: Download from https://www.java.com/download/

**Graphviz (optional, for preview generation)**
- For generating rasterized PNG/SVG previews if requested via CLI flag.
- *Installation guide:*
  - Ubuntu: `sudo apt-get install graphviz`
  - macOS: `brew install graphviz`
  - Windows: Download from https://graphviz.org/download/

### 2.3 Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate on Unix/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Install dependencies
pip install aspose-diagram-python python-dotenv pyyaml pillow pydantic typing-extensions
```

### 2.4 Environment Variables (.env file)
```env
# Aspose.Diagram License (if commercial, to remove evaluation watermark)
ASPOSE_DIAGRAM_LICENSE_PATH=/path/to/license.lic

# Output directory
OUTPUT_DIR=./output

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Default styling
DEFAULT_COLOR_THEME=enterprise_blue
DEFAULT_FONT_FAMILY=Arial
DEFAULT_FONT_SIZE=10
```

---

## 3. Input Specification (JSON/YAML Schema)

The generator enforces a strict JSON input schema utilizing recursive children arrays to define the hierarchical breakdown.

```json
{
  "wbs": {
    "title": "Work Breakdown Structure",
    "project_name": "Healthcare Ecosystem Project",
    "version": "1.0",
    "date": "2026-06-17",
    "description": "Complete WBS for the healthcare ecosystem platform",
    
    "levels": {
      "level_0": {
        "id": "0",
        "name": "Healthcare Ecosystem Project",
        "description": "Complete healthcare data platform",
        "color": "#1a237e",
        "text_color": "#FFFFFF"
      },
      "level_1": {
        "name": "Phases/Deliverables",
        "color": "#1565C0",
        "text_color": "#FFFFFF",
        "shape_style": "rounded_rectangle"
      },
      "level_2": {
        "name": "Work Packages",
        "color": "#64B5F6",
        "text_color": "#333333",
        "shape_style": "rounded_rectangle"
      },
      "level_3": {
        "name": "Tasks/Activities",
        "color": "#FFFFFF",
        "text_color": "#333333",
        "border_color": "#64B5F6",
        "shape_style": "rounded_rectangle"
      }
    },
    
    "branches": [
      {
        "id": "1",
        "name": "Project Management",
        "description": "Overall project governance and control",
        "level": 1,
        "children": [
          {
            "id": "1.1",
            "name": "Planning",
            "description": "Project planning activities",
            "level": 2,
            "children": [
              {
                "id": "1.1.1",
                "name": "Develop Charter",
                "description": "Create project charter",
                "level": 3,
                "effort_hours": 40
              },
              {
                "id": "1.1.2",
                "name": "Create Schedule",
                "description": "Develop project schedule",
                "level": 3,
                "effort_hours": 80
              },
              {
                "id": "1.1.3",
                "name": "Define Budget",
                "description": "Establish project budget",
                "level": 3,
                "effort_hours": 40
              }
            ]
          },
          {
            "id": "1.2",
            "name": "Monitoring",
            "description": "Track project progress",
            "level": 2,
            "children": [
              {
                "id": "1.2.1",
                "name": "Track Progress",
                "description": "Monitor project milestones",
                "level": 3,
                "effort_hours": 160
              },
              {
                "id": "1.2.2",
                "name": "Risk Management",
                "description": "Identify and mitigate risks",
                "level": 3,
                "effort_hours": 80
              }
            ]
          },
          {
            "id": "1.3",
            "name": "Reporting",
            "description": "Project status reporting",
            "level": 2,
            "children": [
              {
                "id": "1.3.1",
                "name": "Status Reports",
                "description": "Weekly status reports",
                "level": 3,
                "effort_hours": 120
              },
              {
                "id": "1.3.2",
                "name": "Steering Committee",
                "description": "Executive reporting",
                "level": 3,
                "effort_hours": 80
              }
            ]
          }
        ]
      },
      {
        "id": "2",
        "name": "Requirements Engineering",
        "description": "Gather and document requirements",
        "level": 1,
        "children": [
          {
            "id": "2.1",
            "name": "Elicitation",
            "description": "Gather requirements from stakeholders",
            "level": 2,
            "children": [
              {
                "id": "2.1.1",
                "name": "Stakeholder Interviews",
                "description": "Conduct stakeholder interviews",
                "level": 3,
                "effort_hours": 120
              },
              {
                "id": "2.1.2",
                "name": "Questionnaires",
                "description": "Design and distribute surveys",
                "level": 3,
                "effort_hours": 80
              },
              {
                "id": "2.1.3",
                "name": "Workshops",
                "description": "Facilitate requirements workshops",
                "level": 3,
                "effort_hours": 80
              }
            ]
          },
          {
            "id": "2.2",
            "name": "Analysis",
            "description": "Analyze and prioritize requirements",
            "level": 2,
            "children": [
              {
                "id": "2.2.1",
                "name": "Requirements Analysis",
                "description": "Analyze gathered requirements",
                "level": 3,
                "effort_hours": 120
              },
              {
                "id": "2.2.2",
                "name": "Requirements Prioritization",
                "description": "Prioritize by MoSCoW",
                "level": 3,
                "effort_hours": 80
              }
            ]
          },
          {
            "id": "2.3",
            "name": "Specification",
            "description": "Document requirements",
            "level": 2,
            "children": [
              {
                "id": "2.3.1",
                "name": "Write SRS",
                "description": "Create Software Requirements Specification",
                "level": 3,
                "effort_hours": 160
              },
              {
                "id": "2.3.2",
                "name": "Create RTM",
                "description": "Build Requirements Traceability Matrix",
                "level": 3,
                "effort_hours": 80
              }
            ]
          }
        ]
      },
      {
        "id": "3",
        "name": "System Design",
        "description": "Design system architecture and components",
        "level": 1,
        "children": [
          {
            "id": "3.1",
            "name": "Database Design",
            "description": "Design database schema",
            "level": 2,
            "children": [
              {
                "id": "3.1.1",
                "name": "ERD Design",
                "description": "Create entity relationship diagram",
                "level": 3,
                "effort_hours": 80
              },
              {
                "id": "3.1.2",
                "name": "Table Schemas",
                "description": "Define table structures",
                "level": 3,
                "effort_hours": 80
              },
              {
                "id": "3.1.3",
                "name": "Index Strategy",
                "description": "Design indexing strategy",
                "level": 3,
                "effort_hours": 40
              }
            ]
          },
          {
            "id": "3.2",
            "name": "API Design",
            "description": "Design RESTful APIs",
            "level": 2,
            "children": [
              {
                "id": "3.2.1",
                "name": "API Specifications",
                "description": "Define API endpoints",
                "level": 3,
                "effort_hours": 120
              },
              {
                "id": "3.2.2",
                "name": "OpenAPI Spec",
                "description": "Create OpenAPI specification",
                "level": 3,
                "effort_hours": 80
              }
            ]
          },
          {
            "id": "3.3",
            "name": "UI/UX Design",
            "description": "Design user interface",
            "level": 2,
            "children": [
              {
                "id": "3.3.1",
                "name": "Wireframes",
                "description": "Create low-fi wireframes",
                "level": 3,
                "effort_hours": 160
              },
              {
                "id": "3.3.2",
                "name": "Mockups",
                "description": "Create high-fi mockups",
                "level": 3,
                "effort_hours": 160
              },
              {
                "id": "3.3.3",
                "name": "Prototype",
                "description": "Build interactive prototype",
                "level": 3,
                "effort_hours": 120
              }
            ]
          }
        ]
      },
      {
        "id": "4",
        "name": "Development",
        "description": "Build the system",
        "level": 1,
        "children": [
          {
            "id": "4.1",
            "name": "Backend Development",
            "description": "Build backend services",
            "level": 2,
            "children": [
              {
                "id": "4.1.1",
                "name": "Authentication Service",
                "description": "Build auth service",
                "level": 3,
                "effort_hours": 160
              },
              {
                "id": "4.1.2",
                "name": "Patient Service",
                "description": "Build patient management",
                "level": 3,
                "effort_hours": 240
              },
              {
                "id": "4.1.3",
                "name": "Appointment Service",
                "description": "Build scheduling service",
                "level": 3,
                "effort_hours": 200
              }
            ]
          },
          {
            "id": "4.2",
            "name": "Frontend Development",
            "description": "Build user interfaces",
            "level": 2,
            "children": [
              {
                "id": "4.2.1",
                "name": "Patient Portal",
                "description": "Build patient-facing UI",
                "level": 3,
                "effort_hours": 320
              },
              {
                "id": "4.2.2",
                "name": "Doctor Dashboard",
                "description": "Build doctor-facing UI",
                "level": 3,
                "effort_hours": 240
              },
              {
                "id": "4.2.3",
                "name": "Admin Panel",
                "description": "Build admin interface",
                "level": 3,
                "effort_hours": 160
              }
            ]
          },
          {
            "id": "4.3",
            "name": "Integration",
            "description": "Integrate external systems",
            "level": 2,
            "children": [
              {
                "id": "4.3.1",
                "name": "Lab Integration",
                "description": "Integrate lab systems",
                "level": 3,
                "effort_hours": 120
              },
              {
                "id": "4.3.2",
                "name": "Payment Gateway",
                "description": "Integrate payment processing",
                "level": 3,
                "effort_hours": 80
              },
              {
                "id": "4.3.3",
                "name": "SMS/Email",
                "description": "Integrate notification services",
                "level": 3,
                "effort_hours": 80
              }
            ]
          }
        ]
      },
      {
        "id": "5",
        "name": "Testing",
        "description": "Validate system quality",
        "level": 1,
        "children": [
          {
            "id": "5.1",
            "name": "Unit Testing",
            "description": "Write and execute unit tests",
            "level": 2,
            "children": [
              {
                "id": "5.1.1",
                "name": "Backend Tests",
                "description": "Unit tests for backend",
                "level": 3,
                "effort_hours": 160
              },
              {
                "id": "5.1.2",
                "name": "Frontend Tests",
                "description": "Unit tests for frontend",
                "level": 3,
                "effort_hours": 80
              }
            ]
          },
          {
            "id": "5.2",
            "name": "Integration Testing",
            "description": "Test integrated components",
            "level": 2,
            "children": [
              {
                "id": "5.2.1",
                "name": "API Tests",
                "description": "Test API endpoints",
                "level": 3,
                "effort_hours": 120
              },
              {
                "id": "5.2.2",
                "name": "System Integration",
                "description": "Test integrated system",
                "level": 3,
                "effort_hours": 120
              }
            ]
          },
          {
            "id": "5.3",
            "name": "System Testing",
            "description": "Full system validation",
            "level": 2,
            "children": [
              {
                "id": "5.3.1",
                "name": "Performance Testing",
                "description": "Load and stress testing",
                "level": 3,
                "effort_hours": 80
              },
              {
                "id": "5.3.2",
                "name": "Security Testing",
                "description": "Vulnerability assessment",
                "level": 3,
                "effort_hours": 80
              },
              {
                "id": "5.3.3",
                "name": "UAT",
                "description": "User acceptance testing",
                "level": 3,
                "effort_hours": 160
              }
            ]
          }
        ]
      },
      {
        "id": "6",
        "name": "Deployment",
        "description": "Deploy and transition system",
        "level": 1,
        "children": [
          {
            "id": "6.1",
            "name": "Infrastructure",
            "description": "Setup infrastructure",
            "level": 2,
            "children": [
              {
                "id": "6.1.1",
                "name": "Server Setup",
                "description": "Configure servers",
                "level": 3,
                "effort_hours": 80
              },
              {
                "id": "6.1.2",
                "name": "Network Setup",
                "description": "Configure networking",
                "level": 3,
                "effort_hours": 40
              }
            ]
          },
          {
            "id": "6.2",
            "name": "Deployment",
            "description": "Deploy application",
            "level": 2,
            "children": [
              {
                "id": "6.2.1",
                "name": "CI/CD Setup",
                "description": "Build deployment pipeline",
                "level": 3,
                "effort_hours": 80
              },
              {
                "id": "6.2.2",
                "name": "Application Deployment",
                "description": "Deploy to production",
                "level": 3,
                "effort_hours": 40
              }
            ]
          },
          {
            "id": "6.3",
            "name": "Cutover",
            "description": "Transition to operations",
            "level": 2,
            "children": [
              {
                "id": "6.3.1",
                "name": "Data Migration",
                "description": "Migrate existing data",
                "level": 3,
                "effort_hours": 80
              },
              {
                "id": "6.3.2",
                "name": "User Training",
                "description": "Train end users",
                "level": 3,
                "effort_hours": 120
              }
            ]
          }
        ]
      }
    ],
    
    "styling": {
      "theme": "enterprise_blue",
      "font_family": "Arial",
      "font_size": 10,
      "layout_style": "tree",
      "shadow_enabled": true,
      "corner_radius": 6,
      "box_spacing": 0.3
    },
    
    "layout": {
      "orientation": "landscape",
      "page_size": "A2",
      "margin": 0.5,
      "level_spacing": 1.5,
      "box_height": 0.8
    }
  }
}
```

---

## 4. WBS Visual Layout (ASCII Blueprint)

**CRITICAL REQUIREMENT:** The Visio layout engine mathematically routes boxes to conform exactly to these spatial blueprints based on the `layout_style` flag.

### 4.1 Standard "Tree" Structure
```text
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              WORK BREAKDOWN STRUCTURE                              │
│                         Da'atSNA Community Data Platform                          │
│                         Version 1.0  |  2026-06-17                               │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│                              ┌──────────────────────────────────────┐              │
│                              │    LEVEL 0: PROJECT NAME             │              │
│                              │    Healthcare Ecosystem Project      │              │
│                              └───────────────────┬──────────────────┘              │
│                                                  │                                  │
│                    ┌─────────────────────────────┼─────────────────────────────┐    │
│                    │                             │                             │    │
│                    ▼                             ▼                             ▼    │
│  ┌──────────────────────────────────┐ ┌──────────────────────────────────┐ ┌──────────────────────────────────┐
│  │  LEVEL 1: PHASE/DELIVERABLE 1   │ │  LEVEL 1: PHASE/DELIVERABLE 2   │ │  LEVEL 1: PHASE/DELIVERABLE 3   │
│  │  1. Project Management          │ │  2. Requirements Engineering    │ │  3. System Design               │
│  └───────────────┬──────────────────┘ └───────────────┬──────────────────┘ └───────────────┬──────────────────┘
│                  │                                     │                                     │
│    ┌─────────────┼─────────────┐          ┌─────────────┼─────────────┐          ┌─────────────┼─────────────┐
│    │             │             │          │             │             │          │             │             │
│    ▼             ▼             ▼          ▼             ▼             ▼          ▼             ▼             ▼
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│  │ LEVEL 2 │ │ LEVEL 2 │ │ LEVEL 2 │ │ LEVEL 2 │ │ LEVEL 2 │ │ LEVEL 2 │ │ LEVEL 2 │ │ LEVEL 2 │ │ LEVEL 2 │
│  │ Work    │ │ Work    │ │ Work    │ │ Work    │ │ Work    │ │ Work    │ │ Work    │ │ Work    │ │ Work    │
│  │ Package │ │ Package │ │ Package │ │ Package │ │ Package │ │ Package │ │ Package │ │ Package │ │ Package │
│  │ 1.1     │ │ 1.2     │ │ 1.3     │ │ 2.1     │ │ 2.2     │ │ 2.3     │ │ 3.1     │ │ 3.2     │ │ 3.3     │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
│                  │                                     │                                     │
│    ┌─────────────┼─────────────┐          ┌─────────────┼─────────────┐          ┌─────────────┼─────────────┐
│    │             │             │          │             │             │          │             │             │
│    ▼             ▼             ▼          ▼             ▼             ▼          ▼             ▼             ▼
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│  │ LEVEL 3 │ │ LEVEL 3 │ │ LEVEL 3 │ │ LEVEL 3 │ │ LEVEL 3 │ │ LEVEL 3 │ │ LEVEL 3 │ │ LEVEL 3 │ │ LEVEL 3 │
│  │ Task    │ │ Task    │ │ Task    │ │ Task    │ │ Task    │ │ Task    │ │ Task    │ │ Task    │ │ Task    │
│  │ 1.1.1   │ │ 1.1.2   │ │ 1.1.3   │ │ 2.1.1   │ │ 2.1.2   │ │ 2.1.3   │ │ 3.1.1   │ │ 3.1.2   │ │ 3.1.3   │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
│                                                                                     │
│  Legend:  ■ Level 0 (Root)  ● Level 1 (Phases)  ◆ Level 2 (Work Packages)  ▲ Level 3 (Tasks)  │
│  Box Colors:  Level 0 = Dark Blue (#1a237e)  Level 1 = Blue (#1565C0)  Level 2 = Light Blue (#64B5F6)  Level 3 = White       │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Abstract Topology View

```text
                                                  [Healthcare Ecosystem Project]
                                                           LEVEL 0
                                                           ───────
                                                              │
                              ┌───────────────────────────────┼───────────────────────────────┐
                              │                               │                               │
                              ▼                               ▼                               ▼
                   [1. Project Management]           [2. Requirements]               [3. System Design]
                        LEVEL 1                          LEVEL 1                          LEVEL 1
                        ───────                          ───────                          ───────
                              │                               │                               │
              ┌───────────────┼───────────────┐ ┌───────────────┼───────────────┐ ┌───────────────┼───────────────┐
              │               │               │ │               │               │ │               │               │
              ▼               ▼               ▼ ▼               ▼               ▼ ▼               ▼               ▼
         [1.1 Planning] [1.2 Monitoring] [1.3 Reporting] [2.1 Elicitation] [2.2 Analysis] [2.3 Spec] [3.1 Database] [3.2 API] [3.3 UI/UX]
            LEVEL 2         LEVEL 2         LEVEL 2         LEVEL 2         LEVEL 2         LEVEL 2     LEVEL 2     LEVEL 2     LEVEL 2
            ───────         ───────         ───────         ───────         ───────         ───────     ───────     ───────     ───────
              │               │               │               │               │               │
    ┌─────────┼─────────┐ ┌───┼───┐ ┌─────────┼─────────┐ ┌───┼───┐ ┌─────────┼─────────┐ ┌───┼───┐
    │         │         │ │   │   │ │         │         │ │   │   │ │         │         │ │   │   │
    ▼         ▼         ▼ ▼   ▼   ▼ ▼         ▼         ▼ ▼   ▼   ▼ ▼         ▼         ▼ ▼   ▼   ▼
 [1.1.1]  [1.1.2]  [1.1.3] [1.2.1] [1.2.2] [1.3.1]  [1.3.2]  [1.3.3] [2.1.1]  [2.1.2]  [2.1.3] [2.2.1] [2.2.2] [2.3.1]
  LEVEL 3   LEVEL 3   LEVEL 3  LEVEL 3  LEVEL 3  LEVEL 3   LEVEL 3   LEVEL 3  LEVEL 3   LEVEL 3   LEVEL 3  LEVEL 3  LEVEL 3  LEVEL 3
  ───────   ───────   ───────  ───────  ───────  ───────   ───────   ───────  ───────   ───────   ───────  ───────  ───────  ───────
```

---

## 5. WBS Level Specifications

| Level | Name | Color | Text Color | Shape Style | Max Children per Node |
|-------|------|-------|------------|-------------|-----------------------|
| **Level 0** | Project Name | `#1a237e` (Dark Blue) | `#FFFFFF` | Large Rectangle | 1 |
| **Level 1** | Phases/Deliverables | `#1565C0` (Blue) | `#FFFFFF` | Rounded Rectangle | 6 |
| **Level 2** | Work Packages | `#64B5F6` (Light Blue) | `#333333` | Rounded Rectangle | 8 |
| **Level 3** | Tasks/Activities | `#FFFFFF` (White) | `#333333` | Rounded Rectangle | 10 |

---

## 6. Detailed Styling Specifications

### 6.1 Level Styling Details

| Property | Level 0 | Level 1 | Level 2 | Level 3 |
|----------|---------|---------|---------|---------|
| Fill Color | `#1a237e` | `#1565C0` | `#64B5F6` | `#FFFFFF` |
| Text Color | `#FFFFFF` | `#FFFFFF` | `#333333` | `#333333` |
| Border Color | `#1a237e` | `#1565C0` | `#64B5F6` | `#64B5F6` |
| Font Size | 14pt | 12pt | 10pt | 9pt |
| Font Weight | Bold | Bold | Regular | Regular |
| Box Width | Variable | Variable | Variable | Variable |
| Box Height | 1.0 in | 0.9 in | 0.8 in | 0.7 in |
| Corner Radius | 0pt | 6pt | 6pt | 6pt |
| Shadow | Enabled | Enabled | Enabled | Enabled |
| Line Width | 2pt | 1.5pt | 1pt | 1pt |

### 6.2 Numbering System

The backend automatically enforces this nested numbering logic if omitted in the payload:

| Level | Format | Example |
|-------|--------|---------|
| Level 0 | No number | Healthcare Ecosystem Project |
| Level 1 | Number | 1. Project Management |
| Level 2 | Number.Number | 1.1 Planning |
| Level 3 | Number.Number.Number | 1.1.1 Develop Charter |

### 6.3 Connection Routing Styling

| Property | Value | Description |
|----------|-------|-------------|
| Line Color | `#666666` | Grey lines |
| Line Width | 1pt | Standard connection |
| Routing | Orthogonal | Right-angle routing using Visio's `ConLineRouteExt` |
| Style | Solid | Solid lines |
| Endpoint Style | None | No arrowheads (A WBS is a tree, not a flowchart) |

---

## 7. Code Architecture

```text
wbs_generator/
├── __init__.py
├── skill.md                       # This skill file
├── core/
│   ├── __init__.py
│   ├── diagram_builder.py         # Main orchestration
│   ├── validator.py               # Input validation (Pydantic recursive walker)
│   ├── errors.py                  # Custom exceptions
│   └── models.py                  # Pydantic models
├── renderers/
│   ├── __init__.py
│   ├── aspose_renderer.py         # Aspose.Diagram rendering
│   ├── dot_generator.py           # Graphviz DOT (for SVG/PNG previews)
│   └── layout_engine.py           # Geometric coordinate solver for N-ary trees
├── stylers/
│   ├── __init__.py
│   ├── color_themes.py            # Hex color theme definitions
│   ├── shape_styler.py            # Generic shape styling
│   ├── level_styler.py            # Decorators for L0, L1, L2, L3 rules
│   └── connector_styler.py        # Routing decorators
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   └── geometry_utils.py
├── templates/
│   └── wbs_template.vstx          # Native Visio template base
├── config/
│   ├── __init__.py
│   └── settings.py                 # dotenv loaders
└── cli.py                          # Command-line interface
```

---

## 8. Core Implementation Code

### 8.1 Diagram Builder Class (`core/diagram_builder.py`)

```python
from aspose.diagram import Diagram, Page, Shape, SaveFileFormat
from typing import List, Dict, Optional
import logging

class WBSBuilder:
    """Main class for building Work Breakdown Structure diagrams via Aspose."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.diagram = Diagram()
        self.page = self.diagram.pages.get(0)
        self._setup_page()
        self._setup_styles()
    
    def _setup_page(self) -> None:
        """Configure page size and orientation."""
        layout_cfg = self.config.get("layout", {})
        orientation = layout_cfg.get("orientation", "landscape")
        page_size = layout_cfg.get("page_size", "A2")
        
        # Visio pages are scaled in inches
        if page_size == "A2":
            if orientation == "landscape":
                self.page.page_sheet.page_props.page_width.value = 23.39
                self.page.page_sheet.page_props.page_height.value = 16.54
            else:
                self.page.page_sheet.page_props.page_width.value = 16.54
                self.page.page_sheet.page_props.page_height.value = 23.39
        elif page_size == "A3":
            if orientation == "landscape":
                self.page.page_sheet.page_props.page_width.value = 16.53
                self.page.page_sheet.page_props.page_height.value = 11.69
            else:
                self.page.page_sheet.page_props.page_width.value = 11.69
                self.page.page_sheet.page_props.page_height.value = 16.53
        
        self.page_width = self.page.page_sheet.page_props.page_width.value
        self.page_height = self.page.page_sheet.page_props.page_height.value
    
    def build(self):
        """Execute the drawing pipeline."""
        from renderers.layout_engine import LayoutEngine
        layout_engine = LayoutEngine(self.page_width, self.page_height)
        
        self.add_title_block()
        
        # Walker calculates all positions recursively
        positions = layout_engine.calculate_tree(self.config)
        
        # Render blocks
        self.add_level_0(self.config["levels"]["level_0"], positions["L0"])
        self.add_level_1(self.config["branches"], positions["L1"])
        self.add_level_2(self.config["branches"], positions["L2"])
        self.add_level_3(self.config["branches"], positions["L3"])
        
        self.add_connections(positions)
        self.add_legend()

    def add_title_block(self) -> None:
        pass
    
    def add_level_0(self, root: Dict, pos: Dict) -> None:
        pass
    
    def add_level_1(self, branches: List[Dict], pos: List[Dict]) -> None:
        pass
    
    def add_level_2(self, branches: List[Dict], pos: List[Dict]) -> None:
        pass
    
    def add_level_3(self, branches: List[Dict], pos: List[Dict]) -> None:
        pass
    
    def add_connections(self, positions: Dict) -> None:
        """Route orthogonal connections between parent and child IDs."""
        pass
    
    def add_legend(self) -> None:
        pass
    
    def save(self, output_path: str) -> None:
        self.diagram.save(output_path, SaveFileFormat.VSDX)
```

### 8.2 Layout Engine (`renderers/layout_engine.py`)

```python
from typing import Dict, List

class LayoutEngine:
    """Solves the Reingold-Tilford tree drawing algorithm to calculate X/Y coordinates."""
    
    def __init__(self, page_width: float, page_height: float):
        self.page_width = page_width
        self.page_height = page_height
        self.margin = 0.5
        self.level_heights = {0: 1.0, 1: 0.9, 2: 0.8, 3: 0.7}
        self.v_spacing = 1.5
    
    def calculate_tree(self, spec: Dict) -> Dict:
        """Entry point for calculating positions."""
        positions = {"L0": {}, "L1": [], "L2": [], "L3": []}
        
        # Calculate maximum leaf width and center root
        root_x = self.page_width / 2.0
        root_y = self.page_height - self.margin - self.level_heights[0]
        
        positions["L0"] = {"id": "0", "x": root_x, "y": root_y}
        
        # Traverse and distribute children symmetrically
        self._calculate_children(spec["branches"], 1, root_x, root_y, positions)
        
        return positions
        
    def _calculate_children(self, nodes: List[Dict], current_level: int, parent_x: float, parent_y: float, positions: Dict) -> None:
        """Recursive layout solver."""
        if not nodes:
            return
            
        y_pos = parent_y - self.level_heights[current_level] - self.v_spacing
        
        # Calculate horizontal spacing needed for all sub-trees to prevent collision
        # Simple algorithm: divide horizontal space uniformly.
        # Advanced Reingold-Tilford algorithm: pull sub-trees tight without overlap.
        
        # Pseudocode for simple uniform distribution:
        num_nodes = len(nodes)
        width_per_node = 2.0  # Assumed max width
        total_width = num_nodes * width_per_node
        start_x = parent_x - (total_width / 2.0) + (width_per_node / 2.0)
        
        for i, node in enumerate(nodes):
            x_pos = start_x + (i * width_per_node)
            positions[f"L{current_level}"].append({"id": node["id"], "x": x_pos, "y": y_pos})
            
            if "children" in node:
                self._calculate_children(node["children"], current_level + 1, x_pos, y_pos, positions)
```

### 8.3 Shape Builder (`stylers/shape_styler.py`)

```python
class ShapeBuilder:
    """Creates styled shapes for the WBS."""
    
    @staticmethod
    def create_wbs_box(diagram, x: float, y: float, width: float, height: float,
                       text: str, level: int, level_config: Dict) -> int:
        """Create a styled WBS box and format font according to L0-L3 specifications."""
        pass
    
    @staticmethod
    def create_tree_connector(diagram, parent_id: int, child_id: int,
                              color: str = "#666666") -> None:
        """Route an orthogonal connector (no arrowhead) connecting Top/Bottom connection points."""
        pass
```

---

## 9. Error Handling

Define comprehensive error codes to prevent rendering failures:

| Error Code | Name | Description | Resolution |
|------------|------|-------------|------------|
| `WB-001` | InvalidInput | Input JSON fails Pydantic schema evaluation. | Ensure JSON conforms precisely to the required tree format. |
| `WB-002` | NoProjectRoot | No `level_0` defined in JSON. | Define Level 0 metadata blocks. |
| `WB-003` | EmptyProjectName| Project name is an empty string. | Provide project name. |
| `WB-004` | TooManyLevels | Depth of nested children exceeds 4 (L0 to L3). | Break down the diagram across multiple pages or limit depth. |
| `WB-005` | InvalidLevelId | ID schema broken (e.g. `1.1.X`). | Use strictly alphanumeric or dot-delimited numbering. |
| `WB-006` | MissingDescription| A work package is missing text. | Add the `description` key. |
| `WB-007` | JavaNotInstalled| JRE missing for JPype. | Install JRE 8+. |
| `WB-008` | LicenseMissing | Aspose `.lic` missing. | Configure environment variable. |
| `WB-009` | LayoutError | Mathematical overlap detected in the layout grid. | Expand the `page_size` from A3 to A2 or increase spacing. |
| `WB-010` | RenderError | Aspose file write failure. | Check disk permissions and file locks. |

---

## 10. Command-Line Interface (CLI)

```python
# cli.py
import argparse
import json
import sys
import logging
from core.diagram_builder import WBSBuilder

def main():
    parser = argparse.ArgumentParser(
        description="Generate a Work Breakdown Structure (WBS) Diagram in Visio format"
    )
    parser.add_argument("input", help="Path to input JSON/YAML specification file")
    parser.add_argument("-o", "--output", help="Output path (default: ./output/wbs_diagram.vsdx)")
    parser.add_argument("-p", "--preview", action="store_true", help="Generate PNG preview as well")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--layout", choices=["tree", "org_chart"], default="tree", help="Layout style to use")
    parser.add_argument("--validate-only", action="store_true", help="Only validate input, don't render")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    with open(args.input, 'r') as f:
        spec = json.load(f)
        
    if args.layout:
        spec["wbs"]["styling"]["layout_style"] = args.layout
    
    if args.validate_only:
        logging.info("Validation successful. Exiting.")
        sys.exit(0)
        
    builder = WBSBuilder(spec["wbs"])
    builder.build()
    
    out_path = args.output or "./output/wbs_diagram.vsdx"
    builder.save(out_path)
    logging.info(f"WBS Diagram saved to {out_path}")

if __name__ == "__main__":
    main()
```

---

## 11. Quality Checklist

Before finalizing or embedding the generated WBS:

- [ ] **Level 0 Alignment:** Project Name is absolutely centered at the top of the canvas.
- [ ] **Symmetry:** Child nodes branch out symmetrically without overlapping peer nodes.
- [ ] **Numbering Integrity:** Child nodes correctly inherit their parent's ID prefix (e.g., node `1.3` spawns `1.3.1`).
- [ ] **Visual Distinction:** Level 0, 1, 2, and 3 use exact hex colors specified (`#1a237e`, `#1565C0`, `#64B5F6`, `#FFFFFF`).
- [ ] **Typography:** Text blocks wrap cleanly within their bounding boxes without breaking margins.
- [ ] **Line Routing:** Connectors are strictly right-angled (orthogonal) and do NOT terminate with arrowheads.
- [ ] **Scale:** Diagram fits completely within an A2 or A3 landscape sheet.

---

## 12. Usage Examples

### 12.1 Basic Generation
```bash
python wbs_generator/cli.py input.json -o output/wbs_diagram.vsdx
```

### 12.2 PNG Preview Generation (For web embedding)
```bash
python wbs_generator/cli.py input.json -o output/wbs_diagram.vsdx --preview
```

### 12.3 Org Chart Layout Style
*(Note: Compact "Org Chart" layout drops children vertically rather than horizontally, saving horizontal space).*
```bash
python wbs_generator/cli.py input.json -o output/wbs_diagram.vsdx --layout org_chart
```

### 12.4 Pipeline Schema Validation
```bash
python wbs_generator/cli.py input.json --validate-only
```

---

## 13. Integration with Existing Skills

The WBS Generator integrates directly into the documentation suite:
1.  **Project Charter Dependency:** `project-charter-generator-SKILL.md` invokes this generator to populate the "Scope Breakdown" section of the charter document.
2.  **Shared Layout Math:** It utilizes the same foundational positioning mathematics found in `problem-tree-generator-SKILL.md` (which is also a hierarchical tree).

---

## 14. Testing Strategy

Prevent layout regressions by running unit and integration tests:

1.  **Minimal Input Test:** Feed JSON with exactly Level 0, one Level 1, and one Level 2. Ensure execution completes without Null Pointer Exceptions.
2.  **Maximum Overflow Test:** Feed an asymmetric JSON with 6 Level 1 nodes, where the first node has 10 children and the rest have 1. Verify `LayoutEngine` correctly prevents the heavy branch from colliding with neighboring branches.
3.  **Missing Field Validation:** Erase the `text_color` metadata block. Assert `WB-001` or `WB-006` properly raises.
4.  **Tree Depth Violation:** Attempt to nest a 5th level (Level 4). Assert the script raises `WB-004` to enforce the 4-level constraint limit.
