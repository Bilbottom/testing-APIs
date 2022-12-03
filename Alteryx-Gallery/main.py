"""
Testing the GalleryConnector class defined in ``alteryx.py``.
"""
from alteryx import GalleryConnector
from utils import pprint


def main() -> None:
    """
    Test the ``GalleryConnector`` class.
    """
    alteryx_server_usage_report_id = "61923e7325d33410083f8932"
    gallery_connector = GalleryConnector()
    pprint(gallery_connector.get_shared_credentials().text)
    pprint(gallery_connector.enqueue(workflow_id=alteryx_server_usage_report_id).text)


if __name__ == '__main__':
    main()
