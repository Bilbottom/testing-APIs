"""
API clients for Confluence.

https://developer.atlassian.com/cloud/confluence/rest/intro/
"""

from src.apis.confluence.connector import ConfluenceConnector

__all__ = [
    "ConfluenceConnector",
]
