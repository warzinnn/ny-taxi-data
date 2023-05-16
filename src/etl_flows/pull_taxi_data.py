import pandas as pd
from prefect import flow, task
from prefect_gcp import GcsBucket
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(name="get-taxi-files", cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1), retries=3)
def download_data(source_url: str):
    """Task download raw data"""
    df = pd.read_csv(source_url, encoding='utf-8', engine='python')
    return df

@task(name="upload-raw-file-to-gcs", cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def write_to_gcs(df, path_name: str) -> None:
    """Task to save raw data into GCS"""
    gcs_bucket = GcsBucket.load("ny-taxi-gcs-bucket")
    gcs_bucket.upload_from_dataframe(df=df, to_path=path_name, serialization_format='csv_gzip')
    
@flow(name="pull-taxi-data", log_prints=True)
def pull_data_orchestrator(source_url: str, taxi_color: str, year: int, month: int):
    df = download_data(source_url)
    write_to_gcs(df, f'data/raw/{taxi_color}/{taxi_color}_tripdata_{year}-{month:02}.csv.gz')
    return df




