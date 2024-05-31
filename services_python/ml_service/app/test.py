import mlflow
import pandas as pd
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier as Model
from sklearn.metrics import accuracy_score as Metric
from prefect import flow, task

# from prefect.runtime import flow_run
# parameters = flow_run.get_parameters()

# MLFLOW_HOST = parameters["env"]["MLFLOW_HOST"]
# MLFLOW_PORT = parameters["env"]["MLFLOW_PORT"]
# mlflow.set_tracking_uri(f"http://{MLFLOW_HOST}:{MLFLOW_PORT}")
# mlflow.set_experiment("8a3bd66e-469f-481e-9df3-7b232846f468")


@task
def initialize_environment(MLFLOW_HOST: str, MLFLOW_PORT: str):
    uri = f"http://{MLFLOW_HOST}:{MLFLOW_PORT}"
    mlflow.set_tracking_uri(f"http://{MLFLOW_HOST}:{MLFLOW_PORT}")
    mlflow.set_experiment("8a3bd66e-469f-481e-9df3-7b232846f468")

    pass


@task
def load_data(test_size: int):
    dataset = load_digits()
    df = pd.DataFrame(data=dataset.data, columns=dataset.feature_names)
    df["target"] = dataset.target
    train_df, test_df = train_test_split(df, test_size=test_size / 100, random_state=42)
    X_train = train_df.drop("target", axis=1)
    y_train = train_df["target"]
    X_test = test_df.drop("target", axis=1)
    y_test = test_df["target"]
    return X_train, y_train, X_test, y_test, dataset.target_names


@task
def train_model(X_train, y_train, X_test, y_test):

    # Start a new MLflow run within the task
    with mlflow.start_run(run) as run:
        mlflow.sklearn.autolog()

        model = Model()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        result = Metric(y_test, y_pred)

        # Manually log the metric with the same run
        mlflow.log_metric("testing_accuracy_score", result)

    return run.info.run_id


@task
def register_model(mlflow_run_id):
    # Register a model to MLflow Registry
    register_name = "8a3bd66e-469f-481e-9df3-7b232846f468"
    mv = mlflow.register_model(
        model_uri=f"runs:/{mlflow_run_id}/model",
        name=register_name,
        tags={"task": "Classification"},
    )
    # Add alias for this model (@champion)
    mlflow.MlflowClient().set_registered_model_alias(
        register_name, "champion", mv.version
    )


@flow(name="sklearnflow", log_prints=True)
def sklearnflow(MLFLOW_HOST: str, MLFLOW_PORT: str):
    initialize_environment(MLFLOW_HOST=MLFLOW_HOST, MLFLOW_PORT=MLFLOW_PORT)
    X_train, y_train, X_test, y_test, _ = load_data(test_size=0.2)
    mlflow_run_id = train_model(X_train, y_train, X_test, y_test)
    register_model(mlflow_run_id)


if __name__ == "__main__":
    sklearnflow()
