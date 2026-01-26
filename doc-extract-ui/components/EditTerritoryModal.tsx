import { useState } from "react";
import { Territory } from "@/app/types";

interface EditTerritoryModalProps {
  territory: Territory;
  onClose: () => void;
  onSave: (updated: Territory) => void;
}

export default function EditTerritoryModal({ territory, onClose, onSave }: EditTerritoryModalProps) {
  const [form, setForm] = useState<Territory>({ ...territory });
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center" style={{ background: 'rgba(0,0,0,0.15)' }}>
      <div className="bg-white rounded-lg shadow-lg p-6 min-w-[320px] max-w-[90vw] relative">
        <button onClick={onClose} className="absolute top-2 right-2 text-xl font-bold">×</button>
        <h2 className="text-xl font-bold mb-4">Edit Territory</h2>
        <form
          onSubmit={e => {
            e.preventDefault();
            onSave(form);
          }}
        >
          <div className="mb-2">
            <label className="block text-sm font-medium">Name</label>
            <input name="name" value={form.name || ""} onChange={handleChange} className="border rounded px-2 py-1 w-full" />
          </div>
          <div className="mb-2">
            <label className="block text-sm font-medium">Country</label>
            <input name="country_region_code" value={form.country_region_code || ""} onChange={handleChange} className="border rounded px-2 py-1 w-full" />
          </div>
          <div className="mb-2">
            <label className="block text-sm font-medium">Group</label>
            <input name="group" value={form.group || ""} onChange={handleChange} className="border rounded px-2 py-1 w-full" />
          </div>
          <div className="flex gap-2 mt-4">
            <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save</button>
            <button type="button" onClick={onClose} className="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}
