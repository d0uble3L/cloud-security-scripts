# Cloud Security Scripts

This repository contains Python scripts designed to help with cloud security management. Each script focuses on a different aspect of cloud security and can be customized to fit your needs.

## Get Started

Follow these steps to get started with the Cloud Security Scripts:

1. **Clone the Repository**

   Clone this repository to your local machine using Git:

   ```bash
   git clone https://github.com/your-username/cloud-security-scripts.git
   cd cloud-security-scripts
   ```

2. **Configure AWS Credentials**
   Ensure your AWS credentials are configured. You can set them up using the AWS CLI or by creating a ~/.aws/credentials file with the following content:

   ```plaintext
   [default]
   aws_access_key_id = YOUR_ACCESS_KEY
   aws_secret_access_key = YOUR_SECRET_KEY
   ```

## Prerequisites

- Python 3.x

Install the required Python library using pip:

```bash
pip install -r requirements.txt
```
## Configuration

### AWS Configuration

The scripts will prompt you for AWS credentials if they're not already set up. Alternatively, you can configure them manually:

1. Use the AWS CLI: Run `aws configure`
2. Or create a `~/.aws/credentials` file with the following content:

   ```plaintext
   [default]
   aws_access_key_id = YOUR_ACCESS_KEY
   aws_secret_access_key = YOUR_SECRET_KEY
   region = YOUR_DEFAULT_REGION
   ```

### Azure Configuration

The scripts will prompt you for Azure credentials if they're not already set up. Alternatively, you can configure them manually by creating an `azure_config.json` file in the root directory with the following content:

json
{
"tenant_id": "YOUR_TENANT_ID",
"client_id": "YOUR_CLIENT_ID",
"client_secret": "YOUR_CLIENT_SECRET",
"subscription_id": "YOUR_SUBSCRIPTION_ID",
"region": "YOUR_DEFAULT_REGION"
}

## Available Scripts

### AWS Scripts

1. **Cloud Resource Inventory Scanner** (`aws-scripts/cloud_resource_inventory.py`)
   - Fetches and lists all resources in your AWS account.

2. **IAM Policy Analyzer** (`aws-scripts/iam_policy_analyzer.py`)
   - Reviews IAM policies to identify overly permissive policies.

3. **CloudTrail Log Analyzer** (`aws-scripts/cloudtrail_log_analyzer.py`)
   - Analyzes AWS CloudTrail logs for suspicious activities.

4. **Security Group Auditor** (`aws-scripts/security_group_auditor.py`)
   - Checks AWS security groups for overly permissive rules.

5. **S3 Bucket Access Checker** (`aws-scripts/s3_bucket_access_checker.py`)
   - Checks the access permissions of S3 buckets.

### Azure Scripts

1. **Azure Resource Inventory Scanner** (`azure-scripts/azure_resource_inventory.py`)
   - Fetches and lists all resources in your Azure subscription.

2. **Azure Role Assignment Analyzer** (`azure-scripts/role_assignment_analyzer.py`)
   - Reviews Azure role assignments to identify overly permissive roles.

3. **Azure Activity Log Analyzer** (`azure-scripts/activity_log_analyzer.py`)
   - Analyzes Azure Activity Logs for suspicious activities.

4. **Azure Network Security Group Auditor** (`azure-scripts/nsg_auditor.py`)
   - Checks Azure Network Security Groups (NSGs) for overly permissive rules.

5. **Azure Storage Account Access Checker** (`azure-scripts/storage_account_access_checker.py`)
   - Checks the access permissions of Azure Storage Accounts.

## Using the Analyzer

The `analyze.py` script provides a user-friendly console interface to run multiple security checks:

1. It prompts you to select the cloud environment (AWS, Azure, or both).
2. It checks for existing credentials and prompts you to set them up if needed.
3. It lists available scripts for the selected environment(s) and lets you choose which to run.
4. It executes the selected scripts and provides a summary of the results.

## Outputs available

The script generates two types of output:

1. An HTML report (`cloud_security_analysis.html`) with formatted results and warnings.
2. A CSV file (`cloud_security_analysis.csv`) with all results, including prefixed warnings.

## Contributing

Contributions to improve existing scripts or add new security checks are welcome. Please ensure that any new scripts follow the existing structure and include a `main()` function.

## Security Note

This tool is designed for security auditing by authorized personnel only. Ensure you have permission to perform security checks on the target AWS and Azure environments before using these scripts.
