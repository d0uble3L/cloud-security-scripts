import boto3

def audit_security_groups():
    ec2 = boto3.client('ec2')
    security_groups = ec2.describe_security_groups()
    for sg in security_groups['SecurityGroups']:
        print(f"Security Group ID: {sg['GroupId']}, Name: {sg['GroupName']}")
        for rule in sg['IpPermissions']:
            for ip_range in rule.get('IpRanges', []):
                if ip_range.get('CidrIp') == '0.0.0.0/0':
                    print(f"  Open to the world: {rule}")

audit_security_groups()
