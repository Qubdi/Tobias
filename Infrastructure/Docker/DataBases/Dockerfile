FROM mcr.microsoft.com/mssql/server:2022-latest

USER root

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies and add Microsoft repo
RUN apt-get update && \
    apt-get install -y curl gnupg apt-transport-https software-properties-common && \
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list

# Remove conflicting packages
RUN apt-get remove -y libodbc2 libodbcinst2 unixodbc-common || true

# Install tools (this now works)
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev


# Add init script and make executable
COPY ./init/mssql/01-init.sh /init/01-init.sh
RUN chmod +x /init/01-init.sh

# Add sqlcmd to PATH
ENV PATH="$PATH:/opt/mssql-tools/bin"
