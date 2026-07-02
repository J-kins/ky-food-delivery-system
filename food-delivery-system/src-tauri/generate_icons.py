import os
from PIL import Image, ImageDraw, ImageFont

# Create icons directory if not exists
os.makedirs("icons", exist_ok=True)

# Create a 1024x1024 image
size = 1024
img = Image.new('RGBA', (size, size), color=(0, 86, 56, 255)) # Forest Green
draw = ImageDraw.Draw(img)

# Try to load a font, otherwise use default
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 400)
except:
    font = ImageFont.load_default()

# Add text
text = "KY"
# Center text manually using textbbox if available
try:
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((size-w)/2, (size-h)/2 - h/4), text, fill="white", font=font)
except:
    draw.text((size/4, size/4), text, fill="white", font=font)

# Save the base icon
img.save("app-icon.png")
print("Saved app-icon.png")
