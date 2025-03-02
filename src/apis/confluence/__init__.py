"""
API clients for Confluence.

https://developer.atlassian.com/cloud/confluence/rest/intro/
"""

from .confluence import ConfluenceConnector

__all__ = [
    "ConfluenceConnector",
]
