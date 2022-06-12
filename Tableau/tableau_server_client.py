"""
Following the documentation at
    https://tableau.github.io/server-client-python/docs

Dependencies
    * TSC (Tableau Server Client)
        pip install tableauserverclient
"""

import tableauserverclient as tsc
# from credentials import PAT, UAP


class TableauUser(object):
    def __init__(self, key: str, secret: str, auth_type: str = 'pat'):
        """
        Class to facilitate using the TSC package for administrative tasks on Tableau Server

        :param key: the REST API key
        :param secret: the REST API secret
        :param auth_type: 'pat' for Personal Access Token and 'uap' for Username And Password
        """
        if auth_type.lower() == 'pat':
            self._auth = tsc.PersonalAccessTokenAuth(key, secret)
        elif auth_type.lower() == 'uap':
            self._auth = tsc.TableauAuth(key, secret)
        else:
            raise ValueError(
                "Acceptable arguments to auth_type are"
                " 'pat' for Personal Access Token and 'uap' for Username And Password"
            )

        self.server = tsc.Server(r'https://tableau.prod.jaja.finance', use_server_version=True)
        # self.server.auth.sign_in(self._auth)

    # def __del__(self):
    #     self.server.auth.sign_out()

    def list_datasources(self):
        """Example method to test the class"""
        with self.server.auth.sign_in(self._auth):
            all_datasources, pagination_item = self.server.datasources.get()
            print(f'\nThere are {pagination_item.total_available} datasources on site:')
            print([datasource.name for datasource in all_datasources])

    def list_workbooks(self):
        """Example method to test the class"""
        with self.server.auth.sign_in(self._auth):
            all_workbooks, pagination_item = self.server.workbooks.get()
            print(f'\nThere are {pagination_item.total_available} workbooks on site:')
            print([workbook.name for workbook in all_workbooks])
