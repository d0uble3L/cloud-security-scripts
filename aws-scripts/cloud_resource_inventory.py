import boto3

def list_ec2_instances():
    ec2 = boto3.client('ec2')
    instances = ec2.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']}, Type: {instance['InstanceType']}, State: {instance['State']['Name']}")

list_ec2_instances()
