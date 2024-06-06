import inspect


def check_config_keys(config):
    required_keys = [
        'SCHEMA',
        'USER_ID',
        'DATASET_ID',
        'KAFKA_SERVER',
        'KAFKA_TOPIC'
    ]

    allowed_types = {
        "StringType",
        "IntegerType",
        "DoubleType",
        "FloatType",
        "LongType",
        "ShortType",
        "BooleanType",
        "ByteType",
        "DateType",
        "DecimalType"
    }

    for key in required_keys:
        if key not in config:
            print(f"Config missing keys:{key}")
            return False

    for field_type in config['SCHEMA'].values():
        if field_type not in allowed_types:
            print(f"Schema type contain invalid type:{field_type}")
            return False

    return True


def get_string(config):
    code = inspect.cleandoc(f"""
import pyspark
from delta import *

builder = (
    pyspark.sql.SparkSession.builder.appName("Spark_job_template") 
)
spark = configure_spark_with_delta_pip(builder).getOrCreate()

from pyspark.sql.types import StructType, StructField, StringType
schema="{config['SCHEMA']}"
minio_bucket = "{config['USER_ID']}"
dataset = "{config['DATASET_ID']}"
kafka_server = "{config['KAFKA_SERVER']}"
kafka_topic = "{config['KAFKA_TOPIC']}"

fields = []
type_mapping = {{
    "StringType": StringType(),
    "IntegerType": IntegerType(),
    "DoubleType": DoubleType(),
    "FloatType": FloatType(),
    "LongType": LongType(),
    "ShortType": ShortType(),
    "BooleanType": BooleanType(),
    "ByteType": ByteType(),
    "DateType": DateType(),
    "DecimalType": DecimalType(),
}}
for field_name, field_type in schema.items():
    if field_type in type_mapping:
        fields.append(StructField(field_name, type_mapping[field_type]))
schema = StructType(fields)


from pyspark.sql.functions import from_json
df = (
  spark.readStream 
  .format("kafka") 
  .option("kafka.bootstrap.servers", kafka_server) 
  .option("subscribe", kafka_topic) 
  .option("failOnDataLoss","false")
  .load()
  .selectExpr("CAST(value AS STRING)")
  .select(from_json("value", schema).alias("data"))
  .select("data.*")
  .writeStream
  .format("delta")
  .option("checkpointLocation", f"s3a://{{minio_bucket}}/{{dataset}}/checkpoint-kafka")
  .start(f"s3a://{{minio_bucket}}/{{dataset}}/kafka")
  .awaitTermination()
)
""")
    return code

def get_file(config,file_path):
    code = get_string(config)
    with open(file_path, "w") as file:
        file.write(code)


def main():
    config = {
        'SCHEMA': {
            "MESSAGE_TYPE": "StringType",
            "DEVICE_ID": "IntegerType",
            "IMSI": "StringType",
            "TRACKER_STATE": "StringType"
        },
        'USER_ID': 'duonghdt',
        'DATASET_ID': 'tracker_data_spark_2c_standalone_template',
        'KAFKA_SERVER': '172.21.5.234:9092',
        'KAFKA_TOPIC': 'Tracker-data'
    }

    file_path = "spark_job_template.py"

    if check_config_keys(config):
        get_file(config, file_path)
    else:
        print("Configuration validation failed. Please check your configuration.")


if __name__ == "__main__":
    main()