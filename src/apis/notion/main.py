"""
Manual testing for the API clients.
"""

import os

import dotenv

from src import utils
from src.apis import notion

dotenv.load_dotenv()


def main() -> None:
    """
    Manually test the API client.
    """
    notion_connector = notion.NotionConnector(
        api_token=os.getenv("NOTION__API_TOKEN"),
    )
    utils.pprint(notion_connector.get_users().json())


if __name__ == "__main__":
    main()
