"""
Manual testing for the API clients.
"""

import os

import dotenv

from src import utils
from src.apis import confluence

dotenv.load_dotenv()


def main() -> None:
    """
    Manually test the API client.
    """
    confluence_connector = confluence.ConfluenceConnector(
        domain=os.getenv("ATLASSIAN__DOMAIN"),
        api_key=os.getenv("ATLASSIAN__API_KEY"),
        api_secret=os.getenv("ATLASSIAN__API_SECRET"),
    )

    utils.pprint(confluence_connector.get_spaces().text)

    cql = """(space=DEV AND type=page AND creator.fullname~"Bill")&limit=500"""
    utils.pprint(confluence_connector.search_content_by_cql(cql=cql).text)


if __name__ == "__main__":
    main()
