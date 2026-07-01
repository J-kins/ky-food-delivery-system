# Layout Pattern Library

Don't design all ~90 screens from scratch. Almost every screen in this system is
a variant of one of the **13 patterns** below. Build each pattern once as a
frame, then duplicate/relabel it for every screen that uses it. The example
templates in `assets/pattern-templates.drawio` already implement Patterns A, C,
and H+I — start by opening that file and reading it.

Two canvas sizes only:
- **Mobile frame: 360 × 780px** — Customer app, Rider app, Kitchen tablet (if
  treated as mobile).
- **Desktop frame: 1440 × 900px** — Restaurant Manager, Admin, Support web
  dashboards, and Kitchen if treated as a web/tablet console.

Style is **low-fidelity / grayscale on purpose** — see `drawio-xml-guide.md`
for the exact style strings. Don't add real icons, photography, or brand
colors. The one allowed accent color (`#4A6FA5`, muted steel blue) marks
primary buttons and links only, so a reviewer can spot interactive elements at
a glance.

---

## A. AUTH_FORM (mobile)
Logo/illustration → heading → stacked input fields → primary button → secondary link.

```
┌─────────────────────────┐
│        9:41              │ status bar
│                           │
│      [ LOGO / ILLUS ]    │
│                           │
│      Welcome Back        │ heading
│   Log in to continue...  │ subtext
│ ┌───────────────────────┐│
│ │ Email / Phone         ││ input field
│ └───────────────────────┘│
│ ┌───────────────────────┐│
│ │ Password               ││ input field
│ └───────────────────────┘│
│                Forgot? → │ link, right-aligned
│ ┌───────────────────────┐│
│ │      LOG IN            ││ primary button (filled)
│ └───────────────────────┘│
│ ┌───────────────────────┐│
│ │  Continue as Guest     ││ outline button
│ └───────────────────────┘│
│   Don't have an account? │ link, centered
└─────────────────────────┘
```
**Used by:** Login, Registration, Forgot Password, Reset Password.
**OTP variant:** replace the field stack with 4–6 individual square boxes
(48×48, evenly spaced) for digit entry, plus a "Resend code in 00:30" countdown
text under the boxes.

---

## B. ONBOARDING_SLIDE (mobile)
Full-bleed illustration, headline, dot pagination, skip/next controls.

```
┌─────────────────────────┐
│ Skip                     │ top-right, small link
│                           │
│   [ FULL ILLUSTRATION ]  │ ~55% of screen height
│                           │
│   Order food in minutes  │ headline, centered
│   Track every step...    │ subtext, centered
│        • ○ ○              │ dot pagination
│ ┌───────────────────────┐│
│ │        Next            ││ primary button
│ └───────────────────────┘│
└─────────────────────────┘
```
**Used by:** Onboarding/Walkthrough (3 slides, same frame, swap text+illustration).

---

## C. LIST_BROWSE (mobile)
Top bar → optional search/filter row → optional chip row → scrollable list or
grid of cards → bottom tab bar.

```
┌─────────────────────────┐
│ Deliver to: Home ▾  🔔 🛒│ top bar
│ ┌───────────────────────┐│
│ │ 🔍 Search...           ││ search field
│ └───────────────────────┘│
│ [Pizza][Burgers][Drinks] │ filter/category chips
│ ┌───────────────────────┐│
│ │   PROMO BANNER         ││ optional banner
│ └───────────────────────┘│
│ Popular Restaurants      │ section label
│ ┌─────┬─────────────────┐│
│ │ IMG │ Name  ★4.5  25m  ││ card, repeats
│ └─────┴─────────────────┘│
│ ┌─────┬─────────────────┐│
│ │ IMG │ Name  ★4.2  30m  ││
│ └─────┴─────────────────┘│
│  Home  Search  Orders  ♡ 👤│ bottom tab bar (active tab bold/accent)
└─────────────────────────┘
```
**Used by:** Home, Restaurant List, Food Categories, Search Results, Order
History, Favorite Foods/Restaurants, Notification Center, Wallet transaction
list, Ticket List (mobile variant).
**Notes per use:** Home adds the promo banner + chip row; History/Notifications
drop the chips and use a simpler card (no image, just text + status badge);
Favorites uses a 2-column grid instead of a single-column list.

---

## D. DETAIL_PAGE (mobile)
Hero image → back button overlay → title/meta block → scrollable body →
sticky bottom action bar.

```
┌─────────────────────────┐
│ ←        [ HERO IMAGE ] │ back button floats over image
│                           │
│ Restaurant / Food Name   │ title
│ ★4.5 (320)  ·  25-35 min │ meta row
│ ─────────────────────── │
│ Description text runs    │
│ here, wraps multiple      │ scrollable body
│ lines...                  │
│ Size:  (S) (M) (L)       │ option group (food detail only)
│ Add-ons: ☐ Cheese ☐ Bacon│ checkboxes (food detail only)
│ Qty:  [-]  1  [+]        │ stepper (food detail only)
│ ┌───────────────────────┐│
│ │  Add to Cart — $12.50  ││ sticky bottom CTA, shows running price
│ └───────────────────────┘│
└─────────────────────────┘
```
**Used by:** Restaurant Details, Food Details (with the option/add-on/qty
rows — these are the extra components that make this the "Select food" required
screen), Order Details (past order — body becomes a read-only item list +
status history, sticky bottom shows "Reorder" instead), Ticket Details.

---

## E. CART_CHECKOUT (mobile)
Title bar → scrollable line items → summary block → sticky bottom CTA.

```
┌─────────────────────────┐
│ Your Cart            Edit│
│ ┌───┬───────────┬──────┐ │
│ │IMG│ Item name  │ [-1+]│ │ line item, repeats
│ │   │ $8.00      │  🗑  │ │
│ └───┴───────────┴──────┘ │
│  Have a promo code?  [Apply]│ promo input row
│ ─────────────────────── │
│ Subtotal        $16.00  │
│ Delivery Fee     $2.00  │ summary block, right-aligned values
│ Tax              $1.20  │
│ Total           $19.20  │ bold
│ ┌───────────────────────┐│
│ │   Proceed to Checkout  ││ sticky bottom CTA
│ └───────────────────────┘│
└─────────────────────────┘
```
**Checkout variant** inserts two tappable summary cards above the price
summary: a **Delivery Address card** (pin icon, address text, "Change" link)
and a **Payment Method card** (selected method, "Change" link), then the CTA
label becomes "Place Order".
**Used by:** Cart, Checkout.

---

## F. PAYMENT (mobile)
Radio list of payment methods → expanding detail for the selected one → fixed
total recap → CTA.

```
┌─────────────────────────┐
│ Select Payment Method    │
│ ○ Mobile Money            │
│ ● Card                    │ selected method, filled radio
│   ┌─────────────────────┐│
│   │ Card Number          ││ detail fields appear only for
│   │ Expiry      CVV      ││ the selected method
│   └─────────────────────┘│
│ ○ Cash on Delivery        │
│ ─────────────────────── │
│ Total to Pay     $19.20  │ fixed recap, bottom
│ ┌───────────────────────┐│
│ │       Pay Now           ││ primary CTA — this is the
│ └───────────────────────┘│ required "Make Payment" screen
└─────────────────────────┘
```
**Confirmation variant:** replace everything above the fold with a centered
success check icon, "Order Placed!", order number, amount, and two buttons:
**Track Order** (primary) / **Back to Home** (outline).
**Used by:** Payment, Payment Confirmation, Add/Edit Payment Method (this one
is actually a FORM_MODAL — see pattern J — not this pattern).

---

## G. STATUS_TRACKING (mobile)
Map area on top → vertical stepper/timeline → driver info card → help/tip area.

```
┌─────────────────────────┐
│ Order #10234              │
│ ┌───────────────────────┐│
│ │     [ MAP / ROUTE ]    ││ map placeholder, ~35% height
│ └───────────────────────┘│
│ ●  Order Placed   12:01  │ stepper, filled = done
│ ●  Preparing       12:04 │
│ ○  Picked Up        --   │ hollow = pending
│ ○  Delivered         --   │
│ ─────────────────────── │
│ 👤 Driver Name  ★4.8     │ driver card
│           [Call] [Chat]  │ action icons
│ ┌───────────────────────┐│
│ │   Add a Tip / Help     ││ secondary actions
│ └───────────────────────┘│
└─────────────────────────┘
```
**Used by:** Order Tracking, Order Status / Current Orders (this is the
required "receive order status" screen — the version shown right after
placing an order, before a driver is assigned, can hide the driver card),
Rider's own "Delivery Status" screen (same shell, customer info instead of
driver info, with **Mark Picked Up / Mark Delivered** buttons instead of
Call/Chat).

---

## H. DASHBOARD_WEB (desktop)
Sidebar nav + top bar + KPI stat-card row + chart area(s).

```
┌──────────┬──────────────────────────────────────────┐
│ FoodDash │  Dashboard Overview      🔍 search  🔔 👤 │ topbar
│ Admin    ├──────────────────────────────────────────┤
│──────────│ [Orders 1284][Riders 56][Rev 4.2M][Disp 3]│ KPI cards
│ Dashboard│ ┌────────────────┐ ┌─────────────────────┐│
│ Users    │ │ Revenue Trend  │ │ Orders by Region     ││ chart placeholders
│ Restaur. │ │ (line chart)   │ │ (map / bar chart)     ││
│ Orders   │ └────────────────┘ └─────────────────────┘│
│ Payments │                                            │
│ Reports  │                                            │
│ Settings │                                            │
│──────────│                                            │
│ Log Out  │                                            │
└──────────┴──────────────────────────────────────────┘
```
**Used by:** every *_Dashboard screen (Kitchen, Manager, Admin, Support) —
swap the sidebar nav items and KPI labels to match the role (e.g. Kitchen:
"Pending / Preparing / Completed" counts; Manager: "Today's Orders / Revenue /
Top Item / Avg Prep Time"; Support: "Open Tickets / Avg Response Time /
Resolved Today").

---

## I. DATA_TABLE_MGMT (desktop)
Same sidebar+topbar shell as H, but the body is a management table instead of
charts.

```
│ Page Title          [+ Add New]│ header row with primary action button
│ [Search...] [Filter ▾] [Status▾]│ filter bar
│ ┌────┬─────────┬───────┬──────┐│
│ │ ID │ Name    │ Status│ ⋯    ││ table header
│ ├────┼─────────┼───────┼──────┤│
│ │ 01 │ Row data│ Active│ ✎ 🗑  ││ row, edit/delete actions
│ │ 02 │ Row data│ Paused│ ✎ 🗑  ││ zebra-striped rows
│ └────┴─────────┴───────┴──────┘│
│                    « 1 2 3 »   │ pagination
```
**Used by:** User Management, Restaurant Management, Menu Management,
Inventory, Staff Management, Promotions, Order Monitoring, Payment
Monitoring, Reviews, Reports, Ticket List (web).

---

## J. FORM_MODAL (overlay, mobile or desktop)
Dimmed background + centered card with header / body / footer.

```
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  dimmed page background
░░┌─────────────────────────┐░░
░░│ Add Menu Item        ✕  │░░ header: title + close
░░│ ─────────────────────── │░░
░░│ Name        [________] │░░
░░│ Price       [________] │░░ body: form fields
░░│ Category    [________▾]│░░
░░│ Description [________] │░░
░░│ ─────────────────────── │░░
░░│        [Cancel] [Save]  │░░ footer: buttons, right-aligned
░░└─────────────────────────┘░░
```
**Used by:** Add/Edit Menu Item, Add/Edit Address, Add/Edit Payment Method,
Add/Edit User, Filters & Sort modal, Promo Code entry, Permission prompts
(smaller variant, no form fields, just message + Allow/Deny buttons).

---

## K. CHAT
Header (contact + status) → scrollable message bubbles → fixed input bar.

```
┌─────────────────────────┐
│ ← 👤 Driver Name  Online │ header
│ ─────────────────────── │
│ ┌──────────┐              │
│ │ Hi, I'm   │              │ left bubble = other person
│ │ outside    │              │
│ └──────────┘ 10:02        │
│              10:03 ┌─────┐│
│              │ On my │     │ right bubble = self
│              │ way!   │     │
│              └─────┘        │
│ ─────────────────────── │
│ [ Type a message...  ] [➤]│ fixed input bar
└─────────────────────────┘
```
**Used by:** Live Chat with Support, In-app Chat (customer ↔ rider), Support
agent Live Chat (desktop variant: add a right-hand side panel showing the
customer's order/ticket context).

---

## L. EMPTY_STATE
Centered illustration + heading + subtext + optional CTA. Drop this into the
content area of any LIST_BROWSE screen when there's no data.

```
┌─────────────────────────┐
│                           │
│      [ ILLUSTRATION ]    │
│   Your cart is empty     │ heading
│  Add items to get started│ subtext
│ ┌───────────────────────┐│
│ │   Browse Restaurants   ││ optional CTA
│ └───────────────────────┘│
│                           │
└─────────────────────────┘
```
**Used by:** empty cart, no past orders, no notifications, no search results,
no favorites, no tickets.

---

## M. SYSTEM_MODAL
Small centered card mimicking an OS-level dialog — used sparingly.

```
░░░░░░░░░░░░░░░░░░░░░░░░░░
░░ ┌─────────────────┐ ░░
░░ │  📍               │ ░░
░░ │ Allow location   │ ░░
░░ │ access?           │ ░░
░░ │   [Deny] [Allow]  │ ░░
░░ └─────────────────┘ ░░
```
**Used by:** Location permission prompt, Notification permission prompt,
generic confirm/delete dialogs ("Delete this address?").

---

## Quick lookup

| Pattern | Canvas | Letter |
|---|---|---|
| Auth form | Mobile | A |
| Onboarding slide | Mobile | B |
| List / browse | Mobile | C |
| Detail page | Mobile | D |
| Cart / checkout | Mobile | E |
| Payment | Mobile | F |
| Status / tracking | Mobile | G |
| Dashboard | Desktop | H |
| Data table management | Desktop | I |
| Form modal | Either | J |
| Chat | Either | K |
| Empty state | Either (overlay on C/E) | L |
| System modal | Either | M |
