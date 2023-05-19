from etl_flows.etl_orchestration_flow import elt_orchestration_flow
from dbt_flows.dbt_orchestration_flow import dbt_orchestrator
from prefect import flow
from prefect.blocks.webhook import Webhook
import asyncio
from datetime import datetime


def do_notification(payload: str):
    """Notification with discord via webhook"""
    webhook_block = Webhook.load("discord-notificator")
    payload_formatted = {"content": str(payload)}
    asyncio.run(webhook_block.call(payload_formatted))


@flow(name="orchestration-flow")
def main_orchestrator(years: list[int], months: list[int]):
    """Main flow"""
    notification_block = {
        "flow_name": main_orchestrator.name,
        "sub_flow": [{"flow_name": elt_orchestration_flow.name}],
        "status": "started",
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    do_notification(notification_block)  # Start
    taxi_colors = ['green', 'yellow']
    for color in taxi_colors:
        elt_orchestration_flow(color, years, months)
    
    notification_block = {
        "flow_name": main_orchestrator.name,
        "sub_flow": [{"flow_name": elt_orchestration_flow.name}],
        "status": "finished",
        "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    do_notification(notification_block)  # End

    notification_block = {
        "flow_name": main_orchestrator.name,
        "sub_flow": [{"flow_name": dbt_orchestrator.name}],
        "status": "started",
        "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    do_notification(notification_block)  # Start
    dbt_orchestrator()

    notification_block = {
        "flow_name": main_orchestrator.name,
        "sub_flow": [{"flow_name": dbt_orchestrator.name}],
        "status": "ended",
        "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    do_notification(notification_block)  # End


if __name__ == "__main__":
    main_orchestrator(
        years=[2020],
        months=[8],
    )
