from airflow.decorators import dag
from airflow.providers.amazon.aws.operators.emr import EmrServerlessStartJobOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from pendulum import datetime

# ------------------------------
# CONFIGS
# ------------------------------
S3_BUCKET_CONFIG = "cjmm-mds-lake-configs"
S3_BUCKET_INPUT = "cjmm-mds-lake-raw"

EMR_APPLICATION_ID = "{{ var.value.emr_serverless_application_id }}"
EMR_EXECUTION_ROLE_ARN = "{{ var.value.emr_serverless_execution_role_arn }}"
S3_EXPRESS_WAREHOUSE = "{{ var.value.s3_express_warehouse }}"  # Exemplo: s3://bucket-express/zone-az1

NAMESPACE = "emr_serverless_exemplo"
TABLE_NAME = "stg_sales_s3express"

ENTRYPOINT_SCRIPT = f"s3://{S3_BUCKET_CONFIG}/scripts/emr/emr_csv_to_iceberg_s3express.py"
INPUT_CSV = f"s3://{S3_BUCKET_INPUT}/sales/amazon.csv"


# ------------------------------
# DAG
# ------------------------------
@dag(
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=['emr-serverless', 'iceberg', 's3-express', 'spark', 'etl']
)
def dag_emr_serverless_csv_to_iceberg_s3express():

    start = EmptyOperator(task_id="start")

    # ------------------------------
    # EMR JOB
    # ------------------------------
    emr_job = EmrServerlessStartJobOperator(
        task_id="run_csv_to_iceberg_s3express",
        application_id=EMR_APPLICATION_ID,
        execution_role_arn=EMR_EXECUTION_ROLE_ARN,

        job_driver={
            "sparkSubmit": {
                "entryPoint": ENTRYPOINT_SCRIPT,
                "entryPointArguments": [
                    INPUT_CSV,
                    S3_EXPRESS_WAREHOUSE,
                    NAMESPACE,
                    TABLE_NAME
                ],
                "sparkSubmitParameters": (
                    "--conf spark.executor.cores=4 "
                    "--conf spark.executor.memory=8g "
                    "--conf spark.driver.cores=2 "
                    "--conf spark.driver.memory=4g "
                )
            }
        },

        configuration_overrides={
            "monitoringConfiguration": {
                "s3MonitoringConfiguration": {
                    "logUri": f"s3://{S3_BUCKET_CONFIG}/logs/emr-serverless/"
                },
                "cloudWatchLoggingConfiguration": {
                    "enabled": True,
                    "logGroupName": "/aws/emr-serverless/data-handson-mds-spark-dev"
                }
            }
        },

        aws_conn_id="aws_default",
        wait_for_completion=True,
    )

    end = EmptyOperator(task_id="end")

    start >> emr_job >> end


dag_emr_serverless_csv_to_iceberg_s3express()
