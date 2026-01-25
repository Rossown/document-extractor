import { PaginatedTable } from "@/components/PaginatedTable";
import { Store } from "@/app/types";

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
] as const;

export default function StoresPage() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Stores</h1>
      <PaginatedTable<Store> columns={storeColumns} endpoint="/api/stores?cursor=business_entity_id" />
    </div>
  );
}
