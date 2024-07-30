from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

credential = DefaultAzureCredential()
client = LogsQueryClient(credential)
query = "AzureActivity | where ActivityStatusValue == 'Failure'"

response = client.query_workspace('YOUR_LOG_ANALYTICS_WORKSPACE_ID', query)
for table in response.tables:
    for row in table.rows:
        print(row)
