-- Create a user FIRST
CREATE USER tobias_user WITH PASSWORD 'tobias_user';

-- THEN create the database
CREATE DATABASE tobias OWNER tobias_user;

-- OPTIONAL: Redundant grant for clarity
GRANT ALL PRIVILEGES ON DATABASE tobias TO tobias_user;