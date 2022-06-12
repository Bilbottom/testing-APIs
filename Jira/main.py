"""
Testing the JiraConnector class defined in jira.py
"""
import json

from jira import JiraConnector


def pprint(json_text: str or dict):
    if type(json_text) is str:
        json_text = json.loads(json_text)

    try:
        print(
            json.dumps(
                json_text,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
        )
    except TypeError:
        print(json_text)


def main():
    jira_connector = JiraConnector()
    project_id = '10000'

    # pprint(jira_connector.get_projects_paginated().text)
    # pprint(jira_connector.get_issue(issue_key='DEV-67').text)
    # pprint(jira_connector.get_project_components(project_id=project_id).text)
    # pprint(
    #     jira_connector.create_issue(
    #         project_id=project_id,
    #         summary='A test from the API',
    #         description='Some basic description'
    #     ).text
    # )


if __name__ == '__main__':
    main()
