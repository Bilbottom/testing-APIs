"""
Manual testing for the API clients.
"""

import src.utils
from src.apis import confluence

BILLWALLIS_ID = "5f60829fcc17bd006f03f1fd"
BILLWALLIS_SPACE_ID = "977666054"
ANALYTICS_SPACE_ID = "1185742862"


def main() -> None:
    """
    Manually test the API client.
    """
    confluence_connector = confluence.ConfluenceConnector()

    src.utils.pprint(confluence_connector.get_spaces().text)
    src.utils.pprint(
        confluence_connector.search_content_by_cql(
            cql='(space=AO AND type=page AND creator.fullname~"Bill")&limit=500'
        ).text
    )


if __name__ == "__main__":
    main()
