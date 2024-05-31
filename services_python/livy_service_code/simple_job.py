from pyspark.sql import SparkSession
from pyspark.sql.functions import rand, col

# Create a SparkSession
spark = SparkSession.builder \
    .appName("SimpleSparkJob") \
    .getOrCreate()

# Generate some random numbers
num_rows = 1000
data = spark.range(num_rows).select((rand() * 100).cast("int").alias("number"))

# Filter out numbers greater than 50
filtered_data = data.filter(col("number") <= 50)

# Count occurrences of each number
number_counts = filtered_data.groupBy("number").count()

# Show the result
number_counts.show()

# Stop the SparkSession
spark.stop()
