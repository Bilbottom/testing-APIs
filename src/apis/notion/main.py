"""
Manual testing for the API clients.
"""

import notion


def main() -> None:
    """
    Manually test the API client.
    """
    notion_connector = notion.NotionConnector()
    print(notion_connector.get_users().text)


if __name__ == "__main__":
    main()
