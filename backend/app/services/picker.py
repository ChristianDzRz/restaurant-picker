import random
from typing import List

from app.models.restaurant import Restaurant


def score_restaurant(restaurant: Restaurant) -> float:
    """Simple scoring function.

    You can evolve this later (user prefs, distance, etc.).
    """
    rating = restaurant.rating or 0.0
    num_reviews = restaurant.num_reviews or 0
    price_penalty = 0.0

    # Example: penalty for very expensive places (price_level 4)
    if restaurant.price_level and restaurant.price_level >= 4:
        price_penalty = 0.5

    # Cap reviews influence so one viral place doesn't dominate forever
    review_factor = min(num_reviews, 300) / 300.0

    return rating + review_factor - price_penalty


def pick_restaurants(
    restaurants: List[Restaurant],
    limit: int = 3,
    strategy: str = "weighted_random",
) -> List[Restaurant]:
    if not restaurants:
        return []

    limit = max(1, min(limit, len(restaurants)))

    if strategy == "top":
        sorted_restaurants = sorted(restaurants, key=score_restaurant, reverse=True)
        return sorted_restaurants[:limit]

    # Default: weighted random
    scores = [max(score_restaurant(r), 0.01) for r in restaurants]
    total = sum(scores)
    weights = [s / total for s in scores]

    chosen: List[Restaurant] = []
    available = restaurants.copy()
    available_weights = weights.copy()

    for _ in range(limit):
        r = random.choices(available, weights=available_weights, k=1)[0]
        chosen.append(r)

        idx = available.index(r)
        available.pop(idx)
        available_weights.pop(idx)

        if not available:
            break

    return chosen
