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
