from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from deltalake import DeltaTable, write_deltalake
import pandas as pd

import duckdb
import psycopg2
from psycopg2 import OperationalError


app = Flask(__name__)


UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

ALLOWED_EXTENSIONS = {"txt", "csv", "xlsx", "xls"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


import string
import random


def get_dataset_id(user_id, username_length=8, dataset_name_length=10):
    random_user_id = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=username_length)
    )
    random_dataset_id = "".join(
        random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits,
            k=dataset_name_length,
        )
    )
    return random_dataset_id
    # return "duonghdt","test_dataset"


from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            sslmode=os.getenv("DB_SSLMODE", "require"),
        )
        return conn
    except OperationalError as e:
        print(f"Error: {e}")
        return None


def get_datasource_info(datasource_id):
    pass


import psycopg2
from psycopg2 import OperationalError
from pymongo import MongoClient
from minio import Minio


def get_datasource_connection(datasource_info):
    try:
        if datasource_info["type"] == "postgresql":
            # Kết nối đến PostgreSQL
            conn = psycopg2.connect(
                host=datasource_info["host"],
                database=datasource_info["database"],
                user=datasource_info["user"],
                password=datasource_info["password"],
                port=datasource_info.get("port", "5432"),
            )
            return conn
        elif datasource_info["type"] == "mongodb":
            # Kết nối đến MongoDB
            client = MongoClient(
                host=datasource_info["host"],
                port=int(datasource_info.get("port", "27017")),
                username=datasource_info.get("user", None),
                password=datasource_info.get("password", None),
            )
            db = client[datasource_info["database"]]
            return db
        elif datasource_info["type"] == "minio":
            # Kết nối đến MinIO
            client = Minio(
                datasource_info["host"],
                access_key=datasource_info.get("access_key", None),
                secret_key=datasource_info.get("secret_key", None),
                secure=datasource_info.get("secure", True),
            )
            return client
        else:
            print("Unsupported datasource", datasource_info["type"])
            return None
    except OperationalError as e:
        print(f"Error: {e}")
        return None


def save_to_s3_as_delta(delta_table_path, df):
    minio_endpoint = "http://10.16.2.211:9000"
    minio_access_key = "KumhEHzLPPuXY0gIGfh8"
    minio_secret_key = "xalF8y041c6Z60XwEuRJajVPUR5NyhF5cOVxN1vo"

    storage_options = {
        "AWS_ACCESS_KEY_ID": minio_access_key,
        "AWS_SECRET_ACCESS_KEY": minio_secret_key,
        "AWS_ENDPOINT_URL": minio_endpoint,
        "AWS_ALLOW_HTTP": "true",
        "AWS_REGION": "us-east-1",
        "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
    }
    write_deltalake(
        delta_table_path,
        df,
        engine="rust",
        storage_options=storage_options,
        overwrite_schema=True,
    )
    return True


def read_from_s3_as_arrow(delta_table_path, version):
    minio_endpoint = "http://10.16.2.211:9000"
    minio_access_key = "KumhEHzLPPuXY0gIGfh8"
    minio_secret_key = "xalF8y041c6Z60XwEuRJajVPUR5NyhF5cOVxN1vo"

    storage_options = {
        "AWS_ACCESS_KEY_ID": minio_access_key,
        "AWS_SECRET_ACCESS_KEY": minio_secret_key,
        "AWS_ENDPOINT_URL": minio_endpoint,
        "AWS_ALLOW_HTTP": "true",
        "AWS_REGION": "us-east-1",
        "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
    }
    df = DeltaTable(
        delta_table_path=delta_table_path,
        storage_options=storage_options,
        version=version,
    ).to_pyarrow_dataset()
    return df


# POST BODY
# {
#     "file": "",
#     "user_id": "asfhbasndjkas"
# }


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    if "user_id" not in request.form:
        return jsonify({"error": "No user_id provided"})

    file = request.files["file"]
    user_id = request.form["user_id"]
    dataset_id = get_dataset_id(user_id)

    if file.filename == "":
        return jsonify({"error": "No selected file"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        file_extension = filename.rsplit(".", 1)[1].lower()
        if file_extension == "csv":
            df = pd.read_csv(file_path)
        elif file_extension in {"xlsx", "xls"}:
            df = pd.read_excel(file_path)
        else:
            return jsonify({"error": "Unsupported file format"})

        delta_table_path = f"s3://{user_id}/{dataset_id}"
        # delta_table_path = f"s3://duonghdt/dataset"
        save_to_s3_as_delta(delta_table_path=delta_table_path, df=df)
        os.remove(file_path)
        return jsonify({"message": "File uploaded successfully"})

    return jsonify({"error": "Invalid file type"})


# POST BODY
# {
#     "sql_command": "select * from dataset",
#     "user_id": "asfhbasndjkas",
#     "datasource_id": "asfhbasndjkas,
#     "page_num": 1,
#     "page_size": 10
# }


@app.route("/postgres", methods=["POST"])
def postgres():
    json_data = request.get_json()

    # Validate required fields
    required_fields = [
        "sql_command",
        "page_num",
        "page_size",
        "user_id",
        "datasource_id",
    ]
    for field in required_fields:
        if field not in json_data:
            return jsonify({"error": f"Missing {field} field"}), 400

    user_id = json_data["user_id"]
    datasource_id = json_data["datasource_id"]
    sql_command = json_data["sql_command"]
    page_num = json_data["page_num"]
    page_size = json_data["page_size"]
    offset = (page_num - 1) * page_size
    limit = page_size
    sql_command = f"{sql_command} OFFSET {offset} LIMIT {limit}"
    print(sql_command)

    try:
        # Connect to DuckDB in-memory database
        datasource_info = get_datasource_info(datasource_id=datasource_id)
        conn = get_datasource_connection(datasource_info=datasource_info)
        result = pd.read_sql_query(sql_command, conn)
        dataset_id = get_dataset_id(user_id)
        delta_table_path = f"s3://{user_id}/{dataset_id}"
        save_to_s3_as_delta(delta_table_path=delta_table_path, df=result)
        conn.close()
        return jsonify({"result": result.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# POST BODY
# {
#     "sql_command": "select * from dataset",
#     "user_id": "asfhbasndjkas"
#     "dataset_id": "asfhbasndjkas",
#     "page_num": 1,
#     "page_size": 10
# }


@app.route("/query", methods=["POST"])
def query_sql():
    json_data = request.get_json()

    # Validate required fields
    required_fields = [
        "sql_command",
        "page_num",
        "page_size",
        "user_id",
        "dataset_id",
        "version",
    ]
    for field in required_fields:
        if field not in json_data:
            return jsonify({"error": f"Missing {field} field"}), 400

    user_id = json_data["user_id"]
    dataset_id = json_data["dataset_id"]
    version = json_data["version"]
    sql_command = json_data["sql_command"]
    page_num = json_data["page_num"]
    page_size = json_data["page_size"]
    offset = (page_num - 1) * page_size
    limit = page_size
    sql_command = f"{sql_command} OFFSET {offset} LIMIT {limit}"
    print(sql_command)

    try:
        # Connect to DuckDB in-memory database
        con = duckdb.connect()
        delta_table_path = f"s3://{user_id}/{dataset_id}"
        dt = read_from_s3_as_arrow(delta_table_path=delta_table_path, version=version)
        result = con.execute(sql_command).fetchdf()

        save_to_s3_as_delta(delta_table_path=delta_table_path, df=result)
        con.close()

        return jsonify({"result": result.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7879, debug=True)
