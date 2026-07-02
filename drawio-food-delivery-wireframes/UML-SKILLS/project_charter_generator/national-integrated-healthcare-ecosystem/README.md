# NIHE Project Charter — Input File Set

**Project:** National Integrated Healthcare Ecosystem (NIHE)
**Sponsor:** Ministry of Health, Uganda
**Version:** 1.1 (expanded)

This package contains all 16 Project Charter Generator input files, located in
`inputs/`, ready to be merged and built into the final Word document and Visio
deck.

## What's in here

| # | File | Purpose |
|---|------|---------|
| 1 | `charter_project_input.json` | Project header (name, sponsor, dates, classification, methodology) |
| 2 | `charter_content_input.json` | Vision, 9 objectives, scope, 9 constraints, 8 assumptions, 13 success criteria, budget, 5 approvals |
| 3 | `charter_people_input.json` | 12 stakeholders + 14-person team |
| 4 | `charter_schedule_risk_input.json` | 11 risks + 10 milestones |
| 5 | `charter_diagram_problem_tree_input.json` | Problem tree (Graphviz) — 7 problem branches |
| 6 | `charter_diagram_stakeholder_matrix_input.json` | Stakeholder power-interest matrix (Graphviz) |
| 7 | `charter_diagram_scope_boundary_input.json` | Scope boundary diagram (Graphviz) |
| 8 | `charter_diagram_org_chart_input.json` | Org chart (Graphviz) — 14 roles |
| 9 | `charter_diagram_milestone_timeline_input.json` | Milestone timeline (Graphviz) — 10 milestones |
| 10 | `charter_diagram_risk_matrix_input.json` | Risk matrix (Graphviz) — 11 risks plotted |
| 11 | `charter_diagram_system_context_input.json` | System context diagram (Graphviz) |
| 12 | `charter_word_styling_input.json` | Word styling: fonts, color theme, cover page, header/footer |
| 13 | `charter_visio_diagrams_input.json` | Visio overrides + deck settings |
| 14 | `charter_word_input.json` | **Word MAIN** — merge of files 1–4, 12 + all 7 diagrams |
| 15 | `charter_visio_input.json` | **Visio MAIN** — merge of files 1–4 + diagrams + deck settings |
| 16 | `charter_input.json` | **Combined MAIN** — everything in one file |

All cross-references have been validated programmatically: budget breakdown
sums to the $1,250,000 total; milestone, risk, stakeholder, and team IDs match
1:1 between the data files and their corresponding diagram node IDs.

## What was expanded vs. the original draft

- **Objectives:** added OBJ-08 (security & privacy) and OBJ-09 (workforce capacity building)
- **Constraints:** added multi-language support and PPDA procurement compliance
- **Assumptions:** added power/data-center reliability and post-launch funding continuity
- **Success criteria:** added security, certification, and help-desk SLAs
- **Budget:** broken into 11 granular line items (was 6) — same $1,250,000 total
- **Stakeholders:** added development partners/donors, civil society & patient advocacy, pharmaceutical suppliers (12 total, was 9)
- **Team:** added Security Lead, Data Protection Officer, Training Lead, M&E Lead, Procurement Lead (14 roles, was 9)
- **Risks:** added cybersecurity, key-personnel attrition, vendor lock-in, and data-migration quality (11 total, was 7)
- **Milestones:** added a Security & Compliance Certification gate and a Post-Go-Live Stabilization & Handover milestone (10 total, was 8); project end date extended to **2028-09-30** to accommodate the hypercare/handover period
- **Diagrams:** every diagram updated to reflect the new branches/nodes/roles above (problem tree gained a "Workforce Capacity Gaps" branch; org chart gained 5 nodes; risk matrix gained 4 risk nodes; etc.)
- **Word & Visio styling:** added color theme, cover page, header/footer, and appendix section list

## Next steps

1. Files are already placed at `national-integrated-healthcare-ecosystem/inputs/`
   matching the directory convention from your generator.

2. **Merge:**
   ```bash
   python project_charter_generator/cli.py merge national-integrated-healthcare-ecosystem/inputs --validate
   ```

3. **Build:**
   ```bash
   python project_charter_generator/cli.py build national-integrated-healthcare-ecosystem/inputs/charter_input.json -o national-integrated-healthcare-ecosystem/output
   ```

4. **Expected output:**
   - `output/project-charter.docx` — Word document with native editable DrawingML shape diagrams
   - `output/visio/project-charter.vsdx` — Visio deck (via Aspose.Diagram)

> Note: files 14–16 are pre-merged for convenience, duplicating content from
> files 1–13. If your `merge` command regenerates these automatically, you can
> treat files 14–16 as a working reference/fallback, or delete them before
> running `merge` to avoid overwrite conflicts — whichever matches how your
> `cli.py` expects the `inputs/` folder to be structured.
