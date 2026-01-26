"use client";

import { PaginatedTable } from "@/components/PaginatedTable";
import { Customer } from "@/app/types";
import { useState, useRef } from "react";
import EditCustomerModal from "@/components/EditCustomerModal";
import { API_BASE_URL } from "@/lib/config";
import CustomerDetailPopup from "./CustomerDetail";

export default function CustomersPage() {
  const [editCustomer, setEditCustomer] = useState<Customer | null>(null);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const tableRef = useRef<{ reload: () => void }>(null);
  const [searchId, setSearchId] = useState("");
  const [searchedCustomer, setSearchedCustomer] = useState<Customer | null>(null);
  const [searchError, setSearchError] = useState("");

  const customerColumns = [
    { key: "id", label: "ID" },
    { key: "account_number", label: "Account Number" },
    { key: "territory_id", label: "Territory ID" },
    { key: "person_id", label: "Person ID" },
    { key: "store_id", label: "Store ID" },
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