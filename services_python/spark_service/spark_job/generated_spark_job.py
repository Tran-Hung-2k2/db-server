import pyspark
from delta import *

builder = (
    pyspark.sql.SparkSession.builder.appName("Spark_job_template") 
)
spark = configure_spark_with_delta_pip(builder).getOrCreate()

from pyspark.sql.types import *
schema="{'MESSAGE_TYPE': 'StringType', 'DEVICE_ID': 'IntegerType', 'IMSI': 'StringType', 'TRACKER_STATE': 'StringType'}"
minio_bucket = "duonghdt"
dataset = "tracker_data_spark_2c_standalone_template"
kafka_server = "172.21.5.234:9092"
kafka_topic = "Tracker-data"

fields = []
type_mapping = {
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
}
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
  .option("checkpointLocation", f"s3a://{minio_bucket}/{dataset}/checkpoint-kafka")
  .start(f"s3a://{minio_bucket}/{dataset}/kafka")
  .awaitTermination()
)