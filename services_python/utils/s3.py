import os
import boto3

# from botocore.client import Config


MINIO_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY_ID")
MINIO_SECRET_ACCESS_KEY = os.getenv("MINIO_SECRET_ACCESS_KEY")
MINIO_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL")
MINIO_ALLOW_HTTP = os.getenv("MINIO_ALLOW_HTTP", "true")
MINIO_REGION = os.getenv("MINIO_REGION", "us-east-1")
MINIO_S3_ALLOW_UNSAFE_RENAME = os.getenv("MINIO_S3_ALLOW_UNSAFE_RENAME", "true")


def save_to_s3(user_id, file_name, content):

    # Set up MinIO client
    s3 = boto3.resource(
        "s3",
        endpoint_url=MINIO_ENDPOINT_URL,
        aws_access_key_id=MINIO_ACCESS_KEY_ID,
        aws_secret_access_key=MINIO_SECRET_ACCESS_KEY,
        # config=Config(signature_version="s3v4"),
    )
    # Create the bucket if it doesn't exist
    if not s3.Bucket(user_id) in s3.buckets.all():
        s3.create_bucket(Bucket=user_id)

    # Write the file to MinIO
    s3.Bucket(user_id).put_object(Key=file_name, Body=content)

    return
