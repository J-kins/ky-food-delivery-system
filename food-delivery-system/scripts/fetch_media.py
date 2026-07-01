#!/usr/bin/env python3
"""
Fetch Media Assets for KY Food Delivery System.
Downloads free stock HD images from Unsplash for UI placeholders.
"""

import os
import urllib.request
import ssl
from pathlib import Path

# Bypass SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / "resources" / "assets" / "images" / "placeholder"

IMAGES = [
    # Foods
    {"id": "food-burger", "url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=1920&q=85&auto=format&fit=crop", "dir": "food"},
    {"id": "food-pizza", "url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=1920&q=85&auto=format&fit=crop", "dir": "food"},
    {"id": "food-salad", "url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=1920&q=85&auto=format&fit=crop", "dir": "food"},
    {"id": "food-pasta", "url": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=1920&q=85&auto=format&fit=crop", "dir": "food"},
    {"id": "food-sushi", "url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=1920&q=85&auto=format&fit=crop", "dir": "food"},
    {"id": "food-dessert", "url": "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=1920&q=85&auto=format&fit=crop", "dir": "food"},
    # Restaurants
    {"id": "restaurant-exterior", "url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1920&q=85&auto=format&fit=crop", "dir": "restaurant"},
    {"id": "restaurant-interior", "url": "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=1920&q=85&auto=format&fit=crop", "dir": "restaurant"},
    {"id": "restaurant-kitchen", "url": "https://images.unsplash.com/photo-1578474846511-04ba529f0b88?w=1920&q=85&auto=format&fit=crop", "dir": "restaurant"},
    {"id": "restaurant-cafe", "url": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1920&q=85&auto=format&fit=crop", "dir": "restaurant"},
    # Users
    {"id": "user-avatar-1", "url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=85&auto=format&fit=crop", "dir": "user"},
    {"id": "user-avatar-2", "url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=85&auto=format&fit=crop", "dir": "user"},
    {"id": "user-avatar-3", "url": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=400&q=85&auto=format&fit=crop", "dir": "user"}
]

def download_media():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    for img in IMAGES:
        target_dir = IMAGES_DIR / img["dir"]
        target_dir.mkdir(parents=True, exist_ok=True)
        
        dest = target_dir / f"{img['id']}.jpg"
        print(f"Downloading {img['id']}...")
        try:
            req = urllib.request.Request(img["url"], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(dest, 'wb') as out_file:
                out_file.write(response.read())
        except Exception as e:
            print(f"Failed to download {img['id']}: {e}")

if __name__ == "__main__":
    print("Fetching media assets...")
    download_media()
    print("Done fetching media!")
