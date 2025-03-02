"""
API clients for Jira.

Note that:

- the ``KEY`` should be your email address for your Atlassian account
- the ``SECRET`` should be a token that you generate for your Atlassian account

See the following documentation:

- https://id.atlassian.com/manage-profile/security/api-tokens
"""

import base64
import os

import dotenv
import requests
import json

dotenv.load_dotenv()


class JiraConnector:
    """
    Bridge class for the Jira REST API.
    """

    def __init__(self):
        """
        Create the connector.
        """
        self.base_url = "https://billiam.atlassian.net/rest/api/3/"
        self._api_key = os.getenv("KEY")
        self._api_secret = os.getenv("SECRET")

    @property
    def auth_basic(self) -> str:
        """
        Encode the key and secret following the Atlassian documentation:

        - https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/#supply-basic-auth-headers
        """
        return (
            "Basic "
            + base64.b64encode(
                f"{self._api_key}:{self._api_secret}".encode("UTF-8")
            ).decode()
        )

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self.auth_basic,
        }

    def get_projects_paginated(self) -> requests.Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/#api-rest-api-3-project-search-get
        """
        endpoint = "project/search"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            params={"maxResults": 50},
        )

    def get_issue(self, issue_key: str) -> requests.Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-get
        """
        endpoint = f"issue/{issue_key}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data={},
        )

    def get_project_components(self, project_id: str) -> requests.Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-components/#api-rest-api-3-project-projectidorkey-components-get
        """
        endpoint = f"project/{project_id}/components"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data={},
        )

    def create_issue(
        self, project_id: str, summary: str, description: str
    ) -> requests.Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post

        For help with Jira IDs, either use the corresponding GET method, or see:

        - https://jaja.atlassian.net/wiki/spaces/AO/pages/2441904132/Jira+API+Guide
        """
        endpoint = "issue"
        payload = json.dumps(
            {
                "update": {},
                "fields": {
                    "summary": summary,
                    "issuetype": {
                        "id": "10001"  # Task
                    },
                    # "components": [
                    #     {
                    #         "id": "10114"  # Analytics
                    #     }
                    # ],
                    "project": {"id": project_id},
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"text": description, "type": "text"}],
                            }
                        ],
                    },
                    # "priority": {
                    #     "id": "3"  # P3 - Medium
                    # },
                    "labels": [],
                    "duedate": None,  # eg "2022-01-01"
                    # "assignee": {
                    #     "id": None  # Unassigned
                    # },
                },
            }
        )
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=payload,
        )
