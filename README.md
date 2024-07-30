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
- `boto3` library for interacting with AWS services

Install the required Python library using pip:

```bash
pip install -r requirements.txt
```

## AWS Scripts

### 1. Cloud Resource Inventory Scanner

Fetches and lists all resources in your cloud account. Useful for creating an inventory of your cloud assets.

**File:** `aws-scripts/cloud_resource_inventory.py`

### 2. IAM Policy Analyzer

Reviews IAM policies to identify overly permissive policies, helping to minimize the risk of privilege escalation.

**File:** `aws-scripts/iam_policy_analyzer.py`

### 3. CloudTrail Log Analyzer

Analyzes AWS CloudTrail logs for suspicious activities, such as unauthorized access or unusual actions.

**File:** `aws-scripts/cloudtrail_log_analyzer.py`

### 4. Security Group Auditor

Checks AWS security groups for overly permissive rules, such as inbound rules that allow traffic from any IP address.

**File:** `aws-scripts/security_group_auditor.py`

### 5. S3 Bucket Access Checker

Checks the access permissions of S3 buckets to ensure they are not publicly accessible or misconfigured.

**File:** `aws-scripts/s3_bucket_access_checker.py`
