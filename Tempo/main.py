"""
Script to POST to Tempo API and update with the latest task details.

Arguments expected are, in order:

- issue_key: str
- time_minutes: int
- start_date: str
- start_time: str
- description: str

https://community.atlassian.com/t5/Jira-questions/What-is-the-simplest-way-to-connect-to-Tempo-API/qaq-p/1280418
"""
import requests
import json
import sys

from credentials import CREDENTIALS


TEMPO_URL = "https://api.tempo.io/core/3/worklogs"


def _make_payload(issue_key: str, time_minutes: int, start_date: str, start_time: str, description: str) -> str:
    """
    Create the payload JSON.
    """
    if not issue_key:
        raise ValueError("issue_key cannot be empty")
    elif time_minutes <= 0:
        raise ValueError("time_minutes must be positive")
    elif not start_date:
        raise ValueError("start_date must be a valid date string")
    elif not start_time:
        raise ValueError("start_time must be a valid time string")

    return json.dumps(
        {
            "issueKey": issue_key,
            "timeSpentSeconds": time_minutes * 60,
            "billableSeconds": time_minutes * 60,
            "startDate": start_date,
            "startTime": start_time,
            "description": description,
            "authorAccountId": CREDENTIALS["account_id"],
            "attributes": []
        }
    )


def main(
    issue_key: str,
    time_minutes: int,
    start_date: str,
    start_time: str,
    description: str
) -> None:
    """"""
    headers = {
        "Authorization": "Bearer " + CREDENTIALS["token"],
        "Content-Type": "application/json"
    }
    payload = _make_payload(
        issue_key=issue_key,
        time_minutes=time_minutes,
        start_date=start_date,
        start_time=start_time,
        description=description
    )
    response = requests.request(
        method="POST",
        url=TEMPO_URL,
        headers=headers,
        data=payload
    )
    print(response.text)
    [print(sys.argv[_]) for _ in range(len(sys.argv))]


if __name__ == "__main__":
    if len(sys.argv) != 6:
        raise ValueError("There was an error retrieving the latest task details.")

    main(
        issue_key=sys.argv[1],
        time_minutes=int(sys.argv[2]),
        start_date=sys.argv[3],
        start_time=sys.argv[4],
        description=sys.argv[5]
    )
