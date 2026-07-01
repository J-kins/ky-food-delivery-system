# Screen Inventory — Food Delivery System

Every screen below names a **Pattern** (letter, see `layout-patterns.md`) and a
**Priority**:

- 🔴 **REQUIRED** — the 5 screens the lecturer explicitly named. Never skip these.
- 🟠 **CORE** — needed for a believable, clickable end-to-end flow per role.
  Build these unless time is extremely short.
- 🟡 **RECOMMENDED** — rounds the system out and is what separates a
  distinction-level submission from a pass. Build if time allows.
- ⚪ **STRETCH** — genuinely optional, enterprise-grade extras. Only attempt
  once everything above is done.

If you're short on time, build top-to-bottom in priority order, not
role-by-role — i.e. finish all 🔴 then all 🟠 across every role before
touching any 🟡.

Total: ~95 screens. Items marked **(NEW)** were not in the original brief and
are added here to round out the system — flag these to the human after the
diagram is built, in case some are out of scope for the assignment.

---

## 0. Shared / Onboarding & Auth

| # | Screen | Pattern | Priority | Layout notes |
|---|---|---|---|---|
| 1 | Splash Screen | — | 🟡 | Just logo centered on a blank frame, no chrome. |
| 2 | Onboarding / Walkthrough **(NEW)** | B | 🟡 | 3 frames, same layout, different illustration+copy. |
| 3 | Welcome Screen | A (simplified) | 🟡 | Logo + tagline + 3 stacked buttons: Login / Sign Up / Continue as Guest. |
| 4 | **Login Screen** | A | 🔴 | See Pattern A exactly. |
| 5 | Registration Screen | A | 🟠 | Same as Login but fields: Name, Email, Phone, Password, Confirm Password; checkbox "I agree to Terms". |
| 6 | OTP Verification Screen | A (OTP variant) | 🟠 | 6 digit boxes + countdown + Resend link. |
| 7 | Forgot Password Screen | A (1 field) | 🟡 | Just an email/phone field + "Send Reset Code" button. |
| 8 | Reset Password Screen | A (2 fields) | 🟡 | New Password + Confirm Password fields. |
| 9 | Set Delivery Location **(NEW)** | full-bleed map + pin | 🟠 | Map placeholder fills frame, center pin icon, search bar floats on top, bottom sheet card with address text + "Confirm Location" button. |
| 10 | Notification Permission Prompt **(NEW)** | M | ⚪ | One-line system dialog. |

---

## 1. Customer — Home & Discovery

| # | Screen | Pattern | Priority | Layout notes |
|---|---|---|---|---|
| 11 | Home Dashboard | C | 🟠 | The natural landing screen after login; not one of the 5 named screens but expected in any flow diagram. |
| 12 | Search Screen | C | 🟠 | Search bar focused, list below shows recent/trending searches before typing. |
| 13 | Search Results | C | 🟡 | Same shell, results list + a "Filter / Sort" pill button top-right that opens #14. |
| 14 | Filters & Sort Modal **(NEW)** | J | 🟡 | Checkboxes for cuisine, price range slider, rating filter, sort radio group (Relevance / Rating / Delivery Time). |
| 15 | Food Categories Screen | C (grid variant) | 🟡 | 2-column grid of category tiles instead of a list. |
| 16 | Restaurant List Screen | C | 🟠 | Standard card list per Pattern C. |
| 17 | Restaurant Details Screen | D | 🟠 | Hero image, name/rating/hours, tabs for "Menu / Reviews / Info", scrollable menu list below, sticky "View Cart" bar if cart non-empty. |

## 2. Customer — Ordering

| # | Screen | Pattern | Priority | Layout notes |
|---|---|---|---|---|
| 18 | **Food Menu Screen (with prices)** | D or C-within-D | 🔴 | List of menu items grouped by category, each row: thumbnail, name, short description, price, "+" add button. This is the required screen — keep prices visibly aligned right on every row. |
| 19 | **Food Details Screen** | D | 🔴 | Full Pattern D including size options, add-ons checkboxes, quantity stepper, sticky "Add to Cart — $X" button that updates live with selections. |
| 20 | Cart Screen | E | 🟠 | Pattern E exactly. |
| 21 | Promo Code Entry **(NEW)** | inline row on E, or J if modal | 🟡 | Text field + "Apply" button inline in the Cart screen; on success show a confirmation line "Promo applied: -$2.00". |
| 22 | Checkout Screen | E (checkout variant) | 🟠 | Address card + payment method card + price summary + "Place Order" CTA. |
| 23 | **Payment Screen** | F | 🔴 | Pattern F exactly — radio list of Mobile Money / Card / Cash, expanding detail fields, fixed total + Pay Now. |
| 24 | Add/Edit Payment Method **(NEW)** | J | 🟡 | Modal form: card number, expiry, CVV OR mobile money number, with a "Set as default" checkbox. |
| 25 | Payment Confirmation Screen | F (confirmation variant) | 🟠 | Success icon, order #, amount, Track Order / Back Home buttons. |

## 3. Customer — Order Management

| # | Screen | Pattern | Priority | Layout notes |
|---|---|---|---|---|
| 26 | **Order Status / Current Orders Screen** | G | 🔴 | Pattern G, hide driver card until a rider is assigned. This screen plus #32 together satisfy "receive order status notifications". |
| 27 | Order Tracking Screen | G (full) | 🟠 | Pattern G with map + driver card fully populated. |
| 28 | Tip the Rider **(NEW)** | inline card or J | ⚪ | Row of preset amount chips (+$1/$2/$5) + custom field + Skip link. |
| 29 | Order History Screen | C (simplified card) | 🟠 | Each row: restaurant name, date, item count, total, status badge, "Reorder" button. |
| 30 | Order Details Screen (past order) | D (read-only variant) | 🟡 | Itemized list, totals, status timeline (all steps filled), no action buttons except Reorder/Help. |
| 31 | Rate & Review Screen **(NEW)** | J or full-screen form | 🟡 | Star rating row (large, tappable), optional tag chips ("Fast delivery", "Cold food"), comment text box, Submit button. |
| 32 | Notification Center | C (notification card variant) | 🟠 | List of notification rows: icon, message, timestamp, unread = bold/dot. Pairs with #26 to fully satisfy the "order status notifications" requirement. |
| 33 | Report a Problem / Refund Request **(NEW)** | J | 🟡 | Order summary recap at top, reason dropdown (Missing item / Wrong order / Late / Quality), comment box, photo-upload placeholder, Submit. |

## 4. Customer — Account & Support

| # | Screen | Pattern | Priority | Layout notes |
|---|---|---|---|---|
| 34 | Profile Screen | D (read-only) | 🟠 | Avatar circle top, name/email/phone rows, list of menu rows linking to Addresses/Payment/Favorites/Settings/Help/Logout. |
| 35 | Edit Profile Screen **(NEW)** | J or full-screen form | 🟡 | Avatar with edit overlay, editable Name/Email/Phone fields, Save button. |
| 36 | Saved Addresses Screen | C (simplified) | 🟡 | List of address cards (label icon Home/Work/Other, address text, Edit/Delete icons), "+ Add New Address" row at bottom. |
| 37 | Add/Edit Address **(NEW)** | same as #9 + J | 🟡 | Map pin picker + label radio (Home/Work/Other) + address text field + Save. |
| 38 | Favorite Foods Screen | C (grid) | ⚪ | Grid of food cards with filled heart icon. |
| 39 | Favorite Restaurants Screen | C (grid) | ⚪ | Same as above, restaurant cards. |
| 40 | Wallet / Loyalty Points **(NEW)** | C (transaction list) + KPI header | ⚪ | Big balance number top, "Top Up" button, scrollable transaction history list below. |
| 41 | Settings Screen | C (simplified, no images) | 🟡 | Grouped list rows: Language, Theme, Notification toggles (switches, not checkboxes), Logout, Delete Account. |
| 42 | Help & Support / FAQ Screen | C (accordion list) | 🟡 | Search bar + expandable FAQ rows; "Still need help? Chat with us" CTA at bottom linking to #43. |
| 43 | Live Chat with Support **(NEW)** | K | 🟡 | Pattern K exactly. |
| 44 | Empty States **(NEW, reusable)** | L | 🟠 | Build once, reuse for: empty cart, no orders, no notifications, no search results, no favorites. |

---

## 5. Kitchen Staff (treat as web/tablet console)

| # | Screen | Pattern | Priority | Layout notes |
|---|---|---|---|---|
| 45 | Kitchen Staff Login | A (desktop-width variant) | 🟠 | Same field stack as Pattern A, centered in a 1440×900 frame instead of a phone frame. |
| 46 | Kitchen Dashboard | H | 🟠 | KPI cards: Pending / Preparing / Completed Today / Avg Prep Time. |
| 47 | Incoming Orders Screen | I (no Add button) | 🟠 | Table or kanban columns: order #, items, time received, "Accept" button per row. |
| 48 | Order Preparation Screen | D-like detail panel | 🟠 | Right-hand detail panel (or modal) showing full item list/recipe notes, Start / Pause / Complete buttons. |
| 49 | Kitchen Queue Screen | I (kanban variant) | 🟡 | Three columns: Pending → Preparing → Ready, order cards as tiles. |
| 50 | Mark Item Out of Stock **(NEW)** | I row toggle | ⚪ | Menu item list with an "In Stock / Out of Stock" switch per row. |
| 51 | Kitchen Notifications Screen | C (list) | ⚪ | Simple alert list: "New order #1023 received". |

## 6. Delivery Rider (mobile app)

| # | Screen | Pattern | Priority | Layout notes |
|---|---|---|---|---|
| 52 | Rider Login Screen | A | 🟠 | Pattern A. |
| 53 | Rider Registration / KYC **(NEW)** | A (multi-step form) | 🟡 | Stepped form: personal info → vehicle info → ID/license photo upload placeholders → Submit for review. |
| 54 | Rider Dashboard | G-like home / H-lite | 🟠 | Online/Offline toggle switch top, today's earnings summary card, list of nearby/available delivery requests below. |
| 55 | New Delivery Request **(NEW, but implied)** | J (bottom sheet) | 🟠 | Bottom sheet slides up: pickup/dropoff addresses, distance, payout amount, countdown ring, Accept / Decline buttons. |
| 56 | Delivery Details Screen | D (read-only) | 🟠 | Customer name/phone, pickup address, dropoff address, order items, Call/Chat icons. |
| 57 | Navigation / Map Route Screen | full-bleed map | 🟠 | Map fills frame, route line, bottom card with next-step instruction + ETA + "Arrived" button. |
| 58 | In-app Chat with Customer **(NEW)** | K | 🟡 | Pattern K. |
| 59 | Proof of Delivery **(NEW)** | D-like form | 🟡 | Camera placeholder square ("Tap to take photo") or signature pad placeholder, "Confirm Delivery" button. |
| 60 | Delivery Status Screen | G | 🟠 | Pattern G, customer info instead of driver info, "Mark Picked Up / Mark Delivered" buttons instead of Call/Chat. |
| 61 | Rider Earnings Screen | C (transaction list) + KPI header | 🟡 | Big total at top with Day/Week/Month toggle tabs, list of completed deliveries with payout per row below. |
| 62 | Rider Profile / Vehicle Info **(NEW)** | D (read-only) | ⚪ | Avatar, name, rating, vehicle type/plate, documents status list. |

## 7. Restaurant Manager (web dashboard)

| # | Screen | Pattern | Priority | Layout notes |
|---|---|---|---|---|
| 63 | Manager Login | A (desktop-width) | 🟡 | Same as #45. |
| 64 | Manager Dashboard | H | 🟠 | KPI cards: Today's Orders / Today's Revenue / Top-Selling Item / Avg Prep Time. |
| 65 | Menu Management Screen | I | 🟠 | Table of menu items: image thumb, name, category, price, in-stock toggle, edit/delete icons, "+ Add Item" top-right. |
| 66 | Add/Edit Menu Item **(NEW)** | J | 🟠 | Form fields: name, description, price, category dropdown, image upload placeholder, add-on options builder. |
| 67 | Inventory Screen | I | 🟡 | Table: ingredient, current stock, unit, low-stock badge when below threshold. |
| 68 | Operating Hours & Closures **(NEW)** | I (simple list) or J | 🟡 | Day-of-week rows each with open/close time pickers and a toggle for "Closed today" / holiday banner. |
| 69 | Staff Management Screen | I | 🟡 | Table: staff name, role (Kitchen/Manager), status, edit/remove icons, "+ Add Staff". |
| 70 | Promotions Screen | I | 🟡 | Table of active/expired promo codes: code, discount, valid dates, usage count, "+ New Promotion". |
| 71 | Reviews Screen | C-like list (desktop width) | 🟡 | List of review cards: customer name, star rating, comment, "Reply" link/textbox. |
| 72 | Payout / Earnings Report **(NEW)** | H (chart) + I (table) | ⚪ | Chart of revenue over time + table of payout transactions. |

## 8. Administrator (web dashboard)

| # | Screen | Pattern | Priority | Layout notes |
|---|---|---|---|---|
| 73 | Admin Login | A (desktop-width) | 🟡 | Same as #45. |
| 74 | Admin Dashboard | H | 🟠 | This is exactly what `assets/pattern-templates.drawio` already builds for you — copy it directly. |
| 75 | User Management Screen | I | 🟠 | Table: name, email, role, status, "Suspend/Activate" + edit icons. |
| 76 | Restaurant Management Screen | I | 🟠 | Table: restaurant name, owner, status (Pending/Approved/Suspended), "Approve/Suspend" action buttons. |
| 77 | Food / Menu Moderation Screen | I | ⚪ | Table of flagged menu items pending review, Approve/Reject buttons. |
| 78 | Order Monitoring Screen | I | 🟡 | Global table of all orders across all restaurants, status filter row. |
| 79 | Delivery Monitoring Screen | full-bleed map + I | 🟡 | Map placeholder showing rider pins + a side list of active deliveries. |
| 80 | Payment Monitoring Screen | I | 🟡 | Table: transaction ID, amount, method, status (Success/Failed/Refunded). |
| 81 | Analytics Dashboard | H (multiple charts) | 🟡 | 4 chart placeholders in a 2×2 grid: Revenue Trend, Order Volume, Top Restaurants, User Growth. |
| 82 | Notification / Broadcast Management **(NEW)** | J | ⚪ | Form: audience dropdown (All Users/Riders/Restaurants), title, message body, "Send Now" / "Schedule" buttons. |
| 83 | Reports Module | I (filters + export) | ⚪ | Date range picker, report-type dropdown, "Export CSV/PDF" button, preview table below. |
| 84 | System Configuration Screen | settings form (full page, not modal) | ⚪ | Grouped sections: Tax Rate, Delivery Fee Rules, Payment Gateway Keys, each with input fields and a Save button per section. |
| 85 | Roles & Permissions Screen **(NEW)** | I | ⚪ | Table: role name, list of permission checkboxes per module, "+ New Role". |
| 86 | Delivery Zones / Geofencing **(NEW)** | full-bleed map + J | ⚪ | Map with drawn zone outlines, side panel listing zone name + delivery fee + edit/delete. |

## 9. Customer Support (web dashboard)

| # | Screen | Pattern | Priority | Layout notes |
|---|---|---|---|---|
| 87 | Support Login | A (desktop-width) | 🟡 | Same as #45. |
| 88 | Support Dashboard | H | 🟡 | KPI cards: Open Tickets / Avg Response Time / Resolved Today / Escalated. |
| 89 | Ticket List Screen | I | 🟡 | Table: ticket #, customer, subject, priority badge, status, assigned agent. |
| 90 | Ticket Details Screen | D-like (desktop) | 🟡 | Left: ticket info + customer/order context panel. Right: message thread (Pattern K) for replying. |
| 91 | Live Chat Screen (agent side) | K + side context panel | ⚪ | Pattern K, plus a right-hand panel showing the customer's profile/order history. |
| 92 | Complaint Resolution Screen | full form | ⚪ | Resolution-type dropdown (Refund/Replacement/Apology Credit/No Action), amount field if refund, internal notes box, "Resolve Ticket" button. |
| 93 | Customer Lookup Screen **(NEW)** | I (search-first) | ⚪ | Search bar by name/email/phone/order #, results table, click-through to that customer's order history. |

---

## 10. System-wide states (build once, reuse everywhere)

| # | Screen | Pattern | Priority | Layout notes |
|---|---|---|---|---|
| 94 | Error / No Internet **(NEW)** | centered illustration | 🟡 | Illustration + "No internet connection" heading + "Retry" button — same shell as Pattern L. |
| 95 | Confirm/Delete Dialog **(NEW)** | M | 🟡 | "Delete this address? This can't be undone." + Cancel/Delete buttons. |

---

## Mapping back to the lecturer's required 5

| Lecturer requirement | Screen(s) in this inventory |
|---|---|
| 1. Login | #4 |
| 2. View food list with prices | #18 |
| 3. Select food | #19 (and #20 Cart as the immediate next step) |
| 4. Make payment | #23 |
| 5. Receive order status notifications | #26 + #32 together |
