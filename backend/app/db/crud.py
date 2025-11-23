"""
CRUD (Create, Read, Update, Delete) operations for Restaurant model.
"""

from typing import List, Optional

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import RestaurantDB
from app.models.restaurant import Restaurant


async def create_restaurant(db: AsyncSession, restaurant: Restaurant) -> RestaurantDB:
    """
    Create a new restaurant in the database.

    Args:
        db: Database session
        restaurant: Pydantic Restaurant model

    Returns:
        Created RestaurantDB instance
    """
    db_restaurant = RestaurantDB(
        id=restaurant.id,
        name=restaurant.name,
        address=restaurant.address,
        lat=restaurant.lat,
        lng=restaurant.lng,
        rating=restaurant.rating,
        price_level=restaurant.price_level,
        cuisine=restaurant.cuisine,
        source=restaurant.source,
        url=restaurant.url,
        num_reviews=restaurant.num_reviews,
    )
    db.add(db_restaurant)
    await db.commit()
    await db.refresh(db_restaurant)
    return db_restaurant


async def get_restaurant(
    db: AsyncSession, restaurant_id: str
) -> Optional[RestaurantDB]:
    """
    Get a restaurant by ID.

    Args:
        db: Database session
        restaurant_id: Restaurant ID

    Returns:
        RestaurantDB instance or None if not found
    """
    result = await db.execute(
        select(RestaurantDB).where(RestaurantDB.id == restaurant_id)
    )
    return result.scalar_one_or_none()


async def get_restaurants(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[RestaurantDB]:
    """
    Get all restaurants with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of RestaurantDB instances
    """
    result = await db.execute(select(RestaurantDB).offset(skip).limit(limit))
    return list(result.scalars().all())


async def search_restaurants(
    db: AsyncSession,
    location: Optional[str] = None,
    cuisine: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_price_level: Optional[int] = None,
    limit: int = 20,
) -> List[RestaurantDB]:
    """
    Search restaurants with filters.

    Args:
        db: Database session
        location: City or location name (searches in city, address, name)
        cuisine: Cuisine type (case-insensitive)
        min_rating: Minimum rating filter
        max_price_level: Maximum price level (1-4)
        limit: Maximum number of results

    Returns:
        List of matching RestaurantDB instances
    """
    query = select(RestaurantDB)

    # Location filter - search in city, address, or name
    if location:
        location_lower = f"%{location.lower()}%"
        query = query.where(
            or_(
                func.lower(RestaurantDB.city).like(location_lower),
                func.lower(RestaurantDB.address).like(location_lower),
                func.lower(RestaurantDB.name).like(location_lower),
            )
        )

    # Cuisine filter
    if cuisine:
        query = query.where(func.lower(RestaurantDB.cuisine) == cuisine.lower())

    # Rating filter
    if min_rating is not None:
        query = query.where(RestaurantDB.rating >= min_rating)

    # Price level filter
    if max_price_level is not None:
        query = query.where(RestaurantDB.price_level <= max_price_level)

    # Order by rating (highest first), then by number of reviews
    query = query.order_by(
        RestaurantDB.rating.desc().nulls_last(),
        RestaurantDB.num_reviews.desc().nulls_last(),
    )

    # Apply limit
    query = query.limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def search_restaurants_near_point(
    db: AsyncSession,
    lat: float,
    lng: float,
    radius_km: float = 5.0,
    cuisine: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_price_level: Optional[int] = None,
    limit: int = 20,
) -> List[RestaurantDB]:
    """
    Search restaurants near a geographic point.

    Uses the Haversine formula to calculate distance.
    Note: For production with large datasets, consider using PostGIS or similar.

    Args:
        db: Database session
        lat: Latitude of search center
        lng: Longitude of search center
        radius_km: Search radius in kilometers
        cuisine: Cuisine type filter
        min_rating: Minimum rating filter
        max_price_level: Maximum price level filter
        limit: Maximum number of results

    Returns:
        List of matching RestaurantDB instances
    """
    # Simple bounding box filter first (much faster than haversine)
    # Approximate: 1 degree latitude ≈ 111 km
    lat_delta = radius_km / 111.0
    # Longitude varies by latitude, rough approximation
    lng_delta = radius_km / (111.0 * abs(func.cos(func.radians(lat))))

    query = select(RestaurantDB).where(
        RestaurantDB.lat.between(lat - lat_delta, lat + lat_delta),
        RestaurantDB.lng.between(lng - lng_delta, lng + lng_delta),
    )

    # Apply other filters
    if cuisine:
        query = query.where(func.lower(RestaurantDB.cuisine) == cuisine.lower())

    if min_rating is not None:
        query = query.where(RestaurantDB.rating >= min_rating)

    if max_price_level is not None:
        query = query.where(RestaurantDB.price_level <= max_price_level)

    # Order by rating
    query = query.order_by(
        RestaurantDB.rating.desc().nulls_last(),
        RestaurantDB.num_reviews.desc().nulls_last(),
    )

    # Apply limit
    query = query.limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def update_restaurant(
    db: AsyncSession,
    restaurant_id: str,
    **kwargs,
) -> Optional[RestaurantDB]:
    """
    Update a restaurant's fields.

    Args:
        db: Database session
        restaurant_id: Restaurant ID
        **kwargs: Fields to update

    Returns:
        Updated RestaurantDB instance or None if not found
    """
    db_restaurant = await get_restaurant(db, restaurant_id)
    if db_restaurant is None:
        return None

    for key, value in kwargs.items():
        if hasattr(db_restaurant, key):
            setattr(db_restaurant, key, value)

    await db.commit()
    await db.refresh(db_restaurant)
    return db_restaurant


async def delete_restaurant(db: AsyncSession, restaurant_id: str) -> bool:
    """
    Delete a restaurant from the database.

    Args:
        db: Database session
        restaurant_id: Restaurant ID

    Returns:
        True if deleted, False if not found
    """
    db_restaurant = await get_restaurant(db, restaurant_id)
    if db_restaurant is None:
        return False

    await db.delete(db_restaurant)
    await db.commit()
    return True


async def bulk_create_restaurants(
    db: AsyncSession,
    restaurants: List[Restaurant],
) -> int:
    """
    Bulk insert multiple restaurants.

    Args:
        db: Database session
        restaurants: List of Pydantic Restaurant models

    Returns:
        Number of restaurants created
    """
    db_restaurants = [
        RestaurantDB(
            id=r.id,
            name=r.name,
            address=r.address,
            lat=r.lat,
            lng=r.lng,
            rating=r.rating,
            price_level=r.price_level,
            cuisine=r.cuisine,
            source=r.source,
            url=r.url,
            num_reviews=r.num_reviews,
        )
        for r in restaurants
    ]

    db.add_all(db_restaurants)
    await db.commit()
    return len(db_restaurants)


async def get_restaurant_count(db: AsyncSession) -> int:
    """
    Get total number of restaurants in database.

    Args:
        db: Database session

    Returns:
        Total count of restaurants
    """
    result = await db.execute(select(func.count(RestaurantDB.id)))
    return result.scalar_one()


async def get_cuisines(db: AsyncSession) -> List[str]:
    """
    Get list of all unique cuisines in the database.

    Args:
        db: Database session

    Returns:
        List of cuisine names (sorted)
    """
    result = await db.execute(
        select(RestaurantDB.cuisine)
        .distinct()
        .where(RestaurantDB.cuisine.is_not(None))
        .order_by(RestaurantDB.cuisine)
    )
    return list(result.scalars().all())


async def get_cities(db: AsyncSession) -> List[str]:
    """
    Get list of all unique cities in the database.

    Args:
        db: Database session

    Returns:
        List of city names (sorted)
    """
    result = await db.execute(
        select(RestaurantDB.city)
        .distinct()
        .where(RestaurantDB.city.is_not(None))
        .order_by(RestaurantDB.city)
    )
    return list(result.scalars().all())
