from prefect import flow
from etl_flows.pull_taxi_data import pull_data_orchestrator
from etl_flows.transform_taxi_data import transformation_orchestrator
from etl_flows.upload_taxi_data import upload_orchestrator


@flow(name="elt-orchestration-flow")
def elt_orchestration_flow(taxi_color: str, years: list, months: list):
    """Main ETL flow"""
    for year in years:
        for month in months:
            source_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_color}_tripdata_{year}-{month:02}.parquet"
            print(f"fetching: {source_url}")
            df = pull_data_orchestrator(source_url, taxi_color, year, month)
            df_cleaned = transformation_orchestrator(df=df)

            path = f"data/treated/{taxi_color}/{taxi_color}_tripdata_{year}-{month:02}.parquet"
            upload_orchestrator(df=df_cleaned, file_path=path)
