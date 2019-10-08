import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

import sys, os
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))
from waqi_dag_managers import *
from waqi_pipeline_jobs import *

# DAG Parameters
args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(0),
}

dag = DAG(
    dag_id='waqi_download_dag_id',
    default_args=args,
    schedule_interval=None,
)

# DAG Definition
context_manager = WaqiPipelineContextManager()

download_manager = WaqiDownloadDagManager(
    context_manager.download_output_contract())

task = PythonOperator(
    task_id='waqi_download_task_id',
    python_callable=download_raw_waqi_data,
    op_kwargs=
    {
        "token" : download_manager.token(), 
        "output_path" : download_manager.data_path_output()
    },
    dag=dag,
)
