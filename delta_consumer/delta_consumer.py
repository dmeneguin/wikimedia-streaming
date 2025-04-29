from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

from delta import configure_spark_with_delta_pip

# Define Delta-compatible Spark session
builder = SparkSession.builder \
    .appName("KafkaToDelta") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
# Define schema of JSON messages
schema = StructType() \
    .add("id", IntegerType()) \
    .add("name", StringType()) \
    .add("event_time", StringType())

# Read from Kafka
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "delta-stream") \
    .option("startingOffsets", "earliest") \
    .option("kafka.group.id", "my_custom_consumer_group_id") \
    .load()

# Parse JSON
df_parsed = df_kafka.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# Write to Delta
query = df_parsed.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/app/delta-checkpoint") \
    .start("/app/delta_table")

query.awaitTermination()
