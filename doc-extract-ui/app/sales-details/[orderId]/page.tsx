// page.tsx
import SalesOrderDetailsTable from "./SalesOrderDetailsTable";

interface PageProps {
  params: { orderId: string };
}

export default async function SalesOrdersDetailsPage({ params }: PageProps) {
  const { orderId } = await params;

  if (!orderId) return <div>Order ID is missing</div>; // debug guard

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">
        Sales Order {orderId} Details
      </h1>
      <SalesOrderDetailsTable orderId={orderId} />
    </div>
  );
}
