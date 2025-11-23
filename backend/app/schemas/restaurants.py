from typing import List

from pydantic import BaseModel

from app.models.restaurant import Restaurant


class RestaurantOut(Restaurant):
    """Response schema for a restaurant"""

    pass


class PickRequest(BaseModel):
    """Request body for the /restaurants/pick endpoint"""

    candidates: List[Restaurant]
    limit: int = 3
    strategy: str = "weighted_random"
