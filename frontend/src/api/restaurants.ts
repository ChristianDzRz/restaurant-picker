import { apiGet, apiPost } from "./client";
import type { Restaurant } from "../types/restaurant";

export async function searchRestaurants(params: {
  location: string;
  cuisine?: string;
  radius_km?: number;
  max_results?: number;
}): Promise<Restaurant[]> {
  return apiGet<Restaurant[]>("/restaurants/search", params);
}

export async function pickRestaurants(input: {
  candidates: Restaurant[];
  limit?: number;
  strategy?: "weighted_random" | "top";
}): Promise<Restaurant[]> {
  return apiPost<Restaurant[], typeof input>("/restaurants/pick", {
    ...input,
    limit: input.limit ?? 3,
    strategy: input.strategy ?? "weighted_random",
  });
}
