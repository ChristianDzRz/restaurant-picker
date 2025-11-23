// src/components/restaurants/PickedRestaurants.tsx
import type { Restaurant } from "../../types/restaurant";

interface Props {
  picked: Restaurant[];
  onPick: () => void;
  disabled: boolean;
}

export function PickedRestaurants({ picked, onPick, disabled }: Props) {
  return (
    <section style={{ marginTop: "1.5rem" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "0.5rem",
        }}
      >
        <h2 style={{ margin: 0, fontSize: "1.1rem" }}>Suggested picks</h2>
        <button
          type="button"
          onClick={onPick}
          disabled={disabled}
          style={{
            padding: "0.4rem 0.8rem",
            borderRadius: 4,
            border: "1px solid #2563eb",
            backgroundColor: disabled ? "#e5e7eb" : "white",
            color: disabled ? "#6b7280" : "#2563eb",
            cursor: disabled ? "default" : "pointer",
            fontSize: "0.85rem",
          }}
        >
          {disabled ? "Pick disabled" : "Pick for me"}
        </button>
      </div>

      {picked.length === 0 ? (
        <p style={{ fontSize: "0.9rem", color: "#6b7280" }}>
          After searching, click &ldquo;Pick for me&rdquo; to see suggestions.
        </p>
      ) : (
        <div style={{ display: "grid", gap: "0.75rem" }}>
          {picked.map((r) => (
            <div
              key={r.id}
              style={{
                backgroundColor: "#fefce8",
                padding: "0.9rem 1rem",
                borderRadius: 6,
                border: "1px solid #facc15",
              }}
            >
              <strong>{r.name}</strong>
              <div style={{ fontSize: "0.85rem" }}>{r.address}</div>
              {typeof r.rating === "number" && (
                <div style={{ fontSize: "0.85rem", marginTop: 4 }}>
                  ⭐ {r.rating.toFixed(1)}{" "}
                  {r.num_reviews ? (
                    <span>({r.num_reviews} reviews)</span>
                  ) : null}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
