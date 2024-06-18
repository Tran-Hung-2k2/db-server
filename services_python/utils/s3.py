import os
import boto3
from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")


def save_to_s3(bucket, entry, content):
    """
    Save a file to the specified S3 (or MinIO) bucket.

    :param bucket: The name of the bucket.
    :param entry: The key under which the object is to be stored.
    :param content: The content to be stored.
    """
    try:
        # Set up S3/MinIO client
        s3 = boto3.resource(
            "s3",
            endpoint_url=AWS_ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        # Create the bucket if it doesn't exist
        if not s3.Bucket(bucket) in s3.buckets.all():
            s3.create_bucket(Bucket=bucket)

        # Write the file to S3/MinIO
        s3.Bucket(bucket).put_object(Key=entry, Body=content)

    except ClientError as e:
        raise e


def list_from_s3(bucket, entry):
    """
    List objects under a folder path in the specified S3 bucket.

    :param bucket: The name of the S3 bucket.
    :param entry: The folder path (prefix) to list objects under.
    :return: A list of dictionaries containing object keys and sizes under the folder path.
    """
    try:
        # Set up S3/MinIO client
        s3 = boto3.client(
            "s3",
            endpoint_url=AWS_ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        # List objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket, Prefix=entry)
        # Extract object keys and sizes
        return response["Contents"]

    except ClientError as e:
        raise e


def read_from_s3(bucket, key):
    """
    Read the content of a file from the specified S3 (or MinIO) bucket.

    :param bucket: The name of the bucket.
    :param file_key: The key of the file.
    :return: The content of the file.
    """
    try:
        # Set up S3/MinIO client
        s3 = boto3.client(
            "s3",
            endpoint_url=AWS_ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        # Get the object from S3/MinIO
        response = s3.get_object(Bucket=bucket, Key=key)

        # Read and return the content
        content = response["Body"].read()
        return content

    except ClientError as e:
        raise e
