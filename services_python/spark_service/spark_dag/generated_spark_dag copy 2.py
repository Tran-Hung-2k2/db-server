from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.models import Variable

default_args = {
    "owner": "duonghdt",
    "depends_on_past": False,
    "email": ["hoatungduong12@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
dag = DAG(
    dag_display_name="3",
    dag_id="3",
    default_args=default_args,
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["user"],
)

# pyspark_app_home = Variable.get("PYSPARK_APP_HOME")
spark_conf = {
    "spark.hadoop.fs.s3a.access.key": "dPiSZxiiVl7qxZOuOKuI",
    "spark.hadoop.fs.s3a.secret.key": "EdhF2cbYS3VqCYlzB1Ao80jQm4FmPQDfyrWnZRz6",
    "spark.hadoop.fs.s3a.endpoint": "http://172.21.5.32:9000",
    "spark.databricks.delta.retentionDurationCheck.enabled": "false",
    "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
    "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
}

Task1 = SparkSubmitOperator(
    task_id="11",
    conn_id="spark_standalone",
    conf=spark_conf,
    # application=f'{pyspark_app_home}/spark/search_event_ingestor.py',
    application="/home/duonghdt/Desktop/Python/db-server/services_python/spark_service/spark_job/random_job_name.py",
    total_executor_cores=2,
    packages="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,io.delta:delta-spark_2.12:3.1.0,org.apache.hadoop:hadoop-aws:3.3.4",
    executor_cores=2,
    executor_memory="4g",
    driver_memory="1g",
    name="Airflow_Spark",
    dag=dag,
)

Task2 = SparkSubmitOperator(
    task_id="12",
    conn_id="spark_standalone",
    conf=spark_conf,
    # application=f'{pyspark_app_home}/spark/search_event_ingestor.py',
    application="/home/duonghdt/Desktop/Python/db-server/services_python/spark_service/spark_job/random_job_name.py",
    total_executor_cores=2,
    packages="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,io.delta:delta-spark_2.12:3.1.0,org.apache.hadoop:hadoop-aws:3.3.4",
    executor_cores=2,
    executor_memory="4g",
    driver_memory="1g",
    name="Airflow_Spark",
    dag=dag,
)

Task3 = SparkSubmitOperator(
    task_id="13",
    conn_id="spark_standalone",
    conf=spark_conf,
    # application=f'{pyspark_app_home}/spark/search_event_ingestor.py',
    application="/home/duonghdt/Desktop/Python/db-server/services_python/spark_service/spark_job/random_job_name.py",
    total_executor_cores=2,
    packages="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,io.delta:delta-spark_2.12:3.1.0,org.apache.hadoop:hadoop-aws:3.3.4",
    executor_cores=2,
    executor_memory="4g",
    driver_memory="1g",
    name="Airflow_Spark",
    dag=dag,
)

Task4 = SparkSubmitOperator(
    task_id="14",
    conn_id="spark_standalone",
    conf=spark_conf,
    # application=f'{pyspark_app_home}/spark/search_event_ingestor.py',
    application="/home/duonghdt/Desktop/Python/db-server/services_python/spark_service/spark_job/random_job_name.py",
    total_executor_cores=2,
    packages="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,io.delta:delta-spark_2.12:3.1.0,org.apache.hadoop:hadoop-aws:3.3.4",
    executor_cores=2,
    executor_memory="4g",
    driver_memory="1g",
    name="Airflow_Spark",
    dag=dag,
)

Task1 >> Task2 >> Task3 >> Task4
