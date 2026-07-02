"""Load environment and apply Aspose licenses."""
from __future__ import annotations

import logging
import os
from pathlib import Path

log = logging.getLogger(__name__)

PAGE_SIZES_IN = {
    "A2": (59.4, 42.0),
    "A3": (42.0, 29.7),
    "A4": (29.7, 21.0),
}

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_dot_path() -> str:
    return os.getenv("GRAPHVIZ_DOT_PATH", "dot")


def get_d2_path() -> str:
    return os.getenv("D2_PATH", "d2")


def apply_aspose_diagram_license() -> bool:
    """Apply Aspose.Diagram license from ASPOSE_DIAGRAM_LICENSE_PATH if present."""
    license_path = os.getenv("ASPOSE_DIAGRAM_LICENSE_PATH", "")
    if not license_path or not Path(license_path).is_file():
        log.debug("Aspose.Diagram license not configured (ASPOSE_DIAGRAM_LICENSE_PATH).")
        return False
    try:
        import jpype
        if not jpype.isJVMStarted():
            jpype.startJVM(convertStrings=False)
        import asposediagram.api as api
        lic = api.License()
        lic.setLicense(license_path)
        log.info("Aspose.Diagram license applied.")
        return True
    except Exception as exc:
        log.warning("Failed to apply Aspose.Diagram license: %s", exc)
        return False
