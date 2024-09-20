import boto3
import configparser
import os
import json

def get_aws_region():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.aws/credentials'))
    
    if 'default' in config and 'region' in config['default']:
        return config['default']['region']
    
    config.read(os.path.expanduser('~/.aws/config'))
    if 'default' in config and 'region' in config['default']:
        return config['default']['region']
    
    return input("Enter your AWS region (e.g., us-west-2): ")

def check_iam_policies():
    region = get_aws_region()
    iam = boto3.client('iam', region_name=region)
    results = []

    try:
        policies = iam.list_policies(Scope='Local')
        for policy in policies['Policies']:
            results.append(f"Policy Name: {policy['PolicyName']}")
            results.append(f"Policy ARN: {policy['Arn']}")

            try:
                policy_details = iam.get_policy_version(PolicyArn=policy['Arn'], VersionId=policy['DefaultVersionId'])
                policy_document = policy_details['PolicyVersion']['Document']

                for statement in policy_document.get('Statement', []):
                    if statement.get('Effect') == 'Allow' and statement.get('Action') == '*':
                        results.append("  WARNING: Policy allows all actions ('*')")
                    if statement.get('Effect') == 'Allow' and statement.get('Resource') == '*':
                        results.append("  WARNING: Policy applies to all resources ('*')")

                results.append("  Policy Summary:")
                for statement in policy_document.get('Statement', []):
                    results.append(f"    Effect: {statement.get('Effect', 'N/A')}")
                    results.append(f"    Action: {statement.get('Action', 'N/A')}")
                    results.append(f"    Resource: {statement.get('Resource', 'N/A')}")

            except iam.exceptions.NoSuchEntityException:
                results.append(f"  Error: Policy version not found for {policy['PolicyName']}")
            except Exception as e:
                results.append(f"  Error analyzing policy {policy['PolicyName']}: {str(e)}")

            results.append("---")

    except Exception as e:
        results.append(f"Error listing policies: {str(e)}")

    return results

def main():
    print("Running AWS IAM Policy Analyzer...")
    results = check_iam_policies()
    for result in results:
        print(result)
    print("IAM Policy Analysis complete.")
    return results

if __name__ == "__main__":
    main()
