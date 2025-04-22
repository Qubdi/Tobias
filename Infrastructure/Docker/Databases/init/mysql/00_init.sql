-- Create the database
CREATE DATABASE IF NOT EXISTS tobias;

-- Create user and grant privileges
CREATE USER IF NOT EXISTS 'tobias_user'@'%' IDENTIFIED BY 'tobias_tobias';
GRANT ALL PRIVILEGES ON tobias.* TO 'tobias_user'@'%';
FLUSH PRIVILEGES;