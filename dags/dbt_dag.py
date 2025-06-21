from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dbt_data_pipeline',
    default_args=default_args,
    description='dbt data pipeline',
    tags=['dbt'],
    catchup=False,
    schedule=None
) as dag:

    dbt_project_dir = '/opt/airflow/dbt'
    dbt_profiles_dir = '/opt/airflow/.dbt'

    dbt_debug = BashOperator(
        task_id='dbt_debug',
        bash_command=f'dbt debug --project-dir {dbt_project_dir} --profiles-dir {dbt_profiles_dir}',
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f'dbt run --project-dir {dbt_project_dir} --profiles-dir {dbt_profiles_dir}',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f'dbt test --project-dir {dbt_project_dir} --profiles-dir {dbt_profiles_dir}',
    )

    dbt_debug >> dbt_run >> dbt_test

   