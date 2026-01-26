"use client";

import React from "react";
import { Territory } from "@/app/types";

interface TerritoryDetailPopupProps {
  territory: Territory;
  onClose: () => void;
}

export default function TerritoryDetailPopup({ territory, onClose }: TerritoryDetailPopupProps) {
  if (!territory) return null;
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
        <h2 className="text-xl font-bold mb-2">Territory #{territory.id}</h2>
        <div className="mb-2">Name: {territory.name}</div>
        <div className="mb-2">Country: {territory.country_region_code}</div>
        <div className="mb-2">Group: {territory.group}</div>
      </div>
    </div>
  );
}
