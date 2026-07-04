"""Utilities for SVG template conversion."""

import logging
from pathlib import Path
from typing import Optional


def setup_logging(
    log_dir: Path,
    verbose: bool = False,
) -> logging.Logger:
    """Setup logging configuration.
    
    Args:
        log_dir: Directory for log files
        verbose: Enable verbose output
        
    Returns:
        Configured logger
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    
    level = logging.DEBUG if verbose else logging.INFO
    logger = logging.getLogger("svg_to_visio")
    logger.setLevel(level)
    
    # File handler
    fh = logging.FileHandler(log_dir / "conversion.log")
    fh.setLevel(level)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger


def resolve_path(path_str: str, base_dir: Optional[Path] = None) -> Path:
    """Resolve path relative to base directory.
    
    Args:
        path_str: Path string
        base_dir: Base directory for relative paths
        
    Returns:
        Resolved absolute path
    """
    path = Path(path_str)
    if path.is_absolute():
        return path
    
    if base_dir:
        return (base_dir / path).resolve()
    
    return path.resolve()
