"use client";

import React, { useEffect, useState, useImperativeHandle, forwardRef } from "react";
import { PaginatedResponse } from "@/app/types";
import { API_BASE_URL } from "@/lib/config";

export interface Column<T> {
  key: string;
  label: string;
  render?: (row: T) => React.ReactNode;
}

interface PaginatedTableProps<T> {
  columns: readonly Column<T>[];
  endpoint: string;
  pageSize?: number;
  filterId?: string;
}

const PaginatedTableInner = <T extends { id: number }>(
  {
    columns,
    endpoint,
    pageSize = 20,
    filterId = "",
  }: PaginatedTableProps<T>,
  ref: React.Ref<{ reload: () => void }>
) => {
  const [data, setData] = useState<T[]>([]);
  const [nextCursor, setNextCursor] = useState<string | undefined>(undefined);
  const [prevCursors, setPrevCursors] = useState<(string | undefined)[]>([]); // history of cursors, include undefined for first page
  const [currentCursor, setCurrentCursor] = useState<string | undefined>(undefined);
  const [loading, setLoading] = useState(false);

  const fetchPage = async (cursor?: string, direction: 'next' | 'prev' = 'next') => {
    setLoading(true);
    try {
      const url = new URL(`${API_BASE_URL}${endpoint}`);
      url.searchParams.set("limit", pageSize.toString());
      if (cursor) url.searchParams.set("cursor", cursor);
      if (filterId && filterId.trim() !== "") {
        url.searchParams.set("id", filterId.trim());
      }

      const res = await fetch(url.toString());
      let json: any = null;
      try {
        json = await res.json();
      } catch {
        json = null;
      }

      if (!res.ok || !json) {
        setData([]);
        setNextCursor(undefined);
      } else if (json && Array.isArray(json.items)) {
        setData(json.items);
        setNextCursor(json.next_cursor);
      } else if (Array.isArray(json)) {
        setData(json);
        setNextCursor(undefined);
      } else {
        setData([]);
        setNextCursor(undefined);
      }

      if (direction === 'next') {
        setPrevCursors((prev) => [...prev, currentCursor]);
        setCurrentCursor(cursor);
      } else if (direction === 'prev') {
        setCurrentCursor(cursor);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setData([]); // reset data when endpoint or filter changes
    setNextCursor(undefined);
    setPrevCursors([]); // start with empty stack
    setCurrentCursor(undefined); // first page cursor is undefined
    fetchPage(undefined); // initial load
  }, [endpoint, filterId]);

  useImperativeHandle(ref, () => ({
    reload: () => fetchPage(undefined),
  }));

  const handleNext = () => {
    if (nextCursor) fetchPage(nextCursor, 'next');
  };

  const handlePrev = () => {
    if (prevCursors.length > 0) {
      const prev = [...prevCursors];
      const prevCursor = prev.pop();
      setPrevCursors(prev);
      fetchPage(prevCursor, 'prev');
    }
  };

  return (
    <div className="w-full overflow-x-auto max-w-full">
      <div className="min-w-[700px] max-w-[1200px] mx-auto">
        <table className="table-auto w-full border border-gray-200 text-sm">
          <thead className="sticky top-0 z-10">
            <tr>
              {columns.map((col) => (
                <th
                  key={`${endpoint}-${col.key as string}`}
                  className="border px-4 py-2 text-left bg-gray-100 whitespace-nowrap"
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
                  <td key={`${endpoint}-${row.id}-${col.key}`} className="border px-4 py-2 whitespace-nowrap">
                    {col.render ? col.render(row) : (row as any)[col.key] ?? ""}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-4 text-center flex justify-center gap-4">
        <button
          onClick={handlePrev}
          className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400 disabled:opacity-50"
          disabled={loading || prevCursors.length === 0}
        >
          Previous
        </button>
        <button
          onClick={handleNext}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          disabled={loading || !nextCursor}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export const PaginatedTable = forwardRef(PaginatedTableInner);