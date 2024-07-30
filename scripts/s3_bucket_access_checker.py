import boto3

def check_s3_bucket_permissions():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        print(f"Bucket Name: {bucket_name}")
        for grant in acl['Grants']:
            if 'AllUsers' in grant['Grantee'].get('URI', ''):
                print(f"  Publicly accessible bucket: {bucket_name}")

check_s3_bucket_permissions()
