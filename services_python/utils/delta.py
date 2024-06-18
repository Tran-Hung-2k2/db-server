import os
import json
import duckdb
from minio.error import S3Error
import polars as pl
import pandas as pd
from minio import Minio
from urllib.parse import urlsplit
from deltalake import write_deltalake, DeltaTable
from fastapi import UploadFile, status
from datetime import datetime
from services_python.utils.exception import MyException

MINIO_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY_ID", "xFHb1cqyhEJ8NVY7I8G1")
MINIO_SECRET_ACCESS_KEY = os.getenv(
    "MINIO_SECRET_ACCESS_KEY", "5XdChUr8wLwHuj9YR8wOPLyZoIjhqwa5EsIUxBEC"
)
MINIO_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL", "http://127.0.0.1:9000")
MINIO_ALLOW_HTTP = os.getenv("MINIO_ALLOW_HTTP", "true")
MINIO_REGION = os.getenv("MINIO_REGION", "us-east-1")
MINIO_S3_ALLOW_UNSAFE_RENAME = os.getenv("MINIO_S3_ALLOW_UNSAFE_RENAME", "true")

storage_options = {
    "AWS_ACCESS_KEY_ID": MINIO_ACCESS_KEY_ID,
    "AWS_SECRET_ACCESS_KEY": MINIO_SECRET_ACCESS_KEY,
    "AWS_ENDPOINT_URL": MINIO_ENDPOINT_URL,
    "AWS_ALLOW_HTTP": MINIO_ALLOW_HTTP,
    "AWS_REGION": MINIO_REGION,
    "AWS_S3_ALLOW_UNSAFE_RENAME": MINIO_S3_ALLOW_UNSAFE_RENAME,
}


def create_s3_bucket(bucket_name):
    try:
        endpoint_url_parts = urlsplit(MINIO_ENDPOINT_URL)
        # Initialize Minio client
        minio_client = Minio(
            endpoint_url_parts.netloc,
            access_key=MINIO_ACCESS_KEY_ID,
            secret_key=MINIO_SECRET_ACCESS_KEY,
            secure=False,  # Set to True if your Minio server uses HTTPS
        )

        # Check if the bucket already exists
        if not minio_client.bucket_exists(bucket_name):
            # Create the bucket
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")

    except S3Error as e:
        # Handle Minio-specific errors
        print(f"Minio S3Error: {e}")
        raise e
    except ConnectionRefusedError as e:
        # Handle connection errors
        print(f"Connection Error: {e}")
        raise e
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")
        raise e


def save_data_to_s3_as_delta(user_id, dataset_id, df: pd.DataFrame):
    dataset_path = f"s3://{user_id}/{dataset_id}"

    # Create S3 bucket with user_id as the bucket name
    create_s3_bucket(user_id)

    write_deltalake(
        dataset_path,
        df,
        engine="pyarrow",
        storage_options=storage_options,
        mode="overwrite",
    )

    return


def save_file_to_s3_as_delta(filepath: str, user_id: str, dataset_id: int):
    try:
        if filepath:
            file_extension = filepath.rsplit(".", 1)[1].lower()
            if file_extension == "csv":
                # Đọc dữ liệu từ file CSV bằng Polars
                df = pl.read_csv(
                    filepath,
                    null_values=["NULL"],
                    infer_schema_length=10000,
                    ignore_errors=True,
                )
            else:
                raise MyException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Định dạng file không được hỗ trợ.",
                )

            try:
                save_data_to_s3_as_delta(user_id, dataset_id, df.to_pandas())
            except Exception as e:
                raise MyException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"{e}",
                )

            return

        raise MyException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không tìm thấy file.",
        )

    except MyException as e:
        # Handle MyException specifically
        print(f"MyException: {e.detail}")
        raise e
    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {e}")
        raise MyException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )


def query_sql_from_delta_table(
    user_id,
    dataset_id,
    dataset_name,
    sql_cmd: str,
    skip: str,
    limit: str,
    #   , version = 0
):
    # Connect to DuckDB in-memory database
    con = duckdb.connect()
    delta_table_path = f"s3://{user_id}/{dataset_id}"

    dataset = DeltaTable(
        table_uri=delta_table_path,
        storage_options=storage_options,
        # version=version,
    ).to_pyarrow_table()
    con.register(dataset_name, dataset)
    # Count the total number of records without skip and limit
    total_records = con.execute(f"SELECT COUNT(*) FROM ({sql_cmd})").fetchone()[0]

    result = con.execute(f"{sql_cmd} OFFSET {skip} LIMIT {limit};").fetchdf()

    schema = dataset.schema

    # Convert schema to dictionary
    schema_dict = {field.name: str(field.type) for field in schema}

    con.close()

    return {
        "schema": schema_dict,
        "result": json.loads(result.to_json(orient="records")),
    }, total_records


def read_delta_from_s3_as_pandas(
    user_id, dataset_id, input: list = [], op: list = [], output: list = []
):
    valid_ops = ["=", "!=", "==", "in", "not in", "<", ">", "<=", ">="]
    if len(input) != len(op) or len(input) != len(output):
        raise ValueError("Lengths of input, op, and output lists must be equal.")

    delta_table_path = f"s3://{user_id}/{dataset_id}"
    dataset = DeltaTable(
        table_uri=delta_table_path,
        storage_options=storage_options,
    )
    if input:
        filter_condition = []
        for i in range(len(input)):
            if op[i] not in valid_ops:
                raise ValueError(f"Invalid operator '{op[i]}' at index {i}.")
            condition = (input[i], op[i], output[i])
            filter_condition.append(condition)
        df = dataset.load_as_version(filter=filter_condition).to_pandas()
        return df
    else:
        df = dataset.load_as_version().to_pandas()
        return df


def read_delta_from_s3_as_pyarrow(
    user_id, dataset_id, input: list = [], op: list = [], output: list = []
):
    valid_ops = ["=", "!=", "==", "in", "not in", "<", ">", "<=", ">="]
    if len(input) != len(op) or len(input) != len(output):
        raise ValueError("Lengths of input, op, and output lists must be equal.")

    delta_table_path = f"s3://{user_id}/{dataset_id}"
    dataset = DeltaTable(
        table_uri=delta_table_path,
        storage_options=storage_options,
    )

    if input:
        filter_condition = []
        for i in range(len(input)):
            if op[i] not in valid_ops:
                raise ValueError(f"Invalid operator '{op[i]}' at index {i}.")
            condition = (input[i], op[i], output[i])
            filter_condition.append(condition)
        df = dataset.load_as_version(filter=filter_condition).to_pyarrow_dataset()
        return df
    else:
        df = dataset.load_as_version().to_pyarrow_dataset()
        return df


def delete_folder_from_s3(user_id: str, dataset_id: str):
    try:
        endpoint_url_parts = urlsplit(MINIO_ENDPOINT_URL)
        # Initialize Minio client
        minio_client = Minio(
            endpoint_url_parts.netloc,
            access_key="Crl6bcvsiKQKqh9IuDDy",
            secret_key="NCpGrwkQHeRFClrwe4vpDpciappmCSElJoOKsqaK",
            secure=False,
        )

        objects = minio_client.list_objects(
            bucket_name=user_id, prefix=dataset_id, recursive=True
        )
        for obj in objects:
            minio_client.remove_object(str(user_id), str(obj.object_name))

    except S3Error as e:
        # Handle Minio-specific errors
        print(f"Minio S3Error: {e}")
        raise e
    except ConnectionRefusedError as e:
        # Handle connection errors
        print(f"Connection Error: {e}")
        raise e
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")
        raise e
