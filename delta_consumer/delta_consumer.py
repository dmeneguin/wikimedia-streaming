from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, TimestampType

from delta import configure_spark_with_delta_pip

builder = SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Create a Delta table
data = spark.range(0, 5)
data.write.format("delta").save("/tmp/delta-table")

# Read data from the Delta table
df = spark.read.format("delta").load("/tmp/delta-table")
df.show()






# spark = SparkSession.builder.appName("Kafka2Delta").getOrCreate()

# deltaPath = "file:///tmp/delta/table"

# df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "kafka:29092").option("subscribe", "test").option("startingOffsets", "earliest").option("failOnDataLoss", "false").load().selectExpr("CAST(value AS STRING) as value")

# query = df.writeStream.format("delta").option("checkpointLocation", "/path/to/sparkCheckpoint").start(deltaPath)

# query.awaitTermination()

# # Define Delta-compatible Spark session
# spark = SparkSession.builder \
#     .appName("KafkaToDelta") \
#     .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,io.delta:delta-core_2.12:2.4.0") \
#     .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
#     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
#     .getOrCreate()

# # Define schema of JSON messages
# schema = StructType() \
#     .add("id", IntegerType()) \
#     .add("name", StringType()) \
#     .add("event_time", StringType())

# # Read from Kafka
# df_kafka = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "kafka:29092") \
#     .option("subscribe", "delta-stream") \
#     .option("startingOffsets", "earliest") \
#     .load()

# # Parse JSON
# df_parsed = df_kafka.selectExpr("CAST(value AS STRING) as json") \
#     .select(from_json(col("json"), schema).alias("data")) \
#     .select("data.*")

# # Write to Delta
# query = df_parsed.writeStream \
#     .format("delta") \
#     .outputMode("append") \
#     .option("checkpointLocation", "/tmp/delta-checkpoint") \
#     .start("/tmp/delta-table")

# query.awaitTermination()


# from pyspark.sql import SparkSession


# def main():
#     # Initialize SparkSession
#     spark = SparkSession.builder \
#         .appName("HelloWorld") \
#         .getOrCreate()

#     # Create an RDD containing numbers from 1 to 1000
#     numbers_rdd = spark.sparkContext.parallelize(range(1, 1000))

#     # Count the elements in the RDD
#     count = numbers_rdd.count()

#     print(f"Count of numbers from 1 to 1000 is: {count}")

#     # Stop the SparkSession
#     spark.stop()


# if __name__ == "__main__":
#     main()