import boto3
from datetime import datetime, timedelta
import configparser
import os

def get_aws_region():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.aws/credentials'))
    
    if 'default' in config and 'region' in config['default']:
        return config['default']['region']
    
    config.read(os.path.expanduser('~/.aws/config'))
    if 'default' in config and 'region' in config['default']:
        return config['default']['region']
    
    return input("Enter your AWS region (e.g., us-west-2): ")

def analyze_cloudtrail_logs(start_time, end_time):
    region = get_aws_region()
    client = boto3.client('cloudtrail', region_name=region)
    results = []
    
    try:
        events = client.lookup_events(StartTime=start_time, EndTime=end_time)
        results.append(f"Analyzing CloudTrail logs from {start_time} to {end_time}")
        
        if not events['Events']:
            results.append("No events found in the specified time range.")
        else:
            for event in events['Events']:
                event_time = event['EventTime'].strftime('%Y-%m-%d %H:%M:%S')
                results.append(f"Event Time: {event_time}")
                results.append(f"Event Name: {event['EventName']}")
                results.append(f"Source IP: {event['SourceIPAddress']}")
                results.append(f"User Name: {event.get('Username', 'N/A')}")
                results.append(f"Event Source: {event.get('EventSource', 'N/A')}")
                
                if event['EventName'] in ['ConsoleLogin', 'AssumeRole', 'CreateAccessKey', 'DeleteAccessKey']:
                    results.append("  WARNING: Potentially sensitive action detected")
                
                results.append("---")
        
    except Exception as e:
        results.append(f"Error analyzing CloudTrail logs: {str(e)}")
    
    return results

def main():
    print("Running CloudTrail Log Analyzer...")
    now = datetime.utcnow()
    start_time = now - timedelta(days=1)
    results = analyze_cloudtrail_logs(start_time, now)
    for result in results:
        print(result)
    print("CloudTrail Log Analysis complete.")
    return results

if __name__ == "__main__":
    main()
