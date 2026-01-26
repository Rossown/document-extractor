// page.tsx
"use client"
import { SalesOrderHeader, SalesOrderDetail } from "@/app/types";
import SalesOrderDetailsTable from "./SalesOrderDetailsTable";
import { use, useState } from "react";
import { API_BASE_URL } from "@/lib/config";
interface PageProps {
  params: { orderId: string };
}

import Link from "next/link";


export default function SalesOrdersDetailsPage({ params }: PageProps) {
  const { orderId } = use(params);
  const [detailId, setDetailId] = useState("");
  const [searchedDetails, setSearchedDetails] = useState<SalesOrderDetail | null>(null);
  const [searchError, setSearchError] = useState("");

  if (!orderId) return <div>Order ID is missing</div>; // debug guard

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setSearchError("");
    setSearchedDetails(null);
    if (!detailId) return;
    try {
      const res = await fetch(`${API_BASE_URL}/api/sales-orders/${orderId}/details/${detailId}`);
      if (!res.ok) throw new Error("Sales order detail not found");
      const data = await res.json();
      setSearchedDetails(data);
    } catch {
      setSearchError("Sales order detail not found");
    }
  };

  return (
    <div className="p-4">
      <div className="mb-4">
        <Link href="/sales-orders" className="inline-block px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">
          ← Back to Sales Orders
        </Link>
      </div>
      <h1 className="text-2xl font-bold mb-4">
        Sales Order {orderId} Details
      </h1>
      <form onSubmit={handleSearch} className="mb-4 flex gap-2">
        <input
          type="text"
          placeholder="Search by sales order detail ID..."
          value={detailId}
          onChange={e => setDetailId(e.target.value)}
          className="border px-2 py-1 rounded w-64"
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-1 rounded">Search</button>
      </form>
      {searchError && <div className="text-red-600 mb-2">{searchError}</div>}
      {searchedDetails && (
        <div className="fixed inset-0 z-50 flex items-center justify-center" style={{ background: "rgba(0,0,0,0.15)" }}>
          <div className="rounded-lg shadow-lg p-6 min-w-[320px] max-w-[90vw] relative bg-gray-50 dark:bg-gray-200" style={{ color: "var(--color-foreground, #171717)" }}>
            <button
              onClick={() => setSearchedDetails(null)}
              className="absolute top-2 right-2 w-10 h-10 flex items-center justify-center rounded-full bg-red-500 text-white text-2xl font-extrabold shadow-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 z-10"
              aria-label="Close"
            >
              ×
            </button>
            <h2 className="text-xl font-bold mb-2">Sales Order Detail #{searchedDetails.id}</h2>
            <div className="mb-2">Product ID: {searchedDetails.product_id}</div>
            <div className="mb-2">Order Quantity: {searchedDetails.order_qty}</div>
            <div className="mb-2">Unit Price: {searchedDetails.unit_price}</div>
            <div className="mb-2">Line Total: {searchedDetails.line_total}</div>
            {/* Add more fields as needed */}
          </div>
        </div>
      )}
      <SalesOrderDetailsTable orderId={orderId} />
    </div>
  );
}
