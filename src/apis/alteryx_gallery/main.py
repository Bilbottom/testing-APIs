"""
Manual testing for the API clients.
"""

# from src.apis.alteryx_gallery import alteryx_alt as connector
from src.apis.alteryx_gallery import connector
from src.utils import pprint


def main() -> None:
    """
    Manually test the API client.
    """
    alteryx_server_usage_report_id = "61923e7325d33410083f8932"
    gallery_connector = connector.GalleryConnector()
    pprint(gallery_connector.get_shared_credentials().text)
    pprint(gallery_connector.enqueue(workflow_id=alteryx_server_usage_report_id).text)


if __name__ == "__main__":
    main()
