CREATE DATABASE tobias;

-- Connect to the newly created database
\connect tobias

-- Create user and grant privileges
CREATE USER tobias_user WITH PASSWORD 'tobias_tobias';
GRANT ALL PRIVILEGES ON DATABASE tobias TO tobias_user;
