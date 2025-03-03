"""
Manual testing for the API clients.
"""

import os

import dotenv

import src.utils
from src.apis import jira

dotenv.load_dotenv()


def main() -> None:
    """
    Test the ``JiraConnector`` class.
    """
    jira_connector = jira.JiraConnector(
        domain=os.getenv("ATLASSIAN__DOMAIN"),
        api_key=os.getenv("ATLASSIAN__API_KEY"),
        api_secret=os.getenv("ATLASSIAN__API_SECRET"),
    )
    project_id = "10000"

    src.utils.pprint(jira_connector.get_projects_paginated().text)
    src.utils.pprint(jira_connector.get_issue(issue_key="DEV-67").text)
    src.utils.pprint(jira_connector.get_project_components(project_id=project_id).text)
    src.utils.pprint(
        jira_connector.create_issue(
            project_id=project_id,
            summary="A test from the API",
            description="Some basic description",
        ).text
    )


if __name__ == "__main__":
    main()
