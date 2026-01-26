"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const navItems = [
  { href: "/", label: "Home" },
  { href: "/customers", label: "Customers" },
  { href: "/products", label: "Products" },
  { href: "/sales-orders", label: "Sales Orders" },
  { href: "/stores", label: "Stores" },
  { href: "/territories", label: "Territories" },
];

function generateBreadcrumbs(pathname: string) {
  const parts = pathname.split("/").filter(Boolean);
  const breadcrumbs = [{ href: "/", label: "Home" }];
  let accumulated = "";

  for (const part of parts) {
    accumulated += `/${part}`;
    breadcrumbs.push({
      href: accumulated,
      label: part.replace(/-/g, " "),
    });
  }

  return breadcrumbs;
}

export function Header() {
  const pathname = usePathname();
  const breadcrumbs = generateBreadcrumbs(pathname);
  const [darkMode, setDarkMode] = useState(false);

  // Initialize theme ONCE
  useEffect(() => {
    const theme = localStorage.getItem("theme");
    const isDark = theme === "dark";
    if (isDark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    setDarkMode(isDark);
  }, []);

  const handleToggle = () => {
    const next = !darkMode;
    setDarkMode(next);
    if (next) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-white dark:bg-gray-900 shadow">
      <div className="max-w-6xl mx-auto px-4 py-3 flex flex-col md:flex-row items-start md:items-center justify-between gap-3">

        {/* Logo */}
        <div className="flex items-center gap-3">
          <Image src="/globe.svg" alt="Logo" width={40} height={40} />
          <Link href="/" className="text-xl font-bold text-gray-900 dark:text-white">
            Document Extractor
          </Link>
        </div>

        {/* Nav */}
        <nav className="flex gap-6 flex-wrap">
          {navItems.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={`text-gray-700 dark:text-gray-300 hover:underline ${
                pathname === href ? "font-bold underline" : ""
              }`}
            >
              {label}
            </Link>
          ))}
        </nav>

        {/* Theme toggle */}
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-700 dark:text-gray-300">
            {darkMode ? "Dark" : "Light"} Mode
          </span>
          <button
            onClick={handleToggle}
            aria-label="Toggle dark mode"
            className={`relative w-12 h-6 rounded-full transition-colors ${
              darkMode ? "bg-blue-600" : "bg-gray-300"
            }`}
          >
            <span
              className={`absolute top-1 left-1 h-4 w-4 rounded-full bg-white shadow transition-transform ${
                darkMode ? "translate-x-6" : ""
              }`}
            />
          </button>
        </div>

        {/* Breadcrumbs */}
        <nav className="text-sm text-gray-500 dark:text-gray-400">
          {breadcrumbs.map((crumb, idx) => (
            <span key={crumb.href}>
              <Link href={crumb.href} className="hover:underline capitalize">
                {crumb.label}
              </Link>
              {idx < breadcrumbs.length - 1 && <span className="mx-1">/</span>}
            </span>
          ))}
        </nav>
      </div>
    </header>
  );
}
