"use client";

import { PaginatedTable } from "@/components/PaginatedTable";
import { Person } from "@/app/types";
import { useState, useRef } from "react";
import { API_BASE_URL } from "@/lib/config";
import EditPersonModal from "./EditPersonModal";

export default function PeoplePage() {
  const tableRef = useRef<{ reload: () => void }>(null);
  const [detailPerson, setDetailPerson] = useState<Person | null>(null);
  const [searchId, setSearchId] = useState("");
  const [searchedPerson, setSearchedPerson] = useState<Person | null>(null);
  const [searchError, setSearchError] = useState("");

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setSearchError("");
    setSearchedPerson(null);
    if (!searchId) return;
    try {
      const res = await fetch(`${API_BASE_URL}/api/persons/${searchId}`);
      if (!res.ok) throw new Error("Person not found");
      const data = await res.json();
      setSearchedPerson(data);
    } catch {
      setSearchError("Person not found");
    }
  };

  const [editPerson, setEditPerson] = useState<Person | null>(null);

  const handleSave = async (updated: Person) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/persons/${updated.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated),
      });
      if (!res.ok) throw new Error("Failed to update person");
      setEditPerson(null);
      tableRef.current?.reload();
    } catch (e) {
      alert("Failed to update person");
      setEditPerson(null);
    }
  };

  const personColumns = [
    {
      key: "business_entity_id",
      label: "Business Entity ID",
      render: (row: Person) => (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => setDetailPerson(row)}
        >
          {row.business_entity_id}
        </button>
      ),
    },
    { key: "id", label: "ID" },
    { key: "first_name", label: "First Name" },
    { key: "middle_name", label: "Middle Name" },
    { key: "last_name", label: "Last Name" },
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
      render: (row: Person) => (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => setEditPerson(row)}
        >
          Edit
        </button>
      ),
    },
  ] as const;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">People</h1>
      <form onSubmit={handleSearch} className="mb-4 flex gap-2">
        <input
          type="text"
          placeholder="Search by person ID..."
          value={searchId}
          onChange={e => setSearchId(e.target.value)}
          className="border px-2 py-1 rounded w-64"
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-1 rounded">Search</button>
      </form>
      {searchError && <div className="text-red-600 mb-2">{searchError}</div>}
      {searchedPerson && (
        <div className="fixed inset-0 z-50 flex items-center justify-center" style={{ background: "rgba(0,0,0,0.15)" }}>
          <div className="rounded-lg shadow-lg p-6 min-w-[320px] max-w-[90vw] relative bg-gray-50 dark:bg-gray-200" style={{ color: "var(--color-foreground, #171717)" }}>
            <button
              onClick={() => setSearchedPerson(null)}
              className="absolute top-2 right-2 w-10 h-10 flex items-center justify-center rounded-full bg-red-500 text-white text-2xl font-extrabold shadow-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 z-10"
              aria-label="Close"
            >
              ×
            </button>
            <h2 className="text-xl font-bold mb-2">Person #{searchedPerson.id}</h2>
            <div className="mb-2">Business Entity ID: {searchedPerson.business_entity_id}</div>
            <div className="mb-2">Name: {searchedPerson.first_name} {searchedPerson.middle_name} {searchedPerson.last_name}</div>
            <div className="mb-2">Address: {searchedPerson.address_line1} {searchedPerson.address_line2}, {searchedPerson.city}, {searchedPerson.state_province}, {searchedPerson.postal_code}, {searchedPerson.country_region}</div>
          </div>
        </div>
      )}
      {editPerson && (
        <EditPersonModal
          person={editPerson}
          onClose={() => setEditPerson(null)}
          onSave={handleSave}
        />
      )}
      <PaginatedTable
        ref={tableRef}
        columns={personColumns}
        endpoint="/api/persons?cursor=business_entity_id"
      />
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
    </div>
  );
}
