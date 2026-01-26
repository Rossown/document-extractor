"use client";

import { PaginatedTable } from "@/components/PaginatedTable";
import { SalesOrderDetail, Product } from "@/app/types";
import { useState } from "react";
import ProductDetailPopup from "../../products/[productId]/ProductDetail";
import { API_BASE_URL } from "@/lib/config";


interface Props {
  orderId: string;
}

export default function SalesOrderDetailsTable({ orderId }: Props) {
  const [showProductPopup, setShowProductPopup] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [loadingProduct, setLoadingProduct] = useState(false);

  const handleProductClick = async (productId: number) => {
    setLoadingProduct(true);
    setShowProductPopup(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/products/${productId}`);
      const data = await res.json();
      setSelectedProduct(data);
    } catch (e) {
      setSelectedProduct(null);
    } finally {
      setLoadingProduct(false);
    }
  };


  const columns = [
    { key: "id", label: "ID" },
    { key: "sales_order_id", label: "Sales Order ID" },
    { key: "carrier_tracking_number", label: "Carrier Tracking Number" },
    { key: "order_qty", label: "Order Quantity" },
    {
      key: "product_id",
      label: "Product ID",
      render: (row: SalesOrderDetail) => (
        <button
          className="text-blue-600 hover:underline cursor-pointer bg-transparent border-none p-0"
          title={`View details for product ${row.product_id}`}
          onClick={() => handleProductClick(row.product_id)}
        >
          {row.product_id}
        </button>
      ),
    },
    { key: "special_offer_id", label: "Special Offer ID" },
    { key: "unit_price", label: "Unit Price" },
    { key: "unit_price_discount", label: "Unit Price Discount" },
    { key: "line_total", label: "Line Total" },
  ] as const;

  return (
    <>
      <PaginatedTable
        columns={columns}
        endpoint={`/api/sales-orders/${orderId}/details`}
        pageSize={20}
      />
      {showProductPopup && (
        loadingProduct ? (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
            <div className="bg-white rounded-lg shadow-lg p-6 min-w-[320px] max-w-[90vw] relative">
              <div>Loading product details...</div>
              <button
                onClick={() => { setShowProductPopup(false); setSelectedProduct(null); }}
                className="absolute top-2 right-2 text-gray-500 hover:text-gray-800 text-xl font-bold"
                aria-label="Close"
              >
                ×
              </button>
            </div>
          </div>
        ) : (
          selectedProduct && (
            <ProductDetailPopup
              product={selectedProduct}
              onClose={() => { setShowProductPopup(false); setSelectedProduct(null); }}
            />
          )
        )
      )}
    </>
  );
}
