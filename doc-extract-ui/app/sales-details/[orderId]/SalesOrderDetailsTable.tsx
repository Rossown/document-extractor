"use client";

import { PaginatedTable } from "@/components/PaginatedTable";
import { SalesOrderDetail } from "@/app/types";

interface Props {
  orderId: string;
}

export default function SalesOrderDetailsTable({ orderId }: Props) {
  const columns = [
    { key: "id", label: "ID" },
    { key: "sales_order_id", label: "Sales Order ID" },
    { key: "carrier_tracking_number", label: "Carrier Tracking Number" },
    { key: "order_qty", label: "Order Quantity" },
    { key: "product_id", label: "Product ID" },
    { key: "special_offer_id", label: "Special Offer ID" },
    { key: "unit_price", label: "Unit Price" },
    { key: "unit_price_discount", label: "Unit Price Discount" },
    { key: "line_total", label: "Line Total" },
  ] as const;

  return (
    <PaginatedTable<SalesOrderDetail>
      columns={columns}
      endpoint={`/api/sales-orders/${orderId}/details`} // now orderId is always defined
      pageSize={20}
    />
  );
}
