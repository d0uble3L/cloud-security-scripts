from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient

credential = DefaultAzureCredential()
subscription_id = 'YOUR_SUBSCRIPTION_ID'
storage_client = StorageManagementClient(credential, subscription_id)

for storage_account in storage_client.storage_accounts.list():
    keys = storage_client.storage_accounts.list_keys(storage_account.resource_group, storage_account.name)
    for key in keys.keys:
        print(f"Storage Account: {storage_account.name}, Key: {key.key_name}")
