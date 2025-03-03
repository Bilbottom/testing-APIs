"""
Manual testing for the API clients.
"""

import os

import dotenv

import src.utils
from src.apis import braze

dotenv.load_dotenv()

BASE_URL = "https://rest.fra-01.braze.eu/"
API_KEYS = {
    "test": os.getenv("BRAZE__TEST__API_KEY"),
    "jaja": os.getenv("BRAZE__JAJA__API_KEY"),
    "boi": os.getenv("BRAZE__BOI__API_KEY"),
    "aa": os.getenv("BRAZE__AA__API_KEY"),
}


def main() -> None:
    """
    Manually test the API client.
    """
    brand = "jaja"
    braze_connector = braze.BrazeConnector(
        base_url=BASE_URL,
        brand=brand,
        api_key=API_KEYS[brand],
    )

    # Campaign list
    src.utils.pprint(braze_connector.get_campaigns_list().text)

    # User Export by Identifier
    user_export_body = {
        "external_ids": [
            "100194",
            "635844",
            "NotInODS_100102",
            "PayB_575974",
            "Jaja_105",
        ],
        "fields_to_export": [
            "external_id",
            "braze_id",
            "campaigns_received",
            "custom_attributes",
            "custom_events",
        ],
    }
    src.utils.pprint(
        braze_connector.user_profile_export_by_identifier(body=user_export_body).text
    )

    # User Export by Segment
    jaja_segment = "7a09f4c1-0f7a-4dfc-8dec-bba78c73d5c9"
    src.utils.pprint(
        braze_connector.user_profile_export_by_segment(segment_id=jaja_segment).text
    )


if __name__ == "__main__":
    main()
