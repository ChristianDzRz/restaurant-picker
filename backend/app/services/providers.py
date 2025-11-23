from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.restaurant import Restaurant


class BaseRestaurantProvider(ABC):
    """Abstract base for all restaurant providers (Google, Yelp, Mock, etc.)."""

    @abstractmethod
    async def search_restaurants(
        self,
        location: str,
        radius_km: float = 5.0,
        cuisine: Optional[str] = None,
        max_results: int = 20,
    ) -> List[Restaurant]: ...


class MockRestaurantProvider(BaseRestaurantProvider):
    """Simple in-memory provider with hardcoded data (for development)."""

    async def search_restaurants(
        self,
        location: str,
        radius_km: float = 5.0,
        cuisine: Optional[str] = None,
        max_results: int = 20,
    ) -> List[Restaurant]:
        # In a real provider you'd use `location` and `radius_km`.
        # For now we ignore them and return static sample data.
        data = [
            Restaurant(
                id="1",
                name="Pasta Palace",
                address="123 Main St",
                lat=52.2297,
                lng=21.0122,
                rating=4.5,
                price_level=2,
                cuisine="italian",
                source="mock",
                num_reviews=120,
                url="https://example.com/pasta-palace",
            ),
            Restaurant(
                id="2",
                name="Sushi Garden",
                address="456 Sakura Ave",
                lat=52.23,
                lng=21.01,
                rating=4.7,
                price_level=3,
                cuisine="japanese",
                source="mock",
                num_reviews=200,
                url="https://example.com/sushi-garden",
            ),
            Restaurant(
                id="3",
                name="Budget Bites",
                address="789 Cheap St",
                lat=52.231,
                lng=21.015,
                rating=4.0,
                price_level=1,
                cuisine="fast food",
                source="mock",
                num_reviews=80,
                url="https://example.com/budget-bites",
            ),
        ]

        if cuisine:
            cuisine_lower = cuisine.lower()
            data = [r for r in data if (r.cuisine or "").lower() == cuisine_lower]

        return data[:max_results]


# Global provider instance for now.
# Later you can wire this via dependency injection and environment config.
provider: BaseRestaurantProvider = MockRestaurantProvider()
