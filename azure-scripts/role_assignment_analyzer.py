from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.authorization.models import RoleAssignment
from azure.core.exceptions import AzureError
import json
import os

def get_azure_config():
    config_path = 'azure_config.json'
    if not os.path.exists(config_path):
        raise FileNotFoundError("Azure configuration file not found. Please run the main analyzer script to set up your Azure credentials.")
    
    with open(config_path, 'r') as f:
        return json.load(f)

def analyze_role_assignments(subscription_id):
    results = []
    try:
        credential = DefaultAzureCredential()
        auth_client = AuthorizationManagementClient(credential, subscription_id)

        results.append("Analyzing Azure Role Assignments...")
        role_assignments = list(auth_client.role_assignments.list())
        
        if not role_assignments:
            results.append("No role assignments found in the subscription.")
        else:
            for role_assignment in role_assignments:
                results.append(f"\nRole Assignment ID: {role_assignment.id}")
                results.append(f"Principal ID: {role_assignment.principal_id}")
                results.append(f"Scope: {role_assignment.scope}")
                
                role_def_id = role_assignment.role_definition_id
                role_def = auth_client.role_definitions.get_by_id(role_def_id)
                results.append(f"Role Name: {role_def.role_name}")
                results.append(f"Role Type: {role_def.role_type}")
                
                if role_def.role_name in ["Owner", "Contributor", "User Access Administrator"]:
                    results.append("WARNING: This is a high-privilege role assignment")
                
                results.append("Permissions:")
                for permission in role_def.permissions:
                    results.append(f"  Actions: {', '.join(permission.actions or [])}")
                    results.append(f"  Not Actions: {', '.join(permission.not_actions or [])}")
                    results.append(f"  Data Actions: {', '.join(permission.data_actions or [])}")
                    results.append(f"  Not Data Actions: {', '.join(permission.not_data_actions or [])}")
                
                results.append("---")

    except FileNotFoundError as e:
        results.append(str(e))
    except AzureError as e:
        results.append(f"Azure API Error: {str(e)}")
    except Exception as e:
        results.append(f"An unexpected error occurred: {str(e)}")

    return results

def main():
    print("Running Azure Role Assignment Analyzer...")
    results = []
    
    try:
        azure_config = get_azure_config()
        subscription_id = azure_config.get('subscription_id')
        
        if not subscription_id:
            subscription_id = input("Enter your Azure Subscription ID: ")
            azure_config['subscription_id'] = subscription_id
            with open('azure_config.json', 'w') as f:
                json.dump(azure_config, f)
        
        results = analyze_role_assignments(subscription_id)
        print("Azure Role Assignment Analysis complete.")
    
    except Exception as e:
        results.append(f"An error occurred: {str(e)}")
    
    for result in results:
        print(result)
    
    return results

if __name__ == "__main__":
    main()
