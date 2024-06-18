import requests
import os

LIVY_HOST = os.getenv("LIVY_HOST", "172.21.5.142")
LIVY_PORT = os.getenv("LIVY_PORT", "8089")

import requests


def get_all_active_sessions():
    endpoint = f"http://{LIVY_HOST}:{LIVY_PORT}/sessions"
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_all_idle_sessions():
    endpoint = f"http://{LIVY_HOST}:{LIVY_PORT}/sessions"
    response = requests.get(endpoint)

    if response.status_code == 200:
        sessions = response.json()
        idle_sessions = [
            session["id"]
            for session in sessions["sessions"]
            if session["state"] == "idle"
        ]  # all state is: ['not_started', 'starting', 'idle', 'busy', 'shutting_down', 'error', 'dead', 'killed', 'success']

        return idle_sessions
    else:
        response.raise_for_status()


import requests


def create_new_session(
    session_name,
    driverMemory=1,
    driverCores=1,
    executorMemory=4,
    executorCores=2,
    numExecutors=2,
):
    endpoint = f"http://{LIVY_HOST}:{LIVY_PORT}/sessions"
    headers = {"Content-Type": "application/json"}
    session_body = {
        "kind": "spark",
        "jars": [],
        "pyFiles": [],
        "files": [],
        "driverMemory": f"{driverMemory}g",
        "driverCores": driverCores,
        "executorMemory": f"{executorMemory}g",
        "executorCores": executorCores,
        "numExecutors": numExecutors,
        "name": session_name,
        "conf": {
            "spark.hadoop.fs.s3a.access.key": "dPiSZxiiVl7qxZOuOKuI",
            "spark.hadoop.fs.s3a.secret.key": "EdhF2cbYS3VqCYlzB1Ao80jQm4FmPQDfyrWnZRz6",
            "spark.hadoop.fs.s3a.endpoint": "http://172.21.5.32:9000",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "false",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.databricks.delta.retentionDurationCheck.enabled": "false",
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            # "spark.cores.max": "2",
            "spark.jars.packages": "io.delta:delta-spark_2.12:3.1.0,org.apache.hadoop:hadoop-aws:3.3.4",
        },
        "heartbeatTimeoutInSecond": 60,
        "ttl": "12h",
    }
    response = requests.post(endpoint, json=session_body, headers=headers)

    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()


def get_one_active_session(session_id):
    endpoint = f"http://{LIVY_HOST}:{LIVY_PORT}/sessions/{session_id}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def delete_one_active_session(session_id):
    endpoint = f"http://{LIVY_HOST}:{LIVY_PORT}/sessions/{session_id}"
    response = requests.delete(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_one_active_session_state(session_id):
    endpoint = f"http://{LIVY_HOST}:{LIVY_PORT}/sessions/{session_id}/state"
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_one_active_session_log(session_id, offset=0, max=20):
    endpoint = f"http://{LIVY_HOST}:{LIVY_PORT}/sessions/{session_id}/log"
    params = {"from": offset, "size": max}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def execute_statement(session_id, statement):
    endpoint = f"http://{LIVY_HOST}:{LIVY_PORT}/sessions/{session_id}/statements"
    headers = {"Content-Type": "application/json"}
    statement_body = {"code": statement}
    response = requests.post(endpoint, json=statement_body, headers=headers)

    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()


def get_statement_output(session_id, statement_id):
    endpoint = (
        f"http://{LIVY_HOST}:{LIVY_PORT}/sessions/{session_id}/statements/{statement_id}"
    )
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def delete_one_statement(session_id, statement_id):
    endpoint = f"http://{LIVY_HOST}:{LIVY_PORT}/sessions/{session_id}/statements/{statement_id}/cancel"
    response = requests.post(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def query_sql_from_delta(user_id, dataset_ids: list, query):
    idle_session = get_all_idle_sessions()[0]
    for dataset_id in dataset_ids:
        query = query.replace(dataset_id, f"delta.`s3a://{user_id}/{dataset_id}")
    query = f"spark.sql({query}).toJSON().collect()"
    response = execute_statement(idle_session, query)
    return response
