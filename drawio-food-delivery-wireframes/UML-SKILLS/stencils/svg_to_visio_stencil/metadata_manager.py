"""Shape metadata and connection point management."""
from __future__ import annotations

from datetime import datetime
from typing import Dict

from . import visio_builder


def add_master_metadata(root_shape, metadata: Dict, config) -> None:
    prop_id = 1
    fields = {
        "ShapeId": metadata.get("id", ""),
        "ShapeName": metadata.get("name", ""),
        "Category": metadata.get("category_name")
        or config.category_display_name(metadata.get("category", "")),
        "CategoryId": metadata.get("category", ""),
        "AssetType": metadata.get("asset_type", "shape"),
        "Description": metadata.get("description", ""),
        "Purpose": metadata.get("purpose", ""),
        "SourceFile": metadata.get("source_file", ""),
        "Created": datetime.now().isoformat(timespec="seconds"),
    }
    for name, value in fields.items():
        if value:
            visio_builder.add_shape_property(root_shape, name, str(value), prop_id)
            prop_id += 1


def add_master_connections(root_shape, metadata: Dict, width_in: float, height_in: float, config) -> None:
    if not config.connection_points.get("enabled", True):
        return

    asset_type = metadata.get("asset_type", "shape")
    if asset_type == "connector":
        point_names = config.connection_points.get("connector", ["left", "right"])
    else:
        point_names = config.connection_points.get(
            "shape", ["top", "bottom", "left", "right", "center"]
        )

    formulas = {
        "top": ("Width*0.5", "Height"),
        "bottom": ("Width*0.5", "0"),
        "left": ("0", "Height*0.5"),
        "right": ("Width", "Height*0.5"),
        "center": ("Width*0.5", "Height*0.5"),
    }

    point_id = 1
    for name in point_names:
        x_formula, y_formula = formulas[name]
        visio_builder.add_connection_point(root_shape, point_id, name.title(), x_formula, y_formula)
        point_id += 1

    xform = root_shape.getXForm()
    if xform is not None:
        xform.getWidth().setValue(width_in)
        xform.getHeight().setValue(height_in)
        xform.getLocPinX().setValue(width_in / 2.0)
        xform.getLocPinY().setValue(height_in / 2.0)
