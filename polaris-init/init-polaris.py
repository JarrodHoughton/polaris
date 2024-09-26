from polaris.catalog.api.iceberg_catalog_api import IcebergCatalogAPI
from polaris.catalog.api.iceberg_o_auth2_api import IcebergOAuth2API
from polaris.catalog.api_client import ApiClient as CatalogApiClient
from polaris.catalog.api_client import Configuration as CatalogApiClientConfiguration
from polaris.management import *
from polaris.management import *
from polaris.catalog.models import CreateNamespaceRequest
import argparse
import psycopg2

parser=argparse.ArgumentParser()
parser.add_argument('--catalog-name', required=True)
parser.add_argument('--catalog-namespace', required=True)
parser.add_argument('--s3-warehouse-location', required=True)
parser.add_argument('--polaris-role-arn', required=True)
parser.add_argument('--polaris-host', required=True)
parser.add_argument('--polaris-port', default=8181)
parser.add_argument('--postgres-host', required=True)
parser.add_argument('--postgres-user', required=True)
parser.add_argument('--postgres-password', required=True)
parser.add_argument('--engineer-principal-name', required=True)


args=parser.parse_args()

catalog_name = args.catalog_name
catalog_namespace = args.catalog_namespace
s3_warehouse_location = args.s3_warehouse_location
polaris_role_arn = args.polaris_role_arn
postgres_host = args.postgres_host
postgres_user = args.postgres_user
postgres_password = args.postgres_password
polaris_host = args.polaris_host
polaris_port = args.polaris_port
engineer_principal_name = args.engineer_principal_name
catalog = None

POLARIS_URL=f'http://{polaris_host}:{polaris_port}'

POLARIS_DB_NAME = 'default-realm'

#####################
# Utility Functions #
#####################

# Creates a principal with the given name
def create_principal(api, principal_name):
  principal = Principal(name=principal_name, type="SERVICE")
  try:
    principal_result = api.create_principal(CreatePrincipalRequest(principal=principal))
    return principal_result
  except ApiException as e:
    if e.status == 409:
        print(api.get_principal(principal_name=principal_name))
        return api.rotate_credentials(principal_name=principal_name)
    else:
      raise e

# Create a catalog role with the given name
def create_catalog_role(api, catalog, role_name):
  catalog_role = CatalogRole(name=role_name)
  try:
    api.create_catalog_role(catalog_name=catalog.name, create_catalog_role_request=CreateCatalogRoleRequest(catalog_role=catalog_role))
    return api.get_catalog_role(catalog_name=catalog.name, catalog_role_name=role_name)
  except ApiException as e:
    return api.get_catalog_role(catalog_name=catalog.name, catalog_role_name=role_name)
  else:
    raise e

# Create a principal role with the given name
def create_principal_role(api, role_name):
  principal_role = PrincipalRole(name=role_name)
  try:
    api.create_principal_role(CreatePrincipalRoleRequest(principal_role=principal_role))
    return api.get_principal_role(principal_role_name=role_name)
  except ApiException as e:
    return api.get_principal_role(principal_role_name=role_name)


###########################################################
# Get root credentials from postgres database for polaris #
###########################################################

print(f"Connecting to PostgreSQL on host: {postgres_host}")
conn = psycopg2.connect(host=postgres_host,
                        database=POLARIS_DB_NAME,
                        user=postgres_user,
                        password=postgres_password)

# Execute select * from principal_secrets
cur = conn.cursor()
cur.execute("SELECT * FROM public.principal_secrets")
# fetch first row
principal_secret_row = cur.fetchone()
# get the principal_client_id and main_secret
client_id = principal_secret_row[0]
client_secret = principal_secret_row[1]
print(f"Obtained root credentials")

#######################################
# Get API Token with root credentials #
#######################################

client = CatalogApiClient(CatalogApiClientConfiguration(username=client_id,
                                 password=client_secret,
                                 host=f'{POLARIS_URL}/api/catalog'))

oauth_api = IcebergOAuth2API(client)
token = oauth_api.get_token(scope='PRINCIPAL_ROLE:ALL',
                            client_id=client_id,
                          client_secret=client_secret,
                          grant_type='client_credentials',
                          _headers={'realm': 'default-realm'})

client = ApiClient(Configuration(access_token=token.access_token,
                                   host=f'{POLARIS_URL}/api/management/v1'))
root_client = PolarisDefaultApi(client)

storage_conf = AwsStorageConfigInfo(storage_type="S3",
                                  allowed_locations=[s3_warehouse_location],
                                  role_arn=polaris_role_arn)

print("Connected to Polaris Catalog")

##########################
# Create Polaris Catalog #
##########################
print(f"Creating catalog: {catalog_name}")
try:
    catalog = Catalog(name=catalog_name, type='INTERNAL', properties={"default-base-location": f"{s3_warehouse_location}polaris_catalog"},
                    storage_config_info=storage_conf)
    catalog.storage_config_info = storage_conf
    root_client.create_catalog(create_catalog_request=CreateCatalogRequest(catalog=catalog))
    resp = root_client.get_catalog(catalog_name=catalog.name)
    print(resp)
except ApiException as e:
    if e.status == 409:
        # catalog already exists
        print(f"Catalog {catalog_name} already exists.")
except Exception as e:
    print(f"Error creating catalog: {e}")


################################
# Create the initial namespace #
################################

print(f"Creating namespace: {catalog_namespace}")

try:
    client = CatalogApiClient(CatalogApiClientConfiguration(access_token=token.access_token,
              host=f'{POLARIS_URL}/api/catalog'))
    catalog_client = IcebergCatalogAPI(client)

    # Create the CreateNamespaceRequest object
    create_namespace_request = CreateNamespaceRequest(namespace=[catalog_namespace])

    # Call the create_namespace method with the correct parameters
    response = catalog_client.create_namespace(
        prefix=catalog_name,
        create_namespace_request=create_namespace_request
    )
    # Print the response
    print(response)
except ApiException as e:
    if e.type == "AlreadyExistsException":
        print(f"Namespace {catalog_namespace} already exists.")
    else:
        print(e)
except Exception as e:
    print(f"Error creating namespace: {e}")
    
    
#####################################################
# Create engineer principal with catalog privileges #
#####################################################

try:
    print(f"Creating engineer principal: {engineer_principal_name}.")
    # Create the engineer_principal
    engineer_principal = create_principal(root_client, "engineer_principal")
    print(f"Engineer principal created: {engineer_principal}")

    print(f"Creating engineer role.")
    # Create the principal role
    engineer_role = create_principal_role(root_client, "engineer")
    print(f"Engineer role created: {engineer_role}")

    print(f"Creating catalog role.")
    # Create the catalog role
    manager_catalog_role = create_catalog_role(root_client, catalog, "manage_catalog")
    print(f"Catalog role created: {manager_catalog_role}")

    print(f"Granting catalog role to engineer role.")
    # Grant the catalog role to the principal role
    # All principals in the principal role have the catalog role's privileges
    response = root_client.assign_catalog_role_to_principal_role(principal_role_name=engineer_role.name,
                                                    catalog_name=catalog.name,
                                                    grant_catalog_role_request=GrantCatalogRoleRequest(catalog_role=manager_catalog_role))
    print(f"Catalog role granted to engineer role. Result: {response}")

    print(f"Granting catalog privileges to catalog role.")
    # Assign privileges to the catalog role
    # Here, we grant CATALOG_MANAGE_CONTENT
    response = root_client.add_grant_to_catalog_role(catalog.name, manager_catalog_role.name,
                                        AddGrantRequest(grant=CatalogGrant(catalog_name=catalog.name,
                                                                        type='catalog',
                                                                        privilege=CatalogPrivilege.CATALOG_MANAGE_CONTENT)))
    print(f"Catalog privileges granted to catalog role. Result: {response}")

    print(f"Assigning engineer role to engineer principal.")
    # Assign the principal role to the principal
    response = root_client.assign_principal_role(engineer_principal.principal.name, grant_principal_role_request=GrantPrincipalRoleRequest(principal_role=engineer_role))
    print(f"Engineer role assigned to engineer principal. Result: {response}")
except Exception as e:
    print(f"Error creating engineer principal: {e}")