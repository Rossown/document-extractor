"use client";

import { PaginatedTable } from "@/components/PaginatedTable";
import { SalesOrderHeader, SalesOrderDetail } from "@/app/types";
    
import Link from "next/link";

const salesOrderColumns = [
  {
    key: "id",
    label: "ID",
    render: (row: SalesOrderHeader) => (
      <Link
        href={`/sales-details/${row.id}`}
        className="text-blue-600 hover:underline"
        title={`View details for order ${row.id}`}
      >
        {row.id}
      </Link>
    ),
  },
  { key: "revision_number", label: "Revision Number" },
  { key: "order_date", label: "Order Date" },
  { key: "due_date", label: "Due Date" },
  { key: "ship_date", label: "Ship Date" },
  { key: "status", label: "Status" },
  { key: "online_order_flag", label: "Online Order Flag" },
  { key: "sales_order_number", label: "Sales Order Number" },
  { key: "purchase_order_number", label: "Purchase Order Number" },
  { key: "account_number", label: "Account Number" },
  { key: "customer_id", label: "Customer ID" },
  { key: "sales_person_id", label: "Sales Person ID" },
  { key: "territory_id", label: "Territory ID" },
  { key: "bill_to_address_id", label: "Bill To Address ID" },
  { key: "ship_to_address_id", label: "Ship To Address ID" },
  { key: "credit_card_id", label: "Credit Card ID" },
  { key: "credit_card_approval_code", label: "Credit Card Approval Code" },
  { key: "currency_rate_id", label: "Currency Rate ID" },
  { key: "sub_total", label: "Sub Total" },
  { key: "tax_amt", label: "Tax Amount" },
  { key: "freight", label: "Freight" },
  { key: "total_due", label: "Total Due" },
] as const;

export default function SalesOrdersPage() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Sales Orders</h1>
      <PaginatedTable columns={salesOrderColumns} endpoint="/api/sales-orders" />
    </div>
  );
}
