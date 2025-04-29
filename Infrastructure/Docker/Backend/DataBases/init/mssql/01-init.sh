#!/bin/bash
set -e

echo "⏳ Waiting for SQL Server to start..."
sleep 30

echo "🚀 Creating database 'tobias'..."
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrong@Passw0rd' -Q "
IF DB_ID('tobias') IS NULL
    CREATE DATABASE tobias;
"

echo "🔐 Creating login 'tobias_user'..."
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrong@Passw0rd' -Q "
IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'tobias_user')
    CREATE LOGIN tobias_user WITH PASSWORD = 'Tobias@2025';
"

echo "👤 Creating user in 'tobias' database..."
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrong@Passw0rd' -d tobias -Q "
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'tobias_user')
    CREATE USER tobias_user FOR LOGIN tobias_user;
"

echo "🎓 Granting db_owner to 'tobias_user'..."
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrong@Passw0rd' -d tobias -Q "
ALTER ROLE db_owner ADD MEMBER tobias_user;
"

echo "✅ MSSQL init completed!"