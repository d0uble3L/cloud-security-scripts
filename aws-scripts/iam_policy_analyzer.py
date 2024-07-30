import boto3

def check_iam_policies():
    iam = boto3.client('iam')
    policies = iam.list_policies(Scope='Local')
    for policy in policies['Policies']:
        print(f"Policy Name: {policy['PolicyName']}")
        policy_details = iam.get_policy_version(PolicyArn=policy['Arn'], VersionId=policy['DefaultVersionId'])
        print(f"Policy Document: {policy_details['PolicyVersion']['Document']}")

check_iam_policies()
