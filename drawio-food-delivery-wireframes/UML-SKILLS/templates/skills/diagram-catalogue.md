# Diagram Catalogue — Mapped to Layout Family

Every diagram type from `diagram-types-and-use-cases.md` (the master catalogue, 74 types), mapped to the layout family it should be built with (see `layout-patterns.md` for what each family means and a code sketch). A few genuinely don't fit one of the six cleanly — noted honestly rather than forced.

## 1. Project Management

| Diagram Type | Layout Family | Note |
|---|---|---|
| Gantt Chart | Timeline / Gantt | The reference case for this family |
| PERT Chart | Graph / node-edge | A DAG of task-nodes, not strictly hierarchical |
| Kanban Board | Matrix / grid | Columns are grid columns; cards stack within a column at variable heights |
| Timeline | Timeline / Gantt | Single-row simplification |
| Risk Matrix | Matrix / grid | Fixed 2D grid (likelihood × impact) |
| Milestone Chart | Timeline / Gantt | Markers only, no bars |
| Stakeholder Power/Interest Grid | Matrix / grid | Fixed 2×2 or 3×3 |
| RACI Matrix | Matrix / grid | Tasks × roles |
| Stakeholder Map | Graph / node-edge | Relationship lines between stakeholder nodes |

## 2. Architecture and Systems

| Diagram Type | Layout Family | Note |
|---|---|---|
| System Context Diagram | Graph / node-edge | Usually a small, hand-placed node set — grid layout is overkill |
| Network Diagram | Graph / node-edge | |
| Cloud Architecture Diagram | Graph / node-edge | Often grouped into regions — a light Matrix/grid for the region containers, Graph for the connections inside |
| Server Rack / Data Center Diagram | Matrix / grid | A rack is literally a grid of unit slots |
| Solution / Software Architecture Diagram | Graph / node-edge | Layered variant: rows = layers (Matrix-like), free placement within each row |

## 3. UML — Structural

| Diagram Type | Layout Family | Note |
|---|---|---|
| Class Diagram | Graph / node-edge | Each box has an internal Matrix/grid (compartments) |
| Object Diagram | Graph / node-edge | |
| Component Diagram | Graph / node-edge | |
| Deployment Diagram | Graph / node-edge | |
| Package Diagram | Tree / hierarchy | Packages usually nest |
| Composite Structure Diagram | Graph / node-edge | Parts/ports inside one classifier — small-scale node-edge |

## 4. UML — Behavioral

| Diagram Type | Layout Family | Note |
|---|---|---|
| Use Case Diagram | Graph / node-edge | |
| Sequence Diagram | Sequence / time-axis | **Proven** — see `gen_sequence_diagram_example.py` |
| Activity Diagram | Graph / node-edge | Swimlane variant when partitioned by role |
| State Machine Diagram | Graph / node-edge | States + transitions is a directed graph |
| Communication Diagram | Sequence / time-axis | Same participants as a sequence diagram, structural emphasis instead of strict time order |
| Timing Diagram | Sequence / time-axis | Explicitly time-axis based |
| Interaction Overview Diagram | Graph / node-edge | Nodes are activity-style, referencing sequence fragments |

## 5. Data and Process

| Diagram Type | Layout Family | Note |
|---|---|---|
| Data Flow Diagram (DFD) | Graph / node-edge | |
| Entity Relationship Diagram (ERD) | Graph / node-edge | Each entity has an internal Matrix/grid (attribute rows) |
| Context Diagram | Graph / node-edge | Single system + surrounding entities |
| Flowchart | Graph / node-edge | |
| Cross-Functional (Swimlane) Flowchart | Swimlane | |
| BPMN Diagram | Swimlane | Pools/lanes are the defining structure |
| Workflow Diagram | Graph / node-edge | |
| Process Map | Graph / node-edge | |
| SIPOC Diagram | Matrix / grid | Fixed 5-column layout |

## 6. Organization and Strategy

| Diagram Type | Layout Family | Note |
|---|---|---|
| Org Chart | Tree / hierarchy | The reference case for this family, alongside sitemaps |
| SWOT Matrix | Matrix / grid | Fixed 2×2 |
| BCG Matrix | Matrix / grid | Fixed 2×2 + sized bubbles |
| Ansoff Matrix | Matrix / grid | Fixed 2×2 |
| PESTEL Analysis | Matrix / grid | Fixed 6-section |
| Fishbone (Ishikawa) Diagram | Tree / hierarchy | Branches off a central spine — same subtree-width logic as an org chart, rotated |
| Gap Analysis | Matrix / grid | Two columns |
| Mind Map | Tree / hierarchy | Radial rather than strictly top-down, but the same bottom-up-width / top-down-position two-pass applies |

## 7. Web and UX Design

| Diagram Type | Layout Family | Note |
|---|---|---|
| Wireframe | Matrix / grid | Treat the page as a grid of layout regions |
| Mobile Wireframe | Matrix / grid | |
| Website Wireframe | Matrix / grid | |
| Sitemap | Tree / hierarchy | |
| User/Customer Journey Map | Timeline / Gantt | Stages are columns across a horizontal time/progress axis |
| Storyboard | Matrix / grid | Grid of scene panels |
| Interface / User Flow Diagram | Graph / node-edge | |

## 8. Business Intelligence and KPI Dashboards

**Different concern — flagged, not force-fit.** These are data visualizations (data → geometry mapping), not diagram *assembly* in the sense this skill covers.

| Diagram Type | Layout Family | Note |
|---|---|---|
| Bar / Column Chart | *Chart / data-viz* | Not a layout-assembly problem — axis scaling + bar geometry from data |
| Pie / Donut Chart | *Chart / data-viz* | Angle math from data proportions |
| Line Chart | *Chart / data-viz* | |
| Dashboard | Matrix / grid | The dashboard *shell* is a grid of chart-cells; each cell's content is chart/data-viz |
| KPI Dashboard | Matrix / grid | Same as above |
| Scorecard | Matrix / grid | |
| Pivot Diagram | Matrix / grid | |

## 9. IT Methodology and Enterprise Architecture

| Diagram Type | Layout Family | Note |
|---|---|---|
| TOGAF Diagram | Graph / node-edge | ADM cycle is often drawn as a circular graph — special-case node placement, same edge-routing rule |
| ArchiMate Diagram | Graph / node-edge | Layers give it a Matrix/grid row structure too |
| C4 Model | Tree / hierarchy | Four nested zoom levels — genuinely hierarchical |
| IDEF0 Diagram | Graph / node-edge | ICOM arrows are just typed edges |
| DMN Diagram | Graph / node-edge | |
| CMMN Diagram | Graph / node-edge | |
| CORAS Diagram | Graph / node-edge | |
| Booch Diagram | Graph / node-edge | Class-like |
| OMT Diagram | Graph / node-edge | |
| Express-G | Graph / node-edge | |

## 10. Miscellaneous and Ideation

| Diagram Type | Layout Family | Note |
|---|---|---|
| Brainstorming Diagram | Tree / hierarchy | Radial from a central bubble, same two-pass logic as a mind map |
| Decision Tree | Tree / hierarchy | The reference case, alongside org charts |
| Venn Diagram | *Geometric / set-based* | Special case — overlap area is the point, not a layout family; positions come from set-intersection math, not a cursor or stack |
| Value Stream Map | Graph / node-edge + Timeline / Gantt | Process boxes are node-edge; the timeline ladder along the bottom is a Timeline/Gantt strip |
| Fault Tree | Graph / node-edge | AND/OR gates make it a DAG, not strictly a tree despite the name |
| Floor Plan | *Freeform spatial* | Closest to Matrix/grid for room layout, but real floor plans use explicit measured coordinates, not grid-derived ones — don't force a grid where the source data is a survey/blueprint |

---

*Six families cover the overwhelming majority of the catalogue. Where a type is flagged as a different concern (BI charts) or a special case (Venn, Floor Plan), that's deliberate — forcing every diagram type into `Canvas` would be worse than naming the exception.*
