import json
import os
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import AzureError

def get_azure_config():
    config_path = 'azure_config.json'
    if not os.path.exists(config_path):
        raise FileNotFoundError("Azure configuration file not found. Please run the main analyzer script to set up your Azure credentials.")
    
    with open(config_path, 'r') as f:
        return json.load(f)

def list_azure_resources():
    results = []
    try:
        azure_config = get_azure_config()

        credential = ClientSecretCredential(
            tenant_id=azure_config['tenant_id'],
            client_id=azure_config['client_id'],
            client_secret=azure_config['client_secret']
        )
        subscription_id = azure_config['subscription_id']
        resource_client = ResourceManagementClient(credential, subscription_id)

        results.append(f"Listing Azure resources for subscription: {subscription_id}")
        resources = list(resource_client.resources.list())
        
        if not resources:
            results.append("No resources found in the subscription.")
        else:
            resource_types = {}
            for resource in resources:
                if resource.type not in resource_types:
                    resource_types[resource.type] = []
                resource_types[resource.type].append(resource)
            
            for resource_type, resources_list in resource_types.items():
                results.append(f"\nResource Type: {resource_type}")
                results.append(f"Total count: {len(resources_list)}")
                for resource in resources_list:
                    results.append(f"  Name: {resource.name}")
                    results.append(f"  ID: {resource.id}")
                    results.append(f"  Location: {resource.location}")
                    results.append("  ---")

    except FileNotFoundError as e:
        results.append(str(e))
    except AzureError as e:
        results.append(f"Azure API Error: {str(e)}")
    except Exception as e:
        results.append(f"An unexpected error occurred: {str(e)}")

    return results

def main():
    print("Running Azure Resource Inventory...")
    results = list_azure_resources()
    
    for result in results:
        print(result)
    
    print("Azure Resource Inventory complete.")
    return results

if __name__ == "__main__":
    main()
