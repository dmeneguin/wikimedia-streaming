# # Use a base image with Python
# FROM python:3.9-slim

# # Install Java (Spark requires Java)
# RUN apt-get update && apt-get install -y default-jre wget tar

# # Download and install Apache Spark
# ENV SPARK_VERSION=3.4.1
# RUN wget https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz \
#     && tar -xzf spark-$SPARK_VERSION-bin-hadoop3.tgz -C /opt \
#     && ln -s /opt/spark-$SPARK_VERSION-bin-hadoop3 /opt/spark \
#     && rm spark-$SPARK_VERSION-bin-hadoop3.tgz

# # Set Spark environment variables
# ENV SPARK_HOME=/opt/spark
# ENV PATH=$SPARK_HOME/bin:$PATH

# COPY requirements.txt .

# # Install PySpark
# RUN pip install -r requirements.txt

# # Copy your Spark application Python script
# COPY delta_consumer.py /opt/spark/delta_consumer.py

# # Set the default command to run the Spark application
# CMD ["spark-submit", "/opt/spark/delta_consumer.py"]

#FROM spark:3.5.1-scala2.12-java17-ubuntu
# FROM spark:3.5.1-scala2.12-java17-python3-ubuntu
# USER root
# RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# # RUN set -ex; \
# #     rm -rf /var/lib/apt/lists/*
# # Install PySpark and Delta Lake
# COPY . .
# RUN pip install -r requirements.txt
# USER spark
# # Add PySpark to PATH for the spark user
# ENV PATH=$PATH:/home/spark/.local/bin
# ENV JAVA_HOME=/opt/java/openjdk
# ENV SPARK_VERSION=3.5
# ENV PYSPARK_PYTHON=3.10.12
# ENV SPARK_PACKAGES="\
# org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
# org.apache.kafka:kafka-clients:3.6.0 \
# org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.5.1"

# RUN mkdir -p /opt/spark/jars

# RUN for pkg in $SPARK_PACKAGES; do \
#     url="https://repo1.maven.org/maven2/$(echo $pkg | \
#         awk -F: '{gsub(/\./, "/", $1); print $1"/"$2"/"$3"/"$2"-"$3".jar"}')"; \
#     echo "Downloading $url"; \
#     curl -fsSL "$url" -o "/opt/spark/jars/$(basename $url)"; \
# done

# ENV SPARK_EXTRA_CLASSPATH=/opt/spark/jars/*

# CMD ["python3", "delta_consumer.py"]

FROM bitnami/spark:3.5.1

# Set environment variables for the Spark packages
ENV PYSPARK_PYTHON=python3 \
    PYSPARK_DRIVER_PYTHON=python3 \
    SPARK_JARS_PACKAGES=\
org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,\
org.apache.kafka:kafka-clients:3.6.0,\
org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.5.1

# Set the working directory
WORKDIR /app

# Copy your PySpark script into the container
COPY . .
RUN pip install -r requirements.txt

# Set the default command to run the PySpark script with the specified packages
CMD [ "spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.kafka:kafka-clients:3.6.0,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.5.1,io.delta:delta-core_2.12:2.4.0", "delta_consumer.py" ]
# CMD [ "spark-submit",\
#       "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.kafka:kafka-clients:3.6.0,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.5.1,io.delta:delta-core_2.12:2.4.0",\
#       "--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension",\
#       "--conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog",\
#       "delta_consumer.py"\
#     ]