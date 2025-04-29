-- Create databases
CREATE DATABASE tobias;

-- Create user
CREATE USER 'tobias_user'@'%' IDENTIFIED BY 'tobias_user';

-- Grant access to each database
GRANT ALL PRIVILEGES ON tobias.* TO 'tobias_user'@'%';

-- Apply privileges immediately
FLUSH PRIVILEGES;
