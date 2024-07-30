import boto3

def analyze_cloudtrail_logs(start_time, end_time):
    client = boto3.client('cloudtrail')
    events = client.lookup_events(StartTime=start_time, EndTime=end_time)
    for event in events['Events']:
        print(f"Event Name: {event['EventName']}, Source IP: {event['SourceIPAddress']}")

# Example usage
from datetime import datetime, timedelta
now = datetime.utcnow()
analyze_cloudtrail_logs(now - timedelta(days=1), now)
