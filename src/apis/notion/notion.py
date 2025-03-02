"""
API clients for Notion.
"""

import os

import dotenv
import requests


dotenv.load_dotenv(dotenv_path=r".env")


class NotionConnector:
    """
    Bridge class for the Notion REST API.
    """

    def __init__(self):
        """
        Create the connector.
        """
        self._base_url = "https://api.notion.com/v1/"
        self._notion_version = "2022-06-28"
        self._token = os.getenv("NOTION_TOKEN")

    @property
    def auth_basic(self) -> str:
        """
        Encode the key and secret following the Notion documentation:

        - https://developers.notion.com/reference/authentication
        """
        return f"Bearer {self._token}"

    @property
    def request_headers(self) -> dict:
        """
        Set up the default headers into a dictionary.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Notion-Version": self._notion_version,
            "Authorization": self.auth_basic,
        }

    def get_users(self) -> requests.Response:
        """
        https://developers.notion.com/reference/get-users
        """
        endpoint = "users"
        print(self._base_url + endpoint)
        return requests.request(
            method="GET",
            url=self._base_url + endpoint,
            headers=self.request_headers,
        )
