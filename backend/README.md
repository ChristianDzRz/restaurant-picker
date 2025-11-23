# Restaurant Picker Backend

FastAPI backend with SQLite database for managing and picking restaurants.

## Features

- 🚀 Fast async API built with FastAPI
- 🗄️ SQLite database with SQLAlchemy ORM
- 🔍 Restaurant search with filters (location, cuisine, rating, price)
- 🎲 Smart restaurant picker with multiple strategies
- 📊 Database seeding script for easy setup

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (async with aiosqlite)
- **ORM**: SQLAlchemy 2.0
- **Package Manager**: uv
- **Python**: 3.11+

---

## Quick Start

### 1. Install Dependencies

```bash
cd backend
uv pip install -e ".[dev]"
```

### 2. Seed the Database

Populate the database with sample restaurant data:

```bash
python -m scripts.seed_database
```

This will create a `restaurant_picker.db` file with 100 sample restaurants.

### 3. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

---

## Project Structure

```
backend/
├── app/
│   ├── api/                 # API endpoints
│   │   ├── health.py       # Health check endpoint
│   │   └── restaurants.py  # Restaurant endpoints
│   ├── core/               # Core configuration
│   │   └── config.py       # Settings and environment config
│   ├── db/                 # Database layer
│   │   ├── base.py         # Database session and engine setup
│   │   ├── models.py       # SQLAlchemy models
│   │   └── crud.py         # Database operations (Create, Read, Update, Delete)
│   ├── models/             # Pydantic models
│   │   └── restaurant.py   # Restaurant data models
│   ├── schemas/            # API request/response schemas
│   │   └── restaurants.py  # Restaurant API schemas
│   ├── services/           # Business logic
│   │   ├── picker.py       # Restaurant picking algorithms
│   │   └── providers.py    # Data providers (deprecated - now using DB)
│   └── main.py             # FastAPI app entry point
├── scripts/                # Utility scripts
│   └── seed_database.py    # Database seeding script
├── pyproject.toml          # Project dependencies
└── restaurant_picker.db    # SQLite database (created after seeding)
```

---

## API Endpoints

### Search Restaurants

```http
GET /restaurants/search?location=New+York&cuisine=italian&min_rating=4.0
```

**Query Parameters:**
- `location` (required): City or location name
- `cuisine` (optional): Cuisine type (e.g., "italian", "japanese")
- `min_rating` (optional): Minimum rating (0.0-5.0)
- `max_price_level` (optional): Maximum price level (1-4)
- `max_results` (optional): Max number of results (default: 20)

**Response:**
```json
[
  {
    "id": "restaurant_1",
    "name": "Pasta Palace",
    "address": "123 Main St, New York",
    "lat": 40.7128,
    "lng": -74.0060,
    "rating": 4.5,
    "price_level": 2,
    "cuisine": "italian",
    "source": "seed_script",
    "url": "https://example.com/pasta-palace",
    "num_reviews": 120
  }
]
```

### Get Restaurant by ID

```http
GET /restaurants/{restaurant_id}
```

### Pick Restaurants

```http
POST /restaurants/pick
Content-Type: application/json

{
  "candidates": [...],
  "limit": 3,
  "strategy": "weighted_random"
}
```

**Strategies:**
- `weighted_random`: Picks randomly with higher weight for better ratings
- `top`: Picks the top-rated restaurants

### Get Available Cuisines

```http
GET /restaurants/stats/cuisines
```

### Get Available Cities

```http
GET /restaurants/stats/cities
```

---

## Database Management

### View Database Contents

```bash
# Enter SQLite shell
sqlite3 restaurant_picker.db

# Count restaurants
SELECT COUNT(*) FROM restaurants;

# View restaurants
SELECT name, cuisine, rating FROM restaurants LIMIT 10;

# Filter by cuisine
SELECT name, rating FROM restaurants WHERE cuisine = 'italian' ORDER BY rating DESC;

# Exit
.exit
```

### Re-seed Database

```bash
# The script will ask if you want to add more data
python -m scripts.seed_database
```

### Reset Database

```bash
# Delete the database file
rm restaurant_picker.db

# Re-seed with fresh data
python -m scripts.seed_database
```

---

## Adding Your Own Restaurant Data

### Option 1: Modify the Seeding Script

Edit `scripts/seed_database.py` and replace the `generate_sample_restaurants()` function with your own data source:

```python
# Example: Load from CSV
import csv

def load_restaurants_from_csv(filepath: str) -> list[Restaurant]:
    restaurants = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            restaurant = Restaurant(
                id=row['id'],
                name=row['name'],
                address=row['address'],
                lat=float(row['lat']),
                lng=float(row['lng']),
                rating=float(row['rating']) if row['rating'] else None,
                price_level=int(row['price_level']) if row['price_level'] else None,
                cuisine=row['cuisine'],
                source='csv_import',
                url=row.get('url'),
                num_reviews=int(row['num_reviews']) if row.get('num_reviews') else None,
            )
            restaurants.append(restaurant)
    return restaurants
```

### Option 2: Create a Custom Import Script

Create a new script in `scripts/` directory:

```python
# scripts/import_from_csv.py
import asyncio
import csv
from app.db.base import AsyncSessionLocal
from app.db.crud import bulk_create_restaurants
from app.models.restaurant import Restaurant

async def import_csv(filepath: str):
    restaurants = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create Restaurant objects from CSV rows
            pass
    
    async with AsyncSessionLocal() as session:
        await bulk_create_restaurants(session, restaurants)

if __name__ == "__main__":
    asyncio.run(import_csv('restaurants.csv'))
```

### Option 3: Use the API Directly

Create an admin endpoint to add restaurants through the API (TODO).

---

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Application
APP_NAME=Restaurant Picker
ENVIRONMENT=local

# Database
DATABASE_URL=sqlite+aiosqlite:///./restaurant_picker.db
DATABASE_ECHO=false
```

---

## Development

### Run Tests

```bash
pytest
```

### Format Code

```bash
black app/
```

### Type Checking

```bash
mypy app/
```

---

## Switching to PostgreSQL (Production)

For production, switch from SQLite to PostgreSQL:

1. **Install PostgreSQL driver:**
```bash
uv pip install asyncpg
```

2. **Update `.env`:**
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/restaurant_picker
```

3. **The code works the same!** SQLAlchemy handles the differences.

---

## Updating Database Weekly

To keep your restaurant data fresh:

### Option 1: Manual Update
```bash
# Run the seeding script weekly
python -m scripts.seed_database
```

### Option 2: Cron Job (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add this line to run every Sunday at 2 AM
0 2 * * 0 cd /path/to/backend && /path/to/.venv/bin/python -m scripts.seed_database
```

### Option 3: Scheduled Task (Windows)
Use Windows Task Scheduler to run `scripts/seed_database.py` weekly.

### Option 4: Fetch from External APIs
Modify `seed_database.py` to fetch real data from Google Places or Yelp APIs and store it locally.

---

## Troubleshooting

### Database Locked Error
**Problem:** `sqlite3.OperationalError: database is locked`

**Solution:** SQLite doesn't handle concurrent writes well. Either:
- Close any open database connections
- Use PostgreSQL for production

### Import Errors
**Problem:** `ModuleNotFoundError: No module named 'app'`

**Solution:** Install the package in editable mode:
```bash
uv pip install -e .
```

### Database Not Found
**Problem:** API returns empty results

**Solution:** Make sure you've seeded the database:
```bash
python -m scripts.seed_database
```

---

## Next Steps

- [ ] Add authentication/admin endpoints
- [ ] Add CSV import functionality
- [ ] Add data validation and duplicate detection
- [ ] Set up Alembic for database migrations
- [ ] Add comprehensive test suite
- [ ] Deploy to production with PostgreSQL
- [ ] Add API rate limiting
- [ ] Add restaurant images/photos support

---

## License

MIT