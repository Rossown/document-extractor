"use client";
import { PaginatedTable } from "@/components/PaginatedTable";
import { Product, ProductCategory, ProductSubCategory } from "@/app/types";

const productColumns = [
  { key: "id", label: "ID" },
  { key: "product_name", label: "Name" },
  { key: "product_number", label: "Product Number" },
  { key: "make_flag", label: "Make Flag" },
  { key: "finished_goods_flag", label: "Finished Goods Flag" },
  { key: "color", label: "Color" },
  { key: "standard_cost", label: "Standard Cost" },
  { key: "list_price", label: "Price" },
  { key: "size", label: "Size" },
  { key: "product_line", label: "Product Line" },
  { key: "class_field", label: "Class" },
  { key: "style", label: "Style" },
  { key: "product_subcategory_id", label: "Sub Category" },
  { key: "product_model_id", label: "Product Model" },
] as const;

export default function ProductsPage() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Products</h1>
      <PaginatedTable<Product> columns={productColumns} endpoint="/api/products?cursor=business_entity_id" />
    </div>
  );
}