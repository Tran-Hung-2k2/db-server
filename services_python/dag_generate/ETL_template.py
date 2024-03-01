import json
from datetime import timedelta
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import pandas as pd
from ProcessingModule.Controller.process_api import ProcessApi
from deltalake import DeltaTable, write_deltalake
import os
from minio.error import S3Error




minio_endpoint = 'http://10.16.2.211:9000'
minio_access_key = 'KumhEHzLPPuXY0gIGfh8'
minio_secret_key = 'xalF8y041c6Z60XwEuRJajVPUR5NyhF5cOVxN1vo'
# bucket_name = 'mybucket'

storage_options = {
    "AWS_ACCESS_KEY_ID": minio_access_key, 
    "AWS_SECRET_ACCESS_KEY": minio_secret_key,
    "AWS_ENDPOINT_URL": minio_endpoint,
    "AWS_ALLOW_HTTP": "true", 
    "AWS_REGION": 'us-east-1',
    "AWS_S3_ALLOW_UNSAFE_RENAME" : "true",
}


@dag(         
    "ETL_TEMPLATE_CLUSTER",                      
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        "schedule_interval" : None,
        "start_date" : days_ago(2),
        "provide_context" : True
    },
    description="DAG receive parameter in cluster mode",

    tags=["test"],
)

# need username,dataset,version
def taskflow_dag(**context):
    @task()
    def extract(**context) -> pd.DataFrame:
        extract_conf=context['dag_run'].conf['extract_conf']
        delta_table_path = f"s3://{username}/{dataset}"
        df = DeltaTable(delta_table_path, version=version, storage_options=storage_options).to_pandas()
        return df

    @task()
    def transform(df: pd.DataFrame,**context) -> pd.DataFrame:
        transform_conf=context['dag_run'].conf['transform_conf']
        process_api = ProcessApi()
        for data in transform_conf:
            process_api.set_api(data)
            df=process_api.processor.process(df)
        return df
    
    @task()
    def load(df: pd.DataFrame,**context) -> bool:
        load_conf=context['dag_run'].conf['extract_conf']
        delta_table_path = f"s3://{username}/{dataset}"
        write_deltalake(delta_table_path, df, mode="append",engine="rust")
    
        return True

    input_data = extract()
    transform_data = transform(input_data)
    load(transform_data)


td = taskflow_dag()