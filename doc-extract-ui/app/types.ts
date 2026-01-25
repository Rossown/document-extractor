export interface Store {
  id: number;
  name: string;
  address_type?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state_province?: string;
  postal_code?: string;
  country_region?: string;
}

export interface Customer {
  id: number;
  person_id?: number;
  store_id?: number;
  territory_id?: number;
  account_number?: string;
}

export interface SalesOrderHeader {
  id: number;
  sales_order_number: string;
  customer_id?: number;
  order_date?: string; // ISO string
  total_due?: number;
  status?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  next_cursor?: string;
}