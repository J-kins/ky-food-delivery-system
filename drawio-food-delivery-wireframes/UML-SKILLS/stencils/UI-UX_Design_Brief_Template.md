# UI/UX Design Brief Template

**Project Name:** [e.g., E-commerce Product Page Redesign]  
**Date:** [Insert Date]  
**Version:** 1.0  
**Prepared by:** [Your Name / Role]

## 1. Project Overview & Objectives
- **Goal**: [Clearly state the high-level objective, e.g., "Create a modern, conversion-focused product detail page that improves user engagement and reduces bounce rate."]
- **Business & UX Objectives**: Increase **conversion rate**, improve **task success rate**, enhance **user engagement**, and ensure excellent **readability** and **legibility** across devices.
- **Scope**: [e.g., Homepage, Product Listing, Checkout Flow, etc.]
- **Success Metrics**:
  - Target **Click-Through Rate (CTR)**, **Conversion Rate**, **Time on Task**, **Task Success Rate**, and reduced **Bounce Rate**.
  - Aim for **Net Promoter Score (NPS)** improvement through better **affordance** and **microinteractions**.

## 2. Target Audience & Research Insights
- **Personas**: [Describe 2–3 primary **personas**, e.g., "Budget-conscious Brenda (35–45, mobile-first) and Power-user Pete (tech-savvy, desktop)."]
- **User Needs & Pain Points**: [Based on **usability testing**, **heuristic evaluation**, or **user journey** mapping.]
- **Key Scenarios / Use Cases**: Detail main **user flows** and **user journeys** (e.g., Browse → View Product → Add to Cart → Checkout).

## 3. Design Requirements

### Navigation & Information Architecture
- **Sitemap**: [Provide or reference a hierarchical diagram of all screens/pages and their parent–child relationships before wireframing begins.]
- **Navigation Schema**: Define **primary navigation**, **secondary navigation**, **utility navigation** (login, settings), **breadcrumbs**, and **search** placement across breakpoints.
- **Taxonomy**: [Define content categories, sub-categories, and labelling conventions — e.g., product categories, filter labels, blog tags — so navigation and search reflect users' language, not internal jargon.]
- **Content Hierarchy**: Map what information is most important per page/screen; this directly drives typographic weight, layout, and visual hierarchy decisions.
- **Card Sorting / Tree Testing**: [Specify whether research methods are required to validate navigation labels and groupings before design begins.]
- **Mental Models**: Align structure and labels with users' expectations uncovered in **usability research**, competitor benchmarking, and persona analysis.

### Layout & Responsive Design
- Use a flexible **grid** system (12-column on desktop, collapsing at **breakpoints**) with consistent **alignment**, **margins**, and **padding**.
- Implement **responsive design** (mobile-first) with proper **viewport** meta tag.
- Containers and **cards** should group related content with appropriate **gutters**.
- Manage overlapping elements with thoughtful **z-index** usage (e.g., modals, tooltips).

### Typography
- **Font Family**: [e.g., Primary: Sans-serif (Helvetica/Arial), Secondary: Serif for headings if needed].
- Ensure good **line height (leading)**, **kerning**, **x-height**, and **cap height** for optimal **readability** and **legibility**.
- Use **bold** sparingly for emphasis. Maintain a consistent **baseline** grid.

### Colour Schema & Visual Hierarchy
- **Color Harmony Approach**: [Select one: **Monochromatic** (one hue, varied lightness & saturation — safe and unified) / **Analogous** (neighbouring hues — calm and cohesive) / **Complementary** (opposite hues — high contrast, use sparingly) / **Split-Complementary** (softer alternative to complementary) / **Triadic** (three evenly spaced hues — vibrant and balanced) / **Tetradic** (four hues — rich but requires careful dominance balance).]
- **Color Models**: Work in **HEX** / **HSL** within design tools (Figma, Sketch). Provide **RGB** equivalents for front-end handoff. Avoid CMYK in digital contexts.
- **Color Palette**: Define **primary**, **secondary**, and **accent color**, plus a **neutral color scale** (e.g., `gray-50` through `gray-950`) with **tints**, **shades**, and **tones** for each core hue.
- **Semantic Color Mapping**: Assign functional colors for system feedback — **error / danger** → [red], **warning** → [amber], **success** → [green], **info** → [blue]. Implement as named **design tokens** (e.g., `color.feedback.error`) so they adapt automatically across themes.
- **Dark Mode / Light Mode**: [Light only / Dark only / Both.] If both modes are required, each design token must map to a separate value per scheme. All **contrast ratios** must be tested and pass independently in each mode. Support `prefers-color-scheme` in CSS.
- **Color Psychology Rationale**: [Brief note on emotional/brand intent — e.g., "Blue conveys trust for a fintech audience; amber accent adds energy without aggression."]
- **Contrast Ratio**: Minimum **4.5:1** for normal body text, **3:1** for large text (18pt+ or 14pt+ bold), and **3:1** for non-text UI elements (icons, input borders, focus rings) per WCAG AA (1.4.3 & 1.4.11).
- Use **gradients** and **opacity** judiciously; always verify contrast of any text placed over a gradient or semi-transparent background.

### Interaction & Microinteractions
- Strong **affordance** on all interactive elements (**buttons**, links, **sliders**).
- Define states: **hover**, **focus**, **active**, **disabled**.
- Include subtle **microinteractions** (e.g., button ripple, toggle switch animation).
- Support **drag and drop** where relevant.

### Motion & Animation
- **Transition Durations**: Micro-interactions (hover tint, ripple) → **100–200 ms**; layout transitions (panel slide, modal open) → **250–400 ms**; complex multi-step sequences → up to **600 ms**. Single-element transitions beyond 500 ms will feel sluggish.
- **Easing**: Default to **ease-out** for elements entering the view (decelerates — feels natural); **ease-in** for exits; **ease-in-out** for elements shifting position. Avoid **linear** easing on UI elements (feels mechanical). Specify custom `cubic-bezier` values for any brand-specific motion signature.
- **Skeleton Screens**: Required for all data-fetching views. Skeleton placeholder shapes must closely mirror the layout of the content they precede. Do not use generic spinners as the sole loading indicator for content-heavy views.
- **Keyframe Animations**: [List any looping or multi-step animations — e.g., loading spinner, onboarding illustration, empty-state animation.]
- **Parallax / Depth Effects**: [Yes / No.] If yes, must be disabled or replaced with a non-motion alternative under `prefers-reduced-motion`.
- **Reduced Motion**: All animations must honour `@media (prefers-reduced-motion: reduce)` — substitute with instant state changes or opacity-only fades. Required per WCAG 2.1 SC 2.3.3 for users with vestibular sensitivities or motion-triggered conditions.

### UI Components & Patterns
- Core components: **Buttons** (primary/secondary), **Cards**, **Input Controls** (text fields, **checkbox**, **radio button**, **slider**), **Dropdowns**, **Tabs**, **Accordion**, **Breadcrumbs**, **Badges**, **Progress Indicators**.
- Navigation: **Navbar**, **hamburger menu** (mobile), **mega menu** (desktop if needed).
- Feedback: **Toast / Snackbar**, **Modal / Dialog**, **Tooltip / Popover**.
- Advanced patterns: **Progressive disclosure**, **Wizard** (for multi-step flows), **Infinite Scroll** or **Pagination**, **Responsive Table**.

### UI States
Every interactive component and data-dependent view must be designed for each applicable state. Include a **state matrix** in deliverables — one Figma frame per component × state.

| State | When it applies | Design requirement |
|---|---|---|
| **Default** | Resting; no interaction | Shown in all primary mockups |
| **Hover** | Pointer over element (desktop only) | Subtle colour shift or elevation; not applicable on touch-only |
| **Focus** | Keyboard focus via Tab key | Visible ring or outline — never remove without a custom replacement (WCAG 2.4.7 / 2.4.11) |
| **Active** | Element being pressed | Pressed / depressed visual (`:active`) |
| **Disabled** | Action currently unavailable | Muted appearance; communicate *why* via tooltip; use `aria-disabled` on custom controls to preserve tab focus |
| **Loading** | Data fetching / process running | Spinner, progress bar, or **skeleton screen** — choose per context and content shape |
| **Empty** | No content to display | Explain *why* it's empty + clear next action (e.g., "No saved items yet. Start browsing →") |
| **Error** | Action failed / invalid input | Semantic red, error icon, plain-language message describing what went wrong and how to fix it |
| **Success** | Action completed | Green / check icon / **toast notification**; confirm what was completed |

### Accessibility (WCAG 2.1 AA Compliance)
- Follow **POUR** principles (**Perceivable**, **Operable**, **Understandable**, **Robust**).
- Provide **alt text**, proper **ARIA** roles/labels, logical **tab order**, **keyboard accessible** controls, and **semantic HTML**.
- Ensure **color contrast**, focus indicators, and screen reader compatibility.

## 4. Design System & Consistency
- Adopt or extend an **Atomic Design** methodology.
- Use **design tokens** for colors (including **semantic color tokens** and per-theme values), spacing, typography, border-radius, and shadow.
- Maintain a **color token map** that documents light-mode and dark-mode values for every token.
- Define **motion tokens** for standard durations and easing values (e.g., `motion.duration.short: 150ms`, `motion.easing.exit: ease-in`).
- Reference **Component Library**, **Style Guide**, and **Pattern Library**.
- Ensure **theme** support (light / dark mode) via token switching.
- Document all **navigation schema** and **taxonomy** decisions in the design system alongside component specs.

## 5. Prototyping & Deliverables
- **Wireframes** and **wireflows** (low-fidelity), including a **sitemap** diagram.
- **Click-through Prototype** (mid-fidelity).
- **High-Fidelity Prototype** / **Mockups** with interactions, including dark mode variants if required.
- **State matrix**: one Figma frame per component × UI state (default, hover, focus, active, disabled, loading, empty, error, success).
- **Motion spec sheet**: document transition durations, easing values, and `prefers-reduced-motion` alternatives for all animated components.
- Final assets: Figma/Sketch files, exported **SVG** icons, **Elementor** JSON-compatible structure (if applicable), and front-end code guidelines (**HTML**, **CSS Grid/Flexbox**, **JavaScript**).

## 6. Technical / Front-End Considerations
- **Responsive Web Design (RWD)** with **media queries** at defined **breakpoints**.
- **Semantic HTML**, **ARIA**, **progressive enhancement**.
- Performance: Lazy loading, optimized assets, good **FPS** for animations.
- **CSS transitions & animations**: implement easing via `transition-timing-function` / `cubic-bezier`; use `@keyframes` for looping animations.
- **Dark mode**: implement via `prefers-color-scheme` media query and/or a `.dark` class toggle; all **design tokens** must resolve correctly in both modes.
- **Reduced motion**: wrap all non-essential animations in `@media (prefers-reduced-motion: reduce)` blocks.
- Cross-browser compatibility and **Retina Display** support.

## 7. Constraints & Assumptions
- [e.g., Brand guidelines, tech stack, timelines, Elementor/WordPress integration, etc.]
- Avoid: Overuse of **z-index**, poor contrast, non-keyboard accessible elements.

## 8. Iteration & Validation Plan
- Conduct **heuristic evaluation**, **usability testing**, and **A/B testing**.
- **Iterate** based on **Fitts’s Law** and **Hick’s Law** principles.
- Final validation against success metrics.

**Approval Signatures:**  
[Stakeholder / Product Manager] ____________________ Date: ________

---

**How to use this brief:**
- Fill in the placeholders with your project details.
- Use it as a system prompt for **agentic AI** tools.
- Share with designers, developers, or stakeholders.
- Customize further for specific needs (e.g., Elementor integration).