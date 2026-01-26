"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import ProductDetailPopup from "./ProductDetail";
import Link from "next/link";
import { API_BASE_URL } from "@/lib/config";

export default function ProductDetailsPage() {
  const params = useParams();
  const productId = params?.productId || params?.productId?.[0];
  const [product, setProduct] = useState(null);
  const [showPopup, setShowPopup] = useState(true);

useEffect(() => {
  if (!productId) return;
  fetch(`${API_BASE_URL}/api/products/${productId}`)
    .then((res) => res.json())
    .then(setProduct);
}, [productId]);

  if (!productId) return <div>Product ID is missing (params: {JSON.stringify(params)})</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Product {productId} Details</h1>
      {showPopup && (
        product ? (
          <ProductDetailPopup product={product} onClose={() => setShowPopup(false)} />
        ) : (
          <div>Loading product details...</div>
        )
      )}
      {!showPopup && (
        <Link href="/products" className="inline-block px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">
          ← Back to Products
        </Link>
      )}
    </div>
  );
}
