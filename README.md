# document-extractor
Extract Sales Invoice information using OpenAI API




# Setup


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

# UI Starter Template
npx create-next-app@latest