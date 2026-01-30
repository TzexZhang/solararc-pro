# SolarArc Pro Backend - Project Structure

## Complete File Structure

```
backend/
├── app/
│   ├── __init__.py                    # Application package initialization
│   ├── main.py                        # FastAPI application entry point
│   ├── config.py                      # Configuration management (Pydantic Settings)
│   ├── database.py                    # Database connection and session management
│   │
│   ├── models/                        # SQLAlchemy ORM Models
│   │   ├── __init__.py
│   │   ├── user.py                    # User and PasswordReset models
│   │   ├── building.py                # Building model with spatial data
│   │   ├── solar_position.py          # Solar position pre-calculation model
│   │   ├── shadow_analysis.py         # Shadow analysis cache model
│   │   ├── project.py                 # User project model
│   │   ├── analysis_report.py         # Analysis report model
│   │   └── building_score.py          # Building daylight score model
│   │
│   ├── schemas/                       # Pydantic Schemas (Request/Response)
│   │   ├── __init__.py
│   │   ├── user.py                    # User schemas (Create, Update, Response)
│   │   ├── building.py                # Building schemas
│   │   ├── solar.py                   # Solar position schemas
│   │   ├── analysis.py                # Analysis request/response schemas
│   │   └── auth.py                    # Authentication schemas (Token, TokenData)
│   │
│   ├── api/                           # API Route Handlers
│   │   ├── __init__.py
│   │   ├── auth.py                    # Authentication endpoints
│   │   ├── buildings.py               # Building data endpoints
│   │   ├── solar.py                   # Solar position calculation endpoints
│   │   ├── shadows.py                 # Shadow calculation endpoints
│   │   ├── analysis.py                # Sunlight analysis endpoints
│   │   └── reports.py                 # Analysis report endpoints
│   │
│   ├── services/                      # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── auth_service.py            # Authentication business logic
│   │   ├── solar_service.py           # Solar position calculations (pvlib)
│   │   ├── shadow_service.py          # Shadow calculations (shapely)
│   │   └── report_service.py          # Report generation logic
│   │
│   ├── core/                          # Core Functionality
│   │   ├── __init__.py
│   │   ├── security.py                # JWT and password hashing (bcrypt)
│   │   ├── deps.py                    # Dependency injection (get_current_user)
│   │   └── utils.py                   # Utility functions
│   │
│   └── alembic/                       # Database Migration
│       ├── versions/                  # Migration versions (empty initially)
│       ├── env.py                     # Alembic environment configuration
│       └── script.py.mako             # Migration script template
│
├── tests/                             # Test Suite
│   ├── __init__.py
│   ├── test_auth.py                   # Authentication tests
│   ├── test_solar.py                  # Solar position tests
│   └── test_buildings.py              # Building data tests
│
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── Dockerfile                         # Docker container configuration
├── README.md                          # Project documentation
├── start.sh                           # Linux/Mac startup script
├── start.bat                          # Windows startup script
└── alembic.ini                        # Alembic configuration
```

## Key Components Overview

### 1. Models (Database Schema)
All models use **VARCHAR(36) UUID** as primary keys:
- **User**: User accounts with authentication
- **Building**: 3D building data with GeoJSON footprints
- **SolarPositionPrecalc**: Cached solar position calculations
- **ShadowAnalysisCache**: Cached shadow calculations
- **Project**: User-saved analysis projects
- **AnalysisReport**: Generated analysis reports
- **BuildingScore**: Daylight scoring for buildings

### 2. API Endpoints

**Authentication** (`/api/v1/auth`):
- User registration, login, logout
- Password management (change, reset)
- JWT token-based authentication

**Buildings** (`/api/v1/buildings`):
- Query buildings by bounding box
- CRUD operations for buildings
- Import GeoJSON building data

**Solar** (`/api/v1/solar`):
- Calculate solar position (altitude, azimuth)
- Get 24-hour solar positions
- Sunrise/sunset times

**Shadows** (`/api/v1/shadows`):
- Calculate building shadows
- Shadow overlap analysis
- Winter/summer solstice comparison

**Analysis** (`/api/v1/analysis`):
- Point sunlight duration analysis
- Shadow overlap analysis

**Reports** (`/api/v1/analysis/reports`):
- Create analysis reports
- Get report list and details
- Export reports to PDF
- Building daylight scores

### 3. Services (Business Logic)
- **auth_service**: User authentication, password management
- **solar_service**: Solar position calculations using pvlib
- **shadow_service**: Shadow calculations using shapely
- **report_service**: Report generation and scoring

### 4. Core Features
- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: bcrypt encryption
- **Spatial Data**: GeoAlchemy2 + MySQL spatial types
- **API Documentation**: Auto-generated Swagger/ReDoc docs
- **Error Handling**: Centralized exception handling
- **CORS**: Configurable CORS middleware

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Framework | FastAPI 0.104+ | High-performance API |
| ASGI Server | Uvicorn | Async server |
| Production Server | Gunicorn | Process manager |
| ORM | SQLAlchemy 2.0+ | Database ORM |
| Database | MySQL 8.0+ | Relational database |
| Spatial DB | GeoAlchemy2 | Spatial data types |
| Solar Calc | pvlib 0.10+ | Solar position algorithm |
| Geometry | shapely 2.0+ | Spatial calculations |
| Auth | PyJWT + passlib | JWT & password hashing |
| Validation | Pydantic 2.x | Request/response validation |
| Testing | pytest | Unit testing |

## Environment Variables

Required variables in `.env`:
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/solararc_pro
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:5173
API_PORT=8000
```

## Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run development server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest tests/

# Run with Docker
docker build -t solararc-backend .
docker run -p 8000:8000 solararc-backend
```

## API Documentation

After starting the server:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

## Database Migrations

```bash
# Initialize Alembic (first time only)
alembic init app/alembic

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Production Deployment

### Using Gunicorn
```bash
gunicorn app.main:app \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker
```

### Using Docker
```bash
docker build -t solararc-backend .
docker run -d -p 8000:8000 --name backend solararc-backend
```

## File Descriptions

### Configuration Files
- **config.py**: Centralized configuration using Pydantic Settings
- **database.py**: Database engine, session, and base class
- **alembic.ini**: Database migration configuration

### Entry Point
- **main.py**: FastAPI application setup, middleware, route registration

### Models (database/)
All models use UUID primary keys and include timestamps

### Schemas (schemas/)
Pydantic models for request validation and response serialization

### API Routes (api/)
FastAPI routers handling HTTP requests and responses

### Services (services/)
Business logic separated from API layer for better testability

### Tests (tests/)
Pytest-based test suite with fixtures for database and client

## Security Features

1. **Password Hashing**: bcrypt with salt
2. **JWT Authentication**: 7-day token expiration
3. **Account Locking**: Auto-lock after 5 failed login attempts
4. **CORS Protection**: Configurable allowed origins
5. **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
6. **Input Validation**: Pydantic schema validation

## Performance Optimizations

1. **Database Connection Pooling**: Configurable pool size
2. **Spatial Indexing**: MySQL SPATIAL INDEX on geometry columns
3. **Shadow Caching**: Cache table for computed shadows
4. **Pre-calculated Solar Positions**: Key dates cached in database
5. **Async Operations**: FastAPI async request handling

## Development Guidelines

1. **Add New Endpoint**:
   - Create Pydantic schemas in `schemas/`
   - Implement business logic in `services/`
   - Add route handler in `api/`
   - Register route in `main.py`

2. **Database Changes**:
   - Modify model in `models/`
   - Generate migration: `alembic revision --autogenerate`
   - Apply migration: `alembic upgrade head`

3. **Testing**:
   - Write test in `tests/`
   - Use pytest fixtures for database
   - Run with: `pytest tests/`

## Known Limitations

1. **Solar Calculations**: Fallback to simplified math if pvlib not installed
2. **Shadow Calculation**: Simplified projection algorithm (not full 3D)
3. **Report Generation**: Basic PDF support (reportlab required)
4. **Email**: Password reset emails not implemented (development only)

## Future Enhancements

1. Real email service for password resets
2. Advanced 3D shadow rendering
3. Cloud integration for weather data
4. Redis caching layer
5. Background task queue (Celery)
6. GraphQL API support
7. WebSocket for real-time updates
