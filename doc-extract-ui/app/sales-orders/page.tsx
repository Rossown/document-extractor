"use client";

import { PaginatedTable } from "@/components/PaginatedTable";
import { SalesOrderHeader, SalesOrderDetail } from "@/app/types";
    
import Link from "next/link";
import CustomerDetailPopup from "../customers/CustomerDetail";
import TerritoryDetailPopup from "../territories/TerritoryDetail";
import { Person } from "@/app/types";
import StoreDetailPopup from "../stores/StoreDetail";
import { API_BASE_URL } from "@/lib/config";
import { useState } from "react";

export default function SalesOrdersPage() {
  // ...existing code...
  const [detailStore, setDetailStore] = useState<any | null>(null);
  const salesOrderColumns = [
    {
      key: "id",
      label: "ID",
      render: (row: SalesOrderHeader) => (
        <Link
          href={`/sales-details/${row.id}`}
          className="text-blue-600 hover:underline"
          title={`View details for order ${row.id}`}
        >
          {row.id}
        </Link>
      ),
    },
    { key: "revision_number", label: "Revision Number" },
    { key: "order_date", label: "Order Date" },
    { key: "due_date", label: "Due Date" },
    { key: "ship_date", label: "Ship Date" },
    { key: "status", label: "Status" },
    { key: "online_order_flag", label: "Online Order Flag" },
    { key: "sales_order_number", label: "Sales Order Number" },
    { key: "purchase_order_number", label: "Purchase Order Number" },
    { key: "account_number", label: "Account Number" },
    {
      key: "customer_id",
      label: "Customer ID",
      render: (row: SalesOrderHeader) => row.customer_id ? (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => handleShowCustomer(row.customer_id)}
        >
          {row.customer_id}
        </button>
      ) : null,
    },
    {
      key: "sales_person_id",
      label: "Sales Person ID",
      render: (row: SalesOrderHeader) => row.sales_person_id ? (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => handleShowPerson(Number(row.sales_person_id))}
        >
          {row.sales_person_id}
        </button>
      ) : null,
    },
    {
      key: "territory_id",
      label: "Territory ID",
      render: (row: SalesOrderHeader) => row.territory_id ? (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => handleShowTerritory(row.territory_id)}
        >
          {row.territory_id}
        </button>
      ) : null,
    },
    {
      key: "bill_to_address_id",
      label: "Bill To",
      render: (row: SalesOrderHeader) => row.bill_to_address_id ? (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => handleShowPerson(row.bill_to_address_id)}
        >
          {row.bill_to_address_id}
        </button>
      ) : null,
    },
    {
      key: "ship_to_address_id",
      label: "Ship To",
      render: (row: SalesOrderHeader) => row.ship_to_address_id ? (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => handleShowPerson(row.ship_to_address_id)}
        >
          {row.ship_to_address_id}
        </button>
      ) : null,
    },
    { key: "credit_card_id", label: "Credit Card ID" },
    { key: "credit_card_approval_code", label: "Credit Card Approval Code" },
    { key: "currency_rate_id", label: "Currency Rate ID" },
    {
      key: "sub_total",
      label: "Sub Total",
      render: (row: SalesOrderHeader) => row.sub_total != null ? row.sub_total.toLocaleString("en-US", { style: "currency", currency: "USD" }) : ""
    },
    {
      key: "tax_amt",
      label: "Tax Amount",
      render: (row: SalesOrderHeader) => row.tax_amt != null ? row.tax_amt.toLocaleString("en-US", { style: "currency", currency: "USD" }) : ""
    },
    {
      key: "freight",
      label: "Freight",
      render: (row: SalesOrderHeader) => row.freight != null ? row.freight.toLocaleString("en-US", { style: "currency", currency: "USD" }) : ""
    },
    {
      key: "total_due",
      label: "Total Due",
      render: (row: SalesOrderHeader) => row.total_due != null ? row.total_due.toLocaleString("en-US", { style: "currency", currency: "USD" }) : ""
    },
  ] as const;
  const [detailCustomer, setDetailCustomer] = useState<any | null>(null);
  const [detailPerson, setDetailPerson] = useState<Person | null>(null);
  const [detailTerritory, setDetailTerritory] = useState<any | null>(null);

  const handleShowCustomer = async (id?: number) => {
    if (id == null || id === undefined) return;
    const res = await fetch(`${API_BASE_URL}/api/customers/${id}`);
    if (res.ok) setDetailCustomer(await res.json());
  };
  const handleShowPerson = async (id?: number) => {
    if (id == null || id === undefined) return;
    const res = await fetch(`${API_BASE_URL}/api/persons/${id}`);
    if (res.ok) setDetailPerson(await res.json());
  };
  const handleShowTerritory = async (id?: number) => {
    if (id == null || id === undefined) return;
    const res = await fetch(`${API_BASE_URL}/api/territories/${id}`);
    if (res.ok) setDetailTerritory(await res.json());
  };
  const handleShowStore = async (id?: number) => {
    if (id == null || id === undefined) return;
    const res = await fetch(`${API_BASE_URL}/api/stores/${id}`);
    if (res.ok) setDetailStore(await res.json());
  };

  const [searchId, setSearchId] = useState("");
  const [searchedOrder, setSearchedOrder] = useState<SalesOrderHeader | null>(null);
  const [searchError, setSearchError] = useState("");

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setSearchError("");
    setSearchedOrder(null);
    if (!searchId) return;
    try {
      const res = await fetch(`${API_BASE_URL}/api/sales-orders/${searchId}`);
      if (!res.ok) throw new Error("Sales order not found");
      const data = await res.json();
      setSearchedOrder(data);
    } catch {
      setSearchError("Sales order not found");
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Sales Orders</h1>
      <form onSubmit={handleSearch} className="mb-4 flex gap-2">
        <input
          type="text"
          placeholder="Search by sales order ID..."
          value={searchId}
          onChange={e => setSearchId(e.target.value)}
          className="border px-2 py-1 rounded w-64"
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-1 rounded">Search</button>
      </form>
      {searchError && <div className="text-red-600 mb-2">{searchError}</div>}
      {searchedOrder && (
        <div className="fixed inset-0 z-50 flex items-center justify-center" style={{ background: "rgba(0,0,0,0.15)" }}>
          <div className="rounded-lg shadow-lg p-6 min-w-[320px] max-w-[90vw] relative bg-gray-50 dark:bg-gray-200" style={{ color: "var(--color-foreground, #171717)" }}>
            <button
              onClick={() => setSearchedOrder(null)}
              className="absolute top-2 right-2 w-10 h-10 flex items-center justify-center rounded-full bg-red-500 text-white text-2xl font-extrabold shadow-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 z-10"
              aria-label="Close"
            >
              ×
            </button>
            <h2 className="text-xl font-bold mb-2">Sales Order #{searchedOrder.id}</h2>
            <div className="mb-2">Order Date: {searchedOrder.order_date}</div>
            <div className="mb-2">Status: {searchedOrder.status}</div>
            <div className="mb-2">Total Due: {searchedOrder.total_due != null ? searchedOrder.total_due.toLocaleString("en-US", { style: "currency", currency: "USD" }) : ""}</div>
            {/* Add more fields as needed */}
          </div>
        </div>
      )}
      <PaginatedTable columns={salesOrderColumns} endpoint="/api/sales-orders" />
      {detailCustomer && (
        <CustomerDetailPopup customer={detailCustomer} onClose={() => setDetailCustomer(null)} />
      )}
      {detailPerson && (
        <div className="fixed inset-0 z-50 flex items-center justify-center" style={{ background: "rgba(0,0,0,0.15)" }}>
          <div className="rounded-lg shadow-lg p-6 min-w-[320px] max-w-[90vw] relative bg-gray-50 dark:bg-gray-200" style={{ color: "var(--color-foreground, #171717)" }}>
            <button
              onClick={() => setDetailPerson(null)}
              className="absolute top-2 right-2 w-10 h-10 flex items-center justify-center rounded-full bg-red-500 text-white text-2xl font-extrabold shadow-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 z-10"
              aria-label="Close"
            >
              ×
            </button>
            <h2 className="text-xl font-bold mb-2">Person #{detailPerson.id}</h2>
            <div className="mb-2">Business Entity ID: {detailPerson.business_entity_id}</div>
            <div className="mb-2">Name: {detailPerson.first_name} {detailPerson.middle_name} {detailPerson.last_name}</div>
            <div className="mb-2">Address: {detailPerson.address_line1} {detailPerson.address_line2}, {detailPerson.city}, {detailPerson.state_province}, {detailPerson.postal_code}, {detailPerson.country_region}</div>
          </div>
        </div>
      )}
      {detailStore && (
        <StoreDetailPopup store={detailStore} onClose={() => setDetailStore(null)} />
      )}
      {detailTerritory && (
        <TerritoryDetailPopup territory={detailTerritory} onClose={() => setDetailTerritory(null)} />
      )}
      {/* TODO: Add Address popup if AddressDetailPopup exists */}
    </div>
  );
}
