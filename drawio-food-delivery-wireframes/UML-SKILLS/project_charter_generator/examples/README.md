# Project Charter Generator — Examples

Da'atSNA sample data aligned with `PROMPT.md` (16 files: 13 split + 3 merged).

## Quick start

```bash
cd project_charter_generator
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Requires: Java JRE for Aspose; Graphviz (dot) or D2 for SVG compilation
# Optional: copy .env.example → .env and set ASPOSE_DIAGRAM_LICENSE_PATH

python cli.py merge examples/split --validate
python cli.py build examples/split/charter_input.json -o examples/output -v

# Or one-shot sample runner with verification:
python scripts/run_example.py
```

## Split files (`examples/split/`)

| Bundle | Files |
|--------|-------|
| Shared | `charter_project_input.json`, `charter_content_input.json`, `charter_people_input.json`, `charter_schedule_risk_input.json` |
| Diagram descriptions (Word) | `charter_diagram_*_input.json` (7 files — Graphviz/D2) |
| Word | `charter_word_styling_input.json` |
| Visio | `charter_visio_diagrams_input.json` |

After `merge`: `charter_word_input.json`, `charter_visio_input.json`, `charter_input.json`

## Output (`examples/output/`)

- `project-charter.docx` — 13 sections with **native DrawingML shape** diagrams (editable in Word)
- `diagrams/source/*.dot` — Graphviz source from diagram descriptions
- `diagrams/svg/*.svg` — SVG archive (reference; Word uses DrawingML shapes)
- `visio/project-charter.vsdx` — Aspose.Diagram multi-page deck

## Word diagram pipeline

```text
charter_diagram_<name>_input.json  →  .dot / .d2  →  .svg XML  →  embedded in .docx
```
