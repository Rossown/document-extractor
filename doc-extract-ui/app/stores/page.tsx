"use client";

import { PaginatedTable } from "@/components/PaginatedTable";
import { Store } from "@/app/types";
import { useState, useRef } from "react";
import EditStoreModal from "@/components/EditStoreModal";
import { API_BASE_URL } from "@/lib/config";


export default function StoresPage() {
  const [editStore, setEditStore] = useState<Store | null>(null);
  const tableRef = useRef<{ reload: () => void }>(null);

  const storeColumns = [
    { key: "business_entity_id", label: "Business Entity ID" },
    { key: "id", label: "ID" },
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

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Stores</h1>
      <PaginatedTable
        ref={tableRef}
        columns={storeColumns}
        endpoint="/api/stores?cursor=business_entity_id"
      />
      {editStore && (
        <EditStoreModal
          store={editStore}
          onClose={() => setEditStore(null)}
          onSave={handleSave}
        />
      )}
    </div>
  );
}
