// src/hooks/useRestaurantSearch.ts
import { useState } from "react";
import type { Restaurant } from "../types/restaurant";
import { searchRestaurants, pickRestaurants } from "../api/restaurants";

interface SearchParams {
  location: string;
  cuisine?: string;
  radius_km?: number;
  max_results?: number;
}

export function useRestaurantSearch() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [picked, setPicked] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(false);
  const [picking, setPicking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function runSearch(params: SearchParams) {
    try {
      setError(null);
      setPicked([]);
      setLoading(true);
      const result = await searchRestaurants(params);
      setRestaurants(result);
    } catch (err: unknown) {
      console.error(err);
      setError(
        err instanceof Error ? err.message : "Failed to search restaurants",
      );
    } finally {
      setLoading(false);
    }
  }

  async function runPick(options?: {
    limit?: number;
    strategy?: "weighted_random" | "top";
  }) {
    if (restaurants.length === 0) return;

    try {
      setError(null);
      setPicking(true);
      const result = await pickRestaurants({
        candidates: restaurants,
        limit: options?.limit,
        strategy: options?.strategy,
      });
      setPicked(result);
    } catch (err: unknown) {
      console.error(err);
      setError(
        err instanceof Error ? err.message : "Failed to pick restaurants",
      );
    } finally {
      setPicking(false);
    }
  }

  return {
    restaurants,
    picked,
    loading,
    picking,
    error,
    search: runSearch,
    pick: runPick,
  };
}
