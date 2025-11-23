from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.models.restaurant import Restaurant
from app.schemas.restaurants import PickRequest, RestaurantOut
from app.services.picker import pick_restaurants
from app.services.providers import (
    BaseRestaurantProvider,
)
from app.services.providers import (
    provider as default_provider,
)

router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
)


def get_provider() -> BaseRestaurantProvider:
    """Dependency to get the active provider.

    Later you can switch provider based on settings/environment.
    """
    return default_provider


@router.get(
    "/search",
    response_model=List[RestaurantOut],
    summary="Search restaurants near a location",
)
async def search_restaurants(
    location: str = Query(..., description="City name or address"),
    radius_km: float = Query(
        5.0,
        ge=0.5,
        le=50,
        description="Search radius in kilometers",
    ),
    cuisine: Optional[str] = Query(
        None,
        description="Cuisine type (e.g., italian, japanese, fast food)",
    ),
    max_results: int = Query(
        20,
        ge=1,
        le=50,
        description="Maximum number of restaurants to return",
    ),
    provider: BaseRestaurantProvider = Depends(get_provider),
) -> List[RestaurantOut]:
    """Search for restaurants (currently using a mock provider)."""
    restaurants: List[Restaurant] = await provider.search_restaurants(
        location=location,
        radius_km=radius_km,
        cuisine=cuisine,
        max_results=max_results,
    )
    return [RestaurantOut(**r.model_dump()) for r in restaurants]


@router.post(
    "/pick",
    response_model=List[RestaurantOut],
    summary="Pick best restaurant options from candidates",
)
async def pick(
    body: PickRequest,
) -> List[RestaurantOut]:
    """Given a list of candidate restaurants, pick the best ones.

    Typical flow for frontend:
    1. Call /restaurants/search to get candidates.
    2. Send candidates to /restaurants/pick to get final suggestions.
    """
    chosen: List[Restaurant] = pick_restaurants(
        restaurants=body.candidates,
        limit=body.limit,
        strategy=body.strategy,
    )
    return [RestaurantOut(**r.model_dump()) for r in chosen]
