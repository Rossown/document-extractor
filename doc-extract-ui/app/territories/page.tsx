"use client";

import { PaginatedTable } from "@/components/PaginatedTable";
import { Territory } from "@/app/types";
import { useState, useRef } from "react";
import EditTerritoryModal from "@/components/EditTerritoryModal";
import { API_BASE_URL } from "@/lib/config";
import TerritoryDetailPopup from "./TerritoryDetail";

export default function TerritoriesPage() {
  const [editTerritory, setEditTerritory] = useState<Territory | null>(null);
  const tableRef = useRef<{ reload: () => void }>(null);
  const [searchId, setSearchId] = useState("");
  const [searchedTerritory, setSearchedTerritory] = useState<Territory | null>(null);
  const [searchError, setSearchError] = useState("");

  const territoryColumns = [
    { key: "id", label: "ID" },
    { key: "name", label: "Name" },
    { key: "country_region_code", label: "Country" },
    { key: "group", label: "Group" },
    {
      key: "edit",
      label: "",
      render: (row: Territory) => (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => setEditTerritory(row)}
        >
          Edit
        </button>
      ),
    },
  ] as const;

  const handleSave = async (updated: Territory) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/territories/${updated.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated),
      });
      if (!res.ok) throw new Error("Failed to update territory");
      setEditTerritory(null);
      tableRef.current?.reload();
    } catch (e) {
      alert("Failed to update territory");
      setEditTerritory(null);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setSearchError("");
    setSearchedTerritory(null);
    if (!searchId) return;
    try {
      const res = await fetch(`${API_BASE_URL}/api/territories/${searchId}`);
      if (!res.ok) throw new Error("Territory not found");
      const data = await res.json();
      setSearchedTerritory(data);
    } catch {
      setSearchError("Territory not found");
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Territories</h1>
      <form onSubmit={handleSearch} className="mb-4 flex gap-2">
        <input
          type="text"
          placeholder="Search by territory ID..."
          value={searchId}
          onChange={e => setSearchId(e.target.value)}
          className="border px-2 py-1 rounded w-64"
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-1 rounded">Search</button>
      </form>
      {searchError && <div className="text-red-600 mb-2">{searchError}</div>}
      {searchedTerritory && (
        <TerritoryDetailPopup territory={searchedTerritory} onClose={() => setSearchedTerritory(null)} />
      )}
      {editTerritory && (
        <EditTerritoryModal
          territory={editTerritory}
          onClose={() => setEditTerritory(null)}
          onSave={handleSave}
        />
      )}
      <PaginatedTable
        ref={tableRef}
        columns={territoryColumns}
        endpoint="/api/territories?cursor=business_entity_id"
      />
    </div>
  );
}