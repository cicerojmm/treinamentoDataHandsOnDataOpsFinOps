#!/bin/bash

# Set your S3 bucket name
S3_BUCKET="cjmm-mds-lake-configs"

# Set Spark version
SPARK_VERSION="3.5"
SCALA_VERSION="2.12"

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
mkdir -p $TEMP_DIR/jars

# Download JAR files - versões compatíveis com EMR Serverless 7.0.0
#curl -L https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/2.20.160/bundle-2.20.160.jar -o $TEMP_DIR/jars/awssdk-bundle-2.20.160.jar
#curl -L https://repo1.maven.org/maven2/software/amazon/awssdk/s3tables/2.29.59/s3tables-2.29.52.jar -o $TEMP_DIR/jars/s3tables-2.29.59.jar
#curl -L https://repo1.maven.org/maven2/software/amazon/s3tables/s3-tables-catalog-for-iceberg/0.1.3/s3-tables-catalog-for-iceberg-0.1.3.jar -o $TEMP_DIR/jars/s3-tables-catalog-for-iceberg-0.1.3.jar
#curl -L https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-${SPARK_VERSION}_${SCALA_VERSION}/1.5.2/iceberg-spark-runtime-${SPARK_VERSION}_${SCALA_VERSION}-1.5.2.jar -o $TEMP_DIR/jars/iceberg-spark-runtime-${SPARK_VERSION}_${SCALA_VERSION}-1.5.2.jar
curl -L https://repo1.maven.org/maven2/org/apache/commons/commons-configuration2/2.11.0/commons-configuration2-2.11.0.jar -o $TEMP_DIR/jars/commons-configuration2-2.11.0.jar
curl -L https://repo1.maven.org/maven2/commons-logging/commons-logging/1.2/commons-logging-1.2.jar -o $TEMP_DIR/jars/commons-logging-1.2.jar

# Upload JAR files to S3
aws s3 cp $TEMP_DIR/jars s3://$S3_BUCKET/jars/emr_serverless/ --recursive

# Clean up temporary directory
rm -rf $TEMP_DIR

echo "JAR files downloaded and uploaded to S3 bucket: $S3_BUCKET/jars/"
