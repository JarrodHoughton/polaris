#!/bin/sh

# Check if necessary environment variables are set
: "${POLARIS_METRIC_PORT:?POLARIS_METRIC_PORT is not set}"
: "${CATALOG_NAME:?CATALOG_NAME is not set}"
: "${S3_WAREHOUSE_LOCATION:?S3_WAREHOUSE_LOCATION is not set}"
: "${POLARIS_ROLE_ARN:?POLARIS_ROLE_ARN is not set}"
: "${CATALOG_NAMESPACE:?CATALOG_NAMESPACE is not set}"
: "${DB_HOST:?DB_HOST is not set}"
: "${DB_USER:?DB_USER is not set}"
: "${DB_PASSWORD:?DB_PASSWORD is not set}"
: "${POLARIS_HOST:?POLARIS_HOST is not set}"
: "${POLARIS_PORT:?POLARIS_PORT is not set}"
: "${ENGINEER_NAME:?ENGINEER_NAME is not set}"

# Wait for Polaris to be ready
echo "Waiting for Polaris to be ready at ${POLARIS_HOST}:${POLARIS_METRIC_PORT}...";
until nc -z "${POLARIS_HOST}" "${POLARIS_METRIC_PORT}"; do
  echo "Polaris not ready, retrying in 5 seconds..."
  sleep 5;
done;

echo "Polaris is ready, initializing..."

# Run the Python script for initialization
python ./init-polaris.py \
  --catalog-name="${CATALOG_NAME}" \
  --s3-warehouse-location="${S3_WAREHOUSE_LOCATION}" \
  --polaris-role-arn="${POLARIS_ROLE_ARN}" \
  --catalog-namespace="${CATALOG_NAMESPACE}" \
  --postgres-host="${DB_HOST}" \
  --postgres-user="${DB_USER}" \
  --postgres-password="${DB_PASSWORD}" \
  --polaris-host="${POLARIS_HOST}" \
  --polaris-port="${POLARIS_PORT}" \
  --engineer-principal-name="${ENGINEER_NAME}"

# Check if the Python script succeeded
if [ $? -eq 0 ]; then
  echo "Polaris initialization completed successfully."
else
  echo "Polaris initialization failed." >&2
  exit 1
fi