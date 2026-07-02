"""
diagrams/layouts.py
────────────────────
Six layout functions — one per diagram type.
Each returns a structured dict of { nodes: [...], edges: [...] }
which is consumed by both the dot_generator (logging) and the
aspose_renderer (Visio shape placement).
"""
from typing import Dict, Any, List


# ── Constants ────────────────────────────────────────────────────────────────

TIER_COLORS = {
    "root":   {"fill": "#EF9A9A", "border": "#E53935", "text": "#B71C1C"},
    "trunk":  {"fill": "#FFCC80", "border": "#F57C00", "text": "#E65100"},
    "branch": {"fill": "#90CAF9", "border": "#1565C0", "text": "#0D47A1"},
    "leaf":   {"fill": "#A5D6A7", "border": "#2E7D32", "text": "#1B5E20"},
}

QUADRANT_STYLES = {
    ("High", "High"): {"fill": "#FFCDD2", "label": "KEY PLAYERS\n(Manage Closely)"},
    ("High", "Low"):  {"fill": "#FFE0B2", "label": "KEEP SATISFIED"},
    ("Low",  "High"): {"fill": "#FFF9C4", "label": "KEEP INFORMED"},
    ("Low",  "Low"):  {"fill": "#C8E6C9", "label": "MONITOR"},
}

RISK_COLORS = {
    "critical": "#E53935",
    "high":     "#FF7043",
    "medium":   "#FFC107",
    "low":      "#66BB6A",
}


# ── 1. Problem Tree ───────────────────────────────────────────────────────────

def layout_problem_tree(payload: Dict) -> Dict:
    """4-tier hierarchical layout: ROOT → TRUNK → BRANCH → LEAF."""
    nodes, edges = [], []

    # TRUNK
    cp = payload.get("core_problem", {
        "id": "TRUNK",
        "statement": payload.get("vision", {}).get("statement", "Core Problem")
    })
    nodes.append({"id": "TRUNK", "tier": "trunk", "text": cp.get("statement", ""),
                  "x": 12.0, "y": 5.5, "w": 8.0, "h": 1.6,
                  **TIER_COLORS["trunk"]})

    # ROOTS — risks serve as root causes when no explicit roots defined
    risks = payload.get("risks", [])[:5]
    root_xs = _spread_xs(len(risks), 2.0, 24.0)
    for i, r in enumerate(risks):
        nid = r["id"]
        nodes.append({"id": nid, "tier": "root",
                      "text": f"{r['id']}: {r['description']}",
                      "x": root_xs[i], "y": 2.0, "w": 3.8, "h": 1.4,
                      **TIER_COLORS["root"]})
        edges.append({"from": nid, "to": "TRUNK", "color": "#666666"})

    # BRANCHES — objectives become direct effects
    objs = payload.get("objectives", [])[:4]
    branch_xs = _spread_xs(len(objs), 2.0, 24.0)
    for i, o in enumerate(objs):
        nid = o["id"]
        nodes.append({"id": nid, "tier": "branch",
                      "text": f"{o['id']}: {o['description']}",
                      "x": branch_xs[i], "y": 8.5, "w": 4.5, "h": 1.4,
                      **TIER_COLORS["branch"]})
        edges.append({"from": "TRUNK", "to": nid, "color": "#666666"})

    # LEAF — success criteria
    sc = payload.get("success_criteria", [])[:3]
    leaf_xs = _spread_xs(len(sc), 2.0, 24.0)
    for i, s in enumerate(sc):
        nid = f"L{i+1}"
        nodes.append({"id": nid, "tier": "leaf",
                      "text": s,
                      "x": leaf_xs[i], "y": 11.5, "w": 5.5, "h": 1.4,
                      **TIER_COLORS["leaf"]})
        for o in objs:
            edges.append({"from": o["id"], "to": nid, "color": "#666666"})

    return {"nodes": nodes, "edges": edges, "title": "Problem Tree"}


# ── 2. Stakeholder Power-Interest Matrix ──────────────────────────────────────

def layout_stakeholder_matrix(payload: Dict) -> Dict:
    """2×2 Power/Interest grid."""
    nodes, edges = [], []
    page_cx, page_cy = 12.0, 7.5
    q_w, q_h = 9.0, 5.5

    nodes.append({"id": "TITLE_Y", "tier": "axis_label",
                  "text": "POWER →", "x": 0.8, "y": page_cy, "w": 1.2, "h": 4.0,
                  "fill": "#FFFFFF", "border": "#FFFFFF", "text_color": "#546E7A"})
    nodes.append({"id": "TITLE_X", "tier": "axis_label",
                  "text": "INTEREST →", "x": page_cx, "y": 13.2, "w": 8.0, "h": 0.5,
                  "fill": "#FFFFFF", "border": "#FFFFFF", "text_color": "#546E7A"})

    # Background quadrant boxes
    for (power, interest), style in QUADRANT_STYLES.items():
        qx = page_cx + (q_w / 2 if interest == "High" else -q_w / 2)
        qy = page_cy + (q_h / 2 if power == "High" else -q_h / 2)
        qid = f"Q_{power}_{interest}"
        nodes.append({"id": qid, "tier": "quadrant",
                      "text": style["label"],
                      "x": qx, "y": qy, "w": q_w, "h": q_h,
                      "fill": style["fill"], "border": "#BDBDBD", "text": style["label"]})

    # Place stakeholders inside their quadrant
    quad_occupancy: Dict[tuple, int] = {}
    for sh in payload.get("stakeholders", []):
        key = (sh.get("power", "Low"), sh.get("interest", "Low"))
        count = quad_occupancy.get(key, 0)
        qx = page_cx + (q_w / 2 if key[1] == "High" else -q_w / 2)
        qy = page_cy + (q_h / 2 if key[0] == "High" else -q_h / 2)
        sx = qx - 1.5 + (count % 2) * 3.0
        sy = qy + 1.0 - (count // 2) * 1.5
        nodes.append({"id": sh["id"], "tier": "stakeholder",
                      "text": f"{sh['name']}\n{sh.get('role', '')}",
                      "x": sx, "y": sy, "w": 3.0, "h": 1.0,
                      "fill": "#FFFFFF", "border": "#1565C0", "text_color": "#0D47A1"})
        quad_occupancy[key] = count + 1

    # Legend
    nodes.append({"id": "LEGEND", "tier": "note",
                  "text": "■ Key Players  ■ Keep Satisfied  ■ Keep Informed  ■ Monitor",
                  "x": 20.5, "y": 12.8, "w": 6.5, "h": 0.6,
                  "fill": "#FAFAFA", "border": "#BDBDBD", "text_color": "#424242"})

    return {"nodes": nodes, "edges": edges, "title": "Stakeholder Power-Interest Matrix"}


# ── 3. Milestone Timeline ─────────────────────────────────────────────────────

def layout_milestone_timeline(payload: Dict) -> Dict:
    """Horizontal left-to-right timeline with milestone diamonds."""
    nodes, edges = [], []
    milestones = payload.get("milestones", [])
    n = len(milestones)
    if n == 0:
        return {"nodes": nodes, "edges": edges, "title": "Milestone Timeline"}

    timeline_y = 6.0
    margin = 1.5
    page_w = 24.0
    span = page_w - (2 * margin)
    spacing = span / max(n - 1, 1)

    # Spine
    nodes.append({"id": "SPINE", "tier": "axis",
                  "text": "", "x": page_w / 2, "y": timeline_y,
                  "w": span, "h": 0.05,
                  "fill": "#1565C0", "border": "#1565C0", "text_color": "#FFFFFF"})

    # Phase bands below spine
    phases = ["Initiation", "Design", "Build", "Deploy"]
    phase_w = span / len(phases)
    for i, ph in enumerate(phases):
        px = margin + i * phase_w + phase_w / 2
        nodes.append({"id": f"PH_{i}", "tier": "phase",
                      "text": ph, "x": px, "y": timeline_y - 1.2,
                      "w": phase_w * 0.9, "h": 0.5,
                      "fill": "#E3F2FD", "border": "#1565C0", "text_color": "#0D47A1"})

    toggle = True
    for i, m in enumerate(milestones):
        x = margin + i * spacing
        y_offset = 2.0 if toggle else -2.0
        my = timeline_y + y_offset
        color = "#E53935" if m.get("is_critical") else "#1565C0"

        # Diamond marker
        nodes.append({"id": m["id"], "tier": "milestone",
                      "text": f"{m['date']}\n{m['name']}",
                      "x": x, "y": my, "w": 0.6, "h": 0.6,
                      "fill": color, "border": color, "text_color": "#FFFFFF"})

        # Leader line
        edges.append({"from": "SPINE", "to": m["id"], "color": "#999999"})
        toggle = not toggle

    nodes.append({"id": "LEGEND", "tier": "note",
                  "text": "● Milestone   │ Phase band   — Red = critical",
                  "x": 3.5, "y": 12.5, "w": 6.0, "h": 0.5,
                  "fill": "#FAFAFA", "border": "#BDBDBD", "text_color": "#424242"})

    return {"nodes": nodes, "edges": edges, "title": "Milestone Timeline"}


# ── 4. Scope Boundary ─────────────────────────────────────────────────────────

def layout_scope_boundary(payload: Dict) -> Dict:
    """Concentric in-scope (green) / out-of-scope (red) layout."""
    nodes, edges = [], []
    scope = payload.get("scope", {})
    in_scope = scope.get("in_scope", [])
    out_scope = scope.get("out_of_scope", [])

    # Outer boundary box
    nodes.append({"id": "OUTER", "tier": "out_scope",
                  "text": "OUT OF SCOPE", "x": 12.0, "y": 8.0,
                  "w": 20.0, "h": 12.0,
                  "fill": "#FFEBEE", "border": "#E53935", "text_color": "#B71C1C"})

    # Inner in-scope box
    nodes.append({"id": "INNER", "tier": "in_scope",
                  "text": "IN SCOPE", "x": 12.0, "y": 8.0,
                  "w": 12.0, "h": 7.0,
                  "fill": "#E8F5E9", "border": "#2E7D32", "text_color": "#1B5E20"})

    # In-scope items
    for i, item in enumerate(in_scope):
        nid = f"IN_{i}"
        nodes.append({"id": nid, "tier": "in_item",
                      "text": item, "x": 9.0 + (i % 2) * 4.0, "y": 7.0 - (i // 2) * 1.3,
                      "w": 3.5, "h": 1.0,
                      "fill": "#C8E6C9", "border": "#2E7D32", "text_color": "#1B5E20"})

    # Out-of-scope items
    out_positions = [(3.0, 12.5), (3.0, 10.5), (21.0, 12.5), (21.0, 10.5)]
    for i, item in enumerate(out_scope[:4]):
        nid = f"OUT_{i}"
        x, y = out_positions[i] if i < len(out_positions) else (3.0 + i * 2, 5.0)
        nodes.append({"id": nid, "tier": "out_item",
                      "text": item, "x": x, "y": y,
                      "w": 3.5, "h": 1.0,
                      "fill": "#FFCDD2", "border": "#E53935", "text_color": "#B71C1C"})

    nodes.append({"id": "LEGEND", "tier": "note",
                  "text": "■ In Scope (green)   ■ Out of Scope (red)",
                  "x": 20.0, "y": 12.8, "w": 6.0, "h": 0.5,
                  "fill": "#FAFAFA", "border": "#BDBDBD", "text_color": "#424242"})

    return {"nodes": nodes, "edges": edges, "title": "Scope Boundary"}


# ── 5. Org Chart ──────────────────────────────────────────────────────────────

def layout_org_chart(payload: Dict) -> Dict:
    """Hierarchical top-down org chart from team members."""
    nodes, edges = [], []
    project = payload.get("project", {})
    team = payload.get("team", [])

    # If no explicit team, synthesise from project metadata
    if not team:
        team = [
            {"id": "SPONSOR", "name": project.get("sponsor", "Sponsor"), "role": "Project Sponsor", "reports_to": None},
            {"id": "PM",      "name": project.get("manager", "Manager"), "role": "Project Manager",  "reports_to": "SPONSOR"},
        ]

    # Build lookup
    member_map = {m["id"]: m for m in team}

    # Calculate layout layers
    layers: Dict[str, int] = {}
    for m in team:
        if m.get("reports_to") is None:
            layers[m["id"]] = 0

    changed = True
    while changed:
        changed = False
        for m in team:
            rt = m.get("reports_to")
            if rt and rt in layers and m["id"] not in layers:
                layers[m["id"]] = layers[rt] + 1
                changed = True

    layer_members: Dict[int, List] = {}
    for mid, layer in layers.items():
        layer_members.setdefault(layer, []).append(mid)

    LAYER_COLORS = ["#1565C0", "#1976D2", "#64B5F6", "#BBDEFB"]
    page_w = 24.0

    for layer_idx, mids in sorted(layer_members.items()):
        n = len(mids)
        xs = _spread_xs(n, 2.0, page_w)
        y = 10.0 - layer_idx * 2.2
        color = LAYER_COLORS[min(layer_idx, len(LAYER_COLORS) - 1)]
        text_c = "#FFFFFF" if layer_idx < 2 else "#1a237e"

        for i, mid in enumerate(mids):
            m = member_map.get(mid, {"name": mid, "role": ""})
            nodes.append({"id": mid, "tier": "member",
                          "text": f"{m['name']}\n{m.get('role', '')}",
                          "x": xs[i], "y": y, "w": 3.5, "h": 1.0,
                          "fill": color, "border": color, "text_color": text_c})
            rt = m.get("reports_to")
            if rt:
                edges.append({"from": rt, "to": mid, "color": "#666666"})

    return {"nodes": nodes, "edges": edges, "title": "Project Org Chart"}


# ── 6. Risk Matrix ────────────────────────────────────────────────────────────

def layout_risk_matrix(payload: Dict) -> Dict:
    """5×5 Impact vs Likelihood heatmap with risk bubbles."""
    nodes, edges = [], []
    risks = payload.get("risks", [])

    nodes.append({"id": "AXIS_L", "tier": "axis_label",
                  "text": "LIKELIHOOD ↑", "x": 0.6, "y": 7.0, "w": 0.8, "h": 6.0,
                  "fill": "#FFFFFF", "border": "#FFFFFF", "text_color": "#546E7A"})
    nodes.append({"id": "AXIS_I", "tier": "axis_label",
                  "text": "IMPACT →", "x": 9.0, "y": 0.8, "w": 8.0, "h": 0.5,
                  "fill": "#FFFFFF", "border": "#FFFFFF", "text_color": "#546E7A"})

    # Grid header labels
    for i in range(1, 6):
        nodes.append({"id": f"LH_{i}", "tier": "axis_label",
                      "text": str(i), "x": 3.0 + i * 2.5, "y": 1.5,
                      "w": 2.0, "h": 0.6,
                      "fill": "#E0E0E0", "border": "#9E9E9E", "text_color": "#000000"})
        nodes.append({"id": f"IMP_{i}", "tier": "axis_label",
                      "text": str(i), "x": 1.5, "y": 2.5 + (5 - i) * 1.5,
                      "w": 1.2, "h": 0.6,
                      "fill": "#E0E0E0", "border": "#9E9E9E", "text_color": "#000000"})

    # Heatmap cells
    for imp in range(1, 6):
        for lh in range(1, 6):
            score = imp * lh
            color = ("#E53935" if score >= 15 else
                     "#FF7043" if score >= 9 else
                     "#FFC107" if score >= 4 else "#66BB6A")
            nodes.append({"id": f"CELL_{imp}_{lh}", "tier": "cell",
                          "text": "",
                          "x": 3.0 + lh * 2.5, "y": 2.5 + (5 - imp) * 1.5,
                          "w": 2.4, "h": 1.4,
                          "fill": color + "55", "border": color, "text_color": "#000000"})

    # Risk bubbles
    for r in risks:
        lh = max(1, min(5, int(r.get("likelihood", 1))))
        imp = max(1, min(5, int(r.get("impact", 1))))
        score = lh * imp
        color = ("#E53935" if score >= 15 else
                 "#FF7043" if score >= 9 else
                 "#FFC107" if score >= 4 else "#66BB6A")
        nodes.append({"id": r["id"], "tier": "risk",
                      "text": r["id"],
                      "x": 3.0 + lh * 2.5, "y": 2.5 + (5 - imp) * 1.5,
                      "w": 1.0, "h": 1.0,
                      "fill": color, "border": "#333333", "text_color": "#FFFFFF"})

    nodes.append({"id": "LEGEND", "tier": "note",
                  "text": "■ Critical  ■ High  ■ Medium  ■ Low",
                  "x": 20.5, "y": 7.0, "w": 5.5, "h": 2.5,
                  "fill": "#FAFAFA", "border": "#BDBDBD", "text_color": "#424242"})

    return {"nodes": nodes, "edges": edges, "title": "Risk Matrix"}


# ── 7. System Context ─────────────────────────────────────────────────────────

def layout_system_context(payload: Dict) -> Dict:
    """Radial system context: center system + external entities."""
    nodes, edges = [], []
    project = payload.get("project", {})
    ctx = payload.get("diagrams", {}).get("system_context") or {}
    center_name = project.get("name", "System")

    nodes.append({"id": "SYSTEM", "tier": "system",
                  "text": center_name, "x": 12.0, "y": 8.0, "w": 6.0, "h": 1.4,
                  "fill": "#1565C0", "border": "#0D47A1", "text_color": "#FFFFFF"})

    ctx = payload.get("diagrams", {}).get("system_context") or {}
    stakeholders = payload.get("stakeholders", [])
    ext_labels = [
        ("EXT1", stakeholders[0]["name"] if len(stakeholders) > 0 else "Patients / Users", 4.0, 4.0),
        ("EXT2", stakeholders[1]["name"] if len(stakeholders) > 1 else "Partner Systems", 20.0, 4.0),
        ("EXT3", stakeholders[2]["name"] if len(stakeholders) > 2 else "Clinic Systems", 4.0, 12.0),
        ("EXT4", stakeholders[3]["name"] if len(stakeholders) > 3 else "Mobile / Field Apps", 20.0, 12.0),
    ]
    for eid, label, x, y in ext_labels:
        nodes.append({"id": eid, "tier": "external",
                      "text": label, "x": x, "y": y, "w": 4.5, "h": 1.2,
                      "fill": "#E3F2FD", "border": "#1565C0", "text_color": "#0D47A1"})
        edges.append({"from": eid, "to": "SYSTEM", "color": "#666666"})

    if ctx.get("description"):
        nodes.append({"id": "DESC", "tier": "note",
                      "text": ctx["description"][:80], "x": 12.0, "y": 13.0, "w": 10.0, "h": 1.0,
                      "fill": "#FFF9C4", "border": "#FBC02D", "text_color": "#000000"})

    return {"nodes": nodes, "edges": edges, "title": "System Context"}


# ── Shared helper ─────────────────────────────────────────────────────────────

def _spread_xs(n: int, left_margin: float, page_w: float) -> List[float]:
    if n == 0:
        return []
    usable = page_w - 2 * left_margin
    spacing = usable / max(n, 1)
    return [left_margin + (i + 0.5) * spacing for i in range(n)]
