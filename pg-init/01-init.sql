CREATE USER cafe_backend_db_user WITH LOGIN PASSWORD 'cafe_backend_db_user';
CREATE DATABASE mr_backend;
GRANT ALL PRIVILEGES ON DATABASE mr_backend TO cafe_backend_db_user;
