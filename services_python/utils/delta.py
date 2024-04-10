# import os
# import json
# import duckdb
# import psycopg2
# import pandas as pd
# from minio import Minio
# from urllib.parse import urlsplit
# from deltalake import write_deltalake, DeltaTable
# from fastapi import UploadFile, status

# from services_python.utils.exception import MyException

# MINIO_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY_ID", "xFHb1cqyhEJ8NVY7I8G1")
# MINIO_SECRET_ACCESS_KEY = os.getenv(
#     "MINIO_SECRET_ACCESS_KEY", "5XdChUr8wLwHuj9YR8wOPLyZoIjhqwa5EsIUxBEC"
# )
# MINIO_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL", "http://127.0.0.1:9000")
# MINIO_ALLOW_HTTP = os.getenv("MINIO_ALLOW_HTTP", "true")
# MINIO_REGION = os.getenv("MINIO_REGION", "us-east-1")
# MINIO_S3_ALLOW_UNSAFE_RENAME = os.getenv("MINIO_S3_ALLOW_UNSAFE_RENAME", "true")

# storage_options = {
#     "AWS_ACCESS_KEY_ID": MINIO_ACCESS_KEY_ID,
#     "AWS_SECRET_ACCESS_KEY": MINIO_SECRET_ACCESS_KEY,
#     "AWS_ENDPOINT_URL": MINIO_ENDPOINT_URL,
#     "AWS_ALLOW_HTTP": MINIO_ALLOW_HTTP,
#     "AWS_REGION": MINIO_REGION,
#     "AWS_S3_ALLOW_UNSAFE_RENAME": MINIO_S3_ALLOW_UNSAFE_RENAME,
# }


# def create_s3_bucket(bucket_name):
#     endpoint_url_parts = urlsplit(MINIO_ENDPOINT_URL)
#     # Initialize Minio client
#     minio_client = Minio(
#         endpoint_url_parts.netloc,
#         access_key=MINIO_ACCESS_KEY_ID,
#         secret_key=MINIO_SECRET_ACCESS_KEY,
#         secure=False,  # Set to True if your Minio server uses HTTPS
#     )

#     # Check if the bucket already exists
#     if not minio_client.bucket_exists(bucket_name):
#         # Create the bucket
#         minio_client.make_bucket(bucket_name)
#         print(f"Bucket '{bucket_name}' created successfully.")
#     else:
#         print(f"Bucket '{bucket_name}' already exists.")


# def save_data_to_s3_as_delta(user_id, dataset_id, df: pd.DataFrame):
#     dataset_path = f"s3://{user_id}/{dataset_id}"

#     # Create S3 bucket with user_id as the bucket name
#     create_s3_bucket(user_id)

#     write_deltalake(
#         dataset_path,
#         df,
#         engine="pyarrow",
#         storage_options=storage_options,
#         mode="overwrite",
#     )

#     return


# def save_file_to_s3_as_delta(file_data: UploadFile, user_id: str, dataset_id: int):
#     if file_data:
#         file_extension = file_data.filename.rsplit(".", 1)[1].lower()
#         if file_extension == "csv":
#             df = pd.read_csv(file_data.file)
#             print(df)
#         elif file_extension in {"xlsx", "xls"}:
#             df = pd.read_excel(file_data.file)
#         else:
#             raise MyException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Định dạng file không được hỗ trợ.",
#             )

#         save_data_to_s3_as_delta(user_id, dataset_id, df)

#         return

#     raise MyException(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         detail="Có lỗi xảy ra, vui lòng thử lại sau.",
#     )


# def query_sql_from_delta_table(
#     user_id,
#     dataset_id,
#     dataset_name,
#     sql_cmd: str,
#     skip: str,
#     limit: str,
#     #   , version = 0
# ):
#     # Connect to DuckDB in-memory database
#     con = duckdb.connect()
#     delta_table_path = f"s3://{user_id}/{dataset_id}"

#     dt = DeltaTable(
#         table_uri=delta_table_path,
#         storage_options=storage_options,
#         # version=version,
#     ).to_pyarrow_dataset()
#     con.register(dataset_name, dt)
#     # Count the total number of records without skip and limit
#     total_records = con.execute(f"SELECT COUNT(*) FROM ({sql_cmd})").fetchone()[0]

#     result = con.execute(f"{sql_cmd} OFFSET {skip} LIMIT {limit};").fetchdf()

#     schema = dt.schema

#     # Convert schema to dictionary
#     schema_dict = {field.name: str(field.type) for field in schema}

#     con.close()

#     return {
#         "schema": schema_dict,
#         "result": json.loads(result.to_json(orient="records")),
#     }, total_records
