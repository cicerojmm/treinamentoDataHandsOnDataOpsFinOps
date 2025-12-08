import sys
from pyspark.sql import SparkSession

def main():
    if len(sys.argv) != 5:
        print("Usage: emr_csv_to_iceberg_s3express.py <input_csv_path> <s3express_warehouse> <namespace> <table_name>")
        sys.exit(1)

    input_path = sys.argv[1]
    warehouse = sys.argv[2]
    namespace = sys.argv[3]
    table_name = sys.argv[4]

    spark = SparkSession.builder \
        .appName("CSV to Iceberg S3 Express") \
        .getOrCreate()

    print(f"Reading CSV from: {input_path}")
    df = spark.read.option("header", "true").option("inferSchema", "true").csv(input_path)

    print(f"Schema: {df.schema}")
    print(f"Row count: {df.count()}")

    full_table_name = f"glue_catalog.{namespace}.{table_name}"
    print(f"Writing to Iceberg table: {full_table_name}")

    df.writeTo(full_table_name).using("iceberg").createOrReplace()

    print(f"Successfully wrote data to {full_table_name}")
    spark.stop()

if __name__ == "__main__":
    main()
