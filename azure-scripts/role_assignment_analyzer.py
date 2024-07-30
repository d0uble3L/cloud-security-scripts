from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient

credential = DefaultAzureCredential()
subscription_id = 'YOUR_SUBSCRIPTION_ID'
auth_client = AuthorizationManagementClient(credential, subscription_id)

for role_assignment in auth_client.role_assignments.list():
    print(f"Role Assignment ID: {role_assignment.id}, Role: {role_assignment.role_definition_name}")
