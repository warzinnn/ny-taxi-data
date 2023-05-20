from dbt_flows.dbt_orchestration_flow import dbt_deps, dbt_run, dbt_seeds
from notificator import do_notification
from prefect import flow
from datetime import datetime

@flow(name="dbt-orchestration-flow")
def dbt_orchestrator():
    """DBT orchestrator flow"""
    notification_block = {
        "flow_name": dbt_orchestrator.name,
        "status": "started",
        "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    do_notification(notification_block)  # Start

    dbt_deps()
    dbt_seeds()
    dbt_run()

    notification_block = {
        "flow_name": dbt_orchestrator.name,
        "status": "ended",
        "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    do_notification(notification_block)  # End

if __name__ == "__main__":
    dbt_orchestrator()
