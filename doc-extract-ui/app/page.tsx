"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import Toast from "@/components/Toast";
import FileUploadModal from "@/components/FileUploadModal";
import { API_BASE_URL } from "@/lib/config";

export default function Home() {
  const [showUpload, setShowUpload] = useState(false);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{
    message: string;
    type?: 'success' | 'error' | 'info';
    show: boolean;
    link?: { href: string; label?: string };
  }>({ message: '', type: 'info', show: false });



  const handleFileUpload = async (file: File) => {
    setShowUpload(false); // Close modal immediately
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const response = await fetch(`${API_BASE_URL}/api/invoices`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        const errorMsg = data && data.error ? `File processing failed: ${data.error}` : "File processing failed.";
        setToast({ message: errorMsg, type: "error", show: true });
        return;
      }
      if (data && data.order_id) {
        setToast({
          message: "File processed successfully!",
          type: "success",
          show: true,
          link: {
            href: `/sales-details/${data.order_id}`,
            label: "View Sales Order"
          }
        });
      } else {
        setToast({ message: "File processed successfully!", type: "success", show: true });
      }
    } catch (err: any) {
      setToast({ message: `File processing failed. ${err?.message || ''}`.trim(), type: "error", show: true });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-white text-gray-900 px-4">
      <div className="max-w-2xl w-full text-center">
        <Image src="/globe.svg" alt="Document Extractor Logo" width={96} height={96} className="mx-auto mb-6" />
        <h1 className="text-4xl font-bold mb-4">Document Extractor</h1>
        <p className="text-lg mb-8">Effortlessly extract, organize, and analyze your Invoices using AI. Fast, secure, and easy to use.</p>
        <button
          className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg shadow hover:bg-blue-700 transition"
          onClick={() => setShowUpload(true)}
        >
          Get Started
        </button>
      </div>
      {showUpload && (
        <FileUploadModal
          onClose={() => setShowUpload(false)}
          onUpload={handleFileUpload}
        />
      )}
      {loading && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/20">
          <div className="bg-white rounded-lg shadow-lg p-8 flex flex-col items-center">
            <svg className="animate-spin h-8 w-8 text-blue-600 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
            </svg>
            <span className="text-lg font-semibold text-gray-900">Processing file...</span>
          </div>
        </div>
      )}
      <Toast
        message={toast.message}
        type={toast.type}
        show={toast.show}
        onClose={() => setToast((t) => ({ ...t, show: false }))}
        link={toast.link}
      />
    </main>
  );
}
