"""
Testing the MetabaseConnector class defined in metabase.py
"""
import json

from utils import pprint
from metabase import MetabaseConnector


def list_databases(mb_connector: MetabaseConnector):
    databases = json.loads(mb_connector.get_databases().text)
    for db in databases['data']:
        # pprint(db)
        print(db['id'], db['name'], db['updated_at'])


def main():
    metabase_connector = MetabaseConnector()

    # pprint(metabase_connector.get_user_current().text)
    # pprint(metabase_connector.get_databases().text)
    # pprint(metabase_connector.get_database_by_id(2).text)

    # list_databases(metabase_connector)


if __name__ == '__main__':
    main()
