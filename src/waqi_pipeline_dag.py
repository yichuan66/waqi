import waqi_pipeline_jobs as jobs
from waqi_pipeline_manager import WaqiPipelineManager

def run_dag():
    # job pipeline
    pipeline_manager = WaqiPipelineManager()

    jobs.download_raw_waqi_data(
        pipeline_manager.token(),
        pipeline_manager.data_path_downloaded())

    jobs.filter_incomplete_row(
        pipeline_manager.data_path_downloaded(),
        pipeline_manager.data_path_cleaned())
