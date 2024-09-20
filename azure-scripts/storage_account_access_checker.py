from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.core.exceptions import AzureError
import json
import os

def get_azure_config():
    config_path = 'azure_config.json'
    if not os.path.exists(config_path):
        raise FileNotFoundError("Azure configuration file not found. Please run the main analyzer script to set up your Azure credentials.")
    
    with open(config_path, 'r') as f:
        return json.load(f)

def check_storage_account_access(subscription_id):
    results = []
    try:
        credential = DefaultAzureCredential()
        storage_client = StorageManagementClient(credential, subscription_id)

        results.append("Checking Azure Storage Account Access...")
        storage_accounts = list(storage_client.storage_accounts.list())
        
        if not storage_accounts:
            results.append("No storage accounts found in the subscription.")
        else:
            for storage_account in storage_accounts:
                results.append(f"\nStorage Account: {storage_account.name}")
                results.append(f"Resource Group: {storage_account.id.split('/')[4]}")
                results.append(f"Location: {storage_account.location}")
                results.append(f"SKU: {storage_account.sku.name}")
                results.append(f"Access Tier: {storage_account.access_tier}")
                
                if storage_account.allow_blob_public_access:
                    results.append("WARNING: Blob public access is allowed!")
                else:
                    results.append("Blob public access is not allowed.")
                
                if storage_account.encryption.services.blob.enabled:
                    results.append("Blob encryption is enabled.")
                else:
                    results.append("WARNING: Blob encryption is not enabled!")
                
                if storage_account.network_rule_set:
                    results.append("Network Rules:")
                    results.append(f"  Default Action: {storage_account.network_rule_set.default_action}")
                    if storage_account.network_rule_set.ip_rules:
                        results.append("  IP Rules:")
                        for ip_rule in storage_account.network_rule_set.ip_rules:
                            results.append(f"    {ip_rule.ip_address_or_range}")
                    else:
                        results.append("  No specific IP rules set.")
                    
                    if storage_account.network_rule_set.virtual_network_rules:
                        results.append("  Virtual Network Rules:")
                        for vnet_rule in storage_account.network_rule_set.virtual_network_rules:
                            results.append(f"    {vnet_rule.virtual_network_resource_id}")
                    else:
                        results.append("  No virtual network rules set.")
                else:
                    results.append("WARNING: No network rules set. Storage account may be publicly accessible.")
                
                results.append("---")

    except FileNotFoundError as e:
        results.append(str(e))
    except AzureError as e:
        results.append(f"Azure API Error: {str(e)}")
    except Exception as e:
        results.append(f"An unexpected error occurred: {str(e)}")

    return results

def main():
    print("Running Azure Storage Account Access Checker...")
    results = []
    
    try:
        azure_config = get_azure_config()
        subscription_id = azure_config.get('subscription_id')
        
        if not subscription_id:
            subscription_id = input("Enter your Azure Subscription ID: ")
            azure_config['subscription_id'] = subscription_id
            with open('azure_config.json', 'w') as f:
                json.dump(azure_config, f)
        
        results = check_storage_account_access(subscription_id)
        print("Azure Storage Account Access Check complete.")
    
    except Exception as e:
        results.append(f"An error occurred: {str(e)}")
    
    for result in results:
        print(result)
    
    return results

if __name__ == "__main__":
    main()
