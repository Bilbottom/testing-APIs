"""
API clients for Slack.

https://api.slack.com/messaging/webhooks
"""

from src.apis.slack.connector import SlackConnector

__all__ = [
    "SlackConnector",
]
