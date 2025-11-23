// src/components/restaurants/RestaurantList.tsx
import type { Restaurant } from "../../types/restaurant";

interface Props {
  restaurants: Restaurant[];
}

export function RestaurantList({ restaurants }: Props) {
  if (restaurants.length === 0) {
    return <p>No restaurants yet. Try searching.</p>;
  }

  return (
    <div style={{ display: "grid", gap: "0.75rem" }}>
      {restaurants.map((r) => (
        <div
          key={r.id}
          style={{
            backgroundColor: "white",
            padding: "0.9rem 1rem",
            borderRadius: 6,
            boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
          }}
        >
          <div
            style={{ display: "flex", justifyContent: "space-between", gap: 8 }}
          >
            <div>
              <strong>{r.name}</strong>
              <div style={{ fontSize: "0.85rem", color: "#4b5563" }}>
                {r.address}
              </div>
              {r.cuisine && (
                <div style={{ fontSize: "0.8rem", color: "#6b7280" }}>
                  Cuisine: {r.cuisine}
                </div>
              )}
            </div>
            <div style={{ textAlign: "right", fontSize: "0.85rem" }}>
              {typeof r.rating === "number" && (
                <div>
                  ⭐ {r.rating.toFixed(1)}{" "}
                  {r.num_reviews ? (
                    <span>({r.num_reviews} reviews)</span>
                  ) : null}
                </div>
              )}
              {r.price_level && (
                <div style={{ fontFamily: "monospace" }}>
                  {"$".repeat(r.price_level)}
                </div>
              )}
              {r.url && (
                <a
                  href={r.url}
                  target="_blank"
                  rel="noreferrer"
                  style={{ fontSize: "0.8rem", color: "#2563eb" }}
                >
                  Open link
                </a>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
