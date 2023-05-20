from prefect import flow
from etl_flows.pull_taxi_data import pull_data_orchestrator
from etl_flows.transform_taxi_data import transformation_orchestrator
from etl_flows.upload_taxi_data import upload_orchestrator
from notificator import do_notification
from datetime import datetime

@flow(name="elt-orchestration-flow")
def elt_orchestration_flow(taxi_color: str, year: int, months: list):
    """Main ETL flow"""
    notification_block = {
        "flow_name": elt_orchestration_flow.name,
        "description": {"message": f"Fetching: {taxi_color} - {year} - {months}"},
        "status": "started",
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    } # Start
    do_notification(notification_block) 

    for month in months:
        source_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_color}_tripdata_{year}-{month:02}.parquet"
        print(f"fetching: {source_url}")
        df = pull_data_orchestrator(source_url, taxi_color, year, month)
        df_cleaned = transformation_orchestrator(df=df)

        path = f"data/treated/{taxi_color}/{taxi_color}_tripdata_{year}-{month:02}.parquet"
        upload_orchestrator(df=df_cleaned, file_path=path)
    
    notification_block = {
        "flow_name": elt_orchestration_flow.name,
        "status": "finished",
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    } # End
    do_notification(notification_block) 

if __name__ == '__main__':
    elt_orchestration_flow(taxi_color="", years=0, months=[])