"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"

const navItems = [
  { href: "/", label: "Home" },
  { href: "/customers", label: "Customers" },
  { href: "/products", label: "Products" },
  { href: "/sales-orders", label: "Sales Orders" },
  { href: "/stores", label: "Stores" },
  { href: "/territories", label: "Territories" },
  { href: "/people", label: "People" }, // Added People link
]

export function Nav() {
  const pathname = usePathname()

  return (
    <nav className="border-b mb-6">
      <ul className="flex gap-4 p-4">
        {navItems.map(({ href, label }) => (
          <li key={href}>
            <Link
              href={href}
              className={`hover:underline ${
                pathname === href ? "font-bold" : ""
              }`}
            >
              {label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  )
}
