"""Environment and Aspose license configuration."""
from __future__ import annotations

import logging
import os
from pathlib import Path

log = logging.getLogger(__name__)

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass

OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./output")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

PAGE_SIZES_IN = {
    "A1": (84.1, 59.4),
    "A2": (59.4, 42.0),
    "A3": (42.0, 29.7),
    "A4": (29.7, 21.0),
}


def apply_aspose_diagram_license() -> bool:
    license_path = os.getenv("ASPOSE_DIAGRAM_LICENSE_PATH", "")
    if not license_path or not Path(license_path).is_file():
        log.debug("Aspose.Diagram license not configured.")
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
        log.warning("Failed to apply Aspose license: %s", exc)
        return False
