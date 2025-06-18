from airflow import  DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

import os 
import sys


sys.path.append("/opt/airflow")
from elt.web_scrape import web_scraping


def perform_web_scraping():
    web_scraping()
    print("Web scraping completed successfully.")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'elt_data_pipeline',
    default_args=default_args,
    description='A simple ELT data pipeline',
    tags=['elt', 'web_scraping'],
    catchup=False,
    schedule=None
) as dag:
    
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=perform_web_scraping,
    )

extract_task