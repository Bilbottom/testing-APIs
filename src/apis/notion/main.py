"""
Manual testing for the API clients.
"""

from src.apis import notion


def main() -> None:
    """
    Manually test the API client.
    """
    notion_connector = notion.NotionConnector()
    print(notion_connector.get_users().text)


if __name__ == "__main__":
    main()
