"""
Script for retrieving the list of emails for users on the server
"""
from tableau import TableauConnector
import json


def get_user_email_list(tableau_connector: TableauConnector) -> list:
    user_list = json.loads(tableau_connector.get_users_on_site().text)['users']['user']
    return [user['email'] for user in user_list if user['siteRole'] != 'Unlicensed']


if __name__ == '__main__':
    tableau_conn = TableauConnector()
    [print(email) for email in get_user_email_list(tableau_conn) if email != 'tableau@jajafinance.com']
