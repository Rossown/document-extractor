"use client";

import React from "react";
import { Person } from "@/app/types";

interface PersonDetailPopupProps {
  person: Person;
  onClose: () => void;
}

export default function PersonDetailPopup({ person, onClose }: PersonDetailPopupProps) {
  if (!person) return null;
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
        <h2 className="text-xl font-bold mb-2">Person #{person.id}</h2>
        <div className="mb-2">Business Entity ID: {person.business_entity_id}</div>
        <div className="mb-2">Name: {person.first_name} {person.middle_name} {person.last_name}</div>
        <div className="mb-2">Address: {person.address_line1} {person.address_line2}, {person.city}, {person.state_province}, {person.postal_code}, {person.country_region}</div>
      </div>
    </div>
  );
}
