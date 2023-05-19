import pandas as pd
from prefect import flow, task
from prefect_gcp import GcsBucket


@task(name="get-taxi-files", retries=3)
def download_data(source_url: str):
    """Task to download raw data"""
    if source_url.endswith(".parquet"):
        df = pd.read_parquet(source_url)
    else:
        df = pd.read_csv(source_url, engine="python", encoding="utf-8")
    return df


@task(name="upload-raw-file-to-gcs")
def write_to_gcs(df, path_name: str, serialization_format: str) -> None:
    """Task to save raw data into GCS"""
    gcs_bucket = GcsBucket.load("ny-taxi-gcs-bucket")
    gcs_bucket.upload_from_dataframe(
        df=df, to_path=path_name, serialization_format=serialization_format
    )


@flow(name="pull-taxi-data", log_prints=True)
def pull_data_orchestrator(source_url: str, taxi_color: str, year: int, month: int):
    df = download_data(source_url)
    if source_url.endswith(".parquet"):
        write_to_gcs(
            df,
            f"data/raw/{taxi_color}/{taxi_color}_tripdata_{year}-{month:02}.parquet",
            "parquet_gzip",
        )
    else:
        write_to_gcs(
            df,
            f"data/raw/{taxi_color}/{taxi_color}_tripdata_{year}-{month:02}.csv.gz",
            "csv_gzip",
        )
    return df
