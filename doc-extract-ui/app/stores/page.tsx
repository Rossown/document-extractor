import { PaginatedTable } from "@/components/PaginatedTable";
import { Store } from "@/app/types";

const storeColumns = [
  { key: "id", label: "ID" },
  { key: "name", label: "Name" },
  { key: "city", label: "City" },
  { key: "state_province", label: "State" },
  { key: "country_region", label: "Country" },
] as const;

export default function StoresPage() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Stores</h1>
      <PaginatedTable<Store> columns={storeColumns} endpoint="/api/stores" />
    </div>
  );
}
