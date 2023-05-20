from prefect.blocks.webhook import Webhook
import asyncio


def do_notification(payload: str):
    """Notification with discord via webhook"""
    webhook_block = Webhook.load("discord-notificator")
    payload_formatted = {"content": str(payload)}
    asyncio.run(webhook_block.call(payload_formatted))