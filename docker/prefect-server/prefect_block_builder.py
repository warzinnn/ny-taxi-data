""" File to create blocks in Prefect 
Envs:
    GITHUB_REPO=<URL>
    GOOGLE_CREDENTIALS=<PATH_TO_JSON>
    GCS_BUCKET=<NAME>
    WEBHOOK_URL=<URL>

"""
from prefect.filesystems import GitHub
from prefect_gcp import GcsBucket, GcpCredentials
from prefect_dbt.cli import BigQueryTargetConfigs, DbtCliProfile
from prefect.blocks.webhook import Webhook
import os
import json


def create_github_block():
    """Creating Github block in Prefect"""
    print("[+] Creating Github block....")
    block = GitHub(repository=os.environ["GITHUB_REPO"])
    block.get_directory("src")
    block.save("ny-taxi-repository", overwrite=True)


def create_gcp_credentials_block():
    """Creating GCP Credentials block in Prefect
    - using python-dotenv to access google credentials file
        GOOGLE_CREDENTIALS=<PATH_TO_JSON>
    """
    print("[+] Creating GCP Credentials block....")

    service_account_info = json.loads(
        os.environ["GOOGLE_CREDENTIALS"].replace("'", '"')
    )

    GcpCredentials(service_account_info=service_account_info).save(
        "ny-taxi-service-account", overwrite=True
    )


def create_gcs_bucket_block():
    """Creating GCS Bucket block in Prefect"""
    print("[+] Creating GCS Bucket block....")
    gcp_credentials = GcpCredentials.load("ny-taxi-service-account")
    gcs_bucket = GcsBucket(
        bucket=os.environ["GCS_BUCKET"],
        gcp_credentials=gcp_credentials,
    ).save("ny-taxi-gcs-bucket", overwrite=True)


def create_dbt_core_block():
    """Creating dbt CLI blocks for Dtb-Profile and BigQuery"""
    print("[+] dbt CLI blocks for Dtb-Profile and BigQuery (STAG) ....")
    credentials = GcpCredentials.load("ny-taxi-service-account")
    target_configs = BigQueryTargetConfigs(
        schema="dbt_nytaxi_stag",
        credentials=credentials,
    )
    target_configs.save("dbt-core-cli", overwrite=True)

    dbt_cli_profile = DbtCliProfile(
        name="bq-dbt-ny-taxi",
        target="dev",
        target_configs=target_configs,
    )
    dbt_cli_profile.save("profile-bq-dbt-ny-taxi", overwrite=True)


def create_dbt_core_block_prod():
    """Creating dbt CLI blocks for Dtb-Profile and BigQuery"""
    print("[+] Creating dbt CLI blocks for Dtb-Profile and BigQuery (PROD) ....")
    credentials = GcpCredentials.load("ny-taxi-service-account")
    target_configs = BigQueryTargetConfigs(
        schema="dbt_nytaxi_prod",
        credentials=credentials,
    )
    target_configs.save("dbt-core-cli-prod", overwrite=True)

    dbt_cli_profile = DbtCliProfile(
        name="bq-dbt-ny-taxi",
        target="prod",
        target_configs=target_configs,
    )
    dbt_cli_profile.save("profile-bq-dbt-ny-taxi-prod", overwrite=True)


def create_notification_block():
    """Creating webhook block to send notifications to a discord server"""
    print("[+] Creating Webhook block ....")
    webhook_block = Webhook(
        method="POST",
        url=os.environ["WEBHOOK_URL"],
        headers={"content": ""},
    ).save(name="discord-notificator", overwrite=True)


if __name__ == "__main__":
    create_github_block()
    create_gcp_credentials_block()
    create_gcs_bucket_block()
    create_dbt_core_block()
    create_dbt_core_block_prod()
    create_notification_block()
