from typing import Optional

from pydantic import BaseModel


class Restaurant(BaseModel):
    id: str
    name: str
    address: str
    lat: float
    lng: float
    rating: Optional[float] = None
    price_level: Optional[int] = None  # e.g. 1–4
    cuisine: Optional[str] = None
    source: str = "mock"  # 'google', 'yelp', etc.
    url: Optional[str] = None  # link to map / details
    num_reviews: Optional[int] = None
