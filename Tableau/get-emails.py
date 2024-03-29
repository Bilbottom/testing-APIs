"""
Script for retrieving the list of emails for users on the server.
"""
import json

from tableau import TableauConnector


def get_user_email_list(tableau_connector: TableauConnector) -> list:
    """
    Get the emails for the licenced users.
    """
    return [
        user["email"]
        for user in json.loads(tableau_connector.get_users_on_site().text)["users"]["user"]
        if user["siteRole"] != "Unlicensed"
    ]


def main() -> None:
    """"""
    tableau_conn = TableauConnector()
    [
        print(email)
        for email in get_user_email_list(tableau_conn)
        if email != "tableau@jajafinance.com"
    ]


if __name__ == "__main__":
    main()
