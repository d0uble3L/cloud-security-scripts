from azure.identity import ClientSecretCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest

# Replace with your Azure service principal details
tenant_id = "<YOUR_TENANT_ID>"
client_id = "<YOUR_CLIENT_ID>"
client_secret = "<YOUR_CLIENT_SECRET>"
subscription_id = "<YOUR_SUBSCRIPTION_ID>"

# Authenticate to Azure using the service principal
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

# Initialize the Resource Graph client
client = ResourceGraphClient(credential)

# Define the Azure Resource Graph query
query = "Resources | project name, type, location | limit 10"

# Create the query request
query_request = QueryRequest(
    subscriptions=[subscription_id],
    query=query
)

# Run the query
response = client.resources(query_request)

# Print the results
for resource in response.data:
    print(f"Name: {resource['name']}, Type: {resource['type']}, Location: {resource['location']}")
