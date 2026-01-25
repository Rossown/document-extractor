import { PaginatedTable } from "@/components/PaginatedTable";
import { Territory } from "@/app/types";

const territoryColumns = [
  { key: "id", label: "ID" },
  { key: "name", label: "Name" },
  { key: "country_region_code", label: "Country" },
  { key: "group", label: "Group" },
] as const;

export default function TerritoriesPage() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Territories</h1>
      <PaginatedTable<Territory> columns={territoryColumns} endpoint="/api/territories" />
    </div>
  );
}