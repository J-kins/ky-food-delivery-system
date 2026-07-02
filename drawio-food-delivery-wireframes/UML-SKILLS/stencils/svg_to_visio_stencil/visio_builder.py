"""Aspose.Diagram JVM bootstrap and low-level Visio helpers."""
from __future__ import annotations

import logging
from typing import Optional

log = logging.getLogger(__name__)

_ASPOSE_READY = False
_api = None


def ensure_jvm() -> None:
    global _ASPOSE_READY, _api
    if _ASPOSE_READY:
        return
    try:
        import jpype

        if not jpype.isJVMStarted():
            jpype.startJVM(convertStrings=False)
        import asposediagram.api as api

        _api = api
        _ASPOSE_READY = True
    except Exception as exc:
        raise RuntimeError(
            "Aspose.Diagram is not available. Install requirements and ensure Java 11+ is installed. "
            f"Original error: {exc}"
        ) from exc


def api():
    ensure_jvm()
    return _api


def new_diagram():
    return api().Diagram()


def save_diagram(diagram, output_path: str, file_format) -> None:
    diagram.save(output_path, file_format)


def get_page(diagram, index: int = 0):
    return diagram.getPages().get(index)


def clear_page_shapes(page) -> None:
    shapes = page.getShapes()
    ids = [shapes.get(i).getID() for i in range(shapes.getCount())]
    for sid in reversed(ids):
        shapes.remove(shapes.getShape(sid))


def apply_line_style(shape, color: str, width: float, dashed: bool = False, no_border: bool = False) -> None:
    line = shape.getLine()
    if line is None:
        return
    if no_border:
        line.getLinePattern().setValue(0)
        return
    line.getLineColor().setValue(color)
    line.getLineWeight().setValue(width / 72.0)
    line.getLinePattern().setValue(2 if dashed else 1)


def apply_fill_style(shape, color: str, no_fill: bool = False) -> None:
    fill = shape.getFill()
    if fill is None:
        return
    if no_fill:
        fill.getFillPattern().setValue(0)
        return
    fill.getFillForegnd().setValue(color)
    fill.getFillBkgnd().setValue(color)
    fill.getFillPattern().setValue(1)


def get_shape(page, shape_id: int):
    return page.getShapes().getShape(shape_id)


def make_double_array(values):
    import jpype

    array = jpype.JClass("double[]")(len(values))
    for index, value in enumerate(values):
        array[index] = float(value)
    return array


def add_connection_point(shape, point_id: int, name: str, x_formula: str, y_formula: str) -> None:
    connection = api().Connection()
    connection.setID(point_id)
    connection.setNameU(name)
    connection.getX().getUfe().setF(x_formula)
    connection.getY().getUfe().setF(y_formula)
    connection.getDirX().setValue(0)
    connection.getDirY().setValue(0)
    connection.getType().setValue(0)
    connection.getAutoGen().setValue(api().BOOL.FALSE)
    shape.getConnections().add(connection)


def add_shape_property(shape, name: str, value: str, prop_id: int) -> None:
    prop = api().Prop()
    prop.setID(prop_id)
    prop.setNameU(name)
    prop.getValue().setVal(value)
    shape.getProps().add(prop)
