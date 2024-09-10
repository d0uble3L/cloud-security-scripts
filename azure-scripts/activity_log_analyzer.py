from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
import json
import os
from datetime import datetime, timedelta

def get_azure_config():
    config_path = 'azure_config.json'
    if not os.path.exists(config_path):
        raise FileNotFoundError("Azure configuration file not found. Please run the main analyzer script to set up your Azure credentials.")
    
    with open(config_path, 'r') as f:
        return json.load(f)

def analyze_activity_logs(workspace_id):
    results = []
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    
    # Query for failures in the last 24 hours
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)
    query = """
    AzureActivity
    | where TimeGenerated between(datetime({start_time}) .. datetime({end_time}))
    | where ActivityStatusValue == 'Failure'
    | project TimeGenerated, OperationName, Caller, ResourceGroup, ResourceProviderValue, ActivityStatusValue, CorrelationId
    """
    formatted_query = query.format(start_time=start_time.isoformat(), end_time=end_time.isoformat())

    results.append(f"Querying Azure Activity Logs for failures between {start_time} and {end_time}...")
    
    try:
        response = client.query_workspace(workspace_id=workspace_id, query=formatted_query)
        
        if not response.tables:
            results.append("No failures found in the activity logs.")
        else:
            for table in response.tables:
                for row in table.rows:
                    failure_time = row[0]
                    operation = row[1]
                    caller = row[2]
                    resource_group = row[3]
                    resource_provider = row[4]
                    status = row[5]
                    correlation_id = row[6]
                    
                    results.append(f"Failure detected:")
                    results.append(f"  Time: {failure_time}")
                    results.append(f"  Operation: {operation}")
                    results.append(f"  Caller: {caller}")
                    results.append(f"  Resource Group: {resource_group}")
                    results.append(f"  Resource Provider: {resource_provider}")
                    results.append(f"  Status: {status}")
                    results.append(f"  Correlation ID: {correlation_id}")
                    results.append("---")  # Separator between failures
    
    except Exception as e:
        results.append(f"Error querying Azure Activity Logs: {str(e)}")
    
    return results

def main():
    print("Running Azure Activity Log Analyzer...")
    results = []
    
    try:
        azure_config = get_azure_config()
        workspace_id = azure_config.get('log_analytics_workspace_id')
        
        if not workspace_id:
            workspace_id = input("Enter your Log Analytics Workspace ID: ")
            azure_config['log_analytics_workspace_id'] = workspace_id
            with open('azure_config.json', 'w') as f:
                json.dump(azure_config, f)
        
        results = analyze_activity_logs(workspace_id)
        print("Azure Activity Log Analysis complete.")
    
    except Exception as e:
        results.append(f"An error occurred: {str(e)}")
    
    # Print results when run standalone
    for result in results:
        print(result)
    
    return results

if __name__ == "__main__":
    main()
