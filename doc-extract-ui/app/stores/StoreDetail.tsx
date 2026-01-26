"use client";

import React from "react";
import { Store } from "@/app/types";

interface StoreDetailPopupProps {
  store: Store;
  onClose: () => void;
}

export default function StoreDetailPopup({ store, onClose }: StoreDetailPopupProps) {
  if (!store) return null;
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      style={{ background: "rgba(0,0,0,0.15)" }}
    >
      <div
        className="rounded-lg shadow-lg p-6 min-w-[320px] max-w-[90vw] relative bg-gray-50 dark:bg-gray-200"
        style={{ color: "var(--color-foreground, #171717)" }}
      >
        <button
          onClick={onClose}
          className="absolute top-2 right-2 w-10 h-10 flex items-center justify-center rounded-full bg-red-500 text-white text-2xl font-extrabold shadow-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 z-10"
          aria-label="Close"
        >
          ×
        </button>
        <h2 className="text-xl font-bold mb-2">Store #{store.id}</h2>
        <div className="mb-2">Name: {store.name}</div>
        <div className="mb-2">Address: {store.address_line1} {store.address_line2}, {store.city}, {store.state_province}, {store.postal_code}, {store.country_region}</div>
        <div className="mb-2">Business Entity ID: {store.business_entity_id}</div>
      </div>
    </div>
  );
}
