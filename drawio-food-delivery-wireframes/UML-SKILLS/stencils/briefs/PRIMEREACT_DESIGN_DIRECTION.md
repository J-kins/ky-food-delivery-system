# PrimeReact Design Direction — UML Stencil Toolkit

**Reference:** [PrimeReact](https://primereact.org/) component library (Lara / Aura design language)  
**Applies to:** Stencil palette UI, diagram canvas chrome, shape rendering on canvas, export dialogs

---

## What “PrimeReact look and feel” means here

PrimeReact is an **enterprise-grade React UI kit**: clean surfaces, restrained colour, soft **border-radius**, subtle **shadows**, and dense but readable layouts. The stencil toolkit should feel like a **PrimeReact admin app** — not a raw drawing canvas bolted onto a page.

### Visual signatures to mirror

| Trait | PrimeReact pattern | Stencil toolkit application |
|-------|-------------------|----------------------------|
| Surfaces | Layered `surface-0` → `surface-100` backgrounds | Canvas, sidebar, property **panel** tiers |
| Borders | 1px `surface-200` borders, not heavy outlines | Palette dividers, shape thumbnails, **grid** guides |
| Radius | `6px` (**card** / **panel**), `4px` inputs, `12px` dialogs | Thumbnail tiles, floating toolbars |
| Primary accent | Blue primary (`#3B82F6` Lara) for focus/selection | Selected shape stroke, active tool, **focus** ring |
| Typography | Inter / system sans, 14px body, muted secondary text | Shape labels, stereotype text, inspector fields |
| Elevation | `shadow-sm` toolbars, `shadow-md` **dialogs** / **popover** | Floating format bar, export **modal** |
| Density | Compact **data grid** / **tree** spacing | Shape library **sidebar** — many items, still scannable |
| Feedback | **Toast**, inline **alert**, **skeleton screen** | Export success, validation **error**, loading stencil pack |
| Motion | 150–200ms ease-out transitions | Panel slide, tool **hover**, snap guides fade-in |

### PrimeReact components to emulate (layout vocabulary)

| UI region | PrimeReact analogue |
|-----------|---------------------|
| Left shape library | **Sidebar** + **Accordion** + **Tree** |
| Top tools | **Toolbar** + **Button** (text/icon) + **SplitButton** |
| Canvas area | **Panel** (borderless content) on `surface-50` |
| Right inspector | **Panel** + **TabView** + **InputText** / **Dropdown** |
| Context actions | **TieredMenu** / **ContextMenu** |
| Modals | **Dialog** + **ConfirmDialog** |
| Notifications | **Toast** (top-right) |
| Search shapes | **IconField** + **InputText** with search icon |
| Theme toggle | **SelectButton** or **ToggleSwitch** (light/dark) |

---

## Design tokens (Lara Light baseline)

Map these to CSS variables / SVG attributes when rendering shapes **on canvas**:

| Token | Value | Usage |
|-------|-------|-------|
| `--p-primary-color` | `#3B82F6` | Selected shape stroke, active connector |
| `--p-primary-50` | `#EFF6FF` | Selected shape fill tint |
| `--p-surface-0` | `#ffffff` | Shape fill (nodes) |
| `--p-surface-50` | `#f8fafc` | Canvas background |
| `--p-surface-100` | `#f1f5f9` | Alternate **grid** / lane fill |
| `--p-surface-200` | `#e2e8f0` | Default shape stroke, borders |
| `--p-surface-700` | `#334155` | Primary text on shapes |
| `--p-text-muted-color` | `#64748b` | Stereotypes, multiplicity labels |
| `--p-border-radius` | `6px` | Rounded nodes (actions, states) |
| `--p-focus-ring` | `0 0 0 2px #BFDBFE` | Keyboard **focus** on canvas controls |

**Dark mode (Lara Dark):** invert surfaces (`#0f172a` canvas, `#1e293b` shape fill), keep primary accent; test **contrast ratio** independently.

---

## Shape rendering rules (PrimeReact-aligned)

1. **Default on canvas:** stroke `surface-200`/`700`, fill `surface-0`, 1.5px stroke — professional, not cartoon-thick.
2. **Hover:** stroke darkens one step; optional `shadow-sm` on bounding box (**card**-like lift).
3. **Selected:** stroke `primary-color`, fill `primary-50`, 2px stroke — matches Prime **DataTable** row selection affordance.
4. **Disabled / locked:** `text-muted` stroke, 50% **opacity**, no **hover** lift.
5. **Connectors:** slightly thinner (1.25px); selected connector uses primary stroke.
6. **Labels:** 12px sans; stereotypes 10px **muted** colour — like Prime **Tag** / caption text.

---

## ASCII — Stencil application shell

```
+------------------------------------------------------------------------+
| [≡] UML Stencil Studio          [Search shapes...]     (?) [theme] [user]|
+----------+-------------------------------------------------------------+
| SIDEBAR  | TOOLBAR: [Select] [Pan] | line v | fill | undo redo | export |
| (Prime)  +-------------------------------------------------------------+
| Accordion|                                                             |
| v Basic  |  CANVAS (surface-50, dot grid)                             |
|   ▭ ◻ ◯  |  +------------------+     dashed lifeline                   |
| v UML    |  | ClassName        |        |                              |
|   class  |  | + attr           |        |                              |
| v Arch   |  +------------------+        |                              |
|          |         selected: primary border + primary-50 fill          |
|          |                                                             |
+----------+----------+--------------------------------------------------+
| (tree)   | INSPECTOR PANEL (TabView)                                   |
|          | [ Style ] [ Text ] [ Data ]                                 |
|          | Stroke [____]  Fill [____]  Radius [ 6px ]                  |
|          | Label  [________________________]                           |
+----------+-------------------------------------------------------------+
| status: 3 shapes | grid 10px | snap on                    [100% v]     |
+------------------------------------------------------------------------+
```

---

## Glossary terms (see full list)

**Sidebar**, **Panel**, **Toolbar**, **Card**, **Modal (Dialog)**, **Toast**, **Affordance**, **Focus**, **Visual Hierarchy**, **Grid**, **Whitespace**, **Design Tokens**, **Responsive Design**, **Microinteraction**

Full reference: [ui-design-glossary.md](../ui-design-glossary.md)
