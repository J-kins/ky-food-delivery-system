# Stencil Toolkit — Design Briefs

UI/UX design briefs for the UML & architecture stencil system.

**Aesthetic:** [PrimeReact](https://primereact.org/) enterprise UI (Lara theme) — clean surfaces, primary blue selection, compact **sidebar**/**panel** layout, subtle shadows, 6px **border-radius**.

## References

| Doc | Purpose |
|-----|---------|
| [PRIMEREACT_DESIGN_DIRECTION.md](./PRIMEREACT_DESIGN_DIRECTION.md) | PrimeReact look & feel for palette + canvas |
| [UI-UX_Design_Brief_Template.md](../UI-UX_Design_Brief_Template.md) | Brief structure template |
| [ui-design-glossary.md](../ui-design-glossary.md) | Terminology |
| [svg/STYLE_GUIDE.md](../svg/STYLE_GUIDE.md) | SVG token mapping |

## Index

**[BRIEFS_INDEX.md](./BRIEFS_INDEX.md)** — full listing

| Folder | Contents |
|--------|----------|
| [system/](./system/) | App shell, palette, canvas, export dialog (4) |
| [categories/](./categories/) | Per-category briefs (15) |
| [shapes/](./shapes/) | Per-shape briefs (~204) |

## Regenerate

```bash
cd stencils/briefs
python3 generate_briefs.py
```

## PrimeReact in one sentence

Think **PrimeReact admin dashboard**: left **Sidebar** with **Accordion** shape library, top **Toolbar**, centre canvas on `surface-50`, right inspector **Panel** with **TabView**, **Toast** feedback — not a bare technical drawing widget.
