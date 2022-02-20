from email.policy import default
import os
import logging
from typing import Any
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# gcp related modules
from google.cloud import storage
# from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

# read/write data locally
import pyarrow.csv as pv
import pyarrow.parquet as pq


# ENV
PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
LOCAL_HOME_PATH = os.environ.get('AIRFLOW_HOME', 'opt/airflow')

# dataset
BASE_URL = 'https://s3.amazonaws.com/nyc-tlc/trip+data'


def csv2pq(input_file_path:str, output_file_path:str):
    """Convert csv file to parquet format"""
    if not input_file_path.endswith('csv'):
        logging.error('Input file should be csv files')
        return
    if not output_file_path.endswith('parquet'):
        logging.error('Output file should be parquet files')
        return
    df = pv.read_csv(input_file_path)
    pq.write_table(df, output_file_path)

def upload_data_local_gcs(bucket:str, object_name:str, local_file_path:str):
    """
    Load data from local to GCS
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python

    Parameters:
    -----------
    bucket (str): GCS bucket nam
    object_name (str): target path/file_name in GCS
    local_file_name (str): source file path from local

    Returns:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file_path)

def data_processing_pipeline(
    dag,
    csv_file_url,
    local_csv_file_path,
    local_pq_file_path,
    gcs_file_path):

    with dag:

        # extract data from s3
        extract_data_from_s3 = BashOperator(
            task_id='extract_data_from_s3',
            bash_command=f'curl -sSL {csv_file_url} > {local_csv_file_path}'
        )

        # transform data format
        transform_data_format = PythonOperator(
            task_id='transform_data_format',
            python_callable=csv2pq,
            op_kwargs={'input_file_path': local_csv_file_path,
                    'output_file_path': local_pq_file_path}
        )

        # load data to GCS
        # ref: https://cloud.google.com/storage/docs/gsutil/commands/cp
        # ERROR: ServiceException: 401 Anonymous caller does not have storage.objects.list access to the Google Cloud Storage bucket
        # this may work if we use Google VM
        # load_data_local_gcs = BashOperator(
        #     task_id='load_data_local_gcs',
        #     bash_command=f'gsutil cp {local_file_pq_path} gs://{GCS_BUCKET}/raw/{file_name_pq}'
        # )

        load_data_local_gcs = PythonOperator(
            task_id='load_data_local_gcs',
            python_callable=upload_data_local_gcs,
            op_kwargs={'bucket': GCS_BUCKET,
                    'object_name': gcs_file_path,
                    'local_file_path': local_pq_file_path}
        )

        rm_local_file = BashOperator(
            task_id='rm_local_file',
            bash_command=f'rm {local_csv_file_path} {local_pq_file_path}'
        )

        extract_data_from_s3 >> transform_data_format >> load_data_local_gcs >> rm_local_file


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1
}

yellow_taxi_dag = DAG(
    dag_id='ingest_s3_local_gcs_yellow_taxi',
    schedule_interval='@monthly',
    default_args=default_args,
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2020, 12, 1),
    catchup=True,
    max_active_runs=3,
    tags=['dtc-de']
)

EXEC_TIME = "{{ execution_date.strftime('%Y-%m') }}"
EXEC_YEAR = "{{ execution_date.strftime('%Y') }}"
print(f'INFO: Execution time: {EXEC_TIME}')
YELLOW_TAXI_FILE_URL = os.path.join(BASE_URL, f'yellow_tripdata_{EXEC_TIME}.csv')
YELLOW_TAXI_CSV_FILE_LOCAL_PATH = os.path.join(LOCAL_HOME_PATH, f'yellow_tripdata_{EXEC_TIME}.csv')
YELLOW_TAXI_PQ_FILE_LOCAL_PATH = YELLOW_TAXI_CSV_FILE_LOCAL_PATH.replace('csv', 'parquet')
YELLOW_TAXI_FILE_GCS_PATH = f'raw/yellow_tripdata/{EXEC_YEAR}/yellow_tripdata_{EXEC_TIME}.parquet'

data_processing_pipeline(
    dag=yellow_taxi_dag,
    csv_file_url=YELLOW_TAXI_FILE_URL,
    local_csv_file_path=YELLOW_TAXI_CSV_FILE_LOCAL_PATH,
    local_pq_file_path=YELLOW_TAXI_PQ_FILE_LOCAL_PATH,
    gcs_file_path=YELLOW_TAXI_FILE_GCS_PATH
)
    


