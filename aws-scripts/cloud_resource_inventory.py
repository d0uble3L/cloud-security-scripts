import boto3
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

def list_ec2_instances(ec2):
    results = []
    try:
        instances = ec2.describe_instances()
        results.append("EC2 Instances:")
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                results.append(f"  Instance ID: {instance['InstanceId']}, Type: {instance['InstanceType']}, State: {instance['State']['Name']}")
    except Exception as e:
        results.append(f"Error listing EC2 instances: {str(e)}")
    return results

def list_s3_buckets(s3):
    results = []
    try:
        buckets = s3.list_buckets()
        results.append("S3 Buckets:")
        for bucket in buckets['Buckets']:
            results.append(f"  Bucket Name: {bucket['Name']}")
    except Exception as e:
        results.append(f"Error listing S3 buckets: {str(e)}")
    return results

def list_rds_instances(rds):
    results = []
    try:
        instances = rds.describe_db_instances()
        results.append("RDS Instances:")
        for instance in instances['DBInstances']:
            results.append(f"  DB Instance ID: {instance['DBInstanceIdentifier']}, Engine: {instance['Engine']}, Status: {instance['DBInstanceStatus']}")
    except Exception as e:
        results.append(f"Error listing RDS instances: {str(e)}")
    return results

def list_lambda_functions(lambda_client):
    results = []
    try:
        functions = lambda_client.list_functions()
        results.append("Lambda Functions:")
        for function in functions['Functions']:
            results.append(f"  Function Name: {function['FunctionName']}, Runtime: {function['Runtime']}, Last Modified: {function['LastModified']}")
    except Exception as e:
        results.append(f"Error listing Lambda functions: {str(e)}")
    return results

def main():
    print("Running AWS Cloud Resource Inventory...")
    region = get_aws_region()
    results = []

    ec2 = boto3.client('ec2', region_name=region)
    s3 = boto3.client('s3', region_name=region)
    rds = boto3.client('rds', region_name=region)
    lambda_client = boto3.client('lambda', region_name=region)

    results.extend(list_ec2_instances(ec2))
    results.append("") 
    results.extend(list_s3_buckets(s3))
    results.append("")
    results.extend(list_rds_instances(rds))
    results.append("")
    results.extend(list_lambda_functions(lambda_client))

    for result in results:
        print(result)

    print("AWS Cloud Resource Inventory complete.")
    return results

if __name__ == "__main__":
    main()
