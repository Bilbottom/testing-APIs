"""
Class to facilitate working with the Metabase API
    * https://www.metabase.com/docs/v0.41/api-documentation.html

Note that:
    * the KEY should be your username for your Metabase account
    * the SECRET should be your password for your Metabase account
"""
import contextlib
import json
import os

import requests
from dotenv import load_dotenv


load_dotenv(dotenv_path=r'.env')
KEY = os.getenv('KEY')
SECRET = os.getenv('SECRET')


class MetabaseConnector(object):
    def __init__(self):
        self.base_url = 'http://localhost:3000/api/'
        self.__api_key = KEY
        self.__api_secret = SECRET
        self.__auth_token = None

        sign_in_response = self.sign_in()
        # print(sign_in_response.text)
        self.__auth_token = json.loads(sign_in_response.text)['id']

    def __del__(self):
        with contextlib.suppress(ImportError):
            self.sign_out()

    @property
    def auth_token(self) -> str:
        """Make auth_token immutable"""
        return self.__auth_token

    @property
    def request_headers(self) -> dict:
        """Set up the default headers into a dictionary"""
        if self.auth_token is None:
            return {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        else:
            return {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Metabase-Session': self.auth_token
            }

    ###
    # Authentication Methods
    ###
    def sign_in(self) -> requests.Response:
        """
        https://www.metabase.com/docs/latest/api-documentation.html#post-apisession
        """
        endpoint = 'session'
        body = {
            'username': self.__api_key,
            'password': self.__api_secret
        }
        return requests.request(
            method='POST',
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body)
        )

    def sign_out(self) -> requests.Response:
        """
        https://www.metabase.com/docs/latest/api-documentation.html#delete-apisession
        """
        endpoint = 'session'
        return requests.request(
            method='DELETE',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )

    ###
    # Database Methods
    ###
    def get_databases(self) -> requests.Response:
        """
        https://www.metabase.com/docs/v0.41/api-documentation.html#get-apidatabase
        """
        endpoint = 'database'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )

    def get_database_by_id(self, database_id: int or str) -> requests.Response:
        """
        https://www.metabase.com/docs/v0.41/api-documentation.html#get-apidatabaseid
        """
        endpoint = f'database/{database_id}'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )

    ###
    # User Methods
    ###
    def get_user_current(self) -> requests.Response:
        """
        https://www.metabase.com/docs/latest/api-documentation.html#get-apiusercurrent
        """
        endpoint = 'user/current'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )
