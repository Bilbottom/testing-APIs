"""
API clients for Twilio.
"""

import requests
import os

import dotenv

dotenv.load_dotenv()


###
# https://stackoverflow.com/questions/26745462/how-do-i-use-basic-http-authentication-with-the-python-requests-library
###


class TwilioConnector:
    """
    Bridge class for the Twilio REST API.
    """

    def __init__(self):
        """
        Create the connector.
        """
        self.base_url = (
            f"https://taskrouter.twilio.com/v1/Workspaces/{os.getenv('WORKSPACE')}/"
        )
        self._auth = (os.getenv("KEY"), os.getenv("SECRET"))

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @property
    def auth(self) -> tuple:
        """Make auth immutable"""
        return self._auth

    def list_all_events(
        self,
        start_datetime: str,
        end_datetime: str,
    ) -> requests.Response:
        """
        https://www.twilio.com/docs/taskrouter/api/event#list-all-events

        Dates must be a string in the ISO-8601 format, e.g. 2020-01-01T00:00:00Z
        """
        endpoint = (
            f"Events?StartDate={start_datetime}&EndDate={end_datetime}&PageSize=100"
        )
        return requests.request(
            method="GET",
            auth=self.auth,
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )
