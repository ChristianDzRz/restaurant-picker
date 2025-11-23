// src/api/client.ts
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function apiGet<T>(
  path: string,
  params?: Record<string, unknown>,
): Promise<T> {
  const url = new URL(path, API_BASE_URL);
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value === undefined || value === null || value === "") return;
      url.searchParams.set(key, String(value));
    });
  }

  const res = await fetch(url.toString());
  if (!res.ok) {
    throw new Error(`GET ${path} failed with status ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function apiPost<T, B = unknown>(
  path: string,
  body: B,
): Promise<T> {
  const url = new URL(path, API_BASE_URL);

  const res = await fetch(url.toString(), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error(`POST ${path} failed with status ${res.status}`);
  }
  return res.json() as Promise<T>;
}
