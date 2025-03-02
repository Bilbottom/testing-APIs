"""
Manual testing for the API clients.
"""

import src.utils
from src.apis import jira


def main() -> None:
    """
    Test the ``JiraConnector`` class.
    """
    jira_connector = jira.JiraConnector()
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
