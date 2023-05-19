from prefect import flow, task
from prefect_dbt.cli.commands import DbtCoreOperation, DbtCliProfile

DBT_CLI_PROFILE = DbtCliProfile.load("profile-bq-dbt-ny-taxi-prod")


@task(name="setup-dbt_deps", log_prints=True)
def dbt_deps():
    DbtCoreOperation(
        commands=["dbt deps"],
        project_dir="src/dbt_nytaxi/",
        profiles_dir=".dbt-profile/",
        dbt_cli_profile=DBT_CLI_PROFILE,
        overwrite_profiles=True,
    ).run()


@task(name="setup-dbt-seeds", log_prints=True)
def dbt_seeds():
    DbtCoreOperation(
        commands=["dbt seed"],
        project_dir="src/dbt_nytaxi/",
        profiles_dir=".dbt-profile/",
        dbt_cli_profile=DBT_CLI_PROFILE,
        overwrite_profiles=True,
    ).run()


@task(name="execute-dbt-build", log_prints=True)
def dbt_run():
    DbtCoreOperation(
        commands=["dbt build -t prod --vars is_test: false"],
        project_dir="src/dbt_nytaxi/",
        profiles_dir=".dbt-profile/",
        dbt_cli_profile=DBT_CLI_PROFILE,
        overwrite_profiles=True,
    ).run()


@flow(name="dbt-orchestration-flow")
def dbt_orchestrator():
    """DBT orchestrator flow"""
    dbt_deps()
    dbt_seeds()
    dbt_run()
