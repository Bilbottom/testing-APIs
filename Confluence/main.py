"""
Testing the ``ConfluenceConnector`` class defined in ``confluence.py``.
"""
import json

from utils import pprint
from confluence import ConfluenceConnector


BILLWALLIS_ID = "5f60829fcc17bd006f03f1fd"
BILLWALLIS_SPACE_ID = "977666054"
ANALYTICS_SPACE_ID = "1185742862"


def main() -> None:
    """
    Test the ``ConfluenceConnector`` class.
    """
    confluence_connector = ConfluenceConnector()

    pprint(confluence_connector.get_spaces().text)
    pprint(confluence_connector.search_content_by_cql(
        cql='(space=AO AND type=page AND creator.fullname~"Bill")&limit=500'
    ).text)


if __name__ == "__main__":
    main()
