#!/bin/bash
set -e

# Set the MySQL root password
MYSQL_PWD=$MYSQL_PASSWORD
MYSQL_USER=$MYSQL_USER

# Check if the database exists, create it if it does not
DB_EXISTS=$(mysql --user=${MYSQL_USER} --password=${MYSQL_PWD} --host=mysql --database=default-realm -sse "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'default-realm';")

if [ -z "$DB_EXISTS" ]; then
    echo "Database 'default-realm' does not exist. Creating..."
    mysql -u root -h mysql -e "CREATE DATABASE \`default-realm\`;"
else
    echo "Database 'default-realm' already exists. Skipping creation."
fi

# Create the `bootstrap_status` table if it doesn't exist
mysql --user=${MYSQL_USER} --password=${MYSQL_PWD} --host=mysql --database=default-realm -e "CREATE TABLE IF NOT EXISTS bootstrap_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bootstrap_done BOOLEAN NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"

echo "Created Bootstrap table, if it did not exist..."

# Check if the bootstrap has already been done by querying the database
BOOTSTRAP_DONE=$(mysql --user=${MYSQL_USER} --password=${MYSQL_PWD} --host=mysql --database=default-realm -sse "SELECT COUNT(*) FROM bootstrap_status WHERE bootstrap_done = TRUE;")

if [ "$BOOTSTRAP_DONE" -eq 0 ]; then
    echo "Bootstrap not done. Running bootstrap..."

    # Create entities table as Polaris tries to make VARCHAR exceeding the character limit
    echo $(mysql --user=${MYSQL_USER} --password=${MYSQL_PWD} --host=mysql --database=default-realm \
    -e 'CREATE TABLE IF NOT EXISTS ENTITIES (
        CATALOGID BIGINT NOT NULL AUTO_INCREMENT, 
        ID BIGINT NOT NULL, 
        CREATETIMESTAMP BIGINT, 
        DROPTIMESTAMP BIGINT, 
        ENTITYVERSION INTEGER, 
        GRANTRECORDSVERSION INTEGER, 
        INTERNALPROPERTIES TEXT,
        LASTUPDATETIMESTAMP BIGINT, 
        NAME VARCHAR(255), 
        PARENTID BIGINT, 
        PROPERTIES TEXT,
        PURGETIMESTAMP BIGINT, 
        SUBTYPECODE INTEGER, 
        TOPURGETIMESTAMP BIGINT, 
        TYPECODE INTEGER, 
        VERSION BIGINT, 
        PRIMARY KEY (CATALOGID, ID)
    );')

    echo "Entities table created..."

    # Run the bootstrap command to setup the persistence layer
    /app/bin/polaris-service bootstrap polaris-server.yml


    # After successful bootstrap, update the table
    mysql --user=${MYSQL_USER} --password=${MYSQL_PWD} --host=mysql --database=default-realm -e "INSERT INTO bootstrap_status (bootstrap_done) VALUES (TRUE);"
    echo "Bootstrap completed."
else
    echo "Bootstrap already done. Skipping."
fi

# Start the application
/app/bin/polaris-service server polaris-server.yml