"""
SQLAlchemy models for the Restaurant Picker application.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class RestaurantDB(Base):
    """
    SQLAlchemy model for Restaurant table.

    This is the database representation of a restaurant.
    Use this for database operations (queries, inserts, updates).
    """

    __tablename__ = "restaurants"

    # Primary key
    id: Mapped[str] = mapped_column(String(255), primary_key=True)

    # Required fields
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    lng: Mapped[float] = mapped_column(Float, nullable=False, index=True)

    # Optional fields
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    price_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cuisine: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, index=True
    )
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="manual")
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    num_reviews: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Location/city for filtering
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Metadata timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Restaurant(id={self.id}, name={self.name}, cuisine={self.cuisine})>"

    def to_dict(self) -> dict:
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "lat": self.lat,
            "lng": self.lng,
            "rating": self.rating,
            "price_level": self.price_level,
            "cuisine": self.cuisine,
            "source": self.source,
            "url": self.url,
            "num_reviews": self.num_reviews,
            "city": self.city,
            "country": self.country,
        }
