"use client"
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const html = document.documentElement;
    if (darkMode) {
      html.classList.add("dark");
    } else {
      html.classList.remove("dark");
    }
  }, [darkMode]);

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-[var(--color-background)] text-[var(--color-foreground)] px-4">
      <div className="absolute top-4 right-4">
        <button
          onClick={() => setDarkMode((d) => !d)}
          className="bg-gray-200 dark:bg-gray-800 text-gray-800 dark:text-gray-200 px-4 py-2 rounded shadow hover:bg-gray-300 dark:hover:bg-gray-700 transition"
        >
          {darkMode ? "🌙 Dark Mode" : "☀️ Light Mode"}
        </button>
      </div>
      <div className="max-w-2xl w-full text-center">
        <Image src="/globe.svg" alt="Document Extractor Logo" width={96} height={96} className="mx-auto mb-6" />
        <h1 className="text-4xl font-bold mb-4">Document Extractor</h1>
        <p className="text-lg mb-8">Effortlessly extract, organize, and analyze your Invoices using AI. Fast, secure, and easy to use.</p>
        <a href="#" className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg shadow hover:bg-blue-700 transition">Get Started</a>
      </div>
    </main>
  );
}
