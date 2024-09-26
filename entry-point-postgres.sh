#!/bin/bash
set -e



export PGPASSWORD=$DB_PASSWORD

# create database if not exist 
psql -U $DB_USER -h $DB_HOST -c "SELECT 'CREATE DATABASE default-realm' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'default-realm')"

# create bootstrap table if not exist
psql -U $DB_USER -h $DB_HOST -d default-realm -c "CREATE TABLE IF NOT EXISTS bootstrap_status ( id SERIAL PRIMARY KEY, bootstrap_done BOOLEAN NOT NULL, completed_at TIMESTAMP DEFAULT NOW());"

# Check if the bootstrap has already been done by querying the database
BOOTSTRAP_DONE=$(psql -U $DB_USER -h $DB_HOST -d default-realm -tAc "SELECT COUNT(*) FROM bootstrap_status WHERE bootstrap_done = TRUE;")

if [ "$BOOTSTRAP_DONE" -eq 0 ]; then
    echo "Bootstrap not done. Running bootstrap..."
    
    # Run the bootstrap command to setup the persistence layer
    /app/bin/polaris-service bootstrap polaris-server.yml

    # After successful bootstrap, update the table
    psql -U $DB_USER -h $DB_HOST -d default-realm -c "INSERT INTO bootstrap_status (bootstrap_done) VALUES (TRUE);"
    echo "Bootstrap completed."
else
    echo "Bootstrap already done. Skipping."
fi

export DB_USER=$DB_USER
export DB_PASSWORD=$DB_PASSWORD
export DB_HOST=$DB_HOST

# Start the application
/app/bin/polaris-service server polaris-server.yml