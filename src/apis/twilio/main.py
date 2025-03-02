"""
Manual testing for the API clients.
"""

import src.utils
from src.apis import twilio


def main():
    """
    Manually test the API client.
    """
    twilio_connector = twilio.TwilioConnector()

    src.utils.pprint(
        twilio_connector.list_all_events(
            start_datetime="2021-11-29T00:00:00Z",
            end_datetime="2021-11-29T23:59:59Z",
        ).text
    )


if __name__ == "__main__":
    main()
