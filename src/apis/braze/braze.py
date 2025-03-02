"""
API clients for Braze.
"""

import os

import requests
import json
import dotenv

dotenv.load_dotenv(dotenv_path=".env")

BRANDS = [
    "test",
    "jaja",
    "boi",
    "aa",
]


class BrazeConnector:
    """
    Bridge class for the Braze REST API.
    """

    def __init__(self, brand: str):
        """
        Create the connector.
        """
        self.base_url = "https://rest.fra-01.braze.eu/"
        self.brand = brand.lower().strip()

        if self.brand not in BRANDS:
            raise ValueError(f"Brand must be one of {BRANDS}")

        self.api_keys = {
            "test": os.getenv("TEST_KEY"),
            "jaja": os.getenv("JAJA_KEY"),
            "boi": os.getenv("BOI_KEY"),
            "aa": os.getenv("AA_KEY"),
        }

    @property
    def request_headers(self) -> dict:
        """Set up the default headers into a dictionary"""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_keys[self.brand]}",
        }

    def get_campaigns_list(self, page: int = 0) -> requests.Response:
        """
        https://www.braze.com/docs/api/endpoints/export/campaigns/get_campaigns/
        """
        endpoint = f"campaigns/list?page={page}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def user_profile_export_by_identifier(self, body: dict) -> requests.Response:
        """
        https://www.braze.com/docs/api/endpoints/export/user_data/post_users_identifier/
        """
        endpoint = "users/export/ids"
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    def user_profile_export_by_segment(self, segment_id: str) -> requests.Response:
        """
        https://www.braze.com/docs/api/endpoints/export/user_data/post_users_segment/
        """
        endpoint = "users/export/segment"
        body = {
            "segment_id": segment_id,
            "fields_to_export": [
                "external_id",
                "braze_id",
                "campaigns_received",
                "custom_attributes",
                "custom_events",
            ],
        }
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )
