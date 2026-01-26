"use client";

import { PaginatedTable } from "@/components/PaginatedTable";
import { Customer } from "@/app/types";
import { useState, useRef } from "react";
import TerritoryDetailPopup from "../territories/TerritoryDetail";
import PersonDetailPopup from "../people/PersonDetail";
import StoreDetailPopup from "../stores/StoreDetail";
import CustomerDetailPopup from "./CustomerDetail";
import EditCustomerModal from "@/components/EditCustomerModal";
import { API_BASE_URL } from "@/lib/config";
export default function CustomersPage() {
  const [editCustomer, setEditCustomer] = useState<Customer | null>(null);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const tableRef = useRef<{ reload: () => void }>(null);
  const [searchId, setSearchId] = useState("");
  const [searchedCustomer, setSearchedCustomer] = useState<Customer | null>(null);
  const [searchError, setSearchError] = useState("");

  const [detailCustomer, setDetailCustomer] = useState<Customer | null>(null);
  const [detailTerritory, setDetailTerritory] = useState<any | null>(null);
  const [detailPerson, setDetailPerson] = useState<any | null>(null);
  const [detailStore, setDetailStore] = useState<any | null>(null);

  const customerColumns = [
    {
      key: "id",
      label: "ID",
      render: (row: Customer) => (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => setDetailCustomer(row)}
        >
          {row.id}
        </button>
      ),
    },
    { key: "account_number", label: "Account Number" },
    {
      key: "territory_id",
      label: "Territory ID",
      render: (row: Customer) => row.territory_id ? (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={async () => {
            const res = await fetch(`${API_BASE_URL}/api/territories/${row.territory_id}`);
            if (res.ok) setDetailTerritory(await res.json());
          }}
        >
          {row.territory_id}
        </button>
      ) : null,
    },
    {
      key: "person_id",
      label: "Person ID",
      render: (row: Customer) => row.person_id ? (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={async () => {
            const res = await fetch(`${API_BASE_URL}/api/persons/${row.person_id}`);
            if (res.ok) setDetailPerson(await res.json());
          }}
        >
          {row.person_id}
        </button>
      ) : null,
    },
    {
      key: "store_id",
      label: "Store Business ID",
      render: (row: Customer) => row.store_id ? (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={async () => {
            const res = await fetch(`${API_BASE_URL}/api/persons/${row.store_id}`);
            if (res.ok) setDetailStore(await res.json());
          }}
        >
          {row.store_id}
        </button>
      ) : null,
    },
    {
      key: "edit",
      label: "",
      render: (row: Customer) => (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => setEditCustomer(row)}
        >
          Edit
        </button>
      ),
    },
  ] as const;

  // Handler for saving edited customer (should call API in real app)
  const handleSave = async (updated: Customer) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/customers/${updated.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated),
      });
      if (!res.ok) throw new Error("Failed to update customer");
      setEditCustomer(null);
      // Reload the customers table only
      tableRef.current?.reload();
    } catch (e) {
      alert("Failed to update customer");
      setEditCustomer(null);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setSearchError("");
    setSearchedCustomer(null);
    if (!searchId) return;
    try {
      const res = await fetch(`${API_BASE_URL}/api/customers/${searchId}`);
      if (!res.ok) throw new Error("Customer not found");
      const data = await res.json();
      setSearchedCustomer(data);
    } catch {
      setSearchError("Customer not found");
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Customers</h1>
      <form onSubmit={handleSearch} className="mb-4 flex gap-2">
        <input
          type="text"
          placeholder="Search by customer ID..."
          value={searchId}
          onChange={e => setSearchId(e.target.value)}
          className="border px-2 py-1 rounded w-64"
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-1 rounded">Search</button>
      </form>
      {searchError && <div className="text-red-600 mb-2">{searchError}</div>}
      {searchedCustomer && (
        <CustomerDetailPopup customer={searchedCustomer} onClose={() => setSearchedCustomer(null)} />
      )}
      {detailCustomer && (
        <CustomerDetailPopup customer={detailCustomer} onClose={() => setDetailCustomer(null)} />
      )}
      {detailTerritory && (
        <TerritoryDetailPopup territory={detailTerritory} onClose={() => setDetailTerritory(null)} />
      )}
      {detailPerson && (
        <PersonDetailPopup person={detailPerson} onClose={() => setDetailPerson(null)} />
      )}
      {detailStore && (
        <StoreDetailPopup store={detailStore} onClose={() => setDetailStore(null)} />
      )}
      <PaginatedTable
        ref={tableRef}
        columns={customerColumns}
        endpoint="/api/customers"
      />
      {editCustomer && (
        <EditCustomerModal
          customer={editCustomer}
          onClose={() => setEditCustomer(null)}
          onSave={handleSave}
        />
      )}
    </div>
  );
}