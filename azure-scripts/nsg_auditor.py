import json
import os
from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient
from azure.core.exceptions import AzureError

def get_azure_config():
    config_path = 'azure_config.json'
    if not os.path.exists(config_path):
        raise FileNotFoundError("Azure configuration file not found. Please run the main analyzer script to set up your Azure credentials.")
    
    with open(config_path, 'r') as f:
        return json.load(f)

def audit_nsgs():
    results = []
    try:
        azure_config = get_azure_config()

        credential = ClientSecretCredential(
            tenant_id=azure_config['tenant_id'],
            client_id=azure_config['client_id'],
            client_secret=azure_config['client_secret']
        )
        subscription_id = azure_config['subscription_id']
        network_client = NetworkManagementClient(credential, subscription_id)

        results.append("Auditing Network Security Groups (NSGs)...")
        nsgs = list(network_client.network_security_groups.list_all())
        
        if not nsgs:
            results.append("No Network Security Groups found in the subscription.")
        else:
            for nsg in nsgs:
                results.append(f"\nNSG Name: {nsg.name}")
                results.append(f"NSG ID: {nsg.id}")
                results.append(f"Location: {nsg.location}")
                
                if not nsg.security_rules:
                    results.append("  No security rules defined for this NSG.")
                else:
                    for rule in nsg.security_rules:
                        if rule.destination_address_prefix == '*' or rule.source_address_prefix == '*':
                            results.append(f"  WARNING: Rule '{rule.name}' allows traffic from/to any IP")
                            results.append(f"    Direction: {rule.direction}")
                            results.append(f"    Access: {rule.access}")
                            results.append(f"    Protocol: {rule.protocol}")
                            results.append(f"    Source Port Range: {rule.source_port_range}")
                            results.append(f"    Destination Port Range: {rule.destination_port_range}")
                            results.append(f"    Source Address Prefix: {rule.source_address_prefix}")
                            results.append(f"    Destination Address Prefix: {rule.destination_address_prefix}")
                        else:
                            results.append(f"  Rule '{rule.name}' is properly restricted")
                
                results.append("  ---")

    except FileNotFoundError as e:
        results.append(str(e))
    except AzureError as e:
        results.append(f"Azure API Error: {str(e)}")
    except Exception as e:
        results.append(f"An unexpected error occurred: {str(e)}")

    return results

def main():
    print("Running Azure NSG Auditor...")
    results = audit_nsgs()
    
    for result in results:
        print(result)
    
    print("Azure NSG Audit complete.")
    return results

if __name__ == "__main__":
    main()
