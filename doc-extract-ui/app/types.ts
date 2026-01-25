export interface Product {
  id: number;
  product_name: string;
  product_number: string;
  make_flag: boolean;
  finished_goods_flag: boolean;
  color: string;
  standard_cost: number;
  list_price: number;
  size: string;
  product_line: string;
  class_field: string;
  style: string;
  product_subcategory_id: number;
  product_model_id: number;
  subcategory?: ProductSubCategory;
}

export interface ProductCategory {
  id: number;
  name: string;
}

export interface ProductSubCategory {
  id: number;
  name: string;
  product_category_id: number;
  category?: ProductCategory;
}

export interface SalesOrderHeader {
  id: number;
  revision_number: number;
  order_date?: string;
  due_date?: string;
  ship_date?: string;
  status: number;
  online_order_flag: boolean;
  sales_order_number: string;
  purchase_order_number?: string;
  account_number?: string;
  customer_id?: number;
  sales_person_id?: string;
  territory_id?: number;
  bill_to_address_id?: number;
  ship_to_address_id?: number;
  credit_card_id?: string;
  credit_card_approval_code?: string;
  currency_rate_id?: number;
  sub_total?: number;
  tax_amt?: number;
  freight?: number;
  total_due?: number;
}

export interface SalesOrderDetail {
  id: number;
  sales_order_id: number;
  carrier_tracking_number: string;
  order_qty: number;
  product_id: number;
  special_offer_id: number;
  unit_price: number;
  unit_price_discount?: number;
  line_total: number;
}

export interface Territory {
  id: number;
  name: string;
  country_region_code?: string;
  group?: string;
}

export interface Customer {
  id: number;
  person_id?: number;
  store_id?: number;
  territory_id?: number;
  account_number?: string;
}

export interface Person {
  id: number;
  business_entity_id: number;
  first_name?: string;
  middle_name?: string;
  last_name?: string;
  address_type?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state_province?: string;
  postal_code?: string;
  country_region?: string;
}

export interface Store {
  id: number;
  business_entity_id: number;
  name: string;
  address_type?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state_province?: string;
  postal_code?: string;
  country_region?: string;
}


export interface PaginatedResponse<T> {
  items: T[];
  next_cursor?: string;
}