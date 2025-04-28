FROM bitnami/spark:3.5.1

# Set environment variables for the Spark packages
ENV PYSPARK_PYTHON=python3 \
    PYSPARK_DRIVER_PYTHON=python3

# Set the working directory
WORKDIR /app
RUN mkdir -p /app/delta_table /app/checkpoint

# Copy your PySpark script into the container
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the PySpark script with the specified packages
CMD [ "spark-submit", "--packages", "io.delta:delta-spark_2.12:3.1.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.kafka:kafka-clients:3.6.0,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.5.1", "delta_consumer.py" ]
