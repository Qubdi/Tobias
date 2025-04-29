FROM mcr.microsoft.com/mssql/server:2022-latest

USER root

ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies
RUN apt-get update
RUN apt-get install -y curl gnupg apt-transport-https software-properties-common dos2unix

# Add Microsoft SQL Server repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list

# Remove conflicting ODBC packages (ignore errors if not found)
RUN apt-get remove -y libodbc2 libodbcinst2 unixodbc-common || true

# Install SQL Server tools
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev

# Copy init script
COPY init/mssql/01-init.sh /init/01-init.sh

# Fix line endings and make the script executable
RUN dos2unix /init/01-init.sh
RUN chmod +x /init/01-init.sh

# Add sqlcmd to PATH
ENV PATH="${PATH}:/opt/mssql-tools/bin"
