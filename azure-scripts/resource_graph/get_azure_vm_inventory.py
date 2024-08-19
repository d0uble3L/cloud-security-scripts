from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from azure.resourcegraph import ResourceGraphClient, QueryRequest

def get_vm_inventory():
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
    resource_graph_client = ResourceGraphClient(credential)

    # Get a list of subscriptions
    subscription_client = SubscriptionClient(credential)
    subscriptions = list(subscription_client.subscriptions.list())   


    # Iterate over each subscription and query for VMs
    vm_inventory = []
    for subscription in subscriptions:
        subscription_id = subscription.subscription_id
        query = "Resources | where type == 'Microsoft.Compute/virtualMachines' | project name, location, resourceGroup"

        query_request = QueryRequest(
            subscriptions=[subscription_id],
            query=query
        )

        response = resource_graph_client.resources(query_request)
        vm_inventory.extend(response.data)

    return vm_inventory

# Example usage
vm_data = get_vm_inventory()
print(vm_data)
