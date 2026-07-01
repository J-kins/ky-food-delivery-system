#!/usr/bin/env python3
"""
Fetch Icons for KY Food Delivery System.
Downloads a curated list of Feather SVG icons directly into resources.
"""

import os
import urllib.request
import ssl
from pathlib import Path

# Bypass SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "resources" / "assets" / "icons" / "svg"

# Essential UI icons for food delivery
ICONS = [
    "shopping-cart",
    "user",
    "search",
    "home",
    "map-pin",
    "bell",
    "chevron-right",
    "chevron-down",
    "chevron-left",
    "chevron-up",
    "star",
    "heart",
    "menu",
    "x",
    "clock",
    "truck",
    "credit-card",
    "info",
    "settings",
    "log-out"
]

def download_icons():
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    
    for icon in ICONS:
        url = f"https://raw.githubusercontent.com/feathericons/feather/master/icons/{icon}.svg"
        dest = ICONS_DIR / f"{icon}.svg"
        print(f"Downloading {icon}.svg...")
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            print(f"Failed to download {icon}: {e}")

if __name__ == "__main__":
    print("Fetching icons...")
    download_icons()
    print("Done fetching icons!")
