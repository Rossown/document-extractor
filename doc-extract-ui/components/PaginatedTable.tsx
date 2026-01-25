"use client";

import React, { useEffect, useState } from "react";
import { PaginatedResponse } from "@/app/types";
import { API_BASE_URL } from "@/lib/config";

export interface Column<T> {
  key: keyof T;
  label: string;
}

interface PaginatedTableProps<T> {
  columns: readonly Column<T>[];
  endpoint: string;
  pageSize?: number;
}

export function PaginatedTable<T extends { id: number }>({
  columns,
  endpoint,
  pageSize = 20,
}: PaginatedTableProps<T>) {
  const [data, setData] = useState<T[]>([]);
  const [nextCursor, setNextCursor] = useState<string | undefined>(undefined);
  const [loading, setLoading] = useState(false);

  const fetchPage = async (cursor?: string) => {
    setLoading(true);
    try {
      const url = new URL(`${API_BASE_URL}${endpoint}`);
      url.searchParams.set("limit", pageSize.toString());
      if (cursor) url.searchParams.set("cursor", cursor);

      const res = await fetch(url.toString());
      const json: PaginatedResponse<T> = await res.json();

      setData(json.items);
      setNextCursor(json.next_cursor);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setData([]); // reset data when endpoint changes
    setNextCursor(undefined); // reset cursor when endpoint changes
    fetchPage(); // initial load
  }, [endpoint]);

  return (
    <div className="overflow-x-auto">
      <table className="table-auto w-full border border-gray-200">
        <thead>
          <tr>
            {columns.map((col) => (
              <th
                key={`${endpoint}-${col.key as string}`}
                className="border px-4 py-2 text-left bg-gray-100"
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={`${endpoint}-${row.id}`}>
              {columns.map((col) => (
                <td key={`${endpoint}-${row.id}-${col.key as string}`} className="border px-4 py-2">
                  {String(row[col.key] ?? "")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      {nextCursor && (
        <div className="mt-4 text-center">
          <button
            onClick={() => fetchPage(nextCursor)}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? "Loading..." : "Load More"}
          </button>
        </div>
      )}
    </div>
  );
}