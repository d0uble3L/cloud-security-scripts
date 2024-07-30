from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient

credential = DefaultAzureCredential()
subscription_id = 'YOUR_SUBSCRIPTION_ID'
network_client = NetworkManagementClient(credential, subscription_id)

for nsg in network_client.network_security_groups.list_all():
    for rule in nsg.security_rules:
        if rule.destination_address_prefix == '*':
            print(f"NSG: {nsg.name}, Rule: {rule.name} allows traffic from any IP")
