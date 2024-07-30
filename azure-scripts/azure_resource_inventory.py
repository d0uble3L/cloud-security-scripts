from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

credential = DefaultAzureCredential()
subscription_id = 'YOUR_SUBSCRIPTION_ID'
resource_client = ResourceManagementClient(credential, subscription_id)

for resource in resource_client.resources.list():
    print(f"Resource ID: {resource.id}, Type: {resource.type}, Name: {resource.name}")
