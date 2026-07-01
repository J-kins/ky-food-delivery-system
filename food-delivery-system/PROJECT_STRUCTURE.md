# KY Food Delivery System - Project Structure

## Directory Organization

### Frontend Web Application
```
web/
├── index.html          # Main entry point
├── js/                 # JavaScript modules
│   ├── app.js
│   ├── router.js
│   └── views/
├── css/                # Stylesheets
├── images/             # Static assets
└── assets/             # Icons, fonts
```

### Portal Routing
- `/public/` - Customer Portal
- `/admin/` - Admin Dashboard
- `/manager/` - Restaurant Manager Portal
- `/kitchen/` - Kitchen Staff Portal
- `/delivery/` - Rider/Delivery Portal

Each portal has:
- `index.php` - Entry point that routes to web/index.html
- `.htaccess` - URL rewriting rules

### Backend Services
```
backend/
├── KYFoodDelivery.sln  # Solution file
└── src/
    ├── KYFoodDelivery.API/       # REST API (.NET 8)
    ├── KYFoodDelivery.Core/      # Business logic
    └── KYFoodDelivery.Data/      # Data access layer
```

### Desktop Application
```
src-tauri/
├── Cargo.toml          # Rust dependencies
├── tauri.conf.json     # Tauri configuration
├── src/
│   └── main.rs         # Rust backend
└── Icons/              # App icons
```

### Multi-Platform Support
```
platforms/
├── android/            # Android app structure
├── ios/                # iOS app structure
└── desktop/            # Desktop app files
```

### Frontend Components & Views
```
resources/
├── views/
│   ├── public/         # Customer portal views
│   ├── admin/          # Admin views
│   ├── manager/        # Manager views
│   ├── kitchen/        # Kitchen views
│   └── delivery/       # Delivery views
└── components/         # Reusable components

resources/styles/
├── base/               # Variables, reset, typography
├── components/         # Component-specific styles
├── layouts/            # Layout CSS files
└── pages/              # Page-specific styles
```

## Build Process

### Web Build
```bash
npm run serve          # Start dev server (port 8000)
npm run build:web      # Build web application
```

### Tauri Build
```bash
npm run build:desktop  # Build Tauri desktop app
npm run tauri          # Tauri commands
```

### Backend Build
```bash
cd backend
dotnet build
dotnet run --project src/KYFoodDelivery.API
```

## URL Routing

### Rewrite Rules (.htaccess)
- `/` → `/web/index.html` (default)
- `/admin/*` → `/admin/index.php?path=*`
- `/manager/*` → `/manager/index.php?path=*`
- `/kitchen/*` → `/kitchen/index.php?path=*`
- `/delivery/*` → `/delivery/index.php?path=*`
- `/api/*` → `/api/index.php?path=*`

## Dependencies

### NPM Packages
- `d3` - Data visualization
- `tiptap` - Rich text editor
- `chart.js` - Charts library
- `axios` - HTTP client
- `date-fns` - Date utilities

### Tauri
- Electron alternative for desktop
- Cross-platform (Windows, macOS, Linux)
- Lightweight runtime

### .NET Backend
- .NET 8.0
- Entity Framework Core
- AutoMapper

## Architecture Flow

1. **Web Request** → Apache/IIS Server
2. **Routing** → `.htaccess` routes to appropriate portal
3. **Portal Entry** → `index.php` loads shared web app
4. **Frontend** → JavaScript SPA handles routing
5. **API Calls** → Backend API endpoint
6. **Backend** → .NET API processes business logic
7. **Database** → Data persistence

## Development Workflow

1. **Frontend Development**
   - Modify files in `/web/` or `/resources/`
   - Hot reload via npm serve
   - Changes reflected immediately

2. **Backend Development**
   - Develop in `/backend/` C# projects
   - Build and run locally
   - Test API endpoints

3. **Desktop (Tauri)**
   - Develop in `/src-tauri/`
   - Run `npm run build:desktop`
   - Generates native executables

4. **Mobile (Future)**
   - Add React Native or Flutter code
   - Build to `/platforms/android/` and `/platforms/ios/`
