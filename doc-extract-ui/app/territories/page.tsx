"use client";

import { PaginatedTable } from "@/components/PaginatedTable";
import { Territory } from "@/app/types";
import { useState, useRef } from "react";
import EditTerritoryModal from "@/components/EditTerritoryModal";
import { API_BASE_URL } from "@/lib/config";


export default function TerritoriesPage() {
  const [editTerritory, setEditTerritory] = useState<Territory | null>(null);
  const tableRef = useRef<{ reload: () => void }>(null);

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

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Territories</h1>
      <PaginatedTable
        ref={tableRef}
        columns={territoryColumns}
        endpoint="/api/territories"
      />
      {editTerritory && (
        <EditTerritoryModal
          territory={editTerritory}
          onClose={() => setEditTerritory(null)}
          onSave={handleSave}
        />
      )}
    </div>
  );
}