from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.crud import search_restaurants as db_search_restaurants
from app.db.models import RestaurantDB
from app.models.restaurant import Restaurant
from app.schemas.restaurants import PickRequest, RestaurantOut
from app.services.picker import pick_restaurants

router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
)


@router.get(
    "/search",
    response_model=List[RestaurantOut],
    summary="Search restaurants from database",
)
async def search_restaurants(
    location: str = Query(..., description="City name or location to search"),
    cuisine: Optional[str] = Query(
        None,
        description="Cuisine type (e.g., italian, japanese, fast food)",
    ),
    min_rating: Optional[float] = Query(
        None,
        ge=0.0,
        le=5.0,
        description="Minimum rating filter",
    ),
    max_price_level: Optional[int] = Query(
        None,
        ge=1,
        le=4,
        description="Maximum price level (1=cheap, 4=expensive)",
    ),
    max_results: int = Query(
        20,
        ge=1,
        le=50,
        description="Maximum number of restaurants to return",
    ),
    db: AsyncSession = Depends(get_db),
) -> List[RestaurantOut]:
    """
    Search for restaurants in the database.

    This searches your local database instead of external APIs,
    making it much faster and avoiding rate limits.
    """
    db_restaurants: List[RestaurantDB] = await db_search_restaurants(
        db=db,
        location=location,
        cuisine=cuisine,
        min_rating=min_rating,
        max_price_level=max_price_level,
        limit=max_results,
    )

    # Convert to response models
    return [RestaurantOut(**r.to_dict()) for r in db_restaurants]


@router.post(
    "/pick",
    response_model=List[RestaurantOut],
    summary="Pick best restaurant options from candidates",
)
async def pick(
    body: PickRequest,
) -> List[RestaurantOut]:
    """
    Given a list of candidate restaurants, pick the best ones.

    Typical flow for frontend:
    1. Call /restaurants/search to get candidates from database.
    2. Send candidates to /restaurants/pick to get final suggestions.
    """
    chosen: List[Restaurant] = pick_restaurants(
        restaurants=body.candidates,
        limit=body.limit,
        strategy=body.strategy,
    )
    return [RestaurantOut(**r.model_dump()) for r in chosen]


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantOut,
    summary="Get a specific restaurant by ID",
)
async def get_restaurant(
    restaurant_id: str,
    db: AsyncSession = Depends(get_db),
) -> RestaurantOut:
    """Get details for a specific restaurant."""
    from app.db.crud import get_restaurant as db_get_restaurant

    db_restaurant = await db_get_restaurant(db, restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return RestaurantOut(**db_restaurant.to_dict())


@router.get(
    "/stats/cuisines",
    response_model=List[str],
    summary="Get list of all available cuisines",
)
async def get_cuisines(
    db: AsyncSession = Depends(get_db),
) -> List[str]:
    """Get a list of all unique cuisines in the database."""
    from app.db.crud import get_cuisines as db_get_cuisines

    return await db_get_cuisines(db)


@router.get(
    "/stats/cities",
    response_model=List[str],
    summary="Get list of all available cities",
)
async def get_cities(
    db: AsyncSession = Depends(get_db),
) -> List[str]:
    """Get a list of all cities with restaurants in the database."""
    from app.db.crud import get_cities as db_get_cities

    return await db_get_cities(db)
