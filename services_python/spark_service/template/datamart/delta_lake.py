import os
import inspect

MINIO_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY_ID", "rUsDgAVuMUyHE0kaNgjI")
MINIO_SECRET_ACCESS_KEY = os.getenv(
    "MINIO_SECRET_ACCESS_KEY", "QfcyE72ETAHUjr9yMhZfFnM2Gh2TrJv93sfpfYGD"
)
MINIO_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL", "http://127.0.0.1:9000")


def check_config_keys(config):
    required_keys = ["USER_ID", "DATA_MART_ID", "MODE"]

    for key in required_keys:
        if key not in config:
            return False
    return True


def get_string(config):
    code = inspect.cleandoc(
        f"""
        from deltalake.writer import write_deltalake
        from datetime import datetime

        def export_data(df, *args, **kwargs):
            storage_options = {{
                'MINIO_ACCESS_KEY_ID': '{MINIO_ACCESS_KEY_ID}',
                'MINIO_SECRET_ACCESS_KEY': '{MINIO_SECRET_ACCESS_KEY}',
                'MINIO_ENDPOINT_URL': '{MINIO_ENDPOINT_URL}',
                'MINIO_ALLOW_HTTP': 'true',
                'MINIO_REGION': 'us-east-1',
                'MINIO_S3_ALLOW_UNSAFE_RENAME': 'true',
            }}
            uri = f's3://{config['USER_ID']}/{config['DATA_MART_ID']}'
            write_deltalake(
                uri,
                data=df,
                mode='{config['MODE']}',
                overwrite_schema=False,
                storage_options=storage_options,
            )
    """
    )
    return code
