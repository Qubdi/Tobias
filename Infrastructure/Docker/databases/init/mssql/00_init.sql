CREATE DATABASE tobias;
GO

USE tobias;
GO

CREATE LOGIN tobias_user WITH PASSWORD = 'tobias_tobias';
GO

CREATE USER tobias_user FOR LOGIN tobias_user;
GO

ALTER ROLE db_owner ADD MEMBER tobias_user;
GO
