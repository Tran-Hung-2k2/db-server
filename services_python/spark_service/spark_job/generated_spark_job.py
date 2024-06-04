
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

import pyspark
from delta import *

builder = (
    pyspark.sql.SparkSession.builder.appName("Spark_job_template") 
)
spark = configure_spark_with_delta_pip(builder).getOrCreate()

minio_bucket = "duonghdt"
dataset = "tracker_data_spark_2c_standalone_template"
kafka_server = "172.21.5.234:9092"
kafka_topic = "Tracker-data"

schema = StructType([
    StructField("MESSAGE_TYPE", StringType()),
    StructField("DEVICE_ID", IntegerType()),
    StructField("IMSI", StringType()),
    StructField("TRACKER_STATE", StringType()),
])

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
    .filter(
        (col("TRACKER_SPEED") > 15) & 
        (col("DEVICE_ID").isin([device1, device2]))
)
    .writeStream
    .format("delta")
    .partitionBy(DEVICE_ID, IMSI)
    .option("checkpointLocation", f"s3a://{minio_bucket}/{dataset}/checkpoint-kafka")
    .start(f"s3a://{minio_bucket}/{dataset}/kafka")
    .awaitTermination()
)