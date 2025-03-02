"""
API clients for Tableau.

https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref.htm
"""

from src.apis.tableau.connector import TableauConnector

__all__ = [
    "TableauConnector",
]
