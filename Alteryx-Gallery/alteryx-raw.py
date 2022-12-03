"""
Class (alternative) to facilitate working with the Alteryx Gallery REST API:

- https://help.alteryx.com/developer-help/gallery-api-overview
"""
import math
import os
import re
import time
import uuid

import requests
import json
import oauthlib.oauth1
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")


class GalleryConnector(object):
    """
    Bridge between Python and the Alteryx Gallery REST API.
    """
    def __init__(self):
        self.base_url = "http://172.28.67.186/api/"
        self._api_key = os.getenv("KEY")
        self._api_secret = os.getenv("SECRET")

    @property
    def oauth_timestamp(self) -> str:
        """Example: 1637748738"""
        return str(int(math.floor(time.time())))

    @property
    def oauth_signature_method(self) -> str:
        return "HMAC-SHA1"

    @property
    def oauth_consumer_key(self) -> str:
        return self._api_key

    @property
    def oauth_version(self) -> str:
        """Optional"""
        return "1.0"

    @property
    def oauth_nonce(self) -> str:
        """
        Example: GeZ1v

        Just a random string that will be used only once. For more info, see:

        - https://stackoverflow.com/a/40328464/8213085
        """
        return uuid.uuid4().hex + uuid.uuid1().hex

    @property
    def oauth_signature(self) -> str:
        """
        Example: 6PT9ZnqXRfLCwp37NrFbVzRUZHg%3D

        Use oauthlib.oauth1 to get the oauth_signature in the response header,
        then parse out the oauth_signature value. This uses ``HMAC-SHA1`` by
        default.
        """
        client = oauthlib.oauth1.Client(
            client_key=self._api_key,
            client_secret=self._api_secret
        )
        return re.search(
            'oauth_signature="(.*)"',
            client.sign("http://172.28.67.186/api")[1]["Authorization"]
        )[1]

    @property
    def oauth_params(self) -> dict:
        return {
            "oauth_timestamp": self.oauth_timestamp,
            "oauth_signature_method": self.oauth_signature_method,
            "oauth_consumer_key": self.oauth_consumer_key,
            "oauth_version": self.oauth_version,
            "oauth_nonce": self.oauth_nonce,
            "oauth_signature": self.oauth_signature,
        }

    @property
    def request_headers(self) -> dict:
        """
        Set up the default headers into a dictionary.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f'OAuth '
                             f'oauth_consumer_key="{self.oauth_consumer_key}",'
                             f'oauth_signature_method="{self.oauth_signature_method}",'
                             f'oauth_signature="{self.oauth_signature}",'
                             f'oauth_timestamp="{self.oauth_timestamp}",'
                             f'oauth_nonce="{self.oauth_nonce}"'
        }

    def get_credentials(self) -> requests.Response:
        endpoint = "user/v2/credentials"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )
