# KY Food Delivery System - Setup Guide

## Project Initialization

### 1. Install Dependencies

```bash
# Install NPM packages
npm install

# Install Tauri dependencies (macOS/Linux)
cargo install tauri-cli

# For Windows, see: https://tauri.app/v1/guides/getting-started/prerequisites
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Restore NuGet packages
dotnet restore

# Build solution
dotnet build

# Run migrations (if database exists)
dotnet ef database update --project src/KYFoodDelivery.Data

# Start API server
dotnet run --project src/KYFoodDelivery.API
# API runs on http://localhost:5000
```

### 3. Frontend Setup

```bash
# From project root
npm run serve
# Web app runs on http://localhost:8000
```

### 4. Desktop App (Optional)

```bash
# Start Tauri development
npm run tauri dev

# Build for production
npm run build:desktop
```

## File Structure Quick Reference

```
food-delivery-system/
│
├── web/                          # SPA entry point (served to all portals)
│   ├── index.html
│   ├── js/
│   ├── css/
│   └── assets/
│
├── public/                        # Customer portal routing
│   ├── index.php
│   ├── .htaccess
│   └── js/
│
├── admin/                         # Admin portal routing
│   ├── index.php
│   ├── .htaccess
│   └── js/
│
├── manager/                       # Manager portal routing
│   ├── index.php
│   ├── .htaccess
│   └── js/
│
├── kitchen/                       # Kitchen portal routing
│   ├── index.php
│   ├── .htaccess
│   └── js/
│
├── delivery/                      # Delivery portal routing
│   ├── index.php
│   ├── .htaccess
│   └── js/
│
├── backend/                       # .NET Core API
│   ├── KYFoodDelivery.sln
│   └── src/
│       ├── KYFoodDelivery.API/
│       ├── KYFoodDelivery.Core/
│       └── KYFoodDelivery.Data/
│
├── src-tauri/                     # Tauri desktop app
│   ├── Cargo.toml
│   ├── tauri.conf.json
│   ├── src/
│   │   └── main.rs
│   └── icons/
│
├── resources/                     # Frontend components & styles
│   ├── views/
│   ├── components/
│   ├── assets/
│   └── styles/
│
├── platforms/                     # Mobile builds
│   ├── android/
│   ├── ios/
│   └── desktop/
│
├── config/                        # Configuration files
├── database/                      # Database scripts
├── storage/                       # File uploads
├── docs/                          # Documentation
│
├── package.json                   # NPM configuration
├── .htaccess                      # Root routing
├── PROJECT_STRUCTURE.md           # Folder layout
├── ARCHITECTURE.md                # System architecture
└── SETUP.md                       # This file
```

## Portal URLs (Local Development)

| Portal | URL | User Type |
|--------|-----|-----------|
| Public | `http://localhost:8000/public/` | Customer |
| Admin | `http://localhost:8000/admin/` | System Admin |
| Manager | `http://localhost:8000/manager/` | Restaurant Manager |
| Kitchen | `http://localhost:8000/kitchen/` | Kitchen Staff |
| Delivery | `http://localhost:8000/delivery/` | Delivery Partner |
| Web API | `http://localhost:5000/api/` | Backend |

## Key Features

### Frontend
✅ Multi-portal SPA (Single Page Application)
✅ D3.js data visualizations for admin analytics
✅ Real-time order tracking
✅ Responsive design for all devices
✅ Tauri desktop app integration

### Backend
✅ RESTful API (.NET 8.0)
✅ Entity Framework Core ORM
✅ Role-based access control
✅ Payment processing integration
✅ Real-time notifications ready

### Cross-Platform
✅ Web browsers (Chrome, Firefox, Safari, Edge)
✅ Desktop (Windows, macOS, Linux via Tauri)
✅ Mobile platforms prepared (Android, iOS)

## Development Workflow

### Making Frontend Changes

```bash
# 1. Modify files in resources/views/ or resources/styles/
# 2. Files auto-reload via browser
# 3. Check web console for errors
# 4. Changes reflected immediately
```

### Adding New Portals Routes

1. Create view in `resources/views/[portal]/`
2. Add route in `web/js/router.js`
3. Portal automatically serves via `.htaccess` rewrite rules

### Backend API Development

```bash
# Add new endpoint
# 1. Create controller in API/Controllers/
# 2. Add service in Core/Services/
# 3. Add data access in Data/Repositories/
# 4. Test via Swagger UI at http://localhost:5000/swagger
```

## Database Configuration

### SQL Server
Update connection string in `backend/src/KYFoodDelivery.API/appsettings.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=KYFoodDelivery;User Id=sa;Password=YourPassword;"
  }
}
```

### PostgreSQL
Update connection string similarly:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=kyfooddelivery;Username=postgres;Password=password"
  }
}
```

Run migrations:
```bash
cd backend/src/KYFoodDelivery.Data
dotnet ef database update
```

## Building for Production

### Web Application
```bash
npm run build:web
# Output in web/ folder - deploy to web server
```

### Desktop Application
```bash
npm run build:desktop
# Creates installers in src-tauri/target/release/bundle/
```

### Backend API
```bash
cd backend
dotnet publish -c Release -o ./publish
# Deploy publish folder to server
```

## Environment Variables

Create `.env.production`:

```
API_URL=https://api.kyfood.com
DATABASE_URL=sqlserver://prod-db:1433
PAYMENT_API_KEY=your_key_here
MAPS_API_KEY=your_maps_key
```

## Troubleshooting

### SPA Not Loading
- Check `.htaccess` is properly configured
- Ensure `mod_rewrite` is enabled in Apache
- Check browser console for errors

### API Not Responding
- Verify backend is running on correct port
- Check CORS configuration
- Verify database connection string

### Tauri Build Fails
- Ensure Rust toolchain is up to date: `rustup update`
- Check platform-specific requirements
- Review Tauri documentation for your OS

## Performance Optimization

### Frontend
- Enable gzip compression (configured in `.htaccess`)
- Use lazy loading for images
- Minimize D3.js bundle size

### Backend
- Add database indexes
- Implement response caching
- Use async/await patterns

### Deployment
- CDN for static assets
- Load balancer for API servers
- Database replication for scaling

## Security Checklist

- [ ] All API endpoints require authentication
- [ ] HTTPS enabled in production
- [ ] .htaccess protects sensitive files
- [ ] Database backups automated
- [ ] API rate limiting configured
- [ ] Input validation on all endpoints
- [ ] CORS properly configured

## Deployment Platforms

### Web Hosting
- Apache/IIS with PHP support
- Node.js server
- Cloud platforms (Azure, AWS, GCP)

### Desktop
- Windows installer (.msi)
- macOS app (.dmg)
- Linux packages (.deb, .rpm)

### Mobile
- Android APK/AAB
- iOS App Store
- Google Play Store

## Support & Documentation

- `PROJECT_STRUCTURE.md` - Folder organization
- `ARCHITECTURE.md` - System design
- Backend: `backend/README.md`
- Frontend: `resources/README.md`
- Desktop: `src-tauri/README.md`
