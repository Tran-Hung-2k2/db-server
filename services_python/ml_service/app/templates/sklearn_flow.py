SKLEARN_FLOW = """
import mlflow
import pandas as pd
import os
from sklearn.datasets import {{ dataset }}
from sklearn.model_selection import train_test_split
from sklearn.{{ lib }} import {{ model }} as Model
from sklearn.metrics import {{ metric }} as Metric
from prefect import flow, task


MLFLOW_HOST = os.getenv("MLFLOW_HOST")
MLFLOW_PORT = os.getenv("MLFLOW_PORT")
mlflow.set_tracking_uri(f"http://{MLFLOW_HOST}:{MLFLOW_PORT}")
mlflow.set_experiment("{{ name }}")

import psycopg2
from psycopg2 import sql

conn_params = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT")
}

@task(
    name="Load dataset", 
    description="Load dataset and split into train and test sets", 
    log_prints=True,
)
def load_data(test_size: int):        
    dataset = {{ dataset }}()
    df = pd.DataFrame(data=dataset.data, columns=dataset.feature_names)
    df["target"] = dataset.target
    train_df, test_df = train_test_split(df, test_size=test_size/100, random_state=42)
    X_train = train_df.drop("target", axis=1)
    y_train = train_df["target"]
    X_test = test_df.drop("target", axis=1)
    y_test = test_df["target"]
    print("Dataset size: ", df.shape[0])
    print("Train size: ", train_df.shape[0])
    print("Test size: ", test_df.shape[0])
    return X_train, y_train, X_test, y_test, dataset.target_names

@task(
    name="Train AI/ML model", 
    description="Train a model using the training data and log the result to MLflow", 
    log_prints=True,
)
def train_model(run_name, X_train, y_train, X_test, y_test):    

    # Start a new MLflow run within the task
    with mlflow.start_run(run_name=run_name) as run:
        mlflow.sklearn.autolog()
        
        model = Model()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        result = Metric(y_test, y_pred)

        # Manually log the metric with the same run
        mlflow.log_metric("testing_{{ metric }}", result)

    return run.info.run_id

@task(
    name="Register trained model", 
    description="Register the trained model to MLflow Registry and set an alias as 'champion'", 
    log_prints=True,
)
def register_model(run_id):
    # Register a model to MLflow Registry
    register_name = "{{ name }}"
    mv = mlflow.register_model(
        model_uri=f"runs:/{run_id}/model", 
        name=register_name,
        tags={"task":"{{ task }}"}
    )
    # Add alias for this model (@champion)
    mlflow.MlflowClient().set_registered_model_alias(register_name, 'champion', mv.version)
    
@task
def commit_run(run_name, run_id):
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE runs SET run_id = '{run_id}' WHERE id = '{run_name}'")
    conn.commit()
    cursor.close()
    conn.close()

@flow(name="{{ flow }}", log_prints=True)
def {{ flow }}(run_name: str):
    X_train, y_train, X_test, y_test, _ = load_data(test_size=20)
    run_id = train_model(run_name, X_train, y_train, X_test, y_test)
    register_model(run_id)
    commit_run(run_name, run_id)
    
if __name__ == "__main__":
    {{ flow }}()
"""
