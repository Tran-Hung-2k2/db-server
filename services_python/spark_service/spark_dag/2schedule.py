from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    "my_scheduled_dag",
    default_args=default_args,
    description="A simple DAG that runs at 3 PM and 5 PM every day",
    schedule_interval="0 15,17 * * *",  # Cron expression for 3 PM and 5 PM
    start_date=datetime(2023, 6, 10),
    catchup=False,  # Disable backfill
)

# Define tasks
start = DummyOperator(
    task_id="start",
    dag=dag,
)

# Example task
dummy_task = DummyOperator(
    task_id="dummy_task",
    dag=dag,
)

# Set task dependencies
start >> dummy_task
