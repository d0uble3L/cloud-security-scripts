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

def audit_security_groups():
    region = get_aws_region()
    ec2 = boto3.client('ec2', region_name=region)
    security_groups = ec2.describe_security_groups()
    
    results = []
    for sg in security_groups['SecurityGroups']:
        sg_info = f"Security Group ID: {sg['GroupId']}, Name: {sg['GroupName']}"
        results.append(sg_info)
        for rule in sg['IpPermissions']:
            for ip_range in rule.get('IpRanges', []):
                if ip_range.get('CidrIp') == '0.0.0.0/0':
                    open_rule = f"  Open to the world: {rule}"
                    results.append(open_rule)
    
    return results

def main():
    print("Running AWS Security Group Auditor...")
    results = audit_security_groups()
    print("AWS Security Group Audit complete.")
    return results

if __name__ == "__main__":
    main()
