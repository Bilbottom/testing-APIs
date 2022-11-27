"""
https://developers.notion.com/
"""
import notion


def main():
    notion_connector = notion.NotionConnector()
    print(notion_connector.get_users().text)


if __name__ == "__main__":
    main()
