"""Optional Visio template (.vstx) generation."""
from __future__ import annotations

import logging

from . import visio_builder
from .config import ConverterConfig
from .utils import ensure_parent

log = logging.getLogger("svg_to_visio")


def build_template(config: ConverterConfig, stencil_path) -> Path:
    from pathlib import Path

    stencil_path = Path(stencil_path)
    if not config.template_output:
        raise ValueError("Template output path is not configured.")

    diagram = visio_builder.new_diagram()
    diagram.getDocumentProps().setTitle(f"{config.stencil_name} Template")
    diagram.getDocumentProps().setSubject(config.stencil_description)
    diagram.getDocumentProps().setCreator(config.stencil_author)

    page = visio_builder.get_page(diagram)
    page.getPageSheet().getPageProps().getPageWidth().setValue(11.0)
    page.getPageSheet().getPageProps().getPageHeight().setValue(8.5)

    try:
        stencil = visio_builder.api().Diagram(str(stencil_path))
        if stencil.getMasters().getCount() > 0:
            master_name = stencil.getMasters().get(0).getNameU()
            diagram.addMaster(str(stencil_path), master_name)
    except Exception as exc:
        log.warning(
            "Could not attach stencil reference to template (%s). Saving blank template.",
            exc,
        )

    ensure_parent(config.template_output)
    visio_builder.save_diagram(
        diagram, str(config.template_output), visio_builder.api().SaveFileFormat.VSTX
    )
    log.info("Template saved to %s", config.template_output)
    return config.template_output
