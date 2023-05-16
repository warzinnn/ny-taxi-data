from prefect import flow
from pull_taxi_data import pull_data_orchestrator
from transform_taxi_data import transformation_orchestrator
from upload_taxi_data import upload_orchestrator


@flow(name="orchestration-flow")
def main_orchestration_flow(taxi_color: str, years: list, months: list):
    """Main ETL flow"""
    for year in years:
        for month in months:
            source_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{taxi_color}/{taxi_color}_tripdata_{year}-{month:02}.csv.gz"
            print(f"fetching: {source_url}")
            df = pull_data_orchestrator(source_url, taxi_color, year, month)
            df_cleaned = transformation_orchestrator(df=df)

            path = f"data/treated/{taxi_color}/{taxi_color}_tripdata_{year}-{month:02}.parquet"
            upload_orchestrator(df=df_cleaned, file_path=path)


if __name__ == "__main__":
    main_orchestration_flow(taxi_color="yellow", years=[2020], months=[7])
