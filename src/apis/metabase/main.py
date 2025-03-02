"""
Testing the ``MetabaseConnector`` class defined in ``metabase.py``.
"""

import json

import src.utils
from src.apis import metabase


def list_databases(mb_connector: metabase.MetabaseConnector) -> None:
    """
    List all databases defined in Metabase.
    """
    databases = json.loads(mb_connector.get_databases().text)
    for db in databases["data"]:
        src.utils.pprint(db)
        print(db["id"], db["name"], db["updated_at"])


def main() -> None:
    """
    Manually test the API client.
    """
    metabase_connector = metabase.MetabaseConnector()

    src.utils.pprint(metabase_connector.get_user_current().text)
    src.utils.pprint(metabase_connector.get_databases().text)
    src.utils.pprint(metabase_connector.get_database_by_id(2).text)

    list_databases(metabase_connector)


if __name__ == "__main__":
    main()
