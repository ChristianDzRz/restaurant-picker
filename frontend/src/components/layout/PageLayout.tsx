// src/components/layout/PageLayout.tsx
import type { PropsWithChildren } from "react";

export function PageLayout({ children }: PropsWithChildren) {
  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#f7f7f7" }}>
      <header
        style={{
          padding: "1rem 2rem",
          backgroundColor: "#111827",
          color: "white",
        }}
      >
        <h1 style={{ margin: 0, fontSize: "1.5rem" }}>Restaurant Picker</h1>
        <p style={{ margin: 0, fontSize: "0.9rem", opacity: 0.8 }}>
          Help me decide where to eat
        </p>
      </header>
      <main style={{ padding: "1.5rem 2rem", maxWidth: 960, margin: "0 auto" }}>
        {children}
      </main>
    </div>
  );
}
