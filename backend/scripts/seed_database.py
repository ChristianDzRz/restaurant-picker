"""
Database seeding script for Restaurant Picker.

This script populates the database with sample restaurant data.
You can run this weekly to update your restaurant database.

Usage:
    python -m scripts.seed_database
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from faker import Faker

from app.db.base import AsyncSessionLocal, init_db
from app.db.crud import bulk_create_restaurants, get_restaurant_count
from app.models.restaurant import Restaurant

fake = Faker()


def generate_sample_restaurants(count: int = 100) -> list[Restaurant]:
    """
    Generate sample restaurant data using Faker.

    In production, replace this with:
    - CSV import
    - External API fetching (Google Places, Yelp)
    - Manual data entry through admin interface

    Args:
        count: Number of restaurants to generate

    Returns:
        List of Restaurant objects
    """
    cuisines = [
        "italian",
        "japanese",
        "chinese",
        "mexican",
        "indian",
        "thai",
        "french",
        "american",
        "mediterranean",
        "korean",
        "vietnamese",
        "greek",
        "spanish",
        "brazilian",
        "fast food",
        "pizza",
        "sushi",
        "bbq",
        "seafood",
        "vegetarian",
    ]

    cities = [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "San Diego",
        "Dallas",
        "San Jose",
        "Austin",
        "Seattle",
        "Denver",
        "Boston",
        "Portland",
        "Miami",
        "Atlanta",
        "San Francisco",
        "Las Vegas",
        "Washington DC",
    ]

    restaurants = []

    for i in range(count):
        city = fake.random_element(elements=cities)
        cuisine = fake.random_element(elements=cuisines)

        # Generate realistic coordinates for US cities (rough approximation)
        # In production, use actual geocoding
        if city == "New York":
            lat, lng = (
                40.7128 + fake.random.uniform(-0.1, 0.1),
                -74.0060 + fake.random.uniform(-0.1, 0.1),
            )
        elif city == "Los Angeles":
            lat, lng = (
                34.0522 + fake.random.uniform(-0.1, 0.1),
                -118.2437 + fake.random.uniform(-0.1, 0.1),
            )
        elif city == "Chicago":
            lat, lng = (
                41.8781 + fake.random.uniform(-0.1, 0.1),
                -87.6298 + fake.random.uniform(-0.1, 0.1),
            )
        elif city == "San Francisco":
            lat, lng = (
                37.7749 + fake.random.uniform(-0.1, 0.1),
                -122.4194 + fake.random.uniform(-0.1, 0.1),
            )
        else:
            # Default to somewhere in the US
            lat = fake.random.uniform(25.0, 48.0)
            lng = fake.random.uniform(-125.0, -65.0)

        restaurant = Restaurant(
            id=f"restaurant_{i + 1}",
            name=fake.company()
            + " "
            + fake.random_element(
                elements=[
                    "Restaurant",
                    "Bistro",
                    "Cafe",
                    "Grill",
                    "Kitchen",
                    "House",
                    "Bar",
                ]
            ),
            address=fake.street_address() + ", " + city,
            lat=lat,
            lng=lng,
            rating=round(fake.random.uniform(3.0, 5.0), 1),
            price_level=fake.random_int(min=1, max=4),
            cuisine=cuisine,
            source="seed_script",
            url=fake.url(),
            num_reviews=fake.random_int(min=10, max=500),
        )
        restaurants.append(restaurant)

    return restaurants


async def seed_database():
    """Main function to seed the database."""
    print("=" * 60)
    print("Restaurant Picker - Database Seeding Script")
    print("=" * 60)

    # Initialize database (create tables if they don't exist)
    print("\n[1/4] Initializing database...")
    await init_db()
    print("✓ Database initialized")

    # Check current count
    async with AsyncSessionLocal() as session:
        current_count = await get_restaurant_count(session)
        print(f"\n[2/4] Current restaurant count: {current_count}")

        if current_count > 0:
            response = input(
                "\nDatabase already has restaurants. Do you want to add more? (y/n): "
            )
            if response.lower() != "y":
                print("Seeding cancelled.")
                return

        # Generate sample data
        print("\n[3/4] Generating sample restaurants...")
        restaurants = generate_sample_restaurants(count=100)
        print(f"✓ Generated {len(restaurants)} sample restaurants")

        # Insert into database
        print("\n[4/4] Inserting restaurants into database...")
        inserted_count = await bulk_create_restaurants(session, restaurants)
        print(f"✓ Inserted {inserted_count} restaurants")

        # Show final count
        final_count = await get_restaurant_count(session)
        print(f"\n✓ Total restaurants in database: {final_count}")

    print("\n" + "=" * 60)
    print("Seeding complete!")
    print("=" * 60)
    print("\nYou can now start the API server:")
    print("  uvicorn app.main:app --reload")
    print("\nOr view the database:")
    print("  sqlite3 restaurant_picker.db")
    print("  > SELECT COUNT(*) FROM restaurants;")
    print("=" * 60)


def main():
    """Entry point for the script."""
    try:
        asyncio.run(seed_database())
    except KeyboardInterrupt:
        print("\n\nSeeding interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during seeding: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
