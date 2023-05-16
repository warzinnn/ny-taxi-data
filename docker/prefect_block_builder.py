from prefect.filesystems import GitHub
from prefect_gcp import GcsBucket, GcpCredentials
from dotenv import dotenv_values
import json


def create_github_block():
    """Creating Github block in Prefect"""
    block = GitHub(repository="https://github.com/warzinnn/ny-taxi-data")
    block.get_directory("src/etl_flows")
    block.save("ny-taxi-repository")


def create_gcp_credentials_block():
    """Creating GCP Credentials block in Prefect
    - using python-dotenv to access google credentials file
        GOOGLE_CREDS=<PATH_TO_JSON>
    """
    config = dotenv_values(".env")
    with open(config["GOOGLE_CREDS"]) as creds:
        service_account_info = json.load(creds)

    GcpCredentials(service_account_info=service_account_info).save(
        "ny-taxi-service-account"
    )


def create_gcs_bucket_block():
    """Creating GCS Bucket block in Prefect"""
    gcp_credentials = GcpCredentials.load("ny-taxi-service-account")
    gcs_bucket = GcsBucket(
        bucket="data_lake_ny_taxi_ny-taxi-data-project-386814",
        gcp_credentials=gcp_credentials,
    ).save("ny-taxi-gcs-bucket")


if __name__ == "__main__":
    create_github_block()
    create_gcp_credentials_block()
    create_gcs_bucket_block()
