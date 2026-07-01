# KY Food Delivery - Professional UI Design System
## Version 1.0 | SVG Component Library & Responsive Specifications

---

## 01. Design System Overview

This document outlines the professional UI design system for KY Food Delivery across **mobile (375px)**, **tablet (768px)**, and **desktop (1440px)** breakpoints.

All SVG files follow the brand guidelines defined in `KY_Food_Delivery_Brand_Guidelines.md` and maintain **WCAG AA accessibility standards** throughout.

---

## 02. Color Palette (Implementation)

```
Primary Brand Colors:
- Forest Green:   #005638
- Tomato Red:     #DC4024
- Sunset Orange:  #F03919
- Mustard Yellow: #F0C019

Neutral Colors:
- Kraft Beige:    #E8D7B5
- Deep Brown:     #3B2A1A
- Off White:      #F7F4EF

Functional Colors:
- Success:        #2E7D32 (Green)
- Error:          #C62828 (Red)
- Warning:        #F57C00 (Orange)
- Info:           #0277BD (Blue)

Grays (for UI elements):
- Gray 50:        #FAFAFA
- Gray 100:       #F5F5F5
- Gray 200:       #EEEEEE
- Gray 300:       #E0E0E0
- Gray 400:       #BDBDBD
- Gray 500:       #9E9E9E
- Gray 600:       #757575
- Gray 700:       #616161
- Gray 800:       #424242
- Gray 900:       #212121
```

---

## 03. Typography Implementation

### Font Stack
- **Primary (Poppins):** Used for all UI text, body copy, buttons, labels
- **Display (Baloo 2):** Used for hero headlines, promotional copy, accents

### Type Scale (Digital)
```
Display / Hero:   72px / 56px, Bold/ExtraBold, line-height 1.1
H1:               40px, Bold, line-height 1.2
H2:               32px, Bold, line-height 1.25
H3:               24px, SemiBold, line-height 1.3
H4 / Subheading:  20px, SemiBold, line-height 1.35
Body Large:       18px, Regular, line-height 1.6
Body Default:     16px, Regular, line-height 1.6
Body Small:       14px, Regular, line-height 1.6
Label / Button:   14px, SemiBold, line-height 1.4
Caption:          12px, Regular, line-height 1.4
Micro:            11px, Medium, line-height 1.3
```

---

## 04. Responsive Breakpoints

```
Mobile:   375px width (base), 812px height (iPhone 13)
Tablet:   768px width, 1024px height (iPad)
Desktop:  1440px width, 900px height+ (Full desktop)
```

### Spacing & Grid
- **Base unit:** 8px
- **Grid columns:** 4 (mobile), 8 (tablet), 12 (desktop)
- **Gutter:** 16px (mobile), 24px (tablet), 32px (desktop)
- **Safe area margins:** 16px (mobile), 24px (tablet), 48px (desktop)

---

## 05. Component Library

### Buttons

**Primary Button**
- Background: Forest Green (#005638)
- Text: Off White (#F7F4EF), SemiBold, 14px
- Padding: 12px 24px
- Border-radius: 8px
- Min-height: 48px (touch target)
- State: hover (darken 10%), active (darken 15%), disabled (opacity 50%)

**Secondary Button**
- Background: Off White (#F7F4EF)
- Border: 2px Tomato Red (#DC4024)
- Text: Tomato Red (#DC4024), SemiBold, 14px
- Padding: 10px 24px
- Border-radius: 8px
- State: hover (Light Red tint), disabled (opacity 50%)

**Icon Button**
- 44px × 44px minimum (touch target)
- 24px icon
- Background: Optional (Forest Green on light, Off White on dark)
- Padding: 10px

**CTA Button (Floating)**
- Background: Tomato Red (#DC4024)
- Text: Off White, SemiBold
- 56px × 56px (mobile), positioned fixed bottom-right
- Border-radius: 50%

### Input Fields

**Text Input**
- Height: 48px
- Border: 1px Gray 300 (#E0E0E0)
- Border-radius: 8px
- Padding: 12px 16px
- Focus: Border 2px Forest Green (#005638)
- Label: Poppins, 14px, SemiBold, Deep Brown (#3B2A1A)
- Placeholder: Gray 500 (#9E9E9E)
- Error state: Border 2px Error Red (#C62828), Error text 12px under field

**Dropdown / Select**
- Height: 48px
- Border: 1px Gray 300
- Background: Off White
- Arrow: Deep Brown
- Selected text: 16px, Regular, Deep Brown
- Hover: Border 2px Forest Green
- Active/Expanded: Border 2px Forest Green, Background Gray 50

**Checkbox**
- Size: 24px × 24px
- Unchecked: Border 2px Gray 400, transparent background
- Checked: Background Forest Green, white checkmark
- Label: 16px, Regular, Deep Brown (to the right)
- Spacing: 8px between checkbox and label

**Radio Button**
- Size: 24px diameter
- Unchecked: Border 3px Gray 400
- Checked: Border 3px Forest Green, filled center dot
- Label: 16px, Regular, Deep Brown
- Spacing: 8px between radio and label

### Cards

**Standard Card**
- Background: Off White (#F7F4EF)
- Border: 1px Gray 200 (#EEEEEE)
- Border-radius: 12px
- Padding: 16px
- Shadow: 0 1px 3px rgba(0,0,0,0.08), 0 2px 6px rgba(0,0,0,0.05)
- Hover: Shadow 0 4px 12px rgba(0,0,0,0.12), slight scale up (1.02)

**Product Card**
- Image area: 100% width, 200px height (mobile), 280px height (tablet), variable (desktop)
- Content area: 16px padding
- Title: 16px, SemiBold, Deep Brown
- Subtitle: 14px, Regular, Gray 600
- Price: 18px, Bold, Tomato Red
- Rating: 12px, Regular, Gray 600 (★ 4.5)
- Badge (optional): Mustard Yellow background, Deep Brown text, 10px padding

**Restaurant Card**
- Horizontal layout (tablet+), vertical layout (mobile)
- Image: 120px width (mobile), 200px (tablet), aspect ratio 4:3
- Content area: 16px padding
- Title: 18px, SemiBold, Deep Brown
- Category: 12px, Regular, Gray 600
- Rating & delivery: 14px, Regular, Gray 600
- Delivery time: Tomato Red accent

### Navigation & Headers

**Top App Bar**
- Height: 56px (mobile), 64px (tablet/desktop)
- Background: Forest Green (#005638)
- Text/Icons: Off White (#F7F4EF)
- Title: Poppins, 20px, SemiBold, Off White
- Leading icon: 24px (back/menu)
- Trailing icons: 24px (search, more)

**Bottom Navigation (Mobile only)**
- Height: 56px
- Background: Off White (#F7F4EF)
- Border-top: 1px Gray 200
- 4–5 nav items
- Icon: 24px, Gray 700
- Label: 10px, SemiBold, Gray 700
- Active item: Tomato Red icon & label
- Safe area bottom: 8px padding (notch support)

**Tab Navigation**
- Height: 48px
- Background: Off White
- Tab: 16px, SemiBold, Gray 600
- Active tab: Tomato Red text + underline (4px)
- Underline animation: 200ms ease-in-out

### Badges & Tags

**Badge**
- Background: Forest Green
- Text: Off White, 11px, SemiBold
- Padding: 4px 8px
- Border-radius: 4px
- Example: "NEW", "HOT", "BESTSELLER"

**Tag**
- Background: Kraft Beige (#E8D7B5)
- Text: Deep Brown (#3B2A1A), 12px, Regular
- Padding: 6px 12px
- Border-radius: 16px (pill-shaped)
- Example: "Vegetarian", "Spicy", "Quick"

### Modals & Dialogs

**Modal**
- Overlay: rgba(0,0,0,0.5)
- Card background: Off White (#F7F4EF)
- Border-radius: 16px
- Max-width: 90% mobile, 80% tablet, 50% desktop
- Padding: 24px
- Title: 24px, SemiBold, Deep Brown
- Close button: X icon, 32px × 32px, top-right
- Action buttons: 48px height, 100% width (stacked on mobile)

### Lists & Item Rows

**List Item**
- Height: 64px+ (touch target 48px minimum)
- Padding: 16px
- Background: Off White / alternating Gray 50
- Border-bottom: 1px Gray 200
- Left icon/image: 48px × 48px, border-radius 8px
- Title: 16px, SemiBold, Deep Brown
- Subtitle: 14px, Regular, Gray 600
- Right: Icon / toggle / badge

### Empty States

**Empty State Component**
- Centered container
- Icon: 80px × 80px, Gray 400
- Title: 20px, SemiBold, Deep Brown
- Description: 14px, Regular, Gray 600
- Action button: 48px, Forest Green
- Example: "No orders yet", "Nothing saved"

### Toast / Snackbar

**Toast**
- Position: Fixed bottom-left / bottom-center
- Background: Deep Brown (#3B2A1A)
- Text: Off White, 14px, Regular
- Padding: 12px 16px
- Border-radius: 8px
- Shadow: 0 3px 12px rgba(0,0,0,0.24)
- Duration: Auto-dismiss 4s
- Action button: Optional, Off White text

### Dividers & Separators

**Divider Line**
- Height: 1px
- Color: Gray 200 (#EEEEEE)
- Margin: 16px vertical (standard spacing)

**Section Divider (Wave)**
- Height: 8px
- SVG: Organic wave pattern
- Color: Mustard Yellow (#F0C019)
- Opacity: 20%

---

## 06. Interaction Patterns

### Touch Targets
- Minimum: 44px × 44px
- Icons: 24px inner, 44px outer touch zone
- Buttons: 48px height minimum
- List items: 56px height minimum

### Animations & Transitions
- Standard: 200ms ease-in-out
- Opacity: 150ms ease
- Scale: 200ms cubic-bezier(0.34, 1.56, 0.64, 1)
- Slide: 300ms ease-in-out

### Loading States
- Spinner: 24px SVG, rotating 360°, 2s infinite
- Color: Forest Green
- Skeleton: Gray 200 shimmer, 1.5s animation

### Micro-interactions
- Button press: Scale 0.98 + shadow reduction (50ms)
- Hover: Scale 1.02 + shadow increase (200ms)
- Active: Scale 0.95 (instant)
- Disabled: Opacity 0.5 (instant)

---

## 07. Accessibility Standards

### WCAG AA Compliance
- **Color contrast:** Minimum 4.5:1 for body text, 3:1 for large text
- **Focus indicators:** 2px outline, Forest Green
- **Button labels:** Always present, descriptive
- **Form labels:** Associated with inputs via `<label>`
- **Alt text:** All images/icons must have descriptive alt text
- **Keyboard navigation:** All interactive elements focusable, tab order logical
- **Touch targets:** 44px minimum for all interactive elements

### Color-Blindness Safe Design
- Do not rely on color alone to convey information
- Use icons + color for status indicators (✓ + Green, ✗ + Red)
- High contrast between foreground and background
- Test contrast with tools like WebAIM Contrast Checker

---

## 08. File Naming Convention

```
Format: [SCREEN_NUMBER]_[SCREEN_NAME]_[BREAKPOINT].svg

Examples:
11_Customer_Home_Dashboard_mobile.svg
11_Customer_Home_Dashboard_tablet.svg
11_Customer_Home_Dashboard_desktop.svg

12_Customer_Search_Screen_mobile.svg
12_Customer_Search_Screen_tablet.svg
12_Customer_Search_Screen_desktop.svg
```

---

## 09. SVG Best Practices

- **Vector-only:** All designs use pure SVG paths, shapes, and text
- **No raster images:** Placeholder areas use solid colors or patterns, not embedded images
- **Optimized paths:** Paths simplified, unnecessary nodes removed
- **Text encoding:** UTF-8, all text editable
- **Layering:** Logical layer naming (header, content, footer, overlay)
- **Responsive:** SVG viewBox scales proportionally across breakpoints
- **File size:** Target <100KB per file, optimized with SVGO or similar
- **Reusable components:** Symbols/groups for buttons, cards, icons used multiple times

---

## 10. Responsive Design Approach

### Mobile-First Strategy
1. Design for 375px width first (base case)
2. Tablet refinements at 768px (column layout changes, increased spacing)
3. Desktop enhancements at 1440px (multi-column grids, full-width optimization)

### Layout Adjustments by Breakpoint

**Mobile (375px)**
- Single column
- 16px margins
- Full-width buttons
- Stacked cards
- Bottom navigation (4 items)
- Simplified headers

**Tablet (768px)**
- 2-column grid (optionally)
- 24px margins
- Side-by-side buttons where appropriate
- 2-column card layout
- Increased padding
- Horizontal tabs

**Desktop (1440px)**
- Multi-column grids (2–4 columns)
- 48px margins
- Horizontal layouts
- Sidebar navigation (optional)
- Increased spacing
- Full-width hero sections

---

## 11. Design Tokens Reference

All numeric values use multiples of 8px base unit:

```
Spacing: 8px, 16px, 24px, 32px, 48px, 64px, 80px
Radius: 4px, 8px, 12px, 16px, 24px
Shadows: 
  - Elevation 1: 0 1px 3px rgba(0,0,0,0.08)
  - Elevation 2: 0 2px 6px rgba(0,0,0,0.12)
  - Elevation 3: 0 4px 12px rgba(0,0,0,0.12)
  - Elevation 4: 0 8px 24px rgba(0,0,0,0.16)
```

---

## 12. Quality Checklist

Before finalizing each SVG screen:

- [ ] All text uses approved fonts (Poppins / Baloo 2)
- [ ] All colors from approved palette (no off-brand colors)
- [ ] Contrast ratios meet WCAG AA (4.5:1 minimum for body text)
- [ ] Touch targets all 44px+ minimum
- [ ] Responsive layouts verified for all three breakpoints
- [ ] Icon set consistent (size, weight, style)
- [ ] Spacing follows 8px grid throughout
- [ ] No placeholder text (all content populated)
- [ ] SVG file size optimized (<100KB)
- [ ] Layers organized logically
- [ ] Button states documented (default, hover, active, disabled)
- [ ] Empty states handled gracefully
- [ ] Loading states (spinners, skeletons) included where needed

---

**Design System Created:** July 2025
**Last Updated:** July 2025
**Status:** Active for Production
