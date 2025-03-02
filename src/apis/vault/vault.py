"""
API clients for HashiCorp Vault.
"""

import requests
import json
import os


class VaultConnector:
    """
    Bridge class for the HashiCorp Vault REST API.
    """

    def __init__(self):
        """
        Create the connector.
        """
        self.base_url = "https://vault.prod.jaja.finance:8200/v1/"
        self._api_key = os.getenv("KEY")
        self._api_secret = os.getenv("SECRET")

        self._auth_token = None
        sign_in_response = self.sign_in()
        self._auth_token = json.loads(sign_in_response.text)["auth"]["client_token"]

    @property
    def auth_token(self) -> str:
        """Make auth_type immutable"""
        return self._auth_token

    @property
    def request_headers(self) -> dict:
        """
        Set up the default headers into a dictionary.
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
                "X-Vault-Token": self.auth_token,
            }

    def sign_in_userpass(self) -> requests.Response:
        """
        https://www.vaultproject.io/api-docs/auth/userpass

        We use LDAP rather than Username & Password.
        """
        endpoint = f"auth/userpass/login/{self._api_key}"
        body = {
            "password": self._api_secret,
        }
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    def sign_in(self) -> requests.Response:
        """
        https://www.vaultproject.io/api-docs/auth/ldap
        """
        endpoint = f"auth/ldap/login/{self._api_key}"
        body = {
            "password": self._api_secret,
        }
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    def list_roles(self) -> requests.Response:
        """
        https://www.vaultproject.io/api-docs/auth/ldap
        """
        endpoint = "database/roles"
        return requests.request(
            method="LIST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def list_secrets(self, secret_path: str) -> requests.Response:
        """
        https://www.vaultproject.io/api-docs/secret/kv/kv-v2#list-secrets
        """
        endpoint = f"secret/metadata/{secret_path}"
        return requests.request(
            method="LIST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def list_connections(self) -> requests.Response:
        """
        https://www.vaultproject.io/api/secret/databases#list-connections
        """
        endpoint = "database/config"
        return requests.request(
            method="LIST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def read_secret(self, role_name: str) -> requests.Response:
        """ """
        endpoint = f"database/static-creds/{role_name}"
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )
