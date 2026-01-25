import { PaginatedResponse } from "../app/types";

export async function fetchPaginated<T>(
  endpoint: string,
  cursor?: string,
  limit: number = 20
): Promise<PaginatedResponse<T>> {
  const params = new URLSearchParams();
  if (cursor) params.append("cursor", cursor);
  params.append("limit", limit.toString());

  //Uses NEXT_PUBLIC_API_BASE_URL from .env.local for your Flask backend URL (e.g., http://127.0.0.1:5000/api).
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}${endpoint}?${params.toString()}`);
  if (!res.ok) throw new Error(`Failed to fetch ${endpoint}: ${res.statusText}`);

  const data: PaginatedResponse<T> = await res.json();
  return data;
}

export async function fetchApi<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
  const url = new URL(`${process.env.NEXT_PUBLIC_API_BASE_URL}${endpoint}`);
  if (params) {
    Object.entries(params).forEach(([key, value]) => url.searchParams.append(key, String(value)));
  }

  const res = await fetch(url.toString());
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || "API request failed");
  }
  return res.json();
}

