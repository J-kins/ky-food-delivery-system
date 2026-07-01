# KY Food Delivery System
## Domain & Entity Design Document — Version 1.1 | 2025

---

> *This document defines the complete business domain model and entity structure for the KY Food Delivery System. KY Food Delivery is the dedicated online ordering and delivery platform for a **single restaurant — KY Foods**. It serves as the authoritative reference for database design, backend architecture, and system integration. Every domain, entity, attribute, and relationship is documented here to ensure consistency across all development teams.*

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Domain Architecture Map](#domain-architecture-map)
3. [Domain 01 — User Management](#domain-01--user-management)
4. [Domain 02 — Store Configuration](#domain-02--store-configuration)
5. [Domain 03 — Menu Management](#domain-03--menu-management)
6. [Domain 04 — Shopping Cart](#domain-04--shopping-cart)
7. [Domain 05 — Order Management](#domain-05--order-management)
8. [Domain 06 — Payment](#domain-06--payment)
9. [Domain 07 — Delivery](#domain-07--delivery)
10. [Domain 08 — Notifications](#domain-08--notifications)
11. [Domain 09 — Reviews & Ratings](#domain-09--reviews--ratings)
12. [Domain 10 — Promotions & Coupons](#domain-10--promotions--coupons)
13. [Domain 11 — Inventory & Kitchen](#domain-11--inventory--kitchen)
14. [Domain 12 — Administration](#domain-12--administration)
15. [Domain 13 — Reporting & Analytics](#domain-13--reporting--analytics)
16. [Domain 14 — Customer Support](#domain-14--customer-support)
17. [Domain 15 — Loyalty & Rewards](#domain-15--loyalty--rewards)
18. [Domain 16 — Delivery Zones & Geolocation](#domain-16--delivery-zones--geolocation)
19. [Domain 17 — Content Management](#domain-17--content-management)
20. [Domain 18 — Subscriptions & Plans](#domain-18--subscriptions--plans)
21. [Complete Entity Summary](#complete-entity-summary)
22. [Global Relationships (ERD)](#global-relationships-erd)
23. [Data Type Conventions](#data-type-conventions)
24. [Design Principles & Notes](#design-principles--notes)

---

## System Overview

**KY Food Delivery System** is the dedicated digital ordering and delivery platform for **KY Foods** — a single restaurant. There is no marketplace of multiple restaurants. Customers visit the platform specifically to order from KY Foods, and the system manages the entire lifecycle of that experience — from browsing the KY Foods menu and placing an order, through payment and kitchen preparation, to last-mile delivery and post-delivery review.

Because this is a single-restaurant system:
- There is no restaurant registration, approval, or multi-tenant restaurant management.
- All menu items, categories, and settings belong to KY Foods by default.
- `restaurant_id` foreign keys are **removed** throughout — they are replaced by system-level ownership where applicable.
- The **Store Configuration domain** replaces the Restaurant Management domain, holding KY Foods' own settings, hours, and branch locations.

### Key Actors

| Actor | Description |
|---|---|
| **Customer** | Browses the KY Foods menu, places orders, makes payments, and tracks delivery |
| **KY Foods Manager** | Manages the menu, monitors orders, and oversees operations |
| **Kitchen Staff** | Receives and prepares kitchen orders from the KY Foods kitchen |
| **Delivery Rider** | KY Foods' own riders who accept and fulfil delivery assignments |
| **System Administrator** | Manages platform settings, user accounts, and reports |
| **Customer Support Agent** | Handles tickets, complaints, and dispute resolution on behalf of KY Foods |

---

## Domain Architecture Map

The system is divided into **18 business domains**, each encapsulating a coherent set of responsibilities, entities, and logic.

```
┌─────────────────────────────────────────────────────────────────┐
│              KY FOOD DELIVERY SYSTEM  (KY Foods)                │
├───────────────────────┬─────────────────────────────────────────┤
│  CORE TRANSACTION     │  SUPPORT & MANAGEMENT                   │
│  ─────────────────    │  ────────────────────                   │
│  01. User Mgmt        │  09. Reviews & Ratings                  │
│  02. Store Config     │  10. Promotions & Coupons               │
│  03. Menu Mgmt        │  11. Inventory & Kitchen                │
│  04. Shopping Cart    │  12. Administration                     │
│  05. Order Mgmt       │  13. Reporting & Analytics              │
│  06. Payment          │  14. Customer Support                   │
│  07. Delivery         │  15. Loyalty & Rewards                  │
│  08. Notifications    │  16. Delivery Zones & Geolocation       │
│                       │  17. Content Management                 │
│                       │  18. Subscriptions & Plans              │
└───────────────────────┴─────────────────────────────────────────┘
```

---

## Domain 01 — User Management

**Purpose:** Manages all system users, their roles, profiles, addresses, authentication, and session state.

---

### Entity: `Roles`

> Defines access levels and permissions for all system actors within KY Foods.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `role_id` | INTEGER | PK, AUTO_INCREMENT | Unique role identifier |
| `role_name` | TEXT | NOT NULL, UNIQUE | Customer / Kitchen Staff / Rider / Manager / Admin / Support |
| `description` | TEXT | | Human-readable role description |
| `permissions` | JSON | | Array of permission keys granted to this role |
| `is_active` | BOOLEAN | DEFAULT TRUE | Whether this role is currently in use |
| `created_at` | DATETIME | DEFAULT NOW() | Record creation timestamp |

---

### Entity: `Users`

> The central identity record for every person who interacts with the KY Food Delivery system.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `user_id` | INTEGER | PK, AUTO_INCREMENT | Unique user identifier |
| `role_id` | INTEGER | FK → Roles, NOT NULL | User's assigned role |
| `first_name` | TEXT | NOT NULL | Legal first name |
| `last_name` | TEXT | NOT NULL | Legal last name |
| `email` | TEXT | UNIQUE, NOT NULL | Login email address |
| `phone` | TEXT | UNIQUE, NOT NULL | Mobile phone number |
| `password_hash` | TEXT | NOT NULL | Bcrypt-hashed password |
| `is_email_verified` | BOOLEAN | DEFAULT FALSE | Has the user verified their email |
| `is_phone_verified` | BOOLEAN | DEFAULT FALSE | Has the user verified their phone |
| `is_active` | BOOLEAN | DEFAULT TRUE | Account active / deactivated status |
| `is_banned` | BOOLEAN | DEFAULT FALSE | Whether the account is banned |
| `ban_reason` | TEXT | NULLABLE | Reason for ban (if banned) |
| `profile_picture_url` | TEXT | NULLABLE | URL to avatar / profile image |
| `preferred_language` | TEXT | DEFAULT 'en' | UI language preference |
| `referral_code` | TEXT | UNIQUE, NULLABLE | Customer's own referral code |
| `referred_by` | INTEGER | FK → Users, NULLABLE | user_id of the referring customer |
| `created_at` | DATETIME | DEFAULT NOW() | Account creation timestamp |
| `updated_at` | DATETIME | | Last profile update |
| `last_login` | DATETIME | NULLABLE | Most recent login timestamp |

---

### Entity: `User_Profiles`

> Extended personal details and dietary preferences for a customer.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `profile_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, UNIQUE | One-to-one with Users |
| `date_of_birth` | DATE | NULLABLE | |
| `gender` | TEXT | NULLABLE | Male / Female / Other / Prefer not to say |
| `bio` | TEXT | NULLABLE | Short personal description |
| `dietary_preferences` | JSON | NULLABLE | e.g., ["Vegetarian", "Halal"] |
| `favourite_food_categories` | JSON | NULLABLE | e.g., ["Burgers", "Grills"] — KY Foods categories |
| `updated_at` | DATETIME | | |

---

### Entity: `User_Addresses`

> Saved delivery addresses for a customer, used when placing orders.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `address_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, NOT NULL | Address owner |
| `address_label` | TEXT | | Home / Work / Other |
| `recipient_name` | TEXT | | Name of person receiving at this address |
| `recipient_phone` | TEXT | | Contact phone at delivery location |
| `street` | TEXT | NOT NULL | Street line 1 |
| `street_2` | TEXT | NULLABLE | Apartment / suite / unit |
| `city` | TEXT | NOT NULL | |
| `state` | TEXT | | |
| `postal_code` | TEXT | | |
| `country` | TEXT | DEFAULT 'Uganda' | |
| `latitude` | REAL | NOT NULL | GPS latitude |
| `longitude` | REAL | NOT NULL | GPS longitude |
| `is_default` | BOOLEAN | DEFAULT FALSE | Whether this is the primary delivery address |
| `delivery_instructions` | TEXT | NULLABLE | e.g., "Gate code 1234, leave at door" |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

### Entity: `User_Sessions`

> Tracks active login sessions per device for security and push notification targeting.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `session_id` | TEXT | PK | UUID token |
| `user_id` | INTEGER | FK → Users, NOT NULL | |
| `device_type` | TEXT | | iOS / Android / Web |
| `device_id` | TEXT | NULLABLE | Unique device fingerprint |
| `device_name` | TEXT | NULLABLE | e.g., "John's iPhone 14" |
| `ip_address` | TEXT | | |
| `user_agent` | TEXT | | Browser / app identifier |
| `fcm_token` | TEXT | NULLABLE | Firebase push notification token |
| `started_at` | DATETIME | DEFAULT NOW() | |
| `expires_at` | DATETIME | NOT NULL | |
| `is_active` | BOOLEAN | DEFAULT TRUE | |

---

### Entity: `Password_Resets`

> Stores one-time tokens for password recovery flows.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `reset_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users | |
| `token` | TEXT | UNIQUE, NOT NULL | Hashed one-time reset token |
| `expires_at` | DATETIME | NOT NULL | |
| `is_used` | BOOLEAN | DEFAULT FALSE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `OTP_Verifications`

> One-time passwords for email and phone verification flows.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `otp_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users | |
| `channel` | TEXT | NOT NULL | Email / SMS |
| `otp_code` | TEXT | NOT NULL | 4–6 digit hashed code |
| `purpose` | TEXT | NOT NULL | Registration / Login / Reset / Payment |
| `expires_at` | DATETIME | NOT NULL | |
| `verified_at` | DATETIME | NULLABLE | Timestamp when used |
| `attempts` | INTEGER | DEFAULT 0 | Number of failed attempts |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

## Domain 02 — Store Configuration

**Purpose:** Holds KY Foods' own operational settings, opening hours, and branch locations. This replaces the multi-restaurant management domain — there is only one "restaurant" in this system: KY Foods.

---

### Entity: `Store_Settings`

> The single configuration record for KY Foods. There will only ever be one row in this table.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `setting_id` | INTEGER | PK, DEFAULT 1 | Always ID = 1 (singleton) |
| `store_name` | TEXT | NOT NULL, DEFAULT 'KY Foods' | Display name |
| `tagline` | TEXT | NULLABLE | e.g., "Bold Flavour. Fast Delivery." |
| `address` | TEXT | NOT NULL | KY Foods' primary physical address |
| `city` | TEXT | NOT NULL | |
| `state` | TEXT | | |
| `country` | TEXT | DEFAULT 'Uganda' | |
| `latitude` | REAL | NOT NULL | Location for map display |
| `longitude` | REAL | NOT NULL | |
| `phone` | TEXT | NOT NULL | Customer contact number |
| `email` | TEXT | NOT NULL | Customer contact email |
| `logo_url` | TEXT | NULLABLE | |
| `cover_image_url` | TEXT | NULLABLE | |
| `min_order_amount` | DECIMAL(10,2) | DEFAULT 0.00 | Minimum cart value to check out |
| `base_delivery_fee` | DECIMAL(10,2) | DEFAULT 0.00 | Default delivery charge |
| `free_delivery_threshold` | DECIMAL(10,2) | NULLABLE | Cart total qualifying for free delivery |
| `tax_rate` | DECIMAL(5,2) | DEFAULT 0.00 | VAT / tax percentage |
| `service_charge` | DECIMAL(5,2) | DEFAULT 0.00 | Platform service fee % |
| `packaging_fee` | DECIMAL(10,2) | DEFAULT 0.00 | |
| `avg_preparation_time` | INTEGER | DEFAULT 20 | In minutes |
| `max_delivery_radius_km` | REAL | NULLABLE | Geographic delivery limit |
| `is_accepting_orders` | BOOLEAN | DEFAULT TRUE | Manual open / closed toggle |
| `accepts_scheduled_orders` | BOOLEAN | DEFAULT FALSE | Pre-order / scheduled delivery |
| `cancellation_policy` | TEXT | NULLABLE | |
| `currency` | TEXT | DEFAULT 'UGX' | |
| `updated_at` | DATETIME | | |

---

### Entity: `Operating_Hours`

> KY Foods' opening and closing times for each day of the week.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `hours_id` | INTEGER | PK, AUTO_INCREMENT | |
| `day_of_week` | INTEGER | NOT NULL | 0 = Sunday … 6 = Saturday |
| `opening_time` | TIME | NOT NULL | |
| `closing_time` | TIME | NOT NULL | |
| `break_start` | TIME | NULLABLE | Midday break start (if any) |
| `break_end` | TIME | NULLABLE | Midday break end |
| `is_closed` | BOOLEAN | DEFAULT FALSE | Mark as holiday / day off |

---

### Entity: `Store_Branches`

> Physical branch locations of KY Foods (e.g., KY Foods — Kampala Central, KY Foods — Ntinda).

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `branch_id` | INTEGER | PK, AUTO_INCREMENT | |
| `branch_name` | TEXT | NOT NULL | e.g., "KY Foods — Kampala Central" |
| `manager_id` | INTEGER | FK → Users, NULLABLE | Branch manager user account |
| `street` | TEXT | NOT NULL | |
| `city` | TEXT | NOT NULL | |
| `latitude` | REAL | NOT NULL | |
| `longitude` | REAL | NOT NULL | |
| `phone` | TEXT | NULLABLE | Branch-specific contact |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Branch_Operating_Hours`

> Per-branch opening hours (branches may have different schedules from the main store).

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `hours_id` | INTEGER | PK, AUTO_INCREMENT | |
| `branch_id` | INTEGER | FK → Store_Branches, NOT NULL | |
| `day_of_week` | INTEGER | NOT NULL | 0 = Sunday … 6 = Saturday |
| `opening_time` | TIME | NOT NULL | |
| `closing_time` | TIME | NOT NULL | |
| `is_closed` | BOOLEAN | DEFAULT FALSE | |

---

## Domain 03 — Menu Management

**Purpose:** Manages all KY Foods menu categories, food items, images, variants, and add-ons. All items belong to KY Foods — no `restaurant_id` foreign key is needed.

---

### Entity: `Categories`

> Menu sections that group KY Foods' food items (e.g., Grills, Burgers, Drinks, Desserts).

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `category_id` | INTEGER | PK, AUTO_INCREMENT | |
| `parent_category_id` | INTEGER | FK → Categories, NULLABLE | For nested sub-categories |
| `name` | TEXT | NOT NULL | e.g., Burgers, Grills, Sides, Drinks |
| `description` | TEXT | NULLABLE | |
| `image_url` | TEXT | NULLABLE | |
| `display_order` | INTEGER | DEFAULT 0 | Sort order on the menu page |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Foods`

> Individual food items on the KY Foods menu.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `food_id` | INTEGER | PK, AUTO_INCREMENT | |
| `category_id` | INTEGER | FK → Categories, NOT NULL | |
| `name` | TEXT | NOT NULL | |
| `description` | TEXT | | |
| `base_price` | DECIMAL(10,2) | NOT NULL | |
| `discount_price` | DECIMAL(10,2) | NULLABLE | Sale / promotional price |
| `sku` | TEXT | NULLABLE | Internal stock code |
| `ingredients` | TEXT | NULLABLE | Plain text or JSON list |
| `allergens` | TEXT | NULLABLE | Nuts, Gluten, Dairy, etc. |
| `calories` | INTEGER | NULLABLE | |
| `carbohydrates_g` | REAL | NULLABLE | |
| `protein_g` | REAL | NULLABLE | |
| `fat_g` | REAL | NULLABLE | |
| `preparation_time` | INTEGER | DEFAULT 15 | Minutes |
| `is_available` | BOOLEAN | DEFAULT TRUE | |
| `is_vegetarian` | BOOLEAN | DEFAULT FALSE | |
| `is_vegan` | BOOLEAN | DEFAULT FALSE | |
| `is_gluten_free` | BOOLEAN | DEFAULT FALSE | |
| `is_halal` | BOOLEAN | DEFAULT FALSE | |
| `is_spicy` | BOOLEAN | DEFAULT FALSE | |
| `spice_level` | INTEGER | NULLABLE | 1 (mild) to 5 (very hot) |
| `is_featured` | BOOLEAN | DEFAULT FALSE | Appears in "Featured" section |
| `rating_avg` | REAL | DEFAULT 0.0 | Computed from food reviews |
| `total_reviews` | INTEGER | DEFAULT 0 | Denormalised count |
| `display_order` | INTEGER | DEFAULT 0 | |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

### Entity: `Food_Images`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `image_id` | INTEGER | PK, AUTO_INCREMENT | |
| `food_id` | INTEGER | FK → Foods, NOT NULL | |
| `image_url` | TEXT | NOT NULL | |
| `alt_text` | TEXT | NULLABLE | Accessibility description |
| `is_primary` | BOOLEAN | DEFAULT FALSE | |
| `display_order` | INTEGER | DEFAULT 0 | |
| `uploaded_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Food_Variants`

> Size or style options for a food item (e.g., Small / Medium / Large).

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `variant_id` | INTEGER | PK, AUTO_INCREMENT | |
| `food_id` | INTEGER | FK → Foods, NOT NULL | |
| `variant_name` | TEXT | NOT NULL | Small / Medium / Large / Boneless / etc. |
| `variant_price` | DECIMAL(10,2) | NOT NULL | Price for this variant |
| `variant_sku` | TEXT | NULLABLE | |
| `calories` | INTEGER | NULLABLE | |
| `stock_quantity` | INTEGER | NULLABLE | NULL = unlimited |
| `is_available` | BOOLEAN | DEFAULT TRUE | |
| `display_order` | INTEGER | DEFAULT 0 | |

---

### Entity: `Food_Addons`

> Optional extras a customer can add to a food item (e.g., Extra Sauce, Coleslaw).

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `addon_id` | INTEGER | PK, AUTO_INCREMENT | |
| `food_id` | INTEGER | FK → Foods, NOT NULL | |
| `addon_group` | TEXT | NULLABLE | e.g., "Sauces", "Sides", "Toppings" |
| `name` | TEXT | NOT NULL | e.g., Extra Sauce / Coleslaw / Jalapeños |
| `price` | DECIMAL(10,2) | NOT NULL | Additional cost |
| `max_quantity` | INTEGER | DEFAULT 1 | Max units per order item |
| `is_available` | BOOLEAN | DEFAULT TRUE | |
| `is_required` | BOOLEAN | DEFAULT FALSE | Must be selected to proceed |

---

### Entity: `Menus`

> Named menu sets for KY Foods (e.g., Breakfast Menu, Lunch Specials, Ramadan Special).

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `menu_id` | INTEGER | PK, AUTO_INCREMENT | |
| `name` | TEXT | NOT NULL | |
| `description` | TEXT | NULLABLE | |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `start_date` | DATE | NULLABLE | For limited-time menus |
| `end_date` | DATE | NULLABLE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Menu_Foods`

> Junction table linking food items to named menus.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `menu_food_id` | INTEGER | PK, AUTO_INCREMENT | |
| `menu_id` | INTEGER | FK → Menus, NOT NULL | |
| `food_id` | INTEGER | FK → Foods, NOT NULL | |
| `display_order` | INTEGER | DEFAULT 0 | |

---

## Domain 04 — Shopping Cart

**Purpose:** Manages each customer's active, pre-checkout cart — temporary until converted into a confirmed order.

---

### Entity: `Carts`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `cart_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, NOT NULL | Cart owner |
| `coupon_id` | INTEGER | FK → Coupons, NULLABLE | Applied coupon code |
| `notes` | TEXT | NULLABLE | Overall order note from customer |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |
| `expires_at` | DATETIME | | Auto-clear after inactivity (e.g., 30 min) |

---

### Entity: `Cart_Items`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `cart_item_id` | INTEGER | PK, AUTO_INCREMENT | |
| `cart_id` | INTEGER | FK → Carts, NOT NULL | |
| `food_id` | INTEGER | FK → Foods, NOT NULL | |
| `variant_id` | INTEGER | FK → Food_Variants, NULLABLE | Selected size / style |
| `quantity` | INTEGER | NOT NULL, DEFAULT 1 | |
| `unit_price` | DECIMAL(10,2) | NOT NULL | Price snapshot at time of adding |
| `addons` | JSON | NULLABLE | Array of {addon_id, name, price, quantity} |
| `addons_total` | DECIMAL(10,2) | DEFAULT 0.00 | Computed add-on cost |
| `special_instructions` | TEXT | NULLABLE | Per-item customer note |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

## Domain 05 — Order Management

**Purpose:** The core transactional domain — manages every KY Foods order from placement through to completion or cancellation.

---

### Entity: `Orders`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `order_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, NOT NULL | Placing customer |
| `branch_id` | INTEGER | FK → Store_Branches, NULLABLE | Which KY Foods branch is preparing this order |
| `delivery_address_id` | INTEGER | FK → User_Addresses, NULLABLE | NULL if order type is Pickup |
| `coupon_id` | INTEGER | FK → Coupons, NULLABLE | Applied coupon |
| `order_reference` | TEXT | UNIQUE, NOT NULL | Human-readable code (e.g., KY-20250612-0043) |
| `order_type` | TEXT | DEFAULT 'Delivery' | Delivery / Pickup |
| `scheduled_for` | DATETIME | NULLABLE | Pre-order delivery time |
| `subtotal` | DECIMAL(10,2) | NOT NULL | Items total before fees |
| `tax_amount` | DECIMAL(10,2) | DEFAULT 0.00 | |
| `delivery_fee` | DECIMAL(10,2) | DEFAULT 0.00 | |
| `service_charge` | DECIMAL(10,2) | DEFAULT 0.00 | |
| `packaging_fee` | DECIMAL(10,2) | DEFAULT 0.00 | |
| `discount_amount` | DECIMAL(10,2) | DEFAULT 0.00 | |
| `tip_amount` | DECIMAL(10,2) | DEFAULT 0.00 | Customer tip to rider |
| `grand_total` | DECIMAL(10,2) | NOT NULL | Final amount charged |
| `payment_status` | TEXT | DEFAULT 'Pending' | Pending / Paid / Failed / Refunded |
| `order_status` | TEXT | DEFAULT 'Received' | Received / Confirmed / Preparing / Ready / Picked Up / On Delivery / Delivered / Cancelled |
| `special_instructions` | TEXT | NULLABLE | Overall order note from customer |
| `is_rated` | BOOLEAN | DEFAULT FALSE | Has customer submitted a review |
| `is_cancelled` | BOOLEAN | DEFAULT FALSE | |
| `cancellation_reason` | TEXT | NULLABLE | |
| `cancelled_by` | INTEGER | FK → Users, NULLABLE | Who cancelled (customer or staff) |
| `cancelled_at` | DATETIME | NULLABLE | |
| `estimated_delivery_time` | DATETIME | NULLABLE | System-generated ETA |
| `actual_delivery_time` | DATETIME | NULLABLE | |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

### Entity: `Order_Items`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `order_item_id` | INTEGER | PK, AUTO_INCREMENT | |
| `order_id` | INTEGER | FK → Orders, NOT NULL | |
| `food_id` | INTEGER | FK → Foods, NOT NULL | |
| `food_name` | TEXT | NOT NULL | Snapshot — name at time of order |
| `variant_id` | INTEGER | FK → Food_Variants, NULLABLE | |
| `variant_name` | TEXT | NULLABLE | Snapshot |
| `quantity` | INTEGER | NOT NULL | |
| `unit_price` | DECIMAL(10,2) | NOT NULL | Snapshot of price at order time |
| `addons` | JSON | NULLABLE | Snapshot of selected add-ons |
| `addons_total` | DECIMAL(10,2) | DEFAULT 0.00 | |
| `line_total` | DECIMAL(10,2) | NOT NULL | (unit_price + addons_total) × quantity |
| `special_instructions` | TEXT | NULLABLE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Order_Status_History`

> Immutable audit trail of every status transition for an order.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `status_id` | INTEGER | PK, AUTO_INCREMENT | |
| `order_id` | INTEGER | FK → Orders, NOT NULL | |
| `status` | TEXT | NOT NULL | Status value at this point in time |
| `notes` | TEXT | NULLABLE | Optional internal note |
| `updated_by` | INTEGER | FK → Users, NULLABLE | Staff member who triggered the change |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

## Domain 06 — Payment

**Purpose:** Tracks all customer payment methods, transactions, refunds, wallet balances, and gateway integrations for KY Foods orders.

---

### Entity: `Payment_Methods`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `method_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, NOT NULL | |
| `method_type` | TEXT | NOT NULL | Mobile Money / Credit Card / Debit Card / Cash / Wallet |
| `provider` | TEXT | NULLABLE | MTN, Airtel, Visa, Mastercard |
| `account_number` | TEXT | NULLABLE | Encrypted / masked |
| `account_name` | TEXT | NULLABLE | |
| `expiry_date` | DATE | NULLABLE | For cards |
| `is_default` | BOOLEAN | DEFAULT FALSE | |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Payments`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `payment_id` | INTEGER | PK, AUTO_INCREMENT | |
| `order_id` | INTEGER | FK → Orders, NOT NULL | |
| `user_id` | INTEGER | FK → Users, NOT NULL | |
| `payment_method_id` | INTEGER | FK → Payment_Methods, NULLABLE | NULL = Cash on Delivery |
| `amount` | DECIMAL(10,2) | NOT NULL | |
| `currency` | TEXT | DEFAULT 'UGX' | |
| `transaction_reference` | TEXT | UNIQUE, NULLABLE | ID from payment gateway |
| `gateway_name` | TEXT | NULLABLE | MTN API / Airtel Money / Flutterwave / Stripe |
| `status` | TEXT | DEFAULT 'Pending' | Pending / Completed / Failed / Refunded / Partially Refunded |
| `gateway_response` | JSON | NULLABLE | Raw response from payment provider |
| `failure_reason` | TEXT | NULLABLE | |
| `paid_at` | DATETIME | NULLABLE | |
| `refunded_at` | DATETIME | NULLABLE | |
| `refund_amount` | DECIMAL(10,2) | DEFAULT 0.00 | |
| `refund_reason` | TEXT | NULLABLE | |
| `refunded_by` | INTEGER | FK → Users, NULLABLE | Admin who processed the refund |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Wallets`

> In-app digital wallet balance per customer, usable for KY Foods orders.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `wallet_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, UNIQUE | One wallet per customer |
| `balance` | DECIMAL(12,2) | DEFAULT 0.00 | Current available balance |
| `currency` | TEXT | DEFAULT 'UGX' | |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

### Entity: `Wallet_Transactions`

> Full ledger of all wallet credits and debits.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `transaction_id` | INTEGER | PK, AUTO_INCREMENT | |
| `wallet_id` | INTEGER | FK → Wallets, NOT NULL | |
| `type` | TEXT | NOT NULL | Credit / Debit |
| `amount` | DECIMAL(10,2) | NOT NULL | |
| `balance_after` | DECIMAL(10,2) | NOT NULL | Running balance after transaction |
| `reference` | TEXT | NULLABLE | Linked order reference or top-up reference |
| `description` | TEXT | | e.g., "Order KY-2025-0043 payment" |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

## Domain 07 — Delivery

**Purpose:** Manages KY Foods' own delivery riders, delivery assignments, real-time location tracking, and rider earnings.

---

### Entity: `Delivery_Riders`

> KY Foods' employed or contracted delivery riders.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `rider_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, UNIQUE | Links to the rider's user account |
| `vehicle_type` | TEXT | NOT NULL | Bicycle / Motorbike / Car / Scooter |
| `vehicle_make` | TEXT | NULLABLE | e.g., Yamaha |
| `vehicle_model` | TEXT | NULLABLE | e.g., YBR 125 |
| `vehicle_colour` | TEXT | NULLABLE | |
| `vehicle_plate` | TEXT | UNIQUE | |
| `license_number` | TEXT | NULLABLE | |
| `insurance_number` | TEXT | NULLABLE | |
| `insurance_expiry` | DATE | NULLABLE | |
| `id_document_url` | TEXT | NULLABLE | National ID / Passport scan |
| `is_verified` | BOOLEAN | DEFAULT FALSE | Admin verification of documents |
| `is_available` | BOOLEAN | DEFAULT FALSE | Rider online / offline toggle |
| `current_latitude` | REAL | NULLABLE | Live location |
| `current_longitude` | REAL | NULLABLE | |
| `last_location_update` | DATETIME | NULLABLE | |
| `rating_avg` | REAL | DEFAULT 0.0 | Computed from customer ratings |
| `total_deliveries` | INTEGER | DEFAULT 0 | |
| `total_earnings` | DECIMAL(12,2) | DEFAULT 0.00 | Lifetime earnings |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

### Entity: `Deliveries`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `delivery_id` | INTEGER | PK, AUTO_INCREMENT | |
| `order_id` | INTEGER | FK → Orders, UNIQUE | One delivery per order |
| `rider_id` | INTEGER | FK → Delivery_Riders, NULLABLE | NULL = not yet assigned |
| `branch_id` | INTEGER | FK → Store_Branches, NULLABLE | KY Foods branch this delivery originates from |
| `assignment_method` | TEXT | NULLABLE | Auto / Manual |
| `assigned_at` | DATETIME | NULLABLE | |
| `pickup_address` | TEXT | NOT NULL | KY Foods branch address snapshot |
| `pickup_latitude` | REAL | NOT NULL | |
| `pickup_longitude` | REAL | NOT NULL | |
| `delivery_address` | TEXT | NOT NULL | Customer address snapshot |
| `delivery_latitude` | REAL | NOT NULL | |
| `delivery_longitude` | REAL | NOT NULL | |
| `status` | TEXT | DEFAULT 'Pending' | Pending / Assigned / Heading to KY Foods / Picked Up / In Transit / Arrived / Delivered / Failed |
| `distance_km` | REAL | NULLABLE | Route distance |
| `estimated_pickup_time` | DATETIME | NULLABLE | |
| `actual_pickup_time` | DATETIME | NULLABLE | |
| `estimated_delivery_time` | DATETIME | NULLABLE | |
| `actual_delivery_time` | DATETIME | NULLABLE | |
| `delivery_fee` | DECIMAL(10,2) | NOT NULL | |
| `rider_earnings` | DECIMAL(10,2) | NULLABLE | Rider's payout for this delivery |
| `rider_notes` | TEXT | NULLABLE | |
| `delivery_photo_url` | TEXT | NULLABLE | Proof of delivery photo |
| `customer_rating` | INTEGER | NULLABLE | 1–5 stars for the rider |
| `customer_feedback` | TEXT | NULLABLE | |
| `failure_reason` | TEXT | NULLABLE | If delivery could not be completed |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

### Entity: `Delivery_Tracking`

> High-frequency real-time GPS pings for a delivery currently in progress.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `tracking_id` | INTEGER | PK, AUTO_INCREMENT | |
| `delivery_id` | INTEGER | FK → Deliveries, NOT NULL | |
| `latitude` | REAL | NOT NULL | |
| `longitude` | REAL | NOT NULL | |
| `speed_kmh` | REAL | NULLABLE | |
| `heading_degrees` | REAL | NULLABLE | Direction of travel |
| `accuracy_meters` | REAL | NULLABLE | GPS accuracy radius |
| `timestamp` | DATETIME | NOT NULL | |

---

### Entity: `Rider_Earnings`

> Per-delivery earnings ledger for each KY Foods rider.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `earning_id` | INTEGER | PK, AUTO_INCREMENT | |
| `rider_id` | INTEGER | FK → Delivery_Riders, NOT NULL | |
| `delivery_id` | INTEGER | FK → Deliveries, NOT NULL | |
| `base_fee` | DECIMAL(10,2) | NOT NULL | Fixed per-delivery payout |
| `distance_bonus` | DECIMAL(10,2) | DEFAULT 0.00 | Extra pay for longer distances |
| `tip` | DECIMAL(10,2) | DEFAULT 0.00 | Customer tip passed through |
| `deductions` | DECIMAL(10,2) | DEFAULT 0.00 | Any deductions applied |
| `net_earning` | DECIMAL(10,2) | NOT NULL | |
| `status` | TEXT | DEFAULT 'Pending' | Pending / Paid |
| `paid_at` | DATETIME | NULLABLE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

## Domain 08 — Notifications

**Purpose:** Manages all push notifications, in-app alerts, email, and SMS communications sent to KY Foods customers, riders, and staff.

---

### Entity: `Notification_Types`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `type_id` | INTEGER | PK, AUTO_INCREMENT | |
| `type_name` | TEXT | UNIQUE, NOT NULL | Order Confirmed / Rider Assigned / Out for Delivery / Delivered / Promo / System |
| `template_title` | TEXT | NOT NULL | Title template with `{{placeholders}}` |
| `template_body` | TEXT | NOT NULL | Body template |
| `icon` | TEXT | NULLABLE | Icon class or emoji |
| `category` | TEXT | | Order / Delivery / Promo / System / Support |
| `is_active` | BOOLEAN | DEFAULT TRUE | |

---

### Entity: `Notifications`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `notification_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, NOT NULL | Recipient |
| `type_id` | INTEGER | FK → Notification_Types, NOT NULL | |
| `order_id` | INTEGER | FK → Orders, NULLABLE | |
| `delivery_id` | INTEGER | FK → Deliveries, NULLABLE | |
| `title` | TEXT | NOT NULL | Rendered title |
| `message` | TEXT | NOT NULL | Rendered body |
| `data` | JSON | NULLABLE | Deep-link data payload |
| `channel` | TEXT | NOT NULL | App / Email / SMS / All |
| `is_read` | BOOLEAN | DEFAULT FALSE | |
| `read_at` | DATETIME | NULLABLE | |
| `sent_at` | DATETIME | NULLABLE | |
| `failed_reason` | TEXT | NULLABLE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Notification_Preferences`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `preference_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, NOT NULL | |
| `type_id` | INTEGER | FK → Notification_Types, NOT NULL | |
| `app_enabled` | BOOLEAN | DEFAULT TRUE | |
| `email_enabled` | BOOLEAN | DEFAULT TRUE | |
| `sms_enabled` | BOOLEAN | DEFAULT FALSE | |
| `updated_at` | DATETIME | | |

---

## Domain 09 — Reviews & Ratings

**Purpose:** Collects verified customer feedback on KY Foods' food items and delivery riders, following a confirmed order.

---

### Entity: `Reviews`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `review_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, NOT NULL | Reviewer |
| `order_id` | INTEGER | FK → Orders, UNIQUE | One review per order |
| `food_rating` | INTEGER | NOT NULL | 1–5 overall food quality rating |
| `food_comment` | TEXT | NULLABLE | General food comment |
| `delivery_id` | INTEGER | FK → Deliveries, NULLABLE | |
| `rider_rating` | INTEGER | NULLABLE | 1–5 rider rating |
| `rider_comment` | TEXT | NULLABLE | |
| `images` | JSON | NULLABLE | Array of customer-uploaded photo URLs |
| `is_verified_purchase` | BOOLEAN | DEFAULT TRUE | Always true — review gated by order completion |
| `is_visible` | BOOLEAN | DEFAULT TRUE | Can be hidden by admin |
| `helpful_count` | INTEGER | DEFAULT 0 | Number of "helpful" votes from other customers |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

### Entity: `Food_Reviews`

> Item-level ratings for individual foods within an order.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `food_review_id` | INTEGER | PK, AUTO_INCREMENT | |
| `review_id` | INTEGER | FK → Reviews, NOT NULL | Parent review |
| `food_id` | INTEGER | FK → Foods, NOT NULL | |
| `rating` | INTEGER | NOT NULL | 1–5 |
| `comment` | TEXT | NULLABLE | |

---

### Entity: `Review_Replies`

> KY Foods manager responses to customer reviews.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `reply_id` | INTEGER | PK, AUTO_INCREMENT | |
| `review_id` | INTEGER | FK → Reviews, UNIQUE | One reply per review |
| `manager_id` | INTEGER | FK → Users, NOT NULL | KY Foods staff member replying |
| `reply_text` | TEXT | NOT NULL | |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

## Domain 10 — Promotions & Coupons

**Purpose:** Manages KY Foods' discount campaigns, promotional offers, and customer-specific coupon codes.

---

### Entity: `Promotions`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `promotion_id` | INTEGER | PK, AUTO_INCREMENT | |
| `created_by` | INTEGER | FK → Users, NOT NULL | Admin or manager who created it |
| `name` | TEXT | NOT NULL | e.g., "Weekend Special", "First Order Discount" |
| `description` | TEXT | NULLABLE | |
| `discount_type` | TEXT | NOT NULL | Percentage / Fixed Amount / Free Delivery / Buy X Get Y |
| `discount_value` | DECIMAL(10,2) | NOT NULL | % or flat amount |
| `min_order_amount` | DECIMAL(10,2) | DEFAULT 0.00 | Minimum cart value to qualify |
| `max_discount_cap` | DECIMAL(10,2) | NULLABLE | Maximum discount amount allowed |
| `applicable_items` | JSON | NULLABLE | Array of food_ids; NULL = entire menu |
| `applicable_categories` | JSON | NULLABLE | Array of category_ids |
| `start_date` | DATETIME | NOT NULL | |
| `end_date` | DATETIME | NOT NULL | |
| `usage_limit` | INTEGER | NULLABLE | Total redemptions allowed platform-wide |
| `used_count` | INTEGER | DEFAULT 0 | |
| `per_user_limit` | INTEGER | DEFAULT 1 | Max uses per individual customer |
| `is_first_order_only` | BOOLEAN | DEFAULT FALSE | Restricts to new customers |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

### Entity: `Coupons`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `coupon_id` | INTEGER | PK, AUTO_INCREMENT | |
| `promotion_id` | INTEGER | FK → Promotions, NOT NULL | Parent promotion |
| `user_id` | INTEGER | FK → Users, NULLABLE | NULL = any customer can use |
| `code` | TEXT | UNIQUE, NOT NULL | e.g., KYFOOD20 |
| `is_used` | BOOLEAN | DEFAULT FALSE | |
| `used_at` | DATETIME | NULLABLE | |
| `order_id` | INTEGER | FK → Orders, NULLABLE | Order the coupon was applied to |
| `expires_at` | DATETIME | NOT NULL | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

## Domain 11 — Inventory & Kitchen

**Purpose:** Manages KY Foods' ingredient stock levels, food recipes, and kitchen order workflow.

---

### Entity: `Ingredients`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `ingredient_id` | INTEGER | PK, AUTO_INCREMENT | |
| `name` | TEXT | NOT NULL | |
| `unit` | TEXT | NOT NULL | kg / g / L / mL / pieces |
| `minimum_stock` | DECIMAL(10,2) | DEFAULT 0.00 | Low-stock alert threshold |
| `current_stock` | DECIMAL(10,2) | DEFAULT 0.00 | |
| `cost_per_unit` | DECIMAL(10,2) | NULLABLE | For food cost tracking |
| `supplier_name` | TEXT | NULLABLE | |
| `supplier_contact` | TEXT | NULLABLE | |
| `last_restocked` | DATETIME | NULLABLE | |
| `updated_at` | DATETIME | | |

---

### Entity: `Food_Ingredients`

> Recipe definition — which KY Foods ingredients a food item requires per serving.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `food_ingredient_id` | INTEGER | PK, AUTO_INCREMENT | |
| `food_id` | INTEGER | FK → Foods, NOT NULL | |
| `ingredient_id` | INTEGER | FK → Ingredients, NOT NULL | |
| `quantity_needed` | DECIMAL(10,2) | NOT NULL | Per serving |
| `unit` | TEXT | NOT NULL | |

---

### Entity: `Kitchen_Orders`

> The kitchen-facing view of a customer order — what the KY Foods kitchen needs to prepare.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `kitchen_order_id` | INTEGER | PK, AUTO_INCREMENT | |
| `order_id` | INTEGER | FK → Orders, NOT NULL | |
| `branch_id` | INTEGER | FK → Store_Branches, NULLABLE | Which branch is preparing |
| `status` | TEXT | DEFAULT 'Pending' | Pending / Preparing / Completed / Cancelled |
| `priority` | INTEGER | DEFAULT 1 | 1 = highest priority |
| `assigned_to` | INTEGER | FK → Users, NULLABLE | Kitchen staff member |
| `notes` | TEXT | NULLABLE | |
| `started_at` | DATETIME | NULLABLE | |
| `completed_at` | DATETIME | NULLABLE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Kitchen_Order_Items`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `kitchen_item_id` | INTEGER | PK, AUTO_INCREMENT | |
| `kitchen_order_id` | INTEGER | FK → Kitchen_Orders, NOT NULL | |
| `order_item_id` | INTEGER | FK → Order_Items, NOT NULL | |
| `food_name` | TEXT | NOT NULL | Snapshot for kitchen display |
| `variant_name` | TEXT | NULLABLE | |
| `quantity` | INTEGER | NOT NULL | |
| `addons` | JSON | NULLABLE | |
| `special_instructions` | TEXT | NULLABLE | |
| `status` | TEXT | DEFAULT 'Pending' | Pending / Preparing / Done |

---

### Entity: `Stock_Movements`

> Full audit trail of all inventory changes — restocks, usage, wastage, and adjustments.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `movement_id` | INTEGER | PK, AUTO_INCREMENT | |
| `ingredient_id` | INTEGER | FK → Ingredients, NOT NULL | |
| `movement_type` | TEXT | NOT NULL | Restock / Usage / Wastage / Adjustment |
| `quantity` | DECIMAL(10,2) | NOT NULL | Positive = in, Negative = out |
| `balance_after` | DECIMAL(10,2) | NOT NULL | Stock level after this movement |
| `reference` | TEXT | NULLABLE | e.g., Order ID or supplier invoice number |
| `notes` | TEXT | NULLABLE | |
| `performed_by` | INTEGER | FK → Users, NOT NULL | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

## Domain 12 — Administration

**Purpose:** System-wide configuration, staff user management, and comprehensive audit logging for KY Foods operations.

---

### Entity: `System_Settings`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `setting_id` | INTEGER | PK, AUTO_INCREMENT | |
| `setting_key` | TEXT | UNIQUE, NOT NULL | e.g., `platform_commission_rate`, `default_tax_rate` |
| `setting_value` | TEXT | NOT NULL | |
| `data_type` | TEXT | NOT NULL | String / Integer / Decimal / Boolean / JSON |
| `category` | TEXT | | General / Payment / Delivery / Notifications |
| `description` | TEXT | NULLABLE | |
| `is_editable` | BOOLEAN | DEFAULT TRUE | |
| `updated_by` | INTEGER | FK → Users, NULLABLE | Admin who last changed this |
| `updated_at` | DATETIME | | |

---

### Entity: `Audit_Logs`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `log_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, NULLABLE | Actor — NULL = system-automated action |
| `action` | TEXT | NOT NULL | Create / Update / Delete / Login / Logout / Approve / Reject |
| `module` | TEXT | NOT NULL | Domain / module name |
| `table_name` | TEXT | NOT NULL | Affected database table |
| `record_id` | INTEGER | NULLABLE | PK of the affected record |
| `old_value` | JSON | NULLABLE | State before change |
| `new_value` | JSON | NULLABLE | State after change |
| `description` | TEXT | NULLABLE | Human-readable summary |
| `ip_address` | TEXT | NULLABLE | |
| `user_agent` | TEXT | NULLABLE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Admin_Actions`

> Records explicit manual decisions by KY Foods admin or managers.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `action_id` | INTEGER | PK, AUTO_INCREMENT | |
| `admin_id` | INTEGER | FK → Users, NOT NULL | |
| `action_type` | TEXT | NOT NULL | Ban User / Process Refund / Hide Review / Restock Alert / etc. |
| `target_type` | TEXT | NOT NULL | User / Order / Review / Food |
| `target_id` | INTEGER | NOT NULL | ID of the target record |
| `reason` | TEXT | NULLABLE | |
| `notes` | TEXT | NULLABLE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

## Domain 13 — Reporting & Analytics

**Purpose:** Stores pre-aggregated data for KY Foods management dashboards, operational reporting, and business insights.

---

### Entity: `Daily_Sales_Reports`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `report_id` | INTEGER | PK, AUTO_INCREMENT | |
| `branch_id` | INTEGER | FK → Store_Branches, NULLABLE | NULL = whole store |
| `report_date` | DATE | NOT NULL | |
| `total_orders` | INTEGER | DEFAULT 0 | |
| `completed_orders` | INTEGER | DEFAULT 0 | |
| `cancelled_orders` | INTEGER | DEFAULT 0 | |
| `gross_revenue` | DECIMAL(12,2) | DEFAULT 0.00 | Before fees / discounts |
| `total_delivery_fees` | DECIMAL(12,2) | DEFAULT 0.00 | |
| `total_tax` | DECIMAL(12,2) | DEFAULT 0.00 | |
| `total_discounts` | DECIMAL(12,2) | DEFAULT 0.00 | |
| `net_revenue` | DECIMAL(12,2) | DEFAULT 0.00 | After all deductions |
| `most_ordered_foods` | JSON | NULLABLE | Top 5 food_ids + order counts |
| `new_customers` | INTEGER | DEFAULT 0 | First-time orderers today |
| `returning_customers` | INTEGER | DEFAULT 0 | |
| `avg_order_value` | DECIMAL(10,2) | NULLABLE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Hourly_Order_Stats`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `stat_id` | INTEGER | PK, AUTO_INCREMENT | |
| `branch_id` | INTEGER | FK → Store_Branches, NULLABLE | |
| `stat_date` | DATE | NOT NULL | |
| `hour` | INTEGER | NOT NULL | 0–23 |
| `orders_received` | INTEGER | DEFAULT 0 | |
| `orders_completed` | INTEGER | DEFAULT 0 | |
| `orders_cancelled` | INTEGER | DEFAULT 0 | |
| `avg_preparation_time` | INTEGER | NULLABLE | Minutes |
| `avg_delivery_time` | INTEGER | NULLABLE | Minutes |
| `avg_rating` | REAL | NULLABLE | |

---

### Entity: `Rider_Performance_Reports`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `report_id` | INTEGER | PK, AUTO_INCREMENT | |
| `rider_id` | INTEGER | FK → Delivery_Riders, NOT NULL | |
| `report_date` | DATE | NOT NULL | |
| `total_deliveries` | INTEGER | DEFAULT 0 | |
| `successful_deliveries` | INTEGER | DEFAULT 0 | |
| `failed_deliveries` | INTEGER | DEFAULT 0 | |
| `avg_delivery_time` | INTEGER | NULLABLE | Minutes |
| `total_distance_km` | REAL | DEFAULT 0.0 | |
| `total_earnings` | DECIMAL(10,2) | DEFAULT 0.00 | |
| `avg_rating` | REAL | NULLABLE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

## Domain 14 — Customer Support

**Purpose:** Manages all customer inquiries, complaints, and disputes relating to KY Foods orders and deliveries.

---

### Entity: `Support_Tickets`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `ticket_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, NOT NULL | Customer raising the issue |
| `order_id` | INTEGER | FK → Orders, NULLABLE | Related order (if any) |
| `subject` | TEXT | NOT NULL | |
| `description` | TEXT | NOT NULL | |
| `category` | TEXT | | Late Delivery / Wrong Item / Missing Item / Payment Issue / App Bug / Other |
| `priority` | TEXT | DEFAULT 'Medium' | Low / Medium / High / Urgent |
| `status` | TEXT | DEFAULT 'Open' | Open / In Progress / Awaiting Customer / Resolved / Closed |
| `assigned_to` | INTEGER | FK → Users, NULLABLE | Support agent |
| `resolution_notes` | TEXT | NULLABLE | |
| `resolved_at` | DATETIME | NULLABLE | |
| `satisfaction_rating` | INTEGER | NULLABLE | 1–5, post-resolution survey |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

### Entity: `Ticket_Messages`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `message_id` | INTEGER | PK, AUTO_INCREMENT | |
| `ticket_id` | INTEGER | FK → Support_Tickets, NOT NULL | |
| `sender_id` | INTEGER | FK → Users, NOT NULL | |
| `message` | TEXT | NOT NULL | |
| `attachment_url` | TEXT | NULLABLE | Screenshot or file |
| `is_internal_note` | BOOLEAN | DEFAULT FALSE | Staff-only note — hidden from customer |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `FAQs`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `faq_id` | INTEGER | PK, AUTO_INCREMENT | |
| `question` | TEXT | NOT NULL | |
| `answer` | TEXT | NOT NULL | |
| `category` | TEXT | | Orders / Payments / Delivery / Account / Menu |
| `display_order` | INTEGER | DEFAULT 0 | |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `helpful_count` | INTEGER | DEFAULT 0 | |
| `not_helpful_count` | INTEGER | DEFAULT 0 | |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

## Domain 15 — Loyalty & Rewards

**Purpose:** Manages KY Foods' customer loyalty points programme, tier progression, and reward redemption.

---

### Entity: `Loyalty_Tiers`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `tier_id` | INTEGER | PK, AUTO_INCREMENT | |
| `tier_name` | TEXT | UNIQUE, NOT NULL | Bronze / Silver / Gold / Platinum |
| `min_points` | INTEGER | NOT NULL | Lifetime points needed to reach this tier |
| `points_multiplier` | REAL | DEFAULT 1.0 | Earn rate multiplier for this tier |
| `perks` | JSON | NULLABLE | Array of perk descriptions |
| `badge_image_url` | TEXT | NULLABLE | |

---

### Entity: `Loyalty_Accounts`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `loyalty_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, UNIQUE | One loyalty account per customer |
| `total_points_earned` | INTEGER | DEFAULT 0 | Lifetime points accumulated |
| `current_points` | INTEGER | DEFAULT 0 | Available points to spend |
| `tier_id` | INTEGER | FK → Loyalty_Tiers | Current tier |
| `tier_updated_at` | DATETIME | NULLABLE | When tier last changed |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

### Entity: `Loyalty_Transactions`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `loyalty_tx_id` | INTEGER | PK, AUTO_INCREMENT | |
| `loyalty_id` | INTEGER | FK → Loyalty_Accounts, NOT NULL | |
| `order_id` | INTEGER | FK → Orders, NULLABLE | Linked KY Foods order |
| `type` | TEXT | NOT NULL | Earn / Redeem / Expire / Bonus / Adjustment |
| `points` | INTEGER | NOT NULL | Positive = earn, Negative = redeem/expire |
| `balance_after` | INTEGER | NOT NULL | Points balance after this transaction |
| `description` | TEXT | | e.g., "Earned 50 pts for order KY-0043" |
| `expires_at` | DATETIME | NULLABLE | When these points expire |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Rewards`

> Items or discounts redeemable with KY Foods loyalty points.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `reward_id` | INTEGER | PK, AUTO_INCREMENT | |
| `name` | TEXT | NOT NULL | e.g., "Free Delivery" / "10% Off Next Order" / "Free Side" |
| `description` | TEXT | NULLABLE | |
| `points_cost` | INTEGER | NOT NULL | Loyalty points required to redeem |
| `reward_type` | TEXT | NOT NULL | Discount / Free Item / Free Delivery / Voucher |
| `reward_value` | DECIMAL(10,2) | NULLABLE | Monetary value of this reward |
| `min_tier_required` | INTEGER | FK → Loyalty_Tiers, NULLABLE | Minimum tier to unlock |
| `expiry_days` | INTEGER | NULLABLE | Days before reward voucher expires after redemption |
| `usage_limit` | INTEGER | NULLABLE | Total platform-wide redemptions allowed |
| `used_count` | INTEGER | DEFAULT 0 | |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

## Domain 16 — Delivery Zones & Geolocation

**Purpose:** Manages KY Foods' delivery coverage areas, zone-based pricing, and geographic restrictions.

---

### Entity: `Delivery_Zones`

> Geographic areas that KY Foods delivers to, each with its own pricing.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `zone_id` | INTEGER | PK, AUTO_INCREMENT | |
| `name` | TEXT | NOT NULL | e.g., "Kampala Central", "Naguru", "Ntinda" |
| `description` | TEXT | NULLABLE | |
| `boundary_polygon` | TEXT | NOT NULL | GeoJSON polygon string |
| `base_delivery_fee` | DECIMAL(10,2) | NOT NULL | |
| `fee_per_km` | DECIMAL(10,2) | DEFAULT 0.00 | Additional charge per km |
| `max_delivery_time` | INTEGER | NULLABLE | Estimated delivery minutes for this zone |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

### Entity: `Branch_Delivery_Zones`

> Which delivery zones each KY Foods branch serves.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `branch_zone_id` | INTEGER | PK, AUTO_INCREMENT | |
| `branch_id` | INTEGER | FK → Store_Branches, NOT NULL | |
| `zone_id` | INTEGER | FK → Delivery_Zones, NOT NULL | |
| `custom_delivery_fee` | DECIMAL(10,2) | NULLABLE | Override zone default fee for this branch |
| `is_active` | BOOLEAN | DEFAULT TRUE | |

---

### Entity: `Geo_Restrictions`

> Areas where KY Foods does not deliver.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `restriction_id` | INTEGER | PK, AUTO_INCREMENT | |
| `name` | TEXT | NOT NULL | e.g., "Outside City Limits", "Industrial Area" |
| `boundary_polygon` | TEXT | NOT NULL | GeoJSON polygon |
| `reason` | TEXT | NULLABLE | |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

## Domain 17 — Content Management

**Purpose:** Manages all customer-facing platform content — promotional banners, static pages, and homepage featured sections for KY Foods.

---

### Entity: `Banners`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `banner_id` | INTEGER | PK, AUTO_INCREMENT | |
| `title` | TEXT | NOT NULL | |
| `subtitle` | TEXT | NULLABLE | |
| `image_url` | TEXT | NOT NULL | |
| `link_url` | TEXT | NULLABLE | Deep-link or external URL |
| `link_type` | TEXT | NULLABLE | Food / Category / Promotion / Page |
| `link_id` | INTEGER | NULLABLE | ID of the linked entity |
| `placement` | TEXT | NOT NULL | Home / Menu / Checkout |
| `display_order` | INTEGER | DEFAULT 0 | |
| `start_date` | DATETIME | NULLABLE | |
| `end_date` | DATETIME | NULLABLE | |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_by` | INTEGER | FK → Users, NOT NULL | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `Pages`

> Static CMS pages managed by KY Foods admin (About Us, Terms, Privacy Policy, etc.).

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `page_id` | INTEGER | PK, AUTO_INCREMENT | |
| `title` | TEXT | NOT NULL | |
| `slug` | TEXT | UNIQUE, NOT NULL | URL path e.g., `about-us`, `privacy-policy` |
| `content` | TEXT | NOT NULL | HTML or Markdown body |
| `meta_description` | TEXT | NULLABLE | SEO description |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `last_updated_by` | INTEGER | FK → Users | |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

### Entity: `Featured_Foods`

> Admin-curated list of food items featured prominently on the KY Foods homepage.

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `feature_id` | INTEGER | PK, AUTO_INCREMENT | |
| `food_id` | INTEGER | FK → Foods, NOT NULL | |
| `feature_label` | TEXT | NULLABLE | e.g., "Chef's Pick", "Best Seller", "New" |
| `display_order` | INTEGER | DEFAULT 0 | |
| `start_date` | DATETIME | NULLABLE | |
| `end_date` | DATETIME | NULLABLE | |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_by` | INTEGER | FK → Users, NOT NULL | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

## Domain 18 — Subscriptions & Plans

**Purpose:** Manages premium subscription plans for KY Foods customers (e.g., KY Pro — unlimited free deliveries, priority orders).

---

### Entity: `Subscription_Plans`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `plan_id` | INTEGER | PK, AUTO_INCREMENT | |
| `name` | TEXT | NOT NULL | e.g., KY Free / KY Pro / KY Family |
| `description` | TEXT | NULLABLE | |
| `billing_cycle` | TEXT | NOT NULL | Monthly / Quarterly / Annual |
| `price` | DECIMAL(10,2) | NOT NULL | |
| `currency` | TEXT | DEFAULT 'UGX' | |
| `features` | JSON | NOT NULL | Array of feature descriptions |
| `free_deliveries_per_month` | INTEGER | NULLABLE | NULL = unlimited |
| `priority_ordering` | BOOLEAN | DEFAULT FALSE | Jumps queue in kitchen |
| `discount_on_orders` | DECIMAL(5,2) | DEFAULT 0.00 | % off all orders for subscribers |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | DEFAULT NOW() | |

---

### Entity: `User_Subscriptions`

| Attribute | Type | Constraints | Description |
|---|---|---|---|
| `subscription_id` | INTEGER | PK, AUTO_INCREMENT | |
| `user_id` | INTEGER | FK → Users, NOT NULL | |
| `plan_id` | INTEGER | FK → Subscription_Plans, NOT NULL | |
| `status` | TEXT | DEFAULT 'Active' | Active / Expired / Cancelled / Paused |
| `start_date` | DATE | NOT NULL | |
| `end_date` | DATE | NOT NULL | |
| `auto_renew` | BOOLEAN | DEFAULT TRUE | |
| `payment_id` | INTEGER | FK → Payments, NULLABLE | Payment for this subscription period |
| `free_deliveries_used` | INTEGER | DEFAULT 0 | Tracked per billing cycle |
| `cancelled_at` | DATETIME | NULLABLE | |
| `cancellation_reason` | TEXT | NULLABLE | |
| `created_at` | DATETIME | DEFAULT NOW() | |
| `updated_at` | DATETIME | | |

---

## Complete Entity Summary

| **#** | **Domain** | **Entities (Tables)** | **Count** |
|---|---|---|---|
| 01 | User Management | Users, Roles, User_Profiles, User_Addresses, User_Sessions, Password_Resets, OTP_Verifications | 7 |
| 02 | Store Configuration | Store_Settings, Operating_Hours, Store_Branches, Branch_Operating_Hours | 4 |
| 03 | Menu Management | Categories, Foods, Food_Images, Food_Variants, Food_Addons, Menus, Menu_Foods | 7 |
| 04 | Shopping Cart | Carts, Cart_Items | 2 |
| 05 | Order Management | Orders, Order_Items, Order_Status_History | 3 |
| 06 | Payment | Payment_Methods, Payments, Wallets, Wallet_Transactions | 4 |
| 07 | Delivery | Delivery_Riders, Deliveries, Delivery_Tracking, Rider_Earnings | 4 |
| 08 | Notifications | Notification_Types, Notifications, Notification_Preferences | 3 |
| 09 | Reviews & Ratings | Reviews, Food_Reviews, Review_Replies | 3 |
| 10 | Promotions & Coupons | Promotions, Coupons | 2 |
| 11 | Inventory & Kitchen | Ingredients, Food_Ingredients, Kitchen_Orders, Kitchen_Order_Items, Stock_Movements | 5 |
| 12 | Administration | System_Settings, Audit_Logs, Admin_Actions | 3 |
| 13 | Reporting & Analytics | Daily_Sales_Reports, Hourly_Order_Stats, Rider_Performance_Reports | 3 |
| 14 | Customer Support | Support_Tickets, Ticket_Messages, FAQs | 3 |
| 15 | Loyalty & Rewards | Loyalty_Tiers, Loyalty_Accounts, Loyalty_Transactions, Rewards | 4 |
| 16 | Delivery Zones & Geolocation | Delivery_Zones, Branch_Delivery_Zones, Geo_Restrictions | 3 |
| 17 | Content Management | Banners, Pages, Featured_Foods | 3 |
| 18 | Subscriptions & Plans | Subscription_Plans, User_Subscriptions | 2 |
| | **TOTAL** | | **65 Tables** |

---

## Global Relationships (ERD)

```
Users >────────────  Roles                          (N:1)
Users ─────────────< User_Profiles                 (1:1)
Users ─────────────< User_Addresses                (1:N)
Users ─────────────< User_Sessions                 (1:N)
Users ─────────────< Password_Resets               (1:N)
Users ─────────────< OTP_Verifications             (1:N)
Users >────────────  Users (referred_by)           (self-ref, N:1)

Store_Branches >───  Users (manager_id)            (N:1)
Store_Branches ────< Branch_Operating_Hours        (1:N)
Store_Branches ────< Branch_Delivery_Zones         (1:N)
Store_Branches ────< Kitchen_Orders                (1:N)
Store_Branches ────< Deliveries                    (1:N)
Store_Branches ────< Daily_Sales_Reports           (1:N)
Store_Branches ────< Hourly_Order_Stats            (1:N)

Categories >───────  Categories (parent)           (self-ref, N:1)
Categories ────────< Foods                         (1:N)

Foods ─────────────< Food_Images                   (1:N)
Foods ─────────────< Food_Variants                 (1:N)
Foods ─────────────< Food_Addons                   (1:N)
Foods ─────────────< Food_Ingredients              (1:N)
Foods >────────────< Menu_Foods                    (N:M via Menu_Foods)
Foods ─────────────< Featured_Foods                (1:N)
Foods ─────────────< Food_Reviews                  (1:N)

Menus >────────────< Menu_Foods                    (N:M via Menu_Foods)

Ingredients ───────< Food_Ingredients              (1:N)
Ingredients ───────< Stock_Movements               (1:N)

Users ─────────────< Carts                         (1:N)
Carts ─────────────< Cart_Items                    (1:N)
Cart_Items >───────  Foods                         (N:1)
Cart_Items >───────  Food_Variants                 (N:1)

Users ─────────────< Orders                        (1:N)
Orders >───────────  Store_Branches                (N:1)
Orders >───────────  User_Addresses                (N:1)
Orders ────────────< Order_Items                   (1:N)
Orders ────────────< Order_Status_History          (1:N)
Order_Items >──────  Foods                         (N:1)
Order_Items >──────  Food_Variants                 (N:1)
Orders ────────────  Kitchen_Orders                (1:1)
Kitchen_Orders ────< Kitchen_Order_Items           (1:N)
Kitchen_Order_Items > Order_Items                  (N:1)

Users ─────────────< Payment_Methods               (1:N)
Orders ────────────  Payments                      (1:1)
Payments >─────────  Payment_Methods               (N:1)
Users ─────────────  Wallets                       (1:1)
Wallets ───────────< Wallet_Transactions           (1:N)

Users ─────────────  Delivery_Riders               (1:1)
Orders ────────────  Deliveries                    (1:1)
Delivery_Riders ───< Deliveries                    (1:N)
Deliveries ────────< Delivery_Tracking             (1:N)
Delivery_Riders ───< Rider_Earnings                (1:N)
Delivery_Riders ───< Rider_Performance_Reports     (1:N)

Users ─────────────< Notifications                 (1:N)
Notification_Types ─< Notifications                (1:N)
Users ─────────────< Notification_Preferences      (1:N)

Orders ────────────  Reviews                       (1:1)
Reviews ───────────< Food_Reviews                  (1:N)
Food_Reviews >─────  Foods                         (N:1)
Reviews ────────────  Review_Replies               (1:1)
Reviews >──────────  Deliveries                    (N:1)

Promotions ────────< Coupons                       (1:N)
Coupons >──────────  Users                         (N:1)
Coupons >──────────  Orders                        (N:1)

Loyalty_Tiers ─────< Loyalty_Accounts              (1:N)
Users ─────────────  Loyalty_Accounts              (1:1)
Loyalty_Accounts ──< Loyalty_Transactions          (1:N)
Loyalty_Transactions > Orders                      (N:1)

Delivery_Zones ────< Branch_Delivery_Zones         (1:N)
Store_Branches ────< Branch_Delivery_Zones         (1:N)

Users ─────────────< User_Subscriptions            (1:N)
Subscription_Plans ─< User_Subscriptions           (1:N)

Support_Tickets ───< Ticket_Messages               (1:N)
Support_Tickets >──  Orders                        (N:1)
```

---

## Data Type Conventions

| Data Type | Usage | Notes |
|---|---|---|
| `INTEGER` | All primary and foreign keys | Auto-incrementing |
| `TEXT` | String fields, enums, URLs | SQLite uses TEXT for all strings |
| `DECIMAL(10,2)` | Monetary amounts | Always 2 decimal places |
| `DECIMAL(5,2)` | Percentages and rates | e.g., 14.50 for 14.5% |
| `REAL` | GPS coordinates, ratings, distances | Floating point |
| `BOOLEAN` | Flags and toggles | Stored as 0/1 in SQLite |
| `DATE` | Calendar dates without time | Format: YYYY-MM-DD |
| `TIME` | Time of day | Format: HH:MM:SS |
| `DATETIME` | Full timestamps | Format: YYYY-MM-DD HH:MM:SS |
| `JSON` | Arrays and structured objects | Stored as TEXT in SQLite |

---