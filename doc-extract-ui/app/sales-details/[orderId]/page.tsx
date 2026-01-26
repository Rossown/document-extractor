// page.tsx
import SalesOrderDetailsTable from "./SalesOrderDetailsTable";

interface PageProps {
  params: { orderId: string };
}

import Link from "next/link";

export default async function SalesOrdersDetailsPage({ params }: PageProps) {
  const { orderId } = await params;

  if (!orderId) return <div>Order ID is missing</div>; // debug guard

  return (
    <div className="p-4">
      <div className="mb-4">
        <Link href="/sales-orders" className="inline-block px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">
          ← Back to Sales Orders
        </Link>
      </div>
      <h1 className="text-2xl font-bold mb-4">
        Sales Order {orderId} Details
      </h1>
      <SalesOrderDetailsTable orderId={orderId} />
    </div>
  );
}
