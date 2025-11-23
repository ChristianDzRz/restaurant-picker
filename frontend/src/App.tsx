// src/App.tsx
import { PageLayout } from "./components/layout/PageLayout";
import { RestaurantSearchForm } from "./components/restaurants/RestaurantSearchForm";
import { RestaurantList } from "./components/restaurants/RestaurantList";
import { PickedRestaurants } from "./components/restaurants/PickedRestaurants";
import { useRestaurantSearch } from "./hooks/useRestaurantSearch";

function App() {
  const { restaurants, picked, loading, picking, error, search, pick } =
    useRestaurantSearch();

  return (
    <PageLayout>
      <RestaurantSearchForm onSearch={search} loading={loading} />

      {error && (
        <div
          style={{
            marginBottom: "1rem",
            padding: "0.6rem 0.8rem",
            backgroundColor: "#fee2e2",
            color: "#b91c1c",
            borderRadius: 4,
            fontSize: "0.9rem",
          }}
        >
          {error}
        </div>
      )}

      <section>
        <h2 style={{ fontSize: "1.1rem", marginBottom: "0.5rem" }}>
          Search results
        </h2>
        {loading ? (
          <p>Loading restaurants...</p>
        ) : (
          <RestaurantList restaurants={restaurants} />
        )}
      </section>

      <PickedRestaurants
        picked={picked}
        onPick={() => pick()}
        disabled={restaurants.length === 0 || picking}
      />
    </PageLayout>
  );
}

export default App;
