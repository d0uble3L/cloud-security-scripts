import boto3
import botocore
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

def check_s3_bucket_permissions():
    results = []
    region = get_aws_region()

    try:
        s3 = boto3.client('s3', region_name=region)
        buckets = s3.list_buckets()
        
        if not buckets['Buckets']:
            results.append("No S3 buckets found in the account.")
            return results

        for bucket in buckets['Buckets']:
            bucket_name = bucket['Name']
            results.append(f"Checking Bucket: {bucket_name}")
            
            try:
                acl = s3.get_bucket_acl(Bucket=bucket_name)
                for grant in acl['Grants']:
                    if 'URI' in grant['Grantee'] and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                        results.append(f"WARNING: Bucket {bucket_name} is publicly accessible")
                        break
                else:
                    results.append(f"Bucket {bucket_name} is not publicly accessible")
                
                try:
                    policy = s3.get_bucket_policy(Bucket=bucket_name)
                    results.append(f"Bucket {bucket_name} has a bucket policy")
                except botocore.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                        results.append(f"Bucket {bucket_name} does not have a bucket policy")
                    else:
                        results.append(f"Error checking bucket policy for {bucket_name}: {str(e)}")
                
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchBucket':
                    results.append(f"Error: Bucket {bucket_name} not found")
                elif e.response['Error']['Code'] == 'AccessDenied':
                    results.append(f"Error: Access denied to bucket {bucket_name}. Please check your permissions.")
                else:
                    results.append(f"Error accessing {bucket_name}: {str(e)}")

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            results.append("Error: Access denied when listing buckets. Please check your AWS credentials and permissions.")
        else:
            results.append(f"Error listing buckets: {str(e)}")
    except Exception as e:
        results.append(f"Unexpected error: {str(e)}")

    return results

def main():
    print("Running S3 Bucket Access Checker...")
    results = check_s3_bucket_permissions()
    for result in results:
        print(result)
    print("S3 Bucket Access Check complete.")
    return results

if __name__ == "__main__":
    main()
