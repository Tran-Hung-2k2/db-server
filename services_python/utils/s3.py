import os
import boto3

# from botocore.client import Config


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
# MINIO_ALLOW_HTTP = os.getenv("MINIO_ALLOW_HTTP", "true")
# MINIO_REGION = os.getenv("MINIO_REGION", "us-east-1")
# MINIO_S3_ALLOW_UNSAFE_RENAME = os.getenv("MINIO_S3_ALLOW_UNSAFE_RENAME", "true")


def save_to_s3(bucket, entry, content):

    # Set up MinIO client
    s3 = boto3.resource(
        "s3",
        endpoint_url=AWS_ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        # config=Config(signature_version="s3v4"),
    )
    # Create the bucket if it doesn't exist
    if not s3.Bucket(bucket) in s3.buckets.all():
        s3.create_bucket(Bucket=bucket)

    # Write the file to MinIO
    s3.Bucket(bucket).put_object(Key=entry, Body=content)

    return
