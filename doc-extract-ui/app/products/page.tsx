"use client";
import { PaginatedTable } from "@/components/PaginatedTable";
import { Product } from "@/app/types";
import { useState, useRef, useEffect } from "react";
import EditProductModal from "@/components/EditProductModal";
import { API_BASE_URL } from "@/lib/config";
import ProductDetailPopup from "./[productId]/ProductDetail";

export default function ProductsPage() {
  const [editProduct, setEditProduct] = useState<Product | null>(null);
  const [detailProduct, setDetailProduct] = useState<Product | null>(null);
  const [detailProductId, setDetailProductId] = useState<number | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const tableRef = useRef<{ reload: () => void }>(null);
  const [search, setSearch] = useState("");
  const [searchInput, setSearchInput] = useState("");

  const [searchId, setSearchId] = useState("");
  const [searchedProduct, setSearchedProduct] = useState<Product | null>(null);
  const [searchError, setSearchError] = useState("");

  // Fetch product details when detailProductId changes
  useEffect(() => {
    if (detailProductId == null) return;
    setLoadingDetail(true);
    fetch(`${API_BASE_URL}/api/products/${detailProductId}`)
      .then((res) => res.json())
      .then((data) => setDetailProduct(data))
      .finally(() => setLoadingDetail(false));
  }, [detailProductId]);

  const productColumns = [
    {
      key: "id",
      label: "ID",
      render: (row: Product) => (
        <button
          className="text-blue-600 hover:underline px-2 py-1"
          onClick={() => setDetailProductId(row.id)}
        >
          {row.id}
        </button>
      ),
    },
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

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setSearchError("");
    setSearchedProduct(null);
    if (!searchId) return;
    try {
      const res = await fetch(`${API_BASE_URL}/api/products/${searchId}`);
      if (!res.ok) throw new Error("Product not found");
      const data = await res.json();
      setSearchedProduct(data);
    } catch {
      setSearchError("Product not found");
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Products</h1>
      <form onSubmit={handleSearch} className="mb-4 flex gap-2">
        <input
          type="text"
          placeholder="Search by product ID..."
          value={searchId}
          onChange={e => setSearchId(e.target.value)}
          className="border px-2 py-1 rounded w-64"
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-1 rounded">Search</button>
      </form>
      {searchError && <div className="text-red-600 mb-2">{searchError}</div>}
      {searchedProduct && (
        <ProductDetailPopup
          product={searchedProduct}
          onClose={() => setSearchedProduct(null)}
        />
      )}
      <PaginatedTable<Product>
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
      {detailProductId && (
        <ProductDetailPopup
          product={detailProduct}
          onClose={() => {
            setDetailProductId(null);
            setDetailProduct(null);
          }}
        />
      )}
      {loadingDetail && detailProductId && !detailProduct && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-20">
          <div className="bg-white p-6 rounded shadow">Loading product details...</div>
        </div>
      )}
    </div>
  );
}