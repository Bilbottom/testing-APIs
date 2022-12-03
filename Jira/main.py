"""
Testing the ``JiraConnector`` class defined in ``jira.py``.
"""
import json

from utils import pprint
from jira import JiraConnector


def main() -> None:
    """
    Test the ``JiraConnector`` class.
    """
    jira_connector = JiraConnector()
    project_id = "10000"

    pprint(jira_connector.get_projects_paginated().text)
    pprint(jira_connector.get_issue(issue_key="DEV-67").text)
    pprint(jira_connector.get_project_components(project_id=project_id).text)
    pprint(
        jira_connector.create_issue(
            project_id=project_id,
            summary="A test from the API",
            description="Some basic description",
        ).text
    )


if __name__ == "__main__":
    main()
