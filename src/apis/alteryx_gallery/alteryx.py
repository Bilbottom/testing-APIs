"""
API clients for Alteryx Gallery.
"""

import os

import dotenv
import requests

# extends `requests` to include OAuth 1.0a (One-Legged)
from requests_oauthlib import OAuth1Session

dotenv.load_dotenv(dotenv_path=".env")


class GalleryConnector(object):
    """
    Bridge class for the Alteryx Gallery REST API.
    """

    def __init__(self):
        self.base_url = "http://172.28.67.186/api/"
        self._api_key = os.getenv("KEY")
        self._api_secret = os.getenv("SECRET")

    @property
    def request_headers(self) -> dict:
        """
        Set up the default headers into a dictionary.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @property
    def oauth_1(self) -> OAuth1Session:
        """
        Get the OAuth1 session.
        """
        return OAuth1Session(
            client_key=self._api_key,
            client_secret=self._api_secret,
        )

    def get_shared_credentials(self) -> requests.Response:
        """
        http://172.28.67.186/api-docs/#!/user-workflowsV2.json/GetSharedCredentialsGET
        """
        endpoint = "user/v2/credentials"
        return self.oauth_1.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def enqueue(self, workflow_id: str) -> requests.Response:
        """
        http://172.28.67.186/api-docs/#!/user-workflowsV2.json/EnqueuePOST
        """
        endpoint = f"user/v2/workflows/{workflow_id}/jobs"
        return self.oauth_1.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )
