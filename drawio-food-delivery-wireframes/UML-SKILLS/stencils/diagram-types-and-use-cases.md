# Diagram Types & Use-Case Reference — The Arsenal, Part 2

Companion to `diagram-shapes-stencils-master-list.md`. That file is the shape library; this one is the catalogue of *diagram types* — what each one is for, and when to reach for it. Deduped and generic (no project-specific content). "Key Shapes" columns are a quick pointer only — full shape breakdowns live in the companion file.

## Table of Contents
1. [Project Management Diagrams](#1-project-management-diagrams)
2. [Architecture and Systems Diagrams](#2-architecture-and-systems-diagrams)
3. [UML Diagrams](#3-uml-diagrams)
4. [Data and Process Diagrams](#4-data-and-process-diagrams)
5. [Organization and Strategy Diagrams](#5-organization-and-strategy-diagrams)
6. [Web and UX Design](#6-web-and-ux-design)
7. [Business Intelligence and KPI Dashboards](#7-business-intelligence-and-kpi-dashboards)
8. [IT Methodology and Enterprise Architecture](#8-it-methodology-and-enterprise-architecture)
9. [Miscellaneous and Ideation Diagrams](#9-miscellaneous-and-ideation-diagrams)
10. [Quick Index — All Diagram Types by Category](#10-quick-index--all-diagram-types-by-category)

---

## 1. Project Management Diagrams

| Diagram Type | Purpose | Key Shapes | When to Use |
|---|---|---|---|
| Gantt Chart | Plan and monitor project schedules over time | Task bars, milestone diamonds, dependency connectors | Tracking timelines, showing dependencies, reporting schedule to stakeholders |
| PERT Chart | Map task dependencies and find the critical path | PERT nodes, dynamic connectors, critical-path indicators | Complex projects with many dependencies; critical-path analysis |
| Kanban Board | Visualize workflow and work-in-progress | Column headers, cards, swimlanes, WIP-limit markers | Agile projects, continuous delivery, WIP tracking |
| Timeline | Show events/milestones in chronological order | Timeline bar, milestone markers, phase bands | Roadmaps, historical overviews, milestone tracking |
| Risk Matrix | Assess and prioritize risks by likelihood × impact | Grid, risk cells, risk dots, mitigation icons | Risk management, project planning, stakeholder reporting |
| Milestone Chart | Track key milestones at a glance | Diamond markers, date markers, completion indicators | Status reporting, executive summaries |
| Stakeholder Power/Interest Grid | Map stakeholder influence vs. interest | 2×2 or 3×3 grid, stakeholder dots, priority zones | Stakeholder analysis, engagement strategy, change management |
| RACI Matrix | Clarify who is Responsible, Accountable, Consulted, Informed | Tasks-by-roles grid, R/A/C/I markers | Role clarity, governance, project kickoff |
| Stakeholder Map | Visualize relationships and influence between stakeholders | Stakeholder nodes, relationship lines | Communication planning, relationship management |

## 2. Architecture and Systems Diagrams

| Diagram Type | Purpose | Key Shapes | When to Use |
|---|---|---|---|
| System Context Diagram | Define a system's boundary and external interactions | Central system box, external entities, boundary line | Initial scoping, stakeholder communication |
| Network Diagram | Document IT infrastructure and connections | PCs, routers/switches/firewalls, server racks, cloud symbols | Infrastructure documentation, planning, troubleshooting |
| Cloud Architecture Diagram | Show cloud service architecture | Cloud service icons, compute/storage/networking shapes | Cloud infra design, service integration, deployment planning |
| Server Rack / Data Center Diagram | Document physical data-center layout | Rack shapes, device units, patch panels, cable management | Data-center planning, hardware documentation, capacity planning |
| Solution / Software Architecture Diagram | Show system components, layers, and how they connect | Layer containers, service boxes, DB cylinders, load balancers | Solution design, technical documentation, architecture review |

## 3. UML Diagrams

### Structural

| Diagram Type | Purpose | Key Shapes | When to Use |
|---|---|---|---|
| Class Diagram | Model system structure via classes and relationships | Class boxes, inheritance/association connectors | OO design, structure documentation |
| Object Diagram | Snapshot of specific object instances and their links | Object boxes, link lines | Illustrating a class diagram with a concrete example |
| Component Diagram | Show component structure and dependencies | Component boxes, lollipop/socket interfaces | Architecture, API design, dependency mapping |
| Deployment Diagram | Map software to physical/virtual hardware | Node shapes, artifacts, communication paths | Infra planning, deployment architecture, cloud design |
| Package Diagram | Organize model elements into namespaces | Package (folder-tab) shapes, dependency arrows | Large systems, module/namespace organization |
| Composite Structure Diagram | Show a classifier's internal structure at runtime | Parts, ports, connectors | Detailed internal-collaboration modeling |

### Behavioral

| Diagram Type | Purpose | Key Shapes | When to Use |
|---|---|---|---|
| Use Case Diagram | Model system functionality from the user's perspective | Actors, use-case ovals, include/extend arrows | Requirements analysis, scope definition |
| Sequence Diagram | Show interactions between objects over time | Lifelines, activation bars, messages, fragments | Use-case scenarios, detailed interaction design |
| Activity Diagram | Model workflow and control/object flow | Start/end nodes, decision/fork/join nodes, swimlanes | Workflow modeling, parallel processes, process detail |
| State Machine Diagram | Show states and transitions for an object/system | States, transitions, guards, entry/exit actions | Object lifecycle, state-dependent behavior |
| Communication Diagram | Show object interactions with a structural emphasis | Objects, links, numbered message arrows | Structure + interaction combined view |
| Timing Diagram | Show state/value changes across a time axis | Lifelines, state bands, time ruler | Real-time or timing-sensitive systems |
| Interaction Overview Diagram | Show control flow between multiple interaction fragments | Activity nodes referencing sequence fragments | High-level view across many related scenarios |

## 4. Data and Process Diagrams

| Diagram Type | Purpose | Key Shapes | When to Use |
|---|---|---|---|
| Data Flow Diagram (DFD) | Show how data moves through a system | Processes, data stores, external entities, flow arrows | Data-movement analysis, system design |
| Entity Relationship Diagram (ERD) | Model database structure and relationships | Entities, relationship diamonds, attributes, cardinality | Database design, data modeling |
| Context Diagram | Show a system and its external interactions at the highest level | System box, external entities, boundary | High-level scoping, architecture kickoff |
| Flowchart | Document and analyze a process step by step | Process/decision/terminator shapes, arrows | Process documentation, training, SOPs |
| Cross-Functional (Swimlane) Flowchart | Show process flow across roles/teams | Lanes, activity boxes, handoff arrows | Multi-department processes, handoffs |
| BPMN Diagram | Model business processes in detail, including events and gateways | Events, gateways, tasks, pools, lanes | Complex business processes, process improvement |
| Workflow Diagram | Document task sequences and decision points | Task nodes, decision diamonds, branch arrows | Task automation, SOP documentation |
| Process Map | Show high-level business processes and interactions | Process nodes, connector arrows, I/O markers | Business-process overview, strategic planning |
| SIPOC Diagram | High-level process mapping (Supplier–Input–Process–Output–Customer) | 5-column layout, process flow | Six Sigma, process-improvement kickoff |

## 5. Organization and Strategy Diagrams

| Diagram Type | Purpose | Key Shapes | When to Use |
|---|---|---|---|
| Org Chart | Visualize company/reporting structure | Position boxes, hierarchy lines, dotted matrix lines | HR planning, role definition |
| SWOT Matrix | Analyze Strengths, Weaknesses, Opportunities, Threats | 4-quadrant grid, item boxes | Strategic planning, business review |
| BCG Matrix | Analyze product portfolio (market growth vs. share) | 2×2 grid, sized bubbles | Portfolio and investment strategy |
| Ansoff Matrix | Analyze growth strategy (markets vs. products) | 2×2 grid, quadrant labels | Growth planning, market/product expansion |
| PESTEL Analysis | Analyze external macro-environmental factors | 6-section grid, factor lists | Environmental scanning, market entry |
| Fishbone (Ishikawa) Diagram | Identify root causes of a problem | Spine, category branches, cause labels | Root-cause analysis, quality improvement |
| Gap Analysis | Identify gaps between current and desired state | Two-column comparison, gap indicators | Process improvement, resource planning |
| Mind Map | Visualize ideas branching from a central concept | Central node, branch/sub-branch nodes | Brainstorming, idea organization |

## 6. Web and UX Design

| Diagram Type | Purpose | Key Shapes | When to Use |
|---|---|---|---|
| Wireframe | Prototype interface layout before visual design/coding | Page containers, input fields, buttons, nav elements | Early UI design, user testing |
| Mobile Wireframe | Prototype a mobile app's interface | Device frames, touch controls, cards | Mobile app design |
| Website Wireframe | Prototype a website's layout | Browser frame, nav menu, content areas | Web development, information architecture |
| Sitemap | Show a site/app's page hierarchy | Homepage/page nodes, hierarchy lines | IA planning, navigation design |
| User/Customer Journey Map | Map user experience across touchpoints and emotions | Stage columns, touchpoint icons, emotion curve | UX design, service design |
| Storyboard | Visualize user interactions as a sequence of scenes | Scene frames, character icons, captions | Scenario design, interaction narrative |
| Interface / User Flow Diagram | Show navigation paths through screens | Page/screen nodes, decision points, action arrows | UX design, usability testing |

## 7. Business Intelligence and KPI Dashboards

| Diagram Type | Purpose | Key Shapes | When to Use |
|---|---|---|---|
| Bar / Column Chart | Compare values across categories | Bars, axes, gridlines | Data comparison, reporting |
| Pie / Donut Chart | Show proportion of parts to a whole | Slices, legend | Composition analysis, market share |
| Line Chart | Show trends over time | Line, data points, axes | Time-series analysis, forecasting |
| Dashboard | Combine multiple visuals for at-a-glance monitoring | KPI tiles, charts, status colors | Executive reporting, real-time monitoring |
| KPI Dashboard | Track key performance indicators | Scorecards, RAG indicators, trend arrows | Performance management |
| Scorecard | Track performance against targets | Grid, RAG status, target markers | Balanced-scorecard tracking |
| Pivot Diagram | Explore data relationships dynamically (data-linked) | Data-linked shapes, linked cube/database | BI exploration, live dashboards |

## 8. IT Methodology and Enterprise Architecture

| Diagram Type | Purpose | Key Shapes | When to Use |
|---|---|---|---|
| TOGAF Diagram | Model enterprise architecture per the TOGAF ADM | ADM-cycle shapes, capability map | Enterprise architecture, IT transformation |
| ArchiMate Diagram | Model enterprise architecture across business/app/tech layers | Layer-specific elements, relationship arrows | EA modeling, EA governance |
| C4 Model | Show software architecture at 4 zoom levels | Context, container, component, code diagrams | Multi-level technical documentation |
| IDEF0 Diagram | Model functions with inputs/controls/outputs/mechanisms | Function boxes, ICOM arrows | Process/function modeling |
| DMN Diagram | Model business decisions and decision logic | Decision, BKM, input-data, knowledge-source shapes | Decision modeling alongside BPMN |
| CMMN Diagram | Model case-management, event-driven work | Case file items, stages, tasks, milestones, sentries | Case-based/knowledge-work processes |
| CORAS Diagram | Model security/risk threats visually | Threat, vulnerability, asset, treatment icons | Risk and security analysis |
| Booch Diagram | Object-oriented design (legacy notation) | Class boxes, relationship connectors | OOAD, early-stage design |
| OMT Diagram | Object-oriented analysis (legacy notation) | Object, dynamic, and functional models | OOA, early-stage design |
| Express-G | Data modeling notation for engineering/manufacturing data | Entity/attribute boxes, relationship shapes | Data-model design (STEP/ISO 10303 contexts) |

## 9. Miscellaneous and Ideation Diagrams

| Diagram Type | Purpose | Key Shapes | When to Use |
|---|---|---|---|
| Brainstorming Diagram | Record and connect related ideas | Central bubble, idea nodes, connectors | Ideation sessions, problem solving |
| Decision Tree | Map decisions and their possible outcomes | Root/branch/leaf nodes | Decision analysis, probability modeling |
| Venn Diagram | Show overlap between sets or categories | Overlapping circles | Comparison, logical relationships |
| Value Stream Map | Map material/info flow in a lean process | Process boxes, inventory triangles, timeline ladder | Lean/Six Sigma process improvement |
| Fault Tree | Model failure paths using logic gates | Event boxes, AND/OR gates | Reliability and safety analysis |
| Floor Plan | Design spatial/office layouts | Walls, doors, furniture, room labels | Office or event space planning |

## 10. Quick Index — All Diagram Types by Category

| Category | Diagram Types |
|---|---|
| Project Management | Gantt Chart, PERT Chart, Kanban Board, Timeline, Risk Matrix, Milestone Chart, Power/Interest Grid, RACI Matrix, Stakeholder Map |
| Architecture & Systems | System Context, Network Diagram, Cloud Architecture, Server Rack/Data Center, Solution Architecture |
| UML — Structural | Class, Object, Component, Deployment, Package, Composite Structure |
| UML — Behavioral | Use Case, Sequence, Activity, State Machine, Communication, Timing, Interaction Overview |
| Data & Process | DFD, ERD, Context Diagram, Flowchart, Cross-Functional Flowchart, BPMN, Workflow Diagram, Process Map, SIPOC |
| Organization & Strategy | Org Chart, SWOT, BCG Matrix, Ansoff Matrix, PESTEL, Fishbone, Gap Analysis, Mind Map |
| Web & UX | Wireframe, Mobile Wireframe, Website Wireframe, Sitemap, Journey Map, Storyboard, User Flow |
| BI & KPI | Bar/Column Chart, Pie/Donut Chart, Line Chart, Dashboard, KPI Dashboard, Scorecard, Pivot Diagram |
| IT Methodology | TOGAF, ArchiMate, C4 Model, IDEF0, DMN, CMMN, CORAS, Booch, OMT, Express-G |
| Misc / Ideation | Brainstorming, Decision Tree, Venn Diagram, Value Stream Map, Fault Tree, Floor Plan |

---

*74 diagram types across 9 working categories. Pairs with `diagram-shapes-stencils-master-list.md` — use that file for the shape inventory, this one for picking the right diagram and knowing why.*
