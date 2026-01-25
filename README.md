# document-extractor
Extract Sales Invoice information using OpenAI API




# Setup

## Flask commands
```bash
#Initialize migrations:
flask --app app db init

#Generate a migration:
flask --app app db migrate -m "Initial migration"

#Apply the migration:
flask --app app db upgrade
```

## Database Commands

```bash
# Pull postgres 
docker pull postgres

# Create docker volume
docker volume create postgres_data

# Run postgres container
docker run -d --name mypostgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -v postgres_data:/var/lib/postgresql postgres

# Connect
psql -U postgres -d doc_extract_api_db

# List tables
\dt

# Describe table
\d table_name
```


```bash
2026-01-25 12:49:49 | INFO     | utils.py:38 | create_database_if_not_exists() | Database doc_extract_api_db already exists.
Sheets: ['Product', 'ProductCategory', 'ProductSubCategory', 'SalesOrderHeader', 'SalesOrderDetail', 'SalesTerritory', 'Customers', 'IndividualCustomers', 'StoreCustomers']
Importing StoreCustomers into Store...
Imported 711 records into store.
Importing IndividualCustomers into Person...
Imported 18508 records into person.
Importing SalesTerritory into SalesTerritory...
Imported 10 records into sales_territory.
Importing Customers into Customer...
Imported 19820 records into customer.
Importing SalesOrderHeader into SalesOrderHeader...
Imported 31465 records into sales_order_header.
Importing ProductCategory into ProductCategory...
Imported 4 records into product_category.
Importing ProductSubCategory into ProductSubCategory...
Imported 37 records into product_subcategory.
Importing Product into ProductData...
Imported 504 records into product_data.
Importing SalesOrderDetail into SalesOrderDetail...
Imported 121317 records into sales_order_detail.
```

# UI Starter Template
npx create-next-app@latest