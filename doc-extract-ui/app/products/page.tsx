"use client";
import { PaginatedTable } from "@/components/PaginatedTable";
import { Product, ProductCategory, ProductSubCategory } from "@/app/types";
import { useState, useRef } from "react";
import EditProductModal from "@/components/EditProductModal";
import { API_BASE_URL } from "@/lib/config";


export default function ProductsPage() {
  const [editProduct, setEditProduct] = useState<Product | null>(null);
  const tableRef = useRef<{ reload: () => void }>(null);

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
    {
      key: "edit",
      label: "",
      render: (row: Product) => (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => setEditProduct(row)}
        >
          Edit
        </button>
      ),
    },
  ] as const;

  const handleSave = async (updated: Product) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/products/${updated.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated),
      });
      if (!res.ok) throw new Error("Failed to update product");
      setEditProduct(null);
      tableRef.current?.reload();
    } catch (e) {
      alert("Failed to update product");
      setEditProduct(null);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Products</h1>
      <PaginatedTable
        ref={tableRef}
        columns={productColumns}
        endpoint="/api/products?cursor=business_entity_id"
      />
      {editProduct && (
        <EditProductModal
          product={editProduct}
          onClose={() => setEditProduct(null)}
          onSave={handleSave}
        />
      )}
    </div>
  );
}