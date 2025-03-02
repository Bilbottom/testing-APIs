"""
Class to facilitate working with the Tableau Server REST API:

- https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref.htm
"""

import contextlib
import json
import os

import dotenv
import requests

dotenv.load_dotenv()

API_VERSION = "3.8"
URL = f"https://tableau.prod.jaja.finance/api/{API_VERSION}/"


class TableauConnector:
    def __init__(self, auth_type: str = "uap"):
        self.base_url = URL
        self._auth_type = auth_type.lower()
        if self.auth_type == "pat":
            self.credentials = [os.getenv("PAT_KEY"), os.getenv("PAT_SECRET")]
        elif self.auth_type == "uap":
            self.credentials = [os.getenv("UAP_KEY"), os.getenv("UAP_SECRET")]
        else:
            raise ValueError(
                "Acceptable arguments to auth_type are"
                " 'pat' for Personal Access Token and 'uap' for Username And Password"
            )

        self._auth_token = None
        _sign_in_response = self.sign_in()
        # pprint(_sign_in_response.text)
        self._site_id = json.loads(_sign_in_response.text)["credentials"]["site"]["id"]
        self._auth_token = json.loads(_sign_in_response.text)["credentials"]["token"]
        self._user_id = json.loads(_sign_in_response.text)["credentials"]["user"]["id"]

    def __del__(self):
        with contextlib.suppress(ImportError):
            self.sign_out()

    @property
    def auth_type(self) -> str:
        """Make auth_type immutable"""
        return self._auth_type

    @property
    def auth_token(self) -> str:
        """Make auth_token immutable"""
        return self._auth_token

    @property
    def site_id(self) -> str:
        """Make site_id immutable"""
        return self._site_id

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """
        if self.auth_token is None:
            return {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        else:
            return {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Tableau-Auth": self.auth_token,
            }

    ###
    # Authentication Methods
    ###
    def sign_in(self) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_authentication.htm#sign_in
        """
        endpoint = "auth/signin"
        if self.auth_type == "pat":
            body = {
                "credentials": {
                    "personalAccessTokenName": self.credentials[0],
                    "personalAccessTokenSecret": self.credentials[1],
                    "site": {
                        "contentUrl": "",
                    },
                }
            }
        else:
            body = {
                "credentials": {
                    "name": self.credentials[0],
                    "password": self.credentials[1],
                    "site": {
                        "contentUrl": "",
                    },
                }
            }

        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    def sign_out(self) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_authentication.htm#sign_out
        """
        endpoint = "auth/signout"
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    ###
    # Users and Groups Methods
    ###
    def get_users_on_site(self) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_users_and_groups.htm#get_users_on_site
        """
        endpoint = f"sites/{self.site_id}/users?fields=_all_&pageSize=1000"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def query_user_on_site(self, user_id: str) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_users_and_groups.htm#query_user_on_site
        """
        endpoint = f"sites/{self.site_id}/users/{user_id}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    ###
    # Data Sources Methods
    ###
    def query_data_source_connections(self, datasource_id: str) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm#query_data_source_connections
        """
        endpoint = f"sites/{self.site_id}/datasources/{datasource_id}/connections"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def query_data_sources(self) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm#query_data_sources
        """
        endpoint = f"sites/{self.site_id}/datasources?pageSize=1000"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def update_data_source_connection(
        self,
        datasource_id: str,
        connection_id: str,
        new_password: str,
    ) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm#update_data_source_connection

        Only set up to change the password.
        """
        endpoint = f"sites/{self.site_id}/datasources/{datasource_id}/connections/{connection_id}"
        body = {
            "connection": {
                "password": new_password,
                "embedPassword": "True",
            }
        }
        return requests.request(
            method="PUT",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    def update_data_source_now(self, datasource_id: str) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm#update_data_source_now
        """
        endpoint = f"sites/{self.site_id}/datasources/{datasource_id}/refresh"
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data="{}",
        )

    def update_data_source(
        self,
        datasource_id: str,
        new_owner_id: str,
    ) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm#update_data_source

        Currently only set up to change the owner
        """
        endpoint = f"sites/{self.site_id}/datasources/{datasource_id}"
        body = {
            "datasource": {
                "owner": {
                    "id": new_owner_id,
                }
            }
        }
        return requests.request(
            method="PUT",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    ###
    # Workbooks and Views Methods
    ###
    def query_workbook_connections(self, workbook_id: str) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#query_workbook_connections
        """
        endpoint = f"sites/{self.site_id}/workbooks/{workbook_id}/connections"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def query_workbooks_for_site(self) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#query_workbooks_for_site
        """
        endpoint = f"sites/{self.site_id}/workbooks?pageSize=1000"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def query_workbooks_for_user(self, user_id: str) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#query_workbooks_for_user
        """
        endpoint = (
            f"sites/{self.site_id}/users/{user_id}/workbooks?ownedBy=true&pageSize=1000"
        )
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def update_workbook_connection(
        self,
        workbook_id: str,
        connection_id: str,
        new_password: str,
    ) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#update_workbook_connection

        Only set up to change the password.
        """
        endpoint = (
            f"sites/{self.site_id}/workbooks/{workbook_id}/connections/{connection_id}"
        )
        body = {
            "connection": {
                "password": new_password,
                "embedPassword": "True",
            }
        }
        return requests.request(
            method="PUT",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    def update_workbook_now(self, workbook_id: str) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#update_workbook_now
        """
        endpoint = f"sites/{self.site_id}/workbooks/{workbook_id}/refresh"
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data="{}",
        )

    def update_workbook(self, workbook_id: str, new_owner_id: str) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#update_workbook

        Currently only set up to change the owner.
        """
        endpoint = f"sites/{self.site_id}/workbooks/{workbook_id}"
        body = {
            "workbook": {
                "owner": {
                    "id": new_owner_id,
                }
            }
        }
        return requests.request(
            method="PUT",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )
