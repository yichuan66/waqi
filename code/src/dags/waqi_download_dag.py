import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys, os
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))
from waqi_dag_managers import *
from waqi_pipeline_jobs import *

# DAG Parameters
args = {
    'owner': 'airflow',
    'start_date': datetime.datetime(2019, 10, 8, 9),
    'email_on_failure' : True,
    'email_on_retry' : True,
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
    'email': ['bbbbcd351@gmail.com'],
}

dag = DAG(
    dag_id='download_waqi_data',
    default_args=args,
    schedule_interval='5 * * * *',
)

# DAG Definition
context_manager = WaqiPipelineContextManager()

download_manager = WaqiDownloadDagManager(
    context_manager.download_output_contract())

task = PythonOperator(
    task_id='waqi_download_task',
    python_callable=download_raw_waqi_data,
    op_kwargs=
    {
        "token" : download_manager.token(), 
        "output_path" : download_manager.data_path_output()
    },
    dag=dag,
)
