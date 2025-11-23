export interface Restaurant {
  id: string;
  name: string;
  address: string;
  lat: number;
  lng: number;
  rating?: number | null;
  price_level?: number | null;
  cuisine?: string | null;
  source: string;
  url?: string | null;
  num_reviews?: number | null;
}
