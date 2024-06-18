from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

# Default arguments for the DAGs
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the first DAG with its schedule (e.g., daily)
dag1 = DAG(
    "dag1_daily",
    default_args=default_args,
    description="A simple daily DAG",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 6, 1),
    catchup=False,
)

# Define the second DAG with its schedule (e.g., hourly)
dag2 = DAG(
    "dag2_hourly",
    default_args=default_args,
    description="A simple hourly DAG",
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2023, 6, 1),
    catchup=False,
)

# Define tasks for the first DAG
task1_dag1 = DummyOperator(
    task_id="task1_dag1",
    dag=dag1,
)

task2_dag1 = DummyOperator(
    task_id="task2_dag1",
    dag=dag1,
)

task1_dag1 >> task2_dag1

# Define tasks for the second DAG
task1_dag2 = DummyOperator(
    task_id="task1_dag2",
    dag=dag2,
)

task2_dag2 = DummyOperator(
    task_id="task2_dag2",
    dag=dag2,
)

task1_dag2 >> task2_dag2
