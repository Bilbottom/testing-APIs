"""
Manual testing for the API clients.
"""

import json
import os

import dotenv

from src import utils
from src.apis import metabase

dotenv.load_dotenv()

BASE_URL = "http://localhost:3000/api/"


def list_databases(mb_connector: metabase.MetabaseConnector) -> None:
    """
    List all databases defined in Metabase.
    """
    databases = json.loads(mb_connector.get_databases().json())
    for db in databases["data"]:
        utils.pprint(db)
        print(db["id"], db["name"], db["updated_at"])


def main() -> None:
    """
    Manually test the API client.
    """
    metabase_connector = metabase.MetabaseConnector(
        base_url=BASE_URL,
        api_key=os.getenv("METABASE__API_KEY"),
        api_secret=os.getenv("METABASE__API_SECRET"),
    )

    utils.pprint(metabase_connector.get_user_current().json())
    utils.pprint(metabase_connector.get_databases().json())
    utils.pprint(metabase_connector.get_database_by_id(2).json())

    list_databases(metabase_connector)


if __name__ == "__main__":
    main()
