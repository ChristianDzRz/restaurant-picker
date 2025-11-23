// src/components/restaurants/RestaurantSearchForm.tsx
import { useState } from "react";

interface SearchParams {
  location: string;
  cuisine?: string;
  radius_km?: number;
  max_results?: number;
}

interface Props {
  onSearch: (params: SearchParams) => void;
  loading: boolean;
}

export function RestaurantSearchForm({ onSearch, loading }: Props) {
  const [location, setLocation] = useState("");
  const [cuisine, setCuisine] = useState("");
  const [radiusKm, setRadiusKm] = useState("5");
  const [maxResults, setMaxResults] = useState("20");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!location.trim()) {
      alert("Please enter a location");
      return;
    }

    onSearch({
      location: location.trim(),
      cuisine: cuisine.trim() || undefined,
      radius_km: parseFloat(radiusKm) || undefined,
      max_results: parseInt(maxResults, 10) || undefined,
    });
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        backgroundColor: "white",
        padding: "1.5rem",
        borderRadius: 8,
        boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
        marginBottom: "1.5rem",
      }}
    >
      <div style={{ display: "grid", gap: "1rem" }}>
        <div>
          <label
            htmlFor="location"
            style={{
              display: "block",
              marginBottom: "0.25rem",
              fontSize: "0.875rem",
              fontWeight: 500,
            }}
          >
            Location *
          </label>
          <input
            id="location"
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="e.g., New York, NY"
            disabled={loading}
            style={{
              width: "100%",
              padding: "0.5rem 0.75rem",
              border: "1px solid #d1d5db",
              borderRadius: 4,
              fontSize: "0.875rem",
            }}
          />
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "1rem",
          }}
        >
          <div>
            <label
              htmlFor="cuisine"
              style={{
                display: "block",
                marginBottom: "0.25rem",
                fontSize: "0.875rem",
                fontWeight: 500,
              }}
            >
              Cuisine
            </label>
            <input
              id="cuisine"
              type="text"
              value={cuisine}
              onChange={(e) => setCuisine(e.target.value)}
              placeholder="e.g., Italian"
              disabled={loading}
              style={{
                width: "100%",
                padding: "0.5rem 0.75rem",
                border: "1px solid #d1d5db",
                borderRadius: 4,
                fontSize: "0.875rem",
              }}
            />
          </div>

          <div>
            <label
              htmlFor="radius"
              style={{
                display: "block",
                marginBottom: "0.25rem",
                fontSize: "0.875rem",
                fontWeight: 500,
              }}
            >
              Radius (km)
            </label>
            <input
              id="radius"
              type="number"
              value={radiusKm}
              onChange={(e) => setRadiusKm(e.target.value)}
              min="1"
              max="50"
              disabled={loading}
              style={{
                width: "100%",
                padding: "0.5rem 0.75rem",
                border: "1px solid #d1d5db",
                borderRadius: 4,
                fontSize: "0.875rem",
              }}
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="maxResults"
            style={{
              display: "block",
              marginBottom: "0.25rem",
              fontSize: "0.875rem",
              fontWeight: 500,
            }}
          >
            Max Results
          </label>
          <input
            id="maxResults"
            type="number"
            value={maxResults}
            onChange={(e) => setMaxResults(e.target.value)}
            min="5"
            max="50"
            disabled={loading}
            style={{
              width: "100%",
              padding: "0.5rem 0.75rem",
              border: "1px solid #d1d5db",
              borderRadius: 4,
              fontSize: "0.875rem",
            }}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "0.625rem 1.25rem",
            backgroundColor: loading ? "#9ca3af" : "#2563eb",
            color: "white",
            border: "none",
            borderRadius: 4,
            fontSize: "0.875rem",
            fontWeight: 500,
            cursor: loading ? "not-allowed" : "pointer",
            transition: "background-color 0.2s",
          }}
        >
          {loading ? "Searching..." : "Search Restaurants"}
        </button>
      </div>
    </form>
  );
}
