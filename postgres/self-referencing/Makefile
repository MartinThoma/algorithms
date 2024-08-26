build:
	docker build -t my_postgres_db .

run:
	docker run --name my_postgres_container -d -p 5432:5432 my_postgres_db

dump:
	docker exec -t my_postgres_container pg_dump -U myuser -d my_database_name > my_database_name_dump.sql