#!/usr/bin/env python3
import os
import re

# Brand Palette
COLORS = {
    "forest_green": "#005638",
    "tomato_red": "#DC4024",
    "sunset_orange": "#F03919",
    "mustard_yellow": "#F0C019",
    "kraft_beige": "#E8D7B5",
    "deep_brown": "#3B2A1A",
    "off_white": "#F7F4EF",
    "white": "#FFFFFF",
    "gray_light": "#EDE9E3",
    "gray_dark": "#A89F93"
}

SVG_STYLE = f"""
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&amp;family=Poppins:wght@400;500;600;700&amp;display=swap');
      
      * {{ box-sizing: border-box; }}
      text {{ font-family: 'Poppins', sans-serif; fill: {COLORS['deep_brown']}; }}
      .heading {{ font-family: 'Baloo 2', sans-serif; font-weight: 700; fill: {COLORS['forest_green']}; }}
      .subheading {{ font-weight: 600; fill: {COLORS['deep_brown']}; }}
      
      .bg {{ fill: {COLORS['off_white']}; }}
      .card {{ fill: {COLORS['white']}; stroke: {COLORS['gray_light']}; stroke-width: 1px; rx: 12px; }}
      .shadow {{ filter: drop-shadow(0 4px 12px rgba(59,42,26,0.08)); }}
      
      .btn-primary {{ fill: {COLORS['forest_green']}; rx: 8px; }}
      .btn-primary-text {{ fill: {COLORS['white']}; font-weight: 600; font-size: 16px; text-anchor: middle; alignment-baseline: middle; }}
      
      .btn-secondary {{ fill: {COLORS['mustard_yellow']}; rx: 8px; }}
      .btn-secondary-text {{ fill: {COLORS['deep_brown']}; font-weight: 600; font-size: 16px; text-anchor: middle; alignment-baseline: middle; }}
      
      .input-bg {{ fill: {COLORS['white']}; stroke: {COLORS['gray_dark']}; stroke-width: 1.5px; rx: 8px; }}
      .input-text {{ fill: {COLORS['gray_dark']}; font-size: 14px; alignment-baseline: middle; }}
      
      .navbar {{ fill: {COLORS['white']}; stroke: {COLORS['gray_light']}; stroke-width: 1px; }}
      .bottom-bar {{ fill: {COLORS['white']}; stroke: {COLORS['gray_light']}; stroke-width: 1px; }}
      .sidebar {{ fill: {COLORS['forest_green']}; }}
      
      .badge-warning {{ fill: {COLORS['mustard_yellow']}; rx: 4px; }}
      .badge-success {{ fill: #D4EDDA; rx: 4px; }}
      .badge-danger {{ fill: #F8D7DA; rx: 4px; }}
      .badge-text {{ font-size: 12px; font-weight: 600; text-anchor: middle; alignment-baseline: middle; }}
    </style>
  </defs>
"""

def generate_mobile_svg(screen_name, layout_notes):
    w, h = 390, 844
    cx = w / 2
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
    svg += SVG_STYLE
    svg += f'<rect class="bg" width="{w}" height="{h}" />'
    
    # Status Bar
    svg += f'<rect width="{w}" height="44" fill="{COLORS["white"]}" />'
    svg += f'<text x="20" y="28" font-weight="600" font-size="14">9:41</text>'
    
    # Navbar
    svg += f'<rect class="navbar shadow" y="44" width="{w}" height="60" />'
    svg += f'<text x="{cx}" y="80" class="heading" font-size="20" text-anchor="middle">{screen_name}</text>'
    svg += f'<circle cx="35" cy="74" r="16" fill="{COLORS["gray_light"]}" />' # Back / Menu btn
    
    # Bottom Tab Bar
    svg += f'<rect class="bottom-bar shadow" y="{h-80}" width="{w}" height="80" />'
    tabs = ["Home", "Search", "Cart", "Profile"]
    for i, tab in enumerate(tabs):
        tx = 40 + (i * 100)
        color = COLORS["forest_green"] if i == 0 else COLORS["gray_dark"]
        svg += f'<circle cx="{tx}" cy="{h-50}" r="12" fill="{color}" />'
        svg += f'<text x="{tx}" y="{h-25}" font-size="10" font-weight="500" fill="{color}" text-anchor="middle">{tab}</text>'
        
    # Content Area
    cy = 120
    name_lower = screen_name.lower()
    
    if "login" in name_lower or "register" in name_lower or "password" in name_lower:
        # Auth form
        svg += f'<rect class="card shadow" x="20" y="{cy}" width="{w-40}" height="400" />'
        svg += f'<text x="{cx}" y="{cy+40}" class="heading" font-size="24" text-anchor="middle">Welcome</text>'
        for i in range(3):
            iy = cy + 80 + (i * 70)
            svg += f'<rect class="input-bg" x="40" y="{iy}" width="{w-80}" height="50" />'
            svg += f'<text x="55" y="{iy+30}" class="input-text">Enter details...</text>'
        
        svg += f'<rect class="btn-primary" x="40" y="{cy+300}" width="{w-80}" height="54" />'
        svg += f'<text x="{cx}" y="{cy+327}" class="btn-primary-text">Continue</text>'

    elif "menu" in name_lower or "list" in name_lower or "category" in name_lower:
        # Grid/List of food
        svg += f'<rect class="input-bg" x="20" y="{cy}" width="{w-40}" height="44" />'
        svg += f'<text x="35" y="{cy+27}" class="input-text">Search {screen_name}...</text>'
        cy += 60
        
        for i in range(4):
            ry = cy + (i * 140)
            svg += f'<rect class="card shadow" x="20" y="{ry}" width="{w-40}" height="120" />'
            svg += f'<rect x="35" y="{ry+15}" width="90" height="90" rx="8" fill="{COLORS["gray_light"]}" />' # Image
            svg += f'<text x="140" y="{ry+35}" class="subheading" font-size="16">Item Name {i+1}</text>'
            svg += f'<text x="140" y="{ry+55}" font-size="14" fill="{COLORS["gray_dark"]}">Description of food.</text>'
            svg += f'<text x="140" y="{ry+80}" font-weight="600" font-size="16" fill="{COLORS["tomato_red"]}">UGX 15,000</text>'
            svg += f'<rect class="btn-primary" x="{w-90}" y="{ry+70}" width="60" height="32" />'
            svg += f'<text x="{w-60}" y="{ry+86}" class="btn-primary-text" font-size="14">Add</text>'

    elif "map" in name_lower or "track" in name_lower or "location" in name_lower or "zone" in name_lower:
        # Full bleed map
        svg += f'<rect x="0" y="104" width="{w}" height="{h-184}" fill="{COLORS["kraft_beige"]}" />'
        # Route lines
        svg += f'<path d="M50 200 L150 400 L250 350 L300 600" stroke="{COLORS["forest_green"]}" stroke-width="6" fill="none" stroke-linejoin="round" />'
        # Map Pins
        svg += f'<circle cx="50" cy="200" r="12" fill="{COLORS["tomato_red"]}" />'
        svg += f'<circle cx="300" cy="600" r="16" fill="{COLORS["forest_green"]}" />'
        
        # Bottom Sheet
        svg += f'<rect class="card shadow" x="10" y="{h-280}" width="{w-20}" height="180" />'
        svg += f'<text x="{cx}" y="{h-240}" class="subheading" font-size="18" text-anchor="middle">Driver is 5 mins away</text>'
        svg += f'<rect class="btn-primary" x="30" y="{h-160}" width="{w-60}" height="48" />'
        svg += f'<text x="{cx}" y="{h-136}" class="btn-primary-text">Contact Driver</text>'

    elif "cart" in name_lower or "checkout" in name_lower or "payment" in name_lower:
        # Cart/Checkout flow
        for i in range(2):
            ry = cy + (i * 100)
            svg += f'<rect class="card shadow" x="20" y="{ry}" width="{w-40}" height="80" />'
            svg += f'<text x="40" y="{ry+35}" class="subheading" font-size="16">Cart Item {i+1}</text>'
            svg += f'<text x="{w-40}" y="{ry+35}" font-weight="600" text-anchor="end">UGX 15,000</text>'
        
        sy = cy + 220
        svg += f'<rect class="card shadow" x="20" y="{sy}" width="{w-40}" height="150" />'
        svg += f'<text x="40" y="{sy+30}" class="subheading" font-size="16">Order Summary</text>'
        svg += f'<line x1="40" y1="{sy+50}" x2="{w-40}" y2="{sy+50}" stroke="{COLORS["gray_light"]}" stroke-width="1"/>'
        svg += f'<text x="40" y="{sy+80}">Total:</text>'
        svg += f'<text x="{w-40}" y="{sy+80}" font-weight="700" font-size="18" fill="{COLORS["forest_green"]}" text-anchor="end">UGX 30,000</text>'
        
        svg += f'<rect class="btn-primary" x="40" y="{sy+100}" width="{w-80}" height="50" />'
        svg += f'<text x="{cx}" y="{sy+125}" class="btn-primary-text">Confirm & Pay</text>'

    else:
        # Generic Dashboard / Settings
        for i in range(4):
            ry = cy + (i * 90)
            svg += f'<rect class="card shadow" x="20" y="{ry}" width="{w-40}" height="70" />'
            svg += f'<circle cx="50" cy="{ry+35}" r="16" fill="{COLORS["gray_light"]}" />'
            svg += f'<text x="80" y="{ry+40}" class="subheading" font-size="16">Feature {i+1}</text>'
            svg += f'<path d="M{w-40} {ry+25} L{w-30} {ry+35} L{w-40} {ry+45}" stroke="{COLORS["gray_dark"]}" stroke-width="2" fill="none" />'
            
    svg += '</svg>'
    return svg

def generate_desktop_svg(screen_name, layout_notes):
    w, h = 1440, 900
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
    svg += SVG_STYLE
    svg += f'<rect class="bg" width="{w}" height="{h}" />'
    
    # Sidebar
    svg += f'<rect class="sidebar" width="280" height="{h}" />'
    svg += f'<text x="140" y="50" class="heading" font-size="28" fill="{COLORS["white"]}" text-anchor="middle">KY FOODS</text>'
    
    nav_items = ["Dashboard", "Orders", "Menu", "Users", "Settings"]
    for i, item in enumerate(nav_items):
        ny = 120 + (i * 60)
        bg = COLORS["tomato_red"] if i == 0 else "none"
        color = COLORS["white"] if i == 0 else COLORS["kraft_beige"]
        svg += f'<rect x="20" y="{ny-30}" width="240" height="50" rx="8" fill="{bg}" />'
        svg += f'<text x="60" y="{ny-10}" font-weight="600" font-size="16" fill="{color}">{item}</text>'
    
    # Topbar
    svg += f'<rect class="navbar shadow" x="280" y="0" width="{w-280}" height="80" />'
    svg += f'<text x="320" y="48" class="heading" font-size="24">{screen_name}</text>'
    svg += f'<circle cx="{w-60}" cy="40" r="20" fill="{COLORS["mustard_yellow"]}" />'
    svg += f'<text x="{w-120}" y="45" font-weight="600" text-anchor="end">Admin User</text>'
    
    # Content Area
    cx = 280
    cy = 100
    name_lower = screen_name.lower()
    
    if "dashboard" in name_lower or "analytics" in name_lower:
        # KPI Cards
        for i in range(4):
            kx = cx + 40 + (i * 270)
            svg += f'<rect class="card shadow" x="{kx}" y="{cy+20}" width="250" height="120" />'
            svg += f'<text x="{kx+20}" y="{cy+50}" class="subheading" font-size="16" fill="{COLORS["gray_dark"]}">Metric {i+1}</text>'
            svg += f'<text x="{kx+20}" y="{cy+90}" font-weight="700" font-size="32" fill="{COLORS["deep_brown"]}">1,234</text>'
            
        # Chart placeholder
        svg += f'<rect class="card shadow" x="{cx+40}" y="{cy+180}" width="1060" height="400" />'
        svg += f'<text x="{cx+70}" y="{cy+230}" class="subheading" font-size="20">Performance Overview</text>'
        svg += f'<rect x="{cx+70}" y="{cy+260}" width="1000" height="280" fill="{COLORS["off_white"]}" rx="8" />'
        # Bar charts
        for j in range(10):
            bx = cx + 120 + (j * 90)
            bh = 50 + (j * 20 % 200)
            svg += f'<rect x="{bx}" y="{cy+540-bh}" width="40" height="{bh}" fill="{COLORS["sunset_orange"]}" rx="4" />'
            
    else:
        # Data Table
        svg += f'<rect class="card shadow" x="{cx+40}" y="{cy+20}" width="1060" height="600" />'
        
        # Table Header/Controls
        svg += f'<rect class="input-bg" x="{cx+70}" y="{cy+50}" width="300" height="40" />'
        svg += f'<text x="{cx+90}" y="{cy+75}" class="input-text">Search records...</text>'
        svg += f'<rect class="btn-primary" x="{cx+960}" y="{cy+50}" width="140" height="40" />'
        svg += f'<text x="{cx+1030}" y="{cy+75}" class="btn-primary-text" font-size="14">+ Add New</text>'
        
        svg += f'<line x1="{cx+40}" y1="{cy+110}" x2="{cx+1100}" y2="{cy+110}" stroke="{COLORS["gray_light"]}" stroke-width="2"/>'
        
        # Table Rows
        cols = ["ID", "Name / Details", "Status", "Date", "Actions"]
        for j, col in enumerate(cols):
            svg += f'<text x="{cx+80 + j*200}" y="{cy+140}" font-weight="600" font-size="14" fill="{COLORS["gray_dark"]}">{col}</text>'
            
        for i in range(7):
            ry = cy + 190 + (i * 60)
            svg += f'<line x1="{cx+40}" y1="{ry-20}" x2="{cx+1100}" y2="{ry-20}" stroke="{COLORS["gray_light"]}" stroke-width="1"/>'
            svg += f'<text x="{cx+80}" y="{ry}" font-size="14">#100{i}</text>'
            svg += f'<text x="{cx+280}" y="{ry}" font-size="14" font-weight="500">Record Data Name</text>'
            
            # Badge
            color_class = "badge-success" if i % 2 == 0 else "badge-warning"
            text = "Active" if i % 2 == 0 else "Pending"
            text_color = "#155724" if i % 2 == 0 else COLORS["deep_brown"]
            svg += f'<rect class="{color_class}" x="{cx+480}" y="{ry-16}" width="80" height="24" />'
            svg += f'<text x="{cx+520}" y="{ry+1}" class="badge-text" fill="{text_color}">{text}</text>'
            
            svg += f'<text x="{cx+680}" y="{ry}" font-size="14">Oct 24, 2025</text>'
            svg += f'<text x="{cx+880}" y="{ry}" font-size="14" font-weight="600" fill="{COLORS["tomato_red"]}">Edit / Delete</text>'

    svg += '</svg>'
    return svg


def process_inventory():
    input_file = '/Users/jenkinskabona/Documents/ky-foods/drawio-food-delivery-wireframes/references/screen-inventory.md'
    out_dir = '/Users/jenkinskabona/Documents/ky-foods/drawio-food-delivery-wireframes/svg'
    os.makedirs(out_dir, exist_ok=True)
    
    with open(input_file, 'r') as f:
        content = f.read()
        
    # Find table rows with screens
    # Format: | # | Screen | Pattern | Priority | Layout notes |
    pattern = re.compile(r'\|\s*(\d+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|')
    
    current_role = "Customer"
    
    # Simple state machine to track roles based on headers
    lines = content.splitlines()
    for line in lines:
        if line.startswith('## '):
            if "Kitchen" in line or "Staff" in line: current_role = "Kitchen"
            elif "Manager" in line: current_role = "Manager"
            elif "Admin" in line: current_role = "Admin"
            elif "Support" in line: current_role = "Support"
            elif "Rider" in line: current_role = "Rider"
            elif "Customer" in line: current_role = "Customer"
            
        match = pattern.search(line)
        if match:
            num = match.group(1).strip()
            name_raw = match.group(2).strip().replace('**', '').replace('(NEW)', '').strip()
            notes = match.group(5).strip()
            
            clean_name = re.sub(r'[^a-zA-Z0-9]', '_', name_raw)
            filename = f"{int(num):02d}_{current_role}_{clean_name}.svg"
            
            # Determine form factor
            is_desktop = current_role in ["Kitchen", "Manager", "Admin", "Support"]
            
            if is_desktop:
                svg_data = generate_desktop_svg(name_raw, notes)
            else:
                svg_data = generate_mobile_svg(name_raw, notes)
                
            filepath = os.path.join(out_dir, filename)
            with open(filepath, 'w') as out:
                out.write(svg_data)
                
            print(f"Generated: {filename}")

if __name__ == '__main__':
    process_inventory()
    print("Done generating 95 screens!")
