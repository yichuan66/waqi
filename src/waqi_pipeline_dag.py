import waqi_pipeline_jobs as jobs
from waqi_dag_managers import *

def run_dag():
    # managers
    context_manager = WaqiPipelineContextManager()

    download_manager = WaqiDownloadDagManager(
        context_manager.download_output_contract())
        
    jobs.download_raw_waqi_data(
        download_manager.token(),
        download_manager.data_path_output())

    transfrom_manager = WaqiTransformDagManager(
        context_manager.download_output_contract(),
        context_manager.transform_output_contract())

    jobs.filter_incomplete_row(
        transfrom_manager.data_path_input(),
        transfrom_manager.data_path_output())
