import { useState } from "react";
import { Customer } from "@/app/types";

interface EditCustomerModalProps {
  customer: Customer;
  onClose: () => void;
  onSave: (updated: Customer) => void;
}

export default function EditCustomerModal({ customer, onClose, onSave }: EditCustomerModalProps) {
  const [form, setForm] = useState<Customer>({ ...customer });
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center" style={{ background: 'rgba(0,0,0,0.15)' }}>
      <div className="bg-white rounded-lg shadow-lg p-6 min-w-[320px] max-w-[90vw] relative">
        <button onClick={onClose} className="absolute top-2 right-2 text-xl font-bold">×</button>
        <h2 className="text-xl font-bold mb-4">Edit Customer</h2>
        <form
          onSubmit={e => {
            e.preventDefault();
            onSave(form);
          }}
        >
          <div className="mb-2">
            <label className="block text-sm font-medium">Account Number</label>
            <input readOnly name="account_number" value={form.account_number || ""} onChange={handleChange} className="border rounded px-2 py-1 w-full" />
          </div>
          <div className="mb-2">
            <label className="block text-sm font-medium">Territory ID</label>
            <input name="territory_id" value={form.territory_id || ""} onChange={handleChange} className="border rounded px-2 py-1 w-full" />
          </div>
          <div className="mb-2">
            <label className="block text-sm font-medium">Person ID</label>
            <input name="person_id" value={form.person_id || ""} onChange={handleChange} className="border rounded px-2 py-1 w-full" />
          </div>
          <div className="mb-2">
            <label className="block text-sm font-medium">Store ID</label>
            <input name="store_id" value={form.store_id || ""} onChange={handleChange} className="border rounded px-2 py-1 w-full" />
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
