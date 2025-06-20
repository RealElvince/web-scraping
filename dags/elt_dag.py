from airflow import  DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

import os 
import sys

from dotenv import load_dotenv
load_dotenv()

PROJECID= os.getenv("PROJECTID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
DATASET_NAME = os.getenv("DATASET_NAME")
TABLE_NAME = os.getenv("TABLE_NAME")

book_ratings = ['One', 'Two', 'Three', 'Four', 'Five']

sys.path.append("/opt/airflow")
from elt.web_scrape import web_scraping




# Function to perform web scraping
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

   

    load_to_gcs_task = LocalFilesystemToGCSOperator(
    
       task_id='load_to_gcs',
       src='data/books.csv',
       dst='books/books.csv',
       bucket=BUCKET_NAME,
       mime_type='text/csv',
       gcp_conn_id='gcp_default',
       gzip=False,
    )
       

    load_to_bigquery_task = GCSToBigQueryOperator(
        task_id='load_to_bigquery',
        bucket=BUCKET_NAME,
        source_objects=['books/books.csv'],
        destination_project_dataset_table=f"{PROJECID}.{DATASET_NAME}.books",
        source_format='CSV',
        skip_leading_rows=1,
        write_disposition='WRITE_TRUNCATE',
        gcp_conn_id='gcp_default',
        allow_jagged_rows=False,
        ignore_unknown_values=True,
        autodetect=True,
        field_delimiter=','
    )

    create_book_rating_tasks = []
    for book_rating in book_ratings:
        create_book_rating_table_task = BigQueryInsertJobOperator(
            task_id=f'create_{book_rating}_star_table',
            configuration={
                "query": {
                    "query": f"""
                        CREATE OR REPLACE TABLE `{PROJECID}.{DATASET_NAME}.{book_rating}_star_table` AS
                        SELECT * FROM `{PROJECID}.{DATASET_NAME}.{TABLE_NAME}`
                        WHERE rating = '{book_rating}';
                    """,
                    "useLegacySql": False,
                }
            },
            gcp_conn_id='gcp_default',
        )

        create_book_rating_tasks.append(create_book_rating_table_task)


for create_book_rating_table_task in create_book_rating_tasks:
    extract_task >> load_to_gcs_task >> load_to_bigquery_task >> create_book_rating_table_task
    
