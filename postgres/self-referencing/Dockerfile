# Use the official PostgreSQL image from Docker Hub
FROM postgres:15

# Environment variables to configure the database
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=my_database_name

# Copy the SQL script to create the table into the Docker container
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the default PostgreSQL port
EXPOSE 5432