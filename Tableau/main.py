"""
Testing the TableauConnector class defined in tableau.py
"""
import json

from utils import pprint
from tableau import TableauConnector


def change_objects_owner(tableau_connector: TableauConnector):
    billwallis_id = 'c8294636-5960-45f8-bc0a-1758f202eac6'
    sian_id = '92c5b714-6c29-43db-a34c-a97d18919cc8'

    # Change datasources owner
    # pprint(tableau_connector.query_data_sources().text)
    for datasource in json.loads(tableau_connector.query_data_sources().text)['datasources']['datasource']:
        if datasource['owner']['id'] == billwallis_id:
            # pprint(data_source)
            pprint(
                tableau_connector.update_data_source(
                    datasource_id=datasource['id'],
                    new_owner_id=sian_id
                ).text
            )

    # Change workbooks owner
    # pprint(tableau_connector.query_workbooks_for_user(billwallis_id).text)
    for workbook in json.loads(tableau_connector.query_workbooks_for_user(billwallis_id).text)['workbooks']['workbook']:
        # pprint(workbook)
        pprint(
            tableau_connector.update_workbook(
                workbook_id=workbook['id'],
                new_owner_id=sian_id
            ).text
        )


def change_connection_passwords(tableau_connector: TableauConnector):
    new_password = 'A1a-pB7F7jiP596ngMgj'

    datasource_list = json.loads(tableau_connector.query_data_sources().text)['datasources']['datasource']
    workbook_list = json.loads(tableau_connector.query_workbooks_for_site().text)['workbooks']['workbook']

    # Update datasources
    for datasource in datasource_list:
        if datasource['type'] == 'redshift':
            # pprint(datasource)
            connection_response = tableau_connector.query_data_source_connections(
                datasource_id=datasource['id']
            ).text
            # pprint(connection_response)
            connection_list = json.loads(connection_response)['connections']['connection']
            for connection in connection_list:
                if connection['userName'] == 'tableau':
                    pprint(tableau_connector.update_data_source_connection(
                        datasource_id=datasource['id'],
                        connection_id=connection['id'],
                        new_password=new_password
                    ).text)

    # Update workbooks
    for workbook in workbook_list:
        # pprint(workbook)
        connection_response = tableau_connector.query_workbook_connections(
            workbook_id=workbook['id']
        ).text
        # pprint(connection_response)
        connection_list = json.loads(connection_response)['connections']['connection']
        for connection in connection_list:
            if connection['type'] == 'redshift' and connection['userName'] == 'tableau':
                pprint(tableau_connector.update_workbook_connection(
                    workbook_id=workbook['id'],
                    connection_id=connection['id'],
                    new_password=new_password
                ).text)


def get_user_email_list(tableau_connector: TableauConnector):
    user_list = json.loads(tableau_connector.get_users_on_site().text)['users']['user']
    email_list = [user['email'] for user in user_list if user['siteRole'] != 'Unlicensed']
    pprint(email_list)


def main():
    agency_payments_workbook_id = '60e884e0-2660-44e1-a1b2-56d855d6d91d'  # Just an example
    tableau_connector = TableauConnector()

    # pprint(tableau_connector.query_data_sources().text)
    # pprint(tableau_connector.query_workbooks_for_site().text)
    # pprint(tableau_connector.query_workbook_connections(agency_payments_workbook_id).text)
    #
    # pprint(tableau_connector.get_users_on_site().text)
    # pprint(tableau_connector.update_workbook_now(workbook_id=agency_payments_workbook_id).text)
    # pprint(tableau_connector.query_workbook_connections(workbook_id=agency_payments_workbook_id).text)
    #
    # change_objects_owner(tableau_connector)
    # change_connection_passwords(tableau_connector)
    # get_user_email_list(tableau_connector)


if __name__ == '__main__':
    main()
