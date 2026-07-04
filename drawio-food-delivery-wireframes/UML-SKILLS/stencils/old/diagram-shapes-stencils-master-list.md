# Diagramming Shapes & Stencils — Master Reference List

Every shape and stencil category across UML, flowcharting, architecture, data/process, project management, org/strategy, UX, and BI diagrams — organized by group. Built on top of the Visio list you shared, expanded to cover UML in full, flowcharts, DFDs, BPMN, BI/KPI dashboards, sitemaps, wireframes, and a few extras. **Names only — nothing here has been created yet.** This is your build checklist.

## Table of Contents
1. [Basic and Primitive Shapes](#1-basic-and-primitive-shapes)
2. [Flowcharts (ANSI Standard)](#2-flowcharts-ansi-standard)
3. [UML Diagrams](#3-uml-diagrams)
4. [Data and Process Diagrams](#4-data-and-process-diagrams)
5. [Project Management Diagrams](#5-project-management-diagrams)
6. [Architecture and Systems Diagrams](#6-architecture-and-systems-diagrams)
7. [Organization and Strategy Diagrams](#7-organization-and-strategy-diagrams)
8. [Web and UX Design](#8-web-and-ux-design)
9. [Business Intelligence and KPI Dashboards](#9-business-intelligence-and-kpi-dashboards)
10. [IT Methodology Stencils](#10-it-methodology-stencils)
11. [Utility and Structural Shapes](#11-utility-and-structural-shapes)
12. [Miscellaneous Diagram Types](#12-miscellaneous-diagram-types)
13. [Quick Shape-Meaning Cheat Sheet](#13-quick-shape-meaning-cheat-sheet)

---

## 1. Basic and Primitive Shapes

The core building blocks reused across almost every diagram type below — including every circle variant you'll need.

- Circle, simple — generic node, connector point
- Circle, small filled/solid — UML initial state / start node
- Circle, bullseye (circle-in-circle) — UML final state
- Circle, hollow/outlined — junction pseudostate, generic node
- Circle with "X" — UML flow-final node, BPMN error marker
- Circle with "+" — OR junction, BPMN sub-process marker
- Double circle — PERT event node, BPMN alternate end-event style
- Concentric circles — wireless/signal indicator, radar/target
- Oval / ellipse — flowchart terminator, UML use case, ER attribute
- Rectangle — process step, entity, class, generic container
- Rounded rectangle — process step (soft), state, button
- Square — icon frame, small container
- Diamond / rhombus — decision, gateway, ER relationship
- Triangle, pointing up — merge, warning/alert
- Triangle, pointing down — extract, sort
- Right triangle — directional marker, play/start icon
- Parallelogram — input/output
- Trapezoid — manual operation
- Pentagon (home-plate) — off-page connector
- Hexagon — preparation step, database (alt. notation)
- Cylinder — database, storage
- Cloud — external system, internet, cloud service
- Cross / plus — add, junction, emergency marker
- X mark — delete, error, terminate
- Star — highlight, favorite, priority flag
- Arrow, straight — direction, flow, association
- Arrow, curved — loop, feedback
- Arrow, block/thick — emphasis, major flow
- Line, solid — connection, sequence
- Line, dashed — dependency, optional/weak link
- Line, dotted — extension, annotation link
- Bracket / brace — grouping, annotation

## 2. Flowcharts (ANSI Standard)

- Terminator (stadium/oval shape) — Start / End
- Process (rectangle) — process step or action
- Decision (diamond) — branch point (Yes/No)
- Input/Output (parallelogram) — data in or out
- Predefined process (rectangle, double vertical bars) — subroutine/call
- Document (rectangle, wavy bottom) — single document output
- Multi-document (stacked wavy rectangles) — multiple documents
- Manual input (rectangle, slanted top) — keyboard/manual entry
- Manual operation (trapezoid, narrow top) — manual step
- Preparation (hexagon) — setup / initialization
- On-page connector (small labeled circle) — same-page jump
- Off-page connector (pentagon/home-plate) — cross-page jump
- Delay (D-shape / half-stadium) — wait period
- Stored data (bowtie-sided rectangle) — generic stored data
- Database (cylinder) — database storage
- Display (curved-bottom screen shape) — output shown on screen
- Merge (triangle) — combine multiple flows into one
- Extract (inverted triangle) — split one flow into many
- Or (circle with "+") — logical OR junction
- Summing junction (circle with "X") — combine paths
- Loop limit (rectangle, cut top corners) — loop start/end boundary
- Direct/magnetic disk (cylinder variant) — direct-access storage
- Sequential/magnetic tape (circle with tail) — sequential storage
- Card (rectangle, cut corner) — legacy punch-card input
- Internal storage (rectangle, T-divider) — variable/memory reference
- Flow line / arrowhead — direction of flow

## 3. UML Diagrams

**Structural diagrams**

### Class Diagram
- Class box (3-compartment: name / attributes / methods)
- Interface box (`<<interface>>` stereotype)
- Abstract class box (italicized name)
- Enumeration box (`<<enumeration>>`)
- Visibility markers (+ public, − private, # protected, ~ package)
- Association line
- Directed association (open arrow)
- Aggregation (hollow diamond end)
- Composition (filled diamond end)
- Generalization / inheritance (hollow triangle arrowhead)
- Realization (dashed line, hollow triangle)
- Dependency (dashed, open arrow)
- Multiplicity label (1, 0..1, *, 1..*)
- Association class (class box on dashed tie-line)

### Object Diagram
- Object box (underlined "name : Class")
- Link line (instance-level association)

### Component Diagram
- Component box (rectangle with component icon / two tabs)
- Provided interface (lollipop)
- Required interface (socket)
- Port (small square on boundary)
- Dependency arrow
- Assembly connector (ball-and-socket pair)

### Deployment Diagram
- Node (3D box) — hardware/execution host
- Device node
- Execution environment node
- Artifact box (`<<artifact>>`, document icon)
- Communication path (line between nodes)
- Deployment dependency (dashed arrow)

### Package Diagram
- Package (folder-tab rectangle)
- Package dependency (dashed arrow)
- Nested package notation

### Composite Structure Diagram
- Part shape
- Port
- Connector
- Collaboration (dashed oval)

### Profile Diagram
- Stereotype box (`<<stereotype>>`)
- Metaclass box
- Extension relationship (filled arrow)

**Behavioral diagrams**

### Use Case Diagram
- Actor (stick figure)
- Use case (oval/ellipse)
- System boundary box
- Association line (actor–use case)
- Include relationship (dashed arrow, `<<include>>`)
- Extend relationship (dashed arrow, `<<extend>>`)
- Generalization (hollow triangle line)

### Sequence Diagram
- Lifeline (vertical dashed line)
- Lifeline head (actor figure or object box)
- Activation bar (thin rectangle on lifeline)
- Synchronous message (solid line, filled arrowhead)
- Asynchronous message (solid line, open arrowhead)
- Return message (dashed line, open arrowhead)
- Self-message (looped arrow)
- Create message (dashed arrow to new lifeline)
- Destroy message (arrow to X marker)
- Combined fragment frame (alt / opt / loop / par / break / critical / ref)
- Guard condition label
- Note/comment box

### Activity Diagram
- Initial node (filled circle)
- Activity/action (rounded rectangle)
- Decision node (diamond)
- Merge node (diamond)
- Fork bar (thick bar, split)
- Join bar (thick bar, combine)
- Activity final node (bullseye circle)
- Flow final node (circle with X)
- Object node (rectangle)
- Swimlane / partition divider
- Signal send (convex pentagon)
- Signal receive (concave pentagon)
- Time event (hourglass)

### State Machine Diagram
- Initial state (filled circle)
- State (rounded rectangle)
- Composite state (rounded rectangle, nested states)
- Transition (arrow, event/guard/action label)
- Final state (bullseye circle)
- Choice pseudostate (diamond)
- Junction pseudostate (small filled circle)
- Fork / join (bar)
- History marker (circle with H or H*)
- Entry / exit point (small circle on boundary)

### Communication Diagram
- Object/lifeline box
- Link line
- Message arrow with sequence number

### Timing Diagram
- Lifeline with state timeline
- State/value change marker
- Time ruler / axis
- Duration constraint marker

### Interaction Overview Diagram
- Activity-style nodes referencing sequence fragments
- Standard activity notation (decision, fork, join, initial/final)

## 4. Data and Process Diagrams

### Entity-Relationship (ER) Diagram
- Entity box (rectangle)
- Weak entity (double-outlined rectangle)
- Relationship diamond
- Weak relationship (double-outlined diamond)
- Attribute oval
- Key attribute (underlined oval)
- Multivalued attribute (double-outlined oval)
- Derived attribute (dashed oval)
- Composite attribute (oval with sub-ovals)
- Cardinality labels (1, N, M, 0..1, *)
- Connecting line

### Crow's Foot Notation (ER alternative)
- Entity/table box (with column list)
- One-and-only-one marker (double tick)
- Zero-or-one marker (circle + tick)
- One-or-many marker (tick + crow's foot)
- Zero-or-many marker (circle + crow's foot)

### Data Flow Diagram (DFD)
- Process (circle or rounded rectangle, numbered)
- External entity (rectangle/square)
- Data store (open-ended rectangle / parallel lines)
- Data flow (labeled arrow)
- System boundary (dashed rectangle — context-level only)

### BPMN (Business Process Model & Notation)
- Start event (thin-border circle)
- Intermediate event (double-border circle)
- End event (thick-border circle)
- Task / activity (rounded rectangle)
- Sub-process (rounded rectangle with "+")
- Exclusive gateway (diamond with X)
- Inclusive gateway (diamond with O)
- Parallel gateway (diamond with +)
- Event-based gateway (diamond with pentagon)
- Complex gateway (diamond with asterisk)
- Sequence flow (solid arrow)
- Message flow (dashed arrow, open circle tail)
- Association (dotted line)
- Pool (outer container)
- Lane (pool subdivision)
- Data object (rectangle, folded corner)
- Data store (cylinder icon)
- Text annotation (bracket + text)
- Group (rounded dashed rectangle)

### Cross-Functional / Swimlane Flowchart
- Lane header
- Lane divider
- Process box within lane
- Handoff arrow (crosses lane boundary)

## 5. Project Management Diagrams

### Gantt Chart
- Task bar
- Milestone diamond
- Summary/roll-up bar
- Dependency connector (finish-to-start, start-to-start, finish-to-finish, start-to-finish)
- Time-scale header (day/week/month)
- Task label
- Percent-complete overlay
- Resource assignment field
- Calendar grid background
- Critical-path highlight
- Baseline bar (planned vs. actual)
- Legend shapes

### PERT Chart
- PERT node (task box with time-estimate sections)
- Dynamic connector
- Start/End node (circle/oval)
- Critical-path indicator
- Time-estimate fields (optimistic / likely / pessimistic)
- Slack/float indicator

### Kanban Board
- Column header
- Card/task shape
- Card label (title, assignee, priority)
- Swimlane divider
- WIP-limit indicator
- Priority marker
- Blocked-item indicator
- In-card progress bar
- Avatar/assignee icon
- Sprint boundary marker

### Timeline
- Timeline axis bar
- Milestone marker (diamond/circle)
- Interval/period span
- Phase band
- Date label
- Collapsible section marker

### Risk Matrix
- Matrix grid (Likelihood × Impact)
- Risk cell (color-coded)
- Risk dot/plot marker
- Risk label box
- Mitigation icon (shield, warning, checkmark)
- RAG legend (Red/Amber/Green)
- Threshold boundary line
- Bow-tie shapes (hazard, controls, top event, consequences)

### Stakeholder / RACI Diagram
- Person/actor icon
- Organization-unit box
- Influence arrow
- Power/Interest grid (4-quadrant)
- RACI cell marker (R/A/C/I)
- Relationship label box
- Grouping container
- Engagement-level indicator
- Communication-frequency marker

## 6. Architecture and Systems Diagrams

### System Context / C4 Model
- Person/actor shape (rounded box + stick figure)
- Software system box
- Container box (C4 level 2)
- Component box (C4 level 3)
- Relationship arrow (labeled)
- System boundary box
- External system box (dashed/greyed)

### General Software / Solution Architecture
- Layer container (horizontal band)
- Component/module box
- Interface marker (lollipop/socket)
- Service box
- Database cylinder
- Storage icon
- Queue shape
- Message-bus bar
- Load-balancer icon
- API gateway box
- Cache shape
- Connector lines (various arrow styles)

### Network Diagram
- PC/workstation icon
- Laptop icon
- Server icon
- Router icon
- Switch icon
- Firewall icon (wall/shield)
- Access-point icon
- Server rack shape
- Cloud symbol (internet/external network)
- VPN tunnel (dashed line + padlock)
- Network segment bar
- Printer / phone / peripheral icon
- Wireless signal (concentric arcs)
- Cable-type icons (Ethernet, fiber, coax)
- Vendor-specific icon sets (Cisco, Juniper, Fortinet, Palo Alto, Dell, HPE)

### Cloud Architecture (AWS / Azure / GCP)
- Compute icon (VM, container, function)
- Storage icon (blob/object/file/block)
- Database icon (SQL, NoSQL, warehouse)
- Networking icon (VPC/VNet, subnet, load balancer, gateway)
- Security icon (IAM, firewall, KMS/encryption)
- DevOps icon (CI/CD pipeline, repo, registry)
- Monitoring/logging icon
- Integration icon (queue, event bus, API management)
- AI/ML service icon
- IoT icon (device, hub, edge gateway)
- Region / availability-zone container

### Data Center / Rack Diagram
- Rack enclosure/frame
- Server unit (1U/2U/blade)
- Patch panel
- Rack-mounted switch
- PDU (power distribution unit)
- UPS shape
- Cable management (D-ring, tray)
- Cooling unit (AC/fan)
- Front/rear elevation templates

## 7. Organization and Strategy Diagrams

### Org Chart
- Position/role box
- Department container
- Hierarchy connector line
- Photo placeholder
- Title/name label
- Dotted matrix-reporting line
- Vacant-position marker
- Legend shape

### SWOT Matrix
- 4-quadrant grid
- Quadrant label (Strengths/Weaknesses/Opportunities/Threats)
- Item box within quadrant
- Color-coded quadrant fill
- Priority indicator

### Business Matrices (BCG / Ansoff)
- BCG matrix grid (Growth vs. Share)
- Ansoff matrix grid (Markets vs. Products)
- Quadrant divider lines
- Cell fill/shading
- Bubble shape (sized by metric)
- Axis label

### Mind Map / Concept Map
- Central topic node (circle/oval)
- Branch node (rounded rectangle)
- Sub-branch node
- Curved connector line
- Icon marker
- Cross-link (dashed, between branches)

## 8. Web and UX Design

### Sitemap
- Homepage node
- Page node (rectangle)
- Subpage node
- Hierarchy connector line
- External-link marker
- Modal/popup node
- Dynamic/CMS-page marker
- Section grouping box

### Wireframe
- Header/nav bar
- Logo placeholder
- Button
- Text input field
- Text area
- Dropdown/select field
- Checkbox
- Radio button
- Toggle switch
- Image placeholder (X-box)
- Card component
- Grid/column guide
- Icon placeholder
- Footer bar
- Sidebar panel
- Breadcrumb trail
- Pagination control
- Modal/dialog box
- Tooltip
- Tab control
- Search bar
- Carousel/slider
- Avatar placeholder
- Progress/stepper indicator

### User Flow Diagram
- Screen/page node (mini wireframe rectangle)
- Decision point (diamond)
- Action/tap arrow
- Entry-point marker
- Exit/end marker
- Error-state node

### Customer Journey Map
- Stage/phase column
- Touchpoint icon
- Emotion curve line
- Persona marker
- Pain-point icon
- Opportunity icon
- Channel icon

## 9. Business Intelligence and KPI Dashboards
- KPI card/tile
- Trend arrow (up/down/flat)
- Gauge/speedometer chart
- Progress/completion bar
- Sparkline
- Bar chart
- Column chart
- Line chart
- Pie chart
- Donut chart
- Scatter plot
- Bubble chart
- Heat map
- Funnel chart
- Waterfall chart
- Treemap
- Scorecard shape
- RAG status indicator (traffic light)
- Data table grid
- Filter/slicer control
- Date-range selector
- Drill-down icon
- Legend box
- Target/benchmark line marker

## 10. IT Methodology Stencils
- TOGAF ADM cycle shapes
- ArchiMate elements (business / application / technology layers)
- C4 Model shapes (Context, Container, Component, Code)
- IDEF0 function box (with ICOM arrows: Input, Control, Output, Mechanism)
- IDEF1X entity notation
- DMN shapes (Decision, Business Knowledge Model, Input Data, Knowledge Source)
- CMMN shapes (Case File Item, Stage, Task, Milestone, Sentry)
- CORAS risk icons (threat, vulnerability, asset, treatment)
- ADAPT agile framework shapes

## 11. Utility and Structural Shapes
- Dynamic connector
- Straight connector
- Curved connector
- Right-angle/orthogonal connector
- Arrowhead styles (open, filled, diamond, circle)
- Text box
- Callout (speech-bubble/pointer)
- Sticky note
- Legend box
- Numbered step marker
- Grouping/container rectangle
- Layer container
- Swimlane (horizontal/vertical)
- Frame/boundary box

## 12. Miscellaneous Diagram Types
- Fishbone/Ishikawa diagram (spine, bone branches, cause boxes, effect head)
- Decision tree (root node, branch line, leaf/outcome node, probability label)
- Venn diagram (overlapping circles, intersection label)
- Value stream map (process box, inventory triangle, data box, timeline ladder)
- Fault tree (event box, AND gate, OR gate, basic event circle)

## 13. Quick Shape-Meaning Cheat Sheet

| Shape | Common Meaning(s) |
|---|---|
| Oval / stadium shape | Start / End (terminator) |
| Rectangle | Process step, entity, class |
| Diamond | Decision, gateway, ER relationship |
| Parallelogram | Input / Output |
| Small filled circle | Initial/start state (UML) |
| Bullseye circle | Final state (UML) |
| Cylinder | Database / storage |
| Cloud | External system / internet |
| Hexagon | Preparation step |
| Pentagon | Off-page connector |
| Stick figure | Actor / user / person |
| Lollipop / socket | Provided / required interface |
| Hollow triangle arrowhead | Inheritance / generalization |
| Filled diamond (line end) | Composition |
| Hollow diamond (line end) | Aggregation |

---

*This is a naming/checklist reference only — nothing has been built yet. Built on top of the Visio stencil list you shared, expanded to cover all 14 UML diagram types, flowcharts, DFDs, BPMN, BI/KPI dashboards, sitemaps, wireframes, and a handful of extras (fishbone, decision tree, Venn, VSM, fault tree).*
