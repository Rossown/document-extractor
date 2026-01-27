import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'doc-extract-api')))
import pandas as pd
from sqlalchemy import text
from api.models import db, ProductData, ProductCategory, ProductSubCategory, SalesOrderHeader, SalesOrderDetail, SalesTerritory, Customer, Person, Store
from app import app
# Path to your Excel file
EXCEL_PATH = './CaseStudyData.xlsx'
BATCH_SIZE = 100

def clean_row(row):
    """Clean a single row from Excel before inserting into DB"""
    cleaned = {}
    for k, v in row.items():
        if pd.isna(v):
            cleaned[k] = None
        elif isinstance(v, float) and v.is_integer():
            cleaned[k] = int(v)
        else:
            cleaned[k] = v
    return cleaned

#  public | customer            | table | postgres
#  public | person              | table | postgres
#  public | product_category    | table | postgres
#  public | product_data        | table | postgres
#  public | product_subcategory | table | postgres
#  public | sales_order_detail  | table | postgres
#  public | sales_order_header  | table | postgres
#  public | sales_territory     | table | postgres
#  public | store               | table | postgres
def set_sequences():
    with app.app_context():
        db.session.execute(text("SELECT setval('customer_id_seq', (SELECT MAX(id) FROM customer) + 1);"))
        db.session.execute(text("SELECT setval('person_business_entity_id_seq', (SELECT MAX(id) FROM person) + 1);"))
        db.session.execute(text("SELECT setval('product_category_id_seq', (SELECT MAX(id) FROM product_category) + 1);"))
        db.session.execute(text("SELECT setval('product_data_id_seq', (SELECT MAX(id) FROM product_data) + 1);"))
        db.session.execute(text("SELECT setval('product_subcategory_id_seq', (SELECT MAX(id) FROM product_subcategory) + 1);"))
        db.session.execute(text("SELECT setval('sales_order_detail_id_seq', (SELECT MAX(id) FROM sales_order_detail) + 1);"))
        db.session.execute(text("SELECT setval('sales_order_header_id_seq', (SELECT MAX(id) FROM sales_order_header) + 1);"))
        db.session.execute(text("SELECT setval('sales_territory_id_seq', (SELECT MAX(id) FROM sales_territory) + 1);"))
        db.session.execute(text("SELECT setval('store_business_entity_id_seq', (SELECT MAX(id) FROM store) + 1);"))
        db.session.commit()
    print("Sequences set successfully")

def import_data():
    # Load the Excel file
    xls = pd.ExcelFile(EXCEL_PATH)
    print('Sheets:', xls.sheet_names)

    sheet_model_map = [
        ('StoreCustomers', Store),
        ('IndividualCustomers', Person),
        ('SalesTerritory', SalesTerritory),
        ('Customers', Customer),
        ('SalesOrderHeader', SalesOrderHeader),
        ('ProductCategory', ProductCategory),
        ('ProductSubCategory', ProductSubCategory),
        ('Product', ProductData),
        ('SalesOrderDetail', SalesOrderDetail),
    ]

    sheet_field_map = {
        'Product': {
            'ProductID': 'id',
            'Name': 'product_name',
            'ProductNumber': 'product_number',
            'MakeFlag': 'make_flag',
            'FinishedGoodsFlag': 'finished_goods_flag',
            'Color': 'color',
            'ListPrice': 'list_price',
            'Size': 'size',
            'ProductLine': 'product_line',
            'Class': 'class_field',
            'Style': 'style',
            'ProductSubcategoryID': 'product_subcategory_id',
            'ProductModelID': 'product_model_id'
        },
        'ProductCategory': {
            'ProductCategoryID': 'id',
            'Name': 'name'
        },
        'ProductSubCategory': {
            'ProductSubCategoryID': 'id',
            'Name': 'name',
            'ProductCategoryID': 'category_id'
        },
        'SalesOrderHeader': {
            'SalesOrderID': 'id',
            'RevisionNumber': 'revision_number',
            'OrderDate': 'order_date',
            'DueDate': 'due_date',
            'ShipDate': 'ship_date',
            'Status': 'status',
            'OnlineOrderFlag': 'online_order_flag',
            'SalesOrderNumber': 'sales_order_number',
            'PurchaseOrderNumber': 'purchase_order_number',
            'AccountNumber': 'account_number',
            'CustomerID': 'customer_id',
            'SalesPersonID': 'sales_person_id',
            'TerritoryID': 'territory_id',
            'BillToAddressID': 'bill_to_address_id',
            'ShipToAddressID': 'ship_to_address_id',
            'ShipMethodID': 'ship_method_id',
            'CreditCardID': 'credit_card_id',
            'CreditCardApprovalCode': 'credit_card_approval_code',
            'CurrencyRateID': 'currency_rate_id',
            'SubTotal': 'sub_total',
            'TaxAmt': 'tax_amt',
            'Freight': 'freight',
            'TotalDue': 'total_due'
        },
        'SalesOrderDetail': {
            'SalesOrderDetailID': 'id',
            'SalesOrderID': 'sales_order_id',
            'CarrierTrackingNumber': 'carrier_tracking_number',
            'OrderQty': 'order_qty',
            'ProductID': 'product_id',
            'SpecialOfferID': 'special_offer_id',
            'UnitPrice': 'unit_price',
            'UnitPriceDiscount': 'unit_price_discount',
            'LineTotal': 'line_total'
        },
        'SalesTerritory': {
            'TerritoryID': 'id',
            'Name': 'name',
            'CountryRegionCode': 'country_region_code',
            'Group': 'group'
        },
        'Customers': {
            'CustomerID': 'id',
            'PersonID': 'person_id',
            'StoreID': 'store_id',
            'TerritoryID': 'territory_id',
            'AccountNumber': 'account_number'
        },
        'IndividualCustomers': {
            'BusinessEntityID': 'id',
            'FirstName': 'first_name',
            'MiddleName': 'middle_name',
            'LastName': 'last_name',
            'AddressType': 'address_type',
            'AddressLine1': 'address_line1',
            'AddressLine2': 'address_line2',
            'City': 'city',
            'StateProvinceName': 'state_province',
            'PostalCode': 'postal_code',
            'CountryRegionName': 'country_region'
        },
        'StoreCustomers': {
            'BusinessEntityID': 'id',
            'Name': 'name',
            'AddressType': 'address_type',
            'AddressLine1': 'address_line1',
            'AddressLine2': 'address_line2',
            'City': 'city',
            'StateProvinceName': 'state_province',
            'PostalCode': 'postal_code',
            'CountryRegionName': 'country_region'
        },
    }

    with app.app_context():
        for sheet, model in sheet_model_map:
            print(f"Importing {sheet} into {model.__name__}...")
            df = pd.read_excel(xls, sheet)
            field_map = sheet_field_map.get(sheet, {})
            if field_map:
                df = df.rename(columns=field_map)

            # Keep only valid model columns
            model_columns = set(c.name for c in model.__table__.columns)
            df = df[[col for col in df.columns if col in model_columns]]

            batch = []
            for row in df.to_dict(orient='records'):
                row = clean_row(row)
                obj = model(**row)
                batch.append(obj)

                if len(batch) >= BATCH_SIZE:
                    db.session.add_all(batch)
                    db.session.commit()
                    batch = []

            if batch:
                db.session.add_all(batch)
                db.session.commit()
                

            print(f"Imported {len(df)} records into {model.__tablename__}.")
            
            

if __name__ == '__main__':
    import_data()
    set_sequences()