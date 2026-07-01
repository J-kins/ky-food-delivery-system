#!/usr/bin/env python3
"""
Fetch Fonts for KY Food Delivery System.
Downloads Poppins and Baloo 2 from the Google Fonts GitHub repository.
"""

import os
import urllib.request
import ssl
from pathlib import Path

# Bypass SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

ROOT = Path(__file__).resolve().parents[1]
FONTS_DIR = ROOT / "resources" / "assets" / "fonts"

FONTS = {
    "Poppins": [
        "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold"
    ],
    "Baloo2": [
        "Regular", "Medium", "SemiBold", "Bold", "ExtraBold"
    ]
}

def download_font():
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Poppins
    poppins_dir = FONTS_DIR / "Poppins"
    poppins_dir.mkdir(exist_ok=True)
    for weight in FONTS["Poppins"]:
        url = f"https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-{weight}.ttf"
        dest = poppins_dir / f"Poppins-{weight}.ttf"
        print(f"Downloading {url}...")
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            print(f"Failed to download {url}: {e}")

    # Baloo 2
    baloo_dir = FONTS_DIR / "Baloo2"
    baloo_dir.mkdir(exist_ok=True)
    for weight in FONTS["Baloo2"]:
        url = f"https://raw.githubusercontent.com/google/fonts/main/ofl/baloo2/Baloo2-{weight}.ttf"
        dest = baloo_dir / f"Baloo2-{weight}.ttf"
        print(f"Downloading {url}...")
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            print(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    print("Fetching fonts...")
    download_font()
    print("Done fetching fonts!")
