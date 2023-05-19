from prefect_gcp import GcsBucket
from prefect import flow, task
from prefect_gcp import GcpCredentials
import tempfile


@task(name="upload-treated-file-to-gcs", log_prints=True)
def write_treated_data_to_gcs(df, file_path: str):
    """Task to save treated data into GCS"""
    print("file_path: ", file_path)
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = file_path.split("/")[-1]
        temp_file_path = f"{tmpdirname}/{file_name}"
        df.to_parquet(temp_file_path)

        gcs_bucket = GcsBucket.load("ny-taxi-gcs-bucket")
        gcs_bucket.upload_from_path(from_path=temp_file_path, to_path=file_path)
    return df


@task(name="upload-dataframe-to-bq")
def write_data_from_gcs_to_bq(df, color: str) -> None:
    """Task to send dataframe to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("ny-taxi-service-account")
    df.to_gbq(
        destination_table=f"nytaxi_bq.{color}-taxi-data",
        project_id="ny-taxi-data-project-386814",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=100000,
        if_exists="append",
    )


@flow(name="upload-orchestrator")
def upload_orchestrator(df, file_path):
    color = file_path.split("/")[2]
    df = write_treated_data_to_gcs(df, file_path)
    write_data_from_gcs_to_bq(df, color)
