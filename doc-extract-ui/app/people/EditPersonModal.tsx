"use client";

import React, { useState } from "react";
import { Person } from "@/app/types";

interface EditPersonModalProps {
  person: Person;
  onClose: () => void;
  onSave: (updated: Person) => void;
}

export default function EditPersonModal({ person, onClose, onSave }: EditPersonModalProps) {
  const [form, setForm] = useState<Person>({ ...person });
  const [saving, setSaving] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    await onSave(form);
    setSaving(false);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center" style={{ background: "rgba(0,0,0,0.15)" }}>
      <form
        onSubmit={handleSubmit}
        className="bg-white dark:bg-gray-200 rounded-lg shadow-lg p-6 min-w-[320px] max-w-[90vw] relative"
        style={{ color: "var(--color-foreground, #171717)" }}
      >
        <button
          type="button"
          onClick={onClose}
          className="absolute top-2 right-2 w-10 h-10 flex items-center justify-center rounded-full bg-red-500 text-white text-2xl font-extrabold shadow-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 z-10"
          aria-label="Close"
        >
          ×
        </button>
        <h2 className="text-xl font-bold mb-4">Edit Person #{person.id}</h2>
        <div className="mb-2">
          <label className="block mb-1">First Name</label>
          <input name="first_name" value={form.first_name || ""} onChange={handleChange} className="border px-2 py-1 rounded w-full" />
        </div>
        <div className="mb-2">
          <label className="block mb-1">Middle Name</label>
          <input name="middle_name" value={form.middle_name || ""} onChange={handleChange} className="border px-2 py-1 rounded w-full" />
        </div>
        <div className="mb-2">
          <label className="block mb-1">Last Name</label>
          <input name="last_name" value={form.last_name || ""} onChange={handleChange} className="border px-2 py-1 rounded w-full" />
        </div>
        <div className="mb-2">
          <label className="block mb-1">Address Line 1</label>
          <input name="address_line1" value={form.address_line1 || ""} onChange={handleChange} className="border px-2 py-1 rounded w-full" />
        </div>
        <div className="mb-2">
          <label className="block mb-1">Address Line 2</label>
          <input name="address_line2" value={form.address_line2 || ""} onChange={handleChange} className="border px-2 py-1 rounded w-full" />
        </div>
        <div className="mb-2">
          <label className="block mb-1">City</label>
          <input name="city" value={form.city || ""} onChange={handleChange} className="border px-2 py-1 rounded w-full" />
        </div>
        <div className="mb-2">
          <label className="block mb-1">State</label>
          <input name="state_province" value={form.state_province || ""} onChange={handleChange} className="border px-2 py-1 rounded w-full" />
        </div>
        <div className="mb-2">
          <label className="block mb-1">Postal Code</label>
          <input name="postal_code" value={form.postal_code || ""} onChange={handleChange} className="border px-2 py-1 rounded w-full" />
        </div>
        <div className="mb-2">
          <label className="block mb-1">Country</label>
          <input name="country_region" value={form.country_region || ""} onChange={handleChange} className="border px-2 py-1 rounded w-full" />
        </div>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded mt-4" disabled={saving}>
          {saving ? "Saving..." : "Save"}
        </button>
      </form>
    </div>
  );
}
