import React, { useRef, useState } from "react";

interface FileUploadModalProps {
  onClose: () => void;
  onUpload: (file: File) => void;
}


export default function FileUploadModal({ onClose, onUpload }: FileUploadModalProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleUploadClick = () => {
    inputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center" style={{ background: 'rgba(0,0,0,0.15)' }}>
      <div className="bg-white rounded-lg shadow-lg p-6 min-w-[320px] max-w-[90vw] relative">
        <button onClick={onClose} className="absolute top-2 right-2 text-xl font-bold text-gray-700">×</button>
        <h2 className="text-xl font-bold mb-4 text-gray-900">Upload File</h2>
        <input
          ref={inputRef}
          type="file"
          className="hidden"
          onChange={handleFileChange}
          accept="*"
        />
        <div className="flex gap-2 mt-4">
          <button
            type="button"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            onClick={handleUploadClick}
          >
            Upload
          </button>
          <button
            type="button"
            onClick={onClose}
            className="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
