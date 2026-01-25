# document-extractor
Extract Sales Invoice information using OpenAI API


# Setup

docker volume create postgres_data

docker run -d --name mypostgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -v postgres_data:/var/lib/postgresql postgres
