# KY Food Delivery System - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER (Frontend)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  Web Portals │  │   Desktop    │  │   Mobile Platforms   │   │
│  │  (JavaScript)│  │   (Tauri)    │  │  (Android/iOS)       │   │
│  │              │  │              │  │                      │   │
│  │ • Public     │  │ • Windows    │  │ • React Native/      │   │
│  │ • Admin      │  │ • macOS      │  │   Flutter            │   │
│  │ • Manager    │  │ • Linux      │  │                      │   │
│  │ • Kitchen    │  │              │  │                      │   │
│  │ • Delivery   │  │              │  │                      │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│         │                 │                      │               │
└─────────┼─────────────────┼──────────────────────┼───────────────┘
          │                 │                      │
          └─────────────────┼──────────────────────┘
                            │
┌───────────────────────────┴──────────────────────────────────────┐
│              ROUTING LAYER (Apache/IIS)                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  .htaccess Routing Rules:                                         │
│  • / → web/index.html (SPA entry)                               │
│  • /admin/* → admin/index.php → web/index.html                 │
│  • /manager/* → manager/index.php → web/index.html             │
│  • /kitchen/* → kitchen/index.php → web/index.html             │
│  • /delivery/* → delivery/index.php → web/index.html           │
│  • /api/* → api/index.php (Backend)                            │
│                                                                   │
└──────────────────────────┬───────────────────────────────────────┘
                           │
┌──────────────────────────┴───────────────────────────────────────┐
│                   API LAYER (.NET Backend)                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  KYFoodDelivery.API (REST Endpoints)                            │
│  ├── Controllers                                                  │
│  │   ├── AuthController                                          │
│  │   ├── OrdersController                                        │
│  │   ├── RestaurantsController                                   │
│  │   ├── UsersController                                         │
│  │   ├── DeliveryController                                      │
│  │   └── PaymentsController                                      │
│  │                                                                │
│  └── Services                                                     │
│      ├── OrderService                                            │
│      ├── RestaurantService                                       │
│      ├── DeliveryService                                         │
│      └── PaymentService                                          │
│                                                                   │
│  KYFoodDelivery.Core (Business Logic)                           │
│  ├── Models                                                       │
│  ├── Interfaces                                                   │
│  └── Services                                                     │
│                                                                   │
│  KYFoodDelivery.Data (Data Access)                              │
│  ├── DbContext (Entity Framework Core)                          │
│  ├── Repositories                                                │
│  └── Migrations                                                  │
│                                                                   │
└──────────────────────────┬───────────────────────────────────────┘
                           │
┌──────────────────────────┴───────────────────────────────────────┐
│               DATA LAYER (Database)                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  • SQL Server / PostgreSQL                                       │
│  • Users, Restaurants, Orders, Payments                          │
│  • Delivery Routes, Transactions                                 │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Portal Structure & Responsibilities

### 1. **Public Portal** (`/public/`)
Customer-facing application for browsing and ordering food.

**Modules:**
- Home & Restaurant Discovery
- Menu Browse & Search
- Cart Management
- Order Checkout
- Order Tracking
- User Profile & Orders

### 2. **Admin Portal** (`/admin/`)
System administration and platform management.

**Modules:**
- Dashboard with D3.js analytics
- System-wide analytics & reports
- Order monitoring
- Payment monitoring
- Delivery fleet monitoring
- Restaurants management
- Users management
- System settings

### 3. **Manager Portal** (`/manager/`)
Restaurant manager operations interface.

**Modules:**
- Restaurant dashboard
- Orders management
- Menu management
- Inventory management
- Staff management
- Promotions management
- Reviews management
- Reports

### 4. **Kitchen Portal** (`/kitchen/`)
Kitchen staff order preparation interface.

**Modules:**
- Incoming orders display
- Kitchen queue (visual order management)
- Order preparation tracking
- Inventory visibility
- Settings

### 5. **Delivery Portal** (`/delivery/`)
Rider/delivery partner operations.

**Modules:**
- Delivery requests & job acceptance
- Real-time navigation/mapping
- Delivery status tracking
- Rider profile management
- Earnings tracking

## Technology Stack

### Frontend
- **Framework:** Vanilla JavaScript (ES6+)
- **Visualization:** D3.js, Chart.js
- **Rich Text Editor:** Tiptap
- **HTTP Client:** Axios
- **Date Utilities:** date-fns

### Desktop
- **Framework:** Tauri (Rust backend)
- **Targets:** Windows, macOS, Linux

### Mobile (Future)
- **Framework:** React Native / Flutter
- **Platforms:** Android, iOS

### Backend
- **Runtime:** .NET 8.0
- **ORM:** Entity Framework Core
- **Mapping:** AutoMapper
- **Database:** SQL Server / PostgreSQL

### DevOps
- **Server:** Apache/IIS
- **Routing:** .htaccess
- **Package Manager:** npm, cargo, dotnet

## Data Flow

### User Request Flow
1. User accesses `/admin/dashboard`
2. Apache routes via `.htaccess` to `admin/index.php`
3. `admin/index.php` loads `web/index.html`
4. JavaScript SPA initializes and detects route
5. Frontend loads admin portal component
6. Admin makes API call to `/api/dashboard`
7. Backend processes request, queries database
8. Response sent back to frontend
9. D3.js renders visualization with data

### Order Creation Flow
1. Customer adds items to cart on Public portal
2. Submits checkout form
3. Frontend validates and sends POST to `/api/orders`
4. Backend API:
   - Validates order data
   - Creates order record
   - Updates restaurant inventory
   - Triggers payment processing
   - Returns order confirmation
5. Frontend navigates to order tracking
6. Kitchen receives notification
7. Manager gets order update
8. Rider receives delivery request

## Security Considerations

- **Input Validation:** All frontend inputs validated before API calls
- **API Security:** CORS, CSRF protection, authentication tokens
- **Role-Based Access:** Portal-level routing with permissions
- **Data Encryption:** HTTPS/TLS for all communications
- **.htaccess Protection:** Restricted access to sensitive files/folders

## Deployment Structure

```
production/
├── web/                    # Compiled SPA (served via Apache)
├── public/                 # Public portal entry point
├── admin/                  # Admin portal entry point
├── manager/                # Manager portal entry point
├── kitchen/                # Kitchen portal entry point
├── delivery/               # Delivery portal entry point
├── api/                    # Backend API (ASP.NET)
├── backend/                # C# solution built binaries
└── platforms/              # Mobile & desktop builds
    ├── android/
    ├── ios/
    └── desktop/
```

## Scaling Strategy

### Horizontal Scaling
- Load balancer routing to multiple API servers
- Database read replicas for analytics
- CDN for static assets

### Vertical Scaling
- Database optimization (indexing, partitioning)
- API caching layer (Redis)
- Background job processing (job queue)

### Monitoring
- Backend logging & tracing
- Frontend error tracking
- Database performance monitoring
- Real-time metrics dashboard
