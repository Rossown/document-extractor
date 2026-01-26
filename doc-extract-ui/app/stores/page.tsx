"use client";

import { PaginatedTable } from "@/components/PaginatedTable";
import { Store } from "@/app/types";
import { useState, useRef } from "react";
import EditStoreModal from "@/components/EditStoreModal";
import { API_BASE_URL } from "@/lib/config";
import StoreDetailPopup from "./StoreDetail";

export default function StoresPage() {
  const [editStore, setEditStore] = useState<Store | null>(null);
  const tableRef = useRef<{ reload: () => void }>(null);
  const [searchId, setSearchId] = useState("");
  const [searchedStore, setSearchedStore] = useState<Store | null>(null);
  const [searchError, setSearchError] = useState("");

  const [detailStore, setDetailStore] = useState<Store | null>(null);

  const storeColumns = [
    {
      key: "business_entity_id",
      label: "Business Entity ID",
      render: (row: Store) => (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => setDetailStore(row)}
        >
          {row.business_entity_id}
        </button>
      ),
    },
    { key: "id", label: "ID" }, // Plain, not a link
    { key: "name", label: "Name" },
    { key: "address_type", label: "Address Type" },
    { key: "address_line1", label: "Address Line 1" },
    { key: "address_line2", label: "Address Line 2" },
    { key: "city", label: "City" },
    { key: "state_province", label: "State" },
    { key: "postal_code", label: "Postal Code" },
    { key: "country_region", label: "Country" },
    {
      key: "edit",
      label: "",
      render: (row: Store) => (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => setEditStore(row)}
        >
          Edit
        </button>
      ),
    },
  ] as const;

  const handleSave = async (updated: Store) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/stores/${updated.business_entity_id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated),
      });
      if (!res.ok) throw new Error("Failed to update store");
      setEditStore(null);
      tableRef.current?.reload();
    } catch (e) {
      alert("Failed to update store");
      setEditStore(null);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setSearchError("");
    setSearchedStore(null);
    if (!searchId) return;
    try {
      const res = await fetch(`${API_BASE_URL}/api/stores/${searchId}`);
      if (!res.ok) throw new Error("Store not found");
      const data = await res.json();
      setSearchedStore(data);
    } catch {
      setSearchError("Store not found");
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Stores</h1>
      <form onSubmit={handleSearch} className="mb-4 flex gap-2">
        <input
          type="text"
          placeholder="Search by store ID..."
          value={searchId}
          onChange={e => setSearchId(e.target.value)}
          className="border px-2 py-1 rounded w-64"
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-1 rounded">Search</button>
      </form>
      {searchError && <div className="text-red-600 mb-2">{searchError}</div>}
      {searchedStore && (
        <StoreDetailPopup store={searchedStore} onClose={() => setSearchedStore(null)} />
      )}
      {detailStore && (
        <StoreDetailPopup store={detailStore} onClose={() => setDetailStore(null)} />
      )}
      {editStore && (
        <EditStoreModal
          store={editStore}
          onClose={() => setEditStore(null)}
          onSave={handleSave}
        />
      )}
      <PaginatedTable
        ref={tableRef}
        columns={storeColumns}
        endpoint="/api/stores?cursor=business_entity_id"
      />
    </div>
  );
}
