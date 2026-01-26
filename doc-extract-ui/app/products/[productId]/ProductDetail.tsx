"use client";

import React from "react";

interface ProductDetailPopupProps {
  product: any;
  onClose: () => void;
}

export default function ProductDetailPopup({ product, onClose }: ProductDetailPopupProps) {
  if (!product) return null;
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      style={{
        background: 'rgba(0,0,0,0.15)',
        // much lighter overlay so background content is visible
      }}
    >
      <div
        className="rounded-lg shadow-lg p-6 min-w-[320px] max-w-[90vw] relative bg-gray-50 dark:bg-gray-200"
        style={{
          color: 'var(--color-foreground, #171717)',
        }}
      >
        <button
          onClick={onClose}
          className="absolute top-2 right-2 w-10 h-10 flex items-center justify-center rounded-full bg-red-500 text-white text-2xl font-extrabold shadow-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 z-10"
          aria-label="Close"
        >
          ×
        </button>
        <h2 className="text-xl font-bold mb-2">{product.product_name}</h2>
        <div className="mb-2">Product Number: {product.product_number}</div>
        <div className="mb-2">Price: <span className="font-semibold">${product.list_price?.toLocaleString(undefined, {minimumFractionDigits: 2})}</span></div>
        <div className="mb-2">Size: {product.size} | Color: {product.color} | Style: {product.style} | Class: {product.class_field}</div>
        <div className="mb-2">Make Flag: {product.make_flag ? "Yes" : "No"} | Finished Goods: {product.finished_goods_flag ? "Yes" : "No"}</div>
        <div className="mb-2">Subcategory: {product.subcategory?.name}</div>
        <div className="mb-2">Category: {product.subcategory?.category?.name}</div>
        <div className="mt-4">
          <pre className="bg-white p-2 rounded text-xs overflow-x-auto max-h-40" style={{ background: 'white' }}>{JSON.stringify(product, null, 2)}</pre>
        </div>
      </div>
    </div>
  );
}
