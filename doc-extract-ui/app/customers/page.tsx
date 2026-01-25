"use client";

import { PaginatedTable } from "@/components/PaginatedTable";
import { Customer } from "@/app/types";

const customerColumns = [
  { key: "id", label: "ID" },
  { key: "account_number", label: "Account Number" },
  { key: "territory_id", label: "Territory ID" },
  { key: "person_id", label: "Person ID" },
  { key: "store_id", label: "Store ID" },
] as const;

export default function CustomersPage() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Customers</h1>
      <PaginatedTable<Customer> columns={customerColumns} endpoint="/api/customers" />
    </div>
  );
}